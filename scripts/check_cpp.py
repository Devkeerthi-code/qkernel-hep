"""Check the C++ kernel against the NumPy engine and benchmark both.

    python scripts/check_cpp.py            (after building cpp/build/qkernel)
Writes results/cpp_check.json.
"""
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src import kernels  # noqa: E402

BUILD = Path(__file__).resolve().parents[1] / "cpp" / "build"


def find_binary() -> Path:
    """Single-config generators put the binary in build/; MSVC/Visual Studio in build/Release/."""
    for sub in ("", "Release", "RelWithDebInfo", "Debug"):
        for name in ("qkernel.exe", "qkernel"):
            p = BUILD / sub / name
            if p.is_file():
                return p
    raise FileNotFoundError(f"qkernel binary not found under {BUILD}; build it first (see cpp/qkernel.cpp)")


BIN = None


def write(path, X):
    with open(path, "wb") as f:
        np.array(X.shape, dtype=np.int64).tofile(f)
        X.astype(np.float64).tofile(f)


def read(path):
    with open(path, "rb") as f:
        r, c = np.fromfile(f, np.int64, 2)
        return np.fromfile(f, np.float64).reshape(r, c)


def main():
    global BIN
    BIN = find_binary()
    print(f"using {BIN}")
    rows = []
    rng = np.random.default_rng(0)
    with tempfile.TemporaryDirectory() as tmp:
        for kind, reps in [("z", 2), ("zz", 1), ("zz", 2)]:
            for n in [2, 4, 6, 8, 10, 12]:
                N = 500
                X = rng.uniform(-np.pi, np.pi, (N, n))
                a, o = f"{tmp}/a.bin", f"{tmp}/k.bin"
                write(a, X)
                cpp_s = float(subprocess.check_output([str(BIN), kind, str(reps), a, a, o], text=True))
                K_cpp = read(o)
                t0 = time.perf_counter()
                K_py = kernels.fidelity_kernel(kernels.statevectors(X, kind, reps))
                py_s = time.perf_counter() - t0
                err = float(np.abs(K_cpp - K_py).max())
                rows.append({"feature_map": kind, "reps": reps, "n_qubits": n, "N": N,
                             "max_abs_diff": err, "cpp_seconds": cpp_s, "numpy_seconds": py_s})
                print(f"{kind}{reps} n={n:2d}  max|dK|={err:.1e}  C++ {cpp_s:.3f}s  NumPy {py_s:.3f}s")
                assert err < 1e-10
    out = Path(__file__).resolve().parents[1] / "results" / "cpp_check.json"
    out.write_text(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()
