"""Cross-check the NumPy statevector engine (src/kernels.statevectors) against Qiskit.

Two references:
* scripts/ibm_hardware_run.feature_map_circuit -- the circuits actually sent to IBM hardware
* qiskit.circuit.library z_feature_map / zz_feature_map -- Qiskit's own ZFeatureMap / ZZFeatureMap

Skipped automatically when Qiskit (or qiskit-ibm-runtime, imported by the script) is missing.
"""
import importlib.util
from pathlib import Path

import numpy as np
import pytest

pytest.importorskip("qiskit")
pytest.importorskip("qiskit_ibm_runtime")

from qiskit.circuit.library import z_feature_map, zz_feature_map  # noqa: E402
from qiskit.quantum_info import Statevector  # noqa: E402

from src import kernels  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
TOL = 1e-10
CASES = [("z", 1), ("z", 2), ("zz", 1), ("zz", 2)]


def _load_hw_script():
    spec = importlib.util.spec_from_file_location("ibm_hardware_run", ROOT / "scripts" / "ibm_hardware_run.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


hw = _load_hw_script()


def _angles(n, kind, reps, rows=8):
    # include the edges of the [-pi, pi] range used after preprocessing
    rng = np.random.default_rng(100 * n + 10 * reps + len(kind))
    X = rng.uniform(-np.pi, np.pi, (rows, n))
    X[0], X[1] = -np.pi, np.pi
    return X


@pytest.mark.parametrize("n", [2, 3, 4, 5])
@pytest.mark.parametrize("kind,reps", CASES)
def test_engine_matches_hardware_circuit(n, kind, reps):
    X = _angles(n, kind, reps)
    S = kernels.statevectors(X, kind, reps)
    for x, s in zip(X, S):
        ref = Statevector(hw.feature_map_circuit(x, kind, reps)).data
        assert np.abs(ref - s).max() < TOL


@pytest.mark.parametrize("n", [2, 3, 4, 5])
@pytest.mark.parametrize("kind,reps", CASES)
def test_engine_matches_qiskit_library_feature_map(n, kind, reps):
    qc = z_feature_map(n, reps=reps) if kind == "z" else zz_feature_map(n, reps=reps, entanglement="linear")
    X = _angles(n, kind, reps)
    S = kernels.statevectors(X, kind, reps)
    for x, s in zip(X, S):
        ref = Statevector(qc.assign_parameters(x)).data
        assert np.abs(ref - s).max() < TOL


@pytest.mark.parametrize("n", [2, 3, 4, 5])
@pytest.mark.parametrize("kind,reps", CASES)
def test_fidelity_kernel_matches_qiskit(n, kind, reps):
    X = _angles(n, kind, reps)
    S_ref = np.array([Statevector(hw.feature_map_circuit(x, kind, reps)).data for x in X])
    K_ref = np.abs(S_ref.conj() @ S_ref.T) ** 2
    K = kernels.fidelity_kernel(kernels.statevectors(X, kind, reps))
    assert np.abs(K - K_ref).max() < TOL
