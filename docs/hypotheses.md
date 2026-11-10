# Hypotheses

Written in the project guide on **7 Nov 2026**, before any experiment was run. They were not formally
pre-registered (no timestamped entry in a public registry). Reproduced verbatim:

> **H1:** The tuned classical baselines match or beat every quantum kernel on this data.
> Test: AUC with error bars across all configurations.
>
> **H2:** Geometric difference correlates positively with the quantum-minus-classical AUC gap.
> Test: Spearman correlation across configurations, with a confidence interval.
>
> **H3:** As qubits and depth grow at fixed bandwidth, concentration rises and AUC falls.
> Test: plot variance and AUC against qubit count.
>
> **H4:** Reducing bandwidth c reduces concentration and recovers performance, while pulling g
> back toward 1. Test: sweep c at fixed qubits; plot g, variance and AUC together.

## Where they are tested

`scripts/make_figures.py` (also run by `notebooks/02_analysis.ipynb`) evaluates each hypothesis with
exactly these definitions and writes the verdicts, with the numbers behind them, to
`results/h2_analysis.json` (key `verdicts`). Figures: H1 Fig. 1, H2 Fig. 2, H3 Fig. 3 and 5,
H4 Fig. 4, noise Fig. 6, robustness to the feature reduction (PCA vs boosted-tree feature selection,
`configs/fs_gbdt.yaml`) Fig. 7.

Operational choices made when testing (not part of the hypotheses above):

- *Significant* means the seed-paired mean difference exceeds its seed-to-seed standard deviation
  (5 seeds); a correlation is significant when its 95% bootstrap CI over configurations excludes 0.
- "Concentration" is measured by the off-diagonal variance of the training kernel matrix.
- g is reported unregularised (lambda = 0) and regularised (lambda = 1e-3, 1e-2, 1e-1); the
  headline uses lambda = 0.01, the regularised g plotted in Fig. 4, and the other values are listed
  next to it.
