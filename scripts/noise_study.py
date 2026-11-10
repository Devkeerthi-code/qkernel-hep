"""Do the main-grid conclusions survive shot noise and global depolarizing noise?

    python scripts/noise_study.py            # writes results/noise.csv and results/noise_summary.md

Part 1 (study="grid"): four main_grid settings, zz feature map reps 2, N_train=500, N_test=1000,
seeds 0-4 -- a healthy (c=0.1) and a concentrated (c=1.0) kernel at n=4 and at n=8. For each,
the fidelity QSVM is re-tuned and re-scored on kernels estimated with
kernels.shot_noisy_kernel at 100 / 1,000 / 10,000 shots (and exactly, shots="exact"), each
with global depolarizing strength p_tot in {0, 0.01, 0.05, 0.1}. Train and test kernels are
both noisy; the train diagonal is exactly 1 (never measured), the train kernel is projected
to PSD, as on hardware. The exact noiseless row must reproduce main_grid (checked).

Part 2 (study="hw_model" / "hw_observed"): the same analytic model on the exact hardware setup
of scripts/ibm_hardware_run.py (n=4, zz reps 1, 24 train + 24 test events, seed 0, 500 shots,
c=0.05 and c=0.25), with many noise draws, next to the fake_torino and ibm_marrakesh results
in results/hardware/*.json. The effective p_tot of a hardware kernel is inferred from its
off-diagonal mean: mean_hw = (1 - p) mean_exact + p / 2^n.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src import classical, data, kernels, metrics  # noqa: E402

DATA = ROOT / "data" / "atlas-higgs-challenge-2014-v2.csv.gz"
SHOTS = [None, 100, 1000, 10000]  # None = exact expectation values
P_TOT = [0.0, 0.01, 0.05, 0.1]
SEEDS = [0, 1, 2, 3, 4]
GRID = [  # (label, n_qubits, kind, reps, bandwidth)
    ("n4_healthy", 4, "zz", 2, 0.1),
    ("n4_concentrated", 4, "zz", 2, 1.0),
    ("n8_healthy", 8, "zz", 2, 0.1),
    ("n8_concentrated", 8, "zz", 2, 1.0),
]
N_TRAIN, N_TEST = 500, 1000
HW = [("hw_c0.05", 0.05), ("hw_c0.25", 0.25)]  # n=4, zz reps 1, 24+24, seed 0, 500 shots
HW_N, HW_KIND, HW_REPS, HW_NTRAIN, HW_NTEST, HW_SEED, HW_SHOTS = 4, "zz", 1, 24, 24, 0, 500
HW_DRAWS = 200


def noisy(K_tr, K_te, shots, p, n, rng):
    """Noisy train/test kernels. shots=None: depolarizing only, exact expectation values."""
    if shots is None:
        mix = lambda K: (1 - p) * K + p / 2**n  # noqa: E731
        A = mix(K_tr)
        np.fill_diagonal(A, 1.0)
        return A, mix(K_te)
    A = kernels.shot_noisy_kernel(K_tr, shots, rng, depolarizing=p, n_qubits=n)
    B = kernels.shot_noisy_kernel(K_te, shots, rng, depolarizing=p, n_qubits=n, symmetric=False)
    return A, B


def kernel_stats(K_noisy, K_exact, K_rbf=None) -> dict:
    iu = np.triu_indices(len(K_exact), 1)
    out = {"offdiag_mean": float(K_noisy[iu].mean()), "offdiag_var": float(K_noisy[iu].var()),
           "kernel_mae_train": float(np.abs(K_noisy - K_exact)[iu].mean())}
    if K_rbf is not None:
        out["g"] = metrics.geometric_difference(K_rbf, K_noisy, 0.0)
        out["g_lam0.01"] = metrics.geometric_difference(K_rbf, K_noisy, 0.01)
    return out


def rng_for(*parts) -> np.random.Generator:
    return np.random.default_rng([int(round(x * 1000)) if isinstance(x, float) else int(x) for x in parts])


def grid_part(df, cols, main: pd.DataFrame) -> list[dict]:
    rows = []
    for label, n, kind, reps, c in GRID:
        for seed in SEEDS:
            ref = main[(main.n_qubits == n) & (main.n_train == N_TRAIN) & (main.seed == seed) &
                       (main.feature_map == kind) & (main.reps == reps) & (main.bandwidth == c)]
            assert len(ref) == 1, (label, seed, len(ref))
            ref = ref.iloc[0]
            d = data.prepare(df, cols, n, N_TRAIN, N_TEST, seed)
            S_tr = kernels.statevectors(d["X_train"] * c, kind, reps)
            S_te = kernels.statevectors(d["X_test"] * c, kind, reps)
            K_tr, K_te = kernels.fidelity_kernel(S_tr), kernels.fidelity_kernel(S_te, S_tr)
            K_rbf = kernels.rbf_kernel(d["X_train"], gamma=ref["rbf_gamma"])
            t0 = time.perf_counter()
            for shots in SHOTS:
                for p in P_TOT:
                    A, B = noisy(K_tr, K_te, shots, p, n, rng_for(seed, n, c, reps, shots or 0, p))
                    res = classical.precomputed_svm(A, d["y_train"], B, d["y_test"], seed)
                    row = {"study": "grid", "config": label, "n_qubits": n, "feature_map": kind, "reps": reps,
                           "bandwidth": c, "n_train": N_TRAIN, "n_test": N_TEST, "seed": seed, "draw": 0,
                           "shots": "exact" if shots is None else shots, "p_tot": p,
                           "qsvm_auc": res["auc"], "qsvm_cv_auc": res["cv_auc"], "qsvm_C": res["params"]["C"],
                           "exact_auc": ref["qsvm_auc"], "best_classical_auc": ref["best_classical_auc"],
                           "rbf_auc": ref["rbf_auc"], "exact_offdiag_var": ref["q_offdiag_var"],
                           **kernel_stats(A, K_tr, K_rbf)}
                    row["gap_vs_best"] = row["qsvm_auc"] - row["best_classical_auc"]
                    if shots is None and p == 0.0:  # must reproduce the main grid exactly
                        assert abs(row["qsvm_auc"] - ref["qsvm_auc"]) < 1e-9, (label, seed, row["qsvm_auc"], ref["qsvm_auc"])
                        assert abs(row["g_lam0.01"] - ref["g_lam0.01"]) < 1e-6 * max(1, ref["g_lam0.01"])
                    rows.append(row)
            worst = rows[-1]  # last condition: 100 shots, p_tot=0.1
            print(f"{label} seed={seed}: exact {ref['qsvm_auc']:.3f}, 100 shots p=0.1 {worst['qsvm_auc']:.3f} "
                  f"({time.perf_counter() - t0:.0f}s)", flush=True)
    return rows


def hardware_part(df, cols) -> list[dict]:
    rows = []
    d = data.prepare(df, cols, HW_N, HW_NTRAIN, HW_NTEST, HW_SEED)
    for label, c in HW:
        S_tr = kernels.statevectors(d["X_train"] * c, HW_KIND, HW_REPS)
        S_te = kernels.statevectors(d["X_test"] * c, HW_KIND, HW_REPS)
        K_tr, K_te = kernels.fidelity_kernel(S_tr), kernels.fidelity_kernel(S_te, S_tr)
        exact = classical.precomputed_svm(K_tr, d["y_train"], K_te, d["y_test"], HW_SEED)["auc"]
        base = {"config": label, "n_qubits": HW_N, "feature_map": HW_KIND, "reps": HW_REPS, "bandwidth": c,
                "n_train": HW_NTRAIN, "n_test": HW_NTEST, "seed": HW_SEED, "exact_auc": exact,
                "exact_offdiag_var": float(K_tr[np.triu_indices(HW_NTRAIN, 1)].var())}
        for p in P_TOT:
            for draw in range(HW_DRAWS):
                A, B = noisy(K_tr, K_te, HW_SHOTS, p, HW_N, rng_for(7, c, p, draw))
                res = classical.precomputed_svm(A, d["y_train"], B, d["y_test"], HW_SEED)
                rows.append({"study": "hw_model", **base, "draw": draw, "shots": HW_SHOTS, "p_tot": p,
                             "qsvm_auc": res["auc"], "qsvm_cv_auc": res["cv_auc"], "qsvm_C": res["params"]["C"],
                             **kernel_stats(A, K_tr)})
        mean_ex = float(K_tr[np.triu_indices(HW_NTRAIN, 1)].mean())
        for f in sorted((ROOT / "results" / "hardware").glob("*_*_2*.json")):
            h = json.loads(f.read_text())
            cfg = h["config"]
            if not (cfg["n"] == HW_N and cfg["kind"] == HW_KIND and cfg["reps"] == HW_REPS and cfg["c"] == c and
                    cfg["ntrain"] == HW_NTRAIN and cfg["ntest"] == HW_NTEST and cfg["seed"] == HW_SEED and
                    cfg["shots"] == HW_SHOTS and "fidelity" in h):
                continue
            fd = h["fidelity"]
            assert abs(fd["auc_exact"] - exact) < 1e-9, (f.name, fd["auc_exact"], exact)
            p_eff = (mean_ex - fd["offdiag_mean_hardware"]) / (mean_ex - 1 / 2**HW_N)
            rows.append({"study": "hw_observed", **base, "draw": 0, "shots": HW_SHOTS, "p_tot": np.nan,
                         "p_eff": p_eff, "source": f"{h['mode']}:{h['backend']}", "file": f.name,
                         "qsvm_auc": fd["auc_hardware"], "offdiag_mean": fd["offdiag_mean_hardware"],
                         "kernel_mae_train": fd["kernel_mae_train"], "kernel_mae_test": fd["kernel_mae_test"]})
        print(f"{label}: exact {exact:.3f}, observed "
              f"{[(r['source'], round(r['qsvm_auc'], 3)) for r in rows if r['study'] == 'hw_observed' and r['config'] == label]}",
              flush=True)
    return rows


def md_table(t: pd.DataFrame, fmt: str, index: bool = True) -> str:
    """Markdown table without the optional tabulate dependency."""
    t = t.reset_index() if index else t
    cell = lambda v: (format(v, fmt) if isinstance(v, (float, np.floating)) and not np.isnan(v)  # noqa: E731
                      else ("" if isinstance(v, float) else str(v)))
    head = [str(c) for c in t.columns]
    body = [[cell(v) for v in r] for r in t.itertuples(index=False)]
    return "\n".join(["| " + " | ".join(head) + " |", "|" + "---|" * len(head)] +
                     ["| " + " | ".join(r) + " |" for r in body])


def summary(df: pd.DataFrame) -> str:
    g = df[df.study == "grid"].copy()
    g["shots"] = g["shots"].astype(str)
    order = ["exact", "10000", "1000", "100"]
    lines = ["# Noise study (scripts/noise_study.py)", "",
             "Mean over 5 seeds; zz reps 2, N_train=500, N_test=1000. Exact noiseless rows reproduce main_grid.", ""]
    for val, title in [("qsvm_auc", "Fidelity-QSVM test AUC"), ("gap_vs_best", "AUC gap to best classical"),
                       ("offdiag_var", "Off-diagonal variance of the (noisy) train kernel"),
                       ("g_lam0.01", "g(K_RBF || K_noisy), lambda=0.01")]:
        t = g.pivot_table(index=["config", "p_tot"], columns="shots", values=val, aggfunc="mean")[order]
        lines += [f"## {title}", "", md_table(t, ".3g"), ""]
    best = g.groupby("config").best_classical_auc.mean()
    lines += ["Best classical AUC (mean over seeds): " + ", ".join(f"{k} {v:.3f}" for k, v in best.items()), ""]
    m = df[df.study == "hw_model"]
    o = df[df.study == "hw_observed"]
    if len(m):
        t = m.groupby(["config", "p_tot"]).agg(auc_mean=("qsvm_auc", "mean"), auc_std=("qsvm_auc", "std"),
                                               auc_q05=("qsvm_auc", lambda s: s.quantile(0.05)),
                                               auc_q95=("qsvm_auc", lambda s: s.quantile(0.95)),
                                               mae_train=("kernel_mae_train", "mean"))
        lines += [f"## Hardware setup (n=4 zz reps 1, 24+24 events, 500 shots): analytic model, {HW_DRAWS} draws", "",
                  md_table(t, ".3f"), ""]
        lines += ["Observed:", "", md_table(o[["config", "source", "exact_auc", "qsvm_auc", "p_eff",
                                                  "kernel_mae_train"]], ".3f", index=False), ""]
    return "\n".join(lines)


def main():
    df, cols = data.select_features(data.load(str(DATA)))
    main_grid = pd.DataFrame([json.loads(line) for line in
                              (ROOT / "results" / "main_grid" / "runs.jsonl").read_text().splitlines() if line])
    rows = grid_part(df, cols, main_grid) + hardware_part(df, cols)
    out = pd.DataFrame(rows)
    out.to_csv(ROOT / "results" / "noise.csv", index=False)
    (ROOT / "results" / "noise_summary.md").write_text(summary(out), encoding="utf-8")
    print(f"wrote results/noise.csv ({len(out)} rows) and results/noise_summary.md")


if __name__ == "__main__":
    main()
