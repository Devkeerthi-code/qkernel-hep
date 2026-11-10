"""Check the C++ kernel against the NumPy engine and benchmark both.

    python scripts/check_cpp.py [--ref path/to/old/qkernel] [--repeats 5]

Needs a built binary (see cpp/qkernel.cpp). For every feature map and n it checks
max |K_cpp - K_numpy| < 1e-10 and times, end to end from angles to kernel (states + kernel,
file I/O and process start-up excluded for C++):
  numpy_seconds  kernels.statevectors (NumPy) + kernels.fidelity_kernel (one OpenBLAS ZGEMM),
                 also split into numpy_states_seconds and numpy_kernel_seconds
  cpp_seconds    cpp/build/qkernel (time it reports itself), split into cpp_states_seconds
                 and cpp_kernel_seconds; kernel_speedup_vs_numpy_blas compares the kernel step only
  ref_seconds    optional --ref binary, e.g. an older qkernel built from git, same machine
Each time is the median of --repeats runs after one untimed warm-up. Writes
results/cpp_check.json: {"meta": machine/compiler/thread context, "rows": [...]}.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src import kernels  # noqa: E402

BUILD = ROOT / "cpp" / "build"


def find_binary() -> Path:
    """Single-config generators put the binary in build/; MSVC/Visual Studio in build/Release/."""
    for sub in ("", "Release", "RelWithDebInfo", "Debug"):
        for name in ("qkernel.exe", "qkernel"):
            p = BUILD / sub / name
            if p.is_file():
                return p
    raise FileNotFoundError(f"qkernel binary not found under {BUILD}; build it first (see cpp/qkernel.cpp)")


def write(path, X):
    with open(path, "wb") as f:
        np.array(X.shape, dtype=np.int64).tofile(f)
        X.astype(np.float64).tofile(f)


def read(path):
    with open(path, "rb") as f:
        r, c = np.fromfile(f, np.int64, 2)
        return np.fromfile(f, np.float64).reshape(r, c)


def time_binary(binary: Path, kind, reps, a, o, repeats) -> tuple[list[float], np.ndarray]:
    """Median of each number the binary prints: [total] (old binaries) or [total, states, kernel]."""
    run = lambda: [float(t) for t in subprocess.check_output(  # noqa: E731
        [str(binary), kind, str(reps), a, a, o], text=True).split()]
    run()  # warm-up
    out = [run() for _ in range(repeats)]
    return [statistics.median(col) for col in zip(*out)], read(o)


def time_numpy(X, kind, reps, repeats) -> tuple[list[float], np.ndarray]:
    """Medians of [total, statevectors, fidelity_kernel] seconds."""
    def run():
        t0 = time.perf_counter()
        S = kernels.statevectors(X, kind, reps)
        t1 = time.perf_counter()
        K = kernels.fidelity_kernel(S)
        t2 = time.perf_counter()
        return [t2 - t0, t1 - t0, t2 - t1], K
    run()
    out = [run() for _ in range(repeats)]
    return [statistics.median(col) for col in zip(*(t for t, _ in out))], out[-1][1]


def context(binary: Path, ref: Path | None) -> dict:
    meta = {"platform": platform.platform(), "machine": platform.machine(), "cpu_count": os.cpu_count(),
            "python": sys.version.split()[0], "numpy": np.__version__,
            "OMP_NUM_THREADS": os.environ.get("OMP_NUM_THREADS"), "binary": binary.relative_to(ROOT).as_posix(),
            "ref_binary": None if ref is None else ref.name}
    try:
        import threadpoolctl
        meta["numpy_blas"] = [{k: i.get(k) for k in ("internal_api", "version", "num_threads", "architecture")}
                              for i in threadpoolctl.threadpool_info() if i.get("user_api") == "blas"]
    except ImportError:
        cfg = np.show_config(mode="dicts")["Build Dependencies"]["blas"]
        meta["numpy_blas"] = {"name": cfg.get("name"), "version": cfg.get("version")}
    if platform.system() == "Windows":
        ps = lambda cmd: subprocess.check_output(["powershell", "-NoProfile", "-Command", cmd], text=True).strip()  # noqa: E731
        try:
            meta["cpu"] = ps("(Get-CimInstance Win32_Processor).Name")
            status = ps("(Get-CimInstance Win32_Battery).BatteryStatus")  # 2 = on AC power; empty = no battery
            meta["on_ac_power"] = None if not status else status.splitlines()[0].strip() == "2"
        except Exception:
            pass
    else:
        meta["cpu"] = platform.processor()
    cache = BUILD / "CMakeCache.txt"
    if cache.is_file():
        entries = {}
        for line in cache.read_text(errors="ignore").splitlines():
            if "=" in line and ":" in line.split("=", 1)[0] and not line.startswith(("//", "#")):
                key, val = line.split("=", 1)
                entries[key.split(":", 1)[0]] = val
        for k in ("CMAKE_BUILD_TYPE", "CMAKE_GENERATOR"):
            meta[k.lower()] = entries.get(k)
        compiler = entries.get("CMAKE_CXX_COMPILER")
        if compiler:
            try:
                meta["compiler"] = subprocess.check_output([compiler, "--version"], text=True,
                                                           stderr=subprocess.STDOUT).splitlines()[0]
            except Exception:
                meta["compiler"] = Path(compiler).name
        meta["compile_flags"] = "Release: -O3 -march=native -fopenmp (MinGW: linked -static)" \
            if "MSVC" not in str(meta.get("compiler", "")) else "Release: /O2 /openmp:llvm"
    return meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", type=Path, default=None, help="reference qkernel binary to time as well")
    ap.add_argument("--repeats", type=int, default=5)
    ap.add_argument("--N", type=int, default=500)
    args = ap.parse_args()
    binary = find_binary()
    print(f"using {binary}" + (f", reference {args.ref}" if args.ref else ""))
    rows = []
    rng = np.random.default_rng(0)
    with tempfile.TemporaryDirectory() as tmp:
        for kind, reps in [("z", 2), ("zz", 1), ("zz", 2)]:
            for n in [2, 4, 6, 8, 10, 12]:
                X = rng.uniform(-np.pi, np.pi, (args.N, n))
                a, o = f"{tmp}/a.bin", f"{tmp}/k.bin"
                write(a, X)
                (cpp_s, cpp_st, cpp_k), K_cpp = time_binary(binary, kind, reps, a, o, args.repeats)
                (py_s, py_st, py_k), K_py = time_numpy(X, kind, reps, args.repeats)
                err = float(np.abs(K_cpp - K_py).max())
                row = {"feature_map": kind, "reps": reps, "n_qubits": n, "N": args.N, "max_abs_diff": err,
                       "cpp_seconds": cpp_s, "cpp_states_seconds": cpp_st, "cpp_kernel_seconds": cpp_k,
                       "numpy_seconds": py_s, "numpy_states_seconds": py_st, "numpy_kernel_seconds": py_k,
                       "speedup_vs_numpy": py_s / cpp_s, "kernel_speedup_vs_numpy_blas": py_k / cpp_k}
                msg = (f"{kind}{reps} n={n:2d}  max|dK|={err:.1e}  total C++ {cpp_s:.4f}s NumPy {py_s:.4f}s "
                       f"x{py_s / cpp_s:.2f} | kernel only C++ {cpp_k:.4f}s BLAS {py_k:.4f}s x{py_k / cpp_k:.2f}")
                if args.ref:
                    (ref_s, *_), K_ref = time_binary(args.ref, kind, reps, a, o, args.repeats)
                    row["ref_seconds"] = ref_s
                    row["ref_max_abs_diff"] = float(np.abs(K_ref - K_py).max())
                    row["speedup_vs_ref"] = ref_s / cpp_s
                    msg += f"  ref {ref_s:.4f}s (new is x{ref_s / cpp_s:.2f})"
                rows.append(row)
                print(msg, flush=True)
                assert err < 1e-10, err
    meta = context(binary, args.ref)
    meta.update({"repeats": args.repeats, "timing": "median after one warm-up; states + kernel, no file I/O"})
    out = ROOT / "results" / "cpp_check.json"
    out.write_text(json.dumps({"meta": meta, "rows": rows}, indent=2))
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
