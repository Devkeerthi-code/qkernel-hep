"""Figures, summary table and hypothesis tests for the qkernel-hep study.

    python scripts/make_figures.py        # all figures + results/summary_table.csv + results/h2_analysis.json

Inputs: results/{main_grid,n_sweep,big_qubits}/runs.jsonl, results/noise.csv, results/hardware/*.json,
and (for Fig 5 only) the ATLAS CSV in data/. Outputs go to results/figures/ as PDF and PNG.

Hypotheses (the repository does not state them formally; they are tested in their standard
literature form, and were phrased after the grid had been run, so treat the verdicts as
exploratory, not pre-registered):
  H1  a quantum kernel (fidelity or projected) is competitive with, or beats, tuned classical models
  H2  the geometric difference g(K_C || K_Q) predicts the AUC gap (quantum - classical)
  H3  kernel concentration -- off-diagonal variance of K_Q shrinking with qubit count -- degrades
      the quantum model
  H4  at fixed qubit count, a smaller bandwidth c avoids concentration and restores AUC

Significance rule (as requested): a difference whose mean over seeds is smaller in magnitude
than its seed-to-seed standard deviation (the "seed spread", ddof=1, paired by seed) is labelled
"not significant". With 5 seeds, |mean| > 1 sd corresponds to a paired t of about 2.2
(two-sided p ~ 0.09): a lenient bar. Correlations use bootstrap CIs over configurations; a CI that
contains 0 is "not significant". Configurations share data seeds, so they are not independent and
those CIs are somewhat optimistic.

Fairness choices:
  - the quantum model's bandwidth c is chosen per seed by its cross-validated AUC (not test AUC);
  - "best classical" in runs.jsonl is the max of three models' *test* AUCs (their CV AUCs are not
    stored), which flatters the classical side; H1 is therefore judged against the RBF-SVM (one
    model, CV-tuned), and best-of-three is reported alongside.
"""
from __future__ import annotations

import json
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
EXPERIMENTS = ["main_grid", "n_sweep", "big_qubits"]
KEYS = ["experiment", "n_qubits", "n_train", "feature_map", "reps", "bandwidth"]
FMS = [("z", 2), ("zz", 1), ("zz", 2)]
FM_LABEL = {("z", 2): "Z map, reps 2", ("zz", 1): "ZZ map, reps 1", ("zz", 2): "ZZ map, reps 2"}
LAMBDAS = [("g", 0.0), ("g_lam0.001", 1e-3), ("g_lam0.01", 1e-2), ("g_lam0.1", 1e-1)]
N_BOOT = 2000

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
        fig.savefig(p, dpi=200, bbox_inches="tight")
        out.append(p)
    plt.close(fig)
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
            "gap_vs_rbf", "pqk_gap_vs_best", "q_offdiag_mean", "q_offdiag_var", "log_var", "q_eff_dim",
            "g", "g_lam0.001", "g_lam0.01", "g_lam0.1", "g_pqk_lam0.01", "s_classical", "s_quantum", "log_s_ratio"]
    r = runs.copy()
    r["pqk_gap_vs_rbf"] = r.pqk_auc - r.rbf_auc
    cols.append("pqk_gap_vs_rbf")
    agg = r.groupby(KEYS)[cols].agg(["mean", "std"])
    agg.columns = [f"{a}_{b}" if b == "mean" else f"{a}_sd" for a, b in agg.columns]
    agg = agg.rename(columns={f"{c}_mean": c for c in cols})
    agg["n_seeds"] = r.groupby(KEYS).size()
    for gap in ["gap_vs_best", "gap_vs_rbf", "pqk_gap_vs_best", "pqk_gap_vs_rbf"]:
        agg[f"{gap}_label"] = [label_diff(m, s) for m, s in zip(agg[gap], agg[f"{gap}_sd"])]
    return agg.reset_index()


def cv_selected(runs: pd.DataFrame, which: str = "qsvm") -> pd.DataFrame:
    """Per (experiment, fm, n, N, seed): the bandwidth with the best CV AUC for that quantum model."""
    idx = runs.groupby(["experiment", "feature_map", "reps", "n_qubits", "n_train", "seed"])[f"{which}_cv_auc"].idxmax()
    return runs.loc[idx]


# ------------------------------------------------------------------------------------ statistics
def spearman_ci(x, y) -> dict:
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
    for _ in range(N_BOOT):
        i = rng.integers(0, len(y), len(y))
        d = stats.spearmanr(a[i], y[i])[0] - stats.spearmanr(b[i], y[i])[0]
        if np.isfinite(d):
            boots.append(d)
    lo, hi = np.quantile(boots, [0.025, 0.975])
    return {"diff": float(d0), "ci_low": float(lo), "ci_high": float(hi),
            "label": "not significant" if lo <= 0 <= hi else "significant"}


def h2_analysis(table: pd.DataFrame) -> dict:
    """H2 tests on configuration means at N_train=500 (main_grid + big_qubits)."""
    t = table[table.n_train == 500].copy()
    t = t[t.experiment.isin(["main_grid", "big_qubits"])]
    gap = t.gap_vs_best.to_numpy()
    out = {"unit": "configuration mean over 5 seeds (main_grid + big_qubits, N_train=500)", "n_configs": int(len(t)),
           "gap": "fidelity QSVM AUC - best classical AUC (gap_vs_best)",
           "expected_sign": "H2 predicts rho > 0 (larger g -> more room for a quantum advantage)",
           "pooled": {}, "within_feature_map": {}, "partial_controlling_log_var": {},
           "within_feature_map_partial": {}, "label_aware": {}}
    for col, lam in LAMBDAS:
        key = f"lambda={lam:g}"
        out["pooled"][key] = spearman_ci(t[col], gap)
        out["partial_controlling_log_var"][key] = partial_spearman(t[col], gap, t.log_var)
        out["within_feature_map"][key], out["within_feature_map_partial"][key] = {}, {}
        for fm in FMS:
            s = t[(t.feature_map == fm[0]) & (t.reps == fm[1])]
            out["within_feature_map"][key][FM_LABEL[fm]] = spearman_ci(s[col], s.gap_vs_best)
            out["within_feature_map_partial"][key][FM_LABEL[fm]] = partial_spearman(s[col], s.gap_vs_best, s.log_var)
    out["pooled"]["log_kernel_variance"] = spearman_ci(t.log_var, gap)

    # (c) label-aware criterion of Huang et al.: s_C <= g^2 s_Q, so a quantum advantage needs s_C / s_Q large
    la = out["label_aware"]
    la["definition"] = ("log10(s_classical / s_quantum); s = ridge-regularised model complexity "
                        "(src.metrics.model_complexity, a stand-in for Huang et al.'s s_K(N))")
    la["pooled"] = spearman_ci(t.log_s_ratio, gap)
    la["partial_controlling_log_var"] = partial_spearman(t.log_s_ratio, gap, t.log_var)
    la["within_feature_map"] = {FM_LABEL[fm]: spearman_ci(s.log_s_ratio, s.gap_vs_best)
                                for fm in FMS for s in [t[(t.feature_map == fm[0]) & (t.reps == fm[1])]]}
    la["ratio_minus_g"] = {f"lambda={lam:g}": rho_difference(t.log_s_ratio, t[col], gap) for col, lam in LAMBDAS}
    la["ratio_minus_log_var"] = rho_difference(t.log_s_ratio, t.log_var, gap)
    la["note"] = ("H2 expects rho > 0. ratio_minus_g is the signed difference of the two Spearman rhos: "
                  "a CI excluding 0 means the two quantities differ in how they track the gap")
    # Huang et al.'s bound is error ~ sqrt(s_K(N) / N); our s already equals s_K(N) / N, so the bound is only
    # informative when s << 1. Record how often that holds.
    la["bound_regime"] = {
        "s_classical_min": float(t.s_classical.min()), "s_classical_median": float(t.s_classical.median()),
        "fraction_s_classical_below_1": float((t.s_classical < 1).mean()),
        "fraction_s_quantum_below_1": float((t.s_quantum < 1).mean()),
        "spearman_s_quantum_vs_qsvm_auc": spearman_ci(t.s_quantum, t.qsvm_auc),
        "median_s_quantum_when_var_below_1e-3": float(t[t.q_offdiag_var < 1e-3].s_quantum.median()),
        "interpretation": ("s = alpha^T K alpha / N equals Huang et al.'s s_K(N)/N, so their bound ~ sqrt(s) is "
                           "vacuous for s >~ 1. s_classical is never below 1 here, and near-identity (concentrated) "
                           "quantum kernels get s_quantum ~ 1 because they memorise the labels; the ratio "
                           "s_C/s_Q therefore mostly flags memorising kernels, which generalise worst. The "
                           "label-aware test is run outside the regime where the bound means anything.")}

    # classification view: can each quantity rank configurations that are competitive
    # (gap not significantly below 0) above those that are not?
    competitive = (t.gap_vs_best_label != "classical better").to_numpy()
    cls = {"definition": "AUC for separating configurations whose gap is not significantly negative",
           "n_competitive": int(competitive.sum()), "n_total": int(len(t))}
    for name, v in [("g_lam0.01", t["g_lam0.01"]), ("g_lam0", t["g"]), ("log_s_ratio", t.log_s_ratio),
                    ("log_var", t.log_var)]:
        cls[name] = float(roc_auc_score(competitive, v)) if 0 < competitive.sum() < len(t) else None
    out["classification"] = cls

    # sensitivity: projected kernel
    pt = t.copy()
    out["projected_kernel_pooled"] = {f"lambda={lam:g}" if lam else "lambda=0": spearman_ci(pt[c], pt.pqk_gap_vs_best)
                                      for c, lam in [("g_pqk_lam0.01", 1e-2)]}
    return out


def h1_analysis(runs: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for which in ("qsvm", "pqk"):
        sel = cv_selected(runs[runs.n_train == 500], which)
        sel = sel.assign(vs_rbf=sel[f"{which}_auc"] - sel.rbf_auc, vs_best=sel[f"{which}_auc"] - sel.best_classical_auc)
        for (kind, reps, n), g in sel.groupby(["feature_map", "reps", "n_qubits"]):
            rows.append({"model": "fidelity QSVM" if which == "qsvm" else "projected QSVM",
                         "feature_map": FM_LABEL[(kind, reps)], "n_qubits": n, "n_seeds": len(g),
                         "bandwidths_searched": int(runs[(runs.n_train == 500) & (runs.feature_map == kind) &
                                                         (runs.reps == reps) & (runs.n_qubits == n)].bandwidth.nunique()),
                         "auc": g[f"{which}_auc"].mean(), "gap_vs_rbf": g.vs_rbf.mean(), "gap_vs_rbf_sd": g.vs_rbf.std(),
                         "gap_vs_rbf_label": label_diff(g.vs_rbf.mean(), g.vs_rbf.std()),
                         "gap_vs_best": g.vs_best.mean(), "gap_vs_best_sd": g.vs_best.std(),
                         "gap_vs_best_label": label_diff(g.vs_best.mean(), g.vs_best.std())})
    return pd.DataFrame(rows)


def h3_analysis(table: pd.DataFrame) -> dict:
    t = table[(table.n_train == 500) & table.experiment.isin(["main_grid", "big_qubits"])]
    slopes = []
    for (kind, reps, c), g in t.groupby(["feature_map", "reps", "bandwidth"]):
        if g.n_qubits.nunique() < 3:
            continue
        res = stats.linregress(g.n_qubits, g.log_var)
        slopes.append({"feature_map": FM_LABEL[(kind, reps)], "bandwidth": c, "n_range": f"{g.n_qubits.min()}-{g.n_qubits.max()}",
                       "log10_var_per_qubit": res.slope, "slope_ci95": 1.96 * res.stderr, "r2": res.rvalue**2,
                       "label": "decreasing" if res.slope + 1.96 * res.stderr < 0 else
                                ("increasing" if res.slope - 1.96 * res.stderr > 0 else "not significant")})
    corr = spearman_ci(t.log_var, t.qsvm_auc)
    low = t[t.q_offdiag_var < 1e-3]
    # two different low-variance regimes: concentrated towards 1/2^n (mean -> 0) vs nearly constant (mean -> 1)
    regimes = {}
    for name, mask in [("concentrated: var < 1e-3 and off-diagonal mean < 0.1", low.q_offdiag_mean < 0.1),
                       ("near-constant: var < 1e-3 and off-diagonal mean > 0.5", low.q_offdiag_mean > 0.5)]:
        s = low[mask]
        regimes[name] = {"n_configs": int(len(s)), "qsvm_auc_median": float(s.qsvm_auc.median()) if len(s) else None,
                         "qsvm_auc_max": float(s.qsvm_auc.max()) if len(s) else None,
                         "configs": sorted({f"{FM_LABEL[(k, r)]} c={c:g}" for k, r, c in
                                            zip(s.feature_map, s.reps, s.bandwidth)})}
    return {"variance_slope_vs_qubits": slopes, "spearman_log_var_vs_qsvm_auc": corr,
            "configs_with_var_below_1e-3": int(len(low)), "low_variance_regimes": regimes,
            "note": ("off-diagonal variance alone does not identify failure: nearly constant kernels (Z map, small c) "
                     "also have small variance but still classify well in exact simulation; they would be fragile "
                     "under shot noise, which the noise study did not test")}


def h4_analysis(runs: pd.DataFrame) -> list[dict]:
    out = []
    r = runs[(runs.experiment == "main_grid")]
    for n in (4, 8):
        for fm in FMS:
            s = r[(r.n_qubits == n) & (r.feature_map == fm[0]) & (r.reps == fm[1])]
            m = s.groupby("bandwidth")[["qsvm_cv_auc", "qsvm_auc", "log_var", "g_lam0.01"]].mean()
            c_best = float(m.qsvm_cv_auc.idxmax())
            a = s[s.bandwidth == c_best].set_index("seed").qsvm_auc
            b = s[s.bandwidth == 1.0].set_index("seed").qsvm_auc
            d = (a - b)
            out.append({"n_qubits": n, "feature_map": FM_LABEL[fm], "c_best_by_cv": c_best,
                        "auc_at_c_best": float(m.qsvm_auc[c_best]), "auc_at_c1": float(m.qsvm_auc[1.0]),
                        "auc_gain_vs_c1": float(d.mean()), "auc_gain_sd": float(d.std()),
                        "auc_gain_label": label_diff(d.mean(), d.std(), "smaller c better", "c=1 better"),
                        "log10_var_at_c_best": float(m.log_var[c_best]), "log10_var_at_c1": float(m.log_var[1.0]),
                        "c_with_max_g_lam0.01": float(m["g_lam0.01"].idxmax()),
                        "c_with_max_auc_is_c_with_max_g": bool(m.qsvm_auc.idxmax() == m["g_lam0.01"].idxmax())})
    return out


def verdicts(h1: pd.DataFrame, h2: dict, h3: dict, h4: list[dict]) -> dict:
    q = h1[h1.model == "fidelity QSVM"]
    better = h1[h1.gap_vs_rbf_label == "quantum better"]
    better_best = h1[h1.gap_vs_best_label == "quantum better"]
    competitive = h1[h1.gap_vs_rbf_label != "classical better"]
    # under a true gap of 0, |mean| > 1 sd with 5 seeds happens with probability ~0.09 per comparison (each sign ~0.045)
    expected = 0.045 * len(h1)
    v1 = {"held": ("no: no reliable advantage; competitive only at small n" if len(better_best) == 0 else
                   "partly: some configurations beat best-of-three"),
          "detail": (f"{len(better)} of {len(h1)} (model, map, n) combinations beat the RBF-SVM by more than the seed "
                     f"spread (" + ", ".join(f"{r.model} {r.feature_map} n={r.n_qubits}: {r.gap_vs_rbf:+.4f} ± "
                                             f"{r.gap_vs_rbf_sd:.4f}" for r in better.itertuples()) +
                     f"); ~{expected:.1f} such positive hits are expected by chance under a true gap of 0 with this "
                     f"lenient 1-sd rule; {len(better_best)} beat the best of the three classical models. "
                     f"{len(competitive)} of {len(h1)} are not significantly worse than the RBF-SVM "
                     f"(fidelity QSVM: {int((q.gap_vs_rbf_label != 'classical better').sum())} of {len(q)}), "
                     "mostly the Z map and n <= 4; ZZ maps fall significantly behind from n = 6 on")}
    pooled = h2["pooled"]["lambda=0.01"]
    within = h2["within_feature_map"]["lambda=0.01"]
    partial = h2["partial_controlling_log_var"]["lambda=0.01"]
    la = h2["label_aware"]
    pos = lambda d: d["ci_low"] > 0  # noqa: E731
    fmt = lambda d: f"{d['rho']:.2f} [{d['ci_low']:.2f}, {d['ci_high']:.2f}]"  # noqa: E731
    v2 = {"held": "yes" if pos(pooled) and pos(partial) and all(pos(w) for w in within.values()) else
          "no: g does not predict the gap in the hypothesised direction",
          "detail": (f"(pooled, lambda=0.01) rho(g, gap) = {fmt(pooled)}; (b) partial | log var = {fmt(partial)}; "
                     "(a) within map: " + ", ".join(f"{k} {fmt(w)}" for k, w in within.items()) +
                     f"; lambda=0.1 pooled {fmt(h2['pooled']['lambda=0.1'])} but partial | log var "
                     f"{fmt(h2['partial_controlling_log_var']['lambda=0.1'])}, i.e. explained by kernel variance; "
                     f"(c) label-aware log(s_C/s_Q): pooled {fmt(la['pooled'])}, partial {fmt(la['partial_controlling_log_var'])} "
                     "-- also negative, and computed where Huang's bound is vacuous (see label_aware.bound_regime)")}
    zz_dec = [s for s in h3["variance_slope_vs_qubits"] if s["feature_map"].startswith("ZZ") and s["bandwidth"] >= 0.25]
    c3 = h3["spearman_log_var_vs_qsvm_auc"]
    reg = list(h3["low_variance_regimes"].values())
    v3 = {"held": ("yes for concentration towards 1/2^n; low variance alone is not sufficient"
                   if all(s["label"] == "decreasing" for s in zz_dec) and c3["ci_low"] > 0 else "partly"),
          "detail": (f"ZZ maps at c >= 0.25: variance falls by {min(-s['log10_var_per_qubit'] for s in zz_dec):.2f}-"
                     f"{max(-s['log10_var_per_qubit'] for s in zz_dec):.2f} decades per qubit; "
                     f"rho(log var, QSVM AUC) = {fmt(c3)}; concentrated kernels (var < 1e-3, mean < 0.1, "
                     f"{reg[0]['n_configs']} configs) median AUC {reg[0]['qsvm_auc_median']:.3f}, max "
                     f"{reg[0]['qsvm_auc_max']:.3f}; near-constant kernels (var < 1e-3, mean > 0.5, "
                     f"{reg[1]['n_configs']} configs, Z map c=0.05) median AUC {reg[1]['qsvm_auc_median']:.3f}")}
    zz4 = [h for h in h4 if h["feature_map"].startswith("ZZ")]
    v4 = {"held": "yes for ZZ maps" if all(h["auc_gain_label"] == "smaller c better" for h in zz4) else "partly",
          "detail": "; ".join(f"n={h['n_qubits']} {h['feature_map']}: c*={h['c_best_by_cv']:g}, "
                              f"AUC {h['auc_at_c_best']:.3f} vs {h['auc_at_c1']:.3f} at c=1 ({h['auc_gain_label']})"
                              for h in h4)}
    return {"H1": v1, "H2": v2, "H3": v3, "H4": v4,
            "caveat": "hypotheses phrased after the grid was run: exploratory, not pre-registered"}


# --------------------------------------------------------------------------------------- figures
def _fm_rows(df, fm):
    return df[(df.feature_map == fm[0]) & (df.reps == fm[1])]


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


def main():
    style()
    d = load_all()
    runs = d["runs"]
    table = summary_table(runs)
    table.to_csv(RES / "summary_table.csv", index=False)
    h1 = h1_analysis(runs)
    h2 = h2_analysis(table)
    h3 = h3_analysis(table)
    h4 = h4_analysis(runs)
    report = {"hypotheses": {"H1": "a quantum kernel is competitive with, or beats, tuned classical models",
                             "H2": "g(K_C || K_Q) predicts the AUC gap",
                             "H3": "kernel concentration (off-diagonal variance shrinking with n) degrades the QSVM",
                             "H4": "at fixed n, smaller bandwidth c avoids concentration and restores AUC"},
              "significance_rule": ("mean difference over seeds within one seed-to-seed sd (paired, ddof=1) -> "
                                    "'not significant'; correlations: 95% bootstrap CI over configurations containing 0"),
              "verdicts": verdicts(h1, h2, h3, h4), "H2": h2, "H1": h1.to_dict(orient="records"),
              "H3": h3, "H4": h4}
    (RES / "h2_analysis.json").write_text(json.dumps(report, indent=2, default=float))
    paths = fig1(runs) + fig2(table, h2) + fig3(runs) + fig4(runs) + fig5() + fig6(d["noise"], d["hardware"])
    print(f"wrote results/summary_table.csv ({len(table)} configurations), results/h2_analysis.json and "
          f"{len(paths)} figure files in {FIG.relative_to(ROOT)}")
    for k, v in report["verdicts"].items():
        print(f"{k}: {v if isinstance(v, str) else v['held'] + ' -- ' + v['detail']}")


if __name__ == "__main__":
    main()
