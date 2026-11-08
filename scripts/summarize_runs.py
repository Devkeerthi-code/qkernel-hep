"""Mean +/- std over seeds of every metric in results/<name>/runs.jsonl.

    python scripts/summarize_runs.py results/slice_n4

Groups rows by (n_qubits, n_train, feature_map, reps, bandwidth) and writes summary.md and
summary.json next to runs.jsonl.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

GROUP = ["n_qubits", "n_train", "feature_map", "reps", "bandwidth"]
MODELS = [("Fidelity QSVM", "qsvm_auc"), ("Projected QSVM", "pqk_auc"), ("Logistic regression", "logreg_auc"),
          ("RBF SVM", "rbf_auc"), ("Boosted trees", "gbdt_auc")]
KERNEL = [("g(K_RBF || K_Q), lambda=0", "g"), ("g, lambda=0.01", "g_lam0.01"),
          ("g(K_RBF || K_PQK), lambda=0", "g_pqk"), ("g_pqk, lambda=0.01", "g_pqk_lam0.01"),
          ("K_Q off-diagonal mean", "q_offdiag_mean"), ("K_Q off-diagonal variance", "q_offdiag_var"),
          ("K_PQK off-diagonal variance", "pqk_offdiag_var"), ("K_RBF off-diagonal variance", "rbf_offdiag_var"),
          ("K_Q effective dimension", "q_eff_dim"),
          ("AUC gap fidelity QSVM - best classical", "gap_vs_best"),
          ("AUC gap projected QSVM - best classical", "pqk_gap_vs_best")]


def fmt(m: float, s: float) -> str:
    if abs(m) < 1e-2 and m != 0:
        return f"{m:.2e} ± {s:.1e}"
    return f"{m:.3f} ± {s:.3f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    args = ap.parse_args()
    d = Path(args.run_dir)
    df = pd.DataFrame([json.loads(line) for line in (d / "runs.jsonl").read_text().splitlines() if line])
    lines, out = [f"# {d.name}: mean ± std over seeds (std is the sample std, ddof=1)", ""], []
    for key, g in df.groupby(GROUP):
        setting = dict(zip(GROUP, key))
        seeds = sorted(g["seed"].tolist())
        lines += [f"## n={setting['n_qubits']} qubits, N={setting['n_train']}, {setting['feature_map']} map, "
                  f"reps={setting['reps']}, bandwidth={setting['bandwidth']} (seeds {seeds})", "",
                  "| Model | Test AUC |", "|---|---|"]
        rec = {**setting, "seeds": seeds, "metrics": {}}
        for label, col in MODELS + KERNEL:
            if col not in g:
                continue
            m, s = float(g[col].mean()), float(g[col].std(ddof=1)) if len(g) > 1 else 0.0
            rec["metrics"][col] = {"mean": m, "std": s, "per_seed": g.sort_values("seed")[col].tolist()}
            if (label, col) == KERNEL[0]:
                lines += ["", "| Kernel quantity | Value |", "|---|---|"]
            lines.append(f"| {label} | {fmt(m, s)} |")
        lines += ["", f"boosted-trees implementation: {', '.join(sorted(g['gbdt_impl'].unique()))}", ""]
        out.append(rec)
    (d / "summary.md").write_text("\n".join(lines), encoding="utf-8")
    (d / "summary.json").write_text(json.dumps(out, indent=2) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
