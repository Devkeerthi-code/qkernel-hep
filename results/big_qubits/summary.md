# big_qubits: mean ± std over seeds (std is the sample std, ddof=1)

## n=12 qubits, N=500, zz map, reps=2, bandwidth=0.1 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.754 ± 0.005 |
| Projected QSVM | 0.743 ± 0.010 |
| Logistic regression | 0.780 ± 0.028 |
| RBF SVM | 0.817 ± 0.020 |
| Boosted trees | 0.801 ± 0.013 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 35.566 ± 58.363 |
| g, lambda=0.01 | 5.073 ± 2.690 |
| g(K_RBF || K_PQK), lambda=0 | 36.743 ± 68.984 |
| g_pqk, lambda=0.01 | 6.393 ± 2.580 |
| K_Q off-diagonal mean | 0.045 ± 0.016 |
| K_Q off-diagonal variance | 7.60e-03 ± 2.9e-03 |
| K_PQK off-diagonal variance | 0.013 ± 0.011 |
| K_RBF off-diagonal variance | 0.020 ± 0.012 |
| K_Q effective dimension | 94.486 ± 32.293 |
| AUC gap fidelity QSVM - best classical | -0.066 ± 0.020 |
| AUC gap projected QSVM - best classical | -0.078 ± 0.025 |

boosted-trees implementation: xgboost

## n=12 qubits, N=500, zz map, reps=2, bandwidth=1.0 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.517 ± 0.025 |
| Projected QSVM | 0.530 ± 0.018 |
| Logistic regression | 0.780 ± 0.028 |
| RBF SVM | 0.817 ± 0.020 |
| Boosted trees | 0.801 ± 0.013 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 118.637 ± 159.940 |
| g, lambda=0.01 | 5.014 ± 0.018 |
| g(K_RBF || K_PQK), lambda=0 | 90.676 ± 111.559 |
| g_pqk, lambda=0.01 | 9.041 ± 1.223 |
| K_Q off-diagonal mean | 3.68e-04 ± 5.6e-06 |
| K_Q off-diagonal variance | 8.04e-07 ± 3.9e-08 |
| K_PQK off-diagonal variance | 7.00e-03 ± 3.8e-03 |
| K_RBF off-diagonal variance | 0.020 ± 0.012 |
| K_Q effective dimension | 499.766 ± 0.011 |
| AUC gap fidelity QSVM - best classical | -0.303 ± 0.019 |
| AUC gap projected QSVM - best classical | -0.291 ± 0.020 |

boosted-trees implementation: xgboost

## n=14 qubits, N=500, zz map, reps=2, bandwidth=0.1 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.751 ± 0.003 |
| Projected QSVM | 0.746 ± 0.013 |
| Logistic regression | 0.787 ± 0.025 |
| RBF SVM | 0.819 ± 0.013 |
| Boosted trees | 0.802 ± 0.022 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 279.226 ± 398.140 |
| g, lambda=0.01 | 7.307 ± 2.847 |
| g(K_RBF || K_PQK), lambda=0 | 86.478 ± 110.747 |
| g_pqk, lambda=0.01 | 7.084 ± 3.324 |
| K_Q off-diagonal mean | 0.036 ± 0.015 |
| K_Q off-diagonal variance | 5.69e-03 ± 2.6e-03 |
| K_PQK off-diagonal variance | 0.017 ± 0.011 |
| K_RBF off-diagonal variance | 0.020 ± 0.011 |
| K_Q effective dimension | 124.720 ± 48.256 |
| AUC gap fidelity QSVM - best classical | -0.071 ± 0.017 |
| AUC gap projected QSVM - best classical | -0.075 ± 0.024 |

boosted-trees implementation: xgboost

## n=14 qubits, N=500, zz map, reps=2, bandwidth=1.0 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.523 ± 0.018 |
| Projected QSVM | 0.523 ± 0.011 |
| Logistic regression | 0.787 ± 0.025 |
| RBF SVM | 0.819 ± 0.013 |
| Boosted trees | 0.802 ± 0.022 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 814.313 ± 1082.126 |
| g, lambda=0.01 | 5.002 ± 0.002 |
| g(K_RBF || K_PQK), lambda=0 | 451.032 ± 600.032 |
| g_pqk, lambda=0.01 | 7.999 ± 1.985 |
| K_Q off-diagonal mean | 9.41e-05 ± 2.8e-06 |
| K_Q off-diagonal variance | 7.38e-08 ± 3.9e-09 |
| K_PQK off-diagonal variance | 4.74e-03 ± 3.1e-03 |
| K_RBF off-diagonal variance | 0.020 ± 0.011 |
| K_Q effective dimension | 499.979 ± 0.001 |
| AUC gap fidelity QSVM - best classical | -0.298 ± 0.019 |
| AUC gap projected QSVM - best classical | -0.299 ± 0.013 |

boosted-trees implementation: xgboost
