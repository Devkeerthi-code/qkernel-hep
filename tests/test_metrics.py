import numpy as np

from src import kernels, metrics


def _K(seed=0, n=50):
    X = np.random.default_rng(seed).uniform(-np.pi, np.pi, (n, 4))
    return X, kernels.fidelity_kernel(kernels.statevectors(X, "zz", 2))


def test_geometric_difference_self_is_one():
    X, KQ = _K()
    KC = kernels.rbf_kernel(X, gamma=0.3)
    assert abs(metrics.geometric_difference(KC, KC) - 1) < 1e-6
    assert abs(metrics.geometric_difference(KQ, KQ) - 1) < 1e-6


def test_geometric_difference_at_least_one():
    X, KQ = _K(1)
    KC = kernels.rbf_kernel(X, gamma=1.0)
    assert metrics.geometric_difference(KC, KQ) >= 1 - 1e-8


def test_regularised_tends_to_unregularised():
    X, KQ = _K(2, 30)
    KC = kernels.rbf_kernel(X, gamma=2.0)  # well conditioned
    g0 = metrics.geometric_difference(KC, KQ, 0.0)
    assert abs(metrics.geometric_difference(KC, KQ, 1e-9) - g0) / g0 < 1e-4
    # regularisation can only shrink g
    assert metrics.geometric_difference(KC, KQ, 0.1) <= g0 + 1e-9


def test_scale_invariance():
    X, KQ = _K(3)
    KC = kernels.rbf_kernel(X, gamma=0.5)
    assert np.isclose(metrics.geometric_difference(3 * KC, 0.2 * KQ, 0.01),
                      metrics.geometric_difference(KC, KQ, 0.01))


def test_concentration_identity():
    c = metrics.concentration(np.eye(10))
    assert c["offdiag_mean"] == 0 and c["offdiag_var"] == 0


def test_effective_dimension_limits():
    assert np.isclose(metrics.effective_dimension(np.eye(20)), 20)
    assert np.isclose(metrics.effective_dimension(np.ones((20, 20))), 1)


def test_spearman_ci_contains_rho():
    rng = np.random.default_rng(0)
    x = rng.normal(size=100)
    r = metrics.spearman_with_ci(x, x + rng.normal(size=100))
    assert r["ci_low"] <= r["rho"] <= r["ci_high"] and r["rho"] > 0.4
