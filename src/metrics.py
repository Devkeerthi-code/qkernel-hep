"""Research metrics: geometric difference, model complexity, kernel concentration, AUC statistics."""
from __future__ import annotations

import numpy as np
from scipy import stats
from sklearn.metrics import roc_auc_score


def normalise_trace(K: np.ndarray) -> np.ndarray:
    """Scale K so that trace(K) = N, as in Huang et al. (2021)."""
    return K * (K.shape[0] / np.trace(K))


def _eigh_psd(K: np.ndarray):
    w, V = np.linalg.eigh(0.5 * (K + K.T))
    return np.clip(w, 0.0, None), V


def sqrtm_psd(K: np.ndarray) -> np.ndarray:
    w, V = _eigh_psd(K)
    return (V * np.sqrt(w)) @ V.T


def geometric_difference(K_C: np.ndarray, K_Q: np.ndarray, lam: float = 0.0,
                         eig_floor: float = 1e-12) -> float:
    """Geometric difference g(K_C || K_Q) of Huang et al. (2021), Nat. Commun. 12, 2631.

    lam = 0 :  g = sqrt( || sqrt(K_Q) K_C^{-1} sqrt(K_Q) ||_inf )
    lam > 0 :  g = sqrt( || sqrt(K_Q) sqrt(K_C) (K_C + lam I)^{-2} sqrt(K_C) sqrt(K_Q) ||_inf )
    Both kernels are first normalised to trace N. The middle factor is built from one
    eigendecomposition of K_C:  V diag(e / (e + lam)^2) V^T, which reduces to K_C^{-1}
    when lam = 0 (eigenvalues below eig_floor * max are floored to keep it finite).
    """
    K_C = normalise_trace(K_C)
    K_Q = normalise_trace(K_Q)
    e, V = _eigh_psd(K_C)
    if lam == 0.0:
        e = np.maximum(e, eig_floor * e.max())
        middle = (V / e) @ V.T
    else:
        middle = (V * (e / (e + lam) ** 2)) @ V.T
    sQ = sqrtm_psd(K_Q)
    M = sQ @ middle @ sQ
    top = np.linalg.eigvalsh(0.5 * (M + M.T))[-1]
    return float(np.sqrt(max(top, 0.0)))


def model_complexity(K: np.ndarray, y: np.ndarray, lam: float = 1e-3) -> float:
    """Label-dependent complexity: squared RKHS norm of the kernel-ridge solution, divided by N.

    alpha = (K + lam I)^{-1} y,  s = alpha^T K alpha / N,  with K trace-normalised and y in {-1, +1}.
    Small s means the labels are 'simple' for this kernel. This is a ridge-regularised stand-in
    for s_K(N) = y^T K^{-1} y in Huang et al.; it is not their exact regularised expression.
    """
    K = normalise_trace(K)
    y = np.where(np.asarray(y) > 0, 1.0, -1.0)
    alpha = np.linalg.solve(K + lam * np.eye(len(y)), y)
    return float(alpha @ K @ alpha / len(y))


def concentration(K: np.ndarray) -> dict:
    """Mean and variance of the off-diagonal entries of a square kernel matrix."""
    off = K[~np.eye(K.shape[0], dtype=bool)]
    return {"offdiag_mean": float(off.mean()), "offdiag_var": float(off.var())}


def effective_dimension(K: np.ndarray) -> float:
    """Participation ratio of the eigenvalue spectrum: (sum w)^2 / sum w^2. ~1 = rank-one, N = identity."""
    w, _ = _eigh_psd(K)
    return float(w.sum() ** 2 / (w**2).sum())


def bootstrap_auc_ci(y: np.ndarray, score: np.ndarray, n_boot: int = 1000,
                     alpha: float = 0.05, seed: int = 0) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    y, score = np.asarray(y), np.asarray(score)
    vals = []
    for _ in range(n_boot):
        idx = rng.integers(0, len(y), len(y))
        if len(np.unique(y[idx])) < 2:
            continue
        vals.append(roc_auc_score(y[idx], score[idx]))
    return float(np.quantile(vals, alpha / 2)), float(np.quantile(vals, 1 - alpha / 2))


def spearman_with_ci(x, y, n_boot: int = 2000, alpha: float = 0.05, seed: int = 0) -> dict:
    """Spearman rank correlation with a percentile bootstrap CI over configurations."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    rho, p = stats.spearmanr(x, y)
    rng = np.random.default_rng(seed)
    boots = []
    for _ in range(n_boot):
        idx = rng.integers(0, len(x), len(x))
        r = stats.spearmanr(x[idx], y[idx])[0]
        if np.isfinite(r):
            boots.append(r)
    lo, hi = np.quantile(boots, [alpha / 2, 1 - alpha / 2])
    return {"rho": float(rho), "p": float(p), "ci_low": float(lo), "ci_high": float(hi), "n": int(len(x))}
