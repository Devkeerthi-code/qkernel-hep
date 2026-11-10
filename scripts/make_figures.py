"""Figures, summary table and hypothesis tests for the qkernel-hep study.

    python scripts/make_figures.py        # all figures + results/summary_table.csv + results/h2_analysis.json

Inputs: results/{main_grid,n_sweep,big_qubits,fs_gbdt}/runs.jsonl, results/noise.csv,
results/hardware/*.json, and (for Fig. 5 and the angle-spread diagnostic) the ATLAS CSV in data/.
Outputs go to results/figures/ as PDF and PNG.

Hypotheses H1-H4 are read verbatim from docs/hypotheses.md. They were written in the project guide on
7 Nov 2026, before any experiment was run, but were not formally pre-registered. Each is tested exactly
as its "Test:" line says, on the N_train = 500 PCA grid (main_grid + big_qubits), and again on the
n = 4 and n = 8 slices with PCA replaced by boosted-tree feature selection (fs_gbdt) as a robustness check.

Significance rule: a seed-paired difference whose mean is within one seed-to-seed standard deviation
(ddof=1) is "not significant". With 5 seeds, |mean| > 1 sd is a paired t of about 2.2 (two-sided
p ~ 0.09), a lenient bar. Correlations: 95% bootstrap CI over configurations; a CI containing 0 is not
significant. Configurations share data seeds, so these CIs are somewhat optimistic.

Operational choices (not part of the hypotheses): concentration = off-diagonal variance of the training
kernel; the headline g is the regularised g at lambda = 0.01 (the one in Fig. 4), with lambda = 0, 1e-3
and 1e-1 reported alongside; "best classical" in runs.jsonl is the max of three models' *test* AUCs,
which flatters the classical side -- the CV-selected classical model is stored only for runs made after
fs_gbdt was added, and the size of that bias is reported from those runs.
"""
from __future__ import annotations

import json
import re
import sys
import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.ticker import FixedLocator, NullFormatter, NullLocator  # noqa: E402
from scipy import stats  # noqa: E402
from sklearn.metrics import roc_auc_score  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src import metrics  # noqa: E402

RES = ROOT / "results"
FIG = RES / "figures"
EXPERIMENTS = ["main_grid", "n_sweep", "big_qubits", "fs_gbdt"]
MAIN = ["main_grid", "big_qubits"]  # the N_train = 500 PCA grid on which H1-H4 are judged
KEYS = ["experiment", "n_qubits", "n_train", "feature_map", "reps", "bandwidth"]
FMS = [("z", 2), ("zz", 1), ("zz", 2)]
FM_LABEL = {("z", 2): "Z map, reps 2", ("zz", 1): "ZZ map, reps 1", ("zz", 2): "ZZ map, reps 2"}
LAMBDAS = [("g", 0.0), ("g_lam0.001", 1e-3), ("g_lam0.01", 1e-2), ("g_lam0.1", 1e-1)]
G_HEADLINE = "g_lam0.01"
N_BOOT = 2000
PROVENANCE = ("written in the project guide on 7 Nov 2026, before any experiment was run; "
              "not formally pre-registered")

# ---- palette (validated with the dataviz validator: categorical adjacent pairs, first-3 all pairs,
#      ordinal blue ramp). Low-contrast slots always carry a marker + legend; the CSV is the table view.
INK, INK2, GRID, SURFACE = "#0b0b0b", "#52514e", "#e4e3de", "#fcfcfb"
CAT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]       # slots 1-5
ORDINAL = ["#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#0d366b"]   # light -> dark
SEQ = LinearSegmentedColormap.from_list("blue_seq", ["#86b6ef", "#3987e5", "#1c5cab", "#0d366b"])      # scatter
SEQ_HEAT = LinearSegmentedColormap.from_list("blue_heat", ["#fcfcfb", "#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"])
FM_COLOR = {fm: CAT[i] for i, fm in enumerate(FMS)}
FM_MARKER = {("z", 2): "o", ("zz", 1): "s", ("zz", 2): "^"}
MODELS = [("qsvm_auc", "Fidelity QSVM", "o"), ("pqk_auc", "Projected QSVM", "s"),
          ("logreg_auc", "Logistic regression", "D"), ("rbf_auc", "RBF SVM", "^"),
          ("gbdt_auc", "Boosted trees", "v")]


def style():
    plt.rcParams.update({
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
        "axes.edgecolor": INK2, "axes.labelcolor": INK, "text.color": INK, "xtick.color": INK2,
        "ytick.color": INK2, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
        "axes.spines.top": False, "axes.spines.right": False, "axes.titlesize": 10,
        "axes.labelsize": 9, "xtick.labelsize": 8, "ytick.labelsize": 8, "legend.fontsize": 8,
        "legend.frameon": False, "lines.linewidth": 2, "lines.markersize": 6, "font.size": 9,
        "pdf.fonttype": 42, "errorbar.capsize": 2})


def save(fig, name: str) -> list[Path]:
    FIG.mkdir(parents=True, exist_ok=True)
    out = []
    for ext in ("pdf", "png"):
        p = FIG / f"{name}.{ext}"
        # no creation timestamp in the PDF, so regenerating identical figures leaves git clean
        fig.savefig(p, dpi=200, bbox_inches="tight", metadata={"CreationDate": None} if ext == "pdf" else None)
        out.append(p)
    if fig._suptitle is not None:  # title-free copy for the report, whose captions carry the titles
        fig._suptitle.set_visible(False)
        (FIG / "notitle").mkdir(exist_ok=True)
        p = FIG / "notitle" / f"{name}.pdf"
        fig.savefig(p, bbox_inches="tight", metadata={"CreationDate": None})
        out.append(p)
    plt.close(fig)
    return out


def load_hypotheses(path: Path = ROOT / "docs" / "hypotheses.md") -> dict:
    """H1-H4 exactly as written in docs/hypotheses.md (the quoted block), line breaks joined by spaces."""
    quoted = " ".join(line[1:].strip() for line in path.read_text(encoding="utf-8").splitlines()
                      if line.startswith(">"))
    out = {}
    for m in re.finditer(r"\*\*(H\d):\*\*\s*(.*?)\s*Test:\s*(.*?)(?=\s*\*\*H\d:\*\*|$)", quoted):
        out[m.group(1)] = {"statement": m.group(2).strip(), "test": m.group(3).strip()}
    if sorted(out) != ["H1", "H2", "H3", "H4"]:
        raise ValueError(f"could not parse H1-H4 from {path}")
    return out


# ------------------------------------------------------------------------------------------ data
def load_runs() -> pd.DataFrame:
    frames = []
    for e in EXPERIMENTS:
        path = RES / e / "runs.jsonl"
        if path.exists():
            df = pd.DataFrame([json.loads(line) for line in path.read_text().splitlines() if line])
            df["experiment"] = e
            frames.append(df)
    df = pd.concat(frames, ignore_index=True)
    df["fm"] = list(zip(df.feature_map, df.reps))
    df["log_var"] = np.log10(df.q_offdiag_var)
    df["log_s_ratio"] = np.log10(df.s_classical / df.s_quantum)
    df["pqk_gap_vs_rbf"] = df.pqk_auc - df.rbf_auc
    if "reduction" not in df:
        df["reduction"] = "pca"
    df["reduction"] = df["reduction"].fillna("pca")
    return df


def load_all() -> dict:
    runs = load_runs()
    noise = pd.read_csv(RES / "noise.csv") if (RES / "noise.csv").exists() else None
    hw = []
    for f in sorted((RES / "hardware").glob("*_*_2*.json")):
        h = json.loads(f.read_text())
        if "fidelity" in h:
            hw.append({"file": f.name, "mode": h["mode"], "backend": h["backend"], "c": h["config"]["c"],
                       "n": h["config"]["n"], "kind": h["config"]["kind"], "reps": h["config"]["reps"],
                       "shots": h["config"]["shots"], "auc_exact": h["fidelity"]["auc_exact"],
                       "auc_hardware": h["fidelity"]["auc_hardware"],
                       "pqk_auc_exact": h["projected"]["auc_exact"], "pqk_auc_hardware": h["projected"]["auc_hardware"],
                       "kernel_mae_train": h["fidelity"]["kernel_mae_train"], "quantum_seconds": h.get("quantum_seconds")})
    return {"runs": runs, "noise": noise, "hardware": pd.DataFrame(hw)}


def label_diff(mean: float, sd: float, pos="quantum better", neg="classical better") -> str:
    if not np.isfinite(sd) or abs(mean) <= sd:
        return "not significant"
    return pos if mean > 0 else neg


def summary_table(runs: pd.DataFrame) -> pd.DataFrame:
    """One row per configuration: mean and seed sd of every headline metric, with significance labels."""
    cols = ["qsvm_auc", "pqk_auc", "logreg_auc", "rbf_auc", "gbdt_auc", "best_classical_auc", "gap_vs_best",
            "gap_vs_rbf", "pqk_gap_vs_best", "pqk_gap_vs_rbf", "q_offdiag_mean", "q_offdiag_var", "log_var",
            "q_eff_dim", "g", "g_lam0.001", "g_lam0.01", "g_lam0.1", "g_pqk_lam0.01", "s_classical",
            "s_quantum", "log_s_ratio"]
    cols += [c for c in ("best_classical_cv_selected_auc", "gap_vs_cv_best", "pqk_gap_vs_cv_best") if c in runs]
    agg = runs.groupby(KEYS)[cols].agg(["mean", "std"])
    agg.columns = [f"{a}_{b}" if b == "mean" else f"{a}_sd" for a, b in agg.columns]
    agg = agg.rename(columns={f"{c}_mean": c for c in cols})
    agg["n_seeds"] = runs.groupby(KEYS).size()
    agg["reduction"] = runs.groupby(KEYS).reduction.first()
    for gap in ["gap_vs_best", "gap_vs_rbf", "pqk_gap_vs_best", "pqk_gap_vs_rbf", "gap_vs_cv_best", "pqk_gap_vs_cv_best"]:
        if gap in agg:
            agg[f"{gap}_label"] = [label_diff(m, s) if np.isfinite(m) else None
                                   for m, s in zip(agg[gap], agg[f"{gap}_sd"])]
    return agg.reset_index()


def cv_selected(runs: pd.DataFrame, which: str = "qsvm") -> pd.DataFrame:
    """Per (experiment, fm, n, N, seed): the bandwidth with the best CV AUC for that quantum model."""
    idx = runs.groupby(["experiment", "feature_map", "reps", "n_qubits", "n_train", "seed"])[f"{which}_cv_auc"].idxmax()
    return runs.loc[idx]


# ------------------------------------------------------------------------------------ statistics
def quiet():
    """Silence warnings from degenerate bootstrap resamples (constant ranks -> NaN, which are discarded)."""
    import contextlib

    @contextlib.contextmanager
    def ctx():
        with warnings.catch_warnings(), np.errstate(all="ignore"):
            warnings.simplefilter("ignore")
            yield
    return ctx()


def spearman_ci(x, y) -> dict:
    with quiet():
        out = metrics.spearman_with_ci(x, y, n_boot=N_BOOT)
    out["label"] = "not significant" if out["ci_low"] <= 0 <= out["ci_high"] else "significant"
    return out


def _partial(rx, ry, rz) -> float:
    def resid(a, b):
        A = np.column_stack([np.ones_like(b), b])
        return a - A @ np.linalg.lstsq(A, a, rcond=None)[0]
    ex, ey = resid(rx, rz), resid(ry, rz)
    return float(np.corrcoef(ex, ey)[0, 1])


def partial_spearman(x, y, z, seed: int = 0) -> dict:
    """Spearman correlation of x and y controlling for z (Pearson of rank residuals), bootstrap CI."""
    x, y, z = (np.asarray(v, float) for v in (x, y, z))
    rk = lambda v: stats.rankdata(v)  # noqa: E731
    rho = _partial(rk(x), rk(y), rk(z))
    rng = np.random.default_rng(seed)
    boots = []
    with quiet():
        for _ in range(N_BOOT):
            i = rng.integers(0, len(x), len(x))
            b = _partial(rk(x[i]), rk(y[i]), rk(z[i]))
            if np.isfinite(b):
                boots.append(b)
    lo, hi = np.quantile(boots, [0.025, 0.975])
    return {"rho": rho, "ci_low": float(lo), "ci_high": float(hi), "n": int(len(x)),
            "label": "not significant" if lo <= 0 <= hi else "significant"}


def rho_difference(a, b, y, seed: int = 0) -> dict:
    """Paired bootstrap of spearman(a, y) - spearman(b, y)."""
    a, b, y = (np.asarray(v, float) for v in (a, b, y))
    d0 = stats.spearmanr(a, y)[0] - stats.spearmanr(b, y)[0]
    rng = np.random.default_rng(seed)
    boots = []
    with quiet():
        for _ in range(N_BOOT):
            i = rng.integers(0, len(y), len(y))
            d = stats.spearmanr(a[i], y[i])[0] - stats.spearmanr(b[i], y[i])[0]
            if np.isfinite(d):
                boots.append(d)
    lo, hi = np.quantile(boots, [0.025, 0.975])
    return {"diff": float(d0), "ci_low": float(lo), "ci_high": float(hi),
            "label": "not significant" if lo <= 0 <= hi else "significant"}


def fmt_ci(d: dict) -> str:
    return f"{d['rho']:+.2f} [{d['ci_low']:+.2f}, {d['ci_high']:+.2f}]"


def paired(runs: pd.DataFrame, col: str, mask_a, mask_b) -> tuple[float, float]:
    """Mean and sd over seeds of col(a) - col(b), paired by seed."""
    a = runs[mask_a].set_index("seed")[col]
    b = runs[mask_b].set_index("seed")[col]
    d = (a - b).dropna()
    return float(d.mean()), float(d.std())


# ------------------------------------------------------------------------------- hypothesis tests
def test_h1(runs: pd.DataFrame, table: pd.DataFrame) -> dict:
    """H1: the tuned classical baselines match or beat every quantum kernel (AUC with error bars, all configs)."""
    counts = lambda s: {str(k): int(v) for k, v in s.value_counts().items()}  # noqa: E731
    out = {"unit": "every configuration (feature map, qubits, bandwidth) x both quantum kernels; "
                   "seed-paired AUC difference quantum - best classical",
           "n_configs": int(len(table))}
    for kernel, gap in [("fidelity", "gap_vs_best"), ("projected", "pqk_gap_vs_best")]:
        lab = table[f"{gap}_label"]
        out[kernel] = {"vs_best_classical": counts(lab),
                       "vs_rbf_svm_only": counts(table[f"{gap.replace('best', 'rbf')}_label"]),
                       "max_gap_vs_best": float(table[gap].max())}
        if f"{gap.replace('best', 'cv_best')}_label" in table and table[gap.replace("best", "cv_best")].notna().any():
            out[kernel]["vs_cv_selected_classical"] = counts(table[f"{gap.replace('best', 'cv_best')}_label"])
    better = table[(table.gap_vs_best_label == "quantum better") | (table.pqk_gap_vs_best_label == "quantum better")]
    rbf_better = table[(table.gap_vs_rbf_label == "quantum better") | (table.pqk_gap_vs_rbf_label == "quantum better")]
    out["configs_where_a_quantum_kernel_beats_best_classical"] = [
        f"{FM_LABEL[(r.feature_map, r.reps)]} n={r.n_qubits} c={r.bandwidth:g}" for r in better.itertuples()]
    out["configs_where_a_quantum_kernel_beats_the_rbf_svm"] = [
        f"{FM_LABEL[(r.feature_map, r.reps)]} n={r.n_qubits} c={r.bandwidth:g}: vs RBF-SVM fidelity "
        f"{r.gap_vs_rbf:+.4f} ± {r.gap_vs_rbf_sd:.4f}, projected {r.pqk_gap_vs_rbf:+.4f} ± {r.pqk_gap_vs_rbf_sd:.4f}; "
        f"vs best classical fidelity {r.gap_vs_best:+.4f}, projected {r.pqk_gap_vs_best:+.4f}"
        for r in rbf_better.itertuples()]
    # under a true gap of 0, |mean| > 1 sd with 5 seeds happens with probability ~0.09 (each sign ~0.045)
    out["chance_positive_hits_expected_per_kernel"] = 0.045 * len(table)
    # supplementary: quantum bandwidth chosen per seed by CV
    rows = []
    for which in ("qsvm", "pqk"):
        sel = cv_selected(runs, which)
        sel = sel.assign(vs_rbf=sel[f"{which}_auc"] - sel.rbf_auc, vs_best=sel[f"{which}_auc"] - sel.best_classical_auc)
        for (kind, reps, n), g in sel.groupby(["feature_map", "reps", "n_qubits"]):
            rows.append({"model": "fidelity QSVM" if which == "qsvm" else "projected QSVM",
                         "feature_map": FM_LABEL[(kind, reps)], "n_qubits": int(n), "n_seeds": int(len(g)),
                         "bandwidths_searched": int(runs[(runs.feature_map == kind) & (runs.reps == reps) &
                                                         (runs.n_qubits == n)].bandwidth.nunique()),
                         "auc": g[f"{which}_auc"].mean(), "gap_vs_rbf": g.vs_rbf.mean(), "gap_vs_rbf_sd": g.vs_rbf.std(),
                         "gap_vs_rbf_label": label_diff(g.vs_rbf.mean(), g.vs_rbf.std()),
                         "gap_vs_best": g.vs_best.mean(), "gap_vs_best_sd": g.vs_best.std(),
                         "gap_vs_best_label": label_diff(g.vs_best.mean(), g.vs_best.std())})
    out["cv_selected_bandwidth"] = rows
    held = len(better) == 0
    fid, pqk = out["fidelity"]["vs_best_classical"], out["projected"]["vs_best_classical"]
    out["verdict"] = {
        "held": "HELD" if held else "DID NOT HOLD",
        "detail": (f"no configuration has a quantum kernel above the best classical baseline by more than the seed "
                   f"spread (fidelity: {fid.get('classical better', 0)} classical better, {fid.get('not significant', 0)} "
                   f"not significant, {fid.get('quantum better', 0)} quantum better; projected: "
                   f"{pqk.get('classical better', 0)} / {pqk.get('not significant', 0)} / {pqk.get('quantum better', 0)} "
                   f"of {len(table)}). Against the RBF-SVM alone, {len(rbf_better)} configuration(s) exceed it "
                   f"(~{out['chance_positive_hits_expected_per_kernel']:.1f} per kernel expected by chance with this "
                   f"lenient rule)" if held else
                   "quantum kernel above the best classical baseline in: " +
                   "; ".join(out["configs_where_a_quantum_kernel_beats_best_classical"]))}
    return out


def test_h2(table: pd.DataFrame, extra: bool = True) -> dict:
    """H2: g correlates positively with the quantum - classical AUC gap (Spearman across configurations, CI)."""
    gap = table.gap_vs_best.to_numpy()
    out = {"unit": "configuration means over seeds", "n_configs": int(len(table)),
           "gap": "fidelity QSVM AUC - best classical AUC (gap_vs_best)", "expected_sign": "rho > 0",
           "headline_g": G_HEADLINE, "pooled": {}}
    for col, lam in LAMBDAS:
        out["pooled"][f"lambda={lam:g}"] = spearman_ci(table[col], gap)
    out["pooled"]["log_kernel_variance (reference)"] = spearman_ci(table.log_var, gap)
    # Huang et al.'s own use of g is a necessary condition: an advantage needs g >~ sqrt(N)
    n_train = sorted(int(v) for v in table.n_train.unique())
    if len(n_train) == 1:
        thr = float(np.sqrt(n_train[0]))
        nc = {"N_train": n_train[0], "sqrt_N": thr, "n_configs": int(len(table)), "by_lambda": {}}
        for col, lam in LAMBDAS:
            above = table[table[col] > thr]
            nc["by_lambda"][f"lambda={lam:g}"] = {
                "max_g": float(table[col].max()), "n_above_sqrt_N": int(len(above)),
                "gap_labels_above": {str(k): int(v) for k, v in above.gap_vs_best_label.value_counts().items()},
                "gap_labels_below": {str(k): int(v) for k, v in
                                     table[table[col] <= thr].gap_vs_best_label.value_counts().items()}}
        out["huang_necessary_condition"] = nc
    if extra:
        out["partial_controlling_log_var"], out["within_feature_map"], out["within_feature_map_partial"] = {}, {}, {}
        for col, lam in LAMBDAS:
            key = f"lambda={lam:g}"
            out["partial_controlling_log_var"][key] = partial_spearman(table[col], gap, table.log_var)
            out["within_feature_map"][key], out["within_feature_map_partial"][key] = {}, {}
            for fm in FMS:
                s = _fm_rows(table, fm)
                out["within_feature_map"][key][FM_LABEL[fm]] = spearman_ci(s[col], s.gap_vs_best)
                out["within_feature_map_partial"][key][FM_LABEL[fm]] = partial_spearman(s[col], s.gap_vs_best, s.log_var)
        la = out["label_aware"] = {}
        la["definition"] = ("log10(s_classical / s_quantum); s = ridge-regularised model complexity "
                            "(src.metrics.model_complexity, a stand-in for Huang et al.'s s_K(N))")
        la["pooled"] = spearman_ci(table.log_s_ratio, gap)
        la["partial_controlling_log_var"] = partial_spearman(table.log_s_ratio, gap, table.log_var)
        la["within_feature_map"] = {FM_LABEL[fm]: spearman_ci(_fm_rows(table, fm).log_s_ratio, _fm_rows(table, fm).gap_vs_best)
                                    for fm in FMS}
        la["ratio_minus_g"] = {f"lambda={lam:g}": rho_difference(table.log_s_ratio, table[col], gap) for col, lam in LAMBDAS}
        la["ratio_minus_log_var"] = rho_difference(table.log_s_ratio, table.log_var, gap)
        la["note"] = ("H2 expects rho > 0. ratio_minus_g is the signed difference of the two Spearman rhos: "
                      "a CI excluding 0 means the two quantities differ in how they track the gap")
        la["bound_regime"] = {
            "s_classical_min": float(table.s_classical.min()), "s_classical_median": float(table.s_classical.median()),
            "fraction_s_classical_below_1": float((table.s_classical < 1).mean()),
            "fraction_s_quantum_below_1": float((table.s_quantum < 1).mean()),
            "spearman_s_quantum_vs_qsvm_auc": spearman_ci(table.s_quantum, table.qsvm_auc),
            "median_s_quantum_when_var_below_1e-3": float(table[table.q_offdiag_var < 1e-3].s_quantum.median()),
            "interpretation": ("s = alpha^T K alpha / N equals Huang et al.'s s_K(N)/N, so their bound ~ sqrt(s) is "
                               "vacuous for s >~ 1. s_classical is never below 1 here, and near-identity (concentrated) "
                               "quantum kernels get s_quantum ~ 1 because they memorise the labels; the ratio "
                               "s_C/s_Q therefore mostly flags memorising kernels, which generalise worst. The "
                               "label-aware test is run outside the regime where the bound means anything.")}
        competitive = (table.gap_vs_best_label != "classical better").to_numpy()
        cls = {"definition": "AUC for separating configurations whose gap is not significantly negative",
               "n_competitive": int(competitive.sum()), "n_total": int(len(table))}
        for name, v in [("g_lam0.01", table["g_lam0.01"]), ("g_lam0", table["g"]), ("log_s_ratio", table.log_s_ratio),
                        ("log_var", table.log_var)]:
            cls[name] = float(roc_auc_score(competitive, v)) if 0 < competitive.sum() < len(table) else None
        out["classification"] = cls
        out["projected_kernel_pooled"] = {"lambda=0.01": spearman_ci(table["g_pqk_lam0.01"], table.pqk_gap_vs_best)}
    head = out["pooled"][f"lambda={float(G_HEADLINE.split('lam')[1]):g}"]
    pos = [k for k, v in out["pooled"].items() if k.startswith("lambda") and v["ci_low"] > 0]
    neg = [k for k, v in out["pooled"].items() if k.startswith("lambda") and v["ci_high"] < 0]
    held = head["ci_low"] > 0
    detail = (f"headline ({G_HEADLINE}): rho = {fmt_ci(head)}; all lambdas: " +
              ", ".join(f"{k} {fmt_ci(v)}" for k, v in out["pooled"].items() if k.startswith("lambda")))
    if pos and not held:
        k = pos[0]
        part = out.get("partial_controlling_log_var", {}).get(k)
        detail += (f". Only {', '.join(pos)} is significantly positive" +
                   (f", and it vanishes once log kernel variance is controlled for (partial rho {fmt_ci(part)})"
                    if part and part["ci_low"] <= 0 else ""))
    if neg:
        detail += f". Significantly NEGATIVE (opposite to H2) at {', '.join(neg)}"
    out["verdict"] = {"held": "HELD" if held else "FAILED", "detail": detail}
    return out


def test_h3(runs: pd.DataFrame, table: pd.DataFrame) -> dict:
    """H3: at fixed bandwidth, more qubits and more depth -> concentration rises (variance falls), AUC falls."""
    trend = []
    for (kind, reps, c), g in runs.groupby(["feature_map", "reps", "bandwidth"]):
        if g.n_qubits.nunique() < 2:
            continue
        row = {"feature_map": FM_LABEL[(kind, reps)], "bandwidth": float(c),
               "n_values": sorted(int(v) for v in g.n_qubits.unique())}
        for col, name in [("log_var", "log10_var"), ("qsvm_auc", "auc")]:
            res = stats.linregress(g.n_qubits, g[col])
            ci = 1.96 * res.stderr
            row[f"{name}_slope_per_qubit"] = float(res.slope)
            row[f"{name}_slope_ci95"] = float(ci)
            row[f"{name}_trend"] = ("falls" if res.slope + ci < 0 else "rises" if res.slope - ci > 0 else "flat (n.s.)")
        row["H3_holds_here"] = row["log10_var_trend"] == "falls" and row["auc_trend"] == "falls"
        big_n = g[g.n_qubits >= 4].groupby("n_qubits").qsvm_auc.mean()
        row["auc_at_chance_for_n_ge_4"] = bool(len(big_n) and big_n.max() <= 0.55)
        trend.append(row)
    depth = []  # ZZ reps 2 vs reps 1 at equal (n, c), paired by seed
    zz = runs[runs.feature_map == "zz"]
    for (n, c), g in zz.groupby(["n_qubits", "bandwidth"]):
        if set(g.reps) != {1, 2}:
            continue
        dv = paired(g, "log_var", g.reps == 2, g.reps == 1)
        da = paired(g, "qsvm_auc", g.reps == 2, g.reps == 1)
        depth.append({"n_qubits": int(n), "bandwidth": float(c), "dlog10_var_reps2_minus_reps1": dv[0],
                      "dlog10_var_sd": dv[1], "var_label": label_diff(*dv, "reps 2 less concentrated", "reps 2 more concentrated"),
                      "dauc_reps2_minus_reps1": da[0], "dauc_sd": da[1],
                      "auc_label": label_diff(*da, "reps 2 better", "reps 2 worse")})
    low = table[table.q_offdiag_var < 1e-3]
    regimes = {}
    for name, mask in [("concentrated: var < 1e-3 and off-diagonal mean < 0.1", low.q_offdiag_mean < 0.1),
                       ("near-constant: var < 1e-3 and off-diagonal mean > 0.5", low.q_offdiag_mean > 0.5)]:
        s = low[mask]
        regimes[name] = {"n_configs": int(len(s)), "qsvm_auc_median": float(s.qsvm_auc.median()) if len(s) else None,
                         "qsvm_auc_max": float(s.qsvm_auc.max()) if len(s) else None,
                         "configs": sorted({f"{FM_LABEL[(k, r)]} c={c:g}" for k, r, c in
                                            zip(s.feature_map, s.reps, s.bandwidth)})}
    held_cells = [f"{t['feature_map']} c={t['bandwidth']:g}" for t in trend if t["H3_holds_here"]]
    var_only = [f"{t['feature_map']} c={t['bandwidth']:g}" + (" (AUC already at chance from n=4)"
                                                              if t["auc_at_chance_for_n_ge_4"] else "")
                for t in trend if t["log10_var_trend"] == "falls" and t["auc_trend"] != "falls"]
    n_var_more = sum(d["var_label"] == "reps 2 more concentrated" for d in depth)
    n_auc_worse = sum(d["auc_label"] == "reps 2 worse" for d in depth)
    out = {"trend_vs_qubits": trend, "depth_zz_reps2_vs_reps1": depth,
           "spearman_log_var_vs_qsvm_auc": spearman_ci(table.log_var, table.qsvm_auc),
           "low_variance_regimes": regimes,
           "note": ("AUC is the raw test AUC, as H3 states; more qubits also means more PCA components (more "
                    "information), which by itself raises AUC (the classical models gain 0.08 from n=2 to 10). "
                    "Off-diagonal variance alone does not identify failure: nearly constant kernels (Z map, small c) "
                    "also have small variance but still classify well in exact simulation")}
    if not trend:
        return out
    all_held = len(held_cells) == len(trend)
    out["verdict"] = {
        "held": "HELD" if all_held else ("HELD IN PART" if held_cells else "FAILED"),
        "detail": (f"qubits: variance falls and AUC falls together in {len(held_cells)} of {len(trend)} "
                   f"(map, c) cells: {', '.join(held_cells) or 'none'}; variance falls but AUC does not in: "
                   f"{', '.join(var_only) or 'none'}; the remaining cells show no significant variance fall. "
                   f"Depth (ZZ reps 2 vs reps 1, {len(depth)} (n, c) cells): reps 2 more concentrated in {n_var_more}, "
                   f"AUC lower in {n_auc_worse} -- no consistent depth effect")}
    return out


def test_h4(runs: pd.DataFrame) -> dict:
    """H4: at fixed qubits, smaller c -> less concentration and recovered AUC, while g is pulled back toward 1."""
    cells = []
    for (kind, reps, n), s in runs.groupby(["feature_map", "reps", "n_qubits"]):
        cs = sorted(s.bandwidth.unique())
        if len(cs) < 3:
            continue
        lo_c, hi_c = cs[0], cs[-1]
        a, b = s.bandwidth == lo_c, s.bandwidth == hi_c
        m = s.groupby("bandwidth")[["qsvm_auc", "qsvm_cv_auc", "log_var", "g", "g_lam0.01", "best_classical_auc"]].mean()
        dv, da = paired(s, "log_var", a, b), paired(s, "qsvm_auc", a, b)
        cell = {"feature_map": FM_LABEL[(kind, reps)], "n_qubits": int(n), "c_small": float(lo_c), "c_large": float(hi_c),
                "dlog10_var_small_minus_large": dv[0], "dlog10_var_sd": dv[1],
                "concentration_reduced": label_diff(*dv, "yes", "no (more concentrated)") == "yes",
                "dauc_small_minus_large": da[0], "dauc_sd": da[1],
                "performance_recovered": label_diff(*da, "yes", "no") == "yes",
                "auc_small": float(m.qsvm_auc[lo_c]), "auc_large": float(m.qsvm_auc[hi_c]),
                "gap_vs_best_at_small_c": float(s[a].gap_vs_best.mean()), "gap_vs_best_sd_at_small_c": float(s[a].gap_vs_best.std()),
                "c_best_by_cv": float(m.qsvm_cv_auc.idxmax())}
        for col, name in [("g", "g_lam0"), ("g_lam0.01", "g_lam0.01")]:
            # toward 1: |log g| smaller at small c than at large c, paired by seed; monotone: Spearman(c, g) > 0
            s2 = s.assign(_dist=np.abs(np.log(s[col])))
            dd = paired(s2, "_dist", a, b)
            rho = spearman_ci(s.bandwidth, s[col])
            cell[f"{name}_small_c"] = float(m[col][lo_c])
            cell[f"{name}_large_c"] = float(m[col][hi_c])
            cell[f"{name}_min_over_c"] = float(m[col].min())
            cell[f"{name}_argmax_c"] = float(m[col].idxmax())
            cell[f"{name}_closer_to_1_at_small_c"] = label_diff(-dd[0], dd[1], "yes", "no (further)") == "yes"
            cell[f"{name}_spearman_c_vs_g"] = rho
            cell[f"{name}_monotone_toward_1"] = rho["ci_low"] > 0 and cell[f"{name}_closer_to_1_at_small_c"]
        cells.append(cell)
    out = {"cells": cells, "definition": (
        "per (feature map, n): compare the smallest c (0.05) with the largest (1.0), paired by seed. "
        "'concentration reduced' = log10 variance higher at small c; 'performance recovered' = AUC higher at small c; "
        "'g pulled toward 1' = |log g| smaller at small c AND Spearman(c, g) > 0 over the sweep (g falls steadily "
        "as c falls)")}
    if not cells:
        return out
    k = len(cells)
    first_conc = sum(c["concentration_reduced"] for c in cells)
    first_auc = sum(c["performance_recovered"] for c in cells)
    g_head = sum(c["g_lam0.01_monotone_toward_1"] for c in cells)
    g_raw = sum(c["g_lam0_monotone_toward_1"] for c in cells)
    g_raw_dir = sum(c["g_lam0_closer_to_1_at_small_c"] for c in cells)
    not_reduced = [f"{c['feature_map']} n={c['n_qubits']}" for c in cells if not c["concentration_reduced"]]
    first_held = first_auc == k and first_conc == k
    second_held = g_head == k
    g_small = [c["g_lam0.01_small_c"] for c in cells]
    g_raw_small = [c["g_lam0_small_c"] for c in cells]
    if first_held:
        first_status = "held"
    elif first_auc == k:
        first_status = "held in part"
    else:
        first_status = "failed"
    second_status = "held" if second_held else "failed"
    out["verdict"] = {
        "held": ("HELD" if first_held and second_held else
                 f"first half {first_status}; second half {second_status}").upper(),
        "first_half": (f"smaller c recovers AUC in {first_auc} of {k} (map, n) cells and raises kernel variance in "
                       f"{first_conc} of {k}" + (f"; variance is NOT raised in {', '.join(not_reduced)}: there the kernel "
                                                 f"flattens towards a constant at small c, so its variance falls even "
                                                 f"though AUC recovers" if not_reduced else "")),
        "second_half": (f"verdict based on the headline regularised g (lambda=0.01): it falls steadily toward 1 in "
                        f"only {g_head} of {k} cells; at c=0.05 it is "
                        f"{min(g_small):.1f}-{max(g_small):.1f}, never near 1, and for ZZ maps it peaks at intermediate c. "
                        f"Unregularised g (lambda=0) is closer to 1 at c=0.05 than at c=1 in {g_raw_dir} of {k} cells and "
                        f"falls steadily in {g_raw} of {k}, by orders of magnitude, but still ends at "
                        f"{min(g_raw_small):.1f}-{max(g_raw_small):.0f} at c=0.05: it moves toward 1 without getting there")}
    return out


def run_tests(runs: pd.DataFrame, table: pd.DataFrame, extra_h2: bool = True) -> dict:
    return {"H1": test_h1(runs, table), "H2": test_h2(table, extra_h2), "H3": test_h3(runs, table), "H4": test_h4(runs)}


def angle_spread() -> dict | None:
    """Median over features of the inter-quartile range of the training angles (before bandwidth), PCA vs selection."""
    from src import data
    path = ROOT / "data" / "atlas-higgs-challenge-2014-v2.csv.gz"
    if not path.exists():
        return None
    df, cols = data.select_features(data.load(str(path)))
    out = {}
    for red in ("pca", "gbdt_importance"):
        for n in (4, 8):
            iqr = []
            for seed in range(5):
                X = data.prepare(df, cols, n, 500, 1000, seed, red)["X_train"]
                q1, q3 = np.percentile(X, [25, 75], axis=0)
                iqr.append(float(np.median(q3 - q1)))
            out[f"{red}_n{n}"] = {"median_iqr_radians": float(np.mean(iqr)), "range_radians": float(2 * np.pi)}
    return out


def robustness(runs: pd.DataFrame, table: pd.DataFrame) -> dict | None:
    """Repeat H1-H4 on the n = 4, 8 slices with PCA (main_grid) and with boosted-tree feature selection (fs_gbdt)."""
    fs = runs[runs.experiment == "fs_gbdt"]
    if fs.empty:
        return None
    ns = sorted(fs.n_qubits.unique())
    pca = runs[(runs.experiment == "main_grid") & runs.n_qubits.isin(ns)]
    tp = table[(table.experiment == "main_grid") & table.n_qubits.isin(ns)]
    tf = table[table.experiment == "fs_gbdt"]
    # same tests, same code, on both slices (within-map H2 has only 10 configurations per map here)
    res = {"pca": run_tests(pca, tp), "feature_selection": run_tests(fs, tf)}
    comp = {}
    for h in ("H1", "H2", "H3", "H4"):
        a, b = res["pca"][h].get("verdict", {}), res["feature_selection"][h].get("verdict", {})
        comp[h] = {"pca": a.get("held"), "feature_selection": b.get("held"), "changed": a.get("held") != b.get("held")}
    res["verdict_comparison"] = comp
    # how the inputs and models themselves changed
    key = ["feature_map", "reps", "n_qubits", "bandwidth"]
    m = tp.set_index(key)[["qsvm_auc", "best_classical_auc", "log_var", G_HEADLINE]].join(
        tf.set_index(key)[["qsvm_auc", "best_classical_auc", "log_var", G_HEADLINE]], lsuffix="_pca", rsuffix="_fs")
    cls_p = pca.drop_duplicates(["n_qubits", "seed"]).groupby("n_qubits")[["rbf_auc", "gbdt_auc", "logreg_auc", "best_classical_auc"]].mean()
    cls_f = fs.drop_duplicates(["n_qubits", "seed"]).groupby("n_qubits")[["rbf_auc", "gbdt_auc", "logreg_auc", "best_classical_auc"]].mean()
    res["classical_auc"] = {name: {f"n{int(k)}": v for k, v in c.round(4).to_dict(orient="index").items()}
                            for name, c in (("pca", cls_p), ("feature_selection", cls_f))}
    res["median_change_fs_minus_pca"] = {
        "qsvm_auc": float((m.qsvm_auc_fs - m.qsvm_auc_pca).median()),
        "best_classical_auc": float((m.best_classical_auc_fs - m.best_classical_auc_pca).median()),
        "log10_var": float((m.log_var_fs - m.log_var_pca).median()),
        G_HEADLINE: float((m[f"{G_HEADLINE}_fs"] - m[f"{G_HEADLINE}_pca"]).median())}
    if "best_classical_cv_selected_auc" in fs:
        res["best_of_three_test_auc_bias"] = {
            "mean_max_of_test_minus_cv_selected": float((fs.best_classical_auc - fs.best_classical_cv_selected_auc).mean()),
            "note": "how much picking the best classical model on test AUC flatters the classical side (fs_gbdt runs)"}
    res["selected_features"] = {f"n{int(n)}_seed{int(s)}": f for (n, s), f in
                                fs.drop_duplicates(["n_qubits", "seed"]).set_index(["n_qubits", "seed"]).selected_features.items()}
    res["angle_spread"] = angle_spread()
    return res


def _fm_rows(df, fm):
    return df[(df.feature_map == fm[0]) & (df.reps == fm[1])]


# --------------------------------------------------------------------------------------- figures
def fig1(runs: pd.DataFrame):
    """AUC vs qubits for every model, one panel per feature map; quantum c chosen per seed by CV."""
    r = runs[runs.n_train == 500]
    sel = {"qsvm_auc": cv_selected(r, "qsvm"), "pqk_auc": cv_selected(r, "pqk")}
    cls = r.drop_duplicates(["experiment", "n_qubits", "seed"])  # classical results do not depend on fm or c
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.6), sharey=True)
    for ax, fm in zip(axes, FMS):
        for i, (col, name, mk) in enumerate(MODELS):
            src = _fm_rows(sel[col], fm) if col in sel else cls
            g = src.groupby("n_qubits")[col].agg(["mean", "std"])
            big = src[src.experiment == "big_qubits"].n_qubits.unique() if col in sel else []
            ax.errorbar(g.index, g["mean"], yerr=g["std"], color=CAT[i], marker=mk, ms=5, lw=1.6,
                        label=name, zorder=3 if col in sel else 2)
            for n in big:  # only 2 bandwidths searched at n = 12, 14: open marker
                ax.plot(n, g.loc[n, "mean"], marker=mk, ms=7, mfc=SURFACE, mec=CAT[i], mew=1.6, ls="", zorder=4)
        ax.set_title(FM_LABEL[fm])
        ax.set_xlabel("qubits n (= PCA components)")
        ax.set_xticks(sorted(r.n_qubits.unique()))
    axes[0].set_ylabel("test ROC-AUC (mean ± sd, 5 seeds)")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", ncols=5, bbox_to_anchor=(0.5, -0.02))
    fig.suptitle("Fig. 1  AUC vs qubits. Quantum bandwidth chosen per seed by CV AUC; "
                 "open markers: only c ∈ {0.1, 1} searched", fontsize=10, x=0.01, ha="left")
    return save(fig, "fig1_auc_vs_qubits")


def s_all_range(v) -> tuple[float, float]:
    v = np.asarray(v, float)
    return float(v.min()), float(v.max())


def fig2(table: pd.DataFrame, h2: dict):
    t = table[(table.n_train == 500) & table.experiment.isin(["main_grid", "big_qubits"])]
    fig, axes = plt.subplots(1, 4, figsize=(13, 3.6), sharey=True)
    vmin, vmax = t.log_var.min(), t.log_var.max()
    for ax, (col, lam) in zip(axes, LAMBDAS):
        for fm in FMS:
            s = _fm_rows(t, fm)
            sc = ax.scatter(s[col], s.gap_vs_best, c=s.log_var, cmap=SEQ, vmin=vmin, vmax=vmax,
                            marker=FM_MARKER[fm], s=36, edgecolors=SURFACE, linewidths=0.8, zorder=3)
        ax.axhline(0, color=INK2, lw=0.8, zorder=1)
        ax.set_xscale("log")
        lo_, hi_ = s_all_range(t[col])
        if hi_ / lo_ < 100:  # narrow range: label 1-2-5 steps instead of crowded minor ticks
            ticks = [v for v in (1, 2, 3, 5, 10, 20, 30, 50) if lo_ <= v <= hi_]
            ax.xaxis.set_major_locator(FixedLocator(ticks))
            ax.xaxis.set_major_formatter(matplotlib.ticker.FixedFormatter([f"{v:g}" for v in ticks]))
            ax.xaxis.set_minor_locator(NullLocator())
        ax.xaxis.set_minor_formatter(NullFormatter())
        st = h2["pooled"][f"lambda={lam:g}"]
        ax.set_title(f"λ = {lam:g}:  ρ = {st['rho']:.2f} [{st['ci_low']:.2f}, {st['ci_high']:.2f}]")
        ax.set_xlabel("g(K_RBF ‖ K_Q)" if lam == 0 else f"g_λ (λ = {lam:g})")
    axes[0].set_ylabel("AUC gap: fidelity QSVM − best classical")
    handles = [Line2D([], [], marker=FM_MARKER[fm], ls="", color=INK2, label=FM_LABEL[fm]) for fm in FMS]
    fig.legend(handles=handles, loc="lower center", ncols=3, bbox_to_anchor=(0.45, -0.08))
    cb = fig.colorbar(sc, ax=axes, pad=0.01, fraction=0.02)
    cb.set_label("log10 off-diagonal variance of K_Q")
    fig.suptitle("Fig. 2  AUC gap vs geometric difference, one point per configuration (mean over 5 seeds); "
                 "Spearman ρ with 95% bootstrap CI", fontsize=10, x=0.01, ha="left")
    return save(fig, "fig2_gap_vs_g")


def fig3(runs: pd.DataFrame):
    r = runs[(runs.n_train == 500) & runs.experiment.isin(["main_grid", "big_qubits"])]
    cs = sorted(r.bandwidth.unique())
    fig, axes = plt.subplots(2, 3, figsize=(11, 6), sharex=True, sharey="row")
    for j, fm in enumerate(FMS):
        s = _fm_rows(r, fm)
        for i, c in enumerate(cs):
            g = s[s.bandwidth == c].groupby("n_qubits")
            lv, au = g.log_var.agg(["mean", "std"]), g.qsvm_auc.agg(["mean", "std"])
            kw = dict(color=ORDINAL[i], marker="o", ms=4, lw=1.6, label=f"c = {c:g}")
            axes[0, j].errorbar(lv.index, lv["mean"], yerr=lv["std"], **kw)
            axes[1, j].errorbar(au.index, au["mean"], yerr=au["std"], **kw)
        axes[0, j].set_title(FM_LABEL[fm])
        axes[1, j].set_xlabel("qubits n")
        axes[1, j].axhline(0.5, color=INK2, lw=0.8, ls=":")
    axes[0, 0].set_ylabel("log10 off-diagonal variance of K_Q")
    axes[1, 0].set_ylabel("fidelity QSVM test AUC")
    axes[0, 0].legend(loc="lower left", ncols=2)
    fig.suptitle("Fig. 3  Kernel concentration and AUC vs qubits, one line per bandwidth c (mean ± sd, 5 seeds)",
                 fontsize=10, x=0.01, ha="left")
    return save(fig, "fig3_concentration_vs_qubits")


def fig4(runs: pd.DataFrame):
    r = runs[runs.experiment == "main_grid"]
    fig, axes = plt.subplots(2, 3, figsize=(11.5, 6), sharex=True, gridspec_kw={"wspace": 0.38})
    for i, n in enumerate((4, 8)):
        s0 = r[r.n_qubits == n]
        for fm in FMS:
            g = _fm_rows(s0, fm).groupby("bandwidth")
            kw = dict(color=FM_COLOR[fm], marker=FM_MARKER[fm], ms=5, lw=1.6, label=FM_LABEL[fm])
            for ax, col in zip(axes[i], ["g_lam0.01", "log_var", "qsvm_auc"]):
                a = g[col].agg(["mean", "std"])
                ax.errorbar(a.index, a["mean"], yerr=a["std"], **kw)
        best = s0.drop_duplicates("seed").best_classical_auc.agg(["mean", "std"])
        axes[i, 2].axhspan(best["mean"] - best["std"], best["mean"] + best["std"], color=GRID, zorder=0)
        axes[i, 2].axhline(best["mean"], color=INK2, lw=1, ls="--")
        axes[i, 2].annotate("best classical", (1.0, best["mean"] + best["std"]), xytext=(0, 2),
                            textcoords="offset points", fontsize=7, color=INK2, ha="right", va="bottom")
        axes[i, 0].set_ylabel(f"n = {n}\ng_λ, λ = 0.01")
        axes[i, 1].set_ylabel("log10 off-diag. variance")
        axes[i, 2].set_ylabel("fidelity QSVM test AUC")
    for ax in axes[1]:
        ax.set_xscale("log")
        ax.set_xlabel("bandwidth c")
        ax.set_xticks([0.05, 0.1, 0.25, 0.5, 1.0], ["0.05", "0.1", "0.25", "0.5", "1"])
    axes[0, 2].legend(loc="lower left")
    fig.suptitle("Fig. 4  Regularised g, kernel variance and AUC vs bandwidth at fixed n (mean ± sd, 5 seeds)",
                 fontsize=10, x=0.01, ha="left")
    return save(fig, "fig4_vs_bandwidth")


def fig5(n: int = 8, seed: int = 0, healthy: float = 0.1, concentrated: float = 1.0):
    from src import data, kernels
    path = ROOT / "data" / "atlas-higgs-challenge-2014-v2.csv.gz"
    if not path.exists():
        warnings.warn(f"Fig 5 skipped: {path.name} not found in data/")
        return []
    df, cols = data.select_features(data.load(str(path)))
    d = data.prepare(df, cols, n, 500, 1000, seed)
    order = np.argsort(d["y_train"], kind="stable")
    Ks = {c: kernels.fidelity_kernel(kernels.statevectors(d["X_train"][order] * c, "zz", 2)) for c in (healthy, concentrated)}
    n_bkg = int((d["y_train"] == 0).sum())
    fig = plt.figure(figsize=(12, 3.9))
    gs = fig.add_gridspec(1, 5, width_ratios=[1, 1, 0.05, 0.22, 1.1], wspace=0.25)
    for k, (c, title) in enumerate([(healthy, "healthy"), (concentrated, "concentrated")]):
        ax = fig.add_subplot(gs[0, k])
        K = Ks[c]
        im = ax.imshow(K, cmap=SEQ_HEAT, vmin=0, vmax=1, interpolation="nearest")
        ax.axhline(n_bkg - 0.5, color=CAT[1], lw=0.8)
        ax.axvline(n_bkg - 0.5, color=CAT[1], lw=0.8)
        off = K[~np.eye(len(K), dtype=bool)]
        ax.set_title(f"{title}: c = {c:g}\noff-diag mean {off.mean():.3f}, var {off.var():.1e}")
        ax.set_xlabel("training event (background | signal)")
        ax.grid(False)
        if k == 0:
            ax.set_ylabel("training event")
    fig.colorbar(im, cax=fig.add_subplot(gs[0, 2]), label="K(x, x')")
    ax = fig.add_subplot(gs[0, 4])
    bins = np.linspace(0, 1, 51)
    for k, (c, title) in enumerate([(healthy, "healthy"), (concentrated, "concentrated")]):
        off = Ks[c][np.triu_indices(len(Ks[c]), 1)]
        ax.hist(off, bins=bins, color=CAT[k], alpha=0.85, label=f"{title} (c = {c:g})", histtype="stepfilled",
                edgecolor=SURFACE, linewidth=0.5)
    ax.axvline(1 / 2**n, color=INK2, ls=":", lw=1)
    ax.annotate("1/2ⁿ", (1 / 2**n, 1), xycoords=("data", "axes fraction"), xytext=(3, -12),
                textcoords="offset points", fontsize=8, color=INK2)
    ax.set_yscale("log")
    ax.set_xlabel("off-diagonal kernel value")
    ax.set_ylabel("pairs")
    ax.legend(loc="upper right")
    fig.suptitle(f"Fig. 5  Fidelity kernel matrices, ZZ map reps 2, n = {n}, seed {seed}, 500 training events "
                 "sorted by label (orange lines: class boundary)", fontsize=10, x=0.01, ha="left")
    return save(fig, "fig5_kernel_heatmaps")


def fig6(noise: pd.DataFrame, hw: pd.DataFrame):
    if noise is None:
        warnings.warn("Fig 6 skipped: results/noise.csv not found")
        return []
    g = noise[noise.study == "grid"].copy()
    g["shots_x"] = g.shots.replace({"exact": "100000"}).astype(int)
    confs = [("n4_healthy", CAT[0], "-", "o"), ("n4_concentrated", CAT[0], "--", "o"),
             ("n8_healthy", CAT[1], "-", "s"), ("n8_concentrated", CAT[1], "--", "s")]
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.8))
    ax = axes[0]
    for name, color, ls, mk in confs:
        a = g[(g.config == name) & (g.p_tot == 0)].groupby("shots_x").qsvm_auc.agg(["mean", "std"])
        ax.errorbar(a.index, a["mean"], yerr=a["std"], color=color, ls=ls, marker=mk, ms=5, lw=1.6,
                    label=name.replace("_", ", "))
    for n, color in ((4, CAT[0]), (8, CAT[1])):
        b = g[g.n_qubits == n].best_classical_auc.mean()
        ax.axhline(b, color=color, lw=0.8, ls=":")
        ax.annotate(f"best classical, n={n}", (130, b), xytext=(0, 2), textcoords="offset points", fontsize=7, color=INK2)
    ax.set_xscale("log")
    ax.set_xticks([100, 1000, 10000, 100000], ["100", "1k", "10k", "exact"])
    ax.set_xlabel("shots per kernel entry (p_tot = 0)")
    ax.set_ylabel("fidelity QSVM test AUC (mean ± sd)")
    ax.set_title("(a) shot noise")
    ax.legend(loc="center right", fontsize=7)

    ax = axes[1]
    for name, color, ls, mk in confs:
        for shots, mfc in (("exact", color), ("1000", SURFACE)):
            a = g[(g.config == name) & (g.shots.astype(str) == shots)].groupby("p_tot").qsvm_auc.agg(["mean", "std"])
            ax.errorbar(a.index, a["mean"], yerr=a["std"], color=color, ls=ls, marker=mk, mfc=mfc, ms=5, lw=1.4)
    ax.set_xlabel("global depolarizing strength p_tot")
    ax.set_title("(b) depolarizing noise")
    ax.legend(handles=[Line2D([], [], color=INK2, marker="o", ls="", label="exact expectation"),
                       Line2D([], [], color=INK2, marker="o", mfc=SURFACE, ls="", label="1,000 shots")],
              loc="center right", fontsize=7)

    ax = axes[2]
    m = noise[noise.study == "hw_model"]
    labels, pos = [], 0
    for cfg in ("hw_c0.05", "hw_c0.25"):
        sub = m[m.config == cfg]
        if sub.empty:
            continue
        c = float(sub.bandwidth.iloc[0])
        data_ = [sub[sub.p_tot == p].qsvm_auc.to_numpy() for p in (0.0, 0.1)]
        bp = ax.boxplot(data_, positions=[pos, pos + 1], widths=0.6, patch_artist=True, showfliers=False,
                        medianprops=dict(color=INK), whiskerprops=dict(color=INK2), capprops=dict(color=INK2))
        for patch in bp["boxes"]:
            patch.set(facecolor="#cde2fb", edgecolor=INK2)
        ex = float(sub.exact_auc.iloc[0])
        ax.hlines(ex, pos - 0.4, pos + 1.4, color=INK, lw=1.2)
        ax.annotate("exact", (pos + 1.4, ex), xytext=(2, -3), textcoords="offset points", fontsize=7, color=INK2)
        obs = hw[np.isclose(hw.c, c)]
        for _, o in obs.iterrows():
            is_real = o["mode"] == "real"
            ax.plot(pos + 0.5, o.auc_hardware, marker="*" if is_real else "D", ms=11 if is_real else 7,
                    color=CAT[2] if is_real else CAT[1], mec=INK, mew=0.6, ls="", zorder=5)
        labels += [f"c={c:g}\np=0", f"c={c:g}\np=0.1"]
        pos += 2.5
    ticks = [p for k in range(len(labels) // 2) for p in (2.5 * k, 2.5 * k + 1)]
    ax.set_xticks(ticks, labels)
    ax.set_ylabel("test AUC (24 test events)")
    ax.set_title("(c) hardware setup: n=4, ZZ reps 1, 24+24 events, 500 shots")
    ax.legend(handles=[Line2D([], [], marker="s", ls="", mfc="#cde2fb", mec=INK2, ms=8, label="analytic model, 200 draws"),
                       Line2D([], [], marker="D", ls="", color=CAT[1], mec=INK, label="fake_torino (noisy simulator)"),
                       Line2D([], [], marker="*", ls="", color=CAT[2], mec=INK, ms=11, label="ibm_marrakesh (real QPU)")],
              loc="upper right", fontsize=7)
    fig.suptitle("Fig. 6  Noise: shot noise and global depolarizing noise (ZZ reps 2, N=500, 5 seeds), "
                 "and the IBM hardware runs", fontsize=10, x=0.01, ha="left")
    return save(fig, "fig6_noise_and_hardware")


def fig7(runs: pd.DataFrame):
    """Robustness: AUC, kernel variance and g vs bandwidth at n = 4, 8 for PCA (solid) and feature selection (dashed)."""
    fs = runs[runs.experiment == "fs_gbdt"]
    if fs.empty:
        warnings.warn("Fig 7 skipped: results/fs_gbdt not found")
        return []
    ns = sorted(fs.n_qubits.unique())
    pca = runs[(runs.experiment == "main_grid") & runs.n_qubits.isin(ns)]
    fig, axes = plt.subplots(len(ns), 3, figsize=(11.5, 3 * len(ns)), sharex=True, gridspec_kw={"wspace": 0.38},
                             squeeze=False)
    for i, n in enumerate(ns):
        for src, ls, mfc_fill in ((pca, "-", True), (fs, "--", False)):
            s0 = src[src.n_qubits == n]
            for fm in FMS:
                g = _fm_rows(s0, fm).groupby("bandwidth")
                color = FM_COLOR[fm]
                kw = dict(color=color, marker=FM_MARKER[fm], ms=5, lw=1.5, ls=ls, mfc=color if mfc_fill else SURFACE)
                for ax, col in zip(axes[i], ["qsvm_auc", "log_var", G_HEADLINE]):
                    a = g[col].agg(["mean", "std"])
                    ax.errorbar(a.index, a["mean"], yerr=a["std"], **kw)
            best = s0.drop_duplicates("seed").best_classical_auc.mean()
            axes[i, 0].axhline(best, color="#8a8984", lw=1.2, ls=ls, zorder=1)
        axes[i, 0].set_ylabel(f"n = {n}\nfidelity QSVM test AUC")
        axes[i, 1].set_ylabel("log10 off-diag. variance")
        axes[i, 2].set_ylabel("g_λ, λ = 0.01")
    for ax in axes[-1]:
        ax.set_xscale("log")
        ax.set_xlabel("bandwidth c")
        ax.set_xticks([0.05, 0.1, 0.25, 0.5, 1.0], ["0.05", "0.1", "0.25", "0.5", "1"])
        ax.xaxis.set_minor_formatter(NullFormatter())
    handles = [Line2D([], [], color=FM_COLOR[fm], marker=FM_MARKER[fm], ls="", label=FM_LABEL[fm]) for fm in FMS]
    handles += [Line2D([], [], color=INK2, ls="-", marker="o", label="PCA (main_grid)"),
                Line2D([], [], color=INK2, ls="--", marker="o", mfc=SURFACE, label="top-n boosted-tree features (fs_gbdt)"),
                Line2D([], [], color="#8a8984", lw=1.2, label="grey line (left panels): best classical AUC, same style")]
    fig.legend(handles=handles, loc="upper center", ncols=3, bbox_to_anchor=(0.5, 0.0))
    fig.suptitle("Fig. 7  Robustness to the feature reduction: PCA vs top-n features by boosted-tree importance "
                 "(fitted on training events only); mean ± sd, 5 seeds", fontsize=10, x=0.01, ha="left")
    return save(fig, "fig7_robustness_feature_selection")


def fig8(table: pd.DataFrame, rob: dict | None):
    """H2 on the n = 4, 8 slices: gap vs regularised g for PCA and for feature selection."""
    fs = table[table.experiment == "fs_gbdt"]
    if fs.empty or rob is None:
        return []
    ns = sorted(fs.n_qubits.unique())
    pca = table[(table.experiment == "main_grid") & table.n_qubits.isin(ns)]
    vmin = min(pca.log_var.min(), fs.log_var.min())
    vmax = max(pca.log_var.max(), fs.log_var.max())
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 3.8), sharey=True)
    for ax, (name, t, key) in zip(axes, (("PCA", pca, "pca"), ("top-n boosted-tree features", fs, "feature_selection"))):
        for fm in FMS:
            s = _fm_rows(t, fm)
            sc = ax.scatter(s[G_HEADLINE], s.gap_vs_best, c=s.log_var, cmap=SEQ, vmin=vmin, vmax=vmax,
                            marker=FM_MARKER[fm], s=40, edgecolors=SURFACE, linewidths=0.8, zorder=3)
        ax.axhline(0, color=INK2, lw=0.8, zorder=1)
        st = rob[key]["H2"]["pooled"]["lambda=0.01"]
        n_set = ", ".join(str(n) for n in ns)
        ax.set_title(f"{name}, n ∈ {{{n_set}}}" + "\n" + f"ρ = {fmt_ci(st)}")
        ax.set_xlabel("g_λ, λ = 0.01")
    axes[0].set_ylabel("AUC gap: fidelity QSVM − best classical")
    handles = [Line2D([], [], marker=FM_MARKER[fm], ls="", color=INK2, label=FM_LABEL[fm]) for fm in FMS]
    fig.legend(handles=handles, loc="upper center", ncols=3, bbox_to_anchor=(0.45, 0.0))
    cb = fig.colorbar(sc, ax=axes, pad=0.01, fraction=0.03)
    cb.set_label("log10 off-diagonal variance of K_Q")
    fig.suptitle("Fig. 8  H2 under the alternative feature reduction: gap vs g, one point per configuration "
                 "(Spearman ρ, 95% bootstrap CI)", fontsize=10, x=0.01, ha="left", y=1.07)
    return save(fig, "fig8_h2_feature_selection")


def figures_only(which: list[int]) -> list[Path]:
    """Regenerate only the requested figures from results/; summary_table.csv and h2_analysis.json are not touched."""
    style()
    d = load_all()
    runs = d["runs"]
    main_runs = runs[runs.experiment.isin(MAIN) & (runs.n_train == 500)]
    table = summary_table(runs) if {2, 8} & set(which) else None
    paths: list[Path] = []
    for f in which:
        if f == 1:
            paths += fig1(main_runs)
        elif f == 2:
            mt = table[table.experiment.isin(MAIN) & (table.n_train == 500)]
            paths += fig2(table, test_h2(mt, extra=False))
        elif f == 3:
            paths += fig3(runs)
        elif f == 4:
            paths += fig4(runs)
        elif f == 5:
            paths += fig5()
        elif f == 6:
            paths += fig6(d["noise"], d["hardware"])
        elif f == 7:
            paths += fig7(runs)
        elif f == 8:
            ns = sorted(runs[runs.experiment == "fs_gbdt"].n_qubits.unique())
            tp = table[(table.experiment == "main_grid") & table.n_qubits.isin(ns)]
            tf = table[table.experiment == "fs_gbdt"]
            rob = ({"pca": {"H2": test_h2(tp, extra=False)}, "feature_selection": {"H2": test_h2(tf, extra=False)}}
                   if len(tf) else None)
            paths += fig8(table, rob)
    return paths


def main(argv: list[str] | None = None):
    import argparse
    ap = argparse.ArgumentParser(description="Figures, summary table and hypothesis tests (see module docstring).")
    ap.add_argument("--fig", type=int, nargs="+", choices=range(1, 9), metavar="N",
                    help="only regenerate figure(s) N (1-8) from results/, without rewriting the analysis files")
    args = ap.parse_args(argv)
    if args.fig:
        paths = figures_only(args.fig)
        print("wrote " + (", ".join(p.relative_to(ROOT).as_posix() for p in paths) or "nothing (inputs missing)"))
        return
    style()
    hyp = load_hypotheses()
    d = load_all()
    runs = d["runs"]
    table = summary_table(runs)
    table.to_csv(RES / "summary_table.csv", index=False)
    main_runs = runs[runs.experiment.isin(MAIN) & (runs.n_train == 500)]
    main_table = table[table.experiment.isin(MAIN) & (table.n_train == 500)]
    tests = run_tests(main_runs, main_table)
    rob = robustness(runs, table)
    report = {
        "hypotheses": hyp, "source": "docs/hypotheses.md", "provenance": PROVENANCE,
        "data": "main_grid + big_qubits: PCA, N_train = 500, N_test = 1000, 5 seeds",
        "significance_rule": ("seed-paired mean difference within one seed-to-seed sd (ddof=1) -> 'not significant'; "
                              "correlations: 95% bootstrap CI over configurations containing 0 -> 'not significant'"),
        "bootstrap_resamples": N_BOOT,
        "operational_choices": {
            "concentration": "off-diagonal variance of the training kernel matrix",
            "headline_g": f"{G_HEADLINE} (regularised g, as in Fig. 4); lambda = 0, 1e-3, 1e-1 reported alongside",
            "best_classical": "max of the three classical models' test AUCs (flatters classical; see robustness bias)"},
        "verdicts": {h: tests[h]["verdict"] for h in ("H1", "H2", "H3", "H4")},
        "H1": tests["H1"], "H2": tests["H2"], "H3": tests["H3"], "H4": tests["H4"],
        "robustness_feature_selection": rob}
    (RES / "h2_analysis.json").write_text(json.dumps(report, indent=2, default=float))
    paths = (fig1(main_runs) + fig2(table, tests["H2"]) + fig3(runs) + fig4(runs) + fig5() +
             fig6(d["noise"], d["hardware"]) + fig7(runs) + fig8(table, rob))
    print(f"wrote results/summary_table.csv ({len(table)} configurations), results/h2_analysis.json and "
          f"{len(paths)} figure files in {FIG.relative_to(ROOT)}")
    for h, v in report["verdicts"].items():
        print(f"{h}: {v['held']}")
        for k, txt in v.items():
            if k != "held":
                print(f"    {txt}")
    if rob:
        print("robustness (PCA -> feature selection):",
              {h: f"{c['pca']} -> {c['feature_selection']}" for h, c in rob["verdict_comparison"].items()})


if __name__ == "__main__":
    main()
