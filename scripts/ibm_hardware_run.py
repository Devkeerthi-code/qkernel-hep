"""Run a small quantum-kernel experiment on IBM Quantum hardware (or a fake backend first).

Fidelity kernel: one compute-uncompute circuit U(x_j)^dagger U(x_i) per pair, K = P(0...0).
Projected kernel: per event, measure all qubits in the X, Y and Z bases -> Bloch vectors ->
single-qubit reduced density matrices -> exp(-gamma sum_k ||rho_k - rho_k'||_F^2).
Both are compared with the exact statevector kernels on the same events.

    # 1. free, local, unlimited: noisy simulation of a real IBM device
    python scripts/ibm_hardware_run.py --mode fake
    # 2. real hardware: prints a cost estimate and asks before submitting
    python scripts/ibm_hardware_run.py --mode real
    # 3. if the script was interrupted after submitting, collect results by job id
    python scripts/ibm_hardware_run.py --mode real --retrieve <job_id> [<job_id> ...]

Needs: pip install qiskit qiskit-ibm-runtime qiskit-aer, and an IBM account saved once with
QiskitRuntimeService.save_account(...) (see docs/IBM_HARDWARE.md). The API key is never read
from or written to this repository.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src import data, hardware, kernels  # noqa: E402

from qiskit import QuantumCircuit  # noqa: E402
from qiskit.quantum_info import Statevector  # noqa: E402
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager  # noqa: E402
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2  # noqa: E402

CHUNK = 250  # circuits per job


def feature_map_circuit(x: np.ndarray, kind: str, reps: int) -> QuantumCircuit:
    """Same convention as src/kernels.py: per rep H^n, P(2x_i), then CX . P(2(pi-x_i)(pi-x_j)) . CX."""
    n = len(x)
    qc = QuantumCircuit(n)
    for _ in range(reps):
        qc.h(range(n))
        for i in range(n):
            qc.p(2 * x[i], i)
        if kind == "zz":
            for i, j in kernels.entangling_pairs(n, "linear"):
                qc.cx(i, j)
                qc.p(2 * (np.pi - x[i]) * (np.pi - x[j]), j)
                qc.cx(i, j)
    return qc


def check_circuits_match_engine(X: np.ndarray, kind: str, reps: int) -> float:
    S = kernels.statevectors(X, kind, reps)
    err = max(np.abs(Statevector(feature_map_circuit(x, kind, reps)).data - s).max() for x, s in zip(X, S))
    assert err < 1e-10, f"circuit and NumPy engine disagree: {err}"
    return float(err)


def fidelity_circuit(xa, xb, kind, reps) -> QuantumCircuit:
    qc = feature_map_circuit(xa, kind, reps).compose(feature_map_circuit(xb, kind, reps).inverse())
    qc.measure_all()
    return qc


def basis_circuit(x, kind, reps, basis: str) -> QuantumCircuit:
    qc = feature_map_circuit(x, kind, reps)
    if basis == "X":
        qc.h(range(qc.num_qubits))
    elif basis == "Y":
        qc.sdg(range(qc.num_qubits))
        qc.h(range(qc.num_qubits))
    qc.measure_all()
    return qc


def get_backend(mode: str, name: str | None):
    if mode == "fake":
        from qiskit_ibm_runtime import fake_provider
        cls = getattr(fake_provider, name or "FakeTorino")
        return cls()
    service = QiskitRuntimeService()
    if name:
        return service.backend(name)
    return service.least_busy(operational=True, simulator=False, min_num_qubits=5)


def run_sampler(backend, circuits, shots, mode, retrieve_ids=None):
    """Returns (list of counts dicts, job ids, usage seconds or None)."""
    if retrieve_ids:
        service = QiskitRuntimeService()
        jobs = [service.job(j) for j in retrieve_ids]
    else:
        sampler = SamplerV2(mode=backend)
        jobs = []
        for s in range(0, len(circuits), CHUNK):
            jobs.append(sampler.run(circuits[s:s + CHUNK], shots=shots))
            print(f"submitted job {jobs[-1].job_id()} ({min(s + CHUNK, len(circuits))}/{len(circuits)} circuits)")
        if mode == "real":
            ids = [j.job_id() for j in jobs]
            (ROOT / "results" / "hardware").mkdir(parents=True, exist_ok=True)
            (ROOT / "results" / "hardware" / "pending_jobs.json").write_text(json.dumps(ids))
            print("job ids saved to results/hardware/pending_jobs.json; use --retrieve if interrupted")
    counts, usage = [], 0.0
    for j in jobs:
        res = j.result()
        counts += [r.data.meas.get_counts() for r in res]
        try:
            usage += float(j.usage())
        except Exception:
            usage = None if usage == 0.0 else usage
    return counts, [j.job_id() for j in jobs], usage


def svm_auc(K_tr, ytr, K_te, yte, seed=0):
    from src.classical import precomputed_svm
    r = precomputed_svm(K_tr, ytr, K_te, yte, seed)
    return r["auc"], r["params"]["C"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["fake", "real"], default="fake")
    ap.add_argument("--backend", default=None, help="fake class name (e.g. FakeTorino) or real device name")
    ap.add_argument("--data", default=str(ROOT / "data" / "atlas-higgs-challenge-2014-v2.csv.gz"))
    ap.add_argument("--n", type=int, default=4)
    ap.add_argument("--kind", choices=["z", "zz"], default="zz")
    ap.add_argument("--reps", type=int, default=1)
    ap.add_argument("--c", type=float, default=0.25, help="bandwidth")
    ap.add_argument("--ntrain", type=int, default=24)
    ap.add_argument("--ntest", type=int, default=24)
    ap.add_argument("--shots", type=int, default=500)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--no-fidelity", action="store_true", help="only run the (much cheaper) projected kernel")
    ap.add_argument("--yes", action="store_true", help="skip the confirmation prompt for real hardware")
    ap.add_argument("--retrieve", nargs="*", default=None, help="job ids to collect instead of submitting")
    args = ap.parse_args()

    df, cols = data.select_features(data.load(args.data))
    d = data.prepare(df, cols, args.n, args.ntrain, args.ntest, args.seed)
    Xtr, Xte = d["X_train"] * args.c, d["X_test"] * args.c
    ytr, yte = d["y_train"], d["y_test"]
    err = check_circuits_match_engine(np.vstack([Xtr[:5], Xte[:5]]), args.kind, args.reps)
    print(f"Qiskit circuits match the NumPy engine (max error {err:.1e})")

    # ---- exact reference on the same events
    S_tr, S_te = kernels.statevectors(Xtr, args.kind, args.reps), kernels.statevectors(Xte, args.kind, args.reps)
    K_tr_ex, K_te_ex = kernels.fidelity_kernel(S_tr), kernels.fidelity_kernel(S_te, S_tr)
    R_tr_ex, R_te_ex = kernels.reduced_density_features(S_tr), kernels.reduced_density_features(S_te)
    d2 = kernels.sq_dists(R_tr_ex)
    gamma = 1.0 / np.median(d2[~np.eye(len(d2), dtype=bool)])  # fixed, same for exact and hardware

    # ---- circuits
    pairs = [(i, j) for i in range(args.ntrain) for j in range(i + 1, args.ntrain)]
    test_pairs = [(i, j) for i in range(args.ntest) for j in range(args.ntrain)]
    circuits, tags = [], []
    if not args.no_fidelity:
        circuits += [fidelity_circuit(Xtr[i], Xtr[j], args.kind, args.reps) for i, j in pairs]
        circuits += [fidelity_circuit(Xte[i], Xtr[j], args.kind, args.reps) for i, j in test_pairs]
        tags += ["ftr"] * len(pairs) + ["fte"] * len(test_pairs)
    for name, X in (("ptr", Xtr), ("pte", Xte)):
        for b in "XYZ":
            circuits += [basis_circuit(x, args.kind, args.reps, b) for x in X]
            tags += [f"{name}{b}"] * len(X)

    backend = get_backend(args.mode, args.backend)
    print(f"backend: {backend.name}")
    pm = generate_preset_pass_manager(optimization_level=3, backend=backend, seed_transpiler=args.seed)
    t0 = time.perf_counter()
    isa = pm.run(circuits)
    depth = int(np.mean([c.depth() for c in isa]))
    twoq = int(np.mean([sum(v for k, v in c.count_ops().items() if k in ("cx", "cz", "ecr")) for c in isa]))
    print(f"{len(isa)} circuits, mean depth {depth}, mean 2-qubit gates {twoq} (transpiled in {time.perf_counter() - t0:.1f}s)")

    if args.mode == "real" and not args.retrieve:
        est = len(isa) * args.shots * 3e-4 + 5 * (len(isa) // CHUNK + 1)
        print(f"ROUGH QPU time estimate: ~{est / 60:.1f} min "
              f"({len(isa)} circuits x {args.shots} shots). The free Open Plan gives 10 min per 28 days.")
        if not args.yes and input("Submit to real hardware? [y/N] ").strip().lower() != "y":
            print("Not submitted.")
            return

    counts, job_ids, usage = run_sampler(backend, isa, args.shots, args.mode, args.retrieve)
    tags_arr = np.array(tags)
    out = {"timestamp": datetime.now(timezone.utc).isoformat(), "mode": args.mode, "backend": backend.name,
           "job_ids": job_ids, "quantum_seconds": usage, "config": vars(args), "n_circuits": len(isa),
           "mean_depth": depth, "mean_2q_gates": twoq, "gamma_projected": gamma}

    # ---- fidelity kernel
    if not args.no_fidelity:
        vals = np.array([hardware.fidelity_from_counts(c, args.n) for c, t in zip(counts, tags) if t == "ftr"])
        K_tr_hw = hardware.assemble_train_kernel(vals, pairs, args.ntrain)
        tv = np.array([hardware.fidelity_from_counts(c, args.n) for c, t in zip(counts, tags) if t == "fte"])
        K_te_hw = tv.reshape(args.ntest, args.ntrain)
        out["fidelity"] = {
            "auc_exact": svm_auc(K_tr_ex, ytr, K_te_ex, yte)[0],
            "auc_hardware": svm_auc(K_tr_hw, ytr, K_te_hw, yte)[0],
            "kernel_mae_train": float(np.abs(K_tr_hw - K_tr_ex)[np.triu_indices(args.ntrain, 1)].mean()),
            "kernel_mae_test": float(np.abs(K_te_hw - K_te_ex).mean()),
            "offdiag_mean_exact": float(K_tr_ex[np.triu_indices(args.ntrain, 1)].mean()),
            "offdiag_mean_hardware": float(K_tr_hw[np.triu_indices(args.ntrain, 1)].mean()),
        }

    # ---- projected kernel
    def bloch(prefix, N):
        B = np.zeros((N, args.n, 3))
        for a, b in enumerate("XYZ"):
            cs = [c for c, t in zip(counts, tags_arr) if t == f"{prefix}{b}"]
            B[:, :, a] = np.array([hardware.pauli_expectations(c, args.n) for c in cs])
        return B
    B_tr, B_te = bloch("ptr", args.ntrain), bloch("pte", args.ntest)
    R_tr_hw, R_te_hw = hardware.bloch_to_rdm_features(B_tr), hardware.bloch_to_rdm_features(B_te)
    Kp = lambda A, B=None: kernels.projected_kernel(A, B, gamma)  # noqa: E731
    out["projected"] = {
        "auc_exact": svm_auc(Kp(R_tr_ex), ytr, Kp(R_te_ex, R_tr_ex), yte)[0],
        "auc_hardware": svm_auc(Kp(R_tr_hw), ytr, Kp(R_te_hw, R_tr_hw), yte)[0],
        "bloch_mae": float(np.abs(np.concatenate([B_tr, B_te]) -
                                  np.concatenate([hardware.exact_bloch(S_tr), hardware.exact_bloch(S_te)])).mean()),
    }

    print(json.dumps({k: out[k] for k in ("backend", "quantum_seconds", "fidelity", "projected") if k in out}, indent=2))
    path = ROOT / "results" / "hardware" / f"{args.mode}_{backend.name}_{datetime.now():%Y%m%d_%H%M%S}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=2, default=float))
    print(f"saved {path}")
    print(f"note: AUC on {args.ntest} test events is a demonstration, not a statistically strong number.")


if __name__ == "__main__":
    main()
