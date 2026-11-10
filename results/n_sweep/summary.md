# n_sweep: mean ± std over seeds (std is the sample std, ddof=1)

## n=4 qubits, N=100, zz map, reps=2, bandwidth=0.1 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.726 ± 0.048 |
| Projected QSVM | 0.723 ± 0.024 |
| Logistic regression | 0.756 ± 0.033 |
| RBF SVM | 0.753 ± 0.038 |
| Boosted trees | 0.730 ± 0.020 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 331.489 ± 476.146 |
| g, lambda=0.01 | 5.460 ± 3.285 |
| g(K_RBF || K_PQK), lambda=0 | 430.331 ± 743.843 |
| g_pqk, lambda=0.01 | 5.008 ± 2.549 |
| K_Q off-diagonal mean | 0.246 ± 0.049 |
| K_Q off-diagonal variance | 0.061 ± 0.008 |
| K_PQK off-diagonal variance | 0.041 ± 0.010 |
| K_RBF off-diagonal variance | 0.038 ± 0.007 |
| K_Q effective dimension | 7.876 ± 1.764 |
| AUC gap fidelity QSVM - best classical | -0.043 ± 0.040 |
| AUC gap projected QSVM - best classical | -0.046 ± 0.027 |

boosted-trees implementation: xgboost

## n=4 qubits, N=100, zz map, reps=2, bandwidth=1.0 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.512 ± 0.011 |
| Projected QSVM | 0.506 ± 0.019 |
| Logistic regression | 0.756 ± 0.033 |
| RBF SVM | 0.753 ± 0.038 |
| Boosted trees | 0.730 ± 0.020 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 3009.288 ± 4118.602 |
| g, lambda=0.01 | 6.566 ± 0.439 |
| g(K_RBF || K_PQK), lambda=0 | 2008.770 ± 2940.137 |
| g_pqk, lambda=0.01 | 5.995 ± 0.838 |
| K_Q off-diagonal mean | 0.077 ± 0.004 |
| K_Q off-diagonal variance | 6.76e-03 ± 7.0e-04 |
| K_PQK off-diagonal variance | 0.012 ± 0.006 |
| K_RBF off-diagonal variance | 0.038 ± 0.007 |
| K_Q effective dimension | 44.423 ± 2.449 |
| AUC gap fidelity QSVM - best classical | -0.257 ± 0.025 |
| AUC gap projected QSVM - best classical | -0.263 ± 0.032 |

boosted-trees implementation: xgboost

## n=4 qubits, N=250, zz map, reps=2, bandwidth=0.1 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.775 ± 0.032 |
| Projected QSVM | 0.757 ± 0.027 |
| Logistic regression | 0.763 ± 0.029 |
| RBF SVM | 0.788 ± 0.025 |
| Boosted trees | 0.774 ± 0.020 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 2545.780 ± 5486.022 |
| g, lambda=0.01 | 7.268 ± 4.403 |
| g(K_RBF || K_PQK), lambda=0 | 948.702 ± 2011.157 |
| g_pqk, lambda=0.01 | 5.023 ± 2.046 |
| K_Q off-diagonal mean | 0.307 ± 0.024 |
| K_Q off-diagonal variance | 0.070 ± 0.002 |
| K_PQK off-diagonal variance | 0.028 ± 0.014 |
| K_RBF off-diagonal variance | 0.047 ± 0.016 |
| K_Q effective dimension | 5.989 ± 0.590 |
| AUC gap fidelity QSVM - best classical | -0.015 ± 0.020 |
| AUC gap projected QSVM - best classical | -0.033 ± 0.012 |

boosted-trees implementation: xgboost

## n=4 qubits, N=250, zz map, reps=2, bandwidth=1.0 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.512 ± 0.015 |
| Projected QSVM | 0.512 ± 0.011 |
| Logistic regression | 0.763 ± 0.029 |
| RBF SVM | 0.788 ± 0.025 |
| Boosted trees | 0.774 ± 0.020 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 30725.135 ± 49437.680 |
| g, lambda=0.01 | 7.926 ± 0.803 |
| g(K_RBF || K_PQK), lambda=0 | 29598.075 ± 55663.583 |
| g_pqk, lambda=0.01 | 8.056 ± 1.891 |
| K_Q off-diagonal mean | 0.077 ± 0.003 |
| K_Q off-diagonal variance | 6.71e-03 ± 5.0e-04 |
| K_PQK off-diagonal variance | 0.011 ± 0.009 |
| K_RBF off-diagonal variance | 0.047 ± 0.016 |
| K_Q effective dimension | 60.593 ± 3.122 |
| AUC gap fidelity QSVM - best classical | -0.278 ± 0.026 |
| AUC gap projected QSVM - best classical | -0.278 ± 0.023 |

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

## n=4 qubits, N=1000, zz map, reps=2, bandwidth=0.1 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.804 ± 0.013 |
| Projected QSVM | 0.799 ± 0.012 |
| Logistic regression | 0.764 ± 0.018 |
| RBF SVM | 0.805 ± 0.015 |
| Boosted trees | 0.804 ± 0.019 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 5799.141 ± 10648.664 |
| g, lambda=0.01 | 9.377 ± 7.367 |
| g(K_RBF || K_PQK), lambda=0 | 2517.653 ± 4506.920 |
| g_pqk, lambda=0.01 | 6.461 ± 3.389 |
| K_Q off-diagonal mean | 0.394 ± 0.057 |
| K_Q off-diagonal variance | 0.074 ± 0.001 |
| K_PQK off-diagonal variance | 0.038 ± 0.016 |
| K_RBF off-diagonal variance | 0.038 ± 0.021 |
| K_Q effective dimension | 4.434 ± 0.849 |
| AUC gap fidelity QSVM - best classical | -4.13e-03 ± 1.4e-02 |
| AUC gap projected QSVM - best classical | -8.32e-03 ± 8.2e-03 |

boosted-trees implementation: xgboost

## n=4 qubits, N=1000, zz map, reps=2, bandwidth=1.0 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.513 ± 0.014 |
| Projected QSVM | 0.520 ± 0.018 |
| Logistic regression | 0.764 ± 0.018 |
| RBF SVM | 0.805 ± 0.015 |
| Boosted trees | 0.804 ± 0.019 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 84840.254 ± 74569.735 |
| g, lambda=0.01 | 11.417 ± 3.473 |
| g(K_RBF || K_PQK), lambda=0 | 93702.958 ± 89540.222 |
| g_pqk, lambda=0.01 | 12.010 ± 4.641 |
| K_Q off-diagonal mean | 0.078 ± 0.002 |
| K_Q off-diagonal variance | 7.01e-03 ± 3.8e-04 |
| K_PQK off-diagonal variance | 0.012 ± 0.006 |
| K_RBF off-diagonal variance | 0.038 ± 0.021 |
| K_Q effective dimension | 70.854 ± 3.543 |
| AUC gap fidelity QSVM - best classical | -0.295 ± 0.020 |
| AUC gap projected QSVM - best classical | -0.288 ± 0.021 |

boosted-trees implementation: xgboost

## n=8 qubits, N=100, zz map, reps=2, bandwidth=0.1 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.715 ± 0.061 |
| Projected QSVM | 0.705 ± 0.050 |
| Logistic regression | 0.770 ± 0.038 |
| RBF SVM | 0.759 ± 0.064 |
| Boosted trees | 0.742 ± 0.032 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 20.644 ± 16.245 |
| g, lambda=0.01 | 4.898 ± 2.100 |
| g(K_RBF || K_PQK), lambda=0 | 9.695 ± 8.097 |
| g_pqk, lambda=0.01 | 3.749 ± 1.374 |
| K_Q off-diagonal mean | 0.050 ± 0.013 |
| K_Q off-diagonal variance | 0.010 ± 0.002 |
| K_PQK off-diagonal variance | 0.014 ± 0.010 |
| K_RBF off-diagonal variance | 0.028 ± 0.012 |
| K_Q effective dimension | 44.775 ± 6.668 |
| AUC gap fidelity QSVM - best classical | -0.063 ± 0.045 |
| AUC gap projected QSVM - best classical | -0.073 ± 0.041 |

boosted-trees implementation: xgboost

## n=8 qubits, N=100, zz map, reps=2, bandwidth=1.0 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.513 ± 0.033 |
| Projected QSVM | 0.524 ± 0.014 |
| Logistic regression | 0.770 ± 0.038 |
| RBF SVM | 0.759 ± 0.064 |
| Boosted trees | 0.742 ± 0.032 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 41.393 ± 32.978 |
| g, lambda=0.01 | 4.622 ± 1.117 |
| g(K_RBF || K_PQK), lambda=0 | 38.037 ± 32.070 |
| g_pqk, lambda=0.01 | 5.693 ± 0.890 |
| K_Q off-diagonal mean | 5.02e-03 ± 3.7e-04 |
| K_Q off-diagonal variance | 7.80e-05 ± 1.8e-05 |
| K_PQK off-diagonal variance | 4.70e-03 ± 3.6e-03 |
| K_RBF off-diagonal variance | 0.028 ± 0.012 |
| K_Q effective dimension | 98.988 ± 0.211 |
| AUC gap fidelity QSVM - best classical | -0.265 ± 0.061 |
| AUC gap projected QSVM - best classical | -0.254 ± 0.045 |

boosted-trees implementation: xgboost

## n=8 qubits, N=250, zz map, reps=2, bandwidth=0.1 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.760 ± 0.016 |
| Projected QSVM | 0.739 ± 0.031 |
| Logistic regression | 0.771 ± 0.029 |
| RBF SVM | 0.796 ± 0.026 |
| Boosted trees | 0.784 ± 0.034 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 13.914 ± 6.123 |
| g, lambda=0.01 | 5.221 ± 1.332 |
| g(K_RBF || K_PQK), lambda=0 | 9.755 ± 4.529 |
| g_pqk, lambda=0.01 | 4.868 ± 1.008 |
| K_Q off-diagonal mean | 0.077 ± 0.022 |
| K_Q off-diagonal variance | 0.017 ± 0.005 |
| K_PQK off-diagonal variance | 0.033 ± 0.005 |
| K_RBF off-diagonal variance | 0.035 ± 0.008 |
| K_Q effective dimension | 40.709 ± 12.998 |
| AUC gap fidelity QSVM - best classical | -0.041 ± 0.008 |
| AUC gap projected QSVM - best classical | -0.062 ± 0.022 |

boosted-trees implementation: xgboost

## n=8 qubits, N=250, zz map, reps=2, bandwidth=1.0 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.491 ± 0.008 |
| Projected QSVM | 0.493 ± 0.017 |
| Logistic regression | 0.771 ± 0.029 |
| RBF SVM | 0.796 ± 0.026 |
| Boosted trees | 0.784 ± 0.034 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 61.361 ± 35.488 |
| g, lambda=0.01 | 5.306 ± 0.140 |
| g(K_RBF || K_PQK), lambda=0 | 45.431 ± 18.271 |
| g_pqk, lambda=0.01 | 8.707 ± 1.529 |
| K_Q off-diagonal mean | 5.25e-03 ± 1.8e-04 |
| K_Q off-diagonal variance | 7.95e-05 ± 7.2e-06 |
| K_PQK off-diagonal variance | 9.44e-03 ± 5.8e-03 |
| K_RBF off-diagonal variance | 0.035 ± 0.008 |
| K_Q effective dimension | 243.508 ± 0.530 |
| AUC gap fidelity QSVM - best classical | -0.310 ± 0.022 |
| AUC gap projected QSVM - best classical | -0.308 ± 0.023 |

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

## n=8 qubits, N=1000, zz map, reps=2, bandwidth=0.1 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.811 ± 0.013 |
| Projected QSVM | 0.794 ± 0.013 |
| Logistic regression | 0.771 ± 0.012 |
| RBF SVM | 0.833 ± 0.010 |
| Boosted trees | 0.831 ± 0.019 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 995.685 ± 2057.641 |
| g, lambda=0.01 | 9.021 ± 4.697 |
| g(K_RBF || K_PQK), lambda=0 | 1084.280 ± 2357.266 |
| g_pqk, lambda=0.01 | 7.892 ± 4.811 |
| K_Q off-diagonal mean | 0.132 ± 0.035 |
| K_Q off-diagonal variance | 0.029 ± 0.007 |
| K_PQK off-diagonal variance | 0.023 ± 0.010 |
| K_RBF off-diagonal variance | 0.029 ± 0.018 |
| K_Q effective dimension | 22.525 ± 7.134 |
| AUC gap fidelity QSVM - best classical | -0.026 ± 0.017 |
| AUC gap projected QSVM - best classical | -0.044 ± 0.013 |

boosted-trees implementation: xgboost

## n=8 qubits, N=1000, zz map, reps=2, bandwidth=1.0 (seeds [0, 1, 2, 3, 4])

| Model | Test AUC |
|---|---|
| Fidelity QSVM | 0.503 ± 0.022 |
| Projected QSVM | 0.518 ± 0.007 |
| Logistic regression | 0.771 ± 0.012 |
| RBF SVM | 0.833 ± 0.010 |
| Boosted trees | 0.831 ± 0.019 |

| Kernel quantity | Value |
|---|---|
| g(K_RBF || K_Q), lambda=0 | 8568.169 ± 16403.547 |
| g, lambda=0.01 | 5.863 ± 0.410 |
| g(K_RBF || K_PQK), lambda=0 | 8711.555 ± 17003.614 |
| g_pqk, lambda=0.01 | 12.869 ± 1.384 |
| K_Q off-diagonal mean | 5.42e-03 ± 2.2e-04 |
| K_Q off-diagonal variance | 8.48e-05 ± 4.4e-06 |
| K_PQK off-diagonal variance | 8.60e-03 ± 5.3e-03 |
| K_RBF off-diagonal variance | 0.029 ± 0.018 |
| K_Q effective dimension | 897.588 ± 5.441 |
| AUC gap fidelity QSVM - best classical | -0.334 ± 0.027 |
| AUC gap projected QSVM - best classical | -0.319 ± 0.015 |

boosted-trees implementation: xgboost
