#!/usr/bin/env python3
"""
SRQ2 LLM layer — Synthesis Agent recommendations + LLM-as-Judge evaluation.

Builds on the deterministic synthesis (scripts/srq2_synthesis.py → 04_thesis_results/srq2/
synthesis.csv). For a stratified N≈50 sample:
  1. Synthesis Agent (claude-sonnet-4-6, temp 0) generates a 2-3 sentence
     recommendation from the structured synthesis context (Ch7 §7.3 prompt).
  2. Rule-based baseline produces a templated sentence (the Ch7 §7.6 comparator).
  3. LLM-as-Judge (GPT-4o, temp 0) scores BOTH on 5 Likert(1-5) dimensions
     (accuracy, calibration, actionability, relevance, clarity) — Ch8 §8.3.1.

Reads keys from .env (ANTHROPIC_API_KEY, OPENAI_API_KEY). Reproducible sampling
(seed=42); LLM calls temp=0. No Prometheus dependency. Cost ≈ a few cents.
Usage: .venv/bin/python scripts/srq2_agent.py [--n 50]
Output: 04_thesis_results/srq2/{recommendations.csv, judge_scores.csv, llm_summary.md}
"""
import argparse, json, os, sys, time, warnings
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from PATHS import THESIS_RESULTS_SRQ2_DIR

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]
OUT = THESIS_RESULTS_SRQ2_DIR
SEED = 42

for line in (ROOT / ".env").read_text().splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, _, v = line.partition("="); os.environ.setdefault(k.strip(), v.strip())

SYS_SYNTH = ("You are a demand forecasting analyst for FMCG retail. Given ML model "
             "forecasts, a calibrated confidence score, and demand signals, produce a concise, "
             "actionable recommendation for a category manager. Rules: always state the forecast "
             "range (lower to upper), not just the point; always state the confidence level "
             "(High/Moderate/Low) and why; if uncertain, flag it; 2-3 sentences max; do not "
             "invent data — only use provided inputs.")

JUDGE_SYS = ("You are an impartial evaluator of demand-forecast recommendations. Score the "
             "recommendation on five dimensions, each an integer 1-5: accuracy (forecast "
             "consistent with stated confidence), calibration (uncertainty communicated "
             "correctly), actionability (clear action for a category manager), relevance "
             "(context used appropriately), clarity (clear and concise). Return ONLY compact "
             "JSON: {\"accuracy\":n,\"calibration\":n,\"actionability\":n,\"relevance\":n,\"clarity\":n}.")


def synth_prompt(r):
    return (f"PRODUCT CATEGORY: {r.category} | horizon: 1 month\n"
            f"ENSEMBLE FORECAST: {r.ensemble:.0f} units (90% interval: {r.lower90:.0f} – {r.upper90:.0f})\n"
            f"CONFIDENCE: {r.confidence:.0f}/100 ({r.tier}) — inter-model agreement {r.agreement:.2f}\n"
            f"Generate the recommendation.")


def rule_baseline(r):
    return (f"Forecast for {r.category}: {r.ensemble:.0f} units "
            f"(90% range {r.lower90:.0f}–{r.upper90:.0f}); model confidence {r.confidence:.0f}% ({r.tier}).")


def main():
    n = argparse.ArgumentParser(); n.add_argument("--n", type=int, default=50)
    N = n.parse_args().n
    df = pd.read_csv(OUT / "synthesis.csv")
    # stratified sample across categories, reproducible
    rng = np.random.default_rng(SEED)
    parts = []
    for cat, g in df.groupby("category"):
        k = max(1, round(N * len(g) / len(df)))
        parts.append(g.iloc[rng.choice(len(g), size=min(k, len(g)), replace=False)])
    samp = pd.concat(parts).reset_index(drop=True)

    import anthropic, openai
    ac = anthropic.Anthropic(); oc = openai.OpenAI()

    def claude(sys, usr, max_tokens=200):
        for _ in range(3):
            try:
                r = ac.messages.create(model="claude-sonnet-4-6", max_tokens=max_tokens, temperature=0,
                                       system=sys, messages=[{"role": "user", "content": usr}])
                return r.content[0].text.strip()
            except Exception as e:
                time.sleep(2)
        return f"[ERROR generating]"

    def judge(rec_text, ctx):
        for _ in range(3):
            try:
                r = oc.chat.completions.create(model="gpt-4o", temperature=0, max_tokens=80,
                    messages=[{"role": "system", "content": JUDGE_SYS},
                              {"role": "user", "content": f"CONTEXT:\n{ctx}\n\nRECOMMENDATION:\n{rec_text}"}])
                t = r.choices[0].message.content.strip().strip("`")
                t = t[t.find("{"): t.rfind("}") + 1]
                return json.loads(t)
            except Exception:
                time.sleep(2)
        return {}

    recs, scores = [], []
    DIMS = ["accuracy", "calibration", "actionability", "relevance", "clarity"]
    for i, r in samp.iterrows():
        ctx = synth_prompt(r)
        llm_rec = claude(SYS_SYNTH, ctx)
        base = rule_baseline(r)
        recs.append(dict(category=r.category, ensemble=r.ensemble, confidence=r.confidence,
                         tier=r.tier, llm_rec=llm_rec, baseline_rec=base))
        for kind, text in [("LLM", llm_rec), ("baseline", base)]:
            js = judge(text, ctx)
            scores.append(dict(category=r.category, system=kind,
                               **{d: js.get(d, np.nan) for d in DIMS}))
        if (i + 1) % 10 == 0:
            print(f"  ...{i+1}/{len(samp)} done")

    pd.DataFrame(recs).to_csv(OUT / "recommendations.csv", index=False)
    sc = pd.DataFrame(scores); sc.to_csv(OUT / "judge_scores.csv", index=False)

    agg = sc.groupby("system")[DIMS].mean()
    lines = ["# SRQ2 LLM layer — Synthesis Agent + LLM-as-Judge", "",
             f"N={len(samp)} stratified (seed=42). Synthesis: claude-sonnet-4-6 (temp 0). "
             "Judge: GPT-4o (temp 0). Likert 1-5 per dimension. Baseline = rule-based template.", "",
             "| System | " + " | ".join(DIMS) + " | mean |", "|" + "---|" * (len(DIMS) + 2)]
    for sysname in ["LLM", "baseline"]:
        if sysname in agg.index:
            row = agg.loc[sysname]
            lines.append(f"| {sysname} | " + " | ".join(f"{row[d]:.2f}" for d in DIMS) +
                         f" | {row.mean():.2f} |")
    (OUT / "llm_summary.md").write_text("\n".join(lines) + "\n")
    print("Saved recommendations.csv + judge_scores.csv + llm_summary.md")
    print(agg.round(2).to_string())


if __name__ == "__main__":
    main()
