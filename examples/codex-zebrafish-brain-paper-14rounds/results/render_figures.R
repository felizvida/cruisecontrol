#!/usr/bin/env Rscript

script_arg <- commandArgs(trailingOnly = FALSE)[grep("^--file=", commandArgs(trailingOnly = FALSE))][1]
script_path <- normalizePath(sub("^--file=", "", script_arg))
root <- normalizePath(file.path(dirname(script_path), ".."))
results_dir <- file.path(root, "results")
assets_dir <- file.path(root, "figure_assets")
figures_dir <- file.path(root, "figures")

dir.create(assets_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(figures_dir, recursive = TRUE, showWarnings = FALSE)

summary_df <- read.csv(file.path(results_dir, "region_summary.csv"), stringsAsFactors = FALSE)
marker_df <- read.csv(file.path(results_dir, "marker_bias.csv"), stringsAsFactors = FALSE)
axis_df <- read.csv(file.path(results_dir, "axis_summary.csv"), stringsAsFactors = FALSE)
loo_df <- read.csv(file.path(results_dir, "leave_one_out_alignment.csv"), stringsAsFactors = FALSE)
ptm_df <- read.csv(file.path(results_dir, "ptm_summary.csv"), stringsAsFactors = FALSE)
tech_df <- read.csv(file.path(results_dir, "technical_replicate_summary.csv"), stringsAsFactors = FALSE)

metric_value <- function(name) {
  as.numeric(summary_df$value[summary_df$metric == name][1])
}

save_asset_set <- function(stem, draw_fun, width = 8, height = 5, copy_name = NULL) {
  subdir <- file.path(assets_dir, stem)
  dir.create(subdir, recursive = TRUE, showWarnings = FALSE)
  pdf_path <- file.path(subdir, paste0(stem, ".pdf"))
  png_path <- file.path(subdir, paste0(stem, ".png"))
  svg_path <- file.path(subdir, paste0(stem, ".svg"))

  cairo_pdf(pdf_path, width = width, height = height, family = "serif")
  draw_fun()
  dev.off()

  png(png_path, width = width, height = height, units = "in", res = 600, family = "serif")
  draw_fun()
  dev.off()

  svg(svg_path, width = width, height = height)
  draw_fun()
  dev.off()

  if (!is.null(copy_name)) {
    file.copy(pdf_path, file.path(figures_dir, paste0(copy_name, ".pdf")), overwrite = TRUE)
    file.copy(png_path, file.path(figures_dir, paste0(copy_name, ".png")), overwrite = TRUE)
  }
}

save_asset_set(
  "region_overview",
  function() {
    par(mfrow = c(1, 2), mar = c(5, 4, 3, 1) + 0.1, family = "serif")
    barplot(
      c(metric_value("telencephalon_proteoforms"), metric_value("optic_tectum_proteoforms")),
      names.arg = c("Telencephalon", "Optic tectum"),
      col = c("#4063D8", "#CB3C33"),
      ylab = "Identified proteoforms",
      main = "Region totals"
    )
    barplot(
      c(metric_value("telencephalon_unique"), metric_value("shared_proteoforms"), metric_value("optic_tectum_unique")),
      names.arg = c("Tel only", "Shared", "Teo only"),
      col = c("#4063D8", "#7F7F7F", "#CB3C33"),
      ylab = "Proteoforms",
      main = "Unique versus shared"
    )
    mtext(
      paste0(
        "Jaccard = ", metric_value("jaccard_overlap"),
        " | Protein overlap = ", metric_value("protein_overlap_fraction")
      ),
      side = 1,
      outer = FALSE,
      line = 4,
      cex = 0.8
    )
  },
  width = 10,
  height = 4.4,
  copy_name = "fig1_region_overview"
)

save_asset_set(
  "marker_bias",
  function() {
    ord <- order(marker_df$log2_tel_over_teo_plus1)
    df <- marker_df[ord, ]
    cols <- ifelse(df$functional_axis == "telencephalon", "#4063D8", "#CB3C33")
    par(mar = c(5, 10, 3, 1) + 0.1, family = "serif")
    plot(
      df$log2_tel_over_teo_plus1,
      seq_len(nrow(df)),
      pch = 19,
      col = cols,
      yaxt = "n",
      ylab = "",
      xlab = expression(log[2]((Tel + 1)/(Teo + 1))),
      main = "Marker-level proteoform bias"
    )
    segments(0, seq_len(nrow(df)), df$log2_tel_over_teo_plus1, seq_len(nrow(df)), col = cols, lwd = 2)
    abline(v = 0, lty = 2, col = "gray40")
    axis(2, at = seq_len(nrow(df)), labels = df$label, las = 2, cex.axis = 0.8)
  },
  width = 8.5,
  height = 6,
  copy_name = "fig2_marker_bias"
)

save_asset_set(
  "axis_alignment",
  function() {
    par(mfrow = c(1, 2), mar = c(5, 5, 3, 1) + 0.1, family = "serif")
    matched <- axis_df$matched_count
    spill <- axis_df$spillover_count
    mat <- rbind(matched, spill)
    colnames(mat) <- c("Tel-associated", "Teo-associated")
    barplot(
      mat,
      beside = FALSE,
      col = c("#2E8B57", "#E69F00"),
      ylab = "Proteoform counts",
      main = "Axis-level concentration"
    )
    legend("topright", legend = c("Matched region", "Spillover"), fill = c("#2E8B57", "#E69F00"), bty = "n", cex = 0.85)

    loo_df <- loo_df[order(loo_df$remaining_alignment_fraction), ]
    barplot(
      loo_df$remaining_alignment_fraction,
      names.arg = loo_df$removed_marker,
      horiz = TRUE,
      las = 1,
      col = "#7A68A6",
      xlim = c(0.9, 1.0),
      xlab = "Alignment after removing one marker",
      main = "Robustness to leave-one-out marker removal"
    )
    abline(v = metric_value("marker_alignment_fraction"), lty = 2, col = "gray40")
  },
  width = 10.5,
  height = 4.6,
  copy_name = "fig3_axis_alignment"
)

save_asset_set(
  "ptm_and_sensitivity",
  function() {
    par(mfrow = c(1, 2), mar = c(8, 4, 3, 1) + 0.1, family = "serif")
    cols <- ifelse(ptm_df$modification %in% c("total_proteoforms", "modified_total", "unmodified"), "#7F7F7F", "#009E73")
    barplot(
      ptm_df$count,
      names.arg = gsub("_", "\n", ptm_df$modification),
      las = 2,
      col = cols,
      ylab = "Proteoforms",
      main = "PTM inventory"
    )
    bar_centers <- barplot(
      tech_df$duplicate_mean,
      names.arg = c("Telencephalon", "Optic tectum"),
      col = c("#4063D8", "#CB3C33"),
      ylab = "Proteoforms per duplicate set",
      main = "Technical sensitivity",
      ylim = c(0, max(tech_df$duplicate_mean + tech_df$duplicate_sd) * 1.25)
    )
    arrows(
      x0 = bar_centers,
      y0 = tech_df$duplicate_mean - tech_df$duplicate_sd,
      x1 = bar_centers,
      y1 = tech_df$duplicate_mean + tech_df$duplicate_sd,
      angle = 90,
      code = 3,
      length = 0.05
    )
    abline(h = metric_value("single_run_high_water_mark"), lty = 2, col = "gray40")
  },
  width = 10.5,
  height = 4.8,
  copy_name = "fig4_ptm_and_sensitivity"
)
