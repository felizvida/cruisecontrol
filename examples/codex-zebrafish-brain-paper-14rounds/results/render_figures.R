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
overlap_df <- read.csv(file.path(results_dir, "source_table_overlap_metrics.csv"), stringsAsFactors = FALSE)
marker_df <- read.csv(file.path(results_dir, "marker_bias.csv"), stringsAsFactors = FALSE)
axis_df <- read.csv(file.path(results_dir, "axis_summary.csv"), stringsAsFactors = FALSE)
ptm_df <- read.csv(file.path(results_dir, "ptm_summary.csv"), stringsAsFactors = FALSE)
ptm_marker_df <- read.csv(file.path(results_dir, "marker_ptm_summary.csv"), stringsAsFactors = FALSE)

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
    comparison_values <- c(
      metric_value("jaccard_overlap"),
      metric_value("source_table_jaccard_overlap"),
      metric_value("source_table_sorensen_overlap"),
      metric_value("source_table_weighted_jaccard_overlap"),
      metric_value("protein_overlap_fraction")
    )
    comparison_labels <- c(
      "Article\nJaccard",
      "Exact-ID\nJaccard",
      "Exact-ID\nSorensen",
      "Weighted\nJaccard",
      "Protein\noverlap"
    )
    barplot(
      comparison_values,
      names.arg = comparison_labels,
      col = c("#5B8FF9", "#1D39C4", "#91D5FF", "#13C2C2", "#7CB305"),
      ylab = "Similarity / overlap",
      ylim = c(0, max(comparison_values) * 1.25),
      las = 2,
      main = "Overlap metrics across views"
    )
    mtext(
      paste0(
        "Published shared = ", metric_value("shared_proteoforms"),
        " | Exact-ID shared = ", metric_value("source_table_shared_proteoforms")
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

    robustness_values <- c(
      metric_value("marker_alignment_fraction"),
      metric_value("leave_one_out_min_alignment"),
      metric_value("motor_family_exclusion_alignment"),
      metric_value("protein_collapsed_alignment_fraction"),
      metric_value("intensity_alignment_fraction")
    )
    robustness_labels <- c(
      "Observed\ncount panel",
      "Leave-one-out\nminimum",
      "Exclude motor\nfamilies",
      "Protein-\ncollapsed",
      "Intensity-\nweighted"
    )
    barplot(
      robustness_values,
      names.arg = robustness_labels,
      col = c("#5B8FF9", "#9254DE", "#FA8C16", "#36CFC9", "#52C41A"),
      ylim = c(0.85, 1.0),
      ylab = "Matched-region fraction",
      las = 2,
      main = "Robustness across representations"
    )
    abline(h = metric_value("expected_alignment_under_region_prevalence"), lty = 2, col = "gray40")
  },
  width = 10.5,
  height = 4.6,
  copy_name = "fig3_axis_alignment"
)

save_asset_set(
  "ptm_and_sensitivity",
  function() {
    par(mfrow = c(1, 2), mar = c(8, 4, 3, 1) + 0.1, family = "serif")
    ptm_cols <- c("#5B8FF9", "#CB3C33")
    barplot(
      ptm_marker_df$acetylated_fraction,
      names.arg = c("Tel matched\nmarkers", "Teo matched\nmarkers"),
      las = 2,
      col = ptm_cols,
      ylab = "N-terminal acetylation fraction",
      ylim = c(0, max(ptm_marker_df$acetylated_fraction) * 1.25),
      main = "PTM bias within matched markers"
    )
    sensitivity_df <- overlap_df[overlap_df$scenario != "article_reported_counts", ]
    sensitivity_labels <- c(
      source_table_exact_ids = "Exact-ID\nobserved",
      source_table_duplicate_adjusted_shared_fixed = "Chao\nfixed-shared",
      source_table_duplicate_adjusted_scaled_min = "Chao\nscaled-min",
      source_table_duplicate_adjusted_scaled_geomean = "Chao\nscaled-geo",
      source_table_duplicate_adjusted_scaled_max = "Chao\nscaled-max",
      source_table_jackknife1_adjusted_shared_fixed = "Jackknife\nfixed-shared"
    )
    barplot(
      sensitivity_df$jaccard_overlap,
      names.arg = unname(sensitivity_labels[sensitivity_df$scenario]),
      col = c("#1D39C4", "#13C2C2", "#52C41A", "#36CFC9", "#FAAD14", "#9254DE"),
      ylab = "Jaccard overlap",
      ylim = c(0, max(sensitivity_df$jaccard_overlap) * 1.25),
      las = 2,
      main = "Duplicate-informed overlap sensitivity"
    )
  },
  width = 10.5,
  height = 4.8,
  copy_name = "fig4_ptm_and_sensitivity"
)
