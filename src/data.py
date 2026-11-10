"""Loading, sampling, splitting and preprocessing of the ATLAS Higgs ML Challenge 2014 data.

Every fitted step (StandardScaler, PCA or boosted-tree feature ranking, angle rescaling) is learned
from training events only.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

MISSING = -999.0
NON_FEATURES = {"EventId", "Weight", "Label", "KaggleSet", "KaggleWeight", "y"}


def load(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["y"] = (df["Label"] == "s").astype(int)
    return df


def feature_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if c.startswith(("PRI_", "DER_"))]


def always_defined(df: pd.DataFrame) -> list[str]:
    """Features that never take the -999 placeholder, found from the data itself."""
    return [c for c in feature_columns(df) if not (df[c] == MISSING).any()]


def wrap_angle(a: np.ndarray) -> np.ndarray:
    """Map any angle to (-pi, pi]."""
    return np.angle(np.exp(1j * np.asarray(a)))


def add_angle_differences(df: pd.DataFrame) -> pd.DataFrame:
    """|Delta phi| between the always-present objects (tau, lepton, MET). Rotation invariant."""
    out = df.copy()
    for a, b in [("tau", "lep"), ("tau", "met"), ("lep", "met")]:
        out[f"DPHI_{a}_{b}"] = np.abs(wrap_angle(df[f"PRI_{a}_phi"] - df[f"PRI_{b}_phi"]))
    return out


def select_features(df: pd.DataFrame, angle_diffs: bool = True, mmc_flag: bool = False) -> tuple[pd.DataFrame, list[str]]:
    """Always-defined features, raw *_phi dropped, optional |Delta phi| and MMC-failure flag."""
    cols = [c for c in always_defined(df) if not c.endswith("_phi")]
    if angle_diffs:
        df = add_angle_differences(df)
        cols += ["DPHI_tau_lep", "DPHI_tau_met", "DPHI_lep_met"]
    if mmc_flag:
        df = df.copy()
        df["MMC_defined"] = (df["DER_mass_MMC"] != MISSING).astype(float)
        cols.append("MMC_defined")
    return df, cols


def balanced_split(df: pd.DataFrame, n_train: int, n_test: int, seed: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Disjoint, class-balanced train and test samples (stratified by construction)."""
    rng = np.random.default_rng(seed)
    tr, te = [], []
    for label in (0, 1):
        idx = df.index[df["y"] == label].to_numpy()
        pick = rng.choice(idx, size=n_train // 2 + n_test // 2, replace=False)
        tr.append(pick[: n_train // 2])
        te.append(pick[n_train // 2:])
    train = df.loc[rng.permutation(np.concatenate(tr))]
    test = df.loc[rng.permutation(np.concatenate(te))]
    assert not set(train["EventId"]) & set(test["EventId"]), "EventId leaked across splits"
    return train, test


@dataclass
class Preprocessor:
    """StandardScaler -> PCA(n) -> per-component linear map of the train range onto [-pi, pi]."""
    n_components: int
    seed: int = 0
    scaler: StandardScaler = field(default=None, init=False)
    pca: PCA = field(default=None, init=False)
    lo: np.ndarray = field(default=None, init=False)
    hi: np.ndarray = field(default=None, init=False)

    def fit(self, X_train: np.ndarray) -> "Preprocessor":
        self.scaler = StandardScaler().fit(X_train)
        Z = self.scaler.transform(X_train)
        self.pca = PCA(n_components=self.n_components, random_state=self.seed).fit(Z)
        P = self.pca.transform(Z)
        self.lo, self.hi = P.min(0), P.max(0)
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """Angles in [-pi, pi] for training data; test values may fall slightly outside (not clipped)."""
        P = self.pca.transform(self.scaler.transform(X))
        return -np.pi + 2 * np.pi * (P - self.lo) / (self.hi - self.lo)


@dataclass
class ImportanceSelector:
    """StandardScaler -> keep the n features with the largest boosted-tree importance -> per-feature
    linear map of the train range onto [-pi, pi] (the same angle map as Preprocessor).

    Importance is XGBoost's total gain from a fixed, untuned model (300 trees, depth 3, learning rate 0.1)
    fitted on the training events only; without XGBoost, sklearn's GradientBoostingClassifier impurity
    importance is used. Ties are broken by column order. A robustness alternative to PCA.
    """
    n_components: int
    seed: int = 0
    scaler: StandardScaler = field(default=None, init=False)
    importances: np.ndarray = field(default=None, init=False)
    idx: np.ndarray = field(default=None, init=False)
    impl: str = field(default=None, init=False)
    lo: np.ndarray = field(default=None, init=False)
    hi: np.ndarray = field(default=None, init=False)

    def fit(self, X_train: np.ndarray, y_train: np.ndarray) -> "ImportanceSelector":
        if self.n_components > X_train.shape[1]:
            raise ValueError(f"asked for {self.n_components} features, only {X_train.shape[1]} available")
        self.scaler = StandardScaler().fit(X_train)
        Z = self.scaler.transform(X_train)
        try:
            from xgboost import XGBClassifier
            model = XGBClassifier(n_estimators=300, max_depth=3, learning_rate=0.1, importance_type="total_gain",
                                  random_state=self.seed, n_jobs=1, verbosity=0)
            self.impl = "xgboost_total_gain"
        except ImportError:  # pragma: no cover
            from sklearn.ensemble import GradientBoostingClassifier
            model = GradientBoostingClassifier(n_estimators=300, max_depth=3, learning_rate=0.1, random_state=self.seed)
            self.impl = "sklearn_gbdt_impurity"
        model.fit(Z, y_train)
        self.importances = np.asarray(model.feature_importances_, float)
        self.idx = np.argsort(-self.importances, kind="stable")[: self.n_components]
        S = Z[:, self.idx]
        self.lo, self.hi = S.min(0), S.max(0)
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """Angles in [-pi, pi] for training data; test values may fall slightly outside (not clipped)."""
        S = self.scaler.transform(X)[:, self.idx]
        return -np.pi + 2 * np.pi * (S - self.lo) / (self.hi - self.lo)


REDUCTIONS = ("pca", "gbdt_importance")


def prepare(df: pd.DataFrame, cols: list[str], n_qubits: int, n_train: int, n_test: int, seed: int,
            reduction: str = "pca") -> dict:
    """One seeded resample: returns train/test angle arrays (before bandwidth) and labels.

    reduction="pca": StandardScaler -> PCA(n_qubits) (the default used by every main experiment).
    reduction="gbdt_importance": the n_qubits features with the largest boosted-tree importance on the
    training events (ImportanceSelector).
    """
    if reduction not in REDUCTIONS:
        raise ValueError(f"reduction must be one of {REDUCTIONS}, got {reduction!r}")
    train, test = balanced_split(df, n_train, n_test, seed)
    X_tr, X_te = train[cols].to_numpy(float), test[cols].to_numpy(float)
    out = {"y_train": train["y"].to_numpy(), "y_test": test["y"].to_numpy(),
           "train_ids": train["EventId"].to_numpy(), "test_ids": test["EventId"].to_numpy()}
    if reduction == "pca":
        pre = Preprocessor(n_qubits, seed).fit(X_tr)
        out["explained_variance"] = float(pre.pca.explained_variance_ratio_.sum())
    else:
        pre = ImportanceSelector(n_qubits, seed).fit(X_tr, out["y_train"])
        out["explained_variance"] = None
        out["selected_features"] = [cols[i] for i in pre.idx]
    out.update({"X_train": pre.transform(X_tr), "X_test": pre.transform(X_te), "preprocessor": pre})
    return out


def synthetic_atlas_like(n_events: int = 20000, seed: int = 0) -> pd.DataFrame:
    """Small fake dataset with the real file's column conventions, for tests only."""
    rng = np.random.default_rng(seed)
    y = rng.integers(0, 2, n_events)
    df = pd.DataFrame({"EventId": np.arange(100000, 100000 + n_events)})
    for i in range(8):
        df[f"DER_f{i}"] = rng.normal(0.6 * y * (i % 3 == 0), 1.0) + (i == 1) * 0.4 * y * rng.normal(size=n_events)
    for obj in ("tau", "lep", "met"):
        df[f"PRI_{obj}_phi"] = rng.uniform(-np.pi, np.pi, n_events)
    df["PRI_jet_leading_pt"] = np.where(rng.random(n_events) < 0.4, MISSING, rng.exponential(50, n_events))
    df["DER_mass_MMC"] = np.where(rng.random(n_events) < 0.15, MISSING, rng.normal(120 + 5 * y, 20))
    df["Weight"] = 1.0
    df["Label"] = np.where(y == 1, "s", "b")
    df["y"] = y
    return df
