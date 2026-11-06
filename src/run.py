"""Run one experiment (a grid of settings x seeds) from a YAML config and append results.

    python -m src.run configs/slice_n4.yaml

Results go to results/<name>/runs.jsonl (one JSON row per seed x setting) plus meta.json with
the config, package versions and git commit. Existing rows are skipped, so runs are resumable.
Classical baselines only depend on (qubits, N, seed) and are cached per experiment.
"""
from __future__ import annotations

import argparse
import itertools
import json
import platform
import subprocess
import sys
import time
import tracemalloc
from pathlib import Path

import numpy as np
import yaml

from src import classical, data, kernels, metrics


def _versions() -> dict:
    import importlib
    out = {"python": sys.version.split()[0], "platform": platform.platform()}
    for m in ["numpy", "scipy", "pandas", "sklearn", "xgboost", "yaml"]:
        try:
            out[m] = importlib.import_module(m).__version__
        except Exception:
            out[m] = None
    return out


def _git_commit() -> str | None:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL, text=True).strip()
    except Exception:
        return None


def _key(r: dict) -> str:
    return f"{r['n_qubits']}|{r['n_train']}|{r['seed']}|{r['feature_map']}|{r['reps']}|{r['bandwidth']}"


def quantum_block(d: dict, kind: str, reps: int, ent: str, c: float, K_rbf: np.ndarray,
                  lambdas: list[float], seed: int, projected: bool) -> dict:
    Xtr, Xte, ytr, yte = d["X_train"] * c, d["X_test"] * c, d["y_train"], d["y_test"]
    tracemalloc.start()
    t0 = time.perf_counter()
    S_tr = kernels.statevectors(Xtr, kind, reps, ent)
    S_te = kernels.statevectors(Xte, kind, reps, ent)
    K_tr = kernels.fidelity_kernel(S_tr)
    K_te = kernels.fidelity_kernel(S_te, S_tr)
    build_s = time.perf_counter() - t0
    peak_mb = tracemalloc.get_traced_memory()[1] / 2**20
    tracemalloc.stop()

    row = {"build_seconds": build_s, "build_peak_mb": peak_mb}
    fid = classical.precomputed_svm(K_tr, ytr, K_te, yte, seed)
    row["qsvm_auc"], row["qsvm_cv_auc"], row["qsvm_C"] = fid["auc"], fid["cv_auc"], fid["params"]["C"]
    row["qsvm_n_support"] = fid["n_support"]
    row.update({f"q_{k}": v for k, v in metrics.concentration(K_tr).items()})
    row["q_eff_dim"] = metrics.effective_dimension(K_tr)
    row["g"] = metrics.geometric_difference(K_rbf, K_tr, 0.0)
    for lam in lambdas:
        row[f"g_lam{lam:g}"] = metrics.geometric_difference(K_rbf, K_tr, lam)
    row["s_quantum"] = metrics.model_complexity(K_tr, ytr)

    if projected:
        R_tr = kernels.reduced_density_features(S_tr)
        R_te = kernels.reduced_density_features(S_te)
        d2 = kernels.sq_dists(R_tr)
        scale = 1.0 / np.median(d2[~np.eye(len(d2), dtype=bool)] + 1e-12)
        best = None
        for gs in [0.25, 0.5, 1.0, 2.0, 4.0]:  # gamma tuned on CV, relative to median distance
            Kp_tr = np.exp(-gs * scale * d2)
            res = classical.precomputed_svm(Kp_tr, ytr, kernels.projected_kernel(R_te, R_tr, gs * scale), yte, seed)
            if best is None or res["cv_auc"] > best[1]["cv_auc"]:
                best = (gs, res, Kp_tr)
        gs, res, Kp_tr = best
        row["pqk_auc"], row["pqk_cv_auc"], row["pqk_gamma_rel"] = res["auc"], res["cv_auc"], gs
        row.update({f"pqk_{k}": v for k, v in metrics.concentration(Kp_tr).items()})
        row["g_pqk"] = metrics.geometric_difference(K_rbf, Kp_tr, 0.0)
        for lam in lambdas:
            row[f"g_pqk_lam{lam:g}"] = metrics.geometric_difference(K_rbf, Kp_tr, lam)
    return row


def run(cfg: dict, out_root: str = "results", df=None, verbose: bool = True) -> Path:
    out = Path(out_root) / cfg["name"]
    out.mkdir(parents=True, exist_ok=True)
    (out / "meta.json").write_text(json.dumps(
        {"config": cfg, "versions": _versions(), "git_commit": _git_commit()}, indent=2))
    runs_path = out / "runs.jsonl"
    done = set()
    if runs_path.exists():
        done = {_key(json.loads(line)) for line in runs_path.read_text().splitlines() if line}

    if df is None:
        df = data.load(cfg["data"])
    df, cols = data.select_features(df, cfg.get("angle_diffs", True), cfg.get("mmc_flag", False))
    lambdas = cfg.get("lambdas", [1e-3, 1e-2, 1e-1])
    fmaps = cfg["feature_maps"]
    projected = cfg.get("projected", False)

    for N, n, seed in itertools.product(cfg["n_train"], cfg["qubits"], cfg["seeds"]):
        settings = [(fm, c) for fm in fmaps for c in cfg["bandwidths"]]
        base = {"n_qubits": n, "n_train": N, "seed": seed}
        todo = [(fm, c) for fm, c in settings
                if _key({**base, "feature_map": fm["kind"], "reps": fm["reps"], "bandwidth": c}) not in done]
        if not todo:
            continue
        d = data.prepare(df, cols, n, N, cfg.get("n_test", 1000), seed)
        t0 = time.perf_counter()
        base_res = classical.run_baselines(d["X_train"], d["y_train"], d["X_test"], d["y_test"], seed)
        cls_s = time.perf_counter() - t0
        gamma = base_res["rbf_svm"]["params"]["gamma"]
        K_rbf = kernels.rbf_kernel(d["X_train"], gamma=gamma)
        cls = {"logreg_auc": base_res["logreg"]["auc"], "rbf_auc": base_res["rbf_svm"]["auc"],
               "gbdt_auc": base_res["gbdt"]["auc"], "gbdt_impl": base_res["gbdt"]["impl"],
               "rbf_gamma": gamma, "rbf_C": base_res["rbf_svm"]["params"]["C"],
               "logreg_C": base_res["logreg"]["params"]["C"], "gbdt_params": base_res["gbdt"]["params"],
               "rbf_offdiag_var": metrics.concentration(K_rbf)["offdiag_var"],
               "s_classical": metrics.model_complexity(K_rbf, d["y_train"]),
               "pca_explained_variance": d["explained_variance"], "classical_seconds": cls_s}
        cls["best_classical_auc"] = max(cls["logreg_auc"], cls["rbf_auc"], cls["gbdt_auc"])
        for fm, c in todo:
            q = quantum_block(d, fm["kind"], fm["reps"], fm.get("entanglement", "linear"), c,
                              K_rbf, lambdas, seed, projected)
            row = {**base, "feature_map": fm["kind"], "reps": fm["reps"],
                   "entanglement": fm.get("entanglement", "linear"), "bandwidth": c, **cls, **q}
            row["gap_vs_best"] = row["qsvm_auc"] - row["best_classical_auc"]
            row["gap_vs_rbf"] = row["qsvm_auc"] - row["rbf_auc"]
            if projected:
                row["pqk_gap_vs_best"] = row["pqk_auc"] - row["best_classical_auc"]
            with runs_path.open("a") as f:
                f.write(json.dumps(row, default=float) + "\n")
            if verbose:
                print(f"N={N} n={n} seed={seed} {fm['kind']}{fm['reps']} c={c}: "
                      f"Q={row['qsvm_auc']:.3f} best_cl={cls['best_classical_auc']:.3f} "
                      f"g={row['g_lam0.01'] if 'g_lam0.01' in row else row['g']:.2f} var={row['q_offdiag_var']:.2e}",
                      flush=True)
    return runs_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--out", default="results")
    args = ap.parse_args()
    cfg = yaml.safe_load(Path(args.config).read_text())
    run(cfg, args.out)


if __name__ == "__main__":
    main()
