---
type: workflow
applies_to: literature
status: draft
last_updated: 2026-04-20
supersedes:
  - "Build-A-Continuous-Marine-Mammal-Literature-Ingestion — Exploration"
  - "Living Reference Library — Design Concept"
---

# Living Reference Library — Literature Intake & Integration

> **Adapting this for your work.** Examples cite Simon Pierce's reference library on whale sharks, marine mammals, and shark research techniques. The *workflow* — three layers (per-paper integration, chapter-level enrichment, library-wide consolidation), the per-paper integration checklist, and the "living document" model — generalises to any scientific reference library or topic-organised literature collection. The vault paths (`02_MARINE MEGAFAUNA/REFERENCE LIBRARY/...`) are MMF-specific; substitute your own. The associated `/project-intake` skill (referenced by some sections) is **not shipped** with the starter bundle — its logic is too MMF-coupled for safe generalisation.

A system for maintaining "living" book chapters and scientific reference documents that are steadily enriched with new literature over time. Each resource starts from published text and is incrementally updated as new papers come out.

> [!note] Status
> Draft process — consolidated from three earlier documents. Not yet tested end-to-end. The per-paper integration checklist (Layer 3) is the most mature component, in use since late 2025.

## Source collections

| Collection | Source | Vault location | Conversion status |
|---|---|---|---|
| **Whale shark book** — *Whale Sharks: Biology, Ecology, and Conservation* (Dove & Pierce, CRC Press, 2024) | 13 published chapters + 2 new drafts (Ch 14, Ch 15) + Ch 16 | `02_MARINE MEGAFAUNA/REFERENCE LIBRARY/WHALE SHARK BOOK/` | Done |
| **Biology of Sharks and Their Relatives** (Carrier et al., CRC Press, 3rd ed. 2022) | 25 submitted chapter .docx files on Google Drive | `02_MARINE MEGAFAUNA/REFERENCE LIBRARY/Biology of Sharks Book/` | Done |
| **Encyclopedia of Marine Mammals** (Würsig et al., Academic Press, 3rd ed. 2018) | 23 PDFs (selected entries relevant to NZ/Kaikōura marine mammals) | `02_MARINE MEGAFAUNA/REFERENCE LIBRARY/Encyclopedia of Marine Mammals/` | Done |
| **Shark Research Techniques** (Carrier et al., CRC Press, 2022) | Single 408-page PDF, 19 chapters | `02_MARINE MEGAFAUNA/REFERENCE LIBRARY/Shark Research Techniques/` | Done |

Additional collections can be added as they're converted. The system is designed per-chapter, not per-book.

## Architecture overview

Three layers, built incrementally:

```
Layer 1: Setup          Convert chapters to .md → initial enrichment → routing index
Layer 2: Monitoring     Literature feeds (Google Scholar, Paperpile, API alerts) → inbox
Layer 3: Integration    Per-paper triage → intake note → controlled update → review
```

---

## Layer 1 — One-time setup (per book)

### 1a. Convert source chapters to vault .md

Use the `/pdf-to-markdown` skill for all PDF conversions. For full tool chain and known issues, see PDF to Markdown — Conversion Skill.

- **Already .md** (whale shark book): verify formatting, add frontmatter with chapter metadata
- **.docx sources** (sharks book): extract via **gws CLI** (primary) or pandoc, then diff against published PDF for editorial changes. Prefer gws CLI; fall back to Google Workspace MCP if gws is unavailable.
  - **gws CLI** (primary): `cd /tmp && gws drive files get --params '{"fileId": "<ID>", "alt": "media"}' -o chapter.docx` (binary download) or `cd /tmp && gws drive files export --params '{"fileId": "<ID>", "mimeType": "text/plain"}' -o chapter.txt` if stored as a Google Doc. The legacy `--fileId`/`--alt`/`--mimeType` flag form was removed; `--params` JSON is required. `-o` rejects paths outside CWD, so `cd` to the target dir first. Note: gws output includes a leading `Using keyring backend: keyring` line before JSON — skip it when parsing.
  - **Google Workspace MCP** (fallback): `get_drive_file_content` tool.
- **PDF sources** (marine mammals encyclopedia, shark research techniques): convert via `/pdf-to-markdown` skill (marker extraction + cleanup pipeline), clean up OCR artefacts

Each chapter file needs frontmatter. The exact schema varies by book — match the convention already in use for that collection:

**Whale shark book** (established convention):
```yaml
---
title: "Chapter 7: Population Ecology of Whale Sharks"
authors: "Christoph A. Rohner, Brad Norman, Gonzalo Araujo, Jason Holmberg, and Simon J. Pierce"
book: "Whale Sharks: Biology, Ecology, and Conservation"
editors: "Alistair D. M. Dove and Simon J. Pierce"
publisher: CRC Press
year: 2021
chapter: 7
---
```

**Biology of Sharks** (established convention):
```yaml
---
tags: [biology-of-sharks, book, chapter]
author: Whitenack
chapter: 1
---
```

Add `last_enriched: YYYY-MM-DD` when a chapter first receives a literature enrichment pass (Layer 1b or Layer 3).

### 1b. Initial enrichment pass

**Source: Simon's Paperpile library — not web searches.** Paperpile is the curated primary source for all Reference Library enrichment. Do not use WebSearch, Semantic Scholar, `/research`, or any other independent literature discovery. Simon self-selects what enters the pipeline; Claude's job is to integrate what's there, not to find new papers. If Paperpile has gaps for a topic, flag that to Simon rather than filling them independently.

Access Paperpile via Chrome (paperpile.com), Google Drive (Paperpile folder), or an exported list (BibTeX/CSV/JSON). Search within Paperpile for papers relevant to the chapter being enriched, focusing on literature published since the chapter's submission date.

> [!warning] Paperpile JSON exports are large — never read directly with the Read tool
> Paperpile JSON exports are ~796K / 18K lines. Reading them with the Read tool floods context and causes process crashes. Use python3 via Bash to parse and filter:
> ```python
> import json
> with open('/path/to/export.json') as f:
>     data = json.load(f)
> # Year is in published.year (dict), not a top-level field
> relevant = [r for r in data if any(kw in (r.get('title','') + r.get('abstract','')).lower() for kw in keywords)]
> post_cutoff = [r for r in relevant if isinstance(r.get('published'),dict) and r['published'].get('year','0') >= '2017']
> # PDF path: All Papers/{FIRST_LETTER}/{attachments[0].filename}
> ```

For the whale shark book, Voice Reference — Simon Pierce (Whale Shark Book) governs the writing style for any additions.

### PDF access waterfall (for paywalled or locally-unavailable sources)

When a paper's PDF isn't available at the expected local Drive path (common due to Google Drive streaming mode not syncing all files), try these methods in order:

1. **Local Drive path** — `~/Library/CloudStorage/GoogleDrive-*/My Drive/4. Resources/Paperpile/All Papers/{letter}/{filename}.pdf`
2. **Drive API** — `mcp__google-workspace__search_drive_files` → `mcp__google-workspace__get_drive_file_download_url` → `curl -L -o /tmp/paper.pdf "<url>"` → `/opt/homebrew/bin/pdftotext /tmp/paper.pdf -`
3. **Direct PDF URL** — `curl -L` if a known open-access URL exists (e.g. from Paperpile metadata)
4. **Article page extraction** — `defuddle parse <url> --md` for HTML article pages (works well for open-access journals)
5. **WebFetch** — less reliable (AI intermediary may summarise), but works as a fallback for article pages
6. **Playwright** — navigate to the journal page in a browser context, find open-access or institutional link, use `fetch()` in browser context, base64-decode to `/tmp/`, then `pdftotext`

Steps 1–2 are the standard path documented in the enrichment task pre-checks. Steps 3–6 extend coverage for autonomous workhorse use where Drive API also fails. Always prefer earlier steps — later steps are progressively less reliable.

### 1c. Build a routing index

A lightweight index mapping topics, species, and keywords to chapter files. This tells the monitoring layer where to route new papers.

**Format:** A single vault note (`Living Reference Library — Routing Index.md`) with a table:

| Keyword / species | Chapter file | Section hint |
|---|---|---|
| whale shark movements | `Ch 07 — Movements.md` | Migration patterns |
| *Rhincodon typus* growth | `Ch 05 — Growth.md` | Growth rates |
| sperm whale diving | `Marine Mammals — Sperm Whale.md` | Foraging ecology |

Start manually; automate keyword extraction later if the index grows past ~50 entries.

---

## Layer 2 — Literature monitoring

### Primary intake: Paperpile (decision 2026-04-03)

Paperpile is the primary literature intake infrastructure. Simon self-selects which papers enter the pipeline — this provides quality control at the point of entry, excluding low-quality papers before they reach the integration workflow. Google Scholar alerts and API monitoring are secondary channels that surface candidates, but papers should be added to Paperpile before integration.

**Workflow:** Simon adds papers to Paperpile → export Paperpile library to Google Sheet (Paperpile supports this natively) → cross-reference against chapter files to identify what's new → route new papers to the literature inbox for triage and integration.

The Paperpile library on Google Drive also serves as the "what do we already know" baseline — prevents re-ingesting papers that are already integrated.

### 2a. Google Scholar alerts (secondary — surfaces candidates)

Set up Google Scholar alerts for key species and topics. Forward alert emails to `simon+claude@marinemegafauna.org` (existing Claude Review pipeline). A weekly automation scans the inbox, matches papers against the routing index, and writes candidate papers to the literature inbox. Papers that pass triage should be added to Paperpile.

### 2b. API monitoring (future — Phase 3)

A scheduled script queries Semantic Scholar and/or PubMed for new papers matching a species watchlist. Candidates:

- **Semantic Scholar API** (free, 214M+ papers) — keyword search with date filters (`publicationDateOrYear:2026-...`). Rate limit 1 RPS with free API key.
- **PubMed/Entrez API** — strong coverage of marine mammal journals. Free, supports date-windowed species searches.
- **CrossRef API** — DOI-based metadata resolution for full citation details.

This would run as a LaunchAgent (weekly), writing results to `00_INBOX/LITERATURE ALERTS/`.

### 2c. Website onboarding (future — needs manual review)

Some websites are high-quality reference sources for marine mammal and shark biology (e.g. IUCN Red List assessments, DOC species pages, regional marine mammal atlases). These can be onboarded as supplementary sources for chapter enrichment, but require manual review by Simon before inclusion. Process TBD — will be designed after the Paperpile-based workflow is proven.

### 2d. Manual flagging

Simon flags a paper directly: "update the whale shark movements chapter with this." This bypasses monitoring and goes straight to Layer 3.

### 2e. Nightly workhorse enrichment

The nightly workhorse can include chapter enrichment as a task type — scanning for recent literature as part of its existing vault enrichment cycle. This is opportunistic rather than systematic.

### Literature inbox format

All channels write to a shared inbox location. Each entry:

```markdown
## Smith et al. 2026 — Whale shark migration routes in the Indian Ocean

- **Journal:** Marine Ecology Progress Series
- **DOI:** 10.xxxx/xxxxx
- **Abstract:** [full abstract]
- **Routing:** Ch 07 — Movements (migration patterns); Ch 12 — Conservation (habitat connectivity)
- **Source:** Google Scholar alert / Semantic Scholar API / manual
- **Status:** pending
```

---

## Layer 3 — Per-paper integration

This is the operational core. Every paper that passes triage follows this checklist.

### Step 1. Triage — does this paper belong?

- Is it relevant to an existing chapter or reference document?
- Does it add new data, mechanisms, or framing (not just repetition)?
- Is it primary research or a high-quality review?

If no to all, archive or ignore. Do not ingest by default.

### Step 2. Create a literature intake note

Create from scratch (no template file exists yet — create one if the per-paper workflow stabilises). Name format:

```
YYYY — FirstAuthor et al — Short descriptive title.md
```

Fill in at minimum:
- Citation (full)
- Why this paper matters
- Key findings (author claims, not interpretation)
- What's genuinely new
- Relevance to existing chapters (with `wikilinks`)

Set frontmatter: `status: skimmed` or `status: extracted`

Do not synthesise yet.

### Step 3. Identify integration targets

List which chapter files this paper may affect:
- `Ch 07 — Movements` — new satellite tracking data
- `Marine Mammals — Sperm Whale` — revised dive depth estimates

If unsure, list candidates rather than guessing. The routing index helps here.

### Step 4. Controlled integration

Two modes depending on the maturity of the target document:

**Mode A — Direct integration** (for reference documents and early-stage chapters)

Claude reads the target chapter and the intake note, then integrates new content directly:
- Preserve structure and author voice
- Add citations (Author Year + DOI)
- Flag conflicts or uncertainty instead of overwriting
- List exactly which sections were modified and how

**Mode B — PR for papers** (for mature manuscripts and polished chapters)

For text that's stable enough that unsupervised edits could disrupt coherence:
1. Claude reads the paper and cross-references against the current chapter
2. Produces a structured proposal: which section(s) affected, specific text changes with before/after, rationale, new references
3. Proposal saved to a `PROPOSED UPDATES/` subfolder alongside the chapter
4. Author reviews and approves/rejects each change; approved changes applied surgically

Mode B is appropriate for the whale shark book chapters (published text) and any manuscript under active revision.

### Step 5. Review changes

In Obsidian, review only modified sections.

- Are new claims placed in the correct conceptual section?
- Are citations present and accurate?
- Is uncertainty handled conservatively?
- Were existing claims silently altered? (should not happen)

If unhappy: revert manually, or ask Claude to revise specific sections only.

### Step 6. Resolve or park uncertainty

If conflicts exist between new and existing content, document them under a `## Conflicts / Needs review` section in the chapter. Follow the full workflow in Resolving Conflicts & TODOs in Synthesis Notes.

If unresolved:
- Leave `TODO/VERIFY` markers
- Do not force resolution prematurely

### Step 7. Update intake note status

**Verification gate (mandatory before marking done):** two checks, both must pass.

**7a. Dual-grep for author-in-body-and-references.** Grep for the author surname in (1) the chapter body text and (2) the References section separately. Both must return matches. If either grep returns no hit, the integration is incomplete.

**7b. Citation verification (added 2026-04-20).** Run `python3 ~/bin/verify_citations.py "<CHAPTER_PATH>" -o /tmp/citation-report.md` against the modified chapter. Read the report. The gate fails if:
- Any citation in the chapter resolves to `NOT_FOUND` across all three sources (Semantic Scholar, CrossRef, OpenAlex).
- Any citation has an author/year mismatch flagged with confidence ≥ `medium`.

Rationale: Step 7a only catches the specific paper being integrated. When prose written from an abstract-only source introduces *other* citations in the narrative (e.g., Guerra 2020/2022/2023 tracking failures on 2026-04-09, Rohner 2022 red-team finding), 7a gives a false green. 7b runs against the whole chapter so any newly-introduced fabrication is caught regardless of whether it's the target paper or a transitive reference.

Whole-chapter verification is used (not diff-only) because (1) it's simpler to implement and run, and (2) pre-existing bad citations flagged as collateral are useful — they surface legacy cruft from prior integrations for the same low marginal cost.

**If either 7a or 7b fails:** the integration is incomplete — do not mark the unit as done. In workhorse queue tracking, move such units to `units_verify_failed` rather than `units_done`. Capture the specific failure (which author missing from which section, or the list of NOT_FOUND citations) in the unit's tracking block so the next attempt has diagnostic context.

**If both pass:** update frontmatter: `status: integrated`. Optionally add a brief summary of how it changed understanding.

### Step 8. Sanity check

- No duplicate claims added
- No loss of prior nuance
- Vault structure still coherent
- Voice consistent with the rest of the chapter

---

## Operating principles

1. **Claude assists; Simon decides relevance.** Automated monitoring surfaces candidates; a human decides what gets integrated.
2. **Integration is conservative by default.** The existing chapter text is the source of truth, not the new paper. New content is additive unless it corrects a clear factual error.
3. **Uncertainty is explicit, not smoothed over.** When sources conflict or evidence is mixed, surface the disagreement. Flag open questions as `TODO/VERIFY`.
4. **Citation integrity is non-negotiable.** No fabricated DOIs. Every quantitative claim cited. Conflicting values shown explicitly. Where an evidence hierarchy exists (e.g. Tier 1-4 in a fact file prompt), it governs what an automated pipeline may update vs. what requires human review.
5. **Voice preservation matters.** Each book has a distinct authorial voice. Updates must match — not generic academic prose, not AI-tells. Use the relevant voice reference where one exists.

## Common failure modes

| Failure mode | Mitigation |
|---|---|
| Overconfident language creeping in | Tighter prompts, voice reference checks, `/polish` pass |
| Citations missing after rewording | Step 7a dual-grep (author in body + References) |
| Hallucinated citations introduced during abstract-only integration | Step 7b `verify_citations.py` gate — blocks unit completion on any NOT_FOUND |
| Structural drift from repeated integrations | Periodic full-chapter review (quarterly) |
| Hallucinated author names in automated extraction | Author verification step; cross-check DOIs |
| New data overwriting verified content | Evidence hierarchy enforcement; Mode B for mature text |
| False completion — paper marked done but not in chapter | Step 7 dual-grep gate: verify author surname in body AND References before marking done |
| Process crash during Paperpile-based enrichment | Parse Paperpile JSON via python3/Bash (never Read tool on 796K file); save chapter incrementally after each section — not in one final write |

---

## Implementation phases

All four book conversions are complete (as of 2026-03-27). All collections moved to `02_MARINE MEGAFAUNA/REFERENCE LIBRARY/` (2026-04-03).

### Phase 1 — Encyclopedia of Marine Mammals (enrichment pilot)

Starting here because: (a) chapters are short encyclopedia entries that can expand significantly with quality content, (b) NZ/Kaikōura-specific biology and ecology is a high-value enrichment target, (c) content is current to ~2016-17 (published 2018), so there's 8+ years of new literature to integrate.

**Enrichment approach:** Each entry gets a literature review pass focusing on post-2017 research. Entries should expand from encyclopedia summaries toward book-chapter-depth treatments where the literature supports it. NZ-specific and Kaikōura-specific research is prioritised. Use Mode A (direct integration) — these are reference documents, not published manuscripts.

Next steps:
1. Enrich pilot chapter (Sperm Whale) to validate the approach
2. Enrich remaining chapters, prioritising NZ/Kaikōura-relevant species
3. Build initial routing index for marine mammal topics
4. Set up Paperpile cross-reference baseline

### Phase 2 — Whale shark book enrichment

All 16 chapters + preface converted. Voice reference exists. Next steps:
1. Build initial routing index for whale shark topics
2. Run enrichment passes on chapters
3. Integrate new papers using Mode B (published text — PR model)

### Phase 3 — Sharks book + shark research techniques enrichment

Both fully converted. Apply the same enrichment workflow.

### Phase 4 — Automation

Once the manual workflow is proven:
1. Export and cross-reference Paperpile library against all chapter files
2. Build API monitoring script (Semantic Scholar + PubMed → `00_INBOX/LITERATURE ALERTS/`) as secondary intake
3. Wire into a LaunchAgent (weekly cadence)
4. Design website onboarding process (manual review by Simon)
5. Consider nightly workhorse integration for opportunistic enrichment

---

## Related files

- Living Reference Library — Design Concept — original architecture concept (archived — superseded by this doc)
- Build-A-Continuous-Marine-Mammal-Literature-Ingestion — Exploration — API monitoring exploration (archived — superseded by this doc)
- Voice Reference — Simon Pierce (Whale Shark Book) — writing voice for whale shark chapters
- Gmail — Claude Review Pipeline — Google Scholar alert ingestion path
- PDF to Markdown — Conversion Skill — tool chain and known issues for PDF conversion
- Resolving Conflicts & TODOs in Synthesis Notes — conflict resolution workflow (referenced by Step 6)
- `/pdf-to-markdown` skill — primary tool for PDF-to-markdown conversion
- `/project-intake` skill — for ingesting grants, reports, and other MMF documents into project notes (separate workflow; shares integration principles with this doc)

---

## Lessons and improvements

After using this process, note what worked and what didn't. If an improvement is non-controversial, apply it to this document immediately.

- Did any step take longer than expected or produce poor results?
- Was any instruction ambiguous or missing?
- Did the output meet the intended standard?
- Should any step be added, removed, or reordered?
