# Report Template

## Filename

`<vault>/RESEARCH/Research — {Topic}.md` (resolve `<vault>` from the `vault.path` in the active per-vault `config.json`).

Topic is a short descriptive phrase (e.g. "Whale Shark Tourism Economics", "Photo-ID Recapture Methods").

## Frontmatter

```yaml
---
date: YYYY-MM-DD
type: research
question: "{full research question}"
audience: "{audience}"
domain: "{detected domain}"
evidence_window: "{e.g. 2020–present}"
geographic_scope: "{if applicable}"
sub-questions:
  - "{sub-question 1}"
  - "{sub-question 2}"
sources_claude: {count}
sources_codex: {count}
sources_vault: {count}
---
```

## Required sections (in order)

### TL;DR
3–5 bullet points. The answer to the research question in under 100 words. Each bullet includes a confidence tag: (High), (Medium), or (Uncertain).

### Implications
What this means for the stated audience. Concrete, actionable where possible. What should the reader do, decide, or consider based on these findings?

### Uncertainties and Limits
What this research could not resolve. Evidence gaps, conflicting sources, scope boundaries, vault material that was summarised rather than fully included, and anything the reader should verify independently. Be honest about what the report does and does not establish.

### Confidence Map

| Finding | Confidence | Claude | Codex | Vault | Notes |
|---------|-----------|--------|-------|-------|-------|
| one-line summary | High/Med/Unc | Y/N | Y/N | Y/N | brief note |

One row per major finding. Model convergence columns are triangulation cues, not evidence.

### Findings
Organised by theme (not by sub-question or source). Claim-level attribution throughout. Conflicts surfaced explicitly. Includes evidence tables, comparison matrices, recommendation blocks, timelines, or gap analyses where the content warrants — adaptive to what the research found.

### Sources
Full source list, deduplicated, grouped by type:
- Peer-reviewed literature
- Institutional reports
- News / media
- Vault files
- Other

Each entry: Title, URL, one-line relevance note.

### Follow-up Research Questions
3–5 questions that emerged from this research but were out of scope. Each with a one-line note on why it matters and what it would take to investigate.

If the vault briefing was summarised due to size (>10,000 words), note which sub-questions have deeper vault material available and would benefit from a targeted follow-up run.

## Appendix sections (include when materially useful)

### Model Divergence
Where Claude and Codex disagreed and how the synthesis resolved it.

### Vault Context
What was already known from the Obsidian vault before web research. Key vault files referenced, with [[wikilinks]].

### Claim Verification Log

| Claim | Verdict | Source | Note |
|-------|---------|--------|------|
| "quote" | Confirmed/Partial/Unsupported/Contradicted | URL | caveat |

## Writing principles

- **Write for the reader, not the audit trail.** The report should read as a clear, insightful answer — not a catalogue of everything found.
- Lead with what matters, explain why it matters, use plain language.
- Attribution and confidence machinery should be visible but not dominant.
- NZ/UK English throughout.
