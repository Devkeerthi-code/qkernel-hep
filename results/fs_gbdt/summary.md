# fs_gbdt: mean ± std over seeds (std is the sample std, ddof=1)

## n=4 qubits, N=500, z map, reps=2, bandwidth=0.05 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.784 ± 0.026 |
| Projected QSVM | 0.814 ± 0.039 |
| Logistic regression | 0.767 ± 0.025 |
| RBF SVM | 0.812 ± 0.039 |
| Boosted trees | 0.822 ± 0.015 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 3.736 ± 2.134 |
| g, lambda=0.01 | 2.912 ± 2.356 |
| g(K_RBF || K_PQK), lambda=0 | 48.893 ± 58.030 |
| g_pqk, lambda=0.01 | 2.601 ± 1.191 |
| K_Q off-diagonal mean | 0.973 ± 0.015 |
| K_Q off-diagonal variance | 6.83e-04 ± 4.8e-04 |
| K_PQK off-diagonal variance | 0.053 ± 0.015 |
| K_RBF off-diagonal variance | 0.032 ± 0.023 |
| K_Q effective dimension | 1.057 ± 0.032 |
| AUC gap fidelity QSVM - best classical | -0.041 ± 0.021 |
| AUC gap projected QSVM - best classical | -0.011 ± 0.023 |

boosted-trees implementation: xgboost

## n=4 qubits, N=500, z map, reps=2, bandwidth=0.1 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.810 ± 0.031 |
| Projected QSVM | 0.812 ± 0.038 |
| Logistic regression | 0.767 ± 0.025 |
| RBF SVM | 0.812 ± 0.039 |
| Boosted trees | 0.822 ± 0.015 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 3.234 ± 2.128 |
| g, lambda=0.01 | 2.631 ± 2.251 |
| g(K_RBF || K_PQK), lambda=0 | 2930.228 ± 6252.729 |
| g_pqk, lambda=0.01 | 5.263 ± 5.349 |
| K_Q off-diagonal mean | 0.906 ± 0.044 |
| K_Q off-diagonal variance | 5.91e-03 ± 3.5e-03 |
| K_PQK off-diagonal variance | 0.048 ± 0.012 |
| K_RBF off-diagonal variance | 0.032 ± 0.023 |
| K_Q effective dimension | 1.214 ± 0.113 |
| AUC gap fidelity QSVM - best classical | -0.015 ± 0.019 |
| AUC gap projected QSVM - best classical | -0.013 ± 0.021 |

boosted-trees implementation: xgboost

## n=4 qubits, N=500, z map, reps=2, bandwidth=0.25 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.818 ± 0.029 |
| Projected QSVM | 0.817 ± 0.029 |
| Logistic regression | 0.767 ± 0.025 |
| RBF SVM | 0.812 ± 0.039 |
| Boosted trees | 0.822 ± 0.015 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 122.490 ± 74.823 |
| g, lambda=0.01 | 5.895 ± 0.555 |
| g(K_RBF || K_PQK), lambda=0 | 1585.276 ± 1240.288 |
| g_pqk, lambda=0.01 | 5.480 ± 2.606 |
| K_Q off-diagonal mean | 0.669 ± 0.058 |
| K_Q off-diagonal variance | 0.031 ± 0.003 |
| K_PQK off-diagonal variance | 0.024 ± 0.013 |
| K_RBF off-diagonal variance | 0.032 ± 0.023 |
| K_Q effective dimension | 2.117 ± 0.355 |
| AUC gap fidelity QSVM - best classical | -6.96e-03 ± 1.4e-02 |
| AUC gap projected QSVM - best classical | -8.49e-03 ± 1.5e-02 |

boosted-trees implementation: xgboost

## n=4 qubits, N=500, z map, reps=2, bandwidth=0.5 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.811 ± 0.031 |
| Projected QSVM | 0.814 ± 0.033 |
| Logistic regression | 0.767 ± 0.025 |
| RBF SVM | 0.812 ± 0.039 |
| Boosted trees | 0.822 ± 0.015 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 9440.135 ± 7115.048 |
| g, lambda=0.01 | 12.960 ± 5.665 |
| g(K_RBF || K_PQK), lambda=0 | 21486.727 ± 29971.951 |
| g_pqk, lambda=0.01 | 10.196 ± 4.128 |
| K_Q off-diagonal mean | 0.319 ± 0.065 |
| K_Q off-diagonal variance | 0.072 ± 0.013 |
| K_PQK off-diagonal variance | 0.025 ± 0.012 |
| K_RBF off-diagonal variance | 0.032 ± 0.023 |
| K_Q effective dimension | 6.024 ± 1.820 |
| AUC gap fidelity QSVM - best classical | -0.014 ± 0.014 |
| AUC gap projected QSVM - best classical | -0.011 ± 0.019 |

boosted-trees implementation: xgboost

## n=4 qubits, N=500, z map, reps=2, bandwidth=1.0 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.750 ± 0.043 |
| Projected QSVM | 0.769 ± 0.032 |
| Logistic regression | 0.767 ± 0.025 |
| RBF SVM | 0.812 ± 0.039 |
| Boosted trees | 0.822 ± 0.015 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 83900.568 ± 51380.124 |
| g, lambda=0.01 | 16.977 ± 7.126 |
| g(K_RBF || K_PQK), lambda=0 | 48492.172 ± 30275.868 |
| g_pqk, lambda=0.01 | 11.390 ± 3.753 |
| K_Q off-diagonal mean | 0.219 ± 0.038 |
| K_Q off-diagonal variance | 0.046 ± 0.009 |
| K_PQK off-diagonal variance | 8.99e-03 ± 1.6e-03 |
| K_RBF off-diagonal variance | 0.032 ± 0.023 |
| K_Q effective dimension | 10.888 ± 2.437 |
| AUC gap fidelity QSVM - best classical | -0.075 ± 0.031 |
| AUC gap projected QSVM - best classical | -0.056 ± 0.019 |

boosted-trees implementation: xgboost

## n=4 qubits, N=500, zz map, reps=1, bandwidth=0.05 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.812 ± 0.025 |
| Projected QSVM | 0.806 ± 0.029 |
| Logistic regression | 0.767 ± 0.025 |
| RBF SVM | 0.812 ± 0.039 |
| Boosted trees | 0.822 ± 0.015 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 15.702 ± 6.032 |
| g, lambda=0.01 | 3.750 ± 0.912 |
| g(K_RBF || K_PQK), lambda=0 | 4496.925 ± 8269.098 |
| g_pqk, lambda=0.01 | 7.944 ± 5.888 |
| K_Q off-diagonal mean | 0.710 ± 0.112 |
| K_Q off-diagonal variance | 0.056 ± 0.023 |
| K_PQK off-diagonal variance | 0.060 ± 0.025 |
| K_RBF off-diagonal variance | 0.032 ± 0.023 |
| K_Q effective dimension | 1.837 ± 0.448 |
| AUC gap fidelity QSVM - best classical | -0.013 ± 0.008 |
| AUC gap projected QSVM - best classical | -0.019 ± 0.014 |

boosted-trees implementation: xgboost

## n=4 qubits, N=500, zz map, reps=1, bandwidth=0.1 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.808 ± 0.032 |
| Projected QSVM | 0.799 ± 0.021 |
| Logistic regression | 0.767 ± 0.025 |
| RBF SVM | 0.812 ± 0.039 |
| Boosted trees | 0.822 ± 0.015 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 1484.089 ± 1187.460 |
| g, lambda=0.01 | 10.731 ± 4.430 |
| g(K_RBF || K_PQK), lambda=0 | 14413.921 ± 11317.338 |
| g_pqk, lambda=0.01 | 12.049 ± 4.654 |
| K_Q off-diagonal mean | 0.403 ± 0.131 |
| K_Q off-diagonal variance | 0.092 ± 0.011 |
| K_PQK off-diagonal variance | 0.065 ± 0.013 |
| K_RBF off-diagonal variance | 0.032 ± 0.023 |
| K_Q effective dimension | 4.238 ± 1.779 |
| AUC gap fidelity QSVM - best classical | -0.017 ± 0.017 |
| AUC gap projected QSVM - best classical | -0.026 ± 0.008 |

boosted-trees implementation: xgboost

## n=4 qubits, N=500, zz map, reps=1, bandwidth=0.25 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.780 ± 0.029 |
| Projected QSVM | 0.730 ± 0.019 |
| Logistic regression | 0.767 ± 0.025 |
| RBF SVM | 0.812 ± 0.039 |
| Boosted trees | 0.822 ± 0.015 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 73588.767 ± 46295.545 |
| g, lambda=0.01 | 16.566 ± 6.357 |
| g(K_RBF || K_PQK), lambda=0 | 127195.384 ± 75364.378 |
| g_pqk, lambda=0.01 | 15.662 ± 3.347 |
| K_Q off-diagonal mean | 0.123 ± 0.029 |
| K_Q off-diagonal variance | 0.036 ± 0.011 |
| K_PQK off-diagonal variance | 0.041 ± 0.009 |
| K_RBF off-diagonal variance | 0.032 ± 0.023 |
| K_Q effective dimension | 20.592 ± 7.412 |
| AUC gap fidelity QSVM - best classical | -0.045 ± 0.024 |
| AUC gap projected QSVM - best classical | -0.095 ± 0.023 |

boosted-trees implementation: xgboost

## n=4 qubits, N=500, zz map, reps=1, bandwidth=0.5 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.677 ± 0.060 |
| Projected QSVM | 0.688 ± 0.026 |
| Logistic regression | 0.767 ± 0.025 |
| RBF SVM | 0.812 ± 0.039 |
| Boosted trees | 0.822 ± 0.015 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 130005.431 ± 73894.670 |
| g, lambda=0.01 | 9.737 ± 1.186 |
| g(K_RBF || K_PQK), lambda=0 | 145671.432 ± 86039.843 |
| g_pqk, lambda=0.01 | 9.898 ± 2.654 |
| K_Q off-diagonal mean | 0.071 ± 0.005 |
| K_Q off-diagonal variance | 0.012 ± 0.002 |
| K_PQK off-diagonal variance | 0.021 ± 0.007 |
| K_RBF off-diagonal variance | 0.032 ± 0.023 |
| K_Q effective dimension | 55.043 ± 9.316 |
| AUC gap fidelity QSVM - best classical | -0.148 ± 0.056 |
| AUC gap projected QSVM - best classical | -0.137 ± 0.014 |

boosted-trees implementation: xgboost

## n=4 qubits, N=500, zz map, reps=1, bandwidth=1.0 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.530 ± 0.036 |
| Projected QSVM | 0.605 ± 0.020 |
| Logistic regression | 0.767 ± 0.025 |
| RBF SVM | 0.812 ± 0.039 |
| Boosted trees | 0.822 ± 0.015 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 119927.646 ± 67471.626 |
| g, lambda=0.01 | 8.104 ± 1.693 |
| g(K_RBF || K_PQK), lambda=0 | 157822.173 ± 89255.467 |
| g_pqk, lambda=0.01 | 9.202 ± 4.821 |
| K_Q off-diagonal mean | 0.063 ± 0.001 |
| K_Q off-diagonal variance | 7.13e-03 ± 5.6e-04 |
| K_PQK off-diagonal variance | 0.019 ± 0.009 |
| K_RBF off-diagonal variance | 0.032 ± 0.023 |
| K_Q effective dimension | 76.532 ± 3.545 |
| AUC gap fidelity QSVM - best classical | -0.295 ± 0.036 |
| AUC gap projected QSVM - best classical | -0.220 ± 0.029 |

boosted-trees implementation: xgboost

## n=4 qubits, N=500, zz map, reps=2, bandwidth=0.05 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.814 ± 0.025 |
| Projected QSVM | 0.811 ± 0.031 |
| Logistic regression | 0.767 ± 0.025 |
| RBF SVM | 0.812 ± 0.039 |
| Boosted trees | 0.822 ± 0.015 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 379.045 ± 294.715 |
| g, lambda=0.01 | 6.858 ± 1.734 |
| g(K_RBF || K_PQK), lambda=0 | 10767.252 ± 21876.536 |
| g_pqk, lambda=0.01 | 8.729 ± 6.773 |
| K_Q off-diagonal mean | 0.612 ± 0.135 |
| K_Q off-diagonal variance | 0.076 ± 0.022 |
| K_PQK off-diagonal variance | 0.068 ± 0.016 |
| K_RBF off-diagonal variance | 0.032 ± 0.023 |
| K_Q effective dimension | 2.333 ± 0.775 |
| AUC gap fidelity QSVM - best classical | -0.011 ± 0.007 |
| AUC gap projected QSVM - best classical | -0.014 ± 0.014 |

boosted-trees implementation: xgboost

## n=4 qubits, N=500, zz map, reps=2, bandwidth=0.1 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.805 ± 0.028 |
| Projected QSVM | 0.798 ± 0.016 |
| Logistic regression | 0.767 ± 0.025 |
| RBF SVM | 0.812 ± 0.039 |
| Boosted trees | 0.822 ± 0.015 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 13223.034 ± 10919.817 |
| g, lambda=0.01 | 13.539 ± 6.027 |
| g(K_RBF || K_PQK), lambda=0 | 16757.105 ± 17250.160 |
| g_pqk, lambda=0.01 | 11.262 ± 4.486 |
| K_Q off-diagonal mean | 0.348 ± 0.111 |
| K_Q off-diagonal variance | 0.074 ± 0.010 |
| K_PQK off-diagonal variance | 0.049 ± 0.021 |
| K_RBF off-diagonal variance | 0.032 ± 0.023 |
| K_Q effective dimension | 5.548 ± 2.315 |
| AUC gap fidelity QSVM - best classical | -0.020 ± 0.016 |
| AUC gap projected QSVM - best classical | -0.027 ± 0.007 |

boosted-trees implementation: xgboost

## n=4 qubits, N=500, zz map, reps=2, bandwidth=0.25 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.756 ± 0.035 |
| Projected QSVM | 0.734 ± 0.019 |
| Logistic regression | 0.767 ± 0.025 |
| RBF SVM | 0.812 ± 0.039 |
| Boosted trees | 0.822 ± 0.015 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 116769.839 ± 66633.457 |
| g, lambda=0.01 | 14.023 ± 3.386 |
| g(K_RBF || K_PQK), lambda=0 | 128731.205 ± 72457.677 |
| g_pqk, lambda=0.01 | 13.413 ± 2.107 |
| K_Q off-diagonal mean | 0.127 ± 0.011 |
| K_Q off-diagonal variance | 0.025 ± 0.004 |
| K_PQK off-diagonal variance | 0.021 ± 0.008 |
| K_RBF off-diagonal variance | 0.032 ± 0.023 |
| K_Q effective dimension | 23.889 ± 4.051 |
| AUC gap fidelity QSVM - best classical | -0.069 ± 0.029 |
| AUC gap projected QSVM - best classical | -0.091 ± 0.015 |

boosted-trees implementation: xgboost

## n=4 qubits, N=500, zz map, reps=2, bandwidth=0.5 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.654 ± 0.032 |
| Projected QSVM | 0.666 ± 0.034 |
| Logistic regression | 0.767 ± 0.025 |
| RBF SVM | 0.812 ± 0.039 |
| Boosted trees | 0.822 ± 0.015 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 121460.943 ± 68439.620 |
| g, lambda=0.01 | 9.109 ± 1.145 |
| g(K_RBF || K_PQK), lambda=0 | 142719.604 ± 80277.465 |
| g_pqk, lambda=0.01 | 9.455 ± 2.271 |
| K_Q off-diagonal mean | 0.083 ± 0.006 |
| K_Q off-diagonal variance | 9.41e-03 ± 1.2e-03 |
| K_PQK off-diagonal variance | 0.015 ± 0.010 |
| K_RBF off-diagonal variance | 0.032 ± 0.023 |
| K_Q effective dimension | 55.243 ± 5.475 |
| AUC gap fidelity QSVM - best classical | -0.171 ± 0.025 |
| AUC gap projected QSVM - best classical | -0.159 ± 0.024 |

boosted-trees implementation: xgboost

## n=4 qubits, N=500, zz map, reps=2, bandwidth=1.0 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.542 ± 0.022 |
| Projected QSVM | 0.572 ± 0.024 |
| Logistic regression | 0.767 ± 0.025 |
| RBF SVM | 0.812 ± 0.039 |
| Boosted trees | 0.822 ± 0.015 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 122122.837 ± 68453.586 |
| g, lambda=0.01 | 7.694 ± 2.614 |
| g(K_RBF || K_PQK), lambda=0 | 144999.438 ± 82024.558 |
| g_pqk, lambda=0.01 | 8.508 ± 3.467 |
| K_Q off-diagonal mean | 0.078 ± 0.005 |
| K_Q off-diagonal variance | 7.23e-03 ± 5.9e-04 |
| K_PQK off-diagonal variance | 0.014 ± 0.006 |
| K_RBF off-diagonal variance | 0.032 ± 0.023 |
| K_Q effective dimension | 65.903 ± 5.092 |
| AUC gap fidelity QSVM - best classical | -0.283 ± 0.025 |
| AUC gap projected QSVM - best classical | -0.253 ± 0.021 |

boosted-trees implementation: xgboost

## n=8 qubits, N=500, z map, reps=2, bandwidth=0.05 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.808 ± 0.026 |
| Projected QSVM | 0.817 ± 0.031 |
| Logistic regression | 0.781 ± 0.027 |
| RBF SVM | 0.816 ± 0.033 |
| Boosted trees | 0.830 ± 0.017 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 3.952 ± 1.092 |
| g, lambda=0.01 | 3.241 ± 1.275 |
| g(K_RBF || K_PQK), lambda=0 | 3.490 ± 2.288 |
| g_pqk, lambda=0.01 | 1.545 ± 0.498 |
| K_Q off-diagonal mean | 0.930 ± 0.011 |
| K_Q off-diagonal variance | 1.87e-03 ± 2.0e-04 |
| K_PQK off-diagonal variance | 0.041 ± 0.018 |
| K_RBF off-diagonal variance | 0.048 ± 0.020 |
| K_Q effective dimension | 1.154 ± 0.027 |
| AUC gap fidelity QSVM - best classical | -0.024 ± 0.015 |
| AUC gap projected QSVM - best classical | -0.014 ± 0.015 |

boosted-trees implementation: xgboost

## n=8 qubits, N=500, z map, reps=2, bandwidth=0.1 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.819 ± 0.033 |
| Projected QSVM | 0.822 ± 0.033 |
| Logistic regression | 0.781 ± 0.027 |
| RBF SVM | 0.816 ± 0.033 |
| Boosted trees | 0.830 ± 0.017 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 3.754 ± 1.125 |
| g, lambda=0.01 | 2.768 ± 0.993 |
| g(K_RBF || K_PQK), lambda=0 | 11.306 ± 17.819 |
| g_pqk, lambda=0.01 | 2.542 ± 1.018 |
| K_Q off-diagonal mean | 0.776 ± 0.034 |
| K_Q off-diagonal variance | 0.013 ± 0.001 |
| K_PQK off-diagonal variance | 0.026 ± 0.015 |
| K_RBF off-diagonal variance | 0.048 ± 0.020 |
| K_Q effective dimension | 1.631 ± 0.132 |
| AUC gap fidelity QSVM - best classical | -0.013 ± 0.017 |
| AUC gap projected QSVM - best classical | -9.20e-03 ± 1.7e-02 |

boosted-trees implementation: xgboost

## n=8 qubits, N=500, z map, reps=2, bandwidth=0.25 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.820 ± 0.028 |
| Projected QSVM | 0.826 ± 0.025 |
| Logistic regression | 0.781 ± 0.027 |
| RBF SVM | 0.816 ± 0.033 |
| Boosted trees | 0.830 ± 0.017 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 132.606 ± 246.526 |
| g, lambda=0.01 | 5.645 ± 3.493 |
| g(K_RBF || K_PQK), lambda=0 | 73.623 ± 106.805 |
| g_pqk, lambda=0.01 | 4.243 ± 1.585 |
| K_Q off-diagonal mean | 0.406 ± 0.073 |
| K_Q off-diagonal variance | 0.032 ± 0.009 |
| K_PQK off-diagonal variance | 0.012 ± 0.009 |
| K_RBF off-diagonal variance | 0.048 ± 0.020 |
| K_Q effective dimension | 5.328 ± 1.421 |
| AUC gap fidelity QSVM - best classical | -0.011 ± 0.015 |
| AUC gap projected QSVM - best classical | -4.89e-03 ± 1.1e-02 |

boosted-trees implementation: xgboost

## n=8 qubits, N=500, z map, reps=2, bandwidth=0.5 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.799 ± 0.038 |
| Projected QSVM | 0.828 ± 0.019 |
| Logistic regression | 0.781 ± 0.027 |
| RBF SVM | 0.816 ± 0.033 |
| Boosted trees | 0.830 ± 0.017 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 1235.761 ± 1715.525 |
| g, lambda=0.01 | 9.821 ± 3.207 |
| g(K_RBF || K_PQK), lambda=0 | 1132.563 ± 1725.655 |
| g_pqk, lambda=0.01 | 6.863 ± 3.120 |
| K_Q off-diagonal mean | 0.101 ± 0.056 |
| K_Q off-diagonal variance | 0.022 ± 0.016 |
| K_PQK off-diagonal variance | 0.012 ± 0.015 |
| K_RBF off-diagonal variance | 0.048 ± 0.020 |
| K_Q effective dimension | 37.681 ± 16.287 |
| AUC gap fidelity QSVM - best classical | -0.032 ± 0.026 |
| AUC gap projected QSVM - best classical | -2.89e-03 ± 1.1e-02 |

boosted-trees implementation: xgboost

## n=8 qubits, N=500, z map, reps=2, bandwidth=1.0 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.755 ± 0.035 |
| Projected QSVM | 0.780 ± 0.017 |
| Logistic regression | 0.781 ± 0.027 |
| RBF SVM | 0.816 ± 0.033 |
| Boosted trees | 0.830 ± 0.017 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 4949.086 ± 6728.002 |
| g, lambda=0.01 | 10.933 ± 1.413 |
| g(K_RBF || K_PQK), lambda=0 | 5308.113 ± 9490.812 |
| g_pqk, lambda=0.01 | 10.748 ± 2.909 |
| K_Q off-diagonal mean | 0.044 ± 0.011 |
| K_Q off-diagonal variance | 6.65e-03 ± 3.1e-03 |
| K_PQK off-diagonal variance | 7.61e-03 ± 4.5e-03 |
| K_RBF off-diagonal variance | 0.048 ± 0.020 |
| K_Q effective dimension | 102.338 ± 27.850 |
| AUC gap fidelity QSVM - best classical | -0.076 ± 0.022 |
| AUC gap projected QSVM - best classical | -0.051 ± 0.012 |

boosted-trees implementation: xgboost

## n=8 qubits, N=500, zz map, reps=1, bandwidth=0.05 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.813 ± 0.031 |
| Projected QSVM | 0.805 ± 0.033 |
| Logistic regression | 0.781 ± 0.027 |
| RBF SVM | 0.816 ± 0.033 |
| Boosted trees | 0.830 ± 0.017 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 37.430 ± 66.968 |
| g, lambda=0.01 | 4.134 ± 2.897 |
| g(K_RBF || K_PQK), lambda=0 | 89.773 ± 159.780 |
| g_pqk, lambda=0.01 | 4.587 ± 2.497 |
| K_Q off-diagonal mean | 0.338 ± 0.058 |
| K_Q off-diagonal variance | 0.079 ± 0.016 |
| K_PQK off-diagonal variance | 0.033 ± 0.011 |
| K_RBF off-diagonal variance | 0.048 ± 0.020 |
| K_Q effective dimension | 5.337 ± 1.238 |
| AUC gap fidelity QSVM - best classical | -0.019 ± 0.015 |
| AUC gap projected QSVM - best classical | -0.026 ± 0.016 |

boosted-trees implementation: xgboost

## n=8 qubits, N=500, zz map, reps=1, bandwidth=0.1 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.804 ± 0.037 |
| Projected QSVM | 0.794 ± 0.027 |
| Logistic regression | 0.781 ± 0.027 |
| RBF SVM | 0.816 ± 0.033 |
| Boosted trees | 0.830 ± 0.017 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 434.971 ± 663.847 |
| g, lambda=0.01 | 8.529 ± 3.411 |
| g(K_RBF || K_PQK), lambda=0 | 488.562 ± 722.952 |
| g_pqk, lambda=0.01 | 9.826 ± 2.636 |
| K_Q off-diagonal mean | 0.094 ± 0.044 |
| K_Q off-diagonal variance | 0.032 ± 0.018 |
| K_PQK off-diagonal variance | 0.030 ± 0.013 |
| K_RBF off-diagonal variance | 0.048 ± 0.020 |
| K_Q effective dimension | 27.934 ± 11.808 |
| AUC gap fidelity QSVM - best classical | -0.028 ± 0.021 |
| AUC gap projected QSVM - best classical | -0.037 ± 0.012 |

boosted-trees implementation: xgboost

## n=8 qubits, N=500, zz map, reps=1, bandwidth=0.25 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.753 ± 0.034 |
| Projected QSVM | 0.679 ± 0.027 |
| Logistic regression | 0.781 ± 0.027 |
| RBF SVM | 0.816 ± 0.033 |
| Boosted trees | 0.830 ± 0.017 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 4523.463 ± 6090.994 |
| g, lambda=0.01 | 7.781 ± 1.317 |
| g(K_RBF || K_PQK), lambda=0 | 7109.536 ± 11561.667 |
| g_pqk, lambda=0.01 | 11.500 ± 1.716 |
| K_Q off-diagonal mean | 0.010 ± 0.005 |
| K_Q off-diagonal variance | 2.00e-03 ± 1.9e-03 |
| K_PQK off-diagonal variance | 0.012 ± 0.010 |
| K_RBF off-diagonal variance | 0.048 ± 0.020 |
| K_Q effective dimension | 278.922 ± 94.442 |
| AUC gap fidelity QSVM - best classical | -0.078 ± 0.018 |
| AUC gap projected QSVM - best classical | -0.152 ± 0.030 |

boosted-trees implementation: xgboost

## n=8 qubits, N=500, zz map, reps=1, bandwidth=0.5 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.593 ± 0.033 |
| Projected QSVM | 0.661 ± 0.056 |
| Logistic regression | 0.781 ± 0.027 |
| RBF SVM | 0.816 ± 0.033 |
| Boosted trees | 0.830 ± 0.017 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 10329.078 ± 16927.773 |
| g, lambda=0.01 | 5.768 ± 0.348 |
| g(K_RBF || K_PQK), lambda=0 | 9335.424 ± 15851.036 |
| g_pqk, lambda=0.01 | 13.940 ± 2.843 |
| K_Q off-diagonal mean | 4.33e-03 ± 4.1e-04 |
| K_Q off-diagonal variance | 1.92e-04 ± 9.3e-05 |
| K_PQK off-diagonal variance | 0.017 ± 0.008 |
| K_RBF off-diagonal variance | 0.048 ± 0.020 |
| K_Q effective dimension | 453.021 ± 18.952 |
| AUC gap fidelity QSVM - best classical | -0.239 ± 0.028 |
| AUC gap projected QSVM - best classical | -0.170 ± 0.061 |

boosted-trees implementation: xgboost

## n=8 qubits, N=500, zz map, reps=1, bandwidth=1.0 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.544 ± 0.022 |
| Projected QSVM | 0.579 ± 0.028 |
| Logistic regression | 0.781 ± 0.027 |
| RBF SVM | 0.816 ± 0.033 |
| Boosted trees | 0.830 ± 0.017 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 13879.201 ± 24558.935 |
| g, lambda=0.01 | 5.424 ± 0.153 |
| g(K_RBF || K_PQK), lambda=0 | 8807.868 ± 14067.087 |
| g_pqk, lambda=0.01 | 11.856 ± 3.003 |
| K_Q off-diagonal mean | 4.12e-03 ± 1.2e-04 |
| K_Q off-diagonal variance | 9.42e-05 ± 1.1e-05 |
| K_PQK off-diagonal variance | 0.013 ± 0.008 |
| K_RBF off-diagonal variance | 0.048 ± 0.020 |
| K_Q effective dimension | 473.743 ± 2.545 |
| AUC gap fidelity QSVM - best classical | -0.287 ± 0.022 |
| AUC gap projected QSVM - best classical | -0.252 ± 0.032 |

boosted-trees implementation: xgboost

## n=8 qubits, N=500, zz map, reps=2, bandwidth=0.05 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.810 ± 0.036 |
| Projected QSVM | 0.814 ± 0.031 |
| Logistic regression | 0.781 ± 0.027 |
| RBF SVM | 0.816 ± 0.033 |
| Boosted trees | 0.830 ± 0.017 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 132.419 ± 219.438 |
| g, lambda=0.01 | 5.824 ± 3.601 |
| g(K_RBF || K_PQK), lambda=0 | 210.042 ± 417.878 |
| g_pqk, lambda=0.01 | 4.780 ± 2.979 |
| K_Q off-diagonal mean | 0.226 ± 0.056 |
| K_Q off-diagonal variance | 0.067 ± 0.021 |
| K_PQK off-diagonal variance | 0.037 ± 0.015 |
| K_RBF off-diagonal variance | 0.048 ± 0.020 |
| K_Q effective dimension | 8.988 ± 2.662 |
| AUC gap fidelity QSVM - best classical | -0.021 ± 0.020 |
| AUC gap projected QSVM - best classical | -0.017 ± 0.015 |

boosted-trees implementation: xgboost

## n=8 qubits, N=500, zz map, reps=2, bandwidth=0.1 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.802 ± 0.036 |
| Projected QSVM | 0.802 ± 0.021 |
| Logistic regression | 0.781 ± 0.027 |
| RBF SVM | 0.816 ± 0.033 |
| Boosted trees | 0.830 ± 0.017 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 1010.767 ± 1279.251 |
| g, lambda=0.01 | 9.161 ± 2.073 |
| g(K_RBF || K_PQK), lambda=0 | 1245.961 ± 1633.885 |
| g_pqk, lambda=0.01 | 9.273 ± 3.565 |
| K_Q off-diagonal mean | 0.062 ± 0.034 |
| K_Q off-diagonal variance | 0.018 ± 0.013 |
| K_PQK off-diagonal variance | 0.026 ± 0.010 |
| K_RBF off-diagonal variance | 0.048 ± 0.020 |
| K_Q effective dimension | 53.705 ± 26.679 |
| AUC gap fidelity QSVM - best classical | -0.029 ± 0.019 |
| AUC gap projected QSVM - best classical | -0.029 ± 0.005 |

boosted-trees implementation: xgboost

## n=8 qubits, N=500, zz map, reps=2, bandwidth=0.25 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.722 ± 0.041 |
| Projected QSVM | 0.708 ± 0.024 |
| Logistic regression | 0.781 ± 0.027 |
| RBF SVM | 0.816 ± 0.033 |
| Boosted trees | 0.830 ± 0.017 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 7358.668 ± 11311.228 |
| g, lambda=0.01 | 7.227 ± 0.878 |
| g(K_RBF || K_PQK), lambda=0 | 7944.807 ± 12878.800 |
| g_pqk, lambda=0.01 | 12.194 ± 2.921 |
| K_Q off-diagonal mean | 0.011 ± 0.003 |
| K_Q off-diagonal variance | 9.51e-04 ± 7.4e-04 |
| K_PQK off-diagonal variance | 0.011 ± 0.007 |
| K_RBF off-diagonal variance | 0.048 ± 0.020 |
| K_Q effective dimension | 340.284 ± 73.499 |
| AUC gap fidelity QSVM - best classical | -0.109 ± 0.028 |
| AUC gap projected QSVM - best classical | -0.124 ± 0.032 |

boosted-trees implementation: xgboost

## n=8 qubits, N=500, zz map, reps=2, bandwidth=0.5 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.606 ± 0.036 |
| Projected QSVM | 0.628 ± 0.039 |
| Logistic regression | 0.781 ± 0.027 |
| RBF SVM | 0.816 ± 0.033 |
| Boosted trees | 0.830 ± 0.017 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 11239.281 ± 18782.032 |
| g, lambda=0.01 | 5.648 ± 0.280 |
| g(K_RBF || K_PQK), lambda=0 | 10230.532 ± 17462.398 |
| g_pqk, lambda=0.01 | 11.199 ± 2.086 |
| K_Q off-diagonal mean | 5.55e-03 ± 2.9e-04 |
| K_Q off-diagonal variance | 1.27e-04 ± 3.5e-05 |
| K_PQK off-diagonal variance | 0.012 ± 0.005 |
| K_RBF off-diagonal variance | 0.048 ± 0.020 |
| K_Q effective dimension | 463.498 ± 7.669 |
| AUC gap fidelity QSVM - best classical | -0.226 ± 0.034 |
| AUC gap projected QSVM - best classical | -0.203 ± 0.036 |

boosted-trees implementation: xgboost

## n=8 qubits, N=500, zz map, reps=2, bandwidth=1.0 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.553 ± 0.026 |
| Projected QSVM | 0.565 ± 0.037 |
| Logistic regression | 0.781 ± 0.027 |
| RBF SVM | 0.816 ± 0.033 |
| Boosted trees | 0.830 ± 0.017 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 14021.171 ± 24839.216 |
| g, lambda=0.01 | 5.484 ± 0.219 |
| g(K_RBF || K_PQK), lambda=0 | 10005.658 ± 18363.691 |
| g_pqk, lambda=0.01 | 9.202 ± 2.148 |
| K_Q off-diagonal mean | 5.58e-03 ± 3.1e-04 |
| K_Q off-diagonal variance | 1.01e-04 ± 1.5e-05 |
| K_PQK off-diagonal variance | 8.01e-03 ± 5.1e-03 |
| K_RBF off-diagonal variance | 0.048 ± 0.020 |
| K_Q effective dimension | 469.149 ± 3.888 |
| AUC gap fidelity QSVM - best classical | -0.279 ± 0.024 |
| AUC gap projected QSVM - best classical | -0.266 ± 0.036 |

boosted-trees implementation: xgboost
