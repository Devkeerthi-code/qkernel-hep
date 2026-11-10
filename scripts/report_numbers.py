"""Write report/numbers.tex: every result number quoted in report/main.tex, read from results/.

    python scripts/report_numbers.py

Each value becomes  \\defval{key}{text}  followed by a comment naming the source file and field, and
main.tex prints it with \\V{key}. No result is typed into main.tex by hand.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
OUT = ROOT / "report" / "numbers.tex"
VALS: dict[str, tuple[str, str]] = {}


def put(key: str, text: str, src: str) -> None:
    if key in VALS:
        raise KeyError(f"duplicate key {key}")
    VALS[key] = (text, src)


def num(x: float, nd: int = 3, sign: bool = False) -> str:
    s = f"{x:+.{nd}f}" if sign else f"{x:.{nd}f}"
    return r"\ensuremath{" + s.replace("-", "-") + "}"


def integer(x) -> str:
    x = int(x)
    return r"\ensuremath{" + (f"{x:,}".replace(",", "{,}")) + "}"


def sci(x: float, nd: int = 1) -> str:
    m, e = f"{x:.{nd}e}".split("e")
    return r"\ensuremath{" + f"{m}\\times10^{{{int(e)}}}" + "}"


def rho(d: dict, nd: int = 2) -> str:
    return (r"\ensuremath{" + f"{d['rho']:+.{nd}f}" + r"}~[\ensuremath{" + f"{d['ci_low']:+.{nd}f}" +
            r"}, \ensuremath{" + f"{d['ci_high']:+.{nd}f}" + "}]")


def listing(vals, fmt=lambda v: f"{v:g}") -> str:
    return r"\ensuremath{" + ", ".join(fmt(v) for v in vals) + "}"


def load(path: Path):
    return json.loads(path.read_text())


# ------------------------------------------------------------------------------------- data, design
ds = load(RES / "data_summary.json")
put("data_rows", integer(ds["n_rows"]), "data_summary.json n_rows")
put("data_signal", integer(ds["n_signal"]), "data_summary.json n_signal")
put("data_background", integer(ds["n_background"]), "data_summary.json n_background")
put("data_raw_features", integer(ds["n_features_raw"]), "data_summary.json n_features_raw")
put("data_features", integer(ds["n_selected_features"]), "data_summary.json n_selected_features")

mg = load(RES / "main_grid" / "meta.json")["config"]
bq = load(RES / "big_qubits" / "meta.json")["config"]
ns = load(RES / "n_sweep" / "meta.json")["config"]
fs = load(RES / "fs_gbdt" / "meta.json")["config"]
put("ntrain", integer(mg["n_train"][0]), "main_grid/meta.json config.n_train")
put("ntest", integer(mg["n_test"]), "main_grid/meta.json config.n_test")
put("nseeds", integer(len(mg["seeds"])), "main_grid/meta.json config.seeds")
put("qubits_main_min", integer(min(mg["qubits"])), "main_grid/meta.json config.qubits")
put("qubits_main_max", integer(max(mg["qubits"])), "main_grid/meta.json config.qubits")
put("qubits_main", listing(mg["qubits"]), "main_grid/meta.json config.qubits")
put("qubits_big", listing(bq["qubits"]), "big_qubits/meta.json config.qubits")
put("qubits_big_max", integer(max(bq["qubits"])), "big_qubits/meta.json config.qubits")
put("bandwidths", listing(mg["bandwidths"]), "main_grid/meta.json config.bandwidths")
put("bw_min", num(min(mg["bandwidths"]), 2), "main_grid/meta.json config.bandwidths")
put("bw_max", num(max(mg["bandwidths"]), 0), "main_grid/meta.json config.bandwidths")
put("bandwidths_big", listing(bq["bandwidths"]), "big_qubits/meta.json config.bandwidths")
put("lambdas", listing(mg["lambdas"]), "main_grid/meta.json config.lambdas")
put("sweep_ntrain", listing(ns["n_train"]), "n_sweep/meta.json config.n_train")
put("sweep_qubits", listing(ns["qubits"]), "n_sweep/meta.json config.qubits")
put("fs_qubits", listing(fs["qubits"]), "fs_gbdt/meta.json config.qubits")
rows = {e: sum(1 for line in (RES / e / "runs.jsonl").read_text().splitlines() if line)
        for e in ("main_grid", "big_qubits", "n_sweep", "fs_gbdt")}
put("rows_main", integer(rows["main_grid"]), "main_grid/runs.jsonl line count")
put("rows_big", integer(rows["big_qubits"]), "big_qubits/runs.jsonl line count")
put("rows_main_big", integer(rows["main_grid"] + rows["big_qubits"]), "main_grid + big_qubits runs.jsonl")
put("rows_sweep", integer(rows["n_sweep"]), "n_sweep/runs.jsonl line count")
put("rows_fs", integer(rows["fs_gbdt"]), "fs_gbdt/runs.jsonl line count")

rep = load(RES / "h2_analysis.json")
H1, H2, H3, H4 = rep["H1"], rep["H2"], rep["H3"], rep["H4"]
put("nconfigs", integer(H2["n_configs"]), "h2_analysis.json H2.n_configs")
put("nboot", integer(rep["bootstrap_resamples"]), "h2_analysis.json bootstrap_resamples")

tab = pd.read_csv(RES / "summary_table.csv")
main = tab[tab.experiment.isin(["main_grid", "big_qubits"]) & (tab.n_train == 500)]

# ------------------------------------------------------------------------------------------------ H1
for k, kern in (("fid", "fidelity"), ("pqk", "projected")):
    c = H1[kern]["vs_best_classical"]
    put(f"h1_{k}_cb", integer(c.get("classical better", 0)), f"h2_analysis.json H1.{kern}.vs_best_classical")
    put(f"h1_{k}_ns", integer(c.get("not significant", 0)), f"h2_analysis.json H1.{kern}.vs_best_classical")
    put(f"h1_{k}_qb", integer(c.get("quantum better", 0)), f"h2_analysis.json H1.{kern}.vs_best_classical")
    put(f"h1_{k}_maxgap", num(H1[kern]["max_gap_vs_best"], 4, True), f"h2_analysis.json H1.{kern}.max_gap_vs_best")
put("h1_chance", num(H1["chance_positive_hits_expected_per_kernel"], 1), "h2_analysis.json H1.chance_positive_hits_expected_per_kernel")
rb = main[(main.gap_vs_rbf_label == "quantum better") | (main.pqk_gap_vs_rbf_label == "quantum better")]
put("h1_rbf_hits", integer(len(rb)), "summary_table.csv rows with gap_vs_rbf_label or pqk_gap_vs_rbf_label == quantum better")
for i, r in enumerate(rb.sort_values(["feature_map", "reps"]).itertuples()):
    put(f"h1_rbf{i}_desc", rf"{'ZZ' if r.feature_map == 'zz' else 'Z'}, reps~{r.reps}, $n={r.n_qubits}$, $c={r.bandwidth:g}$",
        "summary_table.csv")
    put(f"h1_rbf{i}_gap", num(r.gap_vs_rbf, 4, True) + r" $\pm$ " + num(r.gap_vs_rbf_sd, 4), "summary_table.csv gap_vs_rbf, gap_vs_rbf_sd")
    put(f"h1_rbf{i}_best", num(r.gap_vs_best, 4, True), "summary_table.csv gap_vs_best")
bc = main[main.experiment == "main_grid"].groupby("n_qubits").best_classical_auc.first()
put("best_cl_n2", num(bc[2]), "summary_table.csv best_classical_auc, main_grid n=2")
put("best_cl_n10", num(bc[10]), "summary_table.csv best_classical_auc, main_grid n=10")
cvs = pd.DataFrame(H1["cv_selected_bandwidth"])
q = cvs[cvs.model == "fidelity QSVM"].set_index(["feature_map", "n_qubits"])
put("cv_z_n10_auc", num(q.loc[("Z map, reps 2", 10), "auc"]), "h2_analysis.json H1.cv_selected_bandwidth")
put("cv_z_n10_gap", num(q.loc[("Z map, reps 2", 10), "gap_vs_best"], 4, True), "h2_analysis.json H1.cv_selected_bandwidth")
put("cv_zz2_n10_gap", num(q.loc[("ZZ map, reps 2", 10), "gap_vs_best"], 3, True), "h2_analysis.json H1.cv_selected_bandwidth")
put("cv_zz2_n14_auc", num(q.loc[("ZZ map, reps 2", 14), "auc"]), "h2_analysis.json H1.cv_selected_bandwidth")
put("cv_zz2_n14_gap", num(q.loc[("ZZ map, reps 2", 14), "gap_vs_best"], 3, True), "h2_analysis.json H1.cv_selected_bandwidth")
first_behind = int(q[(q.index.get_level_values(0).str.startswith("ZZ")) & (q.gap_vs_best_label == "classical better")]
                   .index.get_level_values(1).min())
put("cv_zz_first_behind", integer(first_behind), "h2_analysis.json H1.cv_selected_bandwidth (smallest n with ZZ classical better)")

# ------------------------------------------------------------------------------------------------ H2
lam_keys = [("l0", "lambda=0"), ("l0001", "lambda=0.001"), ("l001", "lambda=0.01"), ("l01", "lambda=0.1")]
for k, lk in lam_keys:
    put(f"h2_pool_{k}", rho(H2["pooled"][lk]), f"h2_analysis.json H2.pooled.{lk}")
    put(f"h2_part_{k}", rho(H2["partial_controlling_log_var"][lk]), f"h2_analysis.json H2.partial_controlling_log_var.{lk}")
    for fm, fk in (("Z map, reps 2", "z"), ("ZZ map, reps 1", "zza"), ("ZZ map, reps 2", "zzb")):
        put(f"h2_within_{k}_{fk}", rho(H2["within_feature_map"][lk][fm]), f"h2_analysis.json H2.within_feature_map.{lk}")
        put(f"h2_wpart_{k}_{fk}", rho(H2["within_feature_map_partial"][lk][fm]), f"h2_analysis.json H2.within_feature_map_partial.{lk}")
put("h2_logvar", rho(H2["pooled"]["log_kernel_variance (reference)"]), "h2_analysis.json H2.pooled.log_kernel_variance")
la = H2["label_aware"]
put("h2_ratio_pool", rho(la["pooled"]), "h2_analysis.json H2.label_aware.pooled")
put("h2_ratio_part", rho(la["partial_controlling_log_var"]), "h2_analysis.json H2.label_aware.partial_controlling_log_var")
put("h2_sc_min", num(la["bound_regime"]["s_classical_min"], 1), "h2_analysis.json H2.label_aware.bound_regime.s_classical_min")
put("h2_sq_auc", rho(la["bound_regime"]["spearman_s_quantum_vs_qsvm_auc"]), "h2_analysis.json H2.label_aware.bound_regime")
nc = H2["huang_necessary_condition"]
put("sqrtN", num(nc["sqrt_N"], 1), "h2_analysis.json H2.huang_necessary_condition.sqrt_N")
for k, lk in lam_keys:
    b = nc["by_lambda"][lk]
    mx = b["max_g"]
    put(f"nc_max_{k}", sci(mx, 1) if mx >= 1e3 else num(mx, 1), f"h2_analysis.json H2.huang_necessary_condition.by_lambda.{lk}.max_g")
    put(f"nc_above_{k}", integer(b["n_above_sqrt_N"]), f"h2_analysis.json H2.huang_necessary_condition.by_lambda.{lk}.n_above_sqrt_N")
    put(f"nc_above_{k}_cb", integer(b["gap_labels_above"].get("classical better", 0)), f"... {lk}.gap_labels_above")
    put(f"nc_above_{k}_ns", integer(b["gap_labels_above"].get("not significant", 0)), f"... {lk}.gap_labels_above")

# ------------------------------------------------------------------------------------------------ H3
tr = pd.DataFrame(H3["trend_vs_qubits"])
put("h3_cells", integer(len(tr)), "h2_analysis.json H3.trend_vs_qubits")
put("h3_held", integer(tr.H3_holds_here.sum()), "h2_analysis.json H3.trend_vs_qubits.H3_holds_here")
put("h3_held_list", "; ".join(f"{r.feature_map.replace(' map,', ',')} $c={r.bandwidth:g}$" for r in tr[tr.H3_holds_here].itertuples()),
    "h2_analysis.json H3.trend_vs_qubits")
zz = tr[tr.feature_map.str.startswith("ZZ") & (tr.bandwidth >= 0.25)]
put("h3_slope_min", num(-zz.log10_var_slope_per_qubit.max(), 2), "h2_analysis.json H3.trend_vs_qubits (ZZ, c>=0.25)")
put("h3_slope_max", num(-zz.log10_var_slope_per_qubit.min(), 2), "h2_analysis.json H3.trend_vs_qubits (ZZ, c>=0.25)")
zmap = tr[tr.feature_map.str.startswith("Z map")]
put("h3_z_auc_rises", integer((zmap.auc_trend == "rises").sum()), "h2_analysis.json H3.trend_vs_qubits (Z map auc_trend)")
put("h3_z_cells", integer(len(zmap)), "h2_analysis.json H3.trend_vs_qubits (Z map)")
reg = list(H3["low_variance_regimes"].values())
put("h3_conc_n", integer(reg[0]["n_configs"]), "h2_analysis.json H3.low_variance_regimes[concentrated]")
put("h3_conc_med", num(reg[0]["qsvm_auc_median"]), "h2_analysis.json H3.low_variance_regimes[concentrated]")
put("h3_conc_max", num(reg[0]["qsvm_auc_max"]), "h2_analysis.json H3.low_variance_regimes[concentrated]")
put("h3_flat_n", integer(reg[1]["n_configs"]), "h2_analysis.json H3.low_variance_regimes[near-constant]")
put("h3_flat_med", num(reg[1]["qsvm_auc_median"]), "h2_analysis.json H3.low_variance_regimes[near-constant]")
dep = pd.DataFrame(H3["depth_zz_reps2_vs_reps1"])
put("h3_depth_cells", integer(len(dep)), "h2_analysis.json H3.depth_zz_reps2_vs_reps1")
put("h3_depth_more_conc", integer((dep.var_label == "reps 2 more concentrated").sum()), "h2_analysis.json H3.depth_zz_reps2_vs_reps1")
put("h3_depth_auc_lower", integer((dep.auc_label == "reps 2 worse").sum()), "h2_analysis.json H3.depth_zz_reps2_vs_reps1")
put("h3_rho_var_auc", rho(H3["spearman_log_var_vs_qsvm_auc"]), "h2_analysis.json H3.spearman_log_var_vs_qsvm_auc")
ex = main[(main.feature_map == "zz") & (main.reps == 2) & (main.bandwidth == 1.0)].set_index("n_qubits")
put("ex_zz2_c1_var_n2", sci(ex.loc[2, "q_offdiag_var"], 1), "summary_table.csv zz2 c=1 n=2 q_offdiag_var")
put("ex_zz2_c1_var_n14", sci(ex.loc[14, "q_offdiag_var"], 1), "summary_table.csv zz2 c=1 n=14 q_offdiag_var")
put("ex_zz2_c1_auc_n2", num(ex.loc[2, "qsvm_auc"]), "summary_table.csv zz2 c=1 n=2 qsvm_auc")
put("ex_zz2_c1_auc_n14", num(ex.loc[14, "qsvm_auc"]), "summary_table.csv zz2 c=1 n=14 qsvm_auc")

# ------------------------------------------------------------------------------------------------ H4
cells = pd.DataFrame(H4["cells"])
put("h4_cells", integer(len(cells)), "h2_analysis.json H4.cells")
put("h4_auc_rec", integer(cells.performance_recovered.sum()), "h2_analysis.json H4.cells.performance_recovered")
put("h4_var_raised", integer(cells.concentration_reduced.sum()), "h2_analysis.json H4.cells.concentration_reduced")
put("h4_g01_mono", integer(cells["g_lam0.01_monotone_toward_1"].sum()), "h2_analysis.json H4.cells.g_lam0.01_monotone_toward_1")
put("h4_g01_small_min", num(cells["g_lam0.01_small_c"].min(), 1), "h2_analysis.json H4.cells.g_lam0.01_small_c")
put("h4_g01_small_max", num(cells["g_lam0.01_small_c"].max(), 1), "h2_analysis.json H4.cells.g_lam0.01_small_c")
zzc = cells[cells.feature_map.str.startswith("ZZ")]
put("h4_g01_argmax_zz", listing(sorted(zzc["g_lam0.01_argmax_c"].unique())), "h2_analysis.json H4.cells.g_lam0.01_argmax_c (ZZ)")
put("h4_g0_closer", integer(cells.g_lam0_closer_to_1_at_small_c.sum()), "h2_analysis.json H4.cells.g_lam0_closer_to_1_at_small_c")
put("h4_g0_mono", integer(cells.g_lam0_monotone_toward_1.sum()), "h2_analysis.json H4.cells.g_lam0_monotone_toward_1")
put("h4_g0_small_min", num(cells.g_lam0_small_c.min(), 1), "h2_analysis.json H4.cells.g_lam0_small_c")
put("h4_g0_small_max", integer(round(cells.g_lam0_small_c.max())), "h2_analysis.json H4.cells.g_lam0_small_c")
put("h4_g0_large_min", integer(round(cells.g_lam0_large_c.min())), "h2_analysis.json H4.cells.g_lam0_large_c")
put("h4_g0_large_max", sci(cells.g_lam0_large_c.max(), 1), "h2_analysis.json H4.cells.g_lam0_large_c")
e8 = cells[(cells.feature_map == "ZZ map, reps 2") & (cells.n_qubits == 8)].iloc[0]
put("ex_h4_auc_small", num(e8.auc_small), "h2_analysis.json H4.cells (ZZ reps 2, n=8) auc_small")
put("ex_h4_auc_large", num(e8.auc_large), "h2_analysis.json H4.cells (ZZ reps 2, n=8) auc_large")
put("ex_h4_dvar", num(e8.dlog10_var_small_minus_large, 1), "h2_analysis.json H4.cells (ZZ reps 2, n=8) dlog10_var")
put("ex_h4_g01_small", num(e8["g_lam0.01_small_c"], 1), "h2_analysis.json H4.cells (ZZ reps 2, n=8)")
put("ex_h4_g01_large", num(e8["g_lam0.01_large_c"], 1), "h2_analysis.json H4.cells (ZZ reps 2, n=8)")
put("ex_h4_g01_argmax", num(e8["g_lam0.01_argmax_c"], 2), "h2_analysis.json H4.cells (ZZ reps 2, n=8)")

# ---------------------------------------------------------------------------------------- robustness
rob = rep["robustness_feature_selection"]
put("rob_unchanged", integer(sum(not c["changed"] for c in rob["verdict_comparison"].values())), "h2_analysis.json robustness.verdict_comparison")
ca = rob["classical_auc"]
for side, sk in (("pca", "pca"), ("feature_selection", "fs")):
    for n in ("n4", "n8"):
        put(f"rob_bc_{sk}_{n}", num(ca[side][n]["best_classical_auc"]), f"h2_analysis.json robustness.classical_auc.{side}.{n}")
        put(f"rob_gbdt_{sk}_{n}", num(ca[side][n]["gbdt_auc"]), f"h2_analysis.json robustness.classical_auc.{side}.{n}")
        put(f"rob_rbf_{sk}_{n}", num(ca[side][n]["rbf_auc"]), f"h2_analysis.json robustness.classical_auc.{side}.{n}")
mc = rob["median_change_fs_minus_pca"]
put("rob_dq", num(mc["qsvm_auc"], 3, True), "h2_analysis.json robustness.median_change_fs_minus_pca.qsvm_auc")
put("rob_dbc", num(mc["best_classical_auc"], 3, True), "h2_analysis.json robustness.median_change_fs_minus_pca.best_classical_auc")
put("rob_dvar", num(mc["log10_var"], 2, True), "h2_analysis.json robustness.median_change_fs_minus_pca.log10_var")
put("rob_bias", num(rob["best_of_three_test_auc_bias"]["mean_max_of_test_minus_cv_selected"], 4), "h2_analysis.json robustness.best_of_three_test_auc_bias")
for side, sk in (("pca", "pca"), ("feature_selection", "fs")):
    s = rob[side]
    put(f"rob_{sk}_nconf", integer(s["H1"]["n_configs"]), f"h2_analysis.json robustness.{side}.H1.n_configs")
    for k, kern in (("fid", "fidelity"), ("pqk", "projected")):
        c = s["H1"][kern]["vs_best_classical"]
        put(f"rob_{sk}_{k}_qb", integer(c.get("quantum better", 0)), f"h2_analysis.json robustness.{side}.H1.{kern}")
        if "vs_cv_selected_classical" in s["H1"][kern]:
            cv = s["H1"][kern]["vs_cv_selected_classical"]
            put(f"rob_{sk}_{k}_cv_qb", integer(cv.get("quantum better", 0)), f"h2_analysis.json robustness.{side}.H1.{kern}.vs_cv_selected_classical")
    for k, lk in lam_keys:
        put(f"rob_{sk}_h2_{k}", rho(s["H2"]["pooled"][lk]), f"h2_analysis.json robustness.{side}.H2.pooled.{lk}")
        put(f"rob_{sk}_h2part_{k}", rho(s["H2"]["partial_controlling_log_var"][lk]), f"h2_analysis.json robustness.{side}.H2.partial.{lk}")
    t3 = pd.DataFrame(s["H3"]["trend_vs_qubits"])
    put(f"rob_{sk}_h3_held", integer(t3.H3_holds_here.sum()), f"h2_analysis.json robustness.{side}.H3")
    put(f"rob_{sk}_h3_cells", integer(len(t3)), f"h2_analysis.json robustness.{side}.H3")
    c4 = pd.DataFrame(s["H4"]["cells"])
    put(f"rob_{sk}_h4_cells", integer(len(c4)), f"h2_analysis.json robustness.{side}.H4")
    put(f"rob_{sk}_h4_auc", integer(c4.performance_recovered.sum()), f"h2_analysis.json robustness.{side}.H4")
    put(f"rob_{sk}_h4_var", integer(c4.concentration_reduced.sum()), f"h2_analysis.json robustness.{side}.H4")
    put(f"rob_{sk}_h4_g", integer(c4["g_lam0.01_monotone_toward_1"].sum()), f"h2_analysis.json robustness.{side}.H4")
ang = rob["angle_spread"]
for k in ("pca_n4", "pca_n8", "gbdt_importance_n4", "gbdt_importance_n8"):
    put(f"ang_{k.replace('gbdt_importance', 'fs')}", num(ang[k]["median_iqr_radians"], 2), f"h2_analysis.json robustness.angle_spread.{k}")
sel = rob["selected_features"]
top2 = {tuple(sorted(v[:2])) for v in sel.values()}
assert len(top2) == 1, top2
put("rob_top2", " and ".join(r"\texttt{" + f.replace("_", r"\_") + "}" for f in sorted(next(iter(top2)))),
    "h2_analysis.json robustness.selected_features (first two in every seed and n)")

# -------------------------------------------------------------------------------------- noise study
nz = pd.read_csv(RES / "noise.csv")
g = nz[nz.study == "grid"].copy()
g["shots"] = g.shots.astype(str)
m = g.groupby(["config", "shots", "p_tot"])[["qsvm_auc", "offdiag_var", "best_classical_auc"]].mean()
put("nz_shots", listing(sorted(int(s) for s in g.shots.unique() if s != "exact")), "noise.csv shots")
put("nz_p", listing(sorted(p for p in g.p_tot.unique() if p > 0)), "noise.csv p_tot")
put("nz_c_healthy", num(g[g.config == "n4_healthy"].bandwidth.iloc[0], 1), "noise.csv bandwidth (healthy)")
put("nz_c_conc", num(g[g.config == "n4_concentrated"].bandwidth.iloc[0], 1), "noise.csv bandwidth (concentrated)")
for cfg, k in (("n4_healthy", "h4"), ("n8_healthy", "h8")):
    for shots, sk in (("exact", "ex"), ("10000", "10k"), ("1000", "1k"), ("100", "100")):
        put(f"nz_{k}_{sk}", num(m.loc[(cfg, shots, 0.0), "qsvm_auc"]), f"noise.csv mean qsvm_auc {cfg} shots={shots} p=0")
    put(f"nz_{k}_ex_p01", num(m.loc[(cfg, "exact", 0.1), "qsvm_auc"]), f"noise.csv mean qsvm_auc {cfg} exact p=0.1")
    put(f"nz_{k}_100_p01", num(m.loc[(cfg, "100", 0.1), "qsvm_auc"]), f"noise.csv mean qsvm_auc {cfg} 100 shots p=0.1")
conc = m.loc[["n4_concentrated", "n8_concentrated"], "qsvm_auc"]
put("nz_conc_min", num(conc.min()), "noise.csv mean qsvm_auc, concentrated configs, all conditions")
put("nz_conc_max", num(conc.max()), "noise.csv mean qsvm_auc, concentrated configs, all conditions")
for cfg, k in (("n4_healthy", "bc4"), ("n8_healthy", "bc8")):
    put(f"nz_{k}", num(m.loc[(cfg, "exact", 0.0), "best_classical_auc"]), f"noise.csv mean best_classical_auc {cfg}")
put("nz_var8c_ex", sci(m.loc[("n8_concentrated", "exact", 0.0), "offdiag_var"], 2), "noise.csv mean offdiag_var n8_concentrated exact p=0")
put("nz_var8c_100", sci(m.loc[("n8_concentrated", "100", 0.0), "offdiag_var"], 2), "noise.csv mean offdiag_var n8_concentrated 100 shots p=0")

# ------------------------------------------------------------------------------------------ hardware
hwfile = sorted((RES / "hardware").glob("real_ibm_marrakesh_*.json"))[-1]
hw = load(hwfile)
put("hw_backend", r"\texttt{" + hw["backend"].replace("_", r"\_") + "}", f"{hwfile.name} backend")
put("hw_n", integer(hw["config"]["n"]), f"{hwfile.name} config.n")
put("hw_reps", integer(hw["config"]["reps"]), f"{hwfile.name} config.reps")
put("hw_c", num(hw["config"]["c"], 2), f"{hwfile.name} config.c")
put("hw_ntrain", integer(hw["config"]["ntrain"]), f"{hwfile.name} config.ntrain")
put("hw_ntest", integer(hw["config"]["ntest"]), f"{hwfile.name} config.ntest")
put("hw_shots", integer(hw["config"]["shots"]), f"{hwfile.name} config.shots")
put("hw_circuits", integer(hw["n_circuits"]), f"{hwfile.name} n_circuits")
put("hw_depth", integer(hw["mean_depth"]), f"{hwfile.name} mean_depth")
put("hw_2q", integer(hw["mean_2q_gates"]), f"{hwfile.name} mean_2q_gates")
put("hw_qpu_s", integer(round(hw["quantum_seconds"])), f"{hwfile.name} quantum_seconds")
put("hw_auc_exact", num(hw["fidelity"]["auc_exact"]), f"{hwfile.name} fidelity.auc_exact")
put("hw_auc_real", num(hw["fidelity"]["auc_hardware"]), f"{hwfile.name} fidelity.auc_hardware")
put("hw_pqk_exact", num(hw["projected"]["auc_exact"]), f"{hwfile.name} projected.auc_exact")
put("hw_pqk_real", num(hw["projected"]["auc_hardware"]), f"{hwfile.name} projected.auc_hardware")
put("hw_mae_real", num(hw["fidelity"]["kernel_mae_train"]), f"{hwfile.name} fidelity.kernel_mae_train")
put("hw_mean_exact", num(hw["fidelity"]["offdiag_mean_exact"]), f"{hwfile.name} fidelity.offdiag_mean_exact")
put("hw_mean_real", num(hw["fidelity"]["offdiag_mean_hardware"]), f"{hwfile.name} fidelity.offdiag_mean_hardware")
fake = [load(f) for f in sorted((RES / "hardware").glob("fake_*.json"))]
fk = [f for f in fake if math.isclose(f["config"]["c"], hw["config"]["c"])][0]
put("hw_fake_backend", r"\texttt{" + fk["backend"].replace("_", r"\_") + "}", "fake_*.json backend (same c)")
put("hw_auc_fake", num(fk["fidelity"]["auc_hardware"]), "fake_*.json (same c) fidelity.auc_hardware")
put("hw_pqk_fake", num(fk["projected"]["auc_hardware"]), "fake_*.json (same c) projected.auc_hardware")
put("hw_mae_fake", num(fk["fidelity"]["kernel_mae_train"]), "fake_*.json (same c) fidelity.kernel_mae_train")
obs = nz[nz.study == "hw_observed"]
c05 = obs[np.isclose(obs.bandwidth, hw["config"]["c"])]
put("hw_peff_real", num(c05[c05.source.str.startswith("real")].p_eff.iloc[0]), "noise.csv hw_observed real p_eff")
put("hw_peff_fake", num(c05[c05.source.str.startswith("fake")].p_eff.iloc[0]), "noise.csv hw_observed fake p_eff")
hm = nz[(nz.study == "hw_model") & np.isclose(nz.bandwidth, hw["config"]["c"])]
put("hw_draws", integer(hm.draw.nunique()), "noise.csv hw_model draws")
for p, k in ((0.0, "p0"), (0.1, "p01")):
    s = hm[np.isclose(hm.p_tot, p)].qsvm_auc
    put(f"hwm_{k}_mean", num(s.mean()), f"noise.csv hw_model c={hw['config']['c']} p={p} qsvm_auc mean")
    put(f"hwm_{k}_q05", num(s.quantile(0.05)), f"noise.csv hw_model p={p} 5% quantile")
    put(f"hwm_{k}_q95", num(s.quantile(0.95)), f"noise.csv hw_model p={p} 95% quantile")
    put(f"hwm_{k}_mae", num(hm[np.isclose(hm.p_tot, p)].kernel_mae_train.mean()), f"noise.csv hw_model p={p} kernel_mae_train mean")

# ----------------------------------------------------------------------------------------- write out
lines = ["% Generated by scripts/report_numbers.py from results/ -- do not edit by hand.",
         r"\makeatletter",
         r"\newcommand{\defval}[2]{\expandafter\def\csname qk@#1\endcsname{#2}}",
         r"\newcommand{\V}[1]{\ifcsname qk@#1\endcsname\csname qk@#1\endcsname\else"
         r"\PackageError{numbers}{Undefined value #1}{}\fi}",
         r"\makeatother"]
for k, (text, src) in VALS.items():
    lines.append(f"\\defval{{{k}}}{{{text}}}% {src}")
OUT.parent.mkdir(exist_ok=True)
OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"wrote {OUT.relative_to(ROOT)} with {len(VALS)} values")
