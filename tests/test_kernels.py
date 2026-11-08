import numpy as np
import pytest

from src import kernels

# ---------- independent reference: build the circuit gate by gate as dense matrices ----------
H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
I2 = np.eye(2)


def P(lam):
    return np.diag([1, np.exp(1j * lam)])


def on_qubit(gate, q, n):
    """Embed a 1-qubit gate on qubit q (little-endian: qubit 0 is the rightmost Kronecker factor)."""
    out = np.array([[1.0]])
    for k in reversed(range(n)):
        out = np.kron(out, gate if k == q else I2)
    return out


def cx(c, t, n):
    dim = 2**n
    M = np.zeros((dim, dim))
    for b in range(dim):
        b2 = b ^ (1 << t) if (b >> c) & 1 else b
        M[b2, b] = 1
    return M


def dense_state(x, kind, reps, ent="linear"):
    n = len(x)
    psi = np.zeros(2**n, complex)
    psi[0] = 1
    for _ in range(reps):
        for q in range(n):
            psi = on_qubit(H, q, n) @ psi
        for q in range(n):
            psi = on_qubit(P(2 * x[q]), q, n) @ psi
        if kind == "zz":
            for i, j in kernels.entangling_pairs(n, ent):
                psi = cx(i, j, n) @ psi
                psi = on_qubit(P(2 * (np.pi - x[i]) * (np.pi - x[j])), j, n) @ psi
                psi = cx(i, j, n) @ psi
    return psi


@pytest.mark.parametrize("n", [1, 2, 3, 4])
@pytest.mark.parametrize("kind,reps,ent", [("z", 1, "linear"), ("z", 2, "linear"),
                                           ("zz", 1, "linear"), ("zz", 2, "linear"), ("zz", 2, "full")])
def test_fast_engine_matches_gate_by_gate_circuit(n, kind, reps, ent):
    rng = np.random.default_rng(n)
    X = rng.uniform(-np.pi, np.pi, (5, n))
    fast = kernels.statevectors(X, kind, reps, ent)
    for x, s in zip(X, fast):
        ref = dense_state(x, kind, reps, ent)
        assert np.allclose(s, ref, atol=1e-12)


def test_one_qubit_kernel_by_hand():
    # Z map, 1 rep: |phi(x)> = (|0> + e^{2ix}|1>)/sqrt2  =>  k(x,x') = |1 + e^{2i(x'-x)}|^2 / 4 = cos^2(x - x')
    x = np.linspace(-np.pi, np.pi, 9)[:, None]
    K = kernels.fidelity_kernel(kernels.statevectors(x, "z", 1))
    assert np.allclose(K, np.cos(x - x.T) ** 2, atol=1e-12)


@pytest.mark.parametrize("kind", ["z", "zz"])
def test_kernel_matrix_valid(kind):
    X = np.random.default_rng(0).uniform(-np.pi, np.pi, (60, 5))
    K = kernels.fidelity_kernel(kernels.statevectors(X, kind, 2))
    assert np.allclose(K, K.T)
    assert np.allclose(np.diag(K), 1)
    assert K.min() >= -1e-12 and K.max() <= 1 + 1e-12
    assert np.linalg.eigvalsh(K).min() > -1e-8


def test_states_normalised():
    S = kernels.statevectors(np.random.default_rng(1).uniform(-3, 3, (20, 6)), "zz", 2)
    assert np.allclose(np.linalg.norm(S, axis=1), 1)


def test_batching_does_not_change_states(monkeypatch):
    X = np.random.default_rng(6).uniform(-np.pi, np.pi, (37, 6))
    ref = kernels.statevectors(X, "zz", 2)
    assert np.allclose(kernels.statevectors(X, "zz", 2, batch=5), ref, atol=1e-13, rtol=0)
    monkeypatch.setattr(kernels, "MAX_BATCH_AMPLITUDES", 3 * 2**6)  # forces batches of 3 rows
    assert np.allclose(kernels.statevectors(X, "zz", 2), ref, atol=1e-13, rtol=0)  # BLAS rounding only


def test_test_by_train_matches_full_matrix():
    X = np.random.default_rng(2).uniform(-np.pi, np.pi, (30, 4))
    S = kernels.statevectors(X, "zz", 2)
    full = kernels.fidelity_kernel(S)
    assert np.allclose(kernels.fidelity_kernel(S[20:], S[:20]), full[20:, :20])


def test_reduced_density_matrices():
    # product state from the Z map: each rho_k is pure, trace 1, Hermitian
    X = np.random.default_rng(3).uniform(-np.pi, np.pi, (10, 3))
    R = kernels.reduced_density_features(kernels.statevectors(X, "z", 1))
    for k in range(3):
        re, im = R[:, 8 * k:8 * k + 4].reshape(-1, 2, 2), R[:, 8 * k + 4:8 * k + 8].reshape(-1, 2, 2)
        rho = re + 1j * im
        assert np.allclose(np.trace(rho, axis1=1, axis2=2), 1)
        assert np.allclose(rho, np.conj(np.swapaxes(rho, 1, 2)))
        assert np.allclose(np.einsum("bij,bjk->bik", rho, rho), rho)  # pure


def test_rbf_and_projected_valid():
    X = np.random.default_rng(4).normal(size=(40, 3))
    K = kernels.rbf_kernel(X, gamma=0.5)
    assert np.allclose(np.diag(K), 1) and np.linalg.eigvalsh(K).min() > -1e-8


def test_shot_noise_unbiased_and_psd():
    X = np.random.default_rng(5).uniform(-np.pi, np.pi, (40, 3))
    K = kernels.fidelity_kernel(kernels.statevectors(X, "zz", 2))
    rng = np.random.default_rng(0)
    est = np.mean([kernels.shot_noisy_kernel(K, 1000, rng, enforce_psd=False) for _ in range(50)], axis=0)
    assert np.abs(est - K).max() < 0.02
    psd = kernels.shot_noisy_kernel(K, 100, rng)
    assert np.linalg.eigvalsh(psd).min() > -1e-8
