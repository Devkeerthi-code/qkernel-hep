# Related work

Literature check made on **10 Nov 2026**. BibTeX keys refer to `docs/references.bib`.

**How the search was done.** I used an arXiv-backed paper index (keyword and semantic queries, plus every paper
citing Huang et al. 2021 in its citation graph), general web search, and the arXiv, Crossref and DataCite
records for every bibliographic field. Google Scholar could not be queried: it returned a session-verification
page instead of results. Journal-only papers that are not on arXiv may therefore be missing. Every paper below
was checked against its arXiv or journal record. The descriptions come from abstracts, and also from the full
text for the papers marked **(full text read)**.

**A caution on weight.** Several of the closest results are from 2026 and are **preprints without peer review**,
some by a single author (Shen; Islam; Tekeli; Bhalgami; Bhardwaj & Roy). They agree with each other and with this
project, but treat them as preprints.

## Short answer: has someone already shown that g fails to predict advantage on real data?

**Yes, in part, on non-physics data.** Four groups report that the geometric difference does not track
empirical quantum-vs-classical performance on real datasets:

- **Egginger et al. 2024:** 11 tabular datasets. Good accuracy goes with *small* g, and g grows as predictions
  get worse.
- **Shen 2026:** stock returns. g ≫ 1 throughout, yet the window-level correlation with out-of-sample gain is
  ρ = −0.20.
- **Islam 2026:** power-system attack data. The correlation between g and F1 changes sign from cell to cell
  (−0.82 to +0.63). The author traces this to spectral degeneracy, which g itself tracks, and finds that
  kernel–target alignment predicts accuracy instead.
- **Adams et al. 2026:** materials data. g ≈ 10.7 against RBF, but a third, classical cosine kernel performs
  best.

There is one positive claim, Moradi et al. 2023 (PET radiomics: g > 1 in 9 of the 11 cases where the quantum
model won), with no correlation test. Slattery et al. 2023 and Flórez-Ablan et al. 2025 show that bandwidth-tuned
quantum kernels move geometrically close to classical RBF kernels, which removes the room for advantage that g
measures.

**Not done before, as far as this search found:**

- Any test of the geometric difference, or of Huang et al.'s label-aware criterion, on **collider / HEP data**.
  None of the collider quantum-kernel papers in §2 mentions g in its abstract. The one whose full text I read
  (Bhardwaj & Roy 2026, same dataset) does not tune bandwidth or measure concentration.
- A test of g as a predictor that comes with a written hypothesis, seed-paired significance, bootstrap CIs, and
  checks **within each feature-map family** and **with kernel concentration held fixed** (partial correlation).
- A replication with a second, independent feature reduction (boosted-tree feature selection instead of PCA).

**What this means for the H2 result.** "g fails to predict the gap" is **not a new message in general**. It is
new for physics data, and the controls make it sharper than most prior reports. See §4 for how to frame it.

---

## 1. Geometric difference and the Huang et al. criterion on real or physics data

| Paper | What they did | What they found about g | How this project differs |
|---|---|---|---|
| Huang et al. 2021, *Nat. Commun.* 12, 2631 — [arXiv:2011.01938](https://arxiv.org/abs/2011.01938) `huang2021power` | Introduced g(K_C‖K_Q) and the model complexity s_K(N). Projected quantum kernels beat classical ones on Fashion-MNIST with labels **engineered** from the quantum kernel. | g ≲ √N means classical models are guaranteed competitive. A large g is necessary, not sufficient: s_C vs s_Q must then be compared. g is not claimed to grade the size of the gap. | Natural labels (signal/background), physics data. H2 tests a *correlational* reading of g that is stronger than what Huang et al. claim (see §4). |
| Egginger, Sakhnenko & Lorenz 2024, *Quantum Mach. Intell.* 6, 44 — [arXiv:2310.11891](https://arxiv.org/abs/2310.11891) `egginger2024hyperparameter` **(full text read)** | Hyperparameter study of projected and RDM kernels with a Hamiltonian-evolution feature map on 11 OpenML-style datasets (medical, banknote, phoneme, Fashion-MNIST, …). Gradient-boosting importances for both accuracy and g. | "the t values for which a good performance was achieved correspond to a rather small GD, and as the predictions get worse, the potential for quantum advantage increases." This is qualitative, from marginal plots; no correlation statistic. | Closest methodological precedent, and the same sign as our H2 (g larger where the quantum model is worse). We quantify it (ρ = −0.44 [−0.61, −0.22] at λ = 0.01, 79 configurations), control for concentration, use physics data and AUC against tuned classical baselines. |
| Slattery, Shaydulin, Chakrabarti, Pistoia, Khairy & Wild 2023, *Phys. Rev. A* 107, 062417 — [arXiv:2211.16551](https://arxiv.org/abs/2211.16551) `slattery2023numerical` **(full text read)** | Fidelity kernels (IQP-style and others) on synthetic data, **PLAsTiCC** (astronomical transients) and Fashion-MNIST, with g minimised over a grid of classical kernel bandwidths. | g between the tuned quantum kernel and the best classical kernel **decreases with qubit count**: hyperparameter tuning makes the quantum kernel "behave more classically", removing the possibility of advantage. | They use g as a label-free closeness measure. We test whether g tracks the *achieved* gap, on collider data, with ZZ/Z maps and a bandwidth × qubit × depth grid. |
| Flórez-Ablan, Roth & Schnabel 2025, *Quantum Sci. Technol.* 10, 035051 — [arXiv:2503.05602](https://arxiv.org/abs/2503.05602) `florezablan2025similarity` | Fidelity and projected kernels with IQP, Z and other encodings on PLAsTiCC, kMNIST and hidden-manifold data. Compares bandwidth-tuned kernels with RBF using g and a Frobenius distance. | Optimally tuned quantum kernels "essentially behave like classical RBF kernels". At small bandwidth they approach low-order polynomial kernels. | Explains why our small-c kernels match classical AUC (H1, H4). Our extra result is that g does *not* return to ~1 at small c (H4, second half), which their RBF-similarity picture would lead one to expect. |
| Krunic, Flöther, Seegan, Earnest-Noble & Shehab 2022, *IEEE Trans. Quantum Eng.* 3, 1–11 — [arXiv:2112.06211](https://arxiv.org/abs/2112.06211) `krunic2022ehr` **(full text read)** | Electronic health records (rheumatoid-arthritis persistence), 5–20 features, 200–300 samples, IBM hardware; "empirical quantum advantage" landscapes. | Computed and mapped g between RBF and quantum kernels across the configuration grid ("the first independent application of the geometric difference"), but did not test whether g predicts where the quantum model wins. | We test that relation explicitly. |
| Moradi et al. 2023, *Eur. J. Nucl. Med. Mol. Imaging* 50, 3826–3837 — [doi:10.1007/s00259-023-06362-6](https://doi.org/10.1007/s00259-023-06362-6) `moradi2023pet` | PET radiomics, 18 dataset variants, quantum vs classical ML on simulators and IonQ Aria. | "GDQ scores were ≤ 1.0 in all the 8-feature cases, while they were > 1.0 when QML outperformed CML in 9 out of 11 cases." A *positive* claim, without a correlation test or CI. | The only positive real-data report found. Our test is statistical and points the other way. |
| Adams, Zhu, Steuerman, Kusne & Takeuchi 2026 — [arXiv:2601.11775](https://arxiv.org/abs/2601.11775) `adams2026materials` (preprint) | Gaussian-process active learning on X-ray diffraction data (Fe–Ga–Pd), with the quantum kernel run on IonQ Aria. | g ≈ 10.7 against RBF and s_Q < s_C (≈ 19 vs 37), yet a classical *cosine* kernel performed best. The authors attribute this to the cosine kernel's inductive bias, which the complexity bound does not reflect. | Same lesson from a single comparison; ours comes from a 79-configuration grid with significance tests. |
| Shen 2026 — [arXiv:2607.20168](https://arxiv.org/abs/2607.20168) `shen2026stock` (preprint) | Fidelity and projected kernels vs RBF for Chinese A-share returns, kernel-swap controls, 170 walk-forward windows. | g ≫ 1 throughout (regularised, λ_g = 10⁻⁶) yet "does not predict out-of-sample gains (ρ = −0.20)": a window-level correlation over 60 windows, with no CI reported. | Same conclusion and sign, in finance. We give CIs, within-family and concentration-controlled tests, and several λ. |
| Islam 2026 — [arXiv:2608.15617](https://arxiv.org/abs/2608.15617) `islam2026power` (preprint) | Fidelity-kernel SVMs vs six tuned classical models on the Mississippi State/ORNL power-system attack data (hardware-in-the-loop), across 54 bandwidth configurations. | On engineered labels the quantum win tracks g (r = +0.85, 8 cells). On the **real** labels the correlation between g and F1 "changes sign between cells" (−0.82 to +0.63), because spectral degeneracy, which g tracks (pooled ρ = +0.80), confounds the geometric test: near-constant Gram matrices at small bandwidth, near-identity at large. Kernel–target alignment predicts F1 in every cell (ρ = +0.65 to +0.97). | The closest *mechanistic* match: our H3 finds the same two low-variance regimes (concentrated towards 1/2ⁿ vs near-constant), and the only positive g–gap association we see (λ = 0.1) vanishes once log kernel variance is controlled for. We did not test kernel–target alignment; that is an obvious follow-up. |
| Micah et al. 2026 — [arXiv:2610.09717](https://arxiv.org/abs/2610.09717) `micah2026pareto` (preprint) | One-class SVMs with fidelity and projected kernels on real malware-beaconing traffic, on simulators and IQM Garnet. They choose models on a Pareto front of label-free quality vs g. | The best detector (a fidelity kernel, AUC 0.840) had "a geometric difference too small to certify the gain as quantum". The large-g projected kernel only reached AUC 0.782 vs 0.765. | Unsupervised. Again, large g did not mean better performance. |

Large benchmarks that do **not** compute g, but agree that tuned classical models match or beat quantum
kernels (relevant to H1):

- **Schnabel & Roth 2025**, *Quantum Mach. Intell.* 7, 58 — [arXiv:2409.04406](https://arxiv.org/abs/2409.04406)
  `schnabel2025scrutiny`. 64 datasets, more than 20 000 models. Feature scaling (bandwidth) is the dominant
  hyperparameter, and there is "no clear quantum advantage". They defer the geometric difference to future work.
- **Bowles, Ahmed & Schuld 2024** — [arXiv:2403.07059](https://arxiv.org/abs/2403.07059) `bowles2024better`.
  12 models, 160 datasets. Out-of-the-box classical models win, and removing entanglement often does not hurt.
- **Kakavand, Strohmeyer & Schlotter 2026** — [arXiv:2604.18837](https://arxiv.org/abs/2604.18837)
  `kakavand2026benchmark` (preprint). Nine UCI/OpenML datasets, 970 experiments. None of 29 quantum–classical
  comparisons is significant. They propose a non-linearity gap (ρ = 0.683) instead of g.
- **Bhalgami 2026** — [arXiv:2610.42029](https://arxiv.org/abs/2610.42029) `bhalgami2026empirical` (preprint).
  Bandwidth tuned on the same budget as the RBF γ. Tuned quantum kernels are statistically indistinguishable
  from tuned RBF on four real datasets, and finite sampling costs more accuracy than gate noise.

## 2. Quantum kernels and projected quantum kernels on collider / HEP data

This project's data are the ATLAS Higgs Boson Machine Learning Challenge 2014 events (CERN Open Data record 328,
`atlas2014higgsdata`). The challenge itself is described by Adam-Bourdarios et al. 2015 (PMLR 42:19–55,
`adambourdarios2015higgsml`).

| Paper | What they did | Result | How this project differs |
|---|---|---|---|
| Wu et al. 2021, *Phys. Rev. Research* 3, 033221 — [arXiv:2104.05059](https://arxiv.org/abs/2104.05059) `wu2021qsvm` | QSVM-kernel for the ttH analysis (Higgs production with a top-quark pair), up to 20 qubits and 50 000 events on three simulators; 15 qubits / 100 events on IBM hardware. | "performs as well as its classical counterparts"; hardware approaches the noiseless simulator. | No bandwidth sweep, no g, no concentration analysis. We ask *when* and *why* the kernel matches or loses, not only whether it does. |
| Belis et al. 2021, *EPJ Web Conf.* 251, 03070 — [arXiv:2104.07692](https://arxiv.org/abs/2104.07692) `belis2021higgs` | QSVM and VQC for ttH(bb), with several feature-reduction methods. | Similar or better than classical in specific low-sample cases. | Also studies feature reduction. We add a second reduction as a robustness check of hypothesis verdicts. |
| Heredge, Hill, Hollenberg & Sevior 2021, *Comput. Softw. Big Sci.* 5, 27 — [arXiv:2103.12257](https://arxiv.org/abs/2103.12257) `heredge2021bmeson` | QSVM for continuum suppression in B-meson decays; several encoding circuits; IBM hardware. | Best encoding AUC 0.848 vs 0.793 for the RBF-SVM (simulation); 0.703 on hardware. | A reported quantum win on HEP data, which contrasts with our H1. Differences that could matter: dataset, encoding search, classical tuning. Worth discussing explicitly. |
| Fadol et al. 2024, *Int. J. Mod. Phys. A* 39, 2450007 — [arXiv:2209.12788](https://arxiv.org/abs/2209.12788) `fadol2024cepc` | QSVM-kernel for e⁺e⁻→ZH at CEPC, 6 qubits, IBM and Origin Quantum hardware. | Similar to the classical SVM. | As for Wu et al. |
| Duckett et al. 2024, *Phys. Rev. D* 109, 052002 — [arXiv:2212.07279](https://arxiv.org/abs/2212.07279) `duckett2024tracks` | Quantum-kernel SVM classifying hit triplets for track reconstruction. | Improvement for the innermost detector layers. | Different task (tracking, not event classification). |
| Schuhmacher et al. 2023, *Mach. Learn.: Sci. Technol.* 4, 045031 — [arXiv:2301.10787](https://arxiv.org/abs/2301.10787) `schuhmacher2023bsm` | Classical and quantum SVCs trained on artificially created anomalies, applied to BSM detection. | Both identify realistic BSM events; conditions for a quantum benefit discussed. | Anomaly detection, not a supervised Higgs signal. |
| Belis et al. 2024, *Commun. Phys.* 7, 334 — [arXiv:2301.10780](https://arxiv.org/abs/2301.10780) `belis2024anomaly` | Unsupervised quantum kernel machine and clustering on an autoencoder latent space of LHC events, run on hardware. | A regime where the kernel model "significantly outperforms its classical counterparts", linked to the quantum resources used. | The strongest HEP claim of a quantum-kernel benefit (unsupervised). Not comparable directly with our supervised H1, but should be cited when stating H1. |
| Belis et al. 2024, *Mach. Learn.: Sci. Technol.* 5, 035010 — [arXiv:2402.09524](https://arxiv.org/abs/2402.09524) `belis2024guided`; Odagiu et al. 2025, *Quantum Mach. Intell.* 7, 113 — [arXiv:2512.01509](https://arxiv.org/abs/2512.01509) `odagiu2025reduced` | Higgs identification at the LHC with a dimensionality reduction learned jointly with, or for, the quantum classifier (QSVM in Odagiu et al.). | Learned reductions beat fixed ones; Odagiu et al.'s autoencoder is "40% better than the baseline". | We hold the reduction fixed (PCA, or boosted-tree selection) and vary the kernel geometry instead. |
| Incudini et al. 2026, *IEEE Trans. Emerg. Top. Comput. Intell.* 10, 2210–2219 — [arXiv:2209.11144](https://arxiv.org/abs/2209.11144) `incudini2026automatic` | Automatic search over quantum-kernel circuits, tested on a high-energy-physics problem. | "In the best-case scenario", matches or improves on the hand-designed kernel's test accuracy. | Kernel design, not diagnosis. |
| **Bhardwaj & Roy 2026** — [arXiv:2610.14533](https://arxiv.org/abs/2610.14533) `bhardwaj2026higgs` (preprint) **(full text read)** | **The same ATLAS Higgs ML Challenge dataset.** QSVM (ZZFeatureMap reps 1, full entanglement, exact statevector) and VQC on PCA-4 and PCA-8; training sizes 250–4000; logistic regression, RBF-SVM, random forest and XGBoost baselines; 3 seeds. | The QSVM stays below the best classical models (PCA-4, N = 4000: weighted ROC-AUC 0.853 vs 0.871 for the RBF-SVM). Going from PCA-4 to PCA-8 *hurts* the quantum models and helps tree ensembles. Features are scaled to [0, π] with **no bandwidth sweep**, and g, concentration and noise are not analysed. | The closest paper in data and setup. Their result agrees with our H1, and their PCA-8 drop for the fixed-scale ZZ kernel is what our H3 (concentration at fixed bandwidth) predicts. We add a bandwidth × qubits (2–14) × depth grid, projected kernels, g with four λ, concentration, a noise study, IBM hardware, a feature-selection robustness check and written hypotheses. |
| Maulana 2026 — [arXiv:2601.11937](https://arxiv.org/abs/2601.11937) `maulana2026vqc` (preprint) | VQCs on the same ATLAS dataset, PCA to 4 and 8 qubits. | Accuracy 50.6–56.2%. | Variational, not kernel; cited only to show that the dataset is in use. |
| Billias & Chrisochoides 2026 — [arXiv:2608.27333](https://arxiv.org/abs/2608.27333) `billias2026clas12` (preprint) | QSVC with a 6-qubit ZZFeatureMap on CLAS12 track features, 10⁵ training events on HPC, with a fake-backend noise model. | Highest recall; under noise AUC drops from 0.9985 to 0.9671. | Large-scale engineering; no bandwidth/g analysis. |

Variational (non-kernel) HEP classifiers, for context only: Terashi et al. 2021 `terashi2021event` and Wu et al.
2021 (VQC, *J. Phys. G* 48, 125003) `wu2021vqc`.

**Projected quantum kernels on collider data:** none found in this search. This is a gap the project fills, but
state it with the search-coverage caveat above.

## 3. Exponential concentration and bandwidth in quantum kernels

| Paper | What they did | Relation to this project |
|---|---|---|
| Thanasilp, Wang, Cerezo & Holmes 2024, *Nat. Commun.* 15, 5200 — [arXiv:2208.11060](https://arxiv.org/abs/2208.11060) `thanasilp2024concentration` | Proved that kernel values concentrate exponentially in the number of qubits, from four sources: embedding expressivity, global measurements, entanglement and noise. With polynomially many shots the model becomes input-independent. | The theory behind H3. Our ZZ kernels at c ≥ 0.25 lose 0.27–0.49 decades of off-diagonal variance per qubit and fall to chance; the fidelity kernel is a global measurement. |
| Shaydulin & Wild 2022, *Phys. Rev. A* 106, 042407 — [arXiv:2111.05451](https://arxiv.org/abs/2111.05451) `shaydulin2022bandwidth` | Introduced a bandwidth hyperparameter for quantum kernels and showed "consistent change in the model behavior from underfitting (bandwidth too large) to overfitting (bandwidth too small)". With an optimised bandwidth, performance grows with qubit count and becomes competitive with the best classical methods. | The basis of H4 and of our c grid. (Our c multiplies the features; compare definitions before mapping their "large/small bandwidth" onto our c.) We reproduce their qualitative picture on collider data (small c recovers AUC in 15/15 cells). |
| Canatar, Peters, Pehlevan, Wild & Shaydulin 2023, *TMLR* — [arXiv:2206.06686](https://arxiv.org/abs/2206.06686) `canatar2023bandwidth` | Closed-form large-qubit analysis: bandwidth controls the kernel spectrum and can take a model from no generalisation to good generalisation. | Theory for H4's first half. |
| Kübler, Buchholz & Schölkopf 2021, *NeurIPS* 34 — [arXiv:2106.03747](https://arxiv.org/abs/2106.03747) `kubler2021inductive` | Spectral analysis: an exponentially large RKHS makes generalisation hard; advantage needs an inductive bias that is hard to encode classically. | Explains why a generic ZZ map has no reason to help on Higgs data. |
| Slattery et al. 2023 and Flórez-Ablan et al. 2025 (see §1) | Bandwidth tuning makes quantum kernels approximately classical (RBF, then polynomial). | Consistent with H1 + H4: the configurations that compete with classical models are the near-classical ones. |
| Tekeli 2026 — [arXiv:2608.29422](https://arxiv.org/abs/2608.29422) `tekeli2026zz` (preprint) | Proves that, at small bandwidth, the ZZ-feature-map kernel is to leading order an **anisotropic** Gaussian with metric M = I + π²Q (Q = signless Laplacian of the entanglement graph) under the shifted (π − x) phase convention; under the unshifted convention it is isotropic. | Our code uses Qiskit's (π − x_i)(π − x_j) phases, which appears to be the shifted convention in Tekeli's terms (check before citing). If so, this suggests why g does not return to ~1 at small c (H4): the small-c ZZ kernel approaches an anisotropic Gaussian, not the isotropic tuned RBF used as K_C. A cheap check would be to compute g against Tekeli's surrogate. |
| Wang, Du, Luo & Tao 2021, *Quantum* 5, 531 — [arXiv:2103.16774](https://arxiv.org/abs/2103.16774) `wang2021nisq` | Shot noise and system noise: the advantage of Huang et al. vanishes for large datasets, few measurements and large noise. | Context for our noise study (shot noise costs far more than global depolarising noise). |
| Miroszewski et al. 2024 — [arXiv:2407.15776](https://arxiv.org/abs/2407.15776) `miroszewski2024shots` (preprint) | Rules for the number of shots in fidelity and projected kernels: the "spread" and "concentration" effects. | Relevant to the near-constant low-variance kernels (Z map, small c), which classify well in exact simulation but need many shots to resolve. |
| Peters et al. 2021, *npj Quantum Inf.* 7, 161 — [arXiv:2101.09581](https://arxiv.org/abs/2101.09581) `peters2021highdim` | 17-qubit quantum kernel on Google Sycamore for supernova classification (67-dim physics data). Stresses "shot statistics and mean kernel element size". | An early physics-data kernel on hardware that already treats kernel-value size (concentration) as a design constraint. |
| Kairon, Jäger & Krems 2026, *Phys. Rev. A* 114, 022417 — [arXiv:2501.07433](https://arxiv.org/abs/2501.07433) `kairon2026equivalence` | Formal equivalence between exponential concentration of quantum kernels and barren plateaus. | Background for the H3 discussion. |

---

## 4. What this means for how the contribution is framed

**What the data can and cannot say about Huang et al.** Huang et al. use g as a *necessary condition*: if
g ≲ √N, a classical model is guaranteed competitive. A quantum advantage needs g ≳ √N *and* a favourable
comparison of model complexities. They do not claim that larger g means a larger AUC gap; that graded reading is
the one used in pre-screening practice (Krunic; Moradi; tutorials) and is what H2 tests. On this project's data,
N = 500 and √N ≈ 22.4:

- **Regularised g (λ = 0.01, 0.1):** reaches at most 19.6 and 7.4, so 0 of 79 configurations pass the necessary
  condition. No configuration shows an advantage either (H1 held), which is *consistent* with Huang et al.
- **Unregularised g (λ = 0):** 61 of 79 pass. None shows an advantage (50 classical better, 11 not significant),
  and these are mostly concentrated kernels. Passing is necessary but not sufficient, again consistent with
  Huang et al.
- **The second step (s_C vs s_Q):** vacuous here. Our s is s_K(N)/N, so Huang et al.'s error bound √(s_K(N)/N) equals √s, and with s_C ≥ 4.4 everywhere it exceeds 1.
- **Overall:** the data refute the *graded* use of g (H2 failed: ρ = −0.44 [−0.61, −0.22] at λ = 0.01). They
  cannot refute Huang et al.'s criterion as stated, because there is no advantage for it to predict.

**What not to claim:**

- "First to show g fails on real data": Egginger et al. 2024, Shen 2026, Islam 2026 and Adams et al. 2026 report
  this in other domains.
- "First quantum kernel on Higgs / LHC data": Wu et al. 2021, Belis et al. 2021, Fadol et al. 2024, and Bhardwaj
  & Roy 2026 on the same dataset.
- "Huang et al.'s criterion is wrong": see the point above.

**What the evidence supports claiming:**

1. **First test, as far as this search found, of the geometric difference and the label-aware criterion on
   collider data**, against tuned classical baselines with natural labels.
2. **The test design:** hypotheses written before the experiments; seed-paired significance; bootstrap CIs; the
   correlation checked within each feature-map family and with concentration controlled; and replication under a
   second feature reduction (no verdict changed).
3. **A mechanism, not just a null:**
   - g is *negatively* related to the gap at λ ≤ 0.01, and stays negative with variance controlled (partial
     ρ = −0.66 [−0.75, −0.54]).
   - The positive association at λ = 0.1 (+0.34 pooled; +0.50 and +0.59 within the ZZ maps) disappears once log
     kernel variance is controlled (partial +0.03 pooled; −0.31 and −0.40 within the ZZ maps).
   - Low variance comes in two regimes: concentrated towards 1/2ⁿ (median AUC 0.55) and near-constant (median
     AUC 0.78).
   - This matches Islam 2026's "spectral degeneracy confound" on independent physics data, and links it to the
     concentration theory of Thanasilp et al. 2024.
4. **A practical limit on the label-aware criterion:** at N = 500 the model-complexity bound is vacuous for the
   classical side (s_C ≥ 4.4), so the s_C/s_Q ratio mostly flags memorising kernels rather than advantage.
5. **Noise and hardware on the same pipeline:** shot noise dominates global depolarising noise, and an
   ibm_marrakesh run falls inside the analytic noise model's range.

**A suggested contribution statement:** "On ATLAS H→ττ events, tuned classical baselines match or beat every
quantum kernel we test, and the geometric difference fails as a graded predictor of the quantum–classical gap. It
is anti-correlated with the gap, and its one positive association is explained by kernel concentration. This
extends to collider data recent reports from tabular, financial and power-system data, and identifies
concentration (spectral degeneracy) as the confound."

**Follow-ups the literature suggests (cheap with the existing kernels):**

1. **Kernel–target alignment** as the predictor (Islam 2026 found it works where g fails).
2. **g against an anisotropic Gaussian surrogate** (Tekeli 2026), to see whether the failure of "g → 1 at small c"
   (H4) comes from the isotropic RBF reference.
3. **Shot noise for the near-constant small-c kernels** (Miroszewski et al. 2024), which the noise study did not
   cover.
4. **The Heredge et al. 2021 contrast** (a reported HEP quantum-kernel win), discussed explicitly when stating H1.
