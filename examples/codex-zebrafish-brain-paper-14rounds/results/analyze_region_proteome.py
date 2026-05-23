#!/usr/bin/env python3
"""Compute reproducible summaries for the Codex zebrafish brain paper."""

from __future__ import annotations

import csv
import json
import math
import random
import re
import statistics
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DATA_PATH = DATA_DIR / "curated_evidence.json"
RESULTS_DIR = ROOT / "results"
SOURCE_TABLE_DIR = DATA_DIR / "source_tables"
XLSX_NS = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


ARTICLE_LOCATIONS = {
    "region_totals": (
        "PMC9066772 Results and discussion paragraph reporting 309 telencephalon "
        "proteoforms, 533 optic tectum proteoforms, 35 shared proteoforms, and 60 shared proteins."
    ),
    "marker_panel": (
        "PMC9066772 Results and discussion paragraph listing neuropeptide Y, PENKB, "
        "PYY-A, neurogranin, synucleins, reticulon, myosin, actin, and troponin as "
        "region-linked markers."
    ),
    "ptm_totals": (
        "PMC9066772 Results and discussion paragraph reporting 449 unmodified, "
        "211 N-terminal acetylated, 25 oxidized, 15 disulfide-bonded, 12 methylated, "
        "and 3 phosphorylated proteoforms."
    ),
    "technical_sensitivity": (
        "PMC9066772 discussion around duplicate analyses and the 418-proteoform "
        "single-run high-water mark."
    ),
}

COMPOSITION_SENTINELS = [
    {
        "panel": "glial_support",
        "genes": {"gfap", "s100b"},
        "interpretation": "astroglial support markers",
    },
    {
        "panel": "myelin",
        "genes": {"mbpa", "mbpb"},
        "interpretation": "myelin-associated markers",
    },
    {
        "panel": "housekeeping_translation",
        "genes": {"eef1a", "gapdh-2"},
        "interpretation": "generic abundant translation and glycolysis markers",
    },
    {
        "panel": "microtubule_structural",
        "genes": {"tuba1c", "tubb2b", "nefma"},
        "interpretation": "generic structural/neurofilament markers",
    },
]

TISSUE_SENTINEL_PANELS = [
    {
        "panel": "skeletal_cardiac_muscle",
        "gene_prefixes": ("myh", "myl", "tnn", "ttn", "desm"),
        "description_keywords": (
            "myosin",
            "troponin",
            "titin",
            "desmin",
            "skeletal muscle",
            "cardiac",
            "atrial",
        ),
        "interpretation": "skeletal/cardiac muscle carryover sentinels requested by review",
    },
    {
        "panel": "contractile_cytoskeleton",
        "gene_prefixes": ("act", "myh", "myl", "tnn", "tpm"),
        "description_keywords": ("actin", "myosin", "troponin", "tropomyosin"),
        "interpretation": "contractile and cytoskeletal motor proteins",
    },
    {
        "panel": "neuronal_synaptic",
        "gene_prefixes": ("snap", "stx", "syt", "syn", "nrg", "npy", "penk", "pyy"),
        "description_keywords": (
            "synaptic",
            "synuclein",
            "neurogranin",
            "neuropeptide",
            "vesicle",
            "neuron",
        ),
        "interpretation": "neuronal and synaptic sentinels",
    },
    {
        "panel": "glial_myelin",
        "gene_prefixes": ("mbp", "plp", "mpz", "gfap", "s100", "fabp7"),
        "description_keywords": ("myelin", "glial", "glia", "fatty acid binding protein"),
        "interpretation": "glial and myelin sentinels",
    },
    {
        "panel": "translation_housekeeping",
        "gene_prefixes": ("eef", "rpl", "rps", "gapdh"),
        "description_keywords": ("elongation factor", "ribosomal", "glyceraldehyde"),
        "interpretation": "broad abundant housekeeping sentinels",
    },
]

INDEPENDENT_MARKERS = [
    {
        "gene": "plp1b",
        "label": "PLP1b",
        "functional_axis": "telencephalon",
        "interpretation": "CNS myelin-associated proteolipid marker from adult zebrafish myelin literature.",
    },
    {
        "gene": "mbpa",
        "label": "MBPa",
        "functional_axis": "telencephalon",
        "interpretation": "CNS myelin basic protein marker from adult zebrafish myelin literature.",
    },
    {
        "gene": "mbpb",
        "label": "MBPb",
        "functional_axis": "telencephalon",
        "interpretation": "Paralogous myelin basic protein marker from adult zebrafish myelin literature.",
    },
    {
        "gene": "mpz",
        "label": "MPZ/P0",
        "functional_axis": "telencephalon",
        "interpretation": "Teleost CNS myelin protein zero marker from adult zebrafish myelin literature.",
    },
    {
        "gene": "gfap",
        "label": "GFAP",
        "functional_axis": "optic_tectum",
        "interpretation": "Adult optic tectum radial-glia marker from the PGZ/deep-layer literature.",
    },
    {
        "gene": "fabp7a",
        "label": "FABP7a",
        "functional_axis": "optic_tectum",
        "interpretation": "Adult optic tectum radial-glia marker from the PGZ/deep-layer literature.",
    },
    {
        "gene": "s100b",
        "label": "S100B",
        "functional_axis": "optic_tectum",
        "interpretation": "Adult optic tectum glial marker from the PGZ/deep-layer literature.",
    },
]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def wilson_interval(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return 0.0, 0.0
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    margin = z * math.sqrt((p * (1 - p) + z * z / (4 * n)) / n) / denom
    return max(0.0, center - margin), min(1.0, center + margin)


def hypergeom_prob(a: int, row1: int, col1: int, total: int) -> float:
    return math.comb(col1, a) * math.comb(total - col1, row1 - a) / math.comb(total, row1)


def log_comb(n: int, k: int) -> float:
    if k < 0 or k > n:
        return float("-inf")
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)


def logsumexp(values: list[float]) -> float:
    finite_values = [value for value in values if math.isfinite(value)]
    if not finite_values:
        return float("-inf")
    anchor = max(finite_values)
    return anchor + math.log(sum(math.exp(value - anchor) for value in finite_values))


def hypergeom_log_prob(a: int, row1: int, col1: int, total: int) -> float:
    return log_comb(col1, a) + log_comb(total - col1, row1 - a) - log_comb(total, row1)


def hypergeom_lower_tail_p(a: int, row1: int, col1: int, total: int) -> tuple[float, float]:
    lower = max(0, row1 + col1 - total)
    upper = min(row1, col1)
    if a < lower or a > upper:
        return 0.0, float("inf")
    log_p = logsumexp([hypergeom_log_prob(x, row1, col1, total) for x in range(lower, a + 1)])
    p_value = math.exp(log_p) if log_p > -745 else 0.0
    neg_log10 = -log_p / math.log(10)
    return p_value, neg_log10


def hypergeom_jaccard_summary(row1: int, col1: int, total: int) -> dict[str, float]:
    lower = max(0, row1 + col1 - total)
    upper = min(row1, col1)
    support = list(range(lower, upper + 1))
    log_probs = [hypergeom_log_prob(value, row1, col1, total) for value in support]
    normalizer = logsumexp(log_probs)
    probabilities = [math.exp(value - normalizer) for value in log_probs]
    jaccards = [value / (row1 + col1 - value) for value in support]

    def weighted_quantile(q: float) -> float:
        cumulative = 0.0
        for value, probability in zip(jaccards, probabilities):
            cumulative += probability
            if cumulative >= q:
                return value
        return jaccards[-1]

    return {
        "expected_shared": sum(value * probability for value, probability in zip(support, probabilities)),
        "jaccard_mean": sum(value * probability for value, probability in zip(jaccards, probabilities)),
        "jaccard_low_95": weighted_quantile(0.025),
        "jaccard_high_95": weighted_quantile(0.975),
    }


def fisher_one_sided_greater(a: int, b: int, c: int, d: int) -> float:
    row1 = a + b
    col1 = a + c
    total = a + b + c + d
    max_a = min(row1, col1)
    return sum(hypergeom_prob(x, row1, col1, total) for x in range(a, max_a + 1))


def odds_ratio_with_ci(
    a: int, b: int, c: int, d: int, correction: float = 0.0
) -> tuple[float, float, float]:
    if correction == 0.0 and min(a, b, c, d) == 0:
        correction = 0.5
    ah = a + correction
    bh = b + correction
    ch = c + correction
    dh = d + correction
    odds_ratio = (ah * dh) / (bh * ch)
    se = math.sqrt(1 / ah + 1 / bh + 1 / ch + 1 / dh)
    low = math.exp(math.log(odds_ratio) - 1.96 * se)
    high = math.exp(math.log(odds_ratio) + 1.96 * se)
    return odds_ratio, low, high


def normal_cdf(value: float) -> float:
    return 0.5 * (1 + math.erf(value / math.sqrt(2)))


def dot(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def solve_linear_system(matrix: list[list[float]], vector: list[float]) -> list[float]:
    size = len(vector)
    augmented = [row[:] + [value] for row, value in zip(matrix, vector)]
    for col in range(size):
        pivot = max(range(col, size), key=lambda row_index: abs(augmented[row_index][col]))
        if abs(augmented[pivot][col]) < 1e-12:
            raise ValueError("Singular matrix")
        augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        pivot_value = augmented[col][col]
        for idx in range(col, size + 1):
            augmented[col][idx] /= pivot_value
        for row in range(size):
            if row == col:
                continue
            factor = augmented[row][col]
            if factor == 0:
                continue
            for idx in range(col, size + 1):
                augmented[row][idx] -= factor * augmented[col][idx]
    return [augmented[row][size] for row in range(size)]


def invert_matrix(matrix: list[list[float]]) -> list[list[float]]:
    size = len(matrix)
    inverse_columns = []
    for col in range(size):
        basis = [0.0] * size
        basis[col] = 1.0
        inverse_columns.append(solve_linear_system([row[:] for row in matrix], basis))
    return [[inverse_columns[col][row] for col in range(size)] for row in range(size)]


def logistic_regression(
    design: list[list[float]], response: list[int], ridge: float = 1e-4, max_iter: int = 100
) -> tuple[list[float], list[list[float]], bool]:
    if not design:
        raise ValueError("Empty design matrix")
    feature_count = len(design[0])
    beta = [0.0] * feature_count
    converged = False
    xtwx: list[list[float]] = [[0.0] * feature_count for _ in range(feature_count)]
    for _ in range(max_iter):
        eta = [max(min(dot(row, beta), 30), -30) for row in design]
        probs = [1.0 / (1.0 + math.exp(-value)) for value in eta]
        weights = [max(prob * (1 - prob), 1e-8) for prob in probs]
        z_values = [eta_i + (target - prob) / weight for eta_i, target, prob, weight in zip(eta, response, probs, weights)]
        xtwx = [[0.0] * feature_count for _ in range(feature_count)]
        xtwz = [0.0] * feature_count
        for row, weight, z_value in zip(design, weights, z_values):
            for j in range(feature_count):
                xtwz[j] += weight * row[j] * z_value
                for k in range(feature_count):
                    xtwx[j][k] += weight * row[j] * row[k]
        for idx in range(feature_count):
            xtwx[idx][idx] += ridge
        beta_new = solve_linear_system([row[:] for row in xtwx], xtwz)
        if max(abs(left - right) for left, right in zip(beta_new, beta)) < 1e-8:
            beta = beta_new
            converged = True
            break
        beta = beta_new
    covariance = invert_matrix(xtwx)
    return beta, covariance, converged


def chao2_lower_bound(observed: int, q1: int, q2: int) -> float:
    if q2 > 0:
        return observed + (q1 * q1) / (2 * q2)
    return observed + q1 * (q1 - 1) / 2


def jackknife1_incidence(observed: int, q1: int, sample_count: int = 2) -> float:
    return observed + q1 * (sample_count - 1) / sample_count


def quantile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return 1.0
    position = (len(ordered) - 1) * q
    low = int(math.floor(position))
    high = int(math.ceil(position))
    if low == high:
        return ordered[low]
    fraction = position - low
    return ordered[low] * (1 - fraction) + ordered[high] * fraction


def percentile(values: list[float], q: float) -> float:
    return quantile(values, q)


def weighted_similarity_metrics(
    left: dict[tuple[str, str], float], right: dict[tuple[str, str], float]
) -> tuple[float, float]:
    union_ids = left.keys() | right.keys()
    intersection = sum(min(left.get(pid, 0.0), right.get(pid, 0.0)) for pid in union_ids)
    union = sum(max(left.get(pid, 0.0), right.get(pid, 0.0)) for pid in union_ids)
    total = sum(left.get(pid, 0.0) + right.get(pid, 0.0) for pid in union_ids)
    difference = sum(abs(left.get(pid, 0.0) - right.get(pid, 0.0)) for pid in union_ids)
    return intersection / union, 1 - difference / total


def total_sum_normalize(values: dict[tuple[str, str], float]) -> dict[tuple[str, str], float]:
    total = sum(values.values()) or 1.0
    return {key: value / total for key, value in values.items()}


def upper_quartile_normalize(values: dict[tuple[str, str], float]) -> dict[tuple[str, str], float]:
    scale = quantile([value for value in values.values() if value > 0], 0.75) or 1.0
    return {key: value / scale for key, value in values.items()}


def median_ratio_normalize(
    left: dict[tuple[str, str], float], right: dict[tuple[str, str], float]
) -> tuple[dict[tuple[str, str], float], dict[tuple[str, str], float], float, float]:
    shared_ids = sorted(left.keys() & right.keys())
    ratios: list[tuple[float, float]] = []
    for pid in shared_ids:
        left_value = left[pid]
        right_value = right[pid]
        if left_value > 0 and right_value > 0:
            geomean = math.sqrt(left_value * right_value)
            ratios.append((left_value / geomean, right_value / geomean))
    if not ratios:
        return dict(left), dict(right), 1.0, 1.0
    left_scale = statistics.median(item[0] for item in ratios) or 1.0
    right_scale = statistics.median(item[1] for item in ratios) or 1.0
    return (
        {key: value / left_scale for key, value in left.items()},
        {key: value / right_scale for key, value in right.items()},
        left_scale,
        right_scale,
    )


def parse_shared_strings(workbook: ZipFile) -> list[str]:
    shared_strings: list[str] = []
    if "xl/sharedStrings.xml" not in workbook.namelist():
        return shared_strings
    root = ET.fromstring(workbook.read("xl/sharedStrings.xml"))
    for item in root.findall("a:si", XLSX_NS):
        shared_strings.append("".join(text.text or "" for text in item.iterfind(".//a:t", XLSX_NS)))
    return shared_strings


def load_xlsx_rows(path: Path) -> list[dict[str, str]]:
    with ZipFile(path) as workbook:
        shared_strings = parse_shared_strings(workbook)
        sheet = ET.fromstring(workbook.read("xl/worksheets/sheet1.xml"))
    rows: list[dict[str, str]] = []
    headers: list[str] | None = None
    columns: list[str] | None = None
    for row in sheet.findall(".//a:sheetData/a:row", XLSX_NS):
        cells: list[tuple[str, str]] = []
        for cell in row.findall("a:c", XLSX_NS):
            reference = cell.attrib.get("r", "")
            column = "".join(char for char in reference if char.isalpha())
            value_node = cell.find("a:v", XLSX_NS)
            value = value_node.text if value_node is not None else ""
            if cell.attrib.get("t") == "s" and value:
                value = shared_strings[int(value)]
            cells.append((column, value))
        if not cells:
            continue
        if headers is None:
            columns = [column for column, _ in cells]
            headers = [value for _, value in cells]
            continue
        assert headers is not None and columns is not None
        row_map = {column: value for column, value in cells}
        rows.append({headers[i]: row_map.get(columns[i], "") for i in range(len(columns))})
    return rows


def extract_gene(description: str) -> str:
    match = re.search(r" GN=([^ ]+)", description)
    return match.group(1).lower() if match else ""


def average_intensity(row: dict[str, str]) -> float:
    values = [float(value) for key, value in row.items() if "intensity" in key.lower() and value]
    return sum(values) / len(values) if values else 0.0


def is_acetylated(proteoform: str) -> bool:
    return "[Acetyl]" in proteoform


def canonicalize_proteoform(proteoform: str) -> str:
    cleaned = re.sub(r"\[[^\]]+\]", "", proteoform)
    cleaned = cleaned.replace("(", "").replace(")", "").replace(".", "")
    return re.sub(r"[^A-Z]", "", cleaned)


def proteoform_sequence_core(proteoform: str) -> str:
    parts = proteoform.split(".")
    if len(parts) >= 3:
        return ".".join(parts[1:-1]) if len(parts) > 3 else parts[1]
    return proteoform.strip(".")


def proteoform_modification_tokens(proteoform: str) -> str:
    tokens = re.findall(r"\[([^\]]+)\]", proteoform)
    return ";".join(tokens) if tokens else "none"


def modification_bucket(proteoform: str) -> str:
    tags = re.findall(r"\[([^\]]+)\]", proteoform)
    if not tags:
        return "Unmodified"
    if "Acetyl" in tags:
        return "Acetyl"
    return "Other mass shift"


def load_source_rows(filename: str, region: str) -> list[dict[str, object]]:
    rows = load_xlsx_rows(SOURCE_TABLE_DIR / filename)
    intensity_columns = [key for key in rows[0].keys() if "intensity" in key.lower()]
    intensity_totals = {
        column: sum(float(row[column]) for row in rows if row[column]) for column in intensity_columns
    }
    enriched_rows: list[dict[str, object]] = []
    for index, row in enumerate(rows, start=2):
        description = row["Protein description"]
        proteoform = row["Proteoform"]
        raw_intensities = [float(row[column]) if row[column] else 0.0 for column in intensity_columns]
        relative_intensities = [
            (float(row[column]) / intensity_totals[column]) if row[column] and intensity_totals[column] else 0.0
            for column in intensity_columns
        ]
        enriched_rows.append(
            {
                "region": region,
                "source_table": filename,
                "source_row": index,
                "protein_accession": row["Protein accession"],
                "protein_description": description,
                "description_lower": description.lower(),
                "gene": extract_gene(description),
                "first_residue": row["First residue"],
                "last_residue": row["Last residue"],
                "proteoform": proteoform,
                "precursor_mass": float(row["Precursor mass"]),
                "match_status": row["Match "],
                "avg_intensity": sum(raw_intensities) / len(raw_intensities),
                "avg_relative_intensity": sum(relative_intensities) / len(relative_intensities),
                "run_columns": tuple(intensity_columns),
                "run_intensities": tuple(raw_intensities),
                "run_relative_intensities": tuple(relative_intensities),
                "is_acetylated": is_acetylated(proteoform),
                "canonicalized_proteoform": canonicalize_proteoform(proteoform),
                "proteoform_id": (row["Protein accession"], proteoform),
            }
        )
    return enriched_rows


def aggregate_exact_ids(rows: list[dict[str, object]]) -> dict[tuple[str, str], dict[str, object]]:
    aggregated: dict[tuple[str, str], dict[str, object]] = {}
    for row in rows:
        proteoform_id = row["proteoform_id"]
        if proteoform_id not in aggregated:
            aggregated[proteoform_id] = {
                "region": row["region"],
                "protein_accession": row["protein_accession"],
                "proteoform": row["proteoform"],
                "canonicalized_proteoform": row["canonicalized_proteoform"],
                "first_residue": row["first_residue"],
                "last_residue": row["last_residue"],
                "gene": row["gene"],
                "protein_description": row["protein_description"],
                "precursor_mass": float(row["precursor_mass"]),
                "avg_intensity": float(row["avg_intensity"]),
                "run_intensities": [0.0, 0.0],
            }
        aggregated_row = aggregated[proteoform_id]
        current = aggregated_row["run_intensities"]
        run_values = row["run_intensities"]
        aggregated_row["run_intensities"] = [
            float(current[0]) + float(run_values[0]),
            float(current[1]) + float(run_values[1]),
        ]
    return aggregated


def summarize_detectability(
    aggregated_rows: dict[tuple[str, str], dict[str, object]],
    fallback_detected_at_least_once: float | None = None,
) -> dict[str, float]:
    q1 = 0
    q2 = 0
    for row in aggregated_rows.values():
        detections = sum(1 for value in row["run_intensities"] if float(value) > 0)
        if detections == 1:
            q1 += 1
        elif detections == 2:
            q2 += 1
    exact_id_count = len(aggregated_rows)
    per_run_detection = (2 * q2 / (q1 + 2 * q2)) if (q1 + 2 * q2) else 0.0
    detected_at_least_once = 2 * per_run_detection - per_run_detection * per_run_detection
    fallback_used = 0.0
    if detected_at_least_once == 0.0 and fallback_detected_at_least_once:
        detected_at_least_once = fallback_detected_at_least_once
        per_run_detection = 1.0 - math.sqrt(max(0.0, 1.0 - detected_at_least_once))
        fallback_used = 1.0
    latent_richness = exact_id_count / detected_at_least_once if detected_at_least_once else 0.0
    return {
        "q1": q1,
        "q2": q2,
        "exact_id_count": exact_id_count,
        "per_run_detection": per_run_detection,
        "detected_at_least_once": detected_at_least_once,
        "latent_richness": latent_richness,
        "fallback_used": fallback_used,
    }


def bootstrap_overlap_intervals(
    tel_rows: list[dict[str, object]], teo_rows: list[dict[str, object]], trials: int = 10_000, seed: int = 20260327
) -> tuple[dict[str, object], list[dict[str, object]]]:
    rng = random.Random(seed)
    tel_count = len(tel_rows)
    teo_count = len(teo_rows)
    exact_values: list[float] = []
    canonical_values: list[float] = []
    protein_values: list[float] = []
    weighted_values: list[float] = []
    bray_values: list[float] = []

    for _ in range(trials):
        tel_sample = [tel_rows[rng.randrange(tel_count)] for _ in range(tel_count)]
        teo_sample = [teo_rows[rng.randrange(teo_count)] for _ in range(teo_count)]

        tel_exact_ids = {row["proteoform_id"] for row in tel_sample}
        teo_exact_ids = {row["proteoform_id"] for row in teo_sample}
        tel_canonical_ids = {
            (row["protein_accession"], row["canonicalized_proteoform"]) for row in tel_sample
        }
        teo_canonical_ids = {
            (row["protein_accession"], row["canonicalized_proteoform"]) for row in teo_sample
        }
        tel_proteins = {row["protein_accession"] for row in tel_sample}
        teo_proteins = {row["protein_accession"] for row in teo_sample}

        exact_union = tel_exact_ids | teo_exact_ids
        canonical_union = tel_canonical_ids | teo_canonical_ids
        protein_union = tel_proteins | teo_proteins
        tel_weighted_map: dict[tuple[str, str], float] = {}
        teo_weighted_map: dict[tuple[str, str], float] = {}
        for row in tel_sample:
            key = row["proteoform_id"]
            tel_weighted_map[key] = tel_weighted_map.get(key, 0.0) + float(row["avg_intensity"])
        for row in teo_sample:
            key = row["proteoform_id"]
            teo_weighted_map[key] = teo_weighted_map.get(key, 0.0) + float(row["avg_intensity"])

        exact_values.append(len(tel_exact_ids & teo_exact_ids) / len(exact_union))
        canonical_values.append(len(tel_canonical_ids & teo_canonical_ids) / len(canonical_union))
        protein_values.append(len(tel_proteins & teo_proteins) / len(protein_union))
        weighted_jaccard, bray_curtis = weighted_similarity_metrics(tel_weighted_map, teo_weighted_map)
        weighted_values.append(weighted_jaccard)
        bray_values.append(bray_curtis)

    rows = []
    summary: dict[str, object] = {
        "overlap_bootstrap_trials": trials,
        "overlap_bootstrap_seed": seed,
    }
    metric_specs = [
        (
            "exact_id_jaccard",
            exact_values,
            "Row-bootstrap sensitivity interval for accession+proteoform Jaccard over the released Tel2 and Teo2 tables.",
        ),
        (
            "canonicalized_jaccard",
            canonical_values,
            "Same resampling scheme after canonicalizing proteoform strings for the discrepancy diagnostic.",
        ),
        (
            "protein_overlap_fraction",
            protein_values,
            "Row-bootstrap sensitivity interval after collapsing the released tables to protein accessions.",
        ),
        (
            "weighted_jaccard_overlap",
            weighted_values,
            "Row-bootstrap sensitivity interval for weighted Jaccard using resampled mean duplicate intensities.",
        ),
        (
            "bray_curtis_similarity",
            bray_values,
            "Row-bootstrap sensitivity interval for Bray--Curtis similarity using resampled mean duplicate intensities.",
        ),
    ]
    for metric_name, values, note in metric_specs:
        low = percentile(values, 0.025)
        median = percentile(values, 0.5)
        high = percentile(values, 0.975)
        summary[f"{metric_name}_bootstrap_low"] = round(low, 4)
        summary[f"{metric_name}_bootstrap_median"] = round(median, 4)
        summary[f"{metric_name}_bootstrap_high"] = round(high, 4)
        rows.append(
            {
                "metric": metric_name,
                "bootstrap_trials": trials,
                "low_95": round(low, 4),
                "median": round(median, 4),
                "high_95": round(high, 4),
                "note": note,
            }
        )
    return summary, rows


def build_run_pair_similarity(
    tel_rows: list[dict[str, object]], teo_rows: list[dict[str, object]]
) -> tuple[dict[str, object], list[dict[str, object]]]:
    tel_run_columns = [str(column) for column in tel_rows[0]["run_columns"]]
    teo_run_columns = [str(column) for column in teo_rows[0]["run_columns"]]
    rows: list[dict[str, object]] = []
    weighted_values: list[float] = []
    bray_values: list[float] = []
    relative_weighted_values: list[float] = []
    relative_bray_values: list[float] = []

    for tel_index, tel_label in enumerate(tel_run_columns):
        tel_map = {
            row["proteoform_id"]: float(row["run_intensities"][tel_index])  # type: ignore[index]
            for row in tel_rows
        }
        tel_relative_map = {
            row["proteoform_id"]: float(row["run_relative_intensities"][tel_index])  # type: ignore[index]
            for row in tel_rows
        }
        for teo_index, teo_label in enumerate(teo_run_columns):
            teo_map = {
                row["proteoform_id"]: float(row["run_intensities"][teo_index])  # type: ignore[index]
                for row in teo_rows
            }
            teo_relative_map = {
                row["proteoform_id"]: float(row["run_relative_intensities"][teo_index])  # type: ignore[index]
                for row in teo_rows
            }
            weighted_jaccard, bray_curtis = weighted_similarity_metrics(tel_map, teo_map)
            relative_weighted_jaccard, relative_bray_curtis = weighted_similarity_metrics(
                tel_relative_map, teo_relative_map
            )
            weighted_values.append(weighted_jaccard)
            bray_values.append(bray_curtis)
            relative_weighted_values.append(relative_weighted_jaccard)
            relative_bray_values.append(relative_bray_curtis)
            rows.append(
                {
                    "tel_run": tel_label,
                    "teo_run": teo_label,
                    "weighted_jaccard_overlap": round(weighted_jaccard, 4),
                    "bray_curtis_similarity": round(bray_curtis, 4),
                    "per_run_total_normalized_weighted_jaccard_overlap": round(
                        relative_weighted_jaccard, 4
                    ),
                    "per_run_total_normalized_bray_curtis_similarity": round(relative_bray_curtis, 4),
                }
            )

    summary = {
        "run_pair_weighted_jaccard_min": round(min(weighted_values), 4),
        "run_pair_weighted_jaccard_max": round(max(weighted_values), 4),
        "run_pair_bray_curtis_min": round(min(bray_values), 4),
        "run_pair_bray_curtis_max": round(max(bray_values), 4),
        "run_pair_total_normalized_weighted_jaccard_min": round(min(relative_weighted_values), 4),
        "run_pair_total_normalized_weighted_jaccard_max": round(max(relative_weighted_values), 4),
        "run_pair_total_normalized_bray_curtis_min": round(min(relative_bray_values), 4),
        "run_pair_total_normalized_bray_curtis_max": round(max(relative_bray_values), 4),
    }
    return summary, rows


def build_canonicalization_rule_sensitivity(
    tel_rows: list[dict[str, object]], teo_rows: list[dict[str, object]]
) -> tuple[dict[str, object], list[dict[str, object]]]:
    rule_specs = [
        (
            "strict_accession_plus_proteoform",
            lambda row: (row["protein_accession"], row["proteoform"]),
            "Primary exact-ID analysis unit.",
        ),
        (
            "accession_plus_canonical_sequence",
            lambda row: (row["protein_accession"], row["canonicalized_proteoform"]),
            "Bracketed annotations, punctuation, and non-sequence characters removed before matching.",
        ),
        (
            "accession_plus_canonical_sequence_and_residue_window",
            lambda row: (
                row["protein_accession"],
                row["canonicalized_proteoform"],
                row["first_residue"],
                row["last_residue"],
            ),
            "Same canonical sequence rule, but residue bounds must also agree.",
        ),
        (
            "accession_plus_residue_window",
            lambda row: (row["protein_accession"], row["first_residue"], row["last_residue"]),
            "Residue-window-only matching to probe whether sequence stripping over-merges shifted strings.",
        ),
    ]
    rows: list[dict[str, object]] = []
    summary: dict[str, object] = {}
    for rule_name, key_fn, note in rule_specs:
        tel_ids = {key_fn(row) for row in tel_rows}
        teo_ids = {key_fn(row) for row in teo_rows}
        shared = len(tel_ids & teo_ids)
        union = len(tel_ids | teo_ids)
        jaccard = shared / union
        summary[f"{rule_name}_shared_count"] = shared
        summary[f"{rule_name}_jaccard_overlap"] = round(jaccard, 4)
        rows.append(
            {
                "rule": rule_name,
                "shared_count": shared,
                "union_count": union,
                "jaccard_overlap": round(jaccard, 4),
                "note": note,
            }
        )
    return summary, rows


def build_presence_overlap_significance(
    tel_rows: list[dict[str, object]], teo_rows: list[dict[str, object]]
) -> tuple[dict[str, object], list[dict[str, object]]]:
    exact_tel_ids = {row["proteoform_id"] for row in tel_rows}
    exact_teo_ids = {row["proteoform_id"] for row in teo_rows}
    canonical_tel_ids = {
        (row["protein_accession"], row["canonicalized_proteoform"]) for row in tel_rows
    }
    canonical_teo_ids = {
        (row["protein_accession"], row["canonicalized_proteoform"]) for row in teo_rows
    }
    protein_tel_ids = {row["protein_accession"] for row in tel_rows}
    protein_teo_ids = {row["protein_accession"] for row in teo_rows}

    rows: list[dict[str, object]] = []
    summary: dict[str, object] = {}
    for label, left_ids, right_ids, note in [
        (
            "exact_id",
            exact_tel_ids,
            exact_teo_ids,
            "Conditional lower-tail hypergeometric test on exact accession+proteoform overlap, with centered Jaccard reported relative to the marginal-prevalence independence baseline.",
        ),
        (
            "canonicalized",
            canonical_tel_ids,
            canonical_teo_ids,
            "Same prevalence-adjusted overlap test after deterministic canonicalization of the proteoform strings.",
        ),
        (
            "protein_level",
            protein_tel_ids,
            protein_teo_ids,
            "Same prevalence-adjusted overlap test after collapsing to protein accessions.",
        ),
    ]:
        tel_count = len(left_ids)
        teo_count = len(right_ids)
        overlap = len(left_ids & right_ids)
        universe = len(left_ids | right_ids)
        observed_jaccard = overlap / universe if universe else 0.0
        tel_prevalence = tel_count / universe if universe else 0.0
        teo_prevalence = teo_count / universe if universe else 0.0
        expected_jaccard = (
            (tel_prevalence * teo_prevalence)
            / (tel_prevalence + teo_prevalence - tel_prevalence * teo_prevalence)
            if tel_prevalence + teo_prevalence - tel_prevalence * teo_prevalence
            else 0.0
        )
        null_jaccard = hypergeom_jaccard_summary(tel_count, teo_count, universe)
        p_value, neg_log10 = hypergeom_lower_tail_p(overlap, tel_count, teo_count, universe)
        summary[f"{label}_centered_jaccard"] = round(observed_jaccard - expected_jaccard, 4)
        summary[f"{label}_expected_jaccard_under_independence"] = round(expected_jaccard, 4)
        summary[f"{label}_fixed_margin_expected_shared"] = round(
            null_jaccard["expected_shared"], 4
        )
        summary[f"{label}_fixed_margin_jaccard_mean"] = round(null_jaccard["jaccard_mean"], 4)
        summary[f"{label}_fixed_margin_jaccard_low_95"] = round(
            null_jaccard["jaccard_low_95"], 4
        )
        summary[f"{label}_fixed_margin_jaccard_high_95"] = round(
            null_jaccard["jaccard_high_95"], 4
        )
        summary[f"{label}_overlap_lower_tail_p"] = p_value
        summary[f"{label}_overlap_lower_tail_neg_log10_p"] = round(neg_log10, 4)
        rows.append(
            {
                "representation": label,
                "tel_count": tel_count,
                "teo_count": teo_count,
                "shared_count": overlap,
                "universe_count": universe,
                "observed_jaccard": round(observed_jaccard, 4),
                "expected_jaccard_under_independence": round(expected_jaccard, 4),
                "centered_jaccard": round(observed_jaccard - expected_jaccard, 4),
                "fixed_margin_expected_shared": round(null_jaccard["expected_shared"], 4),
                "fixed_margin_jaccard_mean": round(null_jaccard["jaccard_mean"], 4),
                "fixed_margin_jaccard_low_95": round(null_jaccard["jaccard_low_95"], 4),
                "fixed_margin_jaccard_high_95": round(null_jaccard["jaccard_high_95"], 4),
                "lower_tail_p": f"{p_value:.6g}" if p_value > 0 else "<1e-323",
                "lower_tail_neg_log10_p": round(neg_log10, 4),
                "note": note,
            }
        )
    return summary, rows


def build_occupancy_detectability_model(
    tel_rows: list[dict[str, object]], teo_rows: list[dict[str, object]]
) -> tuple[dict[str, object], list[dict[str, object]]]:
    tel_exact = aggregate_exact_ids(tel_rows)
    teo_exact = aggregate_exact_ids(teo_rows)

    def summarize_region(
        aggregated_rows: dict[tuple[str, str], dict[str, object]], region: str
    ) -> tuple[dict[str, object], dict[str, float]]:
        summary = summarize_detectability(aggregated_rows)
        row = {
            "section": "region_effort",
            "region": region,
            "exact_id_count": int(summary["exact_id_count"]),
            "single_run_only_count": int(summary["q1"]),
            "duplicate_reobserved_count": int(summary["q2"]),
            "per_run_detection_probability": round(summary["per_run_detection"], 4),
            "detected_at_least_once_probability": round(summary["detected_at_least_once"], 4),
            "latent_richness_estimate": round(summary["latent_richness"], 4),
            "adjusted_shared_exact_ids": "",
            "adjusted_jaccard_overlap": "",
            "note": (
                "Two-run occupancy-style bound estimated from exact-ID duplicate rediscovery. "
                "The model treats each exact proteoform as latent and uses only whether it was seen in one run or both."
            ),
        }
        return row, summary

    tel_row, tel_summary = summarize_region(tel_exact, "telencephalon")
    teo_row, teo_summary = summarize_region(teo_exact, "optic_tectum")

    observed_shared = len(set(tel_exact) & set(teo_exact))
    adjusted_shared = (
        observed_shared
        / (tel_summary["detected_at_least_once"] * teo_summary["detected_at_least_once"])
        if tel_summary["detected_at_least_once"] and teo_summary["detected_at_least_once"]
        else 0.0
    )
    adjusted_union = (
        tel_summary["latent_richness"] + teo_summary["latent_richness"] - adjusted_shared
        if adjusted_shared
        else 0.0
    )
    adjusted_jaccard = adjusted_shared / adjusted_union if adjusted_union else 0.0
    hidden_shared_increment = adjusted_shared - observed_shared

    overlap_row = {
        "section": "cross_region_overlap",
        "region": "paired_regions",
        "exact_id_count": "",
        "single_run_only_count": "",
        "duplicate_reobserved_count": "",
        "per_run_detection_probability": "",
        "detected_at_least_once_probability": "",
        "latent_richness_estimate": round(adjusted_union, 4),
        "adjusted_shared_exact_ids": round(adjusted_shared, 4),
        "adjusted_jaccard_overlap": round(adjusted_jaccard, 4),
        "note": (
            "Cross-region overlap after correcting the observed shared exact IDs for the region-specific "
            "two-run detection probabilities. This quantifies how much hidden overlap could be attributed "
            "to uneven duplicate recovery alone."
        ),
    }

    summary = {
        "occupancy_tel_q1_exact_ids": tel_summary["q1"],
        "occupancy_tel_q2_exact_ids": tel_summary["q2"],
        "occupancy_teo_q1_exact_ids": teo_summary["q1"],
        "occupancy_teo_q2_exact_ids": teo_summary["q2"],
        "occupancy_tel_per_run_detection_probability": round(tel_summary["per_run_detection"], 4),
        "occupancy_teo_per_run_detection_probability": round(teo_summary["per_run_detection"], 4),
        "occupancy_tel_detected_at_least_once_probability": round(
            tel_summary["detected_at_least_once"], 4
        ),
        "occupancy_teo_detected_at_least_once_probability": round(
            teo_summary["detected_at_least_once"], 4
        ),
        "occupancy_tel_latent_richness_estimate": round(tel_summary["latent_richness"], 4),
        "occupancy_teo_latent_richness_estimate": round(teo_summary["latent_richness"], 4),
        "occupancy_adjusted_shared_exact_ids": round(adjusted_shared, 4),
        "occupancy_adjusted_hidden_shared_increment": round(hidden_shared_increment, 4),
        "occupancy_adjusted_jaccard_overlap": round(adjusted_jaccard, 4),
    }

    return summary, [tel_row, teo_row, overlap_row]


def build_misidentification_sensitivity_bounds(
    tel_rows: list[dict[str, object]], teo_rows: list[dict[str, object]], protein_overlap_fraction: float
) -> tuple[dict[str, object], list[dict[str, object]]]:
    tel_exact_ids = {row["proteoform_id"] for row in tel_rows}
    teo_exact_ids = {row["proteoform_id"] for row in teo_rows}
    shared = len(tel_exact_ids & teo_exact_ids)
    union = len(tel_exact_ids | teo_exact_ids)
    tel_unique = len(tel_exact_ids) - shared
    teo_unique = len(teo_exact_ids) - shared

    rows: list[dict[str, object]] = []
    summary: dict[str, object] = {}
    scenario_rates = [0.01, 0.025, 0.05, 0.10]
    for rate in scenario_rates:
        reclassified_pairs = min(tel_unique * rate, teo_unique * rate)
        adjusted_shared = shared + reclassified_pairs
        adjusted_union = union - reclassified_pairs
        adjusted_jaccard = adjusted_shared / adjusted_union
        rows.append(
            {
                "scenario_type": "assumed_unique_id_error_rate",
                "scenario": f"{int(rate * 1000) / 10:g}% conservative paired reclassification",
                "assumed_error_rate": round(rate, 4),
                "reclassified_pairs": round(reclassified_pairs, 4),
                "adjusted_shared_count": round(adjusted_shared, 4),
                "adjusted_union_count": round(adjusted_union, 4),
                "adjusted_jaccard_overlap": round(adjusted_jaccard, 4),
                "tel_unique_error_fraction_needed": "",
                "teo_unique_error_fraction_needed": "",
                "note": (
                    "Conservative upper bound that lets an equal fraction of region-unique exact IDs in "
                    "both regions collapse into paired shared IDs. The 1% and 5% scenarios match the "
                    "PrSM- and proteoform-level FDR values reported for the source workflow."
                ),
            }
        )
        summary[f"misidentification_{str(rate).replace('.', '_')}_adjusted_jaccard_overlap"] = round(
            adjusted_jaccard, 4
        )

    target_specs = [
        ("jaccard_0_10", 0.10, "Rate needed to lift the exact-ID Jaccard to 0.10."),
        (
            "protein_overlap_fraction",
            protein_overlap_fraction,
            "Rate needed to lift the exact-ID Jaccard all the way to the observed protein-level overlap.",
        ),
    ]
    for label, target_jaccard, note in target_specs:
        reclassified_pairs = (target_jaccard * union - shared) / (1 + target_jaccard)
        tel_rate = reclassified_pairs / tel_unique if tel_unique else 0.0
        teo_rate = reclassified_pairs / teo_unique if teo_unique else 0.0
        rows.append(
            {
                "scenario_type": "target_jaccard_threshold",
                "scenario": label,
                "assumed_error_rate": "",
                "reclassified_pairs": round(reclassified_pairs, 4),
                "adjusted_shared_count": round(shared + reclassified_pairs, 4),
                "adjusted_union_count": round(union - reclassified_pairs, 4),
                "adjusted_jaccard_overlap": round(target_jaccard, 4),
                "tel_unique_error_fraction_needed": round(tel_rate, 4),
                "teo_unique_error_fraction_needed": round(teo_rate, 4),
                "note": note,
            }
        )
        summary[f"misidentification_rate_needed_for_{label}_tel"] = round(tel_rate, 4)
        summary[f"misidentification_rate_needed_for_{label}_teo"] = round(teo_rate, 4)

    return summary, rows


def build_canonicalization_examples(
    tel_rows: list[dict[str, object]], teo_rows: list[dict[str, object]], limit: int = 12
) -> list[dict[str, object]]:
    tel_exact_ids = {row["proteoform_id"] for row in tel_rows}
    teo_exact_ids = {row["proteoform_id"] for row in teo_rows}
    tel_canonical: dict[tuple[str, str], list[dict[str, object]]] = {}
    teo_canonical: dict[tuple[str, str], list[dict[str, object]]] = {}
    for row in tel_rows:
        key = (str(row["protein_accession"]), str(row["canonicalized_proteoform"]))
        tel_canonical.setdefault(key, []).append(row)
    for row in teo_rows:
        key = (str(row["protein_accession"]), str(row["canonicalized_proteoform"]))
        teo_canonical.setdefault(key, []).append(row)

    rows: list[dict[str, object]] = []
    for key in sorted(tel_canonical.keys() & teo_canonical.keys()):
        tel_candidates = tel_canonical[key]
        teo_candidates = teo_canonical[key]
        example_pair: tuple[dict[str, object], dict[str, object]] | None = None
        for tel_row in tel_candidates:
            for teo_row in teo_candidates:
                if tel_row["proteoform_id"] != teo_row["proteoform_id"]:
                    example_pair = (tel_row, teo_row)
                    break
            if example_pair is not None:
                break
        if example_pair is None:
            continue
        tel_row, teo_row = example_pair
        rows.append(
            {
                "protein_accession": tel_row["protein_accession"],
                "telencephalon_proteoform": tel_row["proteoform"],
                "optic_tectum_proteoform": teo_row["proteoform"],
                "telencephalon_sequence_core": proteoform_sequence_core(str(tel_row["proteoform"])),
                "optic_tectum_sequence_core": proteoform_sequence_core(str(teo_row["proteoform"])),
                "telencephalon_modification_tokens": proteoform_modification_tokens(
                    str(tel_row["proteoform"])
                ),
                "optic_tectum_modification_tokens": proteoform_modification_tokens(
                    str(teo_row["proteoform"])
                ),
                "canonicalized_sequence": key[1],
                "telencephalon_residue_window": f"{tel_row['first_residue']}-{tel_row['last_residue']}",
                "optic_tectum_residue_window": f"{teo_row['first_residue']}-{teo_row['last_residue']}",
                "standards_note": (
                    "The source strings are decomposed into sequence-core and modification-token parts so "
                    "they can be compared in a ProForma-oriented way, even though the public tables do not "
                    "expose the full localization metadata needed for full ProForma 2.0 serialization."
                ),
                "note": (
                    "Strict proteoform strings differ, but accession identity plus the canonicalized sequence "
                    "still indicate the same proteoform family."
                ),
            }
        )
        if len(rows) >= limit:
            break
    return rows


def tertile_label(value: float, thresholds: tuple[float, float]) -> str:
    low_cut, high_cut = thresholds
    if value <= low_cut:
        return "low"
    if value <= high_cut:
        return "middle"
    return "high"


def build_detectability_stratified_sensitivity(
    tel_rows: list[dict[str, object]], teo_rows: list[dict[str, object]]
) -> tuple[dict[str, object], list[dict[str, object]]]:
    tel_exact = aggregate_exact_ids(tel_rows)
    teo_exact = aggregate_exact_ids(teo_rows)
    observed_shared_ids = sorted(set(tel_exact) & set(teo_exact))
    tel_global = summarize_detectability(tel_exact)
    teo_global = summarize_detectability(teo_exact)
    rows: list[dict[str, object]] = []
    summary: dict[str, object] = {}

    scheme_specs = [
        (
            "mass_tertiles",
            "precursor_mass",
            "Exact IDs are stratified by region-specific precursor-mass tertiles before duplicate-based detectability is estimated.",
        ),
        (
            "intensity_tertiles",
            "avg_intensity",
            "Exact IDs are stratified by region-specific mean duplicate-intensity tertiles before duplicate-based detectability is estimated.",
        ),
    ]

    for scheme, value_key, note in scheme_specs:
        tel_thresholds = (
            quantile([float(row[value_key]) for row in tel_exact.values()], 1 / 3),
            quantile([float(row[value_key]) for row in tel_exact.values()], 2 / 3),
        )
        teo_thresholds = (
            quantile([float(row[value_key]) for row in teo_exact.values()], 1 / 3),
            quantile([float(row[value_key]) for row in teo_exact.values()], 2 / 3),
        )
        tel_bins = {
            identifier: tertile_label(float(row[value_key]), tel_thresholds)
            for identifier, row in tel_exact.items()
        }
        teo_bins = {
            identifier: tertile_label(float(row[value_key]), teo_thresholds)
            for identifier, row in teo_exact.items()
        }
        tel_bin_summaries: dict[str, dict[str, float]] = {}
        teo_bin_summaries: dict[str, dict[str, float]] = {}

        for region_name, exact_rows, bin_assignments, region_summary, store in [
            ("telencephalon", tel_exact, tel_bins, tel_global, tel_bin_summaries),
            ("optic_tectum", teo_exact, teo_bins, teo_global, teo_bin_summaries),
        ]:
            for label in ("low", "middle", "high"):
                subset = {
                    identifier: exact_rows[identifier]
                    for identifier, bin_label in bin_assignments.items()
                    if bin_label == label
                }
                bin_summary = summarize_detectability(
                    subset,
                    fallback_detected_at_least_once=region_summary["detected_at_least_once"],
                )
                store[label] = bin_summary
                rows.append(
                    {
                        "scheme": scheme,
                        "section": "region_bin",
                        "region": region_name,
                        "bin": label,
                        "exact_id_count": int(bin_summary["exact_id_count"]),
                        "single_run_only_count": int(bin_summary["q1"]),
                        "duplicate_reobserved_count": int(bin_summary["q2"]),
                        "per_run_detection_probability": round(bin_summary["per_run_detection"], 4),
                        "detected_at_least_once_probability": round(
                            bin_summary["detected_at_least_once"], 4
                        ),
                        "latent_richness_estimate": round(bin_summary["latent_richness"], 4),
                        "adjusted_shared_exact_ids": "",
                        "adjusted_jaccard_overlap": "",
                        "fallback_used": "yes" if bin_summary["fallback_used"] else "no",
                        "note": note,
                    }
                )

        tel_latent = sum(
            1.0 / tel_bin_summaries[tel_bins[identifier]]["detected_at_least_once"]
            for identifier in tel_exact
        )
        teo_latent = sum(
            1.0 / teo_bin_summaries[teo_bins[identifier]]["detected_at_least_once"]
            for identifier in teo_exact
        )
        adjusted_shared = sum(
            1.0
            / (
                tel_bin_summaries[tel_bins[identifier]]["detected_at_least_once"]
                * teo_bin_summaries[teo_bins[identifier]]["detected_at_least_once"]
            )
            for identifier in observed_shared_ids
        )
        adjusted_union = tel_latent + teo_latent - adjusted_shared
        adjusted_jaccard = adjusted_shared / adjusted_union if adjusted_union else 0.0
        rows.append(
            {
                "scheme": scheme,
                "section": "cross_region_overlap",
                "region": "paired_regions",
                "bin": "all",
                "exact_id_count": "",
                "single_run_only_count": "",
                "duplicate_reobserved_count": "",
                "per_run_detection_probability": "",
                "detected_at_least_once_probability": "",
                "latent_richness_estimate": round(adjusted_union, 4),
                "adjusted_shared_exact_ids": round(adjusted_shared, 4),
                "adjusted_jaccard_overlap": round(adjusted_jaccard, 4),
                "fallback_used": "",
                "note": note,
            }
        )
        summary[f"{scheme}_adjusted_shared_exact_ids"] = round(adjusted_shared, 4)
        summary[f"{scheme}_adjusted_jaccard_overlap"] = round(adjusted_jaccard, 4)

    return summary, rows


def build_gene_symbol_sensitivity(
    tel_rows: list[dict[str, object]], teo_rows: list[dict[str, object]], membership_rows: list[dict[str, object]]
) -> tuple[dict[str, object], list[dict[str, object]]]:
    tel_genes = {str(row["gene"]) for row in tel_rows if str(row["gene"])}
    teo_genes = {str(row["gene"]) for row in teo_rows if str(row["gene"])}
    shared = len(tel_genes & teo_genes)
    union = len(tel_genes | teo_genes)
    observed_jaccard = shared / union if union else 0.0
    tel_prevalence = len(tel_genes) / union if union else 0.0
    teo_prevalence = len(teo_genes) / union if union else 0.0
    expected_jaccard = (
        (tel_prevalence * teo_prevalence)
        / (tel_prevalence + teo_prevalence - tel_prevalence * teo_prevalence)
        if tel_prevalence + teo_prevalence - tel_prevalence * teo_prevalence
        else 0.0
    )
    gene_p, gene_neg_log10 = hypergeom_lower_tail_p(shared, len(tel_genes), len(teo_genes), union)

    tel_matched_genes = {
        str(row["gene"])
        for row in membership_rows
        if row["functional_axis"] == "telencephalon" and row["role"] == "matched" and str(row["gene"])
    }
    tel_spill_genes = {
        str(row["gene"])
        for row in membership_rows
        if row["functional_axis"] == "telencephalon" and row["role"] == "spillover" and str(row["gene"])
    }
    teo_matched_genes = {
        str(row["gene"])
        for row in membership_rows
        if row["functional_axis"] == "optic_tectum" and row["role"] == "matched" and str(row["gene"])
    }
    teo_spill_genes = {
        str(row["gene"])
        for row in membership_rows
        if row["functional_axis"] == "optic_tectum" and row["role"] == "spillover" and str(row["gene"])
    }
    a = len(tel_matched_genes)
    b = len(tel_spill_genes)
    c = len(teo_spill_genes)
    d = len(teo_matched_genes)
    gene_or, gene_low, gene_high = odds_ratio_with_ci(a, b, c, d, correction=0.5)
    gene_panel_p = fisher_one_sided_greater(a, b, c, d)
    gene_alignment = (a + d) / (a + b + c + d) if (a + b + c + d) else 0.0

    rows = [
        {
            "analysis": "all_detected_gene_overlap",
            "shared_count": shared,
            "union_count": union,
            "jaccard_overlap": round(observed_jaccard, 4),
            "expected_jaccard_under_independence": round(expected_jaccard, 4),
            "centered_jaccard": round(observed_jaccard - expected_jaccard, 4),
            "lower_tail_p": f"{gene_p:.6g}" if gene_p > 0 else "<1e-323",
            "lower_tail_neg_log10_p": round(gene_neg_log10, 4),
            "alignment_fraction": "",
            "odds_ratio": "",
            "odds_ratio_ci_low": "",
            "odds_ratio_ci_high": "",
            "note": "All detected entries collapsed to gene symbols before overlap is recomputed.",
        },
        {
            "analysis": "marker_panel_gene_collapse",
            "shared_count": "",
            "union_count": "",
            "jaccard_overlap": "",
            "expected_jaccard_under_independence": "",
            "centered_jaccard": "",
            "lower_tail_p": round(gene_panel_p, 6),
            "lower_tail_neg_log10_p": round(-math.log10(max(gene_panel_p, 1e-323)), 4),
            "alignment_fraction": round(gene_alignment, 4),
            "odds_ratio": round(gene_or, 4),
            "odds_ratio_ci_low": round(gene_low, 4),
            "odds_ratio_ci_high": round(gene_high, 4),
            "note": "Curated marker panel collapsed to unique gene symbols within each functional axis.",
        },
    ]
    summary = {
        "gene_symbol_jaccard_overlap": round(observed_jaccard, 4),
        "gene_symbol_centered_jaccard": round(observed_jaccard - expected_jaccard, 4),
        "gene_symbol_lower_tail_neg_log10_p": round(gene_neg_log10, 4),
        "marker_gene_collapsed_alignment_fraction": round(gene_alignment, 4),
        "marker_gene_collapsed_odds_ratio": round(gene_or, 4),
        "marker_gene_collapsed_one_sided_p_greater": round(gene_panel_p, 6),
    }
    return summary, rows


def muscle_annotation(description: str) -> str:
    description_lower = description.lower()
    if "skeletal" in description_lower or "fast" in description_lower:
        return "skeletal-muscle-like"
    if "atrial" in description_lower or "cardiac" in description_lower:
        return "cardiac-like"
    if "regulatory" in description_lower or "non-muscle" in description_lower:
        return "regulatory-or-non-muscle-like"
    return "unspecified"


def build_motor_family_breakdown(
    membership_rows: list[dict[str, object]],
) -> tuple[dict[str, object], list[dict[str, object]]]:
    grouped: dict[tuple[str, str, str, str], dict[str, object]] = {}
    for row in membership_rows:
        family_key = str(row["family_key"])
        if family_key not in {"myosin", "troponin"}:
            continue
        key = (
            family_key,
            str(row["gene"]),
            str(row["protein_accession"]),
            str(row["protein_description"]),
        )
        if key not in grouped:
            grouped[key] = {
                "family_key": family_key,
                "gene": row["gene"],
                "protein_accession": row["protein_accession"],
                "protein_description": row["protein_description"],
                "annotation_class": muscle_annotation(str(row["protein_description"])),
                "telencephalon_count": 0,
                "optic_tectum_count": 0,
                "matched_count": 0,
                "spillover_count": 0,
                "source_rows": [],
            }
        grouped_row = grouped[key]
        grouped_row[f"{row['region']}_count"] += 1
        grouped_row[f"{row['role']}_count"] += 1
        grouped_row["source_rows"].append(str(row["source_row"]))

    rows: list[dict[str, object]] = []
    skeletal_like_total = 0
    all_total = 0
    for grouped_row in sorted(
        grouped.values(),
        key=lambda value: (value["family_key"], -int(value["optic_tectum_count"]), str(value["gene"])),
    ):
        total = int(grouped_row["telencephalon_count"]) + int(grouped_row["optic_tectum_count"])
        all_total += total
        if grouped_row["annotation_class"] in {"skeletal-muscle-like", "cardiac-like"}:
            skeletal_like_total += total
        rows.append(
            {
                "family_key": grouped_row["family_key"],
                "gene": grouped_row["gene"],
                "protein_accession": grouped_row["protein_accession"],
                "protein_description": grouped_row["protein_description"],
                "annotation_class": grouped_row["annotation_class"],
                "telencephalon_count": grouped_row["telencephalon_count"],
                "optic_tectum_count": grouped_row["optic_tectum_count"],
                "matched_count": grouped_row["matched_count"],
                "spillover_count": grouped_row["spillover_count"],
                "source_rows": ";".join(grouped_row["source_rows"]),
            }
        )
    summary = {
        "motor_family_skeletal_like_fraction": round(skeletal_like_total / all_total, 4) if all_total else 0.0,
        "motor_family_total_observations": all_total,
    }
    return summary, rows


def permutation_test_mean_difference(
    values_a: list[float], values_b: list[float], trials: int = 200_000, seed: int = 20260327
) -> tuple[float, float]:
    observed = abs(statistics.mean(values_a) - statistics.mean(values_b))
    combined = list(values_a) + list(values_b)
    rng = random.Random(seed)
    exceedances = 0
    split = len(values_a)
    for _ in range(trials):
        rng.shuffle(combined)
        perm_a = combined[:split]
        perm_b = combined[split:]
        diff = abs(statistics.mean(perm_a) - statistics.mean(perm_b))
        if diff >= observed:
            exceedances += 1
    return observed, (exceedances + 1) / (trials + 1)


def marker_match_rule(row: dict[str, object], marker_key: str) -> bool:
    gene = str(row["gene"])
    description_lower = str(row["description_lower"])
    if marker_key in {"npy", "penkb", "pyya", "nrgna"}:
        return gene == marker_key
    if marker_key == "synucleins":
        return "synuclein" in description_lower
    if marker_key == "reticulon":
        return "reticulon" in description_lower
    if marker_key == "myosin":
        return "myosin" in description_lower
    if marker_key == "actin":
        return "actin" in description_lower
    if marker_key == "troponin":
        return "troponin" in description_lower
    return gene == marker_key


def marker_rule_text(marker_key: str) -> str:
    if marker_key in {"npy", "penkb", "pyya", "nrgna"}:
        return f"Gene symbol extracted from GN= field equals `{marker_key}`."
    keyword_map = {
        "synucleins": "Synuclein",
        "reticulon": "Reticulon",
        "myosin": "Myosin",
        "actin": "Actin",
        "troponin": "Troponin",
    }
    if marker_key not in keyword_map:
        return f"Gene symbol extracted from GN= field equals `{marker_key}`."
    keyword = keyword_map[marker_key]
    return f"Protein description contains `{keyword}`."


def marker_alignment_fraction(
    markers: list[dict[str, object]], tel_rows: list[dict[str, object]], teo_rows: list[dict[str, object]]
) -> float:
    matched = 0
    total = 0
    for marker in markers:
        key = str(marker["gene"])
        axis = str(marker["functional_axis"])
        tel_count = sum(1 for row in tel_rows if marker_match_rule(row, key))
        teo_count = sum(1 for row in teo_rows if marker_match_rule(row, key))
        matched += tel_count if axis == "telencephalon" else teo_count
        total += tel_count + teo_count
    return matched / total if total else 0.0


def jaccard(left: set[object], right: set[object]) -> float:
    union = left | right
    return len(left & right) / len(union) if union else 0.0


def rarefy_larger_set_to_smaller(
    left_ids: set[object], right_ids: set[object], trials: int, rng: random.Random
) -> tuple[list[float], str, int]:
    if len(left_ids) <= len(right_ids):
        fixed_ids = left_ids
        larger_ids = sorted(right_ids, key=repr)
        sampled_region = "optic_tectum"
    else:
        fixed_ids = right_ids
        larger_ids = sorted(left_ids, key=repr)
        sampled_region = "telencephalon"
    sample_size = len(fixed_ids)
    values = []
    for _ in range(trials):
        sampled_ids = set(rng.sample(larger_ids, sample_size))
        values.append(jaccard(fixed_ids, sampled_ids))
    return values, sampled_region, sample_size


def build_identification_count_rarefaction(
    markers: list[dict[str, object]],
    tel_rows: list[dict[str, object]],
    teo_rows: list[dict[str, object]],
    trials: int = 10_000,
    seed: int = 20260515,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    rng = random.Random(seed)
    rows: list[dict[str, object]] = []
    summary: dict[str, object] = {
        "identification_count_rarefaction_trials": trials,
        "identification_count_rarefaction_seed": seed,
    }

    metric_specs = [
        (
            "exact_id_jaccard",
            {row["proteoform_id"] for row in tel_rows},
            {row["proteoform_id"] for row in teo_rows},
            "Exact accession+proteoform Jaccard after sampling the larger regional exact-ID set down to the smaller set size.",
        ),
        (
            "canonicalized_jaccard",
            {(row["protein_accession"], row["canonicalized_proteoform"]) for row in tel_rows},
            {(row["protein_accession"], row["canonicalized_proteoform"]) for row in teo_rows},
            "Canonicalized accession+sequence Jaccard after the same count-normalized sampling.",
        ),
        (
            "protein_jaccard",
            {row["protein_accession"] for row in tel_rows},
            {row["protein_accession"] for row in teo_rows},
            "Protein-accession Jaccard after the same count-normalized sampling.",
        ),
    ]
    for metric_name, tel_ids, teo_ids, note in metric_specs:
        values, sampled_region, sample_size = rarefy_larger_set_to_smaller(
            set(tel_ids), set(teo_ids), trials, rng
        )
        low = percentile(values, 0.025)
        median = percentile(values, 0.5)
        high = percentile(values, 0.975)
        observed = jaccard(set(tel_ids), set(teo_ids))
        summary[f"rarefaction_{metric_name}_low_95"] = round(low, 4)
        summary[f"rarefaction_{metric_name}_median"] = round(median, 4)
        summary[f"rarefaction_{metric_name}_high_95"] = round(high, 4)
        rows.append(
            {
                "metric": metric_name,
                "trials": trials,
                "seed": seed,
                "sampled_region": sampled_region,
                "sample_size": sample_size,
                "low_95": round(low, 4),
                "median": round(median, 4),
                "high_95": round(high, 4),
                "observed_full": round(observed, 4),
                "note": note,
            }
        )

    if len(tel_rows) <= len(teo_rows):
        fixed_rows = tel_rows
        larger_rows = teo_rows
        sampled_region = "optic_tectum"
    else:
        fixed_rows = teo_rows
        larger_rows = tel_rows
        sampled_region = "telencephalon"
    sample_size = len(fixed_rows)
    marker_values = []
    for _ in range(trials):
        sampled_rows = rng.sample(larger_rows, sample_size)
        if sampled_region == "optic_tectum":
            marker_values.append(marker_alignment_fraction(markers, fixed_rows, sampled_rows))
        else:
            marker_values.append(marker_alignment_fraction(markers, sampled_rows, fixed_rows))
    marker_low = percentile(marker_values, 0.025)
    marker_median = percentile(marker_values, 0.5)
    marker_high = percentile(marker_values, 0.975)
    marker_observed = marker_alignment_fraction(markers, tel_rows, teo_rows)
    summary["rarefaction_marker_alignment_fraction_low_95"] = round(marker_low, 4)
    summary["rarefaction_marker_alignment_fraction_median"] = round(marker_median, 4)
    summary["rarefaction_marker_alignment_fraction_high_95"] = round(marker_high, 4)
    rows.append(
        {
            "metric": "marker_alignment_fraction",
            "trials": trials,
            "seed": seed,
            "sampled_region": sampled_region,
            "sample_size": sample_size,
            "low_95": round(marker_low, 4),
            "median": round(marker_median, 4),
            "high_95": round(marker_high, 4),
            "observed_full": round(marker_observed, 4),
            "note": (
                "Marker-axis alignment after sampling the larger regional row set down to the smaller "
                "row count, preserving the locked marker rules."
            ),
        }
    )
    return summary, rows


def build_source_table_metrics(
    article_totals: dict[str, object], tel_rows: list[dict[str, object]], teo_rows: list[dict[str, object]]
) -> tuple[
    dict[str, object],
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
]:
    tel_ids = {row["proteoform_id"] for row in tel_rows}
    teo_ids = {row["proteoform_id"] for row in teo_rows}
    shared_ids = sorted(tel_ids & teo_ids)
    union_ids = tel_ids | teo_ids
    tel_canonical_ids = {
        (row["protein_accession"], row["canonicalized_proteoform"]) for row in tel_rows
    }
    teo_canonical_ids = {
        (row["protein_accession"], row["canonicalized_proteoform"]) for row in teo_rows
    }

    tel_map = {row["proteoform_id"]: float(row["avg_intensity"]) for row in tel_rows}
    teo_map = {row["proteoform_id"]: float(row["avg_intensity"]) for row in teo_rows}
    tel_relative_map = {
        row["proteoform_id"]: float(row["avg_relative_intensity"]) for row in tel_rows
    }
    teo_relative_map = {
        row["proteoform_id"]: float(row["avg_relative_intensity"]) for row in teo_rows
    }
    weighted_jaccard, bray_curtis = weighted_similarity_metrics(tel_map, teo_map)
    per_run_weighted_jaccard, per_run_bray_curtis = weighted_similarity_metrics(
        tel_relative_map, teo_relative_map
    )
    total_sum_weighted_jaccard, total_sum_bray_curtis = weighted_similarity_metrics(
        total_sum_normalize(tel_map), total_sum_normalize(teo_map)
    )
    upper_tel_map = upper_quartile_normalize(tel_map)
    upper_teo_map = upper_quartile_normalize(teo_map)
    upper_quartile_weighted_jaccard, upper_quartile_bray_curtis = weighted_similarity_metrics(
        upper_tel_map, upper_teo_map
    )
    median_ratio_tel_map, median_ratio_teo_map, median_ratio_tel_scale, median_ratio_teo_scale = (
        median_ratio_normalize(tel_map, teo_map)
    )
    median_ratio_weighted_jaccard, median_ratio_bray_curtis = weighted_similarity_metrics(
        median_ratio_tel_map, median_ratio_teo_map
    )

    tel_q1 = sum(1 for row in tel_rows if row["match_status"] == "No match")
    tel_q2 = sum(1 for row in tel_rows if row["match_status"] == "Match")
    teo_q1 = sum(1 for row in teo_rows if row["match_status"] == "No match")
    teo_q2 = sum(1 for row in teo_rows if row["match_status"] == "Match")
    tel_chao = chao2_lower_bound(len(tel_rows), tel_q1, tel_q2)
    teo_chao = chao2_lower_bound(len(teo_rows), teo_q1, teo_q2)
    tel_jackknife = jackknife1_incidence(len(tel_rows), tel_q1)
    teo_jackknife = jackknife1_incidence(len(teo_rows), teo_q1)
    tel_inflation = tel_chao / len(tel_rows)
    teo_inflation = teo_chao / len(teo_rows)
    shared_exact = len(shared_ids)
    chao_fixed_shared = shared_exact / (tel_chao + teo_chao - shared_exact)
    shared_scaled_min = shared_exact * min(tel_inflation, teo_inflation)
    shared_scaled_max = shared_exact * max(tel_inflation, teo_inflation)
    shared_scaled_geomean = shared_exact * math.sqrt(tel_inflation * teo_inflation)
    jackknife_fixed_shared = shared_exact / (tel_jackknife + teo_jackknife - shared_exact)

    source_summary = {
        "article_reported_shared_proteoforms": int(article_totals["shared_proteoforms"]),
        "article_reported_union_proteoforms": int(
            article_totals["telencephalon_proteoforms"]
            + article_totals["optic_tectum_proteoforms"]
            - article_totals["shared_proteoforms"]
        ),
        "article_reported_jaccard_overlap": round(
            int(article_totals["shared_proteoforms"])
            / (
                int(article_totals["telencephalon_proteoforms"])
                + int(article_totals["optic_tectum_proteoforms"])
                - int(article_totals["shared_proteoforms"])
            ),
            4,
        ),
        "source_table_shared_proteoforms": len(shared_ids),
        "source_table_union_proteoforms": len(union_ids),
        "source_table_jaccard_overlap": round(len(shared_ids) / len(union_ids), 4),
        "source_table_sorensen_overlap": round(
            2 * len(shared_ids) / (len(tel_rows) + len(teo_rows)),
            4,
        ),
        "source_table_canonicalized_overlap": len(tel_canonical_ids & teo_canonical_ids),
        "source_table_canonicalized_jaccard_overlap": round(
            len(tel_canonical_ids & teo_canonical_ids) / len(tel_canonical_ids | teo_canonical_ids),
            4,
        ),
        "source_table_weighted_jaccard_overlap": round(weighted_jaccard, 4),
        "source_table_bray_curtis_similarity": round(bray_curtis, 4),
        "source_table_per_run_total_normalized_weighted_jaccard_overlap": round(
            per_run_weighted_jaccard,
            4,
        ),
        "source_table_per_run_total_normalized_bray_curtis_similarity": round(
            per_run_bray_curtis,
            4,
        ),
        "source_table_total_sum_weighted_jaccard_overlap": round(total_sum_weighted_jaccard, 4),
        "source_table_total_sum_bray_curtis_similarity": round(total_sum_bray_curtis, 4),
        "source_table_upper_quartile_weighted_jaccard_overlap": round(
            upper_quartile_weighted_jaccard,
            4,
        ),
        "source_table_upper_quartile_bray_curtis_similarity": round(
            upper_quartile_bray_curtis,
            4,
        ),
        "source_table_median_ratio_weighted_jaccard_overlap": round(
            median_ratio_weighted_jaccard,
            4,
        ),
        "source_table_median_ratio_bray_curtis_similarity": round(
            median_ratio_bray_curtis,
            4,
        ),
        "source_table_protein_overlap_fraction": round(
            len({row["protein_accession"] for row in tel_rows} & {row["protein_accession"] for row in teo_rows})
            / len({row["protein_accession"] for row in tel_rows} | {row["protein_accession"] for row in teo_rows}),
            4,
        ),
        "source_table_shared_delta_vs_article": len(shared_ids) - int(article_totals["shared_proteoforms"]),
        "tel_q1": tel_q1,
        "tel_q2": tel_q2,
        "teo_q1": teo_q1,
        "teo_q2": teo_q2,
        "tel_chao2_lower_bound": round(tel_chao, 4),
        "teo_chao2_lower_bound": round(teo_chao, 4),
        "tel_jackknife1_lower_bound": round(tel_jackknife, 4),
        "teo_jackknife1_lower_bound": round(teo_jackknife, 4),
        "tel_chao2_inflation_factor": round(tel_inflation, 4),
        "teo_chao2_inflation_factor": round(teo_inflation, 4),
        "duplicate_adjusted_jaccard_shared_fixed": round(chao_fixed_shared, 4),
        "duplicate_adjusted_jaccard_scaled_min": round(
            shared_scaled_min / (tel_chao + teo_chao - shared_scaled_min),
            4,
        ),
        "duplicate_adjusted_jaccard_scaled_max": round(
            shared_scaled_max / (tel_chao + teo_chao - shared_scaled_max),
            4,
        ),
        "duplicate_adjusted_jaccard_scaled_geomean": round(
            shared_scaled_geomean / (tel_chao + teo_chao - shared_scaled_geomean),
            4,
        ),
        "jackknife_adjusted_jaccard_shared_fixed": round(jackknife_fixed_shared, 4),
        "median_ratio_tel_scale": round(median_ratio_tel_scale, 4),
        "median_ratio_teo_scale": round(median_ratio_teo_scale, 4),
    }

    overlap_rows = [
        {
            "scenario": "article_reported_counts",
            "shared_proteoforms": int(article_totals["shared_proteoforms"]),
            "union_proteoforms": source_summary["article_reported_union_proteoforms"],
            "jaccard_overlap": source_summary["article_reported_jaccard_overlap"],
            "sorensen_overlap": round(
                2
                * int(article_totals["shared_proteoforms"])
                / (
                    int(article_totals["telencephalon_proteoforms"])
                    + int(article_totals["optic_tectum_proteoforms"])
                ),
                4,
            ),
            "note": "Published aggregate counts quoted in the 2022 paper.",
        },
        {
            "scenario": "source_table_exact_ids",
            "shared_proteoforms": len(shared_ids),
            "union_proteoforms": len(union_ids),
            "jaccard_overlap": source_summary["source_table_jaccard_overlap"],
            "sorensen_overlap": source_summary["source_table_sorensen_overlap"],
            "note": "Exact accession+proteoform matches across the released Tel2 and Teo2 tables.",
        },
        {
            "scenario": "source_table_duplicate_adjusted_shared_fixed",
            "shared_proteoforms": len(shared_ids),
            "union_proteoforms": round(tel_chao + teo_chao - len(shared_ids), 4),
            "jaccard_overlap": source_summary["duplicate_adjusted_jaccard_shared_fixed"],
            "sorensen_overlap": "",
            "note": "Conservative Chao2 sensitivity with unseen richness added but shared overlap held fixed.",
        },
        {
            "scenario": "source_table_duplicate_adjusted_scaled_min",
            "shared_proteoforms": round(shared_scaled_min, 4),
            "union_proteoforms": round(tel_chao + teo_chao - shared_scaled_min, 4),
            "jaccard_overlap": source_summary["duplicate_adjusted_jaccard_scaled_min"],
            "sorensen_overlap": "",
            "note": "Shared overlap scaled by the smaller of the two duplicate-inflation factors.",
        },
        {
            "scenario": "source_table_duplicate_adjusted_scaled_max",
            "shared_proteoforms": round(shared_scaled_max, 4),
            "union_proteoforms": round(tel_chao + teo_chao - shared_scaled_max, 4),
            "jaccard_overlap": source_summary["duplicate_adjusted_jaccard_scaled_max"],
            "sorensen_overlap": "",
            "note": "Shared overlap scaled by the larger duplicate-inflation factor.",
        },
        {
            "scenario": "source_table_duplicate_adjusted_scaled_geomean",
            "shared_proteoforms": round(shared_scaled_geomean, 4),
            "union_proteoforms": round(tel_chao + teo_chao - shared_scaled_geomean, 4),
            "jaccard_overlap": source_summary["duplicate_adjusted_jaccard_scaled_geomean"],
            "sorensen_overlap": "",
            "note": "Shared overlap scaled by the geometric mean of the two duplicate-inflation factors.",
        },
        {
            "scenario": "source_table_jackknife1_adjusted_shared_fixed",
            "shared_proteoforms": len(shared_ids),
            "union_proteoforms": round(tel_jackknife + teo_jackknife - len(shared_ids), 4),
            "jaccard_overlap": source_summary["jackknife_adjusted_jaccard_shared_fixed"],
            "sorensen_overlap": "",
            "note": "First-order incidence jackknife lower bound with shared exact IDs held fixed.",
        },
    ]

    abundance_rows = [
        {
            "normalization": "raw_mean_duplicate_intensity",
            "weighted_jaccard_overlap": round(weighted_jaccard, 4),
            "bray_curtis_similarity": round(bray_curtis, 4),
            "note": "Mean of the two duplicate intensities in each released source-table row.",
        },
        {
            "normalization": "per_run_total_intensity",
            "weighted_jaccard_overlap": round(per_run_weighted_jaccard, 4),
            "bray_curtis_similarity": round(per_run_bray_curtis, 4),
            "note": "Each duplicate run scaled by its own total ion-intensity sum before averaging rows.",
        },
        {
            "normalization": "region_total_sum",
            "weighted_jaccard_overlap": round(total_sum_weighted_jaccard, 4),
            "bray_curtis_similarity": round(total_sum_bray_curtis, 4),
            "note": "Region-level compositional normalization using total summed average intensity.",
        },
        {
            "normalization": "upper_quartile",
            "weighted_jaccard_overlap": round(upper_quartile_weighted_jaccard, 4),
            "bray_curtis_similarity": round(upper_quartile_bray_curtis, 4),
            "note": "Upper-quartile scaling on region-level average intensities.",
        },
        {
            "normalization": "median_ratio",
            "weighted_jaccard_overlap": round(median_ratio_weighted_jaccard, 4),
            "bray_curtis_similarity": round(median_ratio_bray_curtis, 4),
            "note": "Median-ratio scaling using exact-ID shared proteoforms with positive intensity in both regions.",
        },
    ]

    discrepancy_rows = [
        {
            "comparison_basis": "article_reported_aggregate",
            "shared_count": int(article_totals["shared_proteoforms"]),
            "union_count": source_summary["article_reported_union_proteoforms"],
            "jaccard_overlap": source_summary["article_reported_jaccard_overlap"],
            "note": "Published aggregate summary from the 2022 paper.",
        },
        {
            "comparison_basis": "exact_accession_plus_proteoform",
            "shared_count": len(shared_ids),
            "union_count": len(union_ids),
            "jaccard_overlap": source_summary["source_table_jaccard_overlap"],
            "note": "Strict accession+proteoform matching across the released Tel2 and Teo2 tables.",
        },
        {
            "comparison_basis": "accession_plus_canonicalized_sequence",
            "shared_count": source_summary["source_table_canonicalized_overlap"],
            "union_count": len(tel_canonical_ids | teo_canonical_ids),
            "jaccard_overlap": source_summary["source_table_canonicalized_jaccard_overlap"],
            "note": (
                "Bracketed PTM annotations, punctuation, and non-sequence characters removed before matching; "
                "the article's 35 shared proteoforms lies between the strict and canonicalized counts."
            ),
        },
    ]

    shared_rows = []
    for protein_accession, proteoform in shared_ids:
        tel_row = next(row for row in tel_rows if row["proteoform_id"] == (protein_accession, proteoform))
        teo_row = next(row for row in teo_rows if row["proteoform_id"] == (protein_accession, proteoform))
        shared_rows.append(
            {
                "protein_accession": protein_accession,
                "gene": tel_row["gene"],
                "proteoform": proteoform,
                "tel_avg_intensity": round(float(tel_row["avg_intensity"]), 1),
                "teo_avg_intensity": round(float(teo_row["avg_intensity"]), 1),
                "tel_source_row": tel_row["source_row"],
                "teo_source_row": teo_row["source_row"],
            }
        )

    source_rows = []
    for row in tel_rows + teo_rows:
        source_rows.append(
            {
                "region": row["region"],
                "source_table": row["source_table"],
                "source_row": row["source_row"],
                "protein_accession": row["protein_accession"],
                "gene": row["gene"],
                "protein_description": row["protein_description"],
                "first_residue": row["first_residue"],
                "last_residue": row["last_residue"],
                "proteoform": row["proteoform"],
                "avg_intensity": round(float(row["avg_intensity"]), 1),
                "match_status": row["match_status"],
                "is_acetylated": "yes" if row["is_acetylated"] else "no",
            }
        )

    return source_summary, overlap_rows, shared_rows, source_rows, abundance_rows, discrepancy_rows


def build_marker_outputs(
    markers: list[dict[str, object]], tel_rows: list[dict[str, object]], teo_rows: list[dict[str, object]]
) -> tuple[
    dict[str, object],
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
]:
    marker_rows: list[dict[str, object]] = []
    membership_rows: list[dict[str, object]] = []
    group_consistency_rows: list[dict[str, object]] = []
    leave_one_out_rows: list[dict[str, object]] = []
    axis_rows: list[dict[str, object]] = []
    intensity_rows: list[dict[str, object]] = []
    protein_rows: list[dict[str, object]] = []

    axis_totals = {
        "telencephalon": {"matched": 0, "spillover": 0},
        "optic_tectum": {"matched": 0, "spillover": 0},
    }
    axis_intensity_totals = {
        "telencephalon": {"matched": 0.0, "spillover": 0.0},
        "optic_tectum": {"matched": 0.0, "spillover": 0.0},
    }
    axis_protein_sets = {
        "telencephalon": {"matched": set(), "spillover": set()},
        "optic_tectum": {"matched": set(), "spillover": set()},
    }

    aligned_total = 0
    marker_total = 0
    matched_intensity_total = 0.0
    spillover_intensity_total = 0.0
    group_shares: list[float] = []
    groups_favoring_expected = 0

    marker_cache: dict[str, dict[str, object]] = {}
    for marker in markers:
        key = str(marker["gene"])
        axis = str(marker["functional_axis"])
        tel_family_rows = [row for row in tel_rows if marker_match_rule(row, key)]
        teo_family_rows = [row for row in teo_rows if marker_match_rule(row, key)]
        tel_count = len(tel_family_rows)
        teo_count = len(teo_family_rows)
        tel_intensity = sum(float(row["avg_intensity"]) for row in tel_family_rows)
        teo_intensity = sum(float(row["avg_intensity"]) for row in teo_family_rows)
        tel_proteins = {str(row["protein_accession"]) for row in tel_family_rows}
        teo_proteins = {str(row["protein_accession"]) for row in teo_family_rows}
        tel_acetylated = sum(1 for row in tel_family_rows if row["is_acetylated"])
        teo_acetylated = sum(1 for row in teo_family_rows if row["is_acetylated"])
        matched_count = tel_count if axis == "telencephalon" else teo_count
        spillover_count = teo_count if axis == "telencephalon" else tel_count
        matched_intensity = tel_intensity if axis == "telencephalon" else teo_intensity
        spillover_intensity = teo_intensity if axis == "telencephalon" else tel_intensity
        matched_proteins = tel_proteins if axis == "telencephalon" else teo_proteins
        spillover_proteins = teo_proteins if axis == "telencephalon" else tel_proteins
        total_count = tel_count + teo_count
        matched_share = matched_count / total_count
        groups_favoring_expected += 1 if matched_count > spillover_count else 0
        group_shares.append(matched_share)

        marker_cache[key] = {
            "functional_axis": axis,
            "tel_count": tel_count,
            "teo_count": teo_count,
            "matched_count": matched_count,
            "spillover_count": spillover_count,
            "matched_intensity": matched_intensity,
            "spillover_intensity": spillover_intensity,
        }

        aligned_total += matched_count
        marker_total += total_count
        matched_intensity_total += matched_intensity
        spillover_intensity_total += spillover_intensity
        axis_totals[axis]["matched"] += matched_count
        axis_totals[axis]["spillover"] += spillover_count
        axis_intensity_totals[axis]["matched"] += matched_intensity
        axis_intensity_totals[axis]["spillover"] += spillover_intensity
        axis_protein_sets[axis]["matched"].update(matched_proteins)
        axis_protein_sets[axis]["spillover"].update(spillover_proteins)

        marker_rows.append(
            {
                "gene": key,
                "label": marker["label"],
                "functional_axis": axis,
                "match_rule": marker_rule_text(key),
                "tel_count": tel_count,
                "teo_count": teo_count,
                "matched_count": matched_count,
                "spillover_count": spillover_count,
                "matched_share": round(matched_share, 4),
                "log2_tel_over_teo_plus1": round(math.log2((tel_count + 1) / (teo_count + 1)), 3),
                "tel_avg_intensity": round(tel_intensity, 1),
                "teo_avg_intensity": round(teo_intensity, 1),
                "tel_protein_count": len(tel_proteins),
                "teo_protein_count": len(teo_proteins),
                "tel_acetylated_count": tel_acetylated,
                "teo_acetylated_count": teo_acetylated,
                "interpretation": marker["interpretation"],
            }
        )

        group_consistency_rows.append(
            {
                "label": marker["label"],
                "functional_axis": axis,
                "matched_share": round(matched_share, 4),
                "favors_expected_region": "yes" if matched_count > spillover_count else "no",
            }
        )

        for region_rows, region_name in ((tel_family_rows, "telencephalon"), (teo_family_rows, "optic_tectum")):
            for row in region_rows:
                membership_rows.append(
                    {
                        "family": marker["label"],
                        "family_key": key,
                        "functional_axis": axis,
                        "match_rule": marker_rule_text(key),
                        "region": region_name,
                        "role": (
                            "matched"
                            if (axis == "telencephalon" and region_name == "telencephalon")
                            or (axis == "optic_tectum" and region_name == "optic_tectum")
                            else "spillover"
                        ),
                        "source_table": row["source_table"],
                        "source_row": row["source_row"],
                        "protein_accession": row["protein_accession"],
                        "gene": row["gene"],
                        "protein_description": row["protein_description"],
                        "first_residue": row["first_residue"],
                        "last_residue": row["last_residue"],
                        "proteoform": row["proteoform"],
                        "precursor_mass": round(float(row["precursor_mass"]), 4),
                        "avg_intensity": round(float(row["avg_intensity"]), 1),
                        "is_acetylated": "yes" if row["is_acetylated"] else "no",
                    }
                )

    tel_total = axis_totals["telencephalon"]["matched"] + axis_totals["optic_tectum"]["spillover"]
    teo_total = axis_totals["optic_tectum"]["matched"] + axis_totals["telencephalon"]["spillover"]
    tel_prevalence = tel_total / (tel_total + teo_total)
    teo_prevalence = teo_total / (tel_total + teo_total)
    axis_expected = {"telencephalon": tel_prevalence, "optic_tectum": teo_prevalence}

    for axis, counts in axis_totals.items():
        total = counts["matched"] + counts["spillover"]
        low, high = wilson_interval(counts["matched"], total)
        axis_rows.append(
            {
                "functional_axis": axis,
                "matched_count": counts["matched"],
                "spillover_count": counts["spillover"],
                "alignment_fraction": round(counts["matched"] / total, 4),
                "wilson_low": round(low, 4),
                "wilson_high": round(high, 4),
                "expected_fraction_under_region_prevalence": round(axis_expected[axis], 4),
                "alignment_lift_over_prevalence": round(counts["matched"] / total - axis_expected[axis], 4),
            }
        )

        intensity_matched = axis_intensity_totals[axis]["matched"]
        intensity_spillover = axis_intensity_totals[axis]["spillover"]
        intensity_rows.append(
            {
                "functional_axis": axis,
                "matched_intensity": round(intensity_matched, 1),
                "spillover_intensity": round(intensity_spillover, 1),
                "matched_fraction": round(intensity_matched / (intensity_matched + intensity_spillover), 4),
            }
        )

        matched_proteins = len(axis_protein_sets[axis]["matched"])
        spillover_proteins = len(axis_protein_sets[axis]["spillover"])
        protein_rows.append(
            {
                "functional_axis": axis,
                "matched_proteins": matched_proteins,
                "spillover_proteins": spillover_proteins,
                "matched_fraction": round(matched_proteins / (matched_proteins + spillover_proteins), 4),
            }
        )

    a = axis_totals["telencephalon"]["matched"]
    b = axis_totals["telencephalon"]["spillover"]
    c = axis_totals["optic_tectum"]["spillover"]
    d = axis_totals["optic_tectum"]["matched"]
    odds_ratio, odds_low, odds_high = odds_ratio_with_ci(a, b, c, d)
    fisher = {
        "table": {
            "tel_axis_in_tel": a,
            "tel_axis_in_teo": b,
            "teo_axis_in_tel": c,
            "teo_axis_in_teo": d,
        },
        "odds_ratio": round(odds_ratio, 4),
        "odds_ratio_ci_low": round(odds_low, 4),
        "odds_ratio_ci_high": round(odds_high, 4),
        "one_sided_p_greater": fisher_one_sided_greater(a, b, c, d),
    }

    for marker in markers:
        key = str(marker["gene"])
        remaining_keys = [str(item["gene"]) for item in markers if str(item["gene"]) != key]
        matched = 0
        total = 0
        for other_key in remaining_keys:
            matched += int(marker_cache[other_key]["matched_count"])
            total += int(marker_cache[other_key]["matched_count"]) + int(marker_cache[other_key]["spillover_count"])
        leave_one_out_rows.append(
            {
                "removed_marker": marker["label"],
                "remaining_alignment_fraction": round(matched / total, 4),
            }
        )

    sensitivity_rows = [
        {
            "scenario": "baseline",
            "matched_count": a + d,
            "spillover_count": b + c,
            "alignment_fraction": round((a + d) / (a + b + c + d), 4),
            "odds_ratio": round(odds_ratio, 4),
            "odds_ratio_ci_low": round(odds_low, 4),
            "odds_ratio_ci_high": round(odds_high, 4),
            "one_sided_p_greater": fisher["one_sided_p_greater"],
            "notes": "Observed curated marker panel.",
        }
    ]
    for shifted_counts in (1, 2, 3):
        shifted_a = a - shifted_counts
        shifted_b = b + shifted_counts
        shifted_c = c + shifted_counts
        shifted_d = d - shifted_counts
        shifted_or, shifted_low, shifted_high = odds_ratio_with_ci(
            shifted_a, shifted_b, shifted_c, shifted_d
        )
        sensitivity_rows.append(
            {
                "scenario": f"matched_to_spillover_shift_{shifted_counts}_per_axis",
                "matched_count": shifted_a + shifted_d,
                "spillover_count": shifted_b + shifted_c,
                "alignment_fraction": round(
                    (shifted_a + shifted_d) / (shifted_a + shifted_b + shifted_c + shifted_d),
                    4,
                ),
                "odds_ratio": round(shifted_or, 4),
                "odds_ratio_ci_low": round(shifted_low, 4),
                "odds_ratio_ci_high": round(shifted_high, 4),
                "one_sided_p_greater": fisher_one_sided_greater(
                    shifted_a, shifted_b, shifted_c, shifted_d
                ),
                "notes": (
                    f"Pessimistic stress test moving {shifted_counts} matched count(s) per "
                    "functional axis into spillover."
                ),
            }
        )

    motor_family_keys = {"myosin", "actin", "troponin"}
    motor_tel_matched = sum(
        int(marker_cache[key]["matched_count"])
        for key in marker_cache
        if key not in motor_family_keys and marker_cache[key]["functional_axis"] == "telencephalon"
    )
    motor_tel_spill = sum(
        int(marker_cache[key]["spillover_count"])
        for key in marker_cache
        if key not in motor_family_keys and marker_cache[key]["functional_axis"] == "telencephalon"
    )
    motor_teo_spill = sum(
        int(marker_cache[key]["spillover_count"])
        for key in marker_cache
        if key not in motor_family_keys and marker_cache[key]["functional_axis"] == "optic_tectum"
    )
    motor_teo_matched = sum(
        int(marker_cache[key]["matched_count"])
        for key in marker_cache
        if key not in motor_family_keys and marker_cache[key]["functional_axis"] == "optic_tectum"
    )
    motor_or, motor_low, motor_high = odds_ratio_with_ci(
        motor_tel_matched,
        motor_tel_spill,
        motor_teo_spill,
        motor_teo_matched,
        correction=0.5,
    )
    sensitivity_rows.append(
        {
            "scenario": "exclude_motor_marker_families",
            "matched_count": motor_tel_matched + motor_teo_matched,
            "spillover_count": motor_tel_spill + motor_teo_spill,
            "alignment_fraction": round(
                (motor_tel_matched + motor_teo_matched)
                / (
                    motor_tel_matched
                    + motor_tel_spill
                    + motor_teo_spill
                    + motor_teo_matched
                ),
                4,
            ),
            "odds_ratio": round(motor_or, 4),
            "odds_ratio_ci_low": round(motor_low, 4),
            "odds_ratio_ci_high": round(motor_high, 4),
            "one_sided_p_greater": fisher_one_sided_greater(
                motor_tel_matched, motor_tel_spill, motor_teo_spill, motor_teo_matched
            ),
            "notes": "Excludes myosin, actin, and troponin families to stress-test tissue-contamination concerns.",
        }
    )

    tel_matched_intensity = axis_intensity_totals["telencephalon"]["matched"]
    teo_matched_intensity = axis_intensity_totals["optic_tectum"]["matched"]
    tel_spill_intensity = axis_intensity_totals["telencephalon"]["spillover"]
    teo_spill_intensity = axis_intensity_totals["optic_tectum"]["spillover"]

    protein_a = len(axis_protein_sets["telencephalon"]["matched"])
    protein_b = len(axis_protein_sets["telencephalon"]["spillover"])
    protein_c = len(axis_protein_sets["optic_tectum"]["spillover"])
    protein_d = len(axis_protein_sets["optic_tectum"]["matched"])
    protein_or, protein_low, protein_high = odds_ratio_with_ci(protein_a, protein_b, protein_c, protein_d)

    tel_matched_rows = [
        row for row in membership_rows if row["functional_axis"] == "telencephalon" and row["role"] == "matched"
    ]
    teo_matched_rows = [
        row for row in membership_rows if row["functional_axis"] == "optic_tectum" and row["role"] == "matched"
    ]
    acetyl_a = sum(1 for row in tel_matched_rows if row["is_acetylated"] == "yes")
    acetyl_b = len(tel_matched_rows) - acetyl_a
    acetyl_c = sum(1 for row in teo_matched_rows if row["is_acetylated"] == "yes")
    acetyl_d = len(teo_matched_rows) - acetyl_c
    acetyl_or, acetyl_low, acetyl_high = odds_ratio_with_ci(acetyl_a, acetyl_b, acetyl_c, acetyl_d)

    marker_summary = {
        "marker_alignment_fraction": round(aligned_total / marker_total, 4),
        "expected_alignment_under_region_prevalence": round(
            (
                (axis_totals["telencephalon"]["matched"] + axis_totals["telencephalon"]["spillover"]) * tel_prevalence
                + (axis_totals["optic_tectum"]["matched"] + axis_totals["optic_tectum"]["spillover"]) * teo_prevalence
            )
            / marker_total,
            4,
        ),
        "alignment_excess_over_prevalence": round(
            aligned_total / marker_total
            - (
                (
                    (axis_totals["telencephalon"]["matched"] + axis_totals["telencephalon"]["spillover"]) * tel_prevalence
                    + (axis_totals["optic_tectum"]["matched"] + axis_totals["optic_tectum"]["spillover"]) * teo_prevalence
                )
                / marker_total
            ),
            4,
        ),
        "marker_panel_total_counts": marker_total,
        "marker_groups_total": len(markers),
        "marker_groups_favoring_expected_region": groups_favoring_expected,
        "group_level_mean_matched_share": round(sum(group_shares) / len(group_shares), 4),
        "group_level_min_matched_share": round(min(group_shares), 4),
        "group_level_one_sided_sign_p": round(0.5 ** len(markers), 6),
        "odds_ratio": round(odds_ratio, 4),
        "odds_ratio_ci_low": round(odds_low, 4),
        "odds_ratio_ci_high": round(odds_high, 4),
        "leave_one_out_min_alignment": round(
            min(float(row["remaining_alignment_fraction"]) for row in leave_one_out_rows),
            4,
        ),
        "leave_one_out_max_alignment": round(
            max(float(row["remaining_alignment_fraction"]) for row in leave_one_out_rows),
            4,
        ),
        "stress_test_min_alignment": round(
            min(float(row["alignment_fraction"]) for row in sensitivity_rows),
            4,
        ),
        "motor_family_exclusion_alignment": round(
            float(sensitivity_rows[-1]["alignment_fraction"]),
            4,
        ),
        "intensity_alignment_fraction": round(
            matched_intensity_total / (matched_intensity_total + spillover_intensity_total),
            4,
        ),
        "protein_collapsed_alignment_fraction": round(
            (protein_a + protein_d) / (protein_a + protein_b + protein_c + protein_d),
            4,
        ),
        "protein_collapsed_odds_ratio": round(protein_or, 4),
        "protein_collapsed_odds_ratio_ci_low": round(protein_low, 4),
        "protein_collapsed_odds_ratio_ci_high": round(protein_high, 4),
        "protein_collapsed_one_sided_p_greater": fisher_one_sided_greater(
            protein_a, protein_b, protein_c, protein_d
        ),
        "tel_marker_acetylated_fraction": round(acetyl_a / len(tel_matched_rows), 4),
        "teo_marker_acetylated_fraction": round(acetyl_c / len(teo_matched_rows), 4),
        "marker_acetylation_odds_ratio": round(acetyl_or, 4),
        "marker_acetylation_odds_ratio_ci_low": round(acetyl_low, 4),
        "marker_acetylation_odds_ratio_ci_high": round(acetyl_high, 4),
        "marker_acetylation_one_sided_p_greater": fisher_one_sided_greater(
            acetyl_a, acetyl_b, acetyl_c, acetyl_d
        ),
    }

    ptm_marker_rows = [
        {
            "subset": "telencephalon_matched_marker_panel",
            "acetylated_count": acetyl_a,
            "non_acetylated_count": acetyl_b,
            "total_count": len(tel_matched_rows),
            "acetylated_fraction": round(acetyl_a / len(tel_matched_rows), 4),
        },
        {
            "subset": "optic_tectum_matched_marker_panel",
            "acetylated_count": acetyl_c,
            "non_acetylated_count": acetyl_d,
            "total_count": len(teo_matched_rows),
            "acetylated_fraction": round(acetyl_c / len(teo_matched_rows), 4),
        },
    ]

    intensity_rows.append(
        {
            "functional_axis": "overall",
            "matched_intensity": round(matched_intensity_total, 1),
            "spillover_intensity": round(spillover_intensity_total, 1),
            "matched_fraction": round(
                matched_intensity_total / (matched_intensity_total + spillover_intensity_total),
                4,
            ),
        }
    )
    protein_rows.append(
        {
            "functional_axis": "overall",
            "matched_proteins": protein_a + protein_d,
            "spillover_proteins": protein_b + protein_c,
            "matched_fraction": round(
                (protein_a + protein_d) / (protein_a + protein_b + protein_c + protein_d),
                4,
            ),
        }
    )

    return (
        marker_summary,
        marker_rows,
        membership_rows,
        group_consistency_rows,
        axis_rows,
        intensity_rows,
        protein_rows,
        ptm_marker_rows,
        leave_one_out_rows,
        sensitivity_rows,
    )


def build_marker_permutation_test(
    marker_rows: list[dict[str, object]], trials: int = 200_000, seed: int = 20260327
) -> tuple[dict[str, object], list[dict[str, object]]]:
    family_sizes = [int(row["tel_count"]) + int(row["teo_count"]) for row in marker_rows]
    family_axes = [str(row["functional_axis"]) for row in marker_rows]
    total_tel_labels = sum(int(row["tel_count"]) for row in marker_rows)
    total_count = sum(family_sizes)
    labels = [1] * total_tel_labels + [0] * (total_count - total_tel_labels)
    observed_matched = sum(int(row["matched_count"]) for row in marker_rows)
    rng = random.Random(seed)
    null_matched_counts: list[int] = []
    exceedances = 0

    for _ in range(trials):
        rng.shuffle(labels)
        start = 0
        matched = 0
        for family_size, axis in zip(family_sizes, family_axes):
            tel_in_family = sum(labels[start : start + family_size])
            family_matched = tel_in_family if axis == "telencephalon" else family_size - tel_in_family
            matched += family_matched
            start += family_size
        null_matched_counts.append(matched)
        if matched >= observed_matched:
            exceedances += 1

    p_upper_bound = (exceedances + 1) / (trials + 1)
    null_mean = sum(null_matched_counts) / len(null_matched_counts)
    null_q95 = sorted(null_matched_counts)[int(0.95 * (len(null_matched_counts) - 1))]

    summary = {
        "marker_permutation_trials": trials,
        "marker_permutation_seed": seed,
        "marker_permutation_observed_matched_count": observed_matched,
        "marker_permutation_observed_matched_fraction": round(observed_matched / total_count, 4),
        "marker_permutation_null_mean_matched_count": round(null_mean, 4),
        "marker_permutation_null_mean_matched_fraction": round(null_mean / total_count, 4),
        "marker_permutation_null_q95_matched_count": int(null_q95),
        "marker_permutation_null_q95_matched_fraction": round(null_q95 / total_count, 4),
        "marker_permutation_exceedances": exceedances,
        "marker_permutation_p_upper_bound": round(p_upper_bound, 6),
    }
    rows = [
        {
            "metric": "observed_matched_count",
            "value": observed_matched,
            "note": "Observed matched-region counts in the curated marker panel.",
        },
        {
            "metric": "observed_matched_fraction",
            "value": round(observed_matched / total_count, 4),
            "note": "Observed matched-region fraction in the curated marker panel.",
        },
        {
            "metric": "null_mean_matched_count",
            "value": round(null_mean, 4),
            "note": "Mean matched counts under family-size-preserving label randomization.",
        },
        {
            "metric": "null_q95_matched_count",
            "value": int(null_q95),
            "note": "95th percentile of matched counts under the same null.",
        },
        {
            "metric": "p_upper_bound",
            "value": round(p_upper_bound, 6),
            "note": "One-sided Monte Carlo upper bound for a randomization achieving at least the observed match total.",
        },
    ]
    return summary, rows


def build_protein_level_permutation_test(
    marker_rows: list[dict[str, object]], trials: int = 200_000, seed: int = 20260328
) -> tuple[dict[str, object], list[dict[str, object]]]:
    family_sizes = [int(row["tel_protein_count"]) + int(row["teo_protein_count"]) for row in marker_rows]
    family_axes = [str(row["functional_axis"]) for row in marker_rows]
    total_tel_labels = sum(int(row["tel_protein_count"]) for row in marker_rows)
    total_count = sum(family_sizes)
    labels = [1] * total_tel_labels + [0] * (total_count - total_tel_labels)
    observed_matched = sum(
        int(row["tel_protein_count"]) if row["functional_axis"] == "telencephalon" else int(row["teo_protein_count"])
        for row in marker_rows
    )
    rng = random.Random(seed)
    null_matched_counts: list[int] = []
    exceedances = 0

    for _ in range(trials):
        rng.shuffle(labels)
        start = 0
        matched = 0
        for family_size, axis in zip(family_sizes, family_axes):
            tel_in_family = sum(labels[start : start + family_size])
            family_matched = tel_in_family if axis == "telencephalon" else family_size - tel_in_family
            matched += family_matched
            start += family_size
        null_matched_counts.append(matched)
        if matched >= observed_matched:
            exceedances += 1

    p_upper_bound = (exceedances + 1) / (trials + 1)
    null_mean = sum(null_matched_counts) / len(null_matched_counts)
    null_q95 = sorted(null_matched_counts)[int(0.95 * (len(null_matched_counts) - 1))]
    summary = {
        "protein_level_marker_permutation_trials": trials,
        "protein_level_marker_permutation_seed": seed,
        "protein_level_marker_permutation_observed_matched_count": observed_matched,
        "protein_level_marker_permutation_observed_matched_fraction": round(observed_matched / total_count, 4),
        "protein_level_marker_permutation_null_mean_matched_count": round(null_mean, 4),
        "protein_level_marker_permutation_null_mean_matched_fraction": round(null_mean / total_count, 4),
        "protein_level_marker_permutation_null_q95_matched_count": int(null_q95),
        "protein_level_marker_permutation_null_q95_matched_fraction": round(null_q95 / total_count, 4),
        "protein_level_marker_permutation_exceedances": exceedances,
        "protein_level_marker_permutation_p_upper_bound": round(p_upper_bound, 6),
    }
    rows = [
        {
            "metric": "observed_matched_count",
            "value": observed_matched,
            "note": "Observed matched-region protein counts across the curated family panel.",
        },
        {
            "metric": "observed_matched_fraction",
            "value": round(observed_matched / total_count, 4),
            "note": "Observed matched-region fraction after collapsing curated families to unique proteins.",
        },
        {
            "metric": "null_mean_matched_count",
            "value": round(null_mean, 4),
            "note": "Mean matched protein counts under family-size-preserving label randomization.",
        },
        {
            "metric": "null_q95_matched_count",
            "value": int(null_q95),
            "note": "95th percentile of matched protein counts under the same null.",
        },
        {
            "metric": "p_upper_bound",
            "value": round(p_upper_bound, 6),
            "note": "One-sided Monte Carlo upper bound at the protein-collapsed family level.",
        },
    ]
    return summary, rows


def build_ptm_detectability_proxy_screen(
    membership_rows: list[dict[str, object]], trials: int = 200_000, seed: int = 20260329
) -> tuple[dict[str, object], list[dict[str, object]]]:
    tel_acetylated = [
        row
        for row in membership_rows
        if row["functional_axis"] == "telencephalon" and row["role"] == "matched" and row["is_acetylated"] == "yes"
    ]
    teo_acetylated = [
        row
        for row in membership_rows
        if row["functional_axis"] == "optic_tectum" and row["role"] == "matched" and row["is_acetylated"] == "yes"
    ]
    metric_specs = [
        (
            "precursor_mass",
            [float(row["precursor_mass"]) for row in tel_acetylated],
            [float(row["precursor_mass"]) for row in teo_acetylated],
            "Public tables expose precursor mass but not charge state or spectrum-quality scores.",
        ),
        (
            "sequence_span_length",
            [int(row["last_residue"]) - int(row["first_residue"]) + 1 for row in tel_acetylated],
            [int(row["last_residue"]) - int(row["first_residue"]) + 1 for row in teo_acetylated],
            "Span length is derived from the public first-residue and last-residue columns.",
        ),
        (
            "first_residue",
            [int(row["first_residue"]) for row in tel_acetylated],
            [int(row["first_residue"]) for row in teo_acetylated],
            "Lower first-residue values are a coarse public-table proxy for N-terminus coverage.",
        ),
        (
            "avg_intensity",
            [float(row["avg_intensity"]) for row in tel_acetylated],
            [float(row["avg_intensity"]) for row in teo_acetylated],
            "Average duplicate intensity is the only abundance-like detectability proxy exposed for all rows.",
        ),
    ]
    summary: dict[str, object] = {"ptm_detectability_trials": trials, "ptm_detectability_seed": seed}
    rows: list[dict[str, object]] = []
    for index, (metric_name, tel_values, teo_values, note) in enumerate(metric_specs):
        diff, p_value = permutation_test_mean_difference(tel_values, teo_values, trials=trials, seed=seed + index)
        summary[f"ptm_detectability_{metric_name}_tel_mean"] = round(statistics.mean(tel_values), 4)
        summary[f"ptm_detectability_{metric_name}_teo_mean"] = round(statistics.mean(teo_values), 4)
        summary[f"ptm_detectability_{metric_name}_mean_difference_abs"] = round(diff, 4)
        summary[f"ptm_detectability_{metric_name}_permutation_p"] = round(p_value, 6)
        rows.append(
            {
                "metric": metric_name,
                "tel_mean": round(statistics.mean(tel_values), 4),
                "teo_mean": round(statistics.mean(teo_values), 4),
                "tel_median": round(statistics.median(tel_values), 4),
                "teo_median": round(statistics.median(teo_values), 4),
                "absolute_mean_difference": round(diff, 4),
                "permutation_p_two_sided": round(p_value, 6),
                "note": note,
            }
        )
    return summary, rows


def build_mnar_similarity_sensitivity(
    tel_rows: list[dict[str, object]], teo_rows: list[dict[str, object]]
) -> tuple[dict[str, object], list[dict[str, object]]]:
    union_ids = {row["proteoform_id"] for row in tel_rows} | {row["proteoform_id"] for row in teo_rows}
    tel_base = {row["proteoform_id"]: float(row["avg_intensity"]) for row in tel_rows}
    teo_base = {row["proteoform_id"]: float(row["avg_intensity"]) for row in teo_rows}
    tel_nonzero = sorted(value for value in tel_base.values() if value > 0)
    teo_nonzero = sorted(value for value in teo_base.values() if value > 0)

    def build_imputed_map(
        values: dict[tuple[str, str], float], fill_quantile: float | None
    ) -> dict[tuple[str, str], float]:
        if fill_quantile is None:
            fill_value = 0.0
        else:
            nonzero = [value for value in values.values() if value > 0]
            threshold = quantile(nonzero, fill_quantile) if nonzero else 0.0
            fill_value = threshold / 2
        return {identifier: values.get(identifier, fill_value) for identifier in union_ids}

    scenario_specs = [
        ("observed_zero_as_absence", None, "Baseline analysis: blank intensity cells are treated as zeros."),
        (
            "mnar_half_q05_fill",
            0.05,
            "Minimal MNAR sensitivity where undetected rows are imputed to half of the region-specific 5th percentile nonzero intensity.",
        ),
        (
            "mnar_half_q10_fill",
            0.10,
            "Stronger MNAR sensitivity where undetected rows are imputed to half of the region-specific 10th percentile nonzero intensity.",
        ),
    ]
    rows: list[dict[str, object]] = []
    summary: dict[str, object] = {}
    for scenario, fill_quantile, note in scenario_specs:
        tel_map = build_imputed_map(tel_base, fill_quantile)
        teo_map = build_imputed_map(teo_base, fill_quantile)
        weighted_jaccard, bray_curtis = weighted_similarity_metrics(tel_map, teo_map)
        rows.append(
            {
                "scenario": scenario,
                "tel_fill_value": 0.0 if fill_quantile is None else round(quantile(tel_nonzero, fill_quantile) / 2, 4),
                "teo_fill_value": 0.0 if fill_quantile is None else round(quantile(teo_nonzero, fill_quantile) / 2, 4),
                "weighted_jaccard_overlap": round(weighted_jaccard, 4),
                "bray_curtis_similarity": round(bray_curtis, 4),
                "note": note,
            }
        )
        summary[f"{scenario}_weighted_jaccard_overlap"] = round(weighted_jaccard, 4)
        summary[f"{scenario}_bray_curtis_similarity"] = round(bray_curtis, 4)
    return summary, rows


def build_acetylation_covariate_sensitivity(
    membership_rows: list[dict[str, object]],
) -> tuple[dict[str, object], list[dict[str, object]]]:
    matched_rows = [row for row in membership_rows if row["role"] == "matched"]
    span_lengths = [int(row["last_residue"]) - int(row["first_residue"]) + 1 for row in matched_rows]
    log_masses = [math.log(float(row["precursor_mass"])) for row in matched_rows]
    first_residues = [int(row["first_residue"]) for row in matched_rows]

    def zscore(values: list[float]) -> list[float]:
        mean_value = statistics.mean(values)
        stdev_value = statistics.pstdev(values) or 1.0
        return [(value - mean_value) / stdev_value for value in values]

    standardized_mass = zscore(log_masses)
    standardized_span = zscore([float(value) for value in span_lengths])
    standardized_first = zscore([float(value) for value in first_residues])

    design = []
    response = []
    for row, mass_value, span_value, first_value in zip(
        matched_rows, standardized_mass, standardized_span, standardized_first
    ):
        design.append(
            [
                1.0,
                1.0 if row["is_acetylated"] == "yes" else 0.0,
                mass_value,
                span_value,
                first_value,
            ]
        )
        response.append(1 if row["functional_axis"] == "telencephalon" else 0)

    beta, covariance, converged = logistic_regression(design, response)
    acetyl_beta = beta[1]
    acetyl_se = math.sqrt(max(covariance[1][1], 1e-12))
    acetyl_z = acetyl_beta / acetyl_se
    acetyl_p = 2 * (1 - normal_cdf(abs(acetyl_z)))
    adjusted_or = math.exp(acetyl_beta)
    adjusted_low = math.exp(acetyl_beta - 1.96 * acetyl_se)
    adjusted_high = math.exp(acetyl_beta + 1.96 * acetyl_se)

    inverse_design = []
    inverse_response = []
    for row, mass_value, span_value, first_value in zip(
        matched_rows, standardized_mass, standardized_span, standardized_first
    ):
        inverse_design.append(
            [
                1.0,
                1.0 if row["functional_axis"] == "telencephalon" else 0.0,
                mass_value,
                span_value,
                first_value,
            ]
        )
        inverse_response.append(1 if row["is_acetylated"] == "yes" else 0)

    inverse_beta, inverse_covariance, inverse_converged = logistic_regression(
        inverse_design, inverse_response
    )
    inverse_region_beta = inverse_beta[1]
    inverse_region_se = math.sqrt(max(inverse_covariance[1][1], 1e-12))
    inverse_region_z = inverse_region_beta / inverse_region_se
    inverse_region_p = 2 * (1 - normal_cdf(abs(inverse_region_z)))
    inverse_region_or = math.exp(inverse_region_beta)
    inverse_region_low = math.exp(inverse_region_beta - 1.96 * inverse_region_se)
    inverse_region_high = math.exp(inverse_region_beta + 1.96 * inverse_region_se)

    n_terminal_rows = [row for row in matched_rows if int(row["first_residue"]) <= 2]
    tel_nterm = [row for row in n_terminal_rows if row["functional_axis"] == "telencephalon"]
    teo_nterm = [row for row in n_terminal_rows if row["functional_axis"] == "optic_tectum"]
    a = sum(1 for row in tel_nterm if row["is_acetylated"] == "yes")
    b = len(tel_nterm) - a
    c = sum(1 for row in teo_nterm if row["is_acetylated"] == "yes")
    d = len(teo_nterm) - c
    nterm_or, nterm_low, nterm_high = odds_ratio_with_ci(a, b, c, d, correction=0.5)
    nterm_p = fisher_one_sided_greater(a, b, c, d)

    rows = [
        {
            "scenario": "coarse_logistic_adjustment",
            "acetylation_odds_ratio": round(adjusted_or, 4),
            "ci_low": round(adjusted_low, 4),
            "ci_high": round(adjusted_high, 4),
            "p_value": round(acetyl_p, 6),
            "sample_size": len(matched_rows),
            "note": "Logistic sensitivity with region as the outcome and acetylation plus log precursor mass, sequence span length, and first-residue position as predictors.",
        },
        {
            "scenario": "first_residue_leq_2_subset",
            "acetylation_odds_ratio": round(nterm_or, 4),
            "ci_low": round(nterm_low, 4),
            "ci_high": round(nterm_high, 4),
            "p_value": round(nterm_p, 6),
            "sample_size": len(n_terminal_rows),
            "note": "Restriction to matched-marker rows with first residue at or within two residues of the N terminus.",
        },
        {
            "scenario": "inverse_logistic_region_predictor",
            "acetylation_odds_ratio": round(inverse_region_or, 4),
            "ci_low": round(inverse_region_low, 4),
            "ci_high": round(inverse_region_high, 4),
            "p_value": round(inverse_region_p, 6),
            "sample_size": len(matched_rows),
            "note": "Inverse logistic sensitivity with acetylation as the outcome and region plus log precursor mass, sequence span length, and first-residue position as predictors.",
        },
    ]
    summary = {
        "acetylation_adjusted_odds_ratio": round(adjusted_or, 4),
        "acetylation_adjusted_odds_ratio_ci_low": round(adjusted_low, 4),
        "acetylation_adjusted_odds_ratio_ci_high": round(adjusted_high, 4),
        "acetylation_adjusted_p_value": round(acetyl_p, 6),
        "acetylation_adjusted_model_converged": converged,
        "acetylation_first_residue_leq_2_odds_ratio": round(nterm_or, 4),
        "acetylation_first_residue_leq_2_ci_low": round(nterm_low, 4),
        "acetylation_first_residue_leq_2_ci_high": round(nterm_high, 4),
        "acetylation_first_residue_leq_2_p_value": round(nterm_p, 6),
        "acetylation_inverse_region_odds_ratio": round(inverse_region_or, 4),
        "acetylation_inverse_region_ci_low": round(inverse_region_low, 4),
        "acetylation_inverse_region_ci_high": round(inverse_region_high, 4),
        "acetylation_inverse_region_p_value": round(inverse_region_p, 6),
        "acetylation_inverse_model_converged": inverse_converged,
    }
    return summary, rows


def prefix_summary_keys(values: dict[str, object], prefix: str) -> dict[str, object]:
    return {f"{prefix}{key}": value for key, value in values.items()}


def build_independent_marker_panel(
    tel_rows: list[dict[str, object]], teo_rows: list[dict[str, object]]
) -> tuple[dict[str, object], dict[str, list[dict[str, object]]]]:
    (
        marker_summary,
        marker_rows,
        membership_rows,
        group_consistency_rows,
        axis_rows,
        intensity_rows,
        protein_rows,
        _ptm_marker_rows,
        leave_one_out_rows,
        sensitivity_rows,
    ) = build_marker_outputs(INDEPENDENT_MARKERS, tel_rows, teo_rows)
    permutation_summary, permutation_rows = build_marker_permutation_test(marker_rows, seed=20260330)
    protein_permutation_summary, protein_permutation_rows = build_protein_level_permutation_test(
        marker_rows, seed=20260331
    )
    baseline = next(row for row in sensitivity_rows if row["scenario"] == "baseline")
    summary = {
        "marker_groups_total": len(INDEPENDENT_MARKERS),
        "alignment_fraction": marker_summary["marker_alignment_fraction"],
        "expected_alignment_under_region_prevalence": marker_summary[
            "expected_alignment_under_region_prevalence"
        ],
        "alignment_excess_over_prevalence": marker_summary["alignment_excess_over_prevalence"],
        "odds_ratio": baseline["odds_ratio"],
        "odds_ratio_ci_low": baseline["odds_ratio_ci_low"],
        "odds_ratio_ci_high": baseline["odds_ratio_ci_high"],
        "one_sided_p_greater": baseline["one_sided_p_greater"],
        "protein_collapsed_alignment_fraction": marker_summary["protein_collapsed_alignment_fraction"],
        "protein_collapsed_odds_ratio": marker_summary["protein_collapsed_odds_ratio"],
        "protein_collapsed_one_sided_p_greater": marker_summary["protein_collapsed_one_sided_p_greater"],
    }
    summary.update(prefix_summary_keys(permutation_summary, "count_panel_"))
    summary.update(prefix_summary_keys(protein_permutation_summary, "protein_panel_"))
    return summary, {
        "marker_rows": marker_rows,
        "membership_rows": membership_rows,
        "group_consistency_rows": group_consistency_rows,
        "axis_rows": axis_rows,
        "intensity_rows": intensity_rows,
        "protein_rows": protein_rows,
        "leave_one_out_rows": leave_one_out_rows,
        "sensitivity_rows": sensitivity_rows,
        "permutation_rows": permutation_rows,
        "protein_permutation_rows": protein_permutation_rows,
    }


def build_composition_guardrails(
    tel_rows: list[dict[str, object]], teo_rows: list[dict[str, object]]
) -> tuple[dict[str, object], list[dict[str, object]]]:
    rows: list[dict[str, object]] = []
    summary: dict[str, object] = {}
    for sentinel in COMPOSITION_SENTINELS:
        genes = set(sentinel["genes"])
        tel_count = sum(1 for row in tel_rows if str(row["gene"]) in genes)
        teo_count = sum(1 for row in teo_rows if str(row["gene"]) in genes)
        total = tel_count + teo_count
        tel_share = tel_count / total if total else 0.0
        rows.append(
            {
                "panel": sentinel["panel"],
                "genes": ",".join(sorted(genes)),
                "tel_count": tel_count,
                "teo_count": teo_count,
                "tel_share": round(tel_share, 4),
                "interpretation": sentinel["interpretation"],
            }
        )
        summary[f"{sentinel['panel']}_tel_count"] = tel_count
        summary[f"{sentinel['panel']}_teo_count"] = teo_count
        summary[f"{sentinel['panel']}_tel_share"] = round(tel_share, 4)
    return summary, rows


def sentinel_panel_match(row: dict[str, object], panel: dict[str, object]) -> bool:
    gene = str(row["gene"]).lower()
    description = str(row["description_lower"]).lower()
    gene_prefixes = tuple(str(value).lower() for value in panel["gene_prefixes"])
    description_keywords = tuple(str(value).lower() for value in panel["description_keywords"])
    return gene.startswith(gene_prefixes) or any(keyword in description for keyword in description_keywords)


def build_tissue_purity_sentinel_screen(
    tel_rows: list[dict[str, object]], teo_rows: list[dict[str, object]]
) -> tuple[dict[str, object], list[dict[str, object]], list[dict[str, object]]]:
    total_intensity_by_region = {
        "telencephalon": sum(float(row["avg_intensity"]) for row in tel_rows),
        "optic_tectum": sum(float(row["avg_intensity"]) for row in teo_rows),
    }
    panel_rows: list[dict[str, object]] = []
    membership_rows: list[dict[str, object]] = []
    summary: dict[str, object] = {}

    for panel in TISSUE_SENTINEL_PANELS:
        panel_name = str(panel["panel"])
        matched_by_region = {
            "telencephalon": [row for row in tel_rows if sentinel_panel_match(row, panel)],
            "optic_tectum": [row for row in teo_rows if sentinel_panel_match(row, panel)],
        }
        tel_count = len(matched_by_region["telencephalon"])
        teo_count = len(matched_by_region["optic_tectum"])
        tel_intensity = sum(float(row["avg_intensity"]) for row in matched_by_region["telencephalon"])
        teo_intensity = sum(float(row["avg_intensity"]) for row in matched_by_region["optic_tectum"])
        total_count = tel_count + teo_count
        total_panel_intensity = tel_intensity + teo_intensity
        tel_count_share = tel_count / total_count if total_count else 0.0
        tel_intensity_share = tel_intensity / total_panel_intensity if total_panel_intensity else 0.0
        tel_region_intensity_fraction = (
            tel_intensity / total_intensity_by_region["telencephalon"]
            if total_intensity_by_region["telencephalon"]
            else 0.0
        )
        teo_region_intensity_fraction = (
            teo_intensity / total_intensity_by_region["optic_tectum"]
            if total_intensity_by_region["optic_tectum"]
            else 0.0
        )
        panel_rows.append(
            {
                "panel": panel_name,
                "gene_prefixes": ",".join(panel["gene_prefixes"]),
                "description_keywords": ",".join(panel["description_keywords"]),
                "tel_count": tel_count,
                "teo_count": teo_count,
                "tel_count_share": round(tel_count_share, 4),
                "tel_intensity": round(tel_intensity, 1),
                "teo_intensity": round(teo_intensity, 1),
                "tel_intensity_share": round(tel_intensity_share, 4),
                "tel_fraction_of_region_intensity": round(tel_region_intensity_fraction, 6),
                "teo_fraction_of_region_intensity": round(teo_region_intensity_fraction, 6),
                "interpretation": panel["interpretation"],
            }
        )
        summary[f"{panel_name}_tel_count"] = tel_count
        summary[f"{panel_name}_teo_count"] = teo_count
        summary[f"{panel_name}_tel_count_share"] = round(tel_count_share, 4)
        summary[f"{panel_name}_tel_intensity_share"] = round(tel_intensity_share, 4)
        summary[f"{panel_name}_tel_fraction_of_region_intensity"] = round(
            tel_region_intensity_fraction, 6
        )
        summary[f"{panel_name}_teo_fraction_of_region_intensity"] = round(
            teo_region_intensity_fraction, 6
        )
        for row in matched_by_region["telencephalon"] + matched_by_region["optic_tectum"]:
            membership_rows.append(
                {
                    "panel": panel_name,
                    "region": row["region"],
                    "source_table": row["source_table"],
                    "source_row": row["source_row"],
                    "protein_accession": row["protein_accession"],
                    "gene": row["gene"],
                    "protein_description": row["protein_description"],
                    "proteoform": row["proteoform"],
                    "avg_intensity": round(float(row["avg_intensity"]), 1),
                }
            )
    return summary, panel_rows, membership_rows


def build_top_intensity_restriction(
    markers: list[dict[str, object]],
    tel_rows: list[dict[str, object]],
    teo_rows: list[dict[str, object]],
    top_ns: tuple[int, ...] = (50, 100, 150),
) -> tuple[dict[str, object], list[dict[str, object]]]:
    rows: list[dict[str, object]] = []
    summary: dict[str, object] = {}
    for top_n in top_ns:
        tel_top = sorted(tel_rows, key=lambda row: float(row["avg_intensity"]), reverse=True)[:top_n]
        teo_top = sorted(teo_rows, key=lambda row: float(row["avg_intensity"]), reverse=True)[:top_n]
        tel_exact = {row["proteoform_id"] for row in tel_top}
        teo_exact = {row["proteoform_id"] for row in teo_top}
        tel_canonical = {
            (row["protein_accession"], row["canonicalized_proteoform"]) for row in tel_top
        }
        teo_canonical = {
            (row["protein_accession"], row["canonicalized_proteoform"]) for row in teo_top
        }
        tel_proteins = {row["protein_accession"] for row in tel_top}
        teo_proteins = {row["protein_accession"] for row in teo_top}
        tel_genes = {str(row["gene"]) for row in tel_top if str(row["gene"])}
        teo_genes = {str(row["gene"]) for row in teo_top if str(row["gene"])}
        marker_alignment = marker_alignment_fraction(markers, tel_top, teo_top)

        metric_values = {
            "exact_id_jaccard": jaccard(tel_exact, teo_exact),
            "canonicalized_jaccard": jaccard(tel_canonical, teo_canonical),
            "protein_jaccard": jaccard(tel_proteins, teo_proteins),
            "gene_symbol_jaccard": jaccard(tel_genes, teo_genes),
            "marker_alignment_fraction": marker_alignment,
        }
        for metric_name, value in metric_values.items():
            summary[f"top{top_n}_{metric_name}"] = round(value, 4)
        summary[f"top{top_n}_shared_exact_ids"] = len(tel_exact & teo_exact)
        summary[f"top{top_n}_shared_canonical_ids"] = len(tel_canonical & teo_canonical)
        rows.append(
            {
                "top_n_per_region": top_n,
                "tel_rows": len(tel_top),
                "teo_rows": len(teo_top),
                "shared_exact_ids": len(tel_exact & teo_exact),
                "exact_id_jaccard": round(metric_values["exact_id_jaccard"], 4),
                "shared_canonical_ids": len(tel_canonical & teo_canonical),
                "canonicalized_jaccard": round(metric_values["canonicalized_jaccard"], 4),
                "protein_jaccard": round(metric_values["protein_jaccard"], 4),
                "gene_symbol_jaccard": round(metric_values["gene_symbol_jaccard"], 4),
                "marker_alignment_fraction": round(marker_alignment, 4),
                "note": "Each region was restricted to its highest mean-duplicate-intensity rows before overlap and marker alignment were recomputed.",
            }
        )
    return summary, rows


def build_canonicalization_full_map(
    tel_rows: list[dict[str, object]], teo_rows: list[dict[str, object]]
) -> tuple[dict[str, object], list[dict[str, object]], list[dict[str, object]]]:
    rows: list[dict[str, object]] = []
    canonical_to_accessions: dict[str, set[str]] = {}
    canonical_to_regions: dict[str, set[str]] = {}
    for row in tel_rows + teo_rows:
        canonical_sequence = str(row["canonicalized_proteoform"])
        canonical_id = f"{row['protein_accession']}|{canonical_sequence}|{row['first_residue']}-{row['last_residue']}"
        rows.append(
            {
                "region": row["region"],
                "source_table": row["source_table"],
                "source_row": row["source_row"],
                "protein_accession": row["protein_accession"],
                "gene": row["gene"],
                "raw_proteoform": row["proteoform"],
                "sequence_core": proteoform_sequence_core(str(row["proteoform"])),
                "modification_tokens": proteoform_modification_tokens(str(row["proteoform"])),
                "canonicalized_sequence": canonical_sequence,
                "residue_window": f"{row['first_residue']}-{row['last_residue']}",
                "accession_plus_canonical_id": canonical_id,
            }
        )
        canonical_to_accessions.setdefault(canonical_sequence, set()).add(str(row["protein_accession"]))
        canonical_to_regions.setdefault(canonical_sequence, set()).add(str(row["region"]))

    ambiguity_rows: list[dict[str, object]] = []
    for canonical_sequence, accessions in sorted(canonical_to_accessions.items()):
        if len(accessions) <= 1:
            continue
        matching_rows = [row for row in rows if row["canonicalized_sequence"] == canonical_sequence]
        ambiguity_rows.append(
            {
                "canonicalized_sequence": canonical_sequence,
                "accession_count": len(accessions),
                "accessions": ";".join(sorted(accessions)),
                "regions": ";".join(sorted(canonical_to_regions[canonical_sequence])),
                "row_count": len(matching_rows),
                "example_genes": ";".join(sorted({str(row["gene"]) for row in matching_rows if row["gene"]})[:8]),
                "note": "Same canonicalized proteoform-like sequence appears under more than one accession; primary analysis therefore retains accession identity.",
            }
        )
    summary = {
        "canonicalization_full_map_rows": len(rows),
        "cross_accession_canonical_sequence_groups": len(ambiguity_rows),
        "cross_accession_canonical_sequence_rows": sum(int(row["row_count"]) for row in ambiguity_rows),
    }
    return summary, rows, ambiguity_rows


def build_ptm_scope_screen(
    membership_rows: list[dict[str, object]],
) -> tuple[dict[str, object], list[dict[str, object]]]:
    tel_rows = [
        row for row in membership_rows if row["functional_axis"] == "telencephalon" and row["role"] == "matched"
    ]
    teo_rows = [
        row for row in membership_rows if row["functional_axis"] == "optic_tectum" and row["role"] == "matched"
    ]
    categories = ["Acetyl", "Other mass shift"]
    rows: list[dict[str, object]] = []
    summary: dict[str, object] = {}
    p_values: list[tuple[str, float]] = []

    for category in categories:
        tel_positive = sum(1 for row in tel_rows if modification_bucket(str(row["proteoform"])) == category)
        teo_positive = sum(1 for row in teo_rows if modification_bucket(str(row["proteoform"])) == category)
        tel_negative = len(tel_rows) - tel_positive
        teo_negative = len(teo_rows) - teo_positive
        p_value = fisher_one_sided_greater(tel_positive, tel_negative, teo_positive, teo_negative)
        p_values.append((category, p_value))
        rows.append(
            {
                "category": category,
                "tel_positive_count": tel_positive,
                "teo_positive_count": teo_positive,
                "tel_fraction": round(tel_positive / len(tel_rows), 4),
                "teo_fraction": round(teo_positive / len(teo_rows), 4),
                "one_sided_p_greater": p_value,
                "note": (
                    "Acetylation is the pre-specified dominant PTM class from the source paper."
                    if category == "Acetyl"
                    else "All non-acetyl bracketed mass shifts collapsed into a single exploratory bucket."
                ),
            }
        )

    ordered = sorted(p_values, key=lambda item: item[1])
    holm_adjusted: dict[str, float] = {}
    total_tests = len(ordered)
    running_max = 0.0
    for index, (category, p_value) in enumerate(ordered):
        adjusted = min(1.0, p_value * (total_tests - index))
        running_max = max(running_max, adjusted)
        holm_adjusted[category] = running_max

    for row in rows:
        category = str(row["category"])
        row["holm_adjusted_p"] = holm_adjusted[category]
        summary[f"ptm_{category.lower().replace(' ', '_')}_holm_adjusted_p"] = round(
            holm_adjusted[category], 6
        )
        summary[f"ptm_{category.lower().replace(' ', '_')}_tel_fraction"] = float(row["tel_fraction"])
        summary[f"ptm_{category.lower().replace(' ', '_')}_teo_fraction"] = float(row["teo_fraction"])

    return summary, rows


def build_traceability(
    payload: dict[str, object],
    markers: list[dict[str, object]],
    source_metrics: dict[str, object],
    marker_rows: list[dict[str, object]],
) -> dict[str, object]:
    evidence_fields: dict[str, object] = {}
    region_totals = dict(payload["region_totals"])
    for key, value in region_totals.items():
        evidence_fields[f"region_totals.{key}"] = {
            "value": value,
            "article_location": ARTICLE_LOCATIONS["region_totals"]
            if "duplicate" not in key and "high_water_mark" not in key and "cells_per" not in key
            else ARTICLE_LOCATIONS["technical_sensitivity"],
            "local_source_tables": [
                "data/source_tables/Proteoform_ID_Tel2.xlsx",
                "data/source_tables/proteoform_ID_Teo2.xlsx",
            ],
        }
    for ptm_key, value in dict(payload["ptm_totals"]).items():
        evidence_fields[f"ptm_totals.{ptm_key}"] = {
            "value": value,
            "article_location": ARTICLE_LOCATIONS["ptm_totals"],
            "local_source_tables": [
                "data/source_tables/Proteoform_ID_Tel2.xlsx",
                "data/source_tables/proteoform_ID_Teo2.xlsx",
            ],
        }
    for marker in markers:
        gene = str(marker["gene"])
        source_row = next(row for row in marker_rows if row["gene"] == gene)
        evidence_fields[f"marker_counts.{gene}.tel_count"] = {
            "value": int(source_row["tel_count"]),
            "article_location": ARTICLE_LOCATIONS["marker_panel"],
            "local_source_tables": [
                "data/source_tables/Proteoform_ID_Tel2.xlsx",
                "results/marker_family_membership.csv",
            ],
            "match_rule": source_row["match_rule"],
        }
        evidence_fields[f"marker_counts.{gene}.teo_count"] = {
            "value": int(source_row["teo_count"]),
            "article_location": ARTICLE_LOCATIONS["marker_panel"],
            "local_source_tables": [
                "data/source_tables/proteoform_ID_Teo2.xlsx",
                "results/marker_family_membership.csv",
            ],
            "match_rule": source_row["match_rule"],
        }

    evidence_fields["derived.source_table_shared_proteoforms"] = {
        "value": int(source_metrics["source_table_shared_proteoforms"]),
        "article_location": (
            "Derived from exact accession+proteoform intersections in the released Tel2 and Teo2 tables; "
            "contrast with the article's published aggregate value of 35 shared proteoforms."
        ),
        "local_source_tables": [
            "data/source_tables/Proteoform_ID_Tel2.xlsx",
            "data/source_tables/proteoform_ID_Teo2.xlsx",
            "results/source_table_shared_ids.csv",
        ],
    }

    return {
        "article_reference": {
            "pmcid": "PMC9066772",
            "note": "Traceability references the published Molecular Omics article and the released PRIDE region tables.",
        },
        "evidence_fields": evidence_fields,
        "review_relevant_files": [
            "results/source_table_metrics.json",
            "results/source_table_overlap_metrics.csv",
            "results/abundance_normalization_sensitivity.csv",
            "results/run_pair_similarity.csv",
            "results/gene_symbol_sensitivity.csv",
            "results/overlap_bootstrap_intervals.csv",
            "results/presence_overlap_significance.csv",
            "results/discrepancy_diagnostic.csv",
            "results/canonicalization_rule_sensitivity.csv",
            "results/canonicalization_examples.csv",
            "results/canonicalization_full_map.csv",
            "results/cross_accession_ambiguities.csv",
            "results/occupancy_detectability_model.csv",
            "results/detectability_stratified_sensitivity.csv",
            "results/misidentification_sensitivity.csv",
            "results/source_table_shared_ids.csv",
            "results/marker_family_membership.csv",
            "results/motor_family_breakdown.csv",
            "results/tissue_purity_sentinels.csv",
            "results/tissue_purity_sentinel_membership.csv",
            "results/top_intensity_restriction.csv",
            "results/marker_permutation_test.csv",
            "results/protein_level_permutation_test.csv",
            "results/composition_guardrails.csv",
            "results/ptm_scope_screen.csv",
            "results/ptm_detectability_proxies.csv",
            "results/mnar_similarity_sensitivity.csv",
            "results/acetylation_covariate_sensitivity.csv",
            "results/independent_panel_marker_bias.csv",
        ],
    }


def main() -> None:
    payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    article_totals = dict(payload["region_totals"])
    markers = list(payload["marker_counts"])
    ptms = dict(payload["ptm_totals"])

    tel_rows = load_source_rows("Proteoform_ID_Tel2.xlsx", "telencephalon")
    teo_rows = load_source_rows("proteoform_ID_Teo2.xlsx", "optic_tectum")

    source_metrics, overlap_rows, shared_rows, source_rows, abundance_rows, discrepancy_rows = (
        build_source_table_metrics(article_totals, tel_rows, teo_rows)
    )
    (
        marker_summary,
        marker_rows,
        membership_rows,
        group_consistency_rows,
        axis_rows,
        intensity_rows,
        protein_rows,
        ptm_marker_rows,
        leave_one_out_rows,
        sensitivity_rows,
    ) = build_marker_outputs(markers, tel_rows, teo_rows)
    permutation_summary, permutation_rows = build_marker_permutation_test(marker_rows)
    protein_permutation_summary, protein_permutation_rows = build_protein_level_permutation_test(marker_rows)
    composition_summary, composition_rows = build_composition_guardrails(tel_rows, teo_rows)
    tissue_sentinel_summary, tissue_sentinel_rows, tissue_sentinel_membership_rows = (
        build_tissue_purity_sentinel_screen(tel_rows, teo_rows)
    )
    ptm_scope_summary, ptm_scope_rows = build_ptm_scope_screen(membership_rows)
    overlap_bootstrap_summary, overlap_bootstrap_rows = bootstrap_overlap_intervals(tel_rows, teo_rows)
    run_pair_summary, run_pair_rows = build_run_pair_similarity(tel_rows, teo_rows)
    canonicalization_summary, canonicalization_rows = build_canonicalization_rule_sensitivity(tel_rows, teo_rows)
    canonicalization_example_rows = build_canonicalization_examples(tel_rows, teo_rows)
    canonical_full_summary, canonical_full_rows, cross_accession_rows = build_canonicalization_full_map(
        tel_rows, teo_rows
    )
    overlap_significance_summary, overlap_significance_rows = build_presence_overlap_significance(
        tel_rows, teo_rows
    )
    rarefaction_summary, rarefaction_rows = build_identification_count_rarefaction(
        markers, tel_rows, teo_rows
    )
    top_intensity_summary, top_intensity_rows = build_top_intensity_restriction(
        markers, tel_rows, teo_rows
    )
    occupancy_summary, occupancy_rows = build_occupancy_detectability_model(tel_rows, teo_rows)
    detectability_stratified_summary, detectability_stratified_rows = build_detectability_stratified_sensitivity(
        tel_rows, teo_rows
    )
    misidentification_summary, misidentification_rows = build_misidentification_sensitivity_bounds(
        tel_rows, teo_rows, source_metrics["source_table_protein_overlap_fraction"]
    )
    gene_symbol_summary, gene_symbol_rows = build_gene_symbol_sensitivity(
        tel_rows, teo_rows, membership_rows
    )
    motor_family_summary, motor_family_rows = build_motor_family_breakdown(membership_rows)
    ptm_detectability_summary, ptm_detectability_rows = build_ptm_detectability_proxy_screen(membership_rows)
    mnar_similarity_summary, mnar_similarity_rows = build_mnar_similarity_sensitivity(tel_rows, teo_rows)
    acetylation_adjusted_summary, acetylation_adjusted_rows = build_acetylation_covariate_sensitivity(
        membership_rows
    )
    independent_panel_summary, independent_panel_outputs = build_independent_marker_panel(tel_rows, teo_rows)

    technical_rows = [
        {
            "region": "telencephalon",
            "duplicate_mean": article_totals["tel_duplicate_mean"],
            "duplicate_sd": article_totals["tel_duplicate_sd"],
            "cv": round(article_totals["tel_duplicate_sd"] / article_totals["tel_duplicate_mean"], 4),
            "duplicate_recovery_fraction": round(
                article_totals["tel_duplicate_mean"] / article_totals["telencephalon_proteoforms"],
                4,
            ),
        },
        {
            "region": "optic_tectum",
            "duplicate_mean": article_totals["teo_duplicate_mean"],
            "duplicate_sd": article_totals["teo_duplicate_sd"],
            "cv": round(article_totals["teo_duplicate_sd"] / article_totals["teo_duplicate_mean"], 4),
            "duplicate_recovery_fraction": round(
                article_totals["teo_duplicate_mean"] / article_totals["optic_tectum_proteoforms"],
                4,
            ),
        },
    ]

    total_ptm = ptms["total_proteoforms"]
    ptm_rows = [
        {
            "modification": modification,
            "count": value,
            "fraction_of_total": round(value / total_ptm, 4),
        }
        for modification, value in ptms.items()
    ]

    summary = {
        "telencephalon_proteoforms": article_totals["telencephalon_proteoforms"],
        "optic_tectum_proteoforms": article_totals["optic_tectum_proteoforms"],
        "shared_proteoforms": article_totals["shared_proteoforms"],
        "union_proteoforms": int(
            article_totals["telencephalon_proteoforms"]
            + article_totals["optic_tectum_proteoforms"]
            - article_totals["shared_proteoforms"]
        ),
        "jaccard_overlap": round(
            article_totals["shared_proteoforms"]
            / (
                article_totals["telencephalon_proteoforms"]
                + article_totals["optic_tectum_proteoforms"]
                - article_totals["shared_proteoforms"]
            ),
            4,
        ),
        "telencephalon_unique": article_totals["telencephalon_proteoforms"] - article_totals["shared_proteoforms"],
        "optic_tectum_unique": article_totals["optic_tectum_proteoforms"] - article_totals["shared_proteoforms"],
        "telencephalon_specialization_fraction": round(
            (
                article_totals["telencephalon_proteoforms"] - article_totals["shared_proteoforms"]
            )
            / article_totals["telencephalon_proteoforms"],
            4,
        ),
        "optic_tectum_specialization_fraction": round(
            (
                article_totals["optic_tectum_proteoforms"] - article_totals["shared_proteoforms"]
            )
            / article_totals["optic_tectum_proteoforms"],
            4,
        ),
        "protein_overlap_fraction": round(
            article_totals["protein_overlap"] / article_totals["protein_union"], 4
        ),
        "teo_to_tel_ratio": round(
            article_totals["optic_tectum_proteoforms"] / article_totals["telencephalon_proteoforms"],
            4,
        ),
        "modification_fraction": round(ptms["modified_total"] / ptms["total_proteoforms"], 4),
        "n_terminal_acetylation_fraction_of_modified": round(
            ptms["n_terminal_acetylated"] / ptms["modified_total"], 4
        ),
        "single_run_high_water_mark": article_totals["single_run_high_water_mark"],
        "cells_per_section_estimate": article_totals["cells_per_section_estimate"],
        "cells_per_run_estimate": article_totals["cells_per_run_estimate"],
        "single_run_proteoforms_per_estimated_cell": round(
            article_totals["single_run_high_water_mark"] / article_totals["cells_per_run_estimate"],
            4,
        ),
        "protein_to_proteoform_overlap_ratio": round(
            (article_totals["protein_overlap"] / article_totals["protein_union"])
            / (
                article_totals["shared_proteoforms"]
                / (
                    article_totals["telencephalon_proteoforms"]
                    + article_totals["optic_tectum_proteoforms"]
                    - article_totals["shared_proteoforms"]
                )
            ),
            4,
        ),
    }
    summary.update(source_metrics)
    summary.update(marker_summary)
    summary.update(permutation_summary)
    summary.update(protein_permutation_summary)
    summary.update(composition_summary)
    summary.update(tissue_sentinel_summary)
    summary.update(ptm_scope_summary)
    summary.update(overlap_bootstrap_summary)
    summary.update(run_pair_summary)
    summary.update(canonicalization_summary)
    summary["canonicalization_examples_count"] = len(canonicalization_example_rows)
    summary.update(canonical_full_summary)
    summary.update(overlap_significance_summary)
    summary.update(rarefaction_summary)
    summary.update(top_intensity_summary)
    summary.update(occupancy_summary)
    summary.update(detectability_stratified_summary)
    summary.update(misidentification_summary)
    summary.update(gene_symbol_summary)
    summary.update(motor_family_summary)
    summary.update(ptm_detectability_summary)
    summary.update(mnar_similarity_summary)
    summary.update(acetylation_adjusted_summary)
    summary.update(prefix_summary_keys(independent_panel_summary, "independent_panel_"))

    traceability = build_traceability(payload, markers, source_metrics, marker_rows)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    write_json(RESULTS_DIR / "summary_metrics.json", summary)
    write_json(
        RESULTS_DIR / "functional_test.json",
        {
            "table": {
                "tel_axis_in_tel": axis_rows[0]["matched_count"],
                "tel_axis_in_teo": axis_rows[0]["spillover_count"],
                "teo_axis_in_tel": axis_rows[1]["spillover_count"],
                "teo_axis_in_teo": axis_rows[1]["matched_count"],
            },
            "odds_ratio": summary["odds_ratio"],
            "odds_ratio_ci_low": summary["odds_ratio_ci_low"],
            "odds_ratio_ci_high": summary["odds_ratio_ci_high"],
            "one_sided_p_greater": next(
                float(row["one_sided_p_greater"]) for row in sensitivity_rows if row["scenario"] == "baseline"
            ),
        },
    )
    write_json(RESULTS_DIR / "source_table_metrics.json", source_metrics)
    write_json(DATA_DIR / "evidence_traceability.json", traceability)

    write_csv(
        RESULTS_DIR / "region_summary.csv",
        [{"metric": key, "value": value} for key, value in summary.items()],
        ["metric", "value"],
    )
    write_csv(
        RESULTS_DIR / "source_table_overlap_metrics.csv",
        overlap_rows,
        ["scenario", "shared_proteoforms", "union_proteoforms", "jaccard_overlap", "sorensen_overlap", "note"],
    )
    write_csv(
        RESULTS_DIR / "abundance_normalization_sensitivity.csv",
        abundance_rows,
        ["normalization", "weighted_jaccard_overlap", "bray_curtis_similarity", "note"],
    )
    write_csv(
        RESULTS_DIR / "run_pair_similarity.csv",
        run_pair_rows,
        [
            "tel_run",
            "teo_run",
            "weighted_jaccard_overlap",
            "bray_curtis_similarity",
            "per_run_total_normalized_weighted_jaccard_overlap",
            "per_run_total_normalized_bray_curtis_similarity",
        ],
    )
    write_csv(
        RESULTS_DIR / "gene_symbol_sensitivity.csv",
        gene_symbol_rows,
        [
            "analysis",
            "shared_count",
            "union_count",
            "jaccard_overlap",
            "expected_jaccard_under_independence",
            "centered_jaccard",
            "lower_tail_p",
            "lower_tail_neg_log10_p",
            "alignment_fraction",
            "odds_ratio",
            "odds_ratio_ci_low",
            "odds_ratio_ci_high",
            "note",
        ],
    )
    write_csv(
        RESULTS_DIR / "overlap_bootstrap_intervals.csv",
        overlap_bootstrap_rows,
        ["metric", "bootstrap_trials", "low_95", "median", "high_95", "note"],
    )
    write_csv(
        RESULTS_DIR / "presence_overlap_significance.csv",
        overlap_significance_rows,
        [
            "representation",
            "tel_count",
            "teo_count",
            "shared_count",
            "universe_count",
            "observed_jaccard",
            "expected_jaccard_under_independence",
            "centered_jaccard",
            "fixed_margin_expected_shared",
            "fixed_margin_jaccard_mean",
            "fixed_margin_jaccard_low_95",
            "fixed_margin_jaccard_high_95",
            "lower_tail_p",
            "lower_tail_neg_log10_p",
            "note",
        ],
    )
    write_csv(
        RESULTS_DIR / "identification_count_rarefaction.csv",
        rarefaction_rows,
        [
            "metric",
            "trials",
            "seed",
            "sampled_region",
            "sample_size",
            "low_95",
            "median",
            "high_95",
            "observed_full",
            "note",
        ],
    )
    write_csv(
        RESULTS_DIR / "discrepancy_diagnostic.csv",
        discrepancy_rows,
        ["comparison_basis", "shared_count", "union_count", "jaccard_overlap", "note"],
    )
    write_csv(
        RESULTS_DIR / "source_table_shared_ids.csv",
        shared_rows,
        ["protein_accession", "gene", "proteoform", "tel_avg_intensity", "teo_avg_intensity", "tel_source_row", "teo_source_row"],
    )
    write_csv(
        RESULTS_DIR / "source_table_proteoforms.csv",
        source_rows,
        [
            "region",
            "source_table",
            "source_row",
            "protein_accession",
            "gene",
            "protein_description",
            "first_residue",
            "last_residue",
            "proteoform",
            "avg_intensity",
            "match_status",
            "is_acetylated",
        ],
    )
    write_csv(
        RESULTS_DIR / "marker_bias.csv",
        marker_rows,
        [
            "gene",
            "label",
            "functional_axis",
            "match_rule",
            "tel_count",
            "teo_count",
            "matched_count",
            "spillover_count",
            "matched_share",
            "log2_tel_over_teo_plus1",
            "tel_avg_intensity",
            "teo_avg_intensity",
            "tel_protein_count",
            "teo_protein_count",
            "tel_acetylated_count",
            "teo_acetylated_count",
            "interpretation",
        ],
    )
    write_csv(
        RESULTS_DIR / "marker_family_membership.csv",
        membership_rows,
        [
            "family",
            "family_key",
            "functional_axis",
            "match_rule",
            "region",
            "role",
            "source_table",
            "source_row",
            "protein_accession",
            "gene",
            "protein_description",
            "first_residue",
            "last_residue",
            "proteoform",
            "precursor_mass",
            "avg_intensity",
            "is_acetylated",
        ],
    )
    write_csv(
        RESULTS_DIR / "motor_family_breakdown.csv",
        motor_family_rows,
        [
            "family_key",
            "gene",
            "protein_accession",
            "protein_description",
            "annotation_class",
            "telencephalon_count",
            "optic_tectum_count",
            "matched_count",
            "spillover_count",
            "source_rows",
        ],
    )
    write_csv(
        RESULTS_DIR / "group_consistency.csv",
        group_consistency_rows,
        ["label", "functional_axis", "matched_share", "favors_expected_region"],
    )
    write_csv(
        RESULTS_DIR / "axis_summary.csv",
        axis_rows,
        [
            "functional_axis",
            "matched_count",
            "spillover_count",
            "alignment_fraction",
            "wilson_low",
            "wilson_high",
            "expected_fraction_under_region_prevalence",
            "alignment_lift_over_prevalence",
        ],
    )
    write_csv(
        RESULTS_DIR / "marker_intensity_alignment.csv",
        intensity_rows,
        ["functional_axis", "matched_intensity", "spillover_intensity", "matched_fraction"],
    )
    write_csv(
        RESULTS_DIR / "marker_protein_collapse.csv",
        protein_rows,
        ["functional_axis", "matched_proteins", "spillover_proteins", "matched_fraction"],
    )
    write_csv(
        RESULTS_DIR / "marker_ptm_summary.csv",
        ptm_marker_rows,
        ["subset", "acetylated_count", "non_acetylated_count", "total_count", "acetylated_fraction"],
    )
    write_csv(
        RESULTS_DIR / "leave_one_out_alignment.csv",
        leave_one_out_rows,
        ["removed_marker", "remaining_alignment_fraction"],
    )
    write_csv(
        RESULTS_DIR / "marker_permutation_test.csv",
        permutation_rows,
        ["metric", "value", "note"],
    )
    write_csv(
        RESULTS_DIR / "protein_level_permutation_test.csv",
        protein_permutation_rows,
        ["metric", "value", "note"],
    )
    write_csv(
        RESULTS_DIR / "composition_guardrails.csv",
        composition_rows,
        ["panel", "genes", "tel_count", "teo_count", "tel_share", "interpretation"],
    )
    write_csv(
        RESULTS_DIR / "tissue_purity_sentinels.csv",
        tissue_sentinel_rows,
        [
            "panel",
            "gene_prefixes",
            "description_keywords",
            "tel_count",
            "teo_count",
            "tel_count_share",
            "tel_intensity",
            "teo_intensity",
            "tel_intensity_share",
            "tel_fraction_of_region_intensity",
            "teo_fraction_of_region_intensity",
            "interpretation",
        ],
    )
    write_csv(
        RESULTS_DIR / "tissue_purity_sentinel_membership.csv",
        tissue_sentinel_membership_rows,
        [
            "panel",
            "region",
            "source_table",
            "source_row",
            "protein_accession",
            "gene",
            "protein_description",
            "proteoform",
            "avg_intensity",
        ],
    )
    write_csv(
        RESULTS_DIR / "top_intensity_restriction.csv",
        top_intensity_rows,
        [
            "top_n_per_region",
            "tel_rows",
            "teo_rows",
            "shared_exact_ids",
            "exact_id_jaccard",
            "shared_canonical_ids",
            "canonicalized_jaccard",
            "protein_jaccard",
            "gene_symbol_jaccard",
            "marker_alignment_fraction",
            "note",
        ],
    )
    write_csv(
        RESULTS_DIR / "sensitivity_scenarios.csv",
        sensitivity_rows,
        [
            "scenario",
            "matched_count",
            "spillover_count",
            "alignment_fraction",
            "odds_ratio",
            "odds_ratio_ci_low",
            "odds_ratio_ci_high",
            "one_sided_p_greater",
            "notes",
        ],
    )
    write_csv(
        RESULTS_DIR / "technical_replicate_summary.csv",
        technical_rows,
        ["region", "duplicate_mean", "duplicate_sd", "cv", "duplicate_recovery_fraction"],
    )
    write_csv(
        RESULTS_DIR / "ptm_summary.csv",
        ptm_rows,
        ["modification", "count", "fraction_of_total"],
    )
    write_csv(
        RESULTS_DIR / "ptm_scope_screen.csv",
        ptm_scope_rows,
        [
            "category",
            "tel_positive_count",
            "teo_positive_count",
            "tel_fraction",
            "teo_fraction",
            "one_sided_p_greater",
            "holm_adjusted_p",
            "note",
        ],
    )
    write_csv(
        RESULTS_DIR / "canonicalization_rule_sensitivity.csv",
        canonicalization_rows,
        ["rule", "shared_count", "union_count", "jaccard_overlap", "note"],
    )
    write_csv(
        RESULTS_DIR / "canonicalization_examples.csv",
        canonicalization_example_rows,
        [
            "protein_accession",
            "telencephalon_proteoform",
            "optic_tectum_proteoform",
            "telencephalon_sequence_core",
            "optic_tectum_sequence_core",
            "telencephalon_modification_tokens",
            "optic_tectum_modification_tokens",
            "canonicalized_sequence",
            "telencephalon_residue_window",
            "optic_tectum_residue_window",
            "standards_note",
            "note",
        ],
    )
    write_csv(
        RESULTS_DIR / "canonicalization_full_map.csv",
        canonical_full_rows,
        [
            "region",
            "source_table",
            "source_row",
            "protein_accession",
            "gene",
            "raw_proteoform",
            "sequence_core",
            "modification_tokens",
            "canonicalized_sequence",
            "residue_window",
            "accession_plus_canonical_id",
        ],
    )
    write_csv(
        RESULTS_DIR / "cross_accession_ambiguities.csv",
        cross_accession_rows,
        [
            "canonicalized_sequence",
            "accession_count",
            "accessions",
            "regions",
            "row_count",
            "example_genes",
            "note",
        ],
    )
    write_csv(
        RESULTS_DIR / "occupancy_detectability_model.csv",
        occupancy_rows,
        [
            "section",
            "region",
            "exact_id_count",
            "single_run_only_count",
            "duplicate_reobserved_count",
            "per_run_detection_probability",
            "detected_at_least_once_probability",
            "latent_richness_estimate",
            "adjusted_shared_exact_ids",
            "adjusted_jaccard_overlap",
            "note",
        ],
    )
    write_csv(
        RESULTS_DIR / "detectability_stratified_sensitivity.csv",
        detectability_stratified_rows,
        [
            "scheme",
            "section",
            "region",
            "bin",
            "exact_id_count",
            "single_run_only_count",
            "duplicate_reobserved_count",
            "per_run_detection_probability",
            "detected_at_least_once_probability",
            "latent_richness_estimate",
            "adjusted_shared_exact_ids",
            "adjusted_jaccard_overlap",
            "fallback_used",
            "note",
        ],
    )
    write_csv(
        RESULTS_DIR / "misidentification_sensitivity.csv",
        misidentification_rows,
        [
            "scenario_type",
            "scenario",
            "assumed_error_rate",
            "reclassified_pairs",
            "adjusted_shared_count",
            "adjusted_union_count",
            "adjusted_jaccard_overlap",
            "tel_unique_error_fraction_needed",
            "teo_unique_error_fraction_needed",
            "note",
        ],
    )
    write_csv(
        RESULTS_DIR / "ptm_detectability_proxies.csv",
        ptm_detectability_rows,
        [
            "metric",
            "tel_mean",
            "teo_mean",
            "tel_median",
            "teo_median",
            "absolute_mean_difference",
            "permutation_p_two_sided",
            "note",
        ],
    )
    write_csv(
        RESULTS_DIR / "mnar_similarity_sensitivity.csv",
        mnar_similarity_rows,
        [
            "scenario",
            "tel_fill_value",
            "teo_fill_value",
            "weighted_jaccard_overlap",
            "bray_curtis_similarity",
            "note",
        ],
    )
    write_csv(
        RESULTS_DIR / "acetylation_covariate_sensitivity.csv",
        acetylation_adjusted_rows,
        ["scenario", "acetylation_odds_ratio", "ci_low", "ci_high", "p_value", "sample_size", "note"],
    )
    write_csv(
        RESULTS_DIR / "independent_panel_marker_bias.csv",
        independent_panel_outputs["marker_rows"],
        [
            "gene",
            "label",
            "functional_axis",
            "match_rule",
            "tel_count",
            "teo_count",
            "matched_count",
            "spillover_count",
            "matched_share",
            "log2_tel_over_teo_plus1",
            "tel_avg_intensity",
            "teo_avg_intensity",
            "tel_protein_count",
            "teo_protein_count",
            "tel_acetylated_count",
            "teo_acetylated_count",
            "interpretation",
        ],
    )
    write_csv(
        RESULTS_DIR / "independent_panel_membership.csv",
        independent_panel_outputs["membership_rows"],
        [
            "family",
            "family_key",
            "functional_axis",
            "match_rule",
            "region",
            "role",
            "source_table",
            "source_row",
            "protein_accession",
            "gene",
            "protein_description",
            "first_residue",
            "last_residue",
            "proteoform",
            "precursor_mass",
            "avg_intensity",
            "is_acetylated",
        ],
    )
    write_csv(
        RESULTS_DIR / "independent_panel_axis_summary.csv",
        independent_panel_outputs["axis_rows"],
        [
            "functional_axis",
            "matched_count",
            "spillover_count",
            "alignment_fraction",
            "wilson_low",
            "wilson_high",
            "expected_fraction_under_region_prevalence",
            "alignment_lift_over_prevalence",
        ],
    )
    write_csv(
        RESULTS_DIR / "independent_panel_permutation_test.csv",
        independent_panel_outputs["permutation_rows"],
        ["metric", "value", "note"],
    )
    write_csv(
        RESULTS_DIR / "independent_panel_protein_permutation_test.csv",
        independent_panel_outputs["protein_permutation_rows"],
        ["metric", "value", "note"],
    )
    write_csv(
        RESULTS_DIR / "independent_panel_sensitivity.csv",
        independent_panel_outputs["sensitivity_rows"],
        [
            "scenario",
            "matched_count",
            "spillover_count",
            "alignment_fraction",
            "odds_ratio",
            "odds_ratio_ci_low",
            "odds_ratio_ci_high",
            "one_sided_p_greater",
            "notes",
        ],
    )


if __name__ == "__main__":
    main()
