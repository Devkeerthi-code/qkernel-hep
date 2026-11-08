"""Leakage and kernel-concentration checks for one experiment config.

    python scripts/sanity_checks.py configs/slice_n4.yaml

Re-creates each seed's exact train/test split and checks:
  leakage    - no bookkeeping/label columns among features, disjoint EventIds, no identical
               feature rows shared by train and test, scaler fitted on train only, and a
               label-permutation test (shuffled training labels must give test AUC ~ 0.5)
  ceiling    - XGBoost on all 30 raw features with 50k training events: a rough upper reference
               for the AUC the 4-dimensional PCA models could reach
  concentration - off-diagonal statistics and effective dimension of K_Q, K_PQK, K_RBF
                  (K_Q ~ identity would show off-diagonal mean ~ 0 and effective dimension ~ N)
Writes results/<name>/sanity.json.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import yaml
from sklearn.metrics import roc_auc_score

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src import classical, data, kernels, metrics  # noqa: E402

BOOKKEEPING = {"EventId", "Weight", "Label", "KaggleSet", "KaggleWeight", "y"}


def kernel_stats(K: np.ndarray) -> dict:
    off = K[~np.eye(len(K), dtype=bool)]
    return {"offdiag_mean": float(off.mean()), "offdiag_var": float(off.var()),
            "offdiag_median": float(np.median(off)), "frac_offdiag_below_0.01": float((off < 0.01).mean()),
            "eff_dim": metrics.effective_dimension(K), "eff_dim_over_N": metrics.effective_dimension(K) / len(K)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    args = ap.parse_args()
    cfg = yaml.safe_load(Path(args.config).read_text())
    assert len(cfg["n_train"]) == len(cfg["qubits"]) == len(cfg["feature_maps"]) == len(cfg["bandwidths"]) == 1
    N, n, fm, c = cfg["n_train"][0], cfg["qubits"][0], cfg["feature_maps"][0], cfg["bandwidths"][0]
    runs = {r["seed"]: r for r in map(json.loads, (ROOT / "results" / cfg["name"] / "runs.jsonl").read_text().splitlines())}

    df_raw = data.load(str(ROOT / cfg["data"]))
    df, cols = data.select_features(df_raw, cfg.get("angle_diffs", True), cfg.get("mmc_flag", False))
    out = {"config": cfg, "features": cols, "feature_has_bookkeeping": sorted(BOOKKEEPING & set(cols)), "seeds": {}}

    for seed in cfg["seeds"]:
        tr, te = data.balanced_split(df, N, cfg["n_test"], seed)
        d = data.prepare(df, cols, n, N, cfg["n_test"], seed)
        assert (d["train_ids"] == tr["EventId"].to_numpy()).all()
        shared_rows = len(tr[cols].merge(te[cols].drop_duplicates(), how="inner"))
        S_tr = kernels.statevectors(d["X_train"] * c, fm["kind"], fm["reps"])
        S_te = kernels.statevectors(d["X_test"] * c, fm["kind"], fm["reps"])
        K_tr, K_te = kernels.fidelity_kernel(S_tr), kernels.fidelity_kernel(S_te, S_tr)
        r = runs[seed]
        K_rbf = kernels.rbf_kernel(d["X_train"], gamma=r["rbf_gamma"])
        R_tr = kernels.reduced_density_features(S_tr)
        d2 = kernels.sq_dists(R_tr)
        K_pqk = np.exp(-r["pqk_gamma_rel"] / np.median(d2[~np.eye(N, dtype=bool)] + 1e-12) * d2)

        rng = np.random.default_rng(1000 + seed)
        perm = [classical.precomputed_svm(K_tr, rng.permutation(d["y_train"]), K_te, d["y_test"], seed)["auc"]
                for _ in range(5)]
        true_auc = classical.precomputed_svm(K_tr, d["y_train"], K_te, d["y_test"], seed)["auc"]
        out["seeds"][seed] = {
            "event_ids_disjoint": not set(d["train_ids"]) & set(d["test_ids"]),
            "train_test_identical_feature_rows": int(shared_rows),
            "scaler_fitted_on_train_only": bool(np.allclose(d["preprocessor"].scaler.mean_,
                                                            tr[cols].to_numpy(float).mean(0))),
            "qsvm_auc_recomputed": true_auc, "qsvm_auc_in_runs": r["qsvm_auc"],
            "qsvm_auc_shuffled_train_labels": perm,
            "K_Q": kernel_stats(K_tr), "K_PQK": kernel_stats(K_pqk), "K_RBF": kernel_stats(K_rbf),
        }
        s = out["seeds"][seed]
        print(f"seed {seed}: ids disjoint={s['event_ids_disjoint']} shared rows={shared_rows} "
              f"scaler train-only={s['scaler_fitted_on_train_only']} QSVM {true_auc:.4f} (runs {r['qsvm_auc']:.4f}) "
              f"shuffled {np.mean(perm):.3f}±{np.std(perm):.3f}  K_Q offdiag mean {s['K_Q']['offdiag_mean']:.3f} "
              f"effdim {s['K_Q']['eff_dim']:.1f}/{N}", flush=True)

    # rough ceiling: XGBoost on all raw features (with -999 kept, as XGBoost handles them) and many events
    from xgboost import XGBClassifier
    feats = data.feature_columns(df_raw)
    tr, te = data.balanced_split(df, 50000, 20000, seed=0)  # df = raw columns + DPHI_*
    xgb = XGBClassifier(n_estimators=400, max_depth=6, learning_rate=0.1, n_jobs=-1, random_state=0, verbosity=0)
    xgb.fit(tr[feats], tr["y"])
    out["ceiling_xgb_all30_features_N50000"] = float(roc_auc_score(te["y"], xgb.predict_proba(te[feats])[:, 1]))
    single = {f: max(a := roc_auc_score(te["y"], te[f]), 1 - a) for f in cols}
    out["best_single_selected_feature_auc"] = dict(sorted(single.items(), key=lambda kv: -kv[1])[:3])
    out["random_state_offdiag_mean_reference"] = 1 / 2**n
    print("ceiling (XGBoost, 30 raw features, N=50k):", round(out["ceiling_xgb_all30_features_N50000"], 4))
    print("best single selected features:", {k: round(v, 3) for k, v in out["best_single_selected_feature_auc"].items()})
    path = ROOT / "results" / cfg["name"] / "sanity.json"
    path.write_text(json.dumps(out, indent=2, default=float) + "\n")
    print("wrote", path.relative_to(ROOT))


if __name__ == "__main__":
    main()
