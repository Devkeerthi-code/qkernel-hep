# Number check of report/main.pdf against results/

- Numbers found in the body text of the PDF: **459** (242 with decimals, 217 integers)
- Matched to a value in results/ at the displayed precision: **459** (242 of 242 decimals; integer matches are weak evidence on their own, so the key counts are also recounted independently below)
- Not found in results/: **0** (listed below; each needs a reason)
- Independent recount of key counts and the headline rho: **OK**
- Hypotheses quoted verbatim from docs/hypotheses.md: **OK**

## Numbers in the PDF not found in results/

| number | context |
|---|---|

## Numbers typed literally in main.tex (not from numbers.tex)

These are grid values (n, r, c, lambda), formula constants, method constants (5-fold CV, the 10^-10 Qiskit cross-check, the 95% / 5-95% interval levels, the 1-sd rule's t = 2.2 and p = 0.09, the 10^-3 / 0.1 / 0.5 regime thresholds of the H3 analysis, the -999 placeholder) and dates. 'in results/' only says that the same value occurs somewhere in results/: for grid values it confirms the value, for constants such as 2.2 or 0.09 the match is a coincidence.

| line | number | in results/ | context |
|---|---|---|---|
| 20 | 1 | yes | \newcommand{\verdict}[1]{\textbf{Verdict: #1.}} |
| 20 | 1 | yes | \newcommand{\verdict}[1]{\textbf{Verdict: #1.}} |
| 28 | 10 | yes | \date{10 November 2026} |
| 28 | 2026 | yes | \date{10 November 2026} |
| 40 | 0.01 | yes | regularised $g$ ($\lambda=0.01$), the wrong sign. This |
| 44 | 1 | yes | but $g$ does not return towards~1. Boosted-tree feature se |
| 68 | 7 | yes | efore the experiments (in the project guide, 7~November~2026; not forma |
| 68 | 2026 | yes | xperiments (in the project guide, 7~November~2026; not formally pre-regist |
| 76 | 0 | yes | , the fidelity kernel is $K_Q(x,x')=/\langle 0/U(x')^\dagger U(x)/0\ran |
| 76 | 0 | yes | is $K_Q(x,x')=/\langle 0/U(x')^\dagger U(x)/0\rangle/^2$. |
| 76 | 2 | yes | ,x')=/\langle 0/U(x')^\dagger U(x)/0\rangle/^2$. |
| 78 | 2 | yes | \big(-\gamma\sum_k\/\rho_k(x)-\rho_k(x')\/_F^2\big)$. We use Qiskit's Z |
| 79 | 2 | yes | pplies Hadamards and then a diagonal phase: $2x_i$ on qubit $i$, |
| 80 | 2 | yes | and for the ZZ map $2(\pi-x_i)(\pi-x_j)$ on ne |
| 84 | 1 | yes | et al.\ define $\gC=\sqrt{\/\sqrt{K_Q}K_C^{-1}\sqrt{K_Q}\/_\infty}$, |
| 85 | 1 | yes | norm. A regularised version replaces $K_C^{-1}$ by |
| 86 | 2 | yes | $K_C(K_C+\lambda I)^{-2}$~. In their argument, $ |
| 87 | 2 | yes | $s_C\le g^2 s_Q$. A quantum advantag |
| 89 | 1 | yes | \top K\alpha/N$ with $\alpha=(K+\lambda I)^{-1}y$, which equals |
| 102 | 999 | yes | the features that are always defined (no $-999$ placeholder), |
| 111 | 2 | yes | s $n\in\{ \}$, three feature maps (Z with $r=2$; ZZ with $r=1$ and |
| 111 | 1 | yes | three feature maps (Z with $r=2$; ZZ with $r=1$ and |
| 112 | 2 | yes | $r=2$), $c\in\{ \}$ and see |
| 113 | 2 | yes | for ZZ, $r=2$ with $c\in\{ \}$ ( run |
| 116 | 10 | yes | simulation, cross-checked against Qiskit to $10^{-10}$. |
| 116 | 10 | yes | ation, cross-checked against Qiskit to $10^{-10}$. |
| 119 | 5 | yes | $C$ tuned by stratified 5-fold cross-validation (C |
| 123 | 0 | yes | $\lambda\in\{0, \}$; the headline uses |
| 123 | 0.01 | yes | ambda\in\{0, \}$; the headline uses $\lambda=0.01$. |
| 126 | 2.2 | yes | s is a lenient rule: roughly a paired $t$ of 2.2, $p\approx0.09$. Correla |
| 126 | 0.09 | yes | rule: roughly a paired $t$ of 2.2, $p\approx0.09$. Correlations |
| 127 | 95 | yes | rman's $\rho$ over configuration means, with 95\% percentile-bootstrap i |
| 139 | 1 | yes | ers performance, while pulling g back toward 1. Test: |
| 158 | 2 | yes | classical AUC rises from at $n=2$ to at $n=10$. The Z m |
| 158 | 10 | yes | assical AUC rises from at $n=2$ to at $n=10$. The Z map tracks it ( |
| 159 | 10 | yes | $n=10$, gap ). The ZZ maps fa |
| 160 | 10 | yes | at $n=10$ and at $n=14$ for $r= |
| 160 | 14 | yes | at $n=10$ and at $n=14$ for $r=2$). \verdict{ |
| 160 | 2 | yes | at $n=10$ and at $n=14$ for $r=2$). \verdict{ held} |
| 166 | 95 | yes | off-diagonal variance; Spearman $\rho$ with 95\% bootstrap interval abo |
| 170 | 3 | yes | \centering\footnotesize {3. } |
| 171 | 95 | yes | $g$ and the AUC gap across configurations (95\% bootstrap intervals). |
| 172 | 0 | yes | predicts $\rho>0$.} |
| 176 | 0 | yes | & $\lambda=0$ & $\lambda=0.001$ & $\l |
| 176 | 0.001 | yes | & $\lambda=0$ & $\lambda=0.001$ & $\lambda=0.01$ & $\la |
| 176 | 0.01 | yes | & $\lambda=0$ & $\lambda=0.001$ & $\lambda=0.01$ & $\lambda=0.1$\\ |
| 176 | 0.1 | yes | $\lambda=0.001$ & $\lambda=0.01$ & $\lambda=0.1$\\ |
| 180 | 2 | yes | within Z, $r=2$ & & & & \\ |
| 181 | 1 | yes | within ZZ, $r=1$ & & & & \\ |
| 182 | 2 | yes | within ZZ, $r=2$ & & & & \\ |
| 186 | 0.01 | yes | . For the headline regularised $g$ ($\lambda=0.01$), |
| 187 | 0 | yes | \emph{negative}. The same holds at $\lambda=0$ and $0.001$. Only $\lam |
| 187 | 0.001 | yes | egative}. The same holds at $\lambda=0$ and $0.001$. Only $\lambda=0.1$ |
| 187 | 0.1 | yes | ds at $\lambda=0$ and $0.001$. Only $\lambda=0.1$ |
| 189 | 0.1 | yes | ZZ maps the partial correlations at $\lambda=0.1$ are |
| 192 | 1 | yes | nfiguration, so the bound $\sqrt{s}$ exceeds 1 and is vacuous. |
| 193 | 1 | yes | Concentrated kernels get $s_Q$ near 1 because they memorise th |
| 196 | 0.01 | yes | it: the maxima are ($\lambda=0.01$) and ($\lambda=0.1$), |
| 196 | 0.1 | yes | axima are ($\lambda=0.01$) and ($\lambda=0.1$), so |
| 212 | 0.25 | yes | at $c\ge0.25$, the variance falls by |
| 212 | 2 | yes | falls by -- decades per qubit. For ZZ, $r=2$, $c=1$ it drops |
| 212 | 1 | yes | by -- decades per qubit. For ZZ, $r=2$, $c=1$ it drops |
| 213 | 2 | yes | from at $n=2$ to at $n=14$, while t |
| 213 | 14 | yes | from at $n=2$ to at $n=14$, while the AUC is alrea |
| 216 | 2 | yes | Over matched (n, c) cells, ZZ with $r=2$ is more concentrated th |
| 216 | 1 | yes | , ZZ with $r=2$ is more concentrated than $r=1$ in |
| 219 | 10 | yes | ct failure. Concentrated kernels (variance $<10^{-3}$, off-diagonal mean |
| 219 | 3 | yes | ilure. Concentrated kernels (variance $<10^{-3}$, off-diagonal mean $<0 |
| 219 | 0.1 | yes | ls (variance $<10^{-3}$, off-diagonal mean $<0.1$; |
| 221 | 10 | yes | (variance $<10^{-3}$, mean $>0.5$; co |
| 221 | 3 | yes | (variance $<10^{-3}$, mean $>0.5$; config |
| 221 | 0.5 | yes | (variance $<10^{-3}$, mean $>0.5$; configurations, all |
| 228 | 0.01 | yes | \caption{Regularised $g$ ($\lambda=0.01$), $ $ off-diagonal vari |
| 229 | 4 | yes | $c$ at $n=4$ (top) and $n=8$ (bottom |
| 229 | 8 | yes | $c$ at $n=4$ (top) and $n=8$ (bottom); the grey band |
| 234 | 2 | yes | cells; for example, ZZ with $r=2$ at $n=8$ goes from to |
| 234 | 8 | yes | cells; for example, ZZ with $r=2$ at $n=8$ goes from to . A sma |
| 236 | 2 | yes | $n=2$, the kernel flattens to |
| 237 | 0.01 | yes | } For the headline regularised $g$ ($\lambda=0.01$), $g$ falls |
| 238 | 1 | yes | steadily towards 1 as $c$ shrinks in only |
| 240 | 2 | yes | For ZZ, $r=2$, $n=8$ it goes at $c= |
| 240 | 8 | yes | For ZZ, $r=2$, $n=8$ it goes at $c=1$, max |
| 240 | 1 | yes | For ZZ, $r=2$, $n=8$ it goes at $c=1$, maximum at $c= $, then |
| 241 | 0 | yes | at $c= $. The unregularised $g$ ($\lambda=0$) behaves differently. I |
| 241 | 1 | yes | bda=0$) behaves differently. It is closer to 1 at |
| 243 | 1 | yes | -- at $c=1$ to -- at $c= $. It mo |
| 244 | 1 | yes | towards 1 without getting there. \ |
| 245 | 4 | yes | $n\ge4$, for concentration. The |
| 251 | 0.01 | yes | y-kernel AUC, $ $ variance and $g$ ($\lambda=0.01$) against $c$ at $n=4$ a |
| 251 | 4 | yes | e and $g$ ($\lambda=0.01$) against $c$ at $n=4$ and $n=8$, for PCA |
| 251 | 8 | yes | ($\lambda=0.01$) against $c$ at $n=4$ and $n=8$, for PCA |
| 257 | 4 | yes | of 4 verdicts are unchanged ( |
| 260 | 4 | yes | moves from to ($n=4$) and from to ($n=8$ |
| 260 | 8 | yes | oves from to ($n=4$) and from to ($n=8$). The |
| 266 | 0.01 | yes | xtbf{ still fails.} $\rho$ is at $\lambda=0.01$ (PCA slice: ) and |
| 267 | 0 | yes | at $\lambda=0$. The positive value at |
| 267 | 0.1 | yes | $\lambda=0$. The positive value at $\lambda=0.1$ ( ) again disappears on |
| 271 | 1 | yes | . The regularised $g$ falls steadily towards 1 in . |
| 273 | 4 | yes | h feature selection and / rad with PCA ($n=4$/$n=8$), so |
| 273 | 8 | yes | ure selection and / rad with PCA ($n=4$/$n=8$), so |
| 284 | 2 | yes | ragraph{Analytic noise.} We take four ZZ, $r=2$ settings: healthy ($c= |
| 285 | 4 | yes | ($c= $), each at $n=4$ and $n=8$. We re-estima |
| 285 | 8 | yes | ($c= $), each at $n=4$ and $n=8$. We re-estimate both tr |
| 287 | 4 | yes | ~ a,b). Shot noise dominates. The healthy $n=4$ kernel goes from AUC |
| 288 | 1000 | yes | (1000 shots) and (100 shots) |
| 288 | 100 | yes | (1000 shots) and (100 shots). The $n=8$ kernel |
| 288 | 8 | yes | (1000 shots) and (100 shots). The $n=8$ kernel goes from to |
| 289 | 0.1 | yes | oise alone barely matters: at $p_{\rm tot}=0.1$ for healthy $n=4$. The |
| 289 | 4 | yes | tters: at $p_{\rm tot}=0.1$ for healthy $n=4$. The concentrated kerne |
| 291 | 8 | yes | the measured variance of the concentrated $n=8$ kernel, from to |
| 292 | 100 | yes | at 100 shots. So the variance d |
| 292 | 1000 | yes | s. So the variance diagnostic is reliable at 1000 or more shots but can mi |
| 292 | 100 | yes | ble at 1000 or more shots but can mislead at 100. |
| 304 | 0.1 | yes | tem \textbf{Analytic model:} at $p_{\rm tot}=0.1$ and shots, the model |
| 305 | 5 | yes | (5--95\%: -- ) and a kerne |
| 305 | 95 | yes | (5--95\%: -- ) and a kernel er |
| 321 | 1 | yes | regularised $g$ does not return to 1 at small $c$ is that the |
| 328 | 1 | yes | extbf{Lenient significance.} seeds and the 1-sd rule correspond to $p |
| 328 | 0.09 | yes | eds and the 1-sd rule correspond to $p\approx0.09$ per comparison, |
| 346 | 1 | yes | overs AUC but does not pull $g$ back towards 1 ( held in part). |
