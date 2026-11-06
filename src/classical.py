"""Tuned classical baselines and the precomputed-kernel (quantum) SVM.

Every model is tuned by stratified 5-fold cross-validation on the training events only,
scored by ROC-AUC, with grids of similar size, so the comparison is about the kernel.
"""
from __future__ import annotations

import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.svm import SVC

try:  # XGBoost is used when installed; sklearn's histogram GBDT is the same model family
    from xgboost import XGBClassifier
except ImportError:  # pragma: no cover
    XGBClassifier = None

C_GRID = [0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0]
GAMMA_GRID = [0.003, 0.01, 0.03, 0.1, 0.3, 1.0]


def _cv(seed: int) -> StratifiedKFold:
    return StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)


def _search(model, grid, X, y, seed):
    gs = GridSearchCV(model, grid, scoring="roc_auc", cv=_cv(seed), n_jobs=1, refit=True)
    gs.fit(X, y)
    return gs


def logistic(X, y, Xt, yt, seed):
    gs = _search(LogisticRegression(max_iter=5000), {"C": [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]}, X, y, seed)
    return {"auc": roc_auc_score(yt, gs.decision_function(Xt)), "cv_auc": gs.best_score_, "params": gs.best_params_}


def rbf_svm(X, y, Xt, yt, seed):
    gs = _search(SVC(kernel="rbf"), {"C": C_GRID, "gamma": GAMMA_GRID}, X, y, seed)
    return {"auc": roc_auc_score(yt, gs.decision_function(Xt)), "cv_auc": gs.best_score_, "params": gs.best_params_}


def boosted_trees(X, y, Xt, yt, seed):
    if XGBClassifier is not None:
        model = XGBClassifier(random_state=seed, n_jobs=1, verbosity=0)
        grid = {"max_depth": [2, 4, 6], "learning_rate": [0.03, 0.1, 0.3], "n_estimators": [100, 300]}
        name = "xgboost"
    else:
        model = HistGradientBoostingClassifier(random_state=seed)
        grid = {"max_depth": [2, 4, 6], "learning_rate": [0.03, 0.1, 0.3], "max_iter": [100, 300]}
        name = "hist_gbdt"
    gs = _search(model, grid, X, y, seed)
    return {"auc": roc_auc_score(yt, gs.predict_proba(Xt)[:, 1]), "cv_auc": gs.best_score_,
            "params": gs.best_params_, "impl": name}


def precomputed_svm(K_train, y, K_test, yt, seed):
    """SVC on a precomputed kernel. GridSearchCV slices K_train[train_fold][:, train_fold] correctly
    for kernel='precomputed' (scikit-learn's pairwise tag)."""
    gs = _search(SVC(kernel="precomputed"), {"C": C_GRID}, K_train, y, seed)
    return {"auc": roc_auc_score(yt, gs.decision_function(K_test)), "cv_auc": gs.best_score_,
            "params": gs.best_params_, "n_support": int(gs.best_estimator_.n_support_.sum())}


def run_baselines(X, y, Xt, yt, seed) -> dict:
    return {"logreg": logistic(X, y, Xt, yt, seed),
            "rbf_svm": rbf_svm(X, y, Xt, yt, seed),
            "gbdt": boosted_trees(X, y, Xt, yt, seed)}
