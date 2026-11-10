import json

import numpy as np

from src import classical, data, kernels, run


def _df():
    return data.synthetic_atlas_like(6000, seed=0)


def test_always_defined_excludes_missing():
    cols = data.always_defined(_df())
    assert "PRI_jet_leading_pt" not in cols and "DER_mass_MMC" not in cols
    assert "DER_f0" in cols


def test_select_features_drops_raw_phi_and_adds_dphi():
    df, cols = data.select_features(_df())
    assert not any(c.endswith("_phi") for c in cols)
    assert "DPHI_tau_lep" in cols
    assert df["DPHI_tau_lep"].between(0, np.pi).all()


def test_wrap_angle():
    assert np.allclose(data.wrap_angle([3 * np.pi / 2, -3 * np.pi / 2, 0.5]), [-np.pi / 2, np.pi / 2, 0.5])


def test_split_disjoint_balanced_seeded():
    df, _ = data.select_features(_df())
    tr, te = data.balanced_split(df, 200, 400, seed=3)
    assert not set(tr.EventId) & set(te.EventId)
    assert tr.y.mean() == 0.5 and te.y.mean() == 0.5
    tr2, te2 = data.balanced_split(df, 200, 400, seed=3)
    assert (tr.EventId.values == tr2.EventId.values).all()


def test_preprocessor_fitted_on_train_only():
    df, cols = data.select_features(_df())
    d = data.prepare(df, cols, 4, 200, 400, seed=1)
    pre = d["preprocessor"]
    train_rows = df.set_index("EventId").loc[d["train_ids"], cols].to_numpy(float)
    assert np.allclose(pre.scaler.mean_, train_rows.mean(0))  # scaler saw train only
    assert np.allclose(d["X_train"].min(0), -np.pi) and np.allclose(d["X_train"].max(0), np.pi)
    assert d["X_train"].shape == (200, 4) and d["X_test"].shape == (400, 4)


def test_importance_selector_fitted_on_train_only():
    df, cols = data.select_features(_df())
    d = data.prepare(df, cols, 3, 300, 400, seed=2, reduction="gbdt_importance")
    pre = d["preprocessor"]
    train, test = data.balanced_split(df, 300, 400, seed=2)
    # refitting on the same training events with different test events gives the same selection and scaling
    other = data.ImportanceSelector(3, seed=2).fit(train[cols].to_numpy(float), train["y"].to_numpy())
    assert list(other.idx) == list(pre.idx)
    assert np.allclose(other.transform(test[cols].to_numpy(float)), d["X_test"])
    assert np.allclose(pre.scaler.mean_, train[cols].to_numpy(float).mean(0))
    # the synthetic signal lives in DER_f0, DER_f3, DER_f6 (and DER_f1 via its variance): f0 must be picked
    assert "DER_f0" in d["selected_features"] and len(d["selected_features"]) == 3
    assert np.allclose(d["X_train"].min(0), -np.pi) and np.allclose(d["X_train"].max(0), np.pi)
    assert d["X_train"].shape == (300, 3) and d["X_test"].shape == (400, 3) and d["explained_variance"] is None


def test_prepare_rejects_unknown_reduction():
    import pytest
    df, cols = data.select_features(_df())
    with pytest.raises(ValueError):
        data.prepare(df, cols, 3, 100, 100, seed=0, reduction="lda")


def test_precomputed_rbf_equals_builtin_rbf():
    from sklearn.metrics import roc_auc_score
    from sklearn.svm import SVC
    rng = np.random.default_rng(0)
    X, Xt = rng.normal(size=(150, 3)), rng.normal(size=(100, 3))
    y, yt = (X[:, 0] + 0.5 * rng.normal(size=150) > 0).astype(int), (Xt[:, 0] > 0).astype(int)
    a = SVC(kernel="rbf", gamma=0.4, C=3).fit(X, y).decision_function(Xt)
    b = SVC(kernel="precomputed", C=3).fit(kernels.rbf_kernel(X, gamma=0.4), y).decision_function(
        kernels.rbf_kernel(Xt, X, gamma=0.4))
    assert np.allclose(a, b, atol=1e-6)
    assert roc_auc_score(yt, a) == roc_auc_score(yt, b)


def _cfg(name):
    return {"name": name, "n_train": [100], "n_test": 200, "seeds": [0], "qubits": [2],
            "feature_maps": [{"kind": "zz", "reps": 2}], "bandwidths": [0.5], "projected": True}


def test_run_is_reproducible_and_resumable(tmp_path):
    df = _df()
    p1 = run.run(_cfg("a"), str(tmp_path), df=df, verbose=False)
    p2 = run.run(_cfg("b"), str(tmp_path), df=df, verbose=False)
    r1, r2 = json.loads(p1.read_text().splitlines()[0]), json.loads(p2.read_text().splitlines()[0])
    for k in ["qsvm_auc", "rbf_auc", "gbdt_auc", "logreg_auc", "g", "q_offdiag_var", "pqk_auc"]:
        assert r1[k] == r2[k], k
    run.run(_cfg("a"), str(tmp_path), df=df, verbose=False)  # resume: nothing new appended
    assert len(p1.read_text().splitlines()) == 1
    meta = json.loads((tmp_path / "a" / "meta.json").read_text())
    assert "versions" in meta and "config" in meta
