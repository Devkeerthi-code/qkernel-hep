"""Check every number in the report against results/.

    python scripts/check_report_numbers.py      (needs MiKTeX/TeX on PATH and pdftotext)

1. Builds a catalogue of numbers from results/: every numeric leaf of the JSON files (and numbers inside
   their strings), every numeric cell of summary_table.csv, group statistics of noise.csv, line counts of
   runs.jsonl, and derived counts (list lengths, True counts, label tallies).
2. Compiles a draft copy of report/main.tex (figures replaced by boxes, so tick labels inside figures are
   not read), extracts its text, and matches every number in the body to the catalogue at the displayed
   precision. The reference list is excluded (it comes from docs/references.bib).
3. Lists numbers typed literally in main.tex (outside \\V{...}), which are method constants.
4. Recomputes key counts independently from results/ and compares them with numbers.tex.
5. Checks that the hypotheses quoted in main.tex match docs/hypotheses.md word for word.
Writes report/number_check.md and exits non-zero on any mismatch.
"""
from __future__ import annotations

import json
import math
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RES, REP = ROOT / "results", ROOT / "report"
NUM = re.compile(r"(?<![\w.])[-−+]?\d{1,3}(?:,\d{3})+(?![\d])|(?<![\w.])[-−+]?\d+(?:\.\d+)?")


# ------------------------------------------------------------------------------------- catalogue
def walk(o, out: list, depth=0):
    if isinstance(o, bool):
        return
    if isinstance(o, (int, float)) and math.isfinite(o):
        out.append(float(o))
    elif isinstance(o, str):
        out.extend(float(x) for x in re.findall(r"-?\d+(?:\.\d+)?(?:e-?\d+)?", o))
    elif isinstance(o, dict):
        for v in o.values():
            walk(v, out, depth + 1)
        out.extend(float(v) for v in [len(o)])
    elif isinstance(o, list):
        out.append(float(len(o)))
        for v in o:
            walk(v, out, depth + 1)
        if o and all(isinstance(v, dict) for v in o):  # tallies over a list of records
            keys = set().union(*o)
            for k in keys:
                vals = [v.get(k) for v in o]
                if all(isinstance(v, bool) for v in vals if v is not None):
                    out.append(float(sum(bool(v) for v in vals)))
                if all(isinstance(v, str) for v in vals if v is not None):
                    for lab in set(vals):
                        out.append(float(sum(v == lab for v in vals)))


def catalogue() -> np.ndarray:
    vals: list[float] = []
    for f in list(RES.glob("*.json")) + list((RES / "hardware").glob("*.json")) + list(RES.glob("*/meta.json")):
        walk(json.loads(f.read_text()), vals)
    for e in ("main_grid", "big_qubits", "n_sweep", "fs_gbdt"):
        lines = [line for line in (RES / e / "runs.jsonl").read_text().splitlines() if line]
        vals.append(float(len(lines)))
    vals.append(float(sum(1 for e in ("main_grid", "big_qubits")
                          for line in (RES / e / "runs.jsonl").read_text().splitlines() if line)))
    t = pd.read_csv(RES / "summary_table.csv")
    vals += [float(v) for v in t.select_dtypes("number").to_numpy().ravel() if np.isfinite(v)]
    nz = pd.read_csv(RES / "noise.csv")
    nz["shots"] = nz.shots.astype(str)
    num_cols = nz.select_dtypes("number").columns
    for keys in (["study", "config", "shots", "p_tot"], ["study", "config"], ["study"]):
        g = nz.groupby(keys, dropna=False)[list(num_cols)]
        for stat in (g.mean(), g.std(), g.min(), g.max(), g.quantile(0.05), g.quantile(0.95)):
            vals += [float(v) for v in stat.to_numpy().ravel() if np.isfinite(v)]
    vals += [float(v) for v in nz[num_cols].to_numpy().ravel() if np.isfinite(v)]
    vals += [float(s) for s in nz.shots.unique() if s.isdigit()]
    for keys in (["study", "config"], ["study"]):  # distinct counts, e.g. number of noise draws
        vals += [float(v) for v in nz.groupby(keys).nunique().to_numpy().ravel()]
    return np.array(sorted(set(vals)))


def matches(token: str, cat: np.ndarray) -> str | None:
    s = token.replace("−", "-").replace(",", "")
    x = float(s)
    d = len(s.split(".")[1]) if "." in s else 0
    tol = 0.5 * 10 ** (-d) + 1e-12
    for sign_label, target in (("", x), (" (|value|)", abs(x))):
        i = np.searchsorted(cat, target - tol)
        if i < len(cat) and cat[i] <= target + tol:
            return f"{cat[i]:.10g}{sign_label}"
        i = np.searchsorted(cat, -target - tol)
        if sign_label and i < len(cat) and cat[i] <= -target + tol:
            return f"{cat[i]:.10g}{sign_label}"
    return None


# ------------------------------------------------------------------------------------- PDF text
def build_draft() -> str:
    tex = (REP / "main.tex").read_text(encoding="utf-8")
    cmd = r"\PassOptionsToPackage{draft}{graphicx}\input{main.tex}"
    for step in (["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-jobname=numcheck", cmd],
                 ["bibtex", "numcheck"],
                 ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-jobname=numcheck", cmd],
                 ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-jobname=numcheck", cmd]):
        subprocess.run(step, cwd=REP, capture_output=True, text=True)
    out = subprocess.run(["pdftotext", "-layout", "numcheck.pdf", "-"], cwd=REP, capture_output=True,
                         text=True, encoding="utf-8").stdout
    for ext in ("aux", "bbl", "blg", "log", "out", "pdf"):
        (REP / f"numcheck.{ext}").unlink(missing_ok=True)
    del tex
    return out


def body_tokens(text: str) -> list[tuple[str, str]]:
    body = re.split(r"\n\s*References\s*\n", text)[0]
    body = re.sub(r"fig\d_[a-z_]+\.pdf", " ", body)                     # draft-mode figure boxes
    body = re.sub(r"\[(\d+(?:\s*[,–-]\s*\d+)*)\]", " ", body)             # citations [3, 7–9]
    body = re.sub(r"\b(Figure|Fig\.|Table|Sec\.|Section|Figs\.)\s*~?\d+[a-z]?(\s*[a-z,]+)?", " ", body)
    body = re.sub(r"\bH[1-4]\b", " ", body)
    body = re.sub(r"\blog10\b|\blog\s*10\b", " log ", body)
    body = re.sub(r"(?m)^\s*\d+(\.\d+)?\s{2,}(?=[A-Z])", " ", body)       # section numbers
    body = re.sub(r"(?m)^\s*\d+\s*$", " ", body)                          # page numbers
    toks = []
    sci = re.compile(r"(\d+(?:\.\d+)?)\s*×\s*10\s*([−-]?)\s*(\d+)")
    for line in body.splitlines():
        for m in sci.finditer(line):
            toks.append((f"{m.group(1)}e{'-' if m.group(2) else ''}{m.group(3)}", line.strip()))
        line = sci.sub(" ", line)
        for m in NUM.finditer(line):
            toks.append((m.group(0), line.strip()))
    return toks


# ------------------------------------------------------------------------------- literal numbers
def literal_numbers() -> list[tuple[int, str, str]]:
    """(line, number, context) for digits in main.tex outside \\V{}, comments, cite keys and layout options."""
    out = []
    raw = (REP / "main.tex").read_text(encoding="utf-8")
    raw = "\n".join(re.sub(r"(?<!\\)%.*", "", line) for line in raw.splitlines())    # comments
    raw = re.sub(r"\\cite\{[^}]*\}", lambda m: "\n" * m.group(0).count("\n"), raw, flags=re.S)  # cite keys
    for i, line in enumerate(raw.splitlines(), 1):
        s = re.sub(r"\\V\{[^}]*\}", " ", line)
        s = re.sub(r"\\(label|ref|cite|includegraphics(\[[^]]*\])?|graphicspath|usepackage(\[[^]]*\])?|documentclass(\[[^]]*\])?|"
                   r"section|subsection|bibliography(style)?|setlength|input)\{[^}]*\}", " ", s)
        s = re.sub(r"\\log_\{10\}|_\{10\}|\\(?:begin|end)\{[^}]*\}|\{l+c+\}|blue!50!black|margin=[\d.]+cm|"
                   r"\d+pt|\[[\d.]+\\textwidth\]|width=[\d.]+\\textwidth|H[1-4]|fig\d_[a-z_]+", " ", s)
        for m in re.finditer(r"\d+(?:\.\d+)?", s):
            ctx = s[max(0, m.start() - 45): m.end() + 25].strip().replace("|", "/")
            out.append((i, m.group(0), " ".join(ctx.split())))
    return out


# ------------------------------------------------------------------------------- independent recount
def recount() -> list[str]:
    rep = json.loads((RES / "h2_analysis.json").read_text())
    nums = {m.group(1): m.group(2) for m in re.finditer(r"\\defval\{([^}]+)\}\{(.*)\}%", (REP / "numbers.tex").read_text(encoding="utf-8"))}
    val = lambda k: re.sub(r"\\ensuremath\{|\}|\{,\}", "", nums[k]).replace("{", "")  # noqa: E731
    t = pd.read_csv(RES / "summary_table.csv")
    t = t[t.experiment.isin(["main_grid", "big_qubits"]) & (t.n_train == 500)]
    checks = {
        "nconfigs": len(t),
        "h1_fid_cb": int((t.gap_vs_best_label == "classical better").sum()),
        "h1_fid_ns": int((t.gap_vs_best_label == "not significant").sum()),
        "h1_fid_qb": int((t.gap_vs_best_label == "quantum better").sum()),
        "h1_pqk_cb": int((t.pqk_gap_vs_best_label == "classical better").sum()),
        "h1_pqk_qb": int((t.pqk_gap_vs_best_label == "quantum better").sum()),
        "nc_above_l001": int((t["g_lam0.01"] > math.sqrt(500)).sum()),
        "nc_above_l0": int((t["g"] > math.sqrt(500)).sum()),
        "h3_held": sum(c["H3_holds_here"] for c in rep["H3"]["trend_vs_qubits"]),
        "h4_auc_rec": sum(c["performance_recovered"] for c in rep["H4"]["cells"]),
        "h4_var_raised": sum(c["concentration_reduced"] for c in rep["H4"]["cells"]),
        "h4_g01_mono": sum(c["g_lam0.01_monotone_toward_1"] for c in rep["H4"]["cells"]),
        "h4_g0_mono": sum(c["g_lam0_monotone_toward_1"] for c in rep["H4"]["cells"]),
        "rows_main": sum(1 for line in (RES / "main_grid" / "runs.jsonl").read_text().splitlines() if line),
        "data_rows": json.loads((RES / "data_summary.json").read_text())["n_rows"],
    }
    bad = []
    for k, v in checks.items():
        got = val(k).replace(",", "")
        if str(v) != got:
            bad.append(f"{k}: numbers.tex has {got}, independent recount gives {v}")
    # rho values: recompute the headline Spearman rho directly from the table
    from scipy import stats
    rho = stats.spearmanr(t["g_lam0.01"], t.gap_vs_best)[0]
    head = re.findall(r"[-+]\d\.\d+", nums["h2_pool_l001"])[0]
    if f"{rho:+.2f}" != head:
        bad.append(f"h2_pool_l001: numbers.tex has {head}, scipy on summary_table gives {rho:+.2f}")
    return bad


def hypotheses_verbatim() -> list[str]:
    md = (ROOT / "docs" / "hypotheses.md").read_text(encoding="utf-8")
    quoted = " ".join(line[1:].strip() for line in md.splitlines() if line.startswith(">"))
    want = {m.group(1): " ".join(m.group(2).split()) for m in
            re.finditer(r"\*\*(H\d):\*\*\s*(.*?)(?=\s*\*\*H\d:\*\*|$)", quoted)}
    tex = (REP / "main.tex").read_text(encoding="utf-8")
    q = re.search(r"\\begin\{quote\}(.*?)\\end\{quote\}", tex, re.S).group(1)
    got = {m.group(1): " ".join(m.group(2).replace(r"\\", " ").split()) for m in
           re.finditer(r"\\textbf\{(H\d):\}\s*(.*?)(?=\\textbf\{H\d:\}|$)", q.replace(r"\small", ""), re.S)}
    return [f"{h}: report has '{got.get(h)}', docs has '{w}'" for h, w in want.items() if got.get(h) != w]


def main():
    cat = catalogue()
    text = build_draft()
    toks = body_tokens(text)
    matched, unmatched = [], []
    for tok, ctx in toks:
        if "e" in tok:
            m, e = tok.split("e")
            x = float(m) * 10 ** int(e)
            d = len(m.split(".")[1]) if "." in m else 0
            tol = 0.5 * 10 ** (-d) * 10 ** int(e)
            hit = next((f"{c:.4g}" for c in cat if abs(c - x) <= tol), None)
        else:
            hit = matches(tok, cat)
        (matched if hit else unmatched).append((tok, hit, ctx))
    lits = literal_numbers()
    recount_bad = recount()
    hyp_bad = hypotheses_verbatim()
    n_dec = sum("." in t or "e" in t for t, _ in toks)
    m_dec = sum("." in t or "e" in t for t, _, _ in matched)
    lines = ["# Number check of report/main.pdf against results/", "",
             f"- Numbers found in the body text of the PDF: **{len(toks)}** ({n_dec} with decimals, "
             f"{len(toks) - n_dec} integers)",
             f"- Matched to a value in results/ at the displayed precision: **{len(matched)}** "
             f"({m_dec} of {n_dec} decimals; integer matches are weak evidence on their own, so the key counts "
             f"are also recounted independently below)",
             f"- Not found in results/: **{len(unmatched)}** (listed below; each needs a reason)",
             f"- Independent recount of key counts and the headline rho: **{'OK' if not recount_bad else 'MISMATCH'}**",
             f"- Hypotheses quoted verbatim from docs/hypotheses.md: **{'OK' if not hyp_bad else 'MISMATCH'}**", ""]
    if recount_bad or hyp_bad:
        lines += ["## Mismatches", ""] + [f"- {b}" for b in recount_bad + hyp_bad] + [""]
    lines += ["## Numbers in the PDF not found in results/", "", "| number | context |", "|---|---|"]
    lines += [f"| {t} | {c[:110].replace('|', '/')} |" for t, _, c in unmatched]
    lines += ["", "## Numbers typed literally in main.tex (not from numbers.tex)", "",
              "These are grid values (n, r, c, lambda), formula constants, method constants (5-fold CV, the "
              "10^-10 Qiskit cross-check, the 95% / 5-95% interval levels, the 1-sd rule's t = 2.2 and p = 0.09, "
              "the 10^-3 / 0.1 / 0.5 regime thresholds of the H3 analysis, the -999 placeholder) and dates. "
              "'in results/' only says that the same value occurs somewhere in results/: for grid values it "
              "confirms the value, for constants such as 2.2 or 0.09 the match is a coincidence.", "",
              "| line | number | in results/ | context |", "|---|---|---|---|"]
    lines += [f"| {i} | {n} | {'yes' if matches(n, cat) else 'no'} | {c} |" for i, n, c in lits]
    (REP / "number_check.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print("\n".join(lines[:8]))
    print(f"unmatched: {[t for t, _, _ in unmatched]}")
    print(f"literal numbers in main.tex: {sorted({n for _, n, _ in lits}, key=float)}")
    sys.exit(1 if recount_bad or hyp_bad else 0)


if __name__ == "__main__":
    main()
