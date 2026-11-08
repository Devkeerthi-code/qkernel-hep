import numpy as np

from src import hardware, kernels


def test_bloch_roundtrip_matches_rdm_features():
    X = np.random.default_rng(0).uniform(-np.pi, np.pi, (15, 4))
    S = kernels.statevectors(X, "zz", 2)
    F = kernels.reduced_density_features(S)
    assert np.allclose(hardware.bloch_to_rdm_features(hardware.exact_bloch(S)), F, atol=1e-12)


def test_pauli_expectations_little_endian():
    # qubit 0 always 1, qubit 1 always 0 -> bitstring "01" (qubit 1 left, qubit 0 right)
    assert np.allclose(hardware.pauli_expectations({"01": 100}, 2), [-1, 1])
    assert np.allclose(hardware.pauli_expectations({"00": 50, "11": 50}, 2), [0, 0])


def test_fidelity_and_assembly():
    assert hardware.fidelity_from_counts({"000": 30, "101": 70}, 3) == 0.3
    K = hardware.assemble_train_kernel(np.array([0.5, 0.2, 0.9]), [(0, 1), (0, 2), (1, 2)], 3)
    assert np.allclose(K, K.T) and np.linalg.eigvalsh(K).min() > -1e-10
