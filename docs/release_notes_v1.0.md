qkernel-hep v1.0: the first complete release of the code, results and report for testing whether the geometric
difference of Huang et al. (2021) predicts when a quantum kernel helps on ATLAS H→ττ events.

**Results** (four hypotheses written before the experiments, [docs/hypotheses.md](docs/hypotheses.md)):

- **H1 held.** Tuned classical baselines match or beat every quantum kernel. In 0 of 79 configurations does a
  fidelity or projected kernel beat the best classical model by more than the seed spread.
- **H2 failed.** Spearman ρ between g and the quantum-minus-classical AUC gap is −0.44 [−0.61, −0.22] for the
  regularised g (λ = 0.01), the wrong sign. This is consistent with Huang et al.'s necessary condition: the
  regularised g never exceeds √N = 22.4. What fails is the graded use of g as a pre-screen.
- **H3 and H4 held only in part.** Concentration rises with qubits only for the entangling map at larger
  bandwidths. A smaller bandwidth recovers AUC but does not pull g back towards 1.
- **Robustness.** Replacing PCA with boosted-tree feature selection changes no verdict.
- **Hardware.** On ibm_marrakesh the fidelity-kernel AUC is 0.681 against 0.722 exact, on 24 test events.

No quantum advantage is claimed.

**Included:**

- Library (`src/`), experiment configs, all committed results, figures 1–8.
- The 8-page report (`report/main.pdf`, attached), with a script that checks every number in it against `results/`.
- Literature review and bibliography (`docs/`), and tests run in CI.

**Reproduce Figure 1 in a few minutes:** see the README quick start
(`pip install -r requirements-figures.txt`, then `python scripts/make_figures.py --fig 1`).
