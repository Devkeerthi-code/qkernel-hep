"""Quantum and classical kernel matrices.

The quantum feature maps are simulated exactly with a small NumPy statevector
engine instead of a circuit library, so every step is visible:

* ZFeatureMap   (Qiskit convention):  per repetition  H^n  then  P(2 x_i) on qubit i
* ZZFeatureMap  (Qiskit convention):  as above, plus for each entangled pair (i, j)
                                      CX(i,j) . P(2 (pi - x_i)(pi - x_j)) on j . CX(i,j)

Every gate after the Hadamards is diagonal in the computational basis, so one
repetition is "Walsh-Hadamard transform, then multiply by a phase vector".
For a basis state with bits b:
    phase(b) = sum_i 2 x_i b_i + sum_(i,j) 2 (pi - x_i)(pi - x_j) (b_i XOR b_j)
(the CX . P . CX block puts the phase on b_i XOR b_j). Qubit i is bit i of the
basis index (little-endian, as in Qiskit); fidelities do not depend on this choice.
"""
from __future__ import annotations

import numpy as np

FEATURE_MAPS = ("z", "zz")


def entangling_pairs(n: int, entanglement: str = "linear") -> list[tuple[int, int]]:
    if entanglement == "linear":
        return [(i, i + 1) for i in range(n - 1)]
    if entanglement == "circular":
        return [(i, i + 1) for i in range(n - 1)] + ([(n - 1, 0)] if n > 2 else [])
    if entanglement == "full":
        return [(i, j) for i in range(n) for j in range(i + 1, n)]
    raise ValueError(f"unknown entanglement {entanglement!r}")


def _bits(n: int) -> np.ndarray:
    """(2^n, n) array: bits[k, i] = value of qubit i in basis state k."""
    return (np.arange(2**n)[:, None] >> np.arange(n)[None, :]) & 1


def walsh_hadamard(psi: np.ndarray) -> np.ndarray:
    """Apply H on every qubit to a batch of states, shape (B, 2^n). Unnormalised (no 1/sqrt)."""
    B, dim = psi.shape
    out = psi
    h = 1
    while h < dim:
        out = out.reshape(B, dim // (2 * h), 2, h)
        a, b = out[:, :, 0, :], out[:, :, 1, :]
        out = np.stack((a + b, a - b), axis=2).reshape(B, dim)
        h *= 2
    return out


def phase_vectors(X: np.ndarray, kind: str, entanglement: str = "linear") -> np.ndarray:
    """Diagonal phase (radians) applied by one repetition, shape (B, 2^n)."""
    X = np.asarray(X, dtype=float)
    _, n = X.shape
    bits = _bits(n).astype(float)
    phase = 2.0 * X @ bits.T
    if kind == "zz":
        for i, j in entangling_pairs(n, entanglement):
            coeff = 2.0 * (np.pi - X[:, i]) * (np.pi - X[:, j])
            parity = np.logical_xor(bits[:, i], bits[:, j]).astype(float)
            phase += coeff[:, None] * parity[None, :]
    elif kind != "z":
        raise ValueError(f"unknown feature map {kind!r}")
    return phase


MAX_BATCH_AMPLITUDES = 2**22  # ~64 MB per complex temporary; keeps 12-14 qubit runs within RAM


def statevectors(X: np.ndarray, kind: str = "zz", reps: int = 2,
                 entanglement: str = "linear", batch: int = 4096) -> np.ndarray:
    """Exact states |phi(x)> = U(x)|0...0> for every row of X. Returns (B, 2^n) complex.

    Rows are processed in batches of at most `batch`, further capped so a batch holds at most
    MAX_BATCH_AMPLITUDES amplitudes (no effect for n <= 10). Batching changes results only by
    floating-point rounding (~1e-15, from BLAS using different kernels for different shapes).
    """
    X = np.asarray(X, dtype=float)
    B, n = X.shape
    dim = 2**n
    batch = max(1, min(batch, MAX_BATCH_AMPLITUDES // dim))
    out = np.empty((B, dim), dtype=complex)
    for s in range(0, B, batch):
        D = np.exp(1j * phase_vectors(X[s:s + batch], kind, entanglement))
        psi = np.full(D.shape, 1 / np.sqrt(dim), dtype=complex) * D  # first H^n on |0> is uniform
        for _ in range(reps - 1):
            psi = walsh_hadamard(psi) / np.sqrt(dim) * D
        out[s:s + batch] = psi
    return out


def fidelity_kernel(S1: np.ndarray, S2: np.ndarray | None = None) -> np.ndarray:
    """k(x, x') = |<phi(x)|phi(x')>|^2 from precomputed statevectors."""
    S2 = S1 if S2 is None else S2
    K = np.abs(S1.conj() @ S2.T) ** 2
    if S2 is S1:
        K = 0.5 * (K + K.T)
        np.fill_diagonal(K, 1.0)
    return K


def reduced_density_features(S: np.ndarray) -> np.ndarray:
    """Flattened single-qubit reduced density matrices rho_k(x) for each qubit, real-valued.

    Returns (B, 8n): real and imaginary parts of the four entries of each rho_k.
    """
    B, dim = S.shape
    n = int(np.log2(dim))
    T = S.reshape((B,) + (2,) * n)  # C order: axis 1 is the highest bit (qubit n-1)
    feats = []
    for k in range(n):
        axis = 1 + (n - 1 - k)
        Tk = np.moveaxis(T, axis, 1).reshape(B, 2, -1)
        rho = np.einsum("bia,bja->bij", Tk, Tk.conj())
        feats.append(np.concatenate([rho.real.reshape(B, 4), rho.imag.reshape(B, 4)], axis=1))
    return np.concatenate(feats, axis=1)


def projected_kernel(R1: np.ndarray, R2: np.ndarray | None = None, gamma: float = 1.0) -> np.ndarray:
    """Projected quantum kernel (Huang et al. 2021): exp(-gamma sum_k ||rho_k(x) - rho_k(x')||_F^2)."""
    return rbf_kernel(R1, R2, gamma)


def sq_dists(A: np.ndarray, B: np.ndarray | None = None) -> np.ndarray:
    B = A if B is None else B
    d = (A**2).sum(1)[:, None] + (B**2).sum(1)[None, :] - 2 * A @ B.T
    return np.maximum(d, 0.0)


def rbf_kernel(X1: np.ndarray, X2: np.ndarray | None = None, gamma: float = 1.0) -> np.ndarray:
    same = X2 is None
    K = np.exp(-gamma * sq_dists(X1, X2))
    if same:
        K = 0.5 * (K + K.T)
        np.fill_diagonal(K, 1.0)
    return K


def shot_noisy_kernel(K: np.ndarray, shots: int, rng: np.random.Generator,
                      depolarizing: float = 0.0, n_qubits: int | None = None,
                      symmetric: bool = True, enforce_psd: bool = True) -> np.ndarray:
    """Simulate estimating a fidelity kernel with the compute-uncompute circuit.

    The circuit U(x')^dagger U(x)|0> returns all-zeros with probability K(x, x'), so a
    finite-shot estimate is Binomial(shots, p) / shots. Optional global depolarizing
    noise of total strength p_tot mixes in the maximally mixed state:
        p = (1 - p_tot) K + p_tot / 2^n
    This is a simple analytic noise model, not a device-calibrated one.
    """
    p = K
    if depolarizing > 0:
        if n_qubits is None:
            raise ValueError("n_qubits needed for depolarizing noise")
        p = (1 - depolarizing) * K + depolarizing / 2**n_qubits
    p = np.clip(p, 0.0, 1.0)
    est = rng.binomial(shots, p) / shots
    if symmetric:
        est = np.triu(est, 1)
        est = est + est.T
        np.fill_diagonal(est, 1.0)  # diagonal is known exactly, never measured
        if enforce_psd:
            w, V = np.linalg.eigh(est)
            est = (V * np.clip(w, 0, None)) @ V.T
    return est
