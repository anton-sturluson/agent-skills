---
name: analyze-earnings
description: "Analyze a company's quarterly earnings and produce an evidence-dense earnings analysis. Use when asked to analyze earnings, review an earnings call, or assess what a quarter reveals about a business."
user_invocable: true
argument: "<ticker> [--quarter Q3 --year 2025]"
---

# analyze-earnings

## References

- Checklist (section guide): `references/checklist.md`
- Audit prompt: `references/audit-prompt.md` (hand to audit subagent as-is)

## Workflow

### 1. Resolve company and gather materials

Look up company in `hard-disk/data/01-portfolio/current/company-directory.md`. No folder? Use `initialize-company` skill first.

Collect in the company's `data/` folder:

| Material | How to get it |
|:---|:---|
| Target quarter transcript | `earnings-transcript` skill or company IR site via `browser` skill |
| Prior quarter transcript(s) — 2 minimum, 3 when turbulent/pivoting | Same as above |
| Investor presentation / supplement (required when available) | Check company IR site (`browser` skill) and SEC 8-K (`minerva sec download {TICKER} --form 8-K`). If image-based slides, extract with `image` tool. Text-based: `minerva extract-files` |
| Earnings press release | `minerva sec bulk-download` or company IR site |
| Most recent 10-Q/10-K | `minerva sec download {TICKER} --form 10-Q --format markdown` |

Proxy (DEF 14A) is NOT required each quarter — only for initial company setup or evidence base refresh.

### 2. Read the checklist

Read `{baseDir}/references/checklist.md`. It defines the output sections and writing rules — ground yourself in these before extracting or writing.

### 3. Read prior quarter(s) and form hypotheses

Read prior transcript(s) and any prior analysis in `analysis/earnings/`. Form 3–5 hypotheses: promises to track, metrics to watch, language baselines.

### 4. Extract from earnings materials

Use `minerva extract-files` for longer filings (press release, 10-Q, supplements). In parallel, extract 10-Q footnotes — the checklist Section 6a specifies what to look for. Save to `data/structured/footnotes-Q{N}-Y{YYYY}.md`.

For investor presentations with charts/images: use `image` tool to extract all metrics before writing.

**Delegation rule:** Steps 1–4 (material collection, extraction, prior-quarter reading) may be delegated to subagents using `gemini-35-flash` with high reasoning — these are evidence-gathering tasks suited to parallel execution. Step 5 (writing the analysis) must be done by the main agent directly — the analysis requires the strongest available model for cross-quarter judgment, pattern recognition, and analytical coherence. Do not delegate the analysis write to a subagent. The main agent should be the orchestrator with enough context to write the final analysis.

### 5. Write the analysis

Follow the checklist section-by-section. The checklist defines both the output structure and the writing rules.

For large analyses (>50KB expected), write in sections and append. Do not attempt single-call writes.

Follow the checklist section-by-section, starting from Section 0 (header and quarter in brief).

Save to: `analysis/earnings/Q{N}-Y{YYYY}.md`

### 6. Audit and revise

Spawn audit subagent (model: `openai/gpt-5.5`, reasoning: `high`) using `{baseDir}/references/audit-prompt.md` as the prompt. Pass the analysis path, checklist path, and company folder.

Critical gaps must be fixed. Analytical gaps should be fixed unless waived with reason (note in appendix). Audit up to 2 rounds. Verify markdown links resolve correctly (`analysis/earnings/` → `../../data/...`).

## Output paths

| File | Location |
|:---|:---|
| Analysis | `{company}/analysis/earnings/Q{N}-Y{YYYY}.md` |
| Audit | `{company}/audits/earnings-audit-Q{N}-Y{YYYY}.md` |
| Footnotes | `{company}/data/structured/footnotes-Q{N}-Y{YYYY}.md` |

After final audit, run `md2pdf <analysis.md> -o <analysis.pdf>` and save alongside.
