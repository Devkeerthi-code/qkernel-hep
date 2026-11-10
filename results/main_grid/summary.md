# main_grid: mean ± std over seeds (std is the sample std, ddof=1)

## n=2 qubits, N=500, z map, reps=2, bandwidth=0.05 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.730 ± 0.018 |
| Projected QSVM | 0.731 ± 0.018 |
| Logistic regression | 0.728 ± 0.018 |
| RBF SVM | 0.732 ± 0.019 |
| Boosted trees | 0.733 ± 0.022 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 2.847 ± 0.658 |
| g, lambda=0.01 | 2.075 ± 0.801 |
| g(K_RBF || K_PQK), lambda=0 | 6144.039 ± 13034.699 |
| g_pqk, lambda=0.01 | 7.228 ± 8.596 |
| K_Q off-diagonal mean | 0.990 ± 0.002 |
| K_Q off-diagonal variance | 1.40e-04 ± 4.8e-05 |
| K_PQK off-diagonal variance | 0.071 ± 0.018 |
| K_RBF off-diagonal variance | 0.054 ± 0.046 |
| K_Q effective dimension | 1.020 ± 0.004 |
| AUC gap fidelity QSVM - best classical | -6.81e-03 ± 8.1e-03 |
| AUC gap projected QSVM - best classical | -5.90e-03 ± 5.5e-03 |

boosted-trees implementation: xgboost

## n=2 qubits, N=500, z map, reps=2, bandwidth=0.1 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.734 ± 0.019 |
| Projected QSVM | 0.730 ± 0.018 |
| Logistic regression | 0.728 ± 0.018 |
| RBF SVM | 0.732 ± 0.019 |
| Boosted trees | 0.733 ± 0.022 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 29.450 ± 60.070 |
| g, lambda=0.01 | 2.663 ± 1.295 |
| g(K_RBF || K_PQK), lambda=0 | 6630.445 ± 13615.051 |
| g_pqk, lambda=0.01 | 7.764 ± 8.114 |
| K_Q off-diagonal mean | 0.962 ± 0.007 |
| K_Q off-diagonal variance | 1.61e-03 ± 4.9e-04 |
| K_PQK off-diagonal variance | 0.073 ± 0.019 |
| K_RBF off-diagonal variance | 0.054 ± 0.046 |
| K_Q effective dimension | 1.078 ± 0.015 |
| AUC gap fidelity QSVM - best classical | -3.18e-03 ± 3.4e-03 |
| AUC gap projected QSVM - best classical | -7.18e-03 ± 5.8e-03 |

boosted-trees implementation: xgboost

## n=2 qubits, N=500, z map, reps=2, bandwidth=0.25 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.730 ± 0.021 |
| Projected QSVM | 0.729 ± 0.018 |
| Logistic regression | 0.728 ± 0.018 |
| RBF SVM | 0.732 ± 0.019 |
| Boosted trees | 0.733 ± 0.022 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 2053.781 ± 4504.444 |
| g, lambda=0.01 | 6.158 ± 6.975 |
| g(K_RBF || K_PQK), lambda=0 | 11956.961 ± 18993.140 |
| g_pqk, lambda=0.01 | 9.542 ± 8.383 |
| K_Q off-diagonal mean | 0.800 ± 0.016 |
| K_Q off-diagonal variance | 0.020 ± 0.001 |
| K_PQK off-diagonal variance | 0.047 ± 0.015 |
| K_RBF off-diagonal variance | 0.054 ± 0.046 |
| K_Q effective dimension | 1.515 ± 0.055 |
| AUC gap fidelity QSVM - best classical | -6.96e-03 ± 4.4e-03 |
| AUC gap projected QSVM - best classical | -8.33e-03 ± 2.2e-03 |

boosted-trees implementation: xgboost

## n=2 qubits, N=500, z map, reps=2, bandwidth=0.5 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.725 ± 0.021 |
| Projected QSVM | 0.724 ± 0.019 |
| Logistic regression | 0.728 ± 0.018 |
| RBF SVM | 0.732 ± 0.019 |
| Boosted trees | 0.733 ± 0.022 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 20741.754 ± 37344.438 |
| g, lambda=0.01 | 11.152 ± 9.284 |
| g(K_RBF || K_PQK), lambda=0 | 50567.366 ± 63117.427 |
| g_pqk, lambda=0.01 | 11.899 ± 7.418 |
| K_Q off-diagonal mean | 0.477 ± 0.027 |
| K_Q off-diagonal variance | 0.088 ± 0.004 |
| K_PQK off-diagonal variance | 0.041 ± 0.016 |
| K_RBF off-diagonal variance | 0.054 ± 0.046 |
| K_Q effective dimension | 3.176 ± 0.271 |
| AUC gap fidelity QSVM - best classical | -0.012 ± 0.009 |
| AUC gap projected QSVM - best classical | -0.013 ± 0.008 |

boosted-trees implementation: xgboost

## n=2 qubits, N=500, z map, reps=2, bandwidth=1.0 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.595 ± 0.052 |
| Projected QSVM | 0.642 ± 0.036 |
| Logistic regression | 0.728 ± 0.018 |
| RBF SVM | 0.732 ± 0.019 |
| Boosted trees | 0.733 ± 0.022 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 96517.352 ± 99935.171 |
| g, lambda=0.01 | 17.212 ± 7.507 |
| g(K_RBF || K_PQK), lambda=0 | 115387.118 ± 95943.938 |
| g_pqk, lambda=0.01 | 15.183 ± 3.609 |
| K_Q off-diagonal mean | 0.431 ± 0.007 |
| K_Q off-diagonal variance | 0.074 ± 0.002 |
| K_PQK off-diagonal variance | 0.031 ± 0.013 |
| K_RBF off-diagonal variance | 0.054 ± 0.046 |
| K_Q effective dimension | 3.831 ± 0.099 |
| AUC gap fidelity QSVM - best classical | -0.142 ± 0.041 |
| AUC gap projected QSVM - best classical | -0.095 ± 0.030 |

boosted-trees implementation: xgboost

## n=2 qubits, N=500, zz map, reps=1, bandwidth=0.05 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.737 ± 0.020 |
| Projected QSVM | 0.717 ± 0.022 |
| Logistic regression | 0.728 ± 0.018 |
| RBF SVM | 0.732 ± 0.019 |
| Boosted trees | 0.733 ± 0.022 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 98.366 ± 214.544 |
| g, lambda=0.01 | 3.799 ± 3.942 |
| g(K_RBF || K_PQK), lambda=0 | 93499.046 ± 76386.888 |
| g_pqk, lambda=0.01 | 20.291 ± 10.403 |
| K_Q off-diagonal mean | 0.904 ± 0.019 |
| K_Q off-diagonal variance | 0.019 ± 0.006 |
| K_PQK off-diagonal variance | 0.106 ± 0.014 |
| K_RBF off-diagonal variance | 0.054 ± 0.046 |
| K_Q effective dimension | 1.197 ± 0.041 |
| AUC gap fidelity QSVM - best classical | 6.84e-05 ± 5.5e-03 |
| AUC gap projected QSVM - best classical | -0.020 ± 0.013 |

boosted-trees implementation: xgboost

## n=2 qubits, N=500, zz map, reps=1, bandwidth=0.1 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.739 ± 0.020 |
| Projected QSVM | 0.725 ± 0.020 |
| Logistic regression | 0.728 ± 0.018 |
| RBF SVM | 0.732 ± 0.019 |
| Boosted trees | 0.733 ± 0.022 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 3019.223 ± 6708.224 |
| g, lambda=0.01 | 9.148 ± 11.819 |
| g(K_RBF || K_PQK), lambda=0 | 186881.300 ± 69514.488 |
| g_pqk, lambda=0.01 | 20.094 ± 3.410 |
| K_Q off-diagonal mean | 0.722 ± 0.039 |
| K_Q off-diagonal variance | 0.080 ± 0.014 |
| K_PQK off-diagonal variance | 0.096 ± 0.023 |
| K_RBF off-diagonal variance | 0.054 ± 0.046 |
| K_Q effective dimension | 1.664 ± 0.116 |
| AUC gap fidelity QSVM - best classical | 1.67e-03 ± 1.9e-03 |
| AUC gap projected QSVM - best classical | -0.012 ± 0.005 |

boosted-trees implementation: xgboost

## n=2 qubits, N=500, zz map, reps=1, bandwidth=0.25 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.736 ± 0.018 |
| Projected QSVM | 0.706 ± 0.023 |
| Logistic regression | 0.728 ± 0.018 |
| RBF SVM | 0.732 ± 0.019 |
| Boosted trees | 0.733 ± 0.022 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 76933.085 ± 129216.312 |
| g, lambda=0.01 | 19.621 ± 12.311 |
| g(K_RBF || K_PQK), lambda=0 | 304764.996 ± 59187.093 |
| g_pqk, lambda=0.01 | 20.880 ± 1.265 |
| K_Q off-diagonal mean | 0.422 ± 0.021 |
| K_Q off-diagonal variance | 0.099 ± 0.005 |
| K_PQK off-diagonal variance | 0.081 ± 0.010 |
| K_RBF off-diagonal variance | 0.054 ± 0.046 |
| K_Q effective dimension | 3.600 ± 0.285 |
| AUC gap fidelity QSVM - best classical | -8.31e-04 ± 1.6e-03 |
| AUC gap projected QSVM - best classical | -0.031 ± 0.008 |

boosted-trees implementation: xgboost

## n=2 qubits, N=500, zz map, reps=1, bandwidth=0.5 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.715 ± 0.030 |
| Projected QSVM | 0.696 ± 0.024 |
| Logistic regression | 0.728 ± 0.018 |
| RBF SVM | 0.732 ± 0.019 |
| Boosted trees | 0.733 ± 0.022 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 231307.820 ± 175213.963 |
| g, lambda=0.01 | 18.634 ± 6.711 |
| g(K_RBF || K_PQK), lambda=0 | 358559.215 ± 17015.170 |
| g_pqk, lambda=0.01 | 14.247 ± 4.098 |
| K_Q off-diagonal mean | 0.301 ± 0.016 |
| K_Q off-diagonal variance | 0.063 ± 0.004 |
| K_PQK off-diagonal variance | 0.063 ± 0.011 |
| K_RBF off-diagonal variance | 0.054 ± 0.046 |
| K_Q effective dimension | 6.503 ± 0.546 |
| AUC gap fidelity QSVM - best classical | -0.022 ± 0.016 |
| AUC gap projected QSVM - best classical | -0.041 ± 0.009 |

boosted-trees implementation: xgboost

## n=2 qubits, N=500, zz map, reps=1, bandwidth=1.0 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.606 ± 0.044 |
| Projected QSVM | 0.588 ± 0.041 |
| Logistic regression | 0.728 ± 0.018 |
| RBF SVM | 0.732 ± 0.019 |
| Boosted trees | 0.733 ± 0.022 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 338116.840 ± 54824.649 |
| g, lambda=0.01 | 12.722 ± 4.083 |
| g(K_RBF || K_PQK), lambda=0 | 381149.645 ± 53674.654 |
| g_pqk, lambda=0.01 | 9.925 ± 1.544 |
| K_Q off-diagonal mean | 0.252 ± 0.001 |
| K_Q off-diagonal variance | 0.049 ± 0.001 |
| K_PQK off-diagonal variance | 0.053 ± 0.011 |
| K_RBF off-diagonal variance | 0.054 ± 0.046 |
| K_Q effective dimension | 8.757 ± 0.085 |
| AUC gap fidelity QSVM - best classical | -0.132 ± 0.039 |
| AUC gap projected QSVM - best classical | -0.150 ± 0.034 |

boosted-trees implementation: xgboost

## n=2 qubits, N=500, zz map, reps=2, bandwidth=0.05 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.739 ± 0.017 |
| Projected QSVM | 0.736 ± 0.019 |
| Logistic regression | 0.728 ± 0.018 |
| RBF SVM | 0.732 ± 0.019 |
| Boosted trees | 0.733 ± 0.022 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 398.342 ± 880.642 |
| g, lambda=0.01 | 3.970 ± 4.169 |
| g(K_RBF || K_PQK), lambda=0 | 40006.397 ± 54254.607 |
| g_pqk, lambda=0.01 | 13.580 ± 12.145 |
| K_Q off-diagonal mean | 0.898 ± 0.020 |
| K_Q off-diagonal variance | 0.021 ± 0.006 |
| K_PQK off-diagonal variance | 0.104 ± 0.020 |
| K_RBF off-diagonal variance | 0.054 ± 0.046 |
| K_Q effective dimension | 1.209 ± 0.043 |
| AUC gap fidelity QSVM - best classical | 1.82e-03 ± 3.9e-03 |
| AUC gap projected QSVM - best classical | -1.36e-03 ± 5.3e-03 |

boosted-trees implementation: xgboost

## n=2 qubits, N=500, zz map, reps=2, bandwidth=0.1 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.734 ± 0.021 |
| Projected QSVM | 0.735 ± 0.019 |
| Logistic regression | 0.728 ± 0.018 |
| RBF SVM | 0.732 ± 0.019 |
| Boosted trees | 0.733 ± 0.022 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 6639.376 ± 13519.389 |
| g, lambda=0.01 | 9.574 ± 11.422 |
| g(K_RBF || K_PQK), lambda=0 | 90366.316 ± 91412.187 |
| g_pqk, lambda=0.01 | 16.263 ± 7.817 |
| K_Q off-diagonal mean | 0.721 ± 0.038 |
| K_Q off-diagonal variance | 0.077 ± 0.014 |
| K_PQK off-diagonal variance | 0.082 ± 0.014 |
| K_RBF off-diagonal variance | 0.054 ± 0.046 |
| K_Q effective dimension | 1.679 ± 0.114 |
| AUC gap fidelity QSVM - best classical | -3.57e-03 ± 6.2e-03 |
| AUC gap projected QSVM - best classical | -2.52e-03 ± 4.1e-03 |

boosted-trees implementation: xgboost

## n=2 qubits, N=500, zz map, reps=2, bandwidth=0.25 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.694 ± 0.022 |
| Projected QSVM | 0.702 ± 0.020 |
| Logistic regression | 0.728 ± 0.018 |
| RBF SVM | 0.732 ± 0.019 |
| Boosted trees | 0.733 ± 0.022 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 97818.263 ± 111346.747 |
| g, lambda=0.01 | 16.661 ± 8.872 |
| g(K_RBF || K_PQK), lambda=0 | 150223.357 ± 65832.196 |
| g_pqk, lambda=0.01 | 18.830 ± 4.982 |
| K_Q off-diagonal mean | 0.542 ± 0.056 |
| K_Q off-diagonal variance | 0.071 ± 0.009 |
| K_PQK off-diagonal variance | 0.059 ± 0.016 |
| K_RBF off-diagonal variance | 0.054 ± 0.046 |
| K_Q effective dimension | 2.760 ± 0.368 |
| AUC gap fidelity QSVM - best classical | -0.043 ± 0.012 |
| AUC gap projected QSVM - best classical | -0.035 ± 0.008 |

boosted-trees implementation: xgboost

## n=2 qubits, N=500, zz map, reps=2, bandwidth=0.5 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.689 ± 0.023 |
| Projected QSVM | 0.687 ± 0.023 |
| Logistic regression | 0.728 ± 0.018 |
| RBF SVM | 0.732 ± 0.019 |
| Boosted trees | 0.733 ± 0.022 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 209973.699 ± 95523.301 |
| g, lambda=0.01 | 17.143 ± 3.530 |
| g(K_RBF || K_PQK), lambda=0 | 187873.543 ± 62293.735 |
| g_pqk, lambda=0.01 | 14.384 ± 3.975 |
| K_Q off-diagonal mean | 0.389 ± 0.009 |
| K_Q off-diagonal variance | 0.068 ± 0.002 |
| K_PQK off-diagonal variance | 0.034 ± 0.015 |
| K_RBF off-diagonal variance | 0.054 ± 0.046 |
| K_Q effective dimension | 4.531 ± 0.188 |
| AUC gap fidelity QSVM - best classical | -0.048 ± 0.016 |
| AUC gap projected QSVM - best classical | -0.050 ± 0.014 |

boosted-trees implementation: xgboost

## n=2 qubits, N=500, zz map, reps=2, bandwidth=1.0 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.546 ± 0.026 |
| Projected QSVM | 0.546 ± 0.032 |
| Logistic regression | 0.728 ± 0.018 |
| RBF SVM | 0.732 ± 0.019 |
| Boosted trees | 0.733 ± 0.022 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 339172.600 ± 44991.490 |
| g, lambda=0.01 | 11.972 ± 3.637 |
| g(K_RBF || K_PQK), lambda=0 | 271196.323 ± 49813.263 |
| g_pqk, lambda=0.01 | 9.077 ± 1.680 |
| K_Q off-diagonal mean | 0.305 ± 0.006 |
| K_Q off-diagonal variance | 0.052 ± 0.002 |
| K_PQK off-diagonal variance | 0.023 ± 0.010 |
| K_RBF off-diagonal variance | 0.054 ± 0.046 |
| K_Q effective dimension | 6.832 ± 0.248 |
| AUC gap fidelity QSVM - best classical | -0.191 ± 0.027 |
| AUC gap projected QSVM - best classical | -0.191 ± 0.037 |

boosted-trees implementation: xgboost

## n=4 qubits, N=500, z map, reps=2, bandwidth=0.05 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.781 ± 0.015 |
| Projected QSVM | 0.789 ± 0.014 |
| Logistic regression | 0.760 ± 0.015 |
| RBF SVM | 0.787 ± 0.013 |
| Boosted trees | 0.784 ± 0.014 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 4.224 ± 0.866 |
| g, lambda=0.01 | 3.384 ± 1.047 |
| g(K_RBF || K_PQK), lambda=0 | 9.191 ± 7.698 |
| g_pqk, lambda=0.01 | 1.827 ± 0.350 |
| K_Q off-diagonal mean | 0.981 ± 0.003 |
| K_Q off-diagonal variance | 2.57e-04 ± 4.5e-05 |
| K_PQK off-diagonal variance | 0.050 ± 0.015 |
| K_RBF off-diagonal variance | 0.050 ± 0.017 |
| K_Q effective dimension | 1.039 ± 0.006 |
| AUC gap fidelity QSVM - best classical | -6.91e-03 ± 7.2e-03 |
| AUC gap projected QSVM - best classical | 1.87e-03 ± 4.3e-03 |

boosted-trees implementation: xgboost

## n=4 qubits, N=500, z map, reps=2, bandwidth=0.1 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.791 ± 0.015 |
| Projected QSVM | 0.786 ± 0.013 |
| Logistic regression | 0.760 ± 0.015 |
| RBF SVM | 0.787 ± 0.013 |
| Boosted trees | 0.784 ± 0.014 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 3.781 ± 0.907 |
| g, lambda=0.01 | 3.096 ± 1.016 |
| g(K_RBF || K_PQK), lambda=0 | 34.081 ± 37.195 |
| g_pqk, lambda=0.01 | 2.203 ± 0.330 |
| K_Q off-diagonal mean | 0.928 ± 0.009 |
| K_Q off-diagonal variance | 2.84e-03 ± 4.5e-04 |
| K_PQK off-diagonal variance | 0.044 ± 0.014 |
| K_RBF off-diagonal variance | 0.050 ± 0.017 |
| K_Q effective dimension | 1.157 ± 0.022 |
| AUC gap fidelity QSVM - best classical | 3.29e-03 ± 5.3e-03 |
| AUC gap projected QSVM - best classical | -1.96e-03 ± 4.3e-03 |

boosted-trees implementation: xgboost

## n=4 qubits, N=500, z map, reps=2, bandwidth=0.25 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.788 ± 0.016 |
| Projected QSVM | 0.787 ± 0.016 |
| Logistic regression | 0.760 ± 0.015 |
| RBF SVM | 0.787 ± 0.013 |
| Boosted trees | 0.784 ± 0.014 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 34.898 ± 70.945 |
| g, lambda=0.01 | 3.237 ± 1.288 |
| g(K_RBF || K_PQK), lambda=0 | 3960.763 ± 8476.861 |
| g_pqk, lambda=0.01 | 5.139 ± 4.504 |
| K_Q off-diagonal mean | 0.663 ± 0.016 |
| K_Q off-diagonal variance | 0.025 ± 0.001 |
| K_PQK off-diagonal variance | 0.037 ± 0.008 |
| K_RBF off-diagonal variance | 0.050 ± 0.017 |
| K_Q effective dimension | 2.150 ± 0.097 |
| AUC gap fidelity QSVM - best classical | 2.38e-04 ± 6.4e-03 |
| AUC gap projected QSVM - best classical | -3.67e-04 ± 6.9e-03 |

boosted-trees implementation: xgboost

## n=4 qubits, N=500, z map, reps=2, bandwidth=0.5 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.781 ± 0.016 |
| Projected QSVM | 0.784 ± 0.016 |
| Logistic regression | 0.760 ± 0.015 |
| RBF SVM | 0.787 ± 0.013 |
| Boosted trees | 0.784 ± 0.014 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 2621.847 ± 5504.535 |
| g, lambda=0.01 | 6.556 ± 5.202 |
| g(K_RBF || K_PQK), lambda=0 | 2317.608 ± 4034.094 |
| g_pqk, lambda=0.01 | 5.937 ± 2.211 |
| K_Q off-diagonal mean | 0.275 ± 0.016 |
| K_Q off-diagonal variance | 0.052 ± 0.003 |
| K_PQK off-diagonal variance | 0.023 ± 0.013 |
| K_RBF off-diagonal variance | 0.050 ± 0.017 |
| K_Q effective dimension | 7.764 ± 0.647 |
| AUC gap fidelity QSVM - best classical | -6.59e-03 ± 7.9e-03 |
| AUC gap projected QSVM - best classical | -4.01e-03 ± 9.7e-03 |

boosted-trees implementation: xgboost

## n=4 qubits, N=500, z map, reps=2, bandwidth=1.0 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.670 ± 0.056 |
| Projected QSVM | 0.704 ± 0.039 |
| Logistic regression | 0.760 ± 0.015 |
| RBF SVM | 0.787 ± 0.013 |
| Boosted trees | 0.784 ± 0.014 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 29767.333 ± 50776.405 |
| g, lambda=0.01 | 15.057 ± 4.117 |
| g(K_RBF || K_PQK), lambda=0 | 27139.864 ± 50495.135 |
| g_pqk, lambda=0.01 | 11.951 ± 5.180 |
| K_Q off-diagonal mean | 0.184 ± 0.010 |
| K_Q off-diagonal variance | 0.033 ± 0.001 |
| K_PQK off-diagonal variance | 0.012 ± 0.008 |
| K_RBF off-diagonal variance | 0.050 ± 0.017 |
| K_Q effective dimension | 14.506 ± 1.082 |
| AUC gap fidelity QSVM - best classical | -0.117 ± 0.045 |
| AUC gap projected QSVM - best classical | -0.083 ± 0.033 |

boosted-trees implementation: xgboost

## n=4 qubits, N=500, zz map, reps=1, bandwidth=0.05 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.789 ± 0.017 |
| Projected QSVM | 0.767 ± 0.026 |
| Logistic regression | 0.760 ± 0.015 |
| RBF SVM | 0.787 ± 0.013 |
| Boosted trees | 0.784 ± 0.014 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 6.197 ± 7.214 |
| g, lambda=0.01 | 2.844 ± 0.713 |
| g(K_RBF || K_PQK), lambda=0 | 858.233 ± 1794.274 |
| g_pqk, lambda=0.01 | 5.141 ± 3.502 |
| K_Q off-diagonal mean | 0.773 ± 0.023 |
| K_Q off-diagonal variance | 0.035 ± 0.006 |
| K_PQK off-diagonal variance | 0.052 ± 0.015 |
| K_RBF off-diagonal variance | 0.050 ± 0.017 |
| K_Q effective dimension | 1.581 ± 0.071 |
| AUC gap fidelity QSVM - best classical | 1.13e-03 ± 6.8e-03 |
| AUC gap projected QSVM - best classical | -0.021 ± 0.017 |

boosted-trees implementation: xgboost

## n=4 qubits, N=500, zz map, reps=1, bandwidth=0.1 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.787 ± 0.016 |
| Projected QSVM | 0.742 ± 0.013 |
| Logistic regression | 0.760 ± 0.015 |
| RBF SVM | 0.787 ± 0.013 |
| Boosted trees | 0.784 ± 0.014 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 433.201 ± 935.037 |
| g, lambda=0.01 | 5.050 ± 4.631 |
| g(K_RBF || K_PQK), lambda=0 | 2676.459 ± 4845.254 |
| g_pqk, lambda=0.01 | 7.900 ± 3.034 |
| K_Q off-diagonal mean | 0.435 ± 0.030 |
| K_Q off-diagonal variance | 0.081 ± 0.003 |
| K_PQK off-diagonal variance | 0.066 ± 0.012 |
| K_RBF off-diagonal variance | 0.050 ± 0.017 |
| K_Q effective dimension | 3.689 ± 0.311 |
| AUC gap fidelity QSVM - best classical | -7.70e-04 ± 5.5e-03 |
| AUC gap projected QSVM - best classical | -0.045 ± 0.011 |

boosted-trees implementation: xgboost

## n=4 qubits, N=500, zz map, reps=1, bandwidth=0.25 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.749 ± 0.024 |
| Projected QSVM | 0.700 ± 0.029 |
| Logistic regression | 0.760 ± 0.015 |
| RBF SVM | 0.787 ± 0.013 |
| Boosted trees | 0.784 ± 0.014 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 20988.568 ± 37386.041 |
| g, lambda=0.01 | 13.508 ± 2.203 |
| g(K_RBF || K_PQK), lambda=0 | 28743.868 ± 37551.535 |
| g_pqk, lambda=0.01 | 13.946 ± 3.135 |
| K_Q off-diagonal mean | 0.104 ± 0.005 |
| K_Q off-diagonal variance | 0.026 ± 0.003 |
| K_PQK off-diagonal variance | 0.029 ± 0.017 |
| K_RBF off-diagonal variance | 0.050 ± 0.017 |
| K_Q effective dimension | 26.114 ± 2.339 |
| AUC gap fidelity QSVM - best classical | -0.039 ± 0.015 |
| AUC gap projected QSVM - best classical | -0.088 ± 0.017 |

boosted-trees implementation: xgboost

## n=4 qubits, N=500, zz map, reps=1, bandwidth=0.5 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.619 ± 0.031 |
| Projected QSVM | 0.614 ± 0.013 |
| Logistic regression | 0.760 ± 0.015 |
| RBF SVM | 0.787 ± 0.013 |
| Boosted trees | 0.784 ± 0.014 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 49927.006 ± 60320.206 |
| g, lambda=0.01 | 10.818 ± 1.876 |
| g(K_RBF || K_PQK), lambda=0 | 67317.077 ± 85366.802 |
| g_pqk, lambda=0.01 | 12.225 ± 2.682 |
| K_Q off-diagonal mean | 0.065 ± 0.001 |
| K_Q off-diagonal variance | 7.81e-03 ± 4.8e-04 |
| K_PQK off-diagonal variance | 0.017 ± 0.008 |
| K_RBF off-diagonal variance | 0.050 ± 0.017 |
| K_Q effective dimension | 71.575 ± 3.055 |
| AUC gap fidelity QSVM - best classical | -0.169 ± 0.031 |
| AUC gap projected QSVM - best classical | -0.174 ± 0.015 |

boosted-trees implementation: xgboost

## n=4 qubits, N=500, zz map, reps=1, bandwidth=1.0 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.493 ± 0.017 |
| Projected QSVM | 0.503 ± 0.024 |
| Logistic regression | 0.760 ± 0.015 |
| RBF SVM | 0.787 ± 0.013 |
| Boosted trees | 0.784 ± 0.014 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 58137.087 ± 51699.667 |
| g, lambda=0.01 | 8.422 ± 1.206 |
| g(K_RBF || K_PQK), lambda=0 | 81908.837 ± 87647.959 |
| g_pqk, lambda=0.01 | 11.960 ± 3.272 |
| K_Q off-diagonal mean | 0.062 ± 0.000 |
| K_Q off-diagonal variance | 6.27e-03 ± 1.1e-04 |
| K_PQK off-diagonal variance | 0.031 ± 0.011 |
| K_RBF off-diagonal variance | 0.050 ± 0.017 |
| K_Q effective dimension | 82.293 ± 0.820 |
| AUC gap fidelity QSVM - best classical | -0.294 ± 0.028 |
| AUC gap projected QSVM - best classical | -0.284 ± 0.030 |

boosted-trees implementation: xgboost

## n=4 qubits, N=500, zz map, reps=2, bandwidth=0.05 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.785 ± 0.016 |
| Projected QSVM | 0.773 ± 0.019 |
| Logistic regression | 0.760 ± 0.015 |
| RBF SVM | 0.787 ± 0.013 |
| Boosted trees | 0.784 ± 0.014 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 114.297 ± 244.691 |
| g, lambda=0.01 | 3.710 ± 2.285 |
| g(K_RBF || K_PQK), lambda=0 | 791.536 ± 1742.370 |
| g_pqk, lambda=0.01 | 3.941 ± 3.358 |
| K_Q off-diagonal mean | 0.654 ± 0.028 |
| K_Q off-diagonal variance | 0.055 ± 0.006 |
| K_PQK off-diagonal variance | 0.054 ± 0.015 |
| K_RBF off-diagonal variance | 0.050 ± 0.017 |
| K_Q effective dimension | 2.072 ± 0.126 |
| AUC gap fidelity QSVM - best classical | -2.41e-03 ± 1.0e-02 |
| AUC gap projected QSVM - best classical | -0.014 ± 0.015 |

boosted-trees implementation: xgboost

## n=4 qubits, N=500, zz map, reps=2, bandwidth=0.1 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.779 ± 0.017 |
| Projected QSVM | 0.763 ± 0.015 |
| Logistic regression | 0.760 ± 0.015 |
| RBF SVM | 0.787 ± 0.013 |
| Boosted trees | 0.784 ± 0.014 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 4899.269 ± 10044.911 |
| g, lambda=0.01 | 8.991 ± 5.645 |
| g(K_RBF || K_PQK), lambda=0 | 2828.666 ± 5259.100 |
| g_pqk, lambda=0.01 | 7.199 ± 4.040 |
| K_Q off-diagonal mean | 0.347 ± 0.039 |
| K_Q off-diagonal variance | 0.072 ± 0.002 |
| K_PQK off-diagonal variance | 0.036 ± 0.013 |
| K_RBF off-diagonal variance | 0.050 ± 0.017 |
| K_Q effective dimension | 5.210 ± 0.662 |
| AUC gap fidelity QSVM - best classical | -8.30e-03 ± 6.8e-03 |
| AUC gap projected QSVM - best classical | -0.025 ± 0.005 |

boosted-trees implementation: xgboost

## n=4 qubits, N=500, zz map, reps=2, bandwidth=0.25 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.717 ± 0.037 |
| Projected QSVM | 0.696 ± 0.049 |
| Logistic regression | 0.760 ± 0.015 |
| RBF SVM | 0.787 ± 0.013 |
| Boosted trees | 0.784 ± 0.014 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 34674.464 ± 51406.337 |
| g, lambda=0.01 | 13.317 ± 1.245 |
| g(K_RBF || K_PQK), lambda=0 | 44577.858 ± 62767.564 |
| g_pqk, lambda=0.01 | 12.541 ± 1.842 |
| K_Q off-diagonal mean | 0.100 ± 0.012 |
| K_Q off-diagonal variance | 0.017 ± 0.003 |
| K_PQK off-diagonal variance | 0.018 ± 0.010 |
| K_RBF off-diagonal variance | 0.050 ± 0.017 |
| K_Q effective dimension | 35.388 ± 6.405 |
| AUC gap fidelity QSVM - best classical | -0.070 ± 0.024 |
| AUC gap projected QSVM - best classical | -0.092 ± 0.040 |

boosted-trees implementation: xgboost

## n=4 qubits, N=500, zz map, reps=2, bandwidth=0.5 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.589 ± 0.013 |
| Projected QSVM | 0.596 ± 0.014 |
| Logistic regression | 0.760 ± 0.015 |
| RBF SVM | 0.787 ± 0.013 |
| Boosted trees | 0.784 ± 0.014 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 56341.183 ± 60660.132 |
| g, lambda=0.01 | 10.049 ± 1.572 |
| g(K_RBF || K_PQK), lambda=0 | 62613.396 ± 71228.551 |
| g_pqk, lambda=0.01 | 11.488 ± 3.135 |
| K_Q off-diagonal mean | 0.079 ± 0.003 |
| K_Q off-diagonal variance | 7.72e-03 ± 7.7e-04 |
| K_PQK off-diagonal variance | 0.014 ± 0.009 |
| K_RBF off-diagonal variance | 0.050 ± 0.017 |
| K_Q effective dimension | 62.869 ± 4.713 |
| AUC gap fidelity QSVM - best classical | -0.199 ± 0.023 |
| AUC gap projected QSVM - best classical | -0.192 ± 0.018 |

boosted-trees implementation: xgboost

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

## n=6 qubits, N=500, z map, reps=2, bandwidth=0.05 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.782 ± 0.020 |
| Projected QSVM | 0.799 ± 0.013 |
| Logistic regression | 0.763 ± 0.021 |
| RBF SVM | 0.793 ± 0.012 |
| Boosted trees | 0.794 ± 0.010 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 5.007 ± 1.204 |
| g, lambda=0.01 | 4.415 ± 1.537 |
| g(K_RBF || K_PQK), lambda=0 | 4.257 ± 5.503 |
| g_pqk, lambda=0.01 | 1.791 ± 0.483 |
| K_Q off-diagonal mean | 0.973 ± 0.004 |
| K_Q off-diagonal variance | 3.87e-04 ± 6.1e-05 |
| K_PQK off-diagonal variance | 0.035 ± 0.010 |
| K_RBF off-diagonal variance | 0.033 ± 0.010 |
| K_Q effective dimension | 1.056 ± 0.008 |
| AUC gap fidelity QSVM - best classical | -0.016 ± 0.015 |
| AUC gap projected QSVM - best classical | 1.00e-03 ± 6.3e-03 |

boosted-trees implementation: xgboost

## n=6 qubits, N=500, z map, reps=2, bandwidth=0.1 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.800 ± 0.016 |
| Projected QSVM | 0.797 ± 0.011 |
| Logistic regression | 0.763 ± 0.021 |
| RBF SVM | 0.793 ± 0.012 |
| Boosted trees | 0.794 ± 0.010 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 4.439 ± 1.297 |
| g, lambda=0.01 | 3.976 ± 1.496 |
| g(K_RBF || K_PQK), lambda=0 | 3.856 ± 4.330 |
| g_pqk, lambda=0.01 | 1.378 ± 0.146 |
| K_Q off-diagonal mean | 0.899 ± 0.013 |
| K_Q off-diagonal variance | 4.03e-03 ± 6.3e-04 |
| K_PQK off-diagonal variance | 0.033 ± 0.011 |
| K_RBF off-diagonal variance | 0.033 ± 0.010 |
| K_Q effective dimension | 1.232 ± 0.034 |
| AUC gap fidelity QSVM - best classical | 2.49e-03 ± 8.3e-03 |
| AUC gap projected QSVM - best classical | -1.18e-03 ± 4.2e-03 |

boosted-trees implementation: xgboost

## n=6 qubits, N=500, z map, reps=2, bandwidth=0.25 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.795 ± 0.008 |
| Projected QSVM | 0.798 ± 0.011 |
| Logistic regression | 0.763 ± 0.021 |
| RBF SVM | 0.793 ± 0.012 |
| Boosted trees | 0.794 ± 0.010 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 15.854 ± 27.816 |
| g, lambda=0.01 | 3.573 ± 1.095 |
| g(K_RBF || K_PQK), lambda=0 | 158.120 ± 335.092 |
| g_pqk, lambda=0.01 | 3.433 ± 2.140 |
| K_Q off-diagonal mean | 0.560 ± 0.023 |
| K_Q off-diagonal variance | 0.026 ± 0.000 |
| K_PQK off-diagonal variance | 0.028 ± 0.001 |
| K_RBF off-diagonal variance | 0.033 ± 0.010 |
| K_Q effective dimension | 2.944 ± 0.216 |
| AUC gap fidelity QSVM - best classical | -2.35e-03 ± 2.6e-03 |
| AUC gap projected QSVM - best classical | 1.28e-05 ± 5.6e-03 |

boosted-trees implementation: xgboost

## n=6 qubits, N=500, z map, reps=2, bandwidth=0.5 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.786 ± 0.014 |
| Projected QSVM | 0.790 ± 0.014 |
| Logistic regression | 0.763 ± 0.021 |
| RBF SVM | 0.793 ± 0.012 |
| Boosted trees | 0.794 ± 0.010 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 547.700 ± 1179.437 |
| g, lambda=0.01 | 5.635 ± 4.013 |
| g(K_RBF || K_PQK), lambda=0 | 1156.457 ± 2465.424 |
| g_pqk, lambda=0.01 | 6.099 ± 3.652 |
| K_Q off-diagonal mean | 0.166 ± 0.013 |
| K_Q off-diagonal variance | 0.029 ± 0.003 |
| K_PQK off-diagonal variance | 0.021 ± 0.002 |
| K_RBF off-diagonal variance | 0.033 ± 0.010 |
| K_Q effective dimension | 17.379 ± 2.031 |
| AUC gap fidelity QSVM - best classical | -0.012 ± 0.012 |
| AUC gap projected QSVM - best classical | -7.35e-03 ± 1.1e-02 |

boosted-trees implementation: xgboost

## n=6 qubits, N=500, z map, reps=2, bandwidth=1.0 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.683 ± 0.036 |
| Projected QSVM | 0.692 ± 0.029 |
| Logistic regression | 0.763 ± 0.021 |
| RBF SVM | 0.793 ± 0.012 |
| Boosted trees | 0.794 ± 0.010 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 3719.599 ± 7936.355 |
| g, lambda=0.01 | 10.493 ± 2.088 |
| g(K_RBF || K_PQK), lambda=0 | 1689.872 ± 3385.107 |
| g_pqk, lambda=0.01 | 9.158 ± 1.566 |
| K_Q off-diagonal mean | 0.079 ± 0.010 |
| K_Q off-diagonal variance | 0.012 ± 0.002 |
| K_PQK off-diagonal variance | 6.98e-03 ± 4.6e-03 |
| K_RBF off-diagonal variance | 0.033 ± 0.010 |
| K_Q effective dimension | 51.138 ± 8.190 |
| AUC gap fidelity QSVM - best classical | -0.115 ± 0.029 |
| AUC gap projected QSVM - best classical | -0.105 ± 0.021 |

boosted-trees implementation: xgboost

## n=6 qubits, N=500, zz map, reps=1, bandwidth=0.05 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.790 ± 0.008 |
| Projected QSVM | 0.757 ± 0.013 |
| Logistic regression | 0.763 ± 0.021 |
| RBF SVM | 0.793 ± 0.012 |
| Boosted trees | 0.794 ± 0.010 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 6.566 ± 7.156 |
| g, lambda=0.01 | 3.365 ± 0.840 |
| g(K_RBF || K_PQK), lambda=0 | 81.849 ± 170.745 |
| g_pqk, lambda=0.01 | 4.178 ± 1.711 |
| K_Q off-diagonal mean | 0.657 ± 0.035 |
| K_Q off-diagonal variance | 0.043 ± 0.006 |
| K_PQK off-diagonal variance | 0.048 ± 0.013 |
| K_RBF off-diagonal variance | 0.033 ± 0.010 |
| K_Q effective dimension | 2.111 ± 0.174 |
| AUC gap fidelity QSVM - best classical | -8.04e-03 ± 4.6e-03 |
| AUC gap projected QSVM - best classical | -0.041 ± 0.016 |

boosted-trees implementation: xgboost

## n=6 qubits, N=500, zz map, reps=1, bandwidth=0.1 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.780 ± 0.007 |
| Projected QSVM | 0.741 ± 0.018 |
| Logistic regression | 0.763 ± 0.021 |
| RBF SVM | 0.793 ± 0.012 |
| Boosted trees | 0.794 ± 0.010 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 162.535 ± 346.293 |
| g, lambda=0.01 | 5.052 ± 4.524 |
| g(K_RBF || K_PQK), lambda=0 | 294.001 ± 553.381 |
| g_pqk, lambda=0.01 | 6.485 ± 2.569 |
| K_Q off-diagonal mean | 0.264 ± 0.035 |
| K_Q off-diagonal variance | 0.056 ± 0.004 |
| K_PQK off-diagonal variance | 0.038 ± 0.014 |
| K_RBF off-diagonal variance | 0.033 ± 0.010 |
| K_Q effective dimension | 7.945 ± 1.342 |
| AUC gap fidelity QSVM - best classical | -0.018 ± 0.005 |
| AUC gap projected QSVM - best classical | -0.057 ± 0.016 |

boosted-trees implementation: xgboost

## n=6 qubits, N=500, zz map, reps=1, bandwidth=0.25 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.732 ± 0.010 |
| Projected QSVM | 0.682 ± 0.034 |
| Logistic regression | 0.763 ± 0.021 |
| RBF SVM | 0.793 ± 0.012 |
| Boosted trees | 0.794 ± 0.010 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 3708.673 ± 7973.012 |
| g, lambda=0.01 | 8.466 ± 1.098 |
| g(K_RBF || K_PQK), lambda=0 | 1692.384 ± 3512.063 |
| g_pqk, lambda=0.01 | 11.801 ± 2.873 |
| K_Q off-diagonal mean | 0.028 ± 0.003 |
| K_Q off-diagonal variance | 5.33e-03 ± 1.3e-03 |
| K_PQK off-diagonal variance | 0.011 ± 0.002 |
| K_RBF off-diagonal variance | 0.033 ± 0.010 |
| K_Q effective dimension | 126.330 ± 21.378 |
| AUC gap fidelity QSVM - best classical | -0.066 ± 0.006 |
| AUC gap projected QSVM - best classical | -0.115 ± 0.029 |

boosted-trees implementation: xgboost

## n=6 qubits, N=500, zz map, reps=1, bandwidth=0.5 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.573 ± 0.045 |
| Projected QSVM | 0.599 ± 0.024 |
| Logistic regression | 0.763 ± 0.021 |
| RBF SVM | 0.793 ± 0.012 |
| Boosted trees | 0.794 ± 0.010 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 7243.807 ± 15401.409 |
| g, lambda=0.01 | 7.166 ± 0.839 |
| g(K_RBF || K_PQK), lambda=0 | 6517.378 ± 13640.001 |
| g_pqk, lambda=0.01 | 13.835 ± 2.923 |
| K_Q off-diagonal mean | 0.016 ± 0.000 |
| K_Q off-diagonal variance | 9.26e-04 ± 1.2e-04 |
| K_PQK off-diagonal variance | 0.013 ± 0.007 |
| K_RBF off-diagonal variance | 0.033 ± 0.010 |
| K_Q effective dimension | 314.628 ± 12.410 |
| AUC gap fidelity QSVM - best classical | -0.225 ± 0.053 |
| AUC gap projected QSVM - best classical | -0.199 ± 0.031 |

boosted-trees implementation: xgboost

## n=6 qubits, N=500, zz map, reps=1, bandwidth=1.0 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.498 ± 0.016 |
| Projected QSVM | 0.527 ± 0.021 |
| Logistic regression | 0.763 ± 0.021 |
| RBF SVM | 0.793 ± 0.012 |
| Boosted trees | 0.794 ± 0.010 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 7921.719 ± 16657.088 |
| g, lambda=0.01 | 6.724 ± 0.560 |
| g(K_RBF || K_PQK), lambda=0 | 8085.735 ± 17386.369 |
| g_pqk, lambda=0.01 | 11.897 ± 2.296 |
| K_Q off-diagonal mean | 0.016 ± 0.000 |
| K_Q off-diagonal variance | 6.88e-04 ± 1.7e-05 |
| K_PQK off-diagonal variance | 8.09e-03 ± 7.8e-04 |
| K_RBF off-diagonal variance | 0.033 ± 0.010 |
| K_Q effective dimension | 341.037 ± 2.007 |
| AUC gap fidelity QSVM - best classical | -0.299 ± 0.012 |
| AUC gap projected QSVM - best classical | -0.271 ± 0.026 |

boosted-trees implementation: xgboost

## n=6 qubits, N=500, zz map, reps=2, bandwidth=0.05 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.780 ± 0.012 |
| Projected QSVM | 0.766 ± 0.009 |
| Logistic regression | 0.763 ± 0.021 |
| RBF SVM | 0.793 ± 0.012 |
| Boosted trees | 0.794 ± 0.010 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 33.659 ± 67.337 |
| g, lambda=0.01 | 3.793 ± 2.098 |
| g(K_RBF || K_PQK), lambda=0 | 31.196 ± 57.684 |
| g_pqk, lambda=0.01 | 3.608 ± 0.720 |
| K_Q off-diagonal mean | 0.497 ± 0.037 |
| K_Q off-diagonal variance | 0.056 ± 0.003 |
| K_PQK off-diagonal variance | 0.040 ± 0.010 |
| K_RBF off-diagonal variance | 0.033 ± 0.010 |
| K_Q effective dimension | 3.306 ± 0.371 |
| AUC gap fidelity QSVM - best classical | -0.018 ± 0.008 |
| AUC gap projected QSVM - best classical | -0.032 ± 0.016 |

boosted-trees implementation: xgboost

## n=6 qubits, N=500, zz map, reps=2, bandwidth=0.1 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.766 ± 0.006 |
| Projected QSVM | 0.755 ± 0.017 |
| Logistic regression | 0.763 ± 0.021 |
| RBF SVM | 0.793 ± 0.012 |
| Boosted trees | 0.794 ± 0.010 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 666.259 ± 1418.950 |
| g, lambda=0.01 | 6.647 ± 4.058 |
| g(K_RBF || K_PQK), lambda=0 | 583.216 ± 1122.945 |
| g_pqk, lambda=0.01 | 7.001 ± 3.663 |
| K_Q off-diagonal mean | 0.163 ± 0.029 |
| K_Q off-diagonal variance | 0.038 ± 0.005 |
| K_PQK off-diagonal variance | 0.028 ± 0.012 |
| K_RBF off-diagonal variance | 0.033 ± 0.010 |
| K_Q effective dimension | 15.550 ± 3.490 |
| AUC gap fidelity QSVM - best classical | -0.032 ± 0.008 |
| AUC gap projected QSVM - best classical | -0.043 ± 0.014 |

boosted-trees implementation: xgboost

## n=6 qubits, N=500, zz map, reps=2, bandwidth=0.25 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.702 ± 0.013 |
| Projected QSVM | 0.681 ± 0.025 |
| Logistic regression | 0.763 ± 0.021 |
| RBF SVM | 0.793 ± 0.012 |
| Boosted trees | 0.794 ± 0.010 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 5476.598 ± 11715.657 |
| g, lambda=0.01 | 8.215 ± 0.428 |
| g(K_RBF || K_PQK), lambda=0 | 4973.301 ± 10579.521 |
| g_pqk, lambda=0.01 | 11.667 ± 1.641 |
| K_Q off-diagonal mean | 0.027 ± 0.006 |
| K_Q off-diagonal variance | 2.88e-03 ± 1.1e-03 |
| K_PQK off-diagonal variance | 0.012 ± 0.005 |
| K_RBF off-diagonal variance | 0.033 ± 0.010 |
| K_Q effective dimension | 186.034 ± 42.282 |
| AUC gap fidelity QSVM - best classical | -0.096 ± 0.013 |
| AUC gap projected QSVM - best classical | -0.117 ± 0.027 |

boosted-trees implementation: xgboost

## n=6 qubits, N=500, zz map, reps=2, bandwidth=0.5 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.553 ± 0.039 |
| Projected QSVM | 0.563 ± 0.014 |
| Logistic regression | 0.763 ± 0.021 |
| RBF SVM | 0.793 ± 0.012 |
| Boosted trees | 0.794 ± 0.010 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 7740.250 ± 16388.133 |
| g, lambda=0.01 | 7.416 ± 1.216 |
| g(K_RBF || K_PQK), lambda=0 | 6539.889 ± 13888.793 |
| g_pqk, lambda=0.01 | 11.255 ± 1.571 |
| K_Q off-diagonal mean | 0.021 ± 0.001 |
| K_Q off-diagonal variance | 9.12e-04 ± 2.0e-04 |
| K_PQK off-diagonal variance | 9.52e-03 ± 7.2e-03 |
| K_RBF off-diagonal variance | 0.033 ± 0.010 |
| K_Q effective dimension | 300.145 ± 22.564 |
| AUC gap fidelity QSVM - best classical | -0.244 ± 0.047 |
| AUC gap projected QSVM - best classical | -0.234 ± 0.018 |

boosted-trees implementation: xgboost

## n=6 qubits, N=500, zz map, reps=2, bandwidth=1.0 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.505 ± 0.024 |
| Projected QSVM | 0.518 ± 0.022 |
| Logistic regression | 0.763 ± 0.021 |
| RBF SVM | 0.793 ± 0.012 |
| Boosted trees | 0.794 ± 0.010 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 8073.538 ± 16997.047 |
| g, lambda=0.01 | 7.064 ± 0.757 |
| g(K_RBF || K_PQK), lambda=0 | 4471.804 ± 9057.538 |
| g_pqk, lambda=0.01 | 12.062 ± 2.902 |
| K_Q off-diagonal mean | 0.020 ± 0.000 |
| K_Q off-diagonal variance | 7.54e-04 ± 3.2e-05 |
| K_PQK off-diagonal variance | 0.011 ± 0.007 |
| K_RBF off-diagonal variance | 0.033 ± 0.010 |
| K_Q effective dimension | 316.686 ± 4.454 |
| AUC gap fidelity QSVM - best classical | -0.292 ± 0.020 |
| AUC gap projected QSVM - best classical | -0.280 ± 0.021 |

boosted-trees implementation: xgboost

## n=8 qubits, N=500, z map, reps=2, bandwidth=0.05 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.792 ± 0.019 |
| Projected QSVM | 0.813 ± 0.014 |
| Logistic regression | 0.765 ± 0.022 |
| RBF SVM | 0.815 ± 0.007 |
| Boosted trees | 0.803 ± 0.017 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 5.210 ± 1.498 |
| g, lambda=0.01 | 4.716 ± 1.808 |
| g(K_RBF || K_PQK), lambda=0 | 39.159 ± 82.951 |
| g_pqk, lambda=0.01 | 2.839 ± 2.583 |
| K_Q off-diagonal mean | 0.969 ± 0.004 |
| K_Q off-diagonal variance | 4.90e-04 ± 6.5e-05 |
| K_PQK off-diagonal variance | 0.031 ± 0.011 |
| K_RBF off-diagonal variance | 0.032 ± 0.011 |
| K_Q effective dimension | 1.065 ± 0.009 |
| AUC gap fidelity QSVM - best classical | -0.025 ± 0.014 |
| AUC gap projected QSVM - best classical | -3.86e-03 ± 1.0e-02 |

boosted-trees implementation: xgboost

## n=8 qubits, N=500, z map, reps=2, bandwidth=0.1 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.816 ± 0.015 |
| Projected QSVM | 0.816 ± 0.009 |
| Logistic regression | 0.765 ± 0.022 |
| RBF SVM | 0.815 ± 0.007 |
| Boosted trees | 0.803 ± 0.017 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 4.529 ± 1.571 |
| g, lambda=0.01 | 4.161 ± 1.757 |
| g(K_RBF || K_PQK), lambda=0 | 47.243 ± 101.645 |
| g_pqk, lambda=0.01 | 2.755 ± 2.666 |
| K_Q off-diagonal mean | 0.884 ± 0.014 |
| K_Q off-diagonal variance | 4.98e-03 ± 6.2e-04 |
| K_PQK off-diagonal variance | 0.033 ± 0.004 |
| K_RBF off-diagonal variance | 0.032 ± 0.011 |
| K_Q effective dimension | 1.272 ± 0.037 |
| AUC gap fidelity QSVM - best classical | -1.32e-03 ± 8.4e-03 |
| AUC gap projected QSVM - best classical | -6.45e-04 ± 3.7e-03 |

boosted-trees implementation: xgboost

## n=8 qubits, N=500, z map, reps=2, bandwidth=0.25 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.813 ± 0.011 |
| Projected QSVM | 0.814 ± 0.008 |
| Logistic regression | 0.765 ± 0.022 |
| RBF SVM | 0.815 ± 0.007 |
| Boosted trees | 0.803 ± 0.017 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 9.335 ± 13.612 |
| g, lambda=0.01 | 3.431 ± 1.141 |
| g(K_RBF || K_PQK), lambda=0 | 96.768 ± 206.827 |
| g_pqk, lambda=0.01 | 3.479 ± 2.755 |
| K_Q off-diagonal mean | 0.509 ± 0.027 |
| K_Q off-diagonal variance | 0.027 ± 0.001 |
| K_PQK off-diagonal variance | 0.023 ± 0.003 |
| K_RBF off-diagonal variance | 0.032 ± 0.011 |
| K_Q effective dimension | 3.495 ± 0.325 |
| AUC gap fidelity QSVM - best classical | -4.33e-03 ± 6.4e-03 |
| AUC gap projected QSVM - best classical | -2.74e-03 ± 5.8e-03 |

boosted-trees implementation: xgboost

## n=8 qubits, N=500, z map, reps=2, bandwidth=0.5 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.801 ± 0.012 |
| Projected QSVM | 0.806 ± 0.015 |
| Logistic regression | 0.765 ± 0.022 |
| RBF SVM | 0.815 ± 0.007 |
| Boosted trees | 0.803 ± 0.017 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 166.475 ± 332.265 |
| g, lambda=0.01 | 5.866 ± 3.403 |
| g(K_RBF || K_PQK), lambda=0 | 67.592 ± 97.766 |
| g_pqk, lambda=0.01 | 5.259 ± 1.895 |
| K_Q off-diagonal mean | 0.121 ± 0.016 |
| K_Q off-diagonal variance | 0.020 ± 0.004 |
| K_PQK off-diagonal variance | 0.014 ± 0.008 |
| K_RBF off-diagonal variance | 0.032 ± 0.011 |
| K_Q effective dimension | 28.007 ± 5.127 |
| AUC gap fidelity QSVM - best classical | -0.016 ± 0.012 |
| AUC gap projected QSVM - best classical | -0.011 ± 0.016 |

boosted-trees implementation: xgboost

## n=8 qubits, N=500, z map, reps=2, bandwidth=1.0 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.707 ± 0.018 |
| Projected QSVM | 0.720 ± 0.016 |
| Logistic regression | 0.765 ± 0.022 |
| RBF SVM | 0.815 ± 0.007 |
| Boosted trees | 0.803 ± 0.017 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 795.302 ± 1558.188 |
| g, lambda=0.01 | 8.478 ± 1.704 |
| g(K_RBF || K_PQK), lambda=0 | 880.410 ± 1785.838 |
| g_pqk, lambda=0.01 | 8.323 ± 1.513 |
| K_Q off-diagonal mean | 0.041 ± 0.009 |
| K_Q off-diagonal variance | 4.78e-03 ± 1.2e-03 |
| K_PQK off-diagonal variance | 7.51e-03 ± 5.1e-03 |
| K_RBF off-diagonal variance | 0.032 ± 0.011 |
| K_Q effective dimension | 123.020 ± 27.418 |
| AUC gap fidelity QSVM - best classical | -0.110 ± 0.012 |
| AUC gap projected QSVM - best classical | -0.097 ± 0.011 |

boosted-trees implementation: xgboost

## n=8 qubits, N=500, zz map, reps=1, bandwidth=0.05 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.804 ± 0.012 |
| Projected QSVM | 0.746 ± 0.020 |
| Logistic regression | 0.765 ± 0.022 |
| RBF SVM | 0.815 ± 0.007 |
| Boosted trees | 0.803 ± 0.017 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 5.164 ± 4.533 |
| g, lambda=0.01 | 3.157 ± 1.058 |
| g(K_RBF || K_PQK), lambda=0 | 13.146 ± 14.664 |
| g_pqk, lambda=0.01 | 4.252 ± 0.906 |
| K_Q off-diagonal mean | 0.593 ± 0.040 |
| K_Q off-diagonal variance | 0.045 ± 0.005 |
| K_PQK off-diagonal variance | 0.036 ± 0.014 |
| K_RBF off-diagonal variance | 0.032 ± 0.011 |
| K_Q effective dimension | 2.529 ± 0.264 |
| AUC gap fidelity QSVM - best classical | -0.013 ± 0.008 |
| AUC gap projected QSVM - best classical | -0.071 ± 0.021 |

boosted-trees implementation: xgboost

## n=8 qubits, N=500, zz map, reps=1, bandwidth=0.1 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.784 ± 0.007 |
| Projected QSVM | 0.741 ± 0.026 |
| Logistic regression | 0.765 ± 0.022 |
| RBF SVM | 0.815 ± 0.007 |
| Boosted trees | 0.803 ± 0.017 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 53.631 ± 101.058 |
| g, lambda=0.01 | 5.224 ± 3.537 |
| g(K_RBF || K_PQK), lambda=0 | 67.489 ± 112.066 |
| g_pqk, lambda=0.01 | 6.471 ± 2.359 |
| K_Q off-diagonal mean | 0.195 ± 0.033 |
| K_Q off-diagonal variance | 0.042 ± 0.005 |
| K_PQK off-diagonal variance | 0.026 ± 0.010 |
| K_RBF off-diagonal variance | 0.032 ± 0.011 |
| K_Q effective dimension | 12.581 ± 2.563 |
| AUC gap fidelity QSVM - best classical | -0.033 ± 0.010 |
| AUC gap projected QSVM - best classical | -0.076 ± 0.027 |

boosted-trees implementation: xgboost

## n=8 qubits, N=500, zz map, reps=1, bandwidth=0.25 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.733 ± 0.008 |
| Projected QSVM | 0.667 ± 0.029 |
| Logistic regression | 0.765 ± 0.022 |
| RBF SVM | 0.815 ± 0.007 |
| Boosted trees | 0.803 ± 0.017 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 715.528 ± 1400.072 |
| g, lambda=0.01 | 7.162 ± 1.140 |
| g(K_RBF || K_PQK), lambda=0 | 1136.329 ± 2405.095 |
| g_pqk, lambda=0.01 | 10.395 ± 2.559 |
| K_Q off-diagonal mean | 0.011 ± 0.003 |
| K_Q off-diagonal variance | 1.88e-03 ± 6.9e-04 |
| K_PQK off-diagonal variance | 0.015 ± 0.007 |
| K_RBF off-diagonal variance | 0.032 ± 0.011 |
| K_Q effective dimension | 255.804 ± 41.506 |
| AUC gap fidelity QSVM - best classical | -0.084 ± 0.007 |
| AUC gap projected QSVM - best classical | -0.150 ± 0.028 |

boosted-trees implementation: xgboost

## n=8 qubits, N=500, zz map, reps=1, bandwidth=0.5 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.550 ± 0.031 |
| Projected QSVM | 0.577 ± 0.027 |
| Logistic regression | 0.765 ± 0.022 |
| RBF SVM | 0.815 ± 0.007 |
| Boosted trees | 0.803 ± 0.017 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 1467.081 ± 2916.813 |
| g, lambda=0.01 | 5.802 ± 0.295 |
| g(K_RBF || K_PQK), lambda=0 | 883.430 ± 1727.673 |
| g_pqk, lambda=0.01 | 13.971 ± 1.901 |
| K_Q off-diagonal mean | 4.15e-03 ± 1.8e-04 |
| K_Q off-diagonal variance | 1.42e-04 ± 4.0e-05 |
| K_PQK off-diagonal variance | 0.015 ± 0.004 |
| K_RBF off-diagonal variance | 0.032 ± 0.011 |
| K_Q effective dimension | 463.337 ± 8.694 |
| AUC gap fidelity QSVM - best classical | -0.267 ± 0.037 |
| AUC gap projected QSVM - best classical | -0.240 ± 0.033 |

boosted-trees implementation: xgboost

## n=8 qubits, N=500, zz map, reps=1, bandwidth=1.0 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.499 ± 0.023 |
| Projected QSVM | 0.523 ± 0.023 |
| Logistic regression | 0.765 ± 0.022 |
| RBF SVM | 0.815 ± 0.007 |
| Boosted trees | 0.803 ± 0.017 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 1784.927 ± 3583.133 |
| g, lambda=0.01 | 5.420 ± 0.126 |
| g(K_RBF || K_PQK), lambda=0 | 1726.061 ± 3466.134 |
| g_pqk, lambda=0.01 | 11.318 ± 1.464 |
| K_Q off-diagonal mean | 3.92e-03 ± 2.2e-05 |
| K_Q off-diagonal variance | 7.12e-05 ± 3.2e-06 |
| K_PQK off-diagonal variance | 4.91e-03 ± 1.0e-03 |
| K_RBF off-diagonal variance | 0.032 ± 0.011 |
| K_Q effective dimension | 479.290 ± 0.767 |
| AUC gap fidelity QSVM - best classical | -0.318 ± 0.017 |
| AUC gap projected QSVM - best classical | -0.294 ± 0.021 |

boosted-trees implementation: xgboost

## n=8 qubits, N=500, zz map, reps=2, bandwidth=0.05 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.796 ± 0.014 |
| Projected QSVM | 0.763 ± 0.010 |
| Logistic regression | 0.765 ± 0.022 |
| RBF SVM | 0.815 ± 0.007 |
| Boosted trees | 0.803 ± 0.017 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 15.150 ± 25.660 |
| g, lambda=0.01 | 3.594 ± 1.595 |
| g(K_RBF || K_PQK), lambda=0 | 12.798 ± 15.267 |
| g_pqk, lambda=0.01 | 3.497 ± 0.559 |
| K_Q off-diagonal mean | 0.413 ± 0.039 |
| K_Q off-diagonal variance | 0.053 ± 0.001 |
| K_PQK off-diagonal variance | 0.051 ± 0.011 |
| K_RBF off-diagonal variance | 0.032 ± 0.011 |
| K_Q effective dimension | 4.494 ± 0.614 |
| AUC gap fidelity QSVM - best classical | -0.021 ± 0.011 |
| AUC gap projected QSVM - best classical | -0.054 ± 0.012 |

boosted-trees implementation: xgboost

## n=8 qubits, N=500, zz map, reps=2, bandwidth=0.1 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.770 ± 0.005 |
| Projected QSVM | 0.759 ± 0.014 |
| Logistic regression | 0.765 ± 0.022 |
| RBF SVM | 0.815 ± 0.007 |
| Boosted trees | 0.803 ± 0.017 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 174.811 ± 334.127 |
| g, lambda=0.01 | 7.086 ± 3.755 |
| g(K_RBF || K_PQK), lambda=0 | 134.348 ± 236.338 |
| g_pqk, lambda=0.01 | 7.341 ± 3.287 |
| K_Q off-diagonal mean | 0.104 ± 0.023 |
| K_Q off-diagonal variance | 0.023 ± 0.005 |
| K_PQK off-diagonal variance | 0.026 ± 0.014 |
| K_RBF off-diagonal variance | 0.032 ± 0.011 |
| K_Q effective dimension | 29.363 ± 7.288 |
| AUC gap fidelity QSVM - best classical | -0.047 ± 0.008 |
| AUC gap projected QSVM - best classical | -0.058 ± 0.014 |

boosted-trees implementation: xgboost

## n=8 qubits, N=500, zz map, reps=2, bandwidth=0.25 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.699 ± 0.007 |
| Projected QSVM | 0.675 ± 0.011 |
| Logistic regression | 0.765 ± 0.022 |
| RBF SVM | 0.815 ± 0.007 |
| Boosted trees | 0.803 ± 0.017 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 996.214 ± 1955.484 |
| g, lambda=0.01 | 6.659 ± 0.481 |
| g(K_RBF || K_PQK), lambda=0 | 1206.613 ± 2445.606 |
| g_pqk, lambda=0.01 | 9.927 ± 2.134 |
| K_Q off-diagonal mean | 8.94e-03 ± 2.6e-03 |
| K_Q off-diagonal variance | 7.63e-04 ± 4.1e-04 |
| K_PQK off-diagonal variance | 7.70e-03 ± 5.5e-03 |
| K_RBF off-diagonal variance | 0.032 ± 0.011 |
| K_Q effective dimension | 357.818 ± 50.823 |
| AUC gap fidelity QSVM - best classical | -0.118 ± 0.009 |
| AUC gap projected QSVM - best classical | -0.142 ± 0.014 |

boosted-trees implementation: xgboost

## n=8 qubits, N=500, zz map, reps=2, bandwidth=0.5 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.556 ± 0.037 |
| Projected QSVM | 0.562 ± 0.008 |
| Logistic regression | 0.765 ± 0.022 |
| RBF SVM | 0.815 ± 0.007 |
| Boosted trees | 0.803 ± 0.017 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 1681.381 ± 3367.056 |
| g, lambda=0.01 | 5.667 ± 0.227 |
| g(K_RBF || K_PQK), lambda=0 | 1679.488 ± 3384.277 |
| g_pqk, lambda=0.01 | 10.271 ± 0.672 |
| K_Q off-diagonal mean | 5.86e-03 ± 3.8e-04 |
| K_Q off-diagonal variance | 1.19e-04 ± 2.3e-05 |
| K_PQK off-diagonal variance | 4.26e-03 ± 3.7e-03 |
| K_RBF off-diagonal variance | 0.032 ± 0.011 |
| K_Q effective dimension | 464.391 ± 5.400 |
| AUC gap fidelity QSVM - best classical | -0.261 ± 0.042 |
| AUC gap projected QSVM - best classical | -0.255 ± 0.011 |

boosted-trees implementation: xgboost

## n=8 qubits, N=500, zz map, reps=2, bandwidth=1.0 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.511 ± 0.019 |
| Projected QSVM | 0.525 ± 0.021 |
| Logistic regression | 0.765 ± 0.022 |
| RBF SVM | 0.815 ± 0.007 |
| Boosted trees | 0.803 ± 0.017 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 1794.328 ± 3601.110 |
| g, lambda=0.01 | 5.508 ± 0.157 |
| g(K_RBF || K_PQK), lambda=0 | 1673.414 ± 3486.860 |
| g_pqk, lambda=0.01 | 9.682 ± 1.318 |
| K_Q off-diagonal mean | 5.41e-03 ± 7.9e-05 |
| K_Q off-diagonal variance | 8.18e-05 ± 3.0e-06 |
| K_PQK off-diagonal variance | 6.19e-03 ± 5.2e-03 |
| K_RBF off-diagonal variance | 0.032 ± 0.011 |
| K_Q effective dimension | 473.733 ± 0.843 |
| AUC gap fidelity QSVM - best classical | -0.306 ± 0.019 |
| AUC gap projected QSVM - best classical | -0.292 ± 0.023 |

boosted-trees implementation: xgboost

## n=10 qubits, N=500, z map, reps=2, bandwidth=0.05 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.804 ± 0.021 |
| Projected QSVM | 0.823 ± 0.012 |
| Logistic regression | 0.778 ± 0.027 |
| RBF SVM | 0.822 ± 0.013 |
| Boosted trees | 0.808 ± 0.016 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 5.142 ± 1.629 |
| g, lambda=0.01 | 4.744 ± 1.825 |
| g(K_RBF || K_PQK), lambda=0 | 3.179 ± 1.676 |
| g_pqk, lambda=0.01 | 1.990 ± 0.515 |
| K_Q off-diagonal mean | 0.963 ± 0.005 |
| K_Q off-diagonal variance | 6.11e-04 ± 5.8e-05 |
| K_PQK off-diagonal variance | 0.029 ± 0.002 |
| K_RBF off-diagonal variance | 0.030 ± 0.010 |
| K_Q effective dimension | 1.077 ± 0.011 |
| AUC gap fidelity QSVM - best classical | -0.019 ± 0.014 |
| AUC gap projected QSVM - best classical | 5.43e-04 ± 5.2e-03 |

boosted-trees implementation: xgboost

## n=10 qubits, N=500, z map, reps=2, bandwidth=0.1 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.824 ± 0.011 |
| Projected QSVM | 0.822 ± 0.011 |
| Logistic regression | 0.778 ± 0.027 |
| RBF SVM | 0.822 ± 0.013 |
| Boosted trees | 0.808 ± 0.016 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 4.379 ± 1.644 |
| g, lambda=0.01 | 4.084 ± 1.761 |
| g(K_RBF || K_PQK), lambda=0 | 7.100 ± 7.848 |
| g_pqk, lambda=0.01 | 2.535 ± 0.766 |
| K_Q off-diagonal mean | 0.865 ± 0.016 |
| K_Q off-diagonal variance | 5.91e-03 ± 6.3e-04 |
| K_PQK off-diagonal variance | 0.028 ± 0.004 |
| K_RBF off-diagonal variance | 0.030 ± 0.010 |
| K_Q effective dimension | 1.327 ± 0.047 |
| AUC gap fidelity QSVM - best classical | 1.99e-03 ± 5.8e-03 |
| AUC gap projected QSVM - best classical | -9.08e-05 ± 5.3e-03 |

boosted-trees implementation: xgboost

## n=10 qubits, N=500, z map, reps=2, bandwidth=0.25 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.820 ± 0.006 |
| Projected QSVM | 0.820 ± 0.007 |
| Logistic regression | 0.778 ± 0.027 |
| RBF SVM | 0.822 ± 0.013 |
| Boosted trees | 0.808 ± 0.016 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 6.323 ± 7.717 |
| g, lambda=0.01 | 3.138 ± 1.305 |
| g(K_RBF || K_PQK), lambda=0 | 31.141 ± 54.139 |
| g_pqk, lambda=0.01 | 3.755 ± 2.092 |
| K_Q off-diagonal mean | 0.454 ± 0.032 |
| K_Q off-diagonal variance | 0.026 ± 0.001 |
| K_PQK off-diagonal variance | 0.020 ± 0.003 |
| K_RBF off-diagonal variance | 0.030 ± 0.010 |
| K_Q effective dimension | 4.317 ± 0.530 |
| AUC gap fidelity QSVM - best classical | -2.14e-03 ± 8.4e-03 |
| AUC gap projected QSVM - best classical | -1.82e-03 ± 8.5e-03 |

boosted-trees implementation: xgboost

## n=10 qubits, N=500, z map, reps=2, bandwidth=0.5 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.802 ± 0.010 |
| Projected QSVM | 0.812 ± 0.017 |
| Logistic regression | 0.778 ± 0.027 |
| RBF SVM | 0.822 ± 0.013 |
| Boosted trees | 0.808 ± 0.016 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 59.518 ± 98.585 |
| g, lambda=0.01 | 5.899 ± 2.638 |
| g(K_RBF || K_PQK), lambda=0 | 69.309 ± 106.424 |
| g_pqk, lambda=0.01 | 6.154 ± 2.619 |
| K_Q off-diagonal mean | 0.087 ± 0.014 |
| K_Q off-diagonal variance | 0.013 ± 0.003 |
| K_PQK off-diagonal variance | 0.013 ± 0.005 |
| K_RBF off-diagonal variance | 0.030 ± 0.010 |
| K_Q effective dimension | 46.317 ± 10.838 |
| AUC gap fidelity QSVM - best classical | -0.020 ± 0.017 |
| AUC gap projected QSVM - best classical | -9.77e-03 ± 1.9e-02 |

boosted-trees implementation: xgboost

## n=10 qubits, N=500, z map, reps=2, bandwidth=1.0 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.718 ± 0.022 |
| Projected QSVM | 0.731 ± 0.019 |
| Logistic regression | 0.778 ± 0.027 |
| RBF SVM | 0.822 ± 0.013 |
| Boosted trees | 0.808 ± 0.016 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 172.984 ± 248.677 |
| g, lambda=0.01 | 7.472 ± 1.252 |
| g(K_RBF || K_PQK), lambda=0 | 178.820 ± 264.446 |
| g_pqk, lambda=0.01 | 7.441 ± 1.303 |
| K_Q off-diagonal mean | 0.020 ± 0.006 |
| K_Q off-diagonal variance | 1.97e-03 ± 6.9e-04 |
| K_PQK off-diagonal variance | 3.04e-03 ± 2.8e-03 |
| K_RBF off-diagonal variance | 0.030 ± 0.010 |
| K_Q effective dimension | 235.417 ± 47.499 |
| AUC gap fidelity QSVM - best classical | -0.104 ± 0.014 |
| AUC gap projected QSVM - best classical | -0.091 ± 0.011 |

boosted-trees implementation: xgboost

## n=10 qubits, N=500, zz map, reps=1, bandwidth=0.05 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.802 ± 0.015 |
| Projected QSVM | 0.747 ± 0.026 |
| Logistic regression | 0.778 ± 0.027 |
| RBF SVM | 0.822 ± 0.013 |
| Boosted trees | 0.808 ± 0.016 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 4.284 ± 3.432 |
| g, lambda=0.01 | 2.894 ± 1.135 |
| g(K_RBF || K_PQK), lambda=0 | 18.766 ± 32.941 |
| g_pqk, lambda=0.01 | 4.566 ± 1.988 |
| K_Q off-diagonal mean | 0.533 ± 0.045 |
| K_Q off-diagonal variance | 0.044 ± 0.004 |
| K_PQK off-diagonal variance | 0.035 ± 0.015 |
| K_RBF off-diagonal variance | 0.030 ± 0.010 |
| K_Q effective dimension | 3.064 ± 0.391 |
| AUC gap fidelity QSVM - best classical | -0.020 ± 0.017 |
| AUC gap projected QSVM - best classical | -0.075 ± 0.022 |

boosted-trees implementation: xgboost

## n=10 qubits, N=500, zz map, reps=1, bandwidth=0.1 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.782 ± 0.012 |
| Projected QSVM | 0.733 ± 0.023 |
| Logistic regression | 0.778 ± 0.027 |
| RBF SVM | 0.822 ± 0.013 |
| Boosted trees | 0.808 ± 0.016 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 30.024 ± 50.832 |
| g, lambda=0.01 | 5.152 ± 2.864 |
| g(K_RBF || K_PQK), lambda=0 | 56.326 ± 105.722 |
| g_pqk, lambda=0.01 | 6.191 ± 3.005 |
| K_Q off-diagonal mean | 0.141 ± 0.032 |
| K_Q off-diagonal variance | 0.028 ± 0.006 |
| K_PQK off-diagonal variance | 0.027 ± 0.010 |
| K_RBF off-diagonal variance | 0.030 ± 0.010 |
| K_Q effective dimension | 20.820 ± 5.346 |
| AUC gap fidelity QSVM - best classical | -0.040 ± 0.016 |
| AUC gap projected QSVM - best classical | -0.090 ± 0.019 |

boosted-trees implementation: xgboost

## n=10 qubits, N=500, zz map, reps=1, bandwidth=0.25 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.720 ± 0.011 |
| Projected QSVM | 0.657 ± 0.034 |
| Logistic regression | 0.778 ± 0.027 |
| RBF SVM | 0.822 ± 0.013 |
| Boosted trees | 0.808 ± 0.016 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 182.863 ± 268.924 |
| g, lambda=0.01 | 6.755 ± 1.027 |
| g(K_RBF || K_PQK), lambda=0 | 141.435 ± 187.756 |
| g_pqk, lambda=0.01 | 11.858 ± 3.165 |
| K_Q off-diagonal mean | 4.51e-03 ± 1.7e-03 |
| K_Q off-diagonal variance | 7.23e-04 ± 3.3e-04 |
| K_PQK off-diagonal variance | 0.017 ± 0.008 |
| K_RBF off-diagonal variance | 0.030 ± 0.010 |
| K_Q effective dimension | 368.740 ± 42.937 |
| AUC gap fidelity QSVM - best classical | -0.102 ± 0.014 |
| AUC gap projected QSVM - best classical | -0.165 ± 0.027 |

boosted-trees implementation: xgboost

## n=10 qubits, N=500, zz map, reps=1, bandwidth=0.5 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.559 ± 0.028 |
| Projected QSVM | 0.582 ± 0.014 |
| Logistic regression | 0.778 ± 0.027 |
| RBF SVM | 0.822 ± 0.013 |
| Boosted trees | 0.808 ± 0.016 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 260.704 ± 331.126 |
| g, lambda=0.01 | 5.402 ± 0.254 |
| g(K_RBF || K_PQK), lambda=0 | 227.848 ± 335.141 |
| g_pqk, lambda=0.01 | 11.645 ± 0.683 |
| K_Q off-diagonal mean | 1.11e-03 ± 7.2e-05 |
| K_Q off-diagonal variance | 3.00e-05 ± 1.5e-05 |
| K_PQK off-diagonal variance | 7.69e-03 ± 6.8e-03 |
| K_RBF off-diagonal variance | 0.030 ± 0.010 |
| K_Q effective dimension | 492.352 ± 3.734 |
| AUC gap fidelity QSVM - best classical | -0.263 ± 0.038 |
| AUC gap projected QSVM - best classical | -0.240 ± 0.027 |

boosted-trees implementation: xgboost

## n=10 qubits, N=500, zz map, reps=1, bandwidth=1.0 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.509 ± 0.014 |
| Projected QSVM | 0.524 ± 0.019 |
| Logistic regression | 0.778 ± 0.027 |
| RBF SVM | 0.822 ± 0.013 |
| Boosted trees | 0.808 ± 0.016 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 276.578 ± 331.091 |
| g, lambda=0.01 | 5.091 ± 0.037 |
| g(K_RBF || K_PQK), lambda=0 | 214.226 ± 231.408 |
| g_pqk, lambda=0.01 | 10.553 ± 1.323 |
| K_Q off-diagonal mean | 9.80e-04 ± 6.0e-06 |
| K_Q off-diagonal variance | 7.06e-06 ± 4.3e-07 |
| K_PQK off-diagonal variance | 4.13e-03 ± 1.2e-03 |
| K_RBF off-diagonal variance | 0.030 ± 0.010 |
| K_Q effective dimension | 498.007 ± 0.108 |
| AUC gap fidelity QSVM - best classical | -0.313 ± 0.017 |
| AUC gap projected QSVM - best classical | -0.298 ± 0.007 |

boosted-trees implementation: xgboost

## n=10 qubits, N=500, zz map, reps=2, bandwidth=0.05 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.794 ± 0.017 |
| Projected QSVM | 0.755 ± 0.014 |
| Logistic regression | 0.778 ± 0.027 |
| RBF SVM | 0.822 ± 0.013 |
| Boosted trees | 0.808 ± 0.016 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 9.597 ± 14.113 |
| g, lambda=0.01 | 3.469 ± 1.760 |
| g(K_RBF || K_PQK), lambda=0 | 13.669 ± 13.347 |
| g_pqk, lambda=0.01 | 4.975 ± 1.394 |
| K_Q off-diagonal mean | 0.348 ± 0.046 |
| K_Q off-diagonal variance | 0.046 ± 0.002 |
| K_PQK off-diagonal variance | 0.031 ± 0.008 |
| K_RBF off-diagonal variance | 0.030 ± 0.010 |
| K_Q effective dimension | 6.051 ± 1.104 |
| AUC gap fidelity QSVM - best classical | -0.028 ± 0.022 |
| AUC gap projected QSVM - best classical | -0.067 ± 0.016 |

boosted-trees implementation: xgboost

## n=10 qubits, N=500, zz map, reps=2, bandwidth=0.1 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.764 ± 0.008 |
| Projected QSVM | 0.753 ± 0.018 |
| Logistic regression | 0.778 ± 0.027 |
| RBF SVM | 0.822 ± 0.013 |
| Boosted trees | 0.808 ± 0.016 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 73.082 ± 118.393 |
| g, lambda=0.01 | 6.687 ± 2.556 |
| g(K_RBF || K_PQK), lambda=0 | 81.655 ± 165.053 |
| g_pqk, lambda=0.01 | 5.895 ± 2.942 |
| K_Q off-diagonal mean | 0.068 ± 0.022 |
| K_Q off-diagonal variance | 0.013 ± 0.004 |
| K_PQK off-diagonal variance | 0.018 ± 0.012 |
| K_RBF off-diagonal variance | 0.030 ± 0.010 |
| K_Q effective dimension | 55.032 ± 17.725 |
| AUC gap fidelity QSVM - best classical | -0.058 ± 0.014 |
| AUC gap projected QSVM - best classical | -0.069 ± 0.020 |

boosted-trees implementation: xgboost

## n=10 qubits, N=500, zz map, reps=2, bandwidth=0.25 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.690 ± 0.015 |
| Projected QSVM | 0.667 ± 0.028 |
| Logistic regression | 0.778 ± 0.027 |
| RBF SVM | 0.822 ± 0.013 |
| Boosted trees | 0.808 ± 0.016 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 217.123 ± 302.342 |
| g, lambda=0.01 | 6.218 ± 0.584 |
| g(K_RBF || K_PQK), lambda=0 | 161.547 ± 239.855 |
| g_pqk, lambda=0.01 | 10.901 ± 2.265 |
| K_Q off-diagonal mean | 3.30e-03 ± 1.3e-03 |
| K_Q off-diagonal variance | 2.68e-04 ± 1.6e-04 |
| K_PQK off-diagonal variance | 0.011 ± 0.001 |
| K_RBF off-diagonal variance | 0.030 ± 0.010 |
| K_Q effective dimension | 440.470 ± 31.748 |
| AUC gap fidelity QSVM - best classical | -0.132 ± 0.009 |
| AUC gap projected QSVM - best classical | -0.155 ± 0.021 |

boosted-trees implementation: xgboost

## n=10 qubits, N=500, zz map, reps=2, bandwidth=0.5 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.560 ± 0.040 |
| Projected QSVM | 0.567 ± 0.017 |
| Logistic regression | 0.778 ± 0.027 |
| RBF SVM | 0.822 ± 0.013 |
| Boosted trees | 0.808 ± 0.016 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 267.481 ± 327.692 |
| g, lambda=0.01 | 5.280 ± 0.149 |
| g(K_RBF || K_PQK), lambda=0 | 253.558 ± 329.309 |
| g_pqk, lambda=0.01 | 10.547 ± 2.137 |
| K_Q off-diagonal mean | 1.52e-03 ± 1.8e-04 |
| K_Q off-diagonal variance | 1.70e-05 ± 8.3e-06 |
| K_PQK off-diagonal variance | 5.59e-03 ± 5.4e-03 |
| K_RBF off-diagonal variance | 0.030 ± 0.010 |
| K_Q effective dimension | 495.221 ± 2.127 |
| AUC gap fidelity QSVM - best classical | -0.262 ± 0.049 |
| AUC gap projected QSVM - best classical | -0.255 ± 0.029 |

boosted-trees implementation: xgboost

## n=10 qubits, N=500, zz map, reps=2, bandwidth=1.0 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.514 ± 0.020 |
| Projected QSVM | 0.524 ± 0.011 |
| Logistic regression | 0.778 ± 0.027 |
| RBF SVM | 0.822 ± 0.013 |
| Boosted trees | 0.808 ± 0.016 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 277.477 ± 331.640 |
| g, lambda=0.01 | 5.099 ± 0.037 |
| g(K_RBF || K_PQK), lambda=0 | 184.762 ± 208.901 |
| g_pqk, lambda=0.01 | 9.463 ± 1.554 |
| K_Q off-diagonal mean | 1.37e-03 ± 5.9e-05 |
| K_Q off-diagonal variance | 8.06e-06 ± 7.6e-07 |
| K_PQK off-diagonal variance | 5.29e-03 ± 3.3e-03 |
| K_RBF off-diagonal variance | 0.030 ± 0.010 |
| K_Q effective dimension | 497.529 ± 0.227 |
| AUC gap fidelity QSVM - best classical | -0.308 ± 0.022 |
| AUC gap projected QSVM - best classical | -0.298 ± 0.007 |

boosted-trees implementation: xgboost
