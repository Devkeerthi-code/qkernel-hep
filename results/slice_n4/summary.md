# slice_n4: mean ± std over seeds (std is the sample std, ddof=1)

## n=4 qubits, N=500, zz map, reps=2, bandwidth=1.0 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.519 ± 0.027 |
| Projected QSVM | 0.513 ± 0.025 |
| Logistic regression | 0.760 ± 0.015 |
| RBF SVM | 0.787 ± 0.013 |
| Boosted trees | 0.784 ± 0.014 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 61863.868 ± 56808.443 |
| g, lambda=0.01 | 9.442 ± 1.780 |
| g(K_RBF || K_PQK), lambda=0 | 63550.831 ± 63903.189 |
| g_pqk, lambda=0.01 | 9.308 ± 2.400 |
| K_Q off-diagonal mean | 0.078 ± 0.001 |
| K_Q off-diagonal variance | 6.94e-03 ± 2.5e-04 |
| K_PQK off-diagonal variance | 7.10e-03 ± 8.7e-04 |
| K_RBF off-diagonal variance | 0.050 ± 0.017 |
| K_Q effective dimension | 66.550 ± 1.923 |
| AUC gap fidelity QSVM - best classical | -0.269 ± 0.029 |
| AUC gap projected QSVM - best classical | -0.275 ± 0.035 |

boosted-trees implementation: xgboost
