"""Hardware-independent helpers for estimating kernels from measurement counts.

Kept free of Qiskit imports so they can be unit-tested anywhere; scripts/ibm_hardware_run.py
builds the circuits and calls these on the counts returned by IBM Quantum (or a fake backend).
"""
from __future__ import annotations

import numpy as np


def fidelity_from_counts(counts: dict, n_qubits: int) -> float:
    """Compute-uncompute estimate: K(x, x') = P(all zeros) for U(x')^dagger U(x)|0>."""
    shots = sum(counts.values())
    return counts.get("0" * n_qubits, 0) / shots


def assemble_train_kernel(values: np.ndarray, pairs: list[tuple[int, int]], N: int,
                          enforce_psd: bool = True) -> np.ndarray:
    """Symmetric N x N kernel from estimates for pairs i < j; diagonal is exactly 1."""
    K = np.eye(N)
    for v, (i, j) in zip(values, pairs):
        K[i, j] = K[j, i] = v
    if enforce_psd:
        w, V = np.linalg.eigh(K)
        K = (V * np.clip(w, 0, None)) @ V.T
    return K


def pauli_expectations(counts: dict, n_qubits: int) -> np.ndarray:
    """<P_k> for every qubit k from counts measured in one Pauli basis.

    Qiskit bitstrings are little-endian: character [-1 - k] is qubit k. Outcome 0 -> +1, 1 -> -1.
    """
    shots = sum(counts.values())
    exp = np.zeros(n_qubits)
    for bitstring, c in counts.items():
        bits = bitstring.replace(" ", "")
        for k in range(n_qubits):
            exp[k] += c * (1 - 2 * int(bits[-1 - k]))
    return exp / shots


def bloch_to_rdm_features(bloch: np.ndarray) -> np.ndarray:
    """Bloch vectors (B, n, 3) -> the same (B, 8n) features as kernels.reduced_density_features.

    rho_k = (I + x X + y Y + z Z) / 2 = [[(1+z)/2, (x - i y)/2], [(x + i y)/2, (1-z)/2]]
    """
    x, y, z = bloch[..., 0], bloch[..., 1], bloch[..., 2]
    re = np.stack([(1 + z) / 2, x / 2, x / 2, (1 - z) / 2], axis=-1)
    im = np.stack([np.zeros_like(x), -y / 2, y / 2, np.zeros_like(x)], axis=-1)
    B, n = x.shape
    return np.concatenate([re, im], axis=-1).reshape(B, 8 * n)


def exact_bloch(S: np.ndarray) -> np.ndarray:
    """Exact Bloch vectors (B, n, 3) of every qubit from statevectors (for comparison)."""
    from src.kernels import reduced_density_features
    B, dim = S.shape
    n = int(np.log2(dim))
    F = reduced_density_features(S).reshape(B, n, 8)
    re, im = F[..., :4], F[..., 4:]
    x = 2 * re[..., 2]          # rho_10 real part = x / 2
    y = 2 * im[..., 2]          # rho_10 imag part = y / 2
    z = re[..., 0] - re[..., 3]  # rho_00 - rho_11
    return np.stack([x, y, z], axis=-1)
