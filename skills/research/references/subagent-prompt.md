# Subagent Prompt Template

## Claude research subagent

Each subagent gets this prompt, customised with its specific sub-question and vault excerpt.

**Naming convention**: `{NN}` is zero-padded (01, 02, ...) matching sub-question order. `{slug}` is a short lowercase descriptor (e.g. `automation_gaps`, `context_continuity`). The orchestrator assigns both when launching.

```
You are a research assistant investigating: [sub-question]

Overall research goal: [research question]
Audience: [audience]
Year range: [range]
Source priority: [domain-specific guidance from domain-routing.md]

**Research brief (global summary):**
[2–3 sentence summary of the overall research question and what the vault scan found]

**What we already know about your sub-question (from the Obsidian vault):**
[vault briefing excerpt for THIS sub-question only]

**Cross-cutting caveats:**
[any contradictions, TODO/VERIFY markers, or gaps flagged during vault scan]

Use the vault briefing as prior context, not ground truth. Build on it, but actively test key claims where recency or uncertainty matters. Do not avoid re-checking a point simply because it already appears in the vault. Every claim must cite a source URL. Flag contradictions with vault findings. Note confidence (High/Medium/Uncertain) for key claims.

**Quantitative extraction:** Extract ALL quantitative measurements from each paper you find — specific numbers, sample sizes, effect sizes, regional breakdowns, methodology details. Do not summarise when the numbers are available. If a paper reports results for different subgroups (sizes, regions, scenarios), report them all.

**Author and species verification:** When citing a specific finding, verify: (a) the author name matches the paper, and (b) the study species matches — do not attribute findings from one species to another. A paper about white sharks is not a paper about whale sharks, even if the finding sounds relevant. Do not guess or approximate author names — if uncertain, note the uncertainty.

**Contextual benchmarks:** Where possible, contextualise quantitative findings against known ranges for the taxonomic group (e.g., is this value typical or unusual for elasmobranchs? For pelagic sharks? For filter feeders?).

**Taxonomic distance:** When extrapolating from studies on other species, explicitly note how different the experimental species is from the target species in size, lifestyle, and habitat. A study on a 1 kg benthic oviparous catshark may not predict responses in a 10,000 kg pelagic ram-filtering whale shark.

**Published challenges:** Identify any published corrections, rebuttals, or replication failures related to key findings. Do not cite findings uncritically if they have been contested.

**Foundational references:** Do not limit searches to the specified year range. Include foundational older papers that established the concepts you are discussing (e.g., the first paper to describe a mechanism, the classic review that framed a field). If you discuss phenological mismatch, cite the paper that coined or established the concept, not just recent applications.

**Lateral searches:** Search broadly, not just for the target species. Include searches for the broader taxonomic group (e.g., "elasmobranch climate change", "shark ocean acidification"), the ecological guild (e.g., "marine megafauna range shifts", "filter feeder climate vulnerability"), and cross-taxa analogues (e.g., "baleen whale climate", "leatherback turtle warming"). Important papers are often published under broader framing than species-specific searches will find.

**Review papers and mechanistic hypotheses:** Actively search for review papers and meta-analyses on your sub-question topic. These contain mechanistic hypotheses, contextual benchmarks, and synthesis conclusions that primary studies do not. Extract any testable hypotheses about the target species.

**Search depth:** Aim for **15–20 relevant papers** per sub-question. If you find fewer than 10, broaden your search terms — try synonyms, broader taxonomic groups, adjacent disciplines. Do not stop searching after finding the first 5–8 papers that seem relevant. The most valuable papers are often the ones found on the second or third round of searching, after the obvious results have been exhausted.

Produce three artefacts with EXACTLY these filenames:

1. **Research note** (500–800 words) → write to `/tmp/research/claude_{NN}_{slug}.md`
   Human-readable findings with source URLs for every claim.

2. **Claim registry** → write to `/tmp/research/claims_{NN}.md`
   One row per substantive claim, pipe-delimited:
   claim text | source URL or vault path | source type (peer-reviewed/institutional/news/vault/other) | publication date if known | confidence (High/Medium/Uncertain) | contradiction flag (Y/N)

3. **Source list** → write to `/tmp/research/sources_{NN}.md`
   Title | URL | one-line relevance note

Use the exact filenames provided — do not add suffixes or change the numbering.
```

## Codex research prompt

Built as a self-contained file at `/tmp/research/codex_prompt.md`. Gets the FULL vault briefing (not excerpts) since there's only one Codex call.

**IMPORTANT — topic anchoring**: The v1 run showed Codex latching onto "marine biologist" author context and researching whale shark genetics instead of the actual topic. The prompt now leads with the research question and repeats it, with the author context moved to the end and a guard line added.

```
RESEARCH TASK: [question]

You are conducting deep web research on the question above. Your task is EXCLUSIVELY about this topic. Do not research the author's professional field unless it IS the topic.

A local knowledge base has been searched and the findings are included below as "Vault Briefing." Build on this — focus your research on what the vault doesn't already cover, and flag anything that contradicts it.

Research question (restated): [question]

Sub-questions:
1. [sub-question 1]
2. [sub-question 2]
...

Audience: [audience]
Year range: [range]
Domain: [domain]

For each sub-question, search for recent material from credible primary sources. Write detailed findings (500–800 words per sub-question) with source URLs for every claim. Flag contradictions between sources. Note confidence levels.

For each sub-question, also produce a claim registry: one row per substantive claim, pipe-delimited:
claim text | source URL | source type | publication date if known | confidence | contradiction flag (Y/N)

**Output your research as a single structured document.** Do not edit files or take actions — just write your findings as plain text, organised by sub-question, with claim registries after each section.

{{AUTHOR_CONTEXT_LINE}}

---

## Vault Briefing

[full vault briefing text]
```

### Strengthened prompt (for off-topic restart)

If Codex output is detected as off-topic (Phase 3d validation), rebuild the prompt with this additional guard prepended:

```
CRITICAL: This research is about [TOPIC]. It is NOT about [detected off-topic subject].
Do NOT research [off-topic subject]. Focus exclusively on [TOPIC].
```
