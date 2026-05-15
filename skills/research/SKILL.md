---
name: research
description: Deep autonomous research with paperpile-mirror seed extraction (curated literature first via `qmd://paperpile/`), vault scan, three-model web research (Claude + Codex + Gemini), claim verification, and formal report. Use when the user says "/research", "deep research on", "investigate this thoroughly", or needs a comprehensive research report they can walk away from. NOT for quick mid-task lookups — those are ad-hoc.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
  - Bash
  - WebSearch
  - WebFetch
  - AskUserQuestion
  - TaskCreate
  - TaskUpdate
  - mcp__qmd__query
  - mcp__qmd__get
  - mcp__qmd__multi_get
  - mcp__claude_ai_Gmail__gmail_search_messages
  - mcp__claude_ai_Gmail__gmail_read_message
  - mcp__claude_ai_Gmail__gmail_read_thread
  - mcp__claude_ai_Slack__slack_search_public_and_private
  - mcp__claude_ai_Slack__slack_read_thread
---

Deep autonomous research with three-model triangulation (Claude + Codex + Gemini), full vault scan, and a polished report.

## Adapting this for your work

This skill ships ready-to-use but expects:

- **Codex CLI** (`npm i -g @openai/codex`) with `codex login` completed. If absent, the pipeline degrades to Claude + Gemini.
- **Gemini CLI** (`npm i -g @google/gemini-cli`) with interactive login completed. If absent, the pipeline degrades to Claude + Codex. If both Codex and Gemini are absent, the pipeline runs single-model with explicit notice.
- **QMD search** over your vault. Falls back to Glob/Grep if QMD is unavailable.
- **Voice matching (Phase 6)** is gated on `features.is_simon` in your per-vault `config.json` AND on the existence of a voice reference under your vault. For standard installs, Phase 6 runs only if a voice reference file is present and named per the conventions in `guides/ai-assisted-writing.md`; otherwise it skips cleanly.
- **Output location** comes from your per-vault config: `vault.path` + the research subfolder (default `<vault>/RESEARCH/` or `<vault>/AI_WORKFLOW/RESEARCH/`). Pick the location during /onboard or edit your config later.
- **Task creation** uses the bundled `/todo` skill, which routes to whichever task manager you configured during /onboard (Things 3, Todoist, Apple Reminders, or vault TODO.md).

# Design principles

1. **Definitive output over speed.** Each run should produce the best possible answer on the topic. Don't optimise for token efficiency at the expense of thoroughness.
2. **The vault is a primary resource.** It gets more valuable over time. Read documents in full, follow wikilinks, don't skimp on vault searches.
3. **Always wait for all *available* models.** Three-model triangulation is the gold-standard feature when Codex and Gemini are present. When the user's `tools.codex_available` or `tools.gemini_available` is `false` (their CLI isn't installed/authenticated), the pipeline degrades cleanly to whatever subset is available rather than blocking. Single-model runs are valid output, not a failure mode — they just record the degradation explicitly in the report's methodology section.
4. **Quality governs, not the clock.** Typical 15–30+ minutes. Longer is fine if the research warrants it.

# Model selection

```
claude_model: opus        # Agent tool model parameter
codex_model: gpt-5.5      # Codex CLI default (don't override with -m)
codex_fallback: none       # If configured gpt-5.5 is unavailable, mark Codex inactive
gemini_model: (default)    # Gemini CLI default model (don't override with -m)
```

Always use the strongest reasoning model available on each side. Three major consumer AI models with different training data and architectures — convergence despite independence is the highest-confidence signal.

# Pipeline

Ten phases (0–9). Pre-flight and interactive scoping, then autonomous execution.


## When something goes wrong

When a step in this skill fails or needs a workaround, update this skill file with what you learned BEFORE continuing to the next step. Add failure modes, correct wrong assumptions, fix timing estimates. This takes 30 seconds and prevents the same friction next time.


## Phase 0: Pre-flight

**Goal**: Ensure all tools and infrastructure are ready before scoping begins.

Run these in parallel:

1. **Clean scratch directory**:
   ```bash
   rm -rf /tmp/research && mkdir -p /tmp/research
   ```

2. **Preload deferred tools** — single batched ToolSearch call:
   ```
   ToolSearch: select:mcp__qmd__query,mcp__qmd__get,mcp__qmd__multi_get,TaskCreate,TaskUpdate,WebSearch,WebFetch
   ```
   This eliminates ad-hoc tool loading throughout the run.

3. **Set tab title**:
   ```bash
   MY_TTY=$(ps -o tty= -p $PPID 2>/dev/null | tr -d ' ') && echo "research: {topic}" > "/tmp/claude-title-${MY_TTY}"
   ```

4. **Read tool availability from config**:
   ```bash
   PROJECT_KEY=$(pwd | sed 's|[^a-zA-Z0-9]|-|g')
   CONFIG="$HOME/.claude/projects/$PROJECT_KEY/config.json"
   CODEX_FLAG=$(python3 -c 'import json,sys; print(str(json.load(open(sys.argv[1])).get("tools",{}).get("codex_available", False)).lower())' "$CONFIG" 2>/dev/null || echo false)
   GEMINI_FLAG=$(python3 -c 'import json,sys; print(str(json.load(open(sys.argv[1])).get("tools",{}).get("gemini_available", False)).lower())' "$CONFIG" 2>/dev/null || echo false)
   ```

   Set `CODEX_ACTIVE` and `GEMINI_ACTIVE` based on the config flags. These gate Phase 3b and 3c launch as well as Phase 3d wait.

5. **Codex pre-flight (only if `CODEX_FLAG=true`)**:
   ```bash
   which codex && codex exec --full-auto --sandbox danger-full-access "Reply with OK" 2>&1
   ```
   Uses the global default model (bare `gpt-5.5` per `~/.codex/config.toml`) — only model variant accessible via CLI on a ChatGPT account.

   | Result | Action |
   |--------|--------|
   | Returns OK | `CODEX_ACTIVE=true`. Proceed with Codex. |
   | `which codex` fails | `CODEX_ACTIVE=false`. Print "Codex unavailable — pipeline will run Claude + Gemini only" and continue. (Don't block — the user may have intentionally not installed Codex.) |
   | Auth/model error | If interactive: "Codex needs login. Run `codex login`, then tell me to continue." Pause and wait. If autonomous: `CODEX_ACTIVE=false` and continue. |

   If `CODEX_FLAG=false`, skip the pre-flight entirely and set `CODEX_ACTIVE=false`.

6. **Gemini pre-flight (only if `GEMINI_FLAG=true`)**:
   ```bash
   which gemini && gemini -p "Reply with OK" --output-format text 2>&1
   ```

   | Result | Action |
   |--------|--------|
   | Returns OK | `GEMINI_ACTIVE=true`. Proceed with Gemini. |
   | `which gemini` fails | `GEMINI_ACTIVE=false`. Print "Gemini unavailable — pipeline will run Claude + Codex only" and continue. |
   | Auth error | If interactive: "Gemini needs login. Run `gemini` interactively to authenticate, then tell me to continue." Pause and wait. If autonomous: `GEMINI_ACTIVE=false` and continue. |

   If `GEMINI_FLAG=false`, skip the pre-flight entirely and set `GEMINI_ACTIVE=false`.

Print: `[0/9] Pre-flight complete — tools loaded, Codex {active/inactive}, Gemini {active/inactive}`. If both Codex and Gemini are inactive, also print: "Single-model run (Claude only). The report will note the reduced triangulation in its methodology section."

## Phase 1: Scoping

**Goal**: Turn the research question into a precise brief.

### Input handling
- `/research [topic]` — use as starting point
- `/research` — ask what to research
- Mid-conversation — infer and confirm

### Establish (via AskUserQuestion, one at a time)

1. **Research question** — restate. "Is this the right framing?"
2. **Scope boundaries** — time range, geographic focus, sector, species. Propose defaults.
3. **Audience** — who reads this? **Critical: if the audience is anyone other than the user themselves, the entire report framing must be tailored to that audience.** Ask: who will read this, what do they already know, what decisions will this inform? This governs tone, assumed knowledge, currency, what sections to include/exclude, and what context is helpful vs. noise.
4. **Sub-questions** — present 3–5. "These are the threads I'd research — anything to add or remove?" Last checkpoint before autonomous execution.

Skip where obvious from context. Use **multi-perspective pre-questioning** (Stanford STORM): before generating sub-questions, consider what angles different domain experts would bring.

### Domain detection

Read `references/domain-routing.md`. Detect domain, note source guidance for Phase 3.

### External model prompts — generate and deliver to clipboard

Generate **one unified prompt** for the user to paste across all three external platforms (Claude Desktop Research, ChatGPT Deep Research, Gemini). One prompt, three independent passes — this is faster and produces comparable results to tailored prompts.

**Author context — read from `config.json`, do NOT hardcode.** External research models work better when they know who's asking (a domain expert vs. a layperson), but baking a fixed identity into the prompt template causes drift — Codex notably latches onto identity context and researches the *person's field* instead of the actual topic (v1 run regression). Construct the author-context line at runtime:

```bash
PROJECT_KEY=$(pwd | sed 's|[^a-zA-Z0-9]|-|g')
CONFIG="$HOME/.claude/projects/$PROJECT_KEY/config.json"
if [ -f "$CONFIG" ]; then
  USER_NAME=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("user",{}).get("name","").strip())' "$CONFIG" 2>/dev/null || echo "")
  USER_ROLE=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("user",{}).get("role","").strip())' "$CONFIG" 2>/dev/null || echo "")
fi
```

If both `USER_NAME` and `USER_ROLE` are non-empty, substitute the line:

```
Author context (for tone/audience calibration only — do NOT research this person's field): <USER_NAME> — <USER_ROLE>.
```

into the prompt template's `{{AUTHOR_CONTEXT_LINE}}` placeholder. If either is empty (newcomer who skipped Q1, or pre-`user` config), substitute the empty string — the prompt works fine without author context, and an absent line is strictly safer than a wrong one.

**Prompt design:**

The unified prompt should:
- Specify the exact scope, sub-questions, and what existing material already covers
- Ask for ALL quantitative measurements from each paper
- Ask for obscure/regional publications, institutional reports, non-English literature
- Request identification of published challenges, rebuttals, or replication failures
- List 5–10 specific papers or authors to search for
- Ask each model to distinguish hard evidence from inference
- Request explicit confidence flags (CONFIRMED / PARTIALLY SUPPORTED / UNCERTAIN / CONTRADICTED)
- Ask what findings a typical pipeline might miss
- Specify output format: full citations with DOIs, equipment details, quantitative specifics

**Delivery — clipboard workflow:**

Write the prompt to `/tmp/research/unified_prompt.md`, then copy to clipboard:

```bash
pbcopy < /tmp/research/unified_prompt.md
```

Print:
```
External research prompt ready — on your clipboard.

Paste into Claude Desktop (Research mode), ChatGPT (Deep Research), and Gemini.
Same prompt, three independent passes.

Drop the outputs back when they're done — I'll run comparison analysis to integrate anything we missed.
```

**Iterative improvement**: After each run, compare what each model found vs missed. Update prompt templates in `references/external-model-prompts.md` (create if needed) to strengthen weak areas for next time.

### Launch

Print: `[1/9] Scoping complete — {N} sub-questions`

Then: "Starting deep research (Claude + Codex + Gemini). Typical runtime 15–30+ minutes depending on topic. I'll scan the vault, run parallel web research across the three available models, synthesise, and verify claims. When done I'll save the report to your research folder and create a follow-up task via /todo."

## Phase 2: Deep Vault Scan

**Goal**: Surface everything in the vault that relates to the research question. The vault is a primary resource — be thorough.

### 2a.0: Paperpile mirror first (curated literature)

**Goal**: extract Simon's curated prior literature for this topic from the Paperpile mirror (`02_MARINE MEGAFAUNA/REFERENCE LIBRARY/Paperpile Library/`) BEFORE broad-vault discovery. The mirror is the high-trust source — papers Simon has deliberately added to his library.

**Pre-flight — build-status gate.** Read `02_MARINE MEGAFAUNA/REFERENCE LIBRARY/Paperpile Library/_meta/build-status` (small JSON). If `status != "ready"` (mid-rebuild, error state, missing file), set `paperpile_coverage: unavailable`, SKIP this section entirely, and run §2a unchanged.

**Steps:**

1. **Paperpile-scoped QMD discovery.** Run 4–6 `mcp__qmd__query` calls against `collections: ["paperpile"]` only:
   - Per sub-question: one `lex` + one `vec` (intent-tagged)
   - Overall question: one `vec`
   - 1–2 lateral framings if the sub-questions are narrow
   - Apply the same QMD gotchas as §2a below — but generalise the vec0 fallback: **any vec/hyde failure** (vec0 module unavailable, `node-llama-cpp` Metal context creation errors, network) falls back to lex-only.

2. **Seed-set extraction — paper notes ONLY.** Filter QMD hits with these guards (per /codex-review v5 MC1/UR1):
   - Path must match `qmd://paperpile/papers/*.md` (drop `authors/`, `labels/`, `_meta/`).
   - Frontmatter must have `type: paper` (defensive; the path filter is usually sufficient).
   - Dedupe by `paperpile_pub_id` (or slug) across queries.
   - QMD scores in the paperpile collection saturate ≥0.9 across both true paper hits and cross-reference proximity. **Do not use raw score as the coverage gate** — count distinct paper notes that survive filter + brief relevance check.
   - Read the filtered top 10 in full via `mcp__qmd__get` (~5–7 KB per paper note).

3. **Coverage threshold decision.**
   - Threshold: **≥6 distinct paper notes survive the filter + relevance check**.
   - **`dense`:** §2a still runs but at REDUCED scope (see §2a below). §2b graph expansion proceeds from the curated seed set. §3 external research still runs — independent quality check.
   - **`sparse`:** §2a runs full broad-vault. The few in-library hits ARE still included as a "Curated subset" in the briefing.

4. **One-hop in-library citation expansion — DEFERRED.** Parent spec §Use case 1 envisions following each seed's `## References in library` + `## Cited by in library` wikilinks one hop out. Those sections are currently placeholder text — `note_writer.write_paper_note` emits no actual citation wikilinks; `citation_graph_built` in paper-note frontmatter is `null` for all 8,808 records. **Document this gap in the briefing** ("In-library citation expansion: deferred until citation-graph rendering ships in note_writer.py — currently no `References in library` / `Cited by in library` wikilinks are populated") so downstream consumers know it's missing, not silently degraded.

Print: `[2a.0] Paperpile mirror — {N} curated seeds (coverage: dense|sparse|unavailable)`

### 2a: Broad discovery

Run 10–15 QMD queries across multiple framings (or 4–6 REDUCED queries if §2a.0 returned `dense` coverage — see Reduced-mode-in-dense-coverage note below). Batch into 3–4 `mcp__qmd__query` calls:

- Per sub-question: one `lex` + one `vec` each
- Overall question: one `vec` + one `hyde`
- 2–3 lateral queries: synonyms, adjacent domains

All with `intent` parameter. Use `minScore: 0.5`. Deduplicate. Read top 15–20 hits in full via `mcp__qmd__get` or `mcp__qmd__multi_get` (8–10 in reduced mode). Do not abbreviate or excerpt — read the full documents.

**Path-dedupe against the Paperpile mirror.** §2a queries `obsidian` (the root vault collection), whose pattern `**/*.md` covers the Paperpile Library subtree — so a default broad search WILL return paperpile hits via `qmd://obsidian/02-marine-megafauna/reference-library/paperpile-library/...`. **Filter those out** — §2a.0 already handled the mirror; §2a's job is to surface NON-mirror content (project notes, manuscripts, transcripts, IDEAs, prior research outputs, daily notes, role notes). Match both the `qmd://obsidian/02-marine-megafauna/reference-library/paperpile-library/` slugified prefix and the literal path `02_MARINE MEGAFAUNA/REFERENCE LIBRARY/Paperpile Library/`.

**Reduced mode in dense coverage.** When §2a.0 returned `dense`, run §2a at reduced scope: 4–6 broad-framing queries, read top 8–10 in full. The vault still has substantial non-mirror content that's worth surfacing (board minutes, meeting transcripts, project IDEAs); skipping §2a entirely would lose that.

**QMD query gotchas** (from v1 run + operational experience):
- Hyphenated terms (e.g. "photo-ID") are parsed as negation in `vec`/`hyde` queries. Use "photo identification" or "photo ID" instead.
- `hyde` queries cannot be in the same batch as `vec`/`lex` queries that contain hyphens — run separately if needed.
- **vec0 module intermittently unavailable**, plus **other non-lex failures**: `vec` and `hyde` queries may fail with "no such module: vec0", `node-llama-cpp` Metal context creation errors, or network errors while `lex` queries work fine. If any vec/hyde batch errors for ANY reason, fall back to `lex`-only QMD queries supplemented by Grep/Glob searches of likely vault folders. Do not block the pipeline on vec0 or any vec/hyde-runtime availability.
- If a batch fails, retry with simplified queries rather than debugging syntax.

### 2b: Graph expansion

For top 10 results, extract `wikilinks` and follow:
- Read each linked file, score relevance
- If relevant, follow its links too (max 2 hops)
- Track visited files (cycle detection)
- Cap at 30 files if >50 found. Score by: keyword match in title, link distance (1 hop > 2), file recency. Skip `06_ARCHIVE/` and `00_INBOX/` unless direct QMD hits.

This step is mandatory. The vault's wikilink structure encodes relationships that QMD search alone can miss.

### 2c: Context packaging

Write vault briefing to `/tmp/research/vault_briefing.md` via Bash (heredoc or cat — do NOT use the Write tool, which requires a prior Read on the path):

```bash
cat > /tmp/research/vault_briefing.md << 'EOF'
... briefing content ...
EOF
```

Include, in this order:

1. **`paperpile_coverage: dense|sparse|unavailable`** — set by §2a.0 outcome.
2. **`## Curated subset (Paperpile mirror)`** — list the seed-set paper notes from §2a.0 with brief annotations: title, year, key claim (1–2 sentences from the abstract), file ref. Appears BEFORE the per-sub-question key findings. If `paperpile_coverage: unavailable`, add a one-line note explaining why this section is empty.
3. **`## Key findings by sub-question`** — per sub-question section. **For each sub-question, copy the relevant curated seeds into its own findings block** with file refs and key claims. The top-of-briefing section alone is not enough because Phase 3a Claude subagents see only sub-question excerpts; they need the curated seeds inline.
4. **`## Coverage assessment`** — what's covered by in-library + vault + what needs web research.
5. **`## Contradictions / gaps`** — disagreements, TODO/VERIFY markers, missing pieces.
6. **`## In-library citation expansion: deferred`** — one-line note that one-hop expansion from seed papers' `## References in library` / `## Cited by in library` sections is not yet wired (placeholder text only; `citation_graph_built: null` across all paper notes). Surfaces the gap explicitly so downstream consumers don't assume coverage.
7. **`## Key files list`** — full paths of all files read across §2a.0 + §2a + §2b.

**Size guard**: If >10,000 words, summarise per sub-question. Note what was summarised — flag in Follow-up Questions.

Print: `[2/9] Vault scan — {N} files found, briefing {N} words`

### 2d: Communications scan (parallel with 2a.0–2c)

**Goal**: Surface unpublished insights, decisions, and expert opinions from email and Slack correspondence. Colleagues often share field observations, preliminary data, and methodological opinions that never make it into published sources.

Launch this as a background Agent (model: "opus") at the start of Phase 2 — in parallel with §2a.0 (not blocked on it). The agent receives the research question, sub-questions, and scope boundaries from Phase 1. (Pre-v0.5.9 wording said "at the same time as 2a"; with 2a.0 inserted before 2a, launching at the same time as 2a would delay comms by the duration of 2a.0. Default: launch at the start of Phase 2.)

**The comms scan agent should:**

1. **Gmail search** — 3–5 queries using `mcp__claude_ai_Gmail__gmail_search_messages`:
   - Topic keywords + key collaborator names (if known from vault scan or scoping)
   - Species/location-specific terms
   - Time-bounded to the research scope (e.g. `after:2024/01/01`)
   - Read the top 5–10 most relevant threads via `mcp__claude_ai_Gmail__gmail_read_thread`

2. **Slack search** — 2–3 queries using `mcp__claude_ai_Slack__slack_search_public_and_private`:
   - Same topic keywords, adapted for conversational language
   - Read the top 3–5 most relevant threads via `mcp__claude_ai_Slack__slack_read_thread`

3. **Score and filter** — for each thread, score relevance (0–10) against the sub-questions. Only include threads scoring 6+ in the briefing. Note the count of lower-relevance threads at the bottom ("Also found N threads below relevance threshold — available on request").

4. **Extract and write** — produce `/tmp/research/comms_briefing.md` containing:
   - Key insights by sub-question (with sender/date attribution)
   - Unpublished data, field observations, or expert opinions
   - Decisions or agreements that affect the research topic
   - Contradictions with vault content or published literature
   - **Privacy note**: Include the substance of insights, not personal details or off-topic content

**Integration**: The comms briefing is appended to the vault briefing in Phase 2c (re-run context packaging after comms agent completes if it finishes after 2c). Both feed into Phase 3 model prompts.

**Graceful degradation**: If Gmail or Slack MCP tools are unavailable or return errors, log the failure and proceed without comms input. This phase is valuable but not blocking.

Print: `[2d] Comms scan — {N} Gmail threads, {N} Slack threads reviewed`

## Phase 3: Parallel Research

**Goal**: Claude subagents, Codex, and Gemini research simultaneously, all informed by vault.

### 3a: Claude subagents

Read `references/subagent-prompt.md`. Launch one subagent per sub-question (3–5) via Agent tool with `model: "opus"`.

Each subagent gets:
- Short global summary of the research brief
- Vault briefing excerpt for its sub-question only (not full briefing) — **including the curated seeds for this sub-question inlined per §2c step 3**
- Relevant comms insights for its sub-question (from comms briefing, if available)
- Cross-cutting caveats from vault scan
- Year range, domain-specific source guidance
- **Curated-seeds instruction (when `paperpile_coverage: dense`):** "The papers listed in the `## Curated subset (Paperpile mirror)` block in your excerpt are Simon's curated prior literature for this topic. Treat these as high-priority sources. Your job is to find gaps, conflicts, newer work that post-dates these, and non-library context — not to re-cover ground these already establish."

Each produces (with standardised naming):
1. Research note (500–800 words) → `/tmp/research/claude_{NN}_{slug}.md` (e.g. `claude_01_automation_gaps.md`)
2. Structured claim registry → `/tmp/research/claims_{NN}.md` (e.g. `claims_01.md`)
3. Source list → `/tmp/research/sources_{NN}.md` (e.g. `sources_01.md`)

Numbering `{NN}` is zero-padded (01, 02, ...) and matches the sub-question order. Slug is a short lowercase descriptor.

All launch in parallel as background agents.

### 3b: Codex CLI (simultaneous, only if `CODEX_ACTIVE=true`)

Skip this entire phase if Phase 0 set `CODEX_ACTIVE=false`. Otherwise:

Read `references/subagent-prompt.md` for the Codex prompt template. Build prompt at `/tmp/research/codex_prompt.md` with full vault briefing and comms briefing (Codex is a single call covering all sub-questions).

Launch in background:
```bash
codex exec --full-auto --sandbox danger-full-access \
  "Read /tmp/research/codex_prompt.md and follow the instructions exactly." \
  2>&1 | tee /tmp/research/codex_findings.md
```

**Model:** bare `gpt-5.5` from `~/.codex/config.toml` (only model variant accessible via CLI on a ChatGPT account — `-fast`/`-pro` return 400). xhigh reasoning from config. Do not pass `-m` or `-c model=...`.

Timeout: 600000ms.

Fallback chain: if Codex errors, retry once → alert user.

### 3c: Gemini CLI (simultaneous, only if `GEMINI_ACTIVE=true`)

Skip this entire phase if Phase 0 set `GEMINI_ACTIVE=false`. Otherwise:

Build prompt at `/tmp/research/gemini_prompt.md` with full vault briefing and comms briefing. Same sub-questions as Codex but with its own open-ended framing — do NOT copy the Codex prompt. Each external model should approach the research independently.

Launch in background:
```bash
gemini -p "" --output-format text --yolo < /tmp/research/gemini_prompt.md 2>&1 | tee /tmp/research/gemini_findings.md
```

Timeout: 600000ms.

### 3d: Wait for launched workers

**Wait for every worker that was actually launched in Phase 3a/3b/3c — not for workers that were skipped at launch.** Claude subagents always run (3a is unconditional). Codex (3b) only runs if `CODEX_ACTIVE=true`; if it was skipped, do not block waiting on it. Gemini (3c) only runs if `GEMINI_ACTIVE=true`; same rule.

While waiting (if some workers finish first), read completed outputs to prepare for synthesis. But do not write the report until all *launched* workers are done. **Wait for background task completion notifications**, not just file-existence checks — subagent output files may be written incrementally, and late-arriving findings can contain critical insights that require report revision if missed.

If only Claude subagents launched (both Codex and Gemini inactive), this phase finishes immediately as soon as the subagents return. Synthesis proceeds with single-model output and records the degradation in Phase 4 — see "Methodology section in degraded mode".

### 3e: Output validation (Codex and Gemini)

After each external model completes, check for topic drift:

```bash
# Check for 3+ expected keywords from the sub-questions
grep -ci "keyword1\|keyword2\|keyword3" /tmp/research/codex_findings.md
grep -ci "keyword1\|keyword2\|keyword3" /tmp/research/gemini_findings.md
```

| Result | Action |
|--------|--------|
| 3+ keyword matches | Output is on-topic. Proceed. |
| <3 keyword matches | **Off-topic.** Restart with strengthened prompt (see below). |
| Empty file | Model failed. Retry once. If still fails, alert user. |

**Strengthened prompt for restart**: Prepend to the prompt:
```
CRITICAL: This research is about [TOPIC]. It is NOT about [detected off-topic subject].
Do NOT research [off-topic subject]. Focus exclusively on [TOPIC].
```

Maximum 2 attempts per model. If both attempts go off-topic, alert user and proceed without that model.

### Error handling

| Failure | Action |
|---------|--------|
| Codex off-topic | Restart with strengthened prompt. Max 2 attempts. |
| Gemini off-topic | Restart with strengthened prompt. Max 2 attempts. |
| Codex fails entirely (after retries) | Alert user. Proceed with whatever else launched (Claude + Gemini, or Claude-only). |
| Gemini fails entirely (after retries) | Alert user. Proceed with whatever else launched (Claude + Codex, or Claude-only). |
| Both external models fail at runtime | Alert user. Proceed Claude-only and record degradation in Phase 4 methodology. |
| Codex / Gemini *not active* per Phase 0 | Not a failure — proceed with the active subset. Phase 4 records the degradation in methodology. |
| Individual subagent fails | Note gap. Sub-question still has whatever external model coverage was active. |

Graceful degradation: three-model → dual-model → single-model. The pre-flight (Phase 0) and the runtime failure handler (this table) both produce the same effect — fewer models, with the report explicit about which ran. Never silently drop a model that was launched without recording it.

Print: `[3/9] Research complete — {N} sources found`

## Phase 4: Synthesis

**Goal**: Merge all findings into a reader-first report.

### 4a: Gather inputs

Read claim registries first (`/tmp/research/claims_*.md`) — these are the structured source of truth for attribution. Then read the full research notes (`/tmp/research/claude_*.md`), Codex findings, and Gemini findings for context, narrative, and nuance. Also read vault briefing and source lists.

Merge and deduplicate sources across all three models' workers.

### 4b: Write report

Read `references/report-template.md`. Write the report following that structure.

**Methodology section in degraded mode.** If `CODEX_ACTIVE=false` or `GEMINI_ACTIVE=false`, add a brief paragraph in the report's methodology section noting the reduced triangulation. Examples:

- Both external models inactive: *"This run used Claude only — Codex and Gemini CLIs were not available on the user's machine. Single-model findings have been validated against vault sources and primary literature, but the cross-model triangulation that normally surfaces blind spots was not possible. Treat this as a one-pass research output."*
- One external inactive: *"This run used Claude + {Codex|Gemini}. The other external model was unavailable, so the dual-model triangulation may have missed blind spots a third model would have caught."*

This is a methodology disclosure, not an apology — single-model and dual-model runs are valid; the note exists so a future reader knows the rigour of the pass.

**Synthesis principles** (in priority order):
1. **Write for the audience, not the user or the audit trail.** If the audience is external (e.g., field researchers, funders, collaborators), the report must be a standalone document they can use without vault context. Remove: internal methodology notes, model attribution ("[CONFIRMED by Codex]"), references to "the previous briefing note", partner recommendations the audience would find patronising, and cost/funding framing if not requested. Use the audience's local currency. Include only context they needed during research, not context the user needed during research.
2. **Claim-level attribution** — every finding traces to a specific source via the claim registries. But attribution goes in the References section, not inline as "[HIGH CONFIDENCE — confirmed by X, Y, Z]".
3. **Source tiering** — per `references/domain-routing.md`.
4. **Surface conflicts explicitly** — present both positions when sources disagree.
5. **Confidence scoring**: High (multiple corroborating credible sources), Medium (single credible or multiple lower-quality), Uncertain (inference, extrapolation, conflicting). For external-facing reports, express confidence through language ("well-established", "limited data suggest") rather than explicit labels.
6. **Model convergence is a triangulation cue, not evidence.** If multiple models surface the same claim, inspect underlying sources — don't treat agreement as additional confidence. Model convergence notes are internal — omit from external-facing reports.

### 4c: Self-audit against external models

1. Re-read Codex findings in full
2. Re-read Gemini findings in full
3. Verify each model's substantive findings appear in draft
4. If omitted: add it or document why
5. Write Model Divergence appendix covering three-way comparison:
   - **All three agree** — highest confidence triangulation
   - **Two of three agree** — note which two and which dissents
   - **Unique to one model** — flag with context, these are often the most interesting findings

Print: `[4/9] Synthesis draft — {N} words`

## Phase 5: Claim Verification

**Goal**: Spot-check top claims before delivery.

Select **5 most consequential verifiable claims**. Prioritise: claims driving conclusions, statistics, single-model findings, Medium/Uncertain confidence.

**Cross-model verification shortcut**: If all three models (Claude, Codex, Gemini) cite the same primary source with consistent findings, that claim is pre-verified. Two-of-three agreement gets partial credit but should still be verified if the claim is consequential. Focus Phase 5 verification budget on: single-model findings, statistics without corroboration, vault contradictions, and claims rated Medium/Uncertain.

For each selected claim, WebSearch against primary sources:
- Claim (quote) → Verdict (Confirmed/Partial/Unsupported/Contradicted) → Source (URL) → Note

**Actions**: Contradicted → fix report. Unsupported → downgrade confidence. Partial → add nuance. Confirmed → bump confidence.

Also spot-check 3–5 URLs via WebFetch. Flag dead links. Can parallelise via subagents.

Print: `[5/9] Verification — {N} claims checked, {N} corrected`

### 5b: Reference document comparison (optional)

If the user provides a reference document — a peer-reviewed review paper, book chapter, or authoritative report on the same topic — run a structured comparison against the draft. This step catches gaps that web searches miss: citation errors, framing improvements, methodological caveats, quantitative benchmarks, and missing nuance from domain specialists.

**When to use:** When the user provides a specific document to "check against", or when the topic overlaps with a known authoritative review. This is not a standard step — it's triggered by the user or suggested by the orchestrator if a relevant reference is identified during the vault scan.

**How to run:** Launch an Opus subagent with the full reference document and the full draft. The subagent compares them structurally, producing:

1. **Missing content** — findings from the reference that are relevant but absent from the draft
2. **Contradictions** — where the reference and draft disagree (including possible citation errors)
3. **Framing improvements** — where the reference's treatment suggests a better way to present material
4. **Key references to add** — prioritised by relevance

Write output to `/tmp/research/{reference_slug}_comparison.md`.

**Why this is distinct from other verification:**
- Phase 5a (claim verification) checks individual facts against web sources
- External model passes (Claude Desktop, ChatGPT) do general enrichment
- Reference document comparison does **structural gap analysis** against a specific authoritative source — it catches the kind of methodological caveats and domain-expert framing that only appear in specialist reviews

**Lessons from v3 run (2026-03-23):** Comparing a whale shark climate chapter against Rummer et al. (2022) caught: a citation error (wrong author for denticle corrosion study), a key quantitative anomaly (whale shark Q10 1.3–1.4 vs typical elasmobranch 2–3 — worth discussing but missed by all web-search workers), meta-analytic context that nuanced the OA findings, a 10-species literature bias that all subagents extrapolated from without flagging, and the paleoclimatic overturning argument that strengthened the conclusion. Several of these would not have been found by any number of web searches.

### 5c: Reference verification (standard for enriched drafts)

After integrating findings from Phase 5b reference comparisons and/or external model outputs, verify all newly added citations that came from external sources (ChatGPT, Claude Desktop, or reference document comparisons). These sources can hallucinate or misattribute citations.

**When to run:** Always, if Phase 5b or external model comparisons introduced new references. Skip only if the draft used exclusively pipeline-sourced references with no external enrichment. Also run when the research output is scientific in nature (literature reviews, species assessments, conservation analyses) — even pipeline-sourced citations can have errors.

**Step 1 — Automated API check:** If the report has a References section, invoke the bundled `/verify-citations` skill against the report path. The skill queries Semantic Scholar, CrossRef, and OpenAlex to verify each reference exists with correct metadata. Takes ~1s per reference. The skill writes its report to `/tmp/research/{topic}_citation_report.md` (or wherever it advertises in its output).

**Step 2 — Manual verification of flagged items:** For any NOT_FOUND or PARTIAL_MATCH results from the script, plus any references the script couldn't parse, WebSearch to confirm: (a) the paper exists, (b) author names are correct, (c) journal/year/volume match, (d) the claimed finding actually appears in that paper.

**What to check for:**
- **Hallucinated author names** — the most common failure mode. Subagents and external models find real findings but invent plausible author names. Three instances caught in v3 run ("Lutz et al." for Dziergwa, "Park & Lee" and "Vo et al." for Ahn et al.).
- **Correct paper, wrong species** — a real paper is cited but attributed to the wrong species. In v4 run, ChatGPT cited a three-lineage population genomics paper (Wagner et al. 2024, *Current Biology*) as being about whale sharks — it was actually about white sharks (*Carcharodon carcharias*). Species-level attribution needs verification, not just author-level.
- **Conflated papers** — two different papers merged into one citation, or one paper split into two.
- **Framing drift** — the paper is real but the claimed finding is a mischaracterisation (e.g., "population decline" when the paper describes "seasonal movement shifts").
- **Wrong journal/year** — especially common when the same author group publishes multiple papers on similar topics. Four journal citations were wrong in the v4 run (Boyd in BMC not Zoologica Scripta; Landau in Zootaxa not Rivista Italiana; Gayford in Evolution & Development not Evolution; Kawaguchi in GigaScience not Genome Biology and Evolution).

Report verdicts as: CONFIRMED, CONFIRMED WITH CORRECTIONS, LIKELY REAL, NOT FOUND.

Fix the draft for any NOT FOUND citations before delivery. For CONFIRMED WITH CORRECTIONS, update the reference entry and check that the in-text citation context still matches.

**Critical: verify external model corrections too.** External model comparisons (Phase 5b) can themselves contain errors. In the v4 run, Claude Desktop incorrectly claimed that Wang et al. (2017) was a Little Skate paper and that the draft's closest-relative claim was wrong — but the paper is actually a Nebrius mitogenome study that supports the draft. Applying that "correction" would have introduced an error. Always verify corrections from external models with the same rigour as the original claims.

### 5d: Skill improvement from external model output (standard)

Every time an external model output is integrated (Claude Desktop, ChatGPT, or a reference document comparison), treat it as a **learning opportunity for the skill itself**. Anthropic and OpenAI invest enormous resources in their research and reasoning capabilities — systematically extracting what they do better than our pipeline improves the skill over time.

**After each external comparison, ask these four questions:**

1. **What did they find that we missed?** Categorise the gaps:
   - Papers we should have found (→ improve search terms in subagent prompts)
   - Quantitative detail from papers we cited but didn't fully extract (→ strengthen extraction instructions)
   - Foundational references our year-range filter excluded (→ adjust foundational reference instruction)
   - Epistemic nuances we glossed over (→ add to synthesis principles)

2. **How did they structure their search differently?** Look at:
   - Search terms or framing they used that our subagents didn't
   - Lateral connections they made (cross-taxa, cross-domain)
   - Whether they searched for reviews/meta-analyses that our subagents skipped

3. **What quality patterns did they apply that we didn't?** Examples:
   - Distinguishing evidence from inference more carefully
   - Flagging contested findings our subagents cited uncritically
   - Contextualising values against known ranges
   - Noting methodological limitations of cited studies

4. **What should change in the skill? Apply it now.** For each gap identified:
   - If it's a subagent prompt issue → update `references/subagent-prompt.md` **immediately**
   - If it's a synthesis principle → update Phase 4b synthesis principles **immediately**
   - If it's a verification checklist gap → update Phase 5c **immediately**
   - If it's a search strategy → note in the lessons section for the orchestrator
   - If it's a recurring pattern across 2+ runs → promote to a permanent skill instruction

**Do not defer improvements to a future session or wait for the user to ask.** If the self-assessment identifies something that should be fixed in the skill, fix it in the same session. The whole point of this step is that every run leaves the skill better than it found it.

**Write a brief `## External model learnings` section in the post-run self-assessment (Phase 9)** documenting what was learned and what was changed. This creates a running record that compounds over time.

**The goal is not just to fix this draft — it's to make the next run better.** Each external model comparison should leave the skill slightly improved. Over many runs, this produces a pipeline that incorporates the best practices of all three major AI research systems.

## Phase 6: Voice Match

**Goal**: Ensure the output matches the user's writing voice when there's an established voice to match. This phase is **gated** — it runs only when a relevant voice reference exists.

### 6a: Locate voice reference

Search for a voice reference file relevant to the output. Standard locations:
- `<vault>/AI_WORKFLOW/CLAUDE/Voice References/Voice Reference — *.md`
- `<project-folder>/Voice Reference — *.md`

If multiple matches exist, pick the one whose filename or content best matches the research topic and audience.

**Skip this entire phase** if:
- No voice reference file is found, OR
- The output is short (<2,000 words) — voice matching matters most for long-form prose (chapters, articles, grant applications), and
- `features.is_simon` is `false` AND no voice reference file exists.

For substantial prose (>2,000 words) where a voice reference would help but none exists, leave a one-line note at the bottom of the report: "Voice not matched — no reference available. See `guides/ai-assisted-writing.md` for how to create one."

### 6b: Voice comparison

Launch an Opus subagent with both the voice reference and the draft. The subagent identifies specific passages that don't match the author's voice, producing a numbered list of edits with: PASSAGE → ISSUE → SUGGESTED REWRITE.

Focus on the most impactful issues:
- AI-tell words/phrases from the voice reference's "What NOT to do" list
- Wrong tone (too dramatic, too casual, too hedged)
- Wrong argumentation structure (conclusion-first when it should be evidence-first)
- Missing author-specific patterns documented in the voice reference (e.g., a particular pivot phrase the author uses, a closing-line pattern)

Write output to `/tmp/research/voice_review.md`.

### 6c: Apply voice edits

Apply all edits that improve voice matching without changing factual content. This is autonomous — don't ask the user to approve individual voice edits. The goal is to deliver prose that sounds like the author wrote it.

Print: `[6/9] Voice matched — {N} edits applied`

## Phase 7: Polish

**Goal**: Grammar, spelling, and AI writing detection sweep. Standard step, always run.

Run `/polish` on the output file:
1. LanguageTool (`--language en-GB`) for grammar and spelling
2. Vale (write-good + proselint) for style
3. AI writing detection pass

Triage results:
- **Fix** clear errors (spelling, grammar, punctuation) — apply automatically
- **Skip** domain terms, markdown syntax, scientific register conventions (passive voice, technical jargon)
- **Consider** only genuinely ambiguous items — for autonomous runs, apply if the fix is clearly an improvement

For scientific writing, be tolerant of passive voice, technical terminology, and formal register. Only flag genuine errors and AI writing patterns.

### Reference list integrity check

After polish, verify the reference list matches in-text citations:

1. Extract all in-text citations (Author Year) from the prose sections
2. Extract all entries from the References section
3. Flag: (a) in-text citations with no matching reference entry, (b) reference entries not cited in-text
4. Fix orphans — add missing reference entries or remove uncited ones

This catches errors introduced by multi-pass enrichment (pipeline + external model additions + voice edits that may remove sentences containing citations).

### Wikilink validation

If the output uses `wikilinks` (e.g., book chapters with cross-references):

1. Grep for all `[[` links in the file
2. For each target, verify the file exists in the vault via Glob
3. Flag any broken links — mistyped filenames, changed chapter titles, or targets that don't exist

Fix broken links before delivery. This is a 30-second check that prevents silent failures in Obsidian.

Print: `[7/9] Polished — {N} fixes applied`

## Phase 8: Delivery

### Save report

Read `vault.path` from `~/.claude/projects/<project-key>/config.json`. Write the report to a `RESEARCH/` subfolder of the vault — typically `<vault>/RESEARCH/` or `<vault>/AI_WORKFLOW/RESEARCH/` depending on the user's layout. Create the folder if missing:

```bash
mkdir -p "<vault>/RESEARCH"
```

Write to `<vault>/RESEARCH/Research — {Topic}.md`.

### Follow-up task

Invoke the bundled `/todo` skill to create a review task. `/todo` routes to whichever task manager the user configured during /onboard (Things 3, Todoist, Apple Reminders, or vault TODO.md). Pass:

- Title: `Review: Research — {Topic}` (under 60 chars)
- Notes: vault link to the report + research question + TL;DR bullets + a Claude Code prompt for resuming work cold

If `/todo` is unavailable, fall back to writing the review task to `05_AI WORKFLOW/OUTPUTS/Daily Log.md` under `## For review`. Do NOT write to `<vault>/TODO.md` — that file was retired 2026-05-15 in Simon's vault.

### Terminal summary

```
Research complete: {Topic}

Report: <vault>/RESEARCH/Research — {Topic}.md
Sources: {X} web ({Y} Claude, {Z} Codex, {W} Gemini) + {V} vault files
Duration: ~{N} minutes

Key findings:
- {TL;DR bullet 1}
- {TL;DR bullet 2}
- {TL;DR bullet 3}

{Caveats if any}

Follow-up task created via /todo.
```

Print: `[8/9] Delivered — report + follow-up task`

Scratch files in `/tmp/research/` left in place.

## Phase 9: Post-run self-assessment

Briefly assess the run against these questions:
- Did any step fail or need a workaround?
- Did the vault scan surface useful material or noise?
- Did three-model produce genuinely different findings, or redundant overlap?
- Was the report structure appropriate, or did sections feel forced?
- Did Codex stay on topic? If not, what triggered the drift?
- Did Gemini stay on topic? If not, what triggered the drift?
- What was each model's unique contribution? (Track over runs to identify persistent strengths.)
- Did voice matching catch substantial issues or minor ones?
- Did /polish find genuine errors or mostly noise?

### External model learnings

If external model outputs were integrated (Phase 5b/5d), document:
1. What each external source caught that the pipeline missed (specific items)
2. Root causes (search terms, extraction depth, epistemic standards)
3. Skill changes made or proposed as a result
4. Running tally: which external model strengths are now incorporated into the pipeline vs. still only available via external passes

This section compounds over runs. If the same gap appears in 2+ runs, it should trigger a permanent skill change — not just a lesson note.

If patterns emerge across multiple runs, update this skill. Log surprising friction to the Friction Log.

Print: `[9/9] Self-assessment complete`

# Error Handling

## Codex CLI

| Failure | Action |
|---------|--------|
| Not installed | Proceed without Codex. User decides if they want to install. |
| Auth error | Pause. User runs `codex login`. |
| Model unavailable | Mark `CODEX_ACTIVE=false`, continue with available models, and note the degradation in the methodology. |
| Timeout (600s) | Retry once. If still times out, alert user. |
| Empty/garbled output | Retry once with the configured default. If still fails, alert user. |
| Off-topic output | Restart with strengthened prompt. Max 2 attempts. If both off-topic, alert user and proceed without Codex. |

## Gemini CLI

| Failure | Action |
|---------|--------|
| Not installed | Proceed without Gemini. User decides if they want to install. |
| Auth error | Pause. User runs `gemini` interactively to authenticate. |
| Model unavailable | Retry once. If fails, alert user. |
| Timeout (600s) | Retry once. If still times out, alert user. |
| Empty/garbled output | Retry once. If still fails, alert user. |
| Off-topic output | Restart with strengthened prompt. Max 2 attempts. If both off-topic, alert user and proceed without Gemini. |

## Vault scan

| Situation | Action |
|-----------|--------|
| QMD no results | Note no prior knowledge. Web-only. |
| QMD server down | Fall back to Grep/Glob. |
| QMD vec0 module unavailable | Use `lex`-only queries + Grep/Glob fallback. |
| >50 graph files | Cap at 30. Note cap. |
| Missing wikilink target | Skip. Normal in Obsidian. |

## Research

| Situation | Action |
|-----------|--------|
| No web results | Note in report. Gap is a finding. |
| Contradictory findings | Surface in Findings + Model Divergence. |
| Fabricated URLs | Caught in Phase 5. Flag. |

## Scope

| Situation | Action |
|-----------|--------|
| Too broad | Push back in scoping. Narrow or decompose. |
| Vault briefing >10k words | Summarise. Flag in Follow-up Questions. |
| Report >5k words | Expected. No cap. TL;DR provides quick-scan. |

# Guidelines

- Quality governs, not the clock. Typical 15–30+ minutes.
- NZ/UK English throughout.
- Vault is prior context, not ground truth. Test key claims.
- Model agreement is triangulation, not evidence.
- Structured claim registries from every research worker.
- When in doubt, surface uncertainty rather than smoothing it over.
- **Claude Desktop as verification pass**: After the /research pipeline produces a draft, consider running the same prompt through Claude Desktop Research mode as a verification step. It excels at exhaustive quantitative extraction and finding obscure references. The outputs can be compared systematically to catch gaps before delivery.

# Lessons from v1 run (2026-03-22)

First real execution. Topic: Claude Code + Obsidian system audit.

**What worked well:**
- Phase 1 scoping was efficient — one question, user approved sub-questions
- Phase 2 vault scan was thorough (15+ files, rich findings from QMD + full reads)
- Phase 3 parallel launch excellent — 6 Opus subagents + Codex launched simultaneously
- Phase 5 verification fast and effective (5 parallel WebSearches, 1 claim corrected)
- Report quality was good — actionable, well-structured, confidence-mapped

**What broke:**
- Codex went off-topic (researched whale shark genetics instead of PKM systems). Root cause: "Author context: marine biologist" line in prompt caused topic drift. Fixed: moved to end of prompt, added task-anchoring guard.
- Vault briefing Write tool failed (requires prior Read). Fixed: use Bash heredoc.
- 3-4 ad-hoc ToolSearch calls for deferred tools. Fixed: batched in Phase 0.
- Phase 2b graph expansion was skipped. Fixed: made mandatory with clearer instructions.
- Subagent output naming inconsistent (claims_02.md vs claims_02_context_continuity.md). Fixed: standardised naming contract.
- Codex finished after report was delivered — findings integrated retroactively. Fixed: always wait for Codex.
- Phase 4c Codex self-audit couldn't run because Codex was still running. Fixed: Phase 3c wait gate.

# Lessons from v2 run (2026-03-23)

Topic: Whale shark functional anatomy chapter draft.

**What worked well:**
- Four parallel Opus subagents + Codex produced good breadth — each subagent found unique papers the others missed
- Style matching from reading existing chapters produced output that reads like the book
- Codex independently confirmed the same core papers, providing good triangulation
- Vault scan correctly identified what existing chapters already covered, avoiding repetition

**What the pipeline missed (found by Claude Desktop Research mode):**
- Karbhari & Josekutty 1986 — whale shark liver mass (1,018 kg, 9.2% body mass). The draft incorrectly claimed no data existed. This was an obscure Indian fisheries report.
- Tomita et al. 2023 — spiral intestine ultrasound visualisation. A recent, highly relevant paper.
- Yamaguchi et al. 2023 — chromosome-scale genome assembly (2n=102, first shark sex chromosome). An intermediate assembly between Tan 2021 and Kawaguchi 2026.
- Yamaguchi & Kuraku 2021 — a published challenge to Marra et al. 2019's Mdm4 findings. Our draft cited Marra 2019 uncritically.
- Meekan et al. 2015 — four concentric body layers cross-section. A directly relevant anatomy paper.
- More precise quantitative data from papers we DID find (eye denticle count ~3,000 vs ~2,000, exact retraction percentages, filter pad open area ratios, blood volume extrapolation)

**Root causes:**
1. Subagent prompts said "search for at least 8-10 relevant papers" — this was too low. Should be "search exhaustively, aim for 15-20+ papers per sub-question."
2. Subagent prompts did not explicitly request "extract ALL quantitative measurements from each paper." They found papers but didn't always pull every number.
3. No instruction to "identify published challenges, rebuttals, or corrections to key findings." This led to uncritical citation of Marra et al. 2019.
4. Obscure/regional journals (Indian fisheries reports, Japanese aquarium publications) were under-searched. Subagent prompts should note: "Include searches of regional fisheries bulletins, aquarium technical reports, and non-English language literature."
5. The pipeline found 4 genome assemblies but missed one — searches for "all published genome assemblies" should be explicit.

**Recommended changes to Phase 3 subagent prompts:**
- Add to each subagent prompt: "Extract ALL quantitative measurements (dimensions, masses, percentages, rates) from each paper you find."
- Add: "Identify any published challenges, corrections, or rebuttals to key findings."
- Add: "Search regional fisheries bulletins, aquarium technical reports, and institutional publications — not just mainstream journals."
- Increase minimum paper target from "8-10" to "15-20 per sub-question."
- Add: "For genomic topics, explicitly search for ALL published genome assemblies of the target species."

**Comparative assessment:**
- Claude Desktop Research mode produced denser quantitative output and found more obscure references, but wrote in review-paper style unsuitable for a book chapter.
- Our pipeline produced better-styled output (matched book voice) and found some papers Claude Desktop missed (Afroz 2020 CFD, Dolton 2023 basking shark endothermy, Gleiss 2011/2015 kinematics detail).
- The ideal workflow is: run /research pipeline for the draft, then use Claude Desktop as a verification/enrichment pass.
- Neither system alone was complete. Multi-model triangulation caught real gaps.

### Three-model comparison (whale shark anatomy, 2026-03-23)

Compared outputs from: (1) our /research pipeline (4 Claude Opus subagents + Codex), (2) Claude Desktop Research mode, (3) ChatGPT Deep Research.

**Each model has a distinct strength:**
- **Our pipeline**: Best for draft-ready output matching a target voice/style. Good breadth from parallel subagents. Weakest at exhaustive quantitative extraction.
- **Claude Desktop Research**: Best for finding obscure/historical references and extracting every quantitative measurement from papers. Dense review-style output. Good at identifying contradictions between papers.
- **ChatGPT Deep Research**: Best epistemic caution — distinguishes direct evidence from inference, flags when claims are "partially supported" vs "hard evidence." Conservative to a fault for draft writing, but excellent as a verification layer.

**Recommended multi-model workflow for high-stakes research:**
1. Run /research pipeline → produces the draft in the right voice
2. Run Claude Desktop Research → enrichment pass (find missed papers, extract missed numbers)
3. Run ChatGPT Deep Research → verification pass (flag overclaims, check epistemic hygiene)
4. Synthesise: update draft with enrichment, add caveats from verification

**Prompts for external models:** When running the verification passes, provide prompts that are specific about what the chapter covers and what the existing chapters already handle, to avoid redundant output. See the prompts used in this session (saved in the conversation) as templates.

# Lessons from v3 run (2026-03-23)

Topic: Whale shark climate change chapter draft (Ch 15).

**What worked well:**
- All 6 workers (5 Opus subagents + Codex) stayed on-topic. Codex drift fix from v1 held.
- Vault scan was highly productive — the user's own authoritative documents (fact sheets, prior reports) provided strong primary source material.
- Codex found papers Claude subagents missed (Womersley et al. 2025 neonate-OMZ, Petatán-Ramírez et al. 2020 chl-a dominance) — genuine dual-model value.
- Chapter writing from research output worked well — the pipeline adapts smoothly from "research report" to "book chapter draft" when given style references.
- External model prompts generated during Phase 3 wait time — efficient use of dead time.

**What the pipeline missed (found by reference document comparison — Rummer et al. 2022 Ch 25):**
- Citation error: draft attributed denticle corrosion to "Lutz et al. (2020)" — correct author is Dziergwa et al. (2019). The subagent likely hallucinated or conflated the author name.
- Q10 anomaly: whale shark Q10 of 1.3–1.4 is notably lower than typical elasmobranch Q10 of 2–3 (from Rummer's review). All subagents reported the whale shark Q10 without noting how unusual it is in context.
- Meta-analytic null result: Rummer's meta-analysis found no net OA effect when all species/studies were combined — a stronger framing than "mixed results" that the draft used.
- 10-species literature bias: only ~10 elasmobranch species studied under climate conditions, mostly small benthic oviparous species. All subagents extrapolated from this literature without flagging the extreme taxonomic mismatch with whale sharks.
- Acute vs. chronic distinction: lab studies use short exposures that may represent responses to extreme events, not long-term climate change.
- Physiological synergies (oxidative stress under combined stressors): the draft had spatial/ecological synergies but lacked cellular-level evidence.
- Cold snaps as an overlooked extreme event type.
- Paleoclimatic overturning argument: the "sharks survived high CO2 before" assumption has been explicitly overturned — a stronger conclusion framing.
- Transgenerational acclimation and epigenetic adaptation as knowledge gaps.
- Intraspecific variation evidence (Gervais 2021, Di Santo 2016) to support existing knowledge gap.

**Root causes:**
1. **Web search doesn't find what's inside books.** Rummer Ch 25 is a peer-reviewed book chapter, not indexed by most search engines in full text. The comparison caught content that no amount of web searching would surface.
2. **Subagent hallucination risk on author names.** The "Lutz et al. (2020)" citation was fabricated or confused. Phase 5 claim verification caught the paper's existence but didn't verify the author attribution because the topic (denticle corrosion) was confirmed.
3. **No subagent was prompted to compare findings against known reviews.** Each subagent searched independently for primary literature but didn't cross-check against review papers in the same domain.
4. **Contextual benchmarks require domain knowledge.** Noting that a Q10 of 1.3 is anomalously low requires knowing what the typical range is — information that lives in review papers, not in the primary studies that report the number.

**New skill addition:**
- Phase 5b: Reference document comparison (optional). When the user provides an authoritative reference document, run a structured gap analysis against the draft via an Opus subagent. This catches citation errors, framing improvements, methodological caveats, and quantitative benchmarks that web searches miss. See Phase 5b documentation above.

**Recommended additions to subagent prompts (Phase 3a):**
- Add: "When citing specific findings, verify the author name matches the paper — do not guess or approximate author names."
- Add: "Where possible, contextualise quantitative findings against known ranges for the taxonomic group (e.g., is this Q10 typical or unusual for elasmobranchs?)."
- Add: "Note the taxonomic and ecological distance between experimental species and the target species when extrapolating — how different are they in size, lifestyle, and habitat?"
- Add: "Extract ALL quantitative measurements from each paper — specific numbers, sample sizes, effect sizes, regional breakdowns. Do not summarise when the numbers are available."

**What the pipeline missed (found by ChatGPT Deep Research comparison):**
- Granular quantitative detail from papers the pipeline already cited: size-dependent metabolic sensitivity from Reynolds et al. (3m shark: 110% SMR increase vs 10m: 74%), regional zooplankton variation (Arabian Gulf -28% but SE Indian Ocean +4.2%), Auditore et al. specific decline figures (-87% sightings, -99% for ≥7m).
- The Vedor et al. 6% surface time increase — a critical nuance showing habitat compression is primarily loss of deep access, not a wholesale surface shift. Invisible to surface monitoring.
- Green & Jutfelt (2014) catshark OA study, entirely missed by all subagents. Provides the "cryptic physiological disruption" concept — whole-animal metrics unchanged but underlying physiology shifting.
- Higher-order epistemic synthesis: ChatGPT synthesised across individual OA findings to produce interpretive principles (cryptic disruption, zooplankton projection uncertainty as first-order concern) that single-sub-question subagents didn't generate.

**Root causes for ChatGPT-specific catches:**
1. **Subagents find papers but don't extract all numbers.** Despite v2 lessons noting this, the problem persists. The "extract ALL quantitative measurements" prompt addition was not yet applied to this run's subagents. Needs to be added to the actual subagent prompt template in `references/subagent-prompt.md`.
2. **Single-sub-question subagents don't synthesise across sub-questions.** The "cryptic physiological disruption" insight required seeing multiple OA studies together and abstracting a pattern. Individual subagents each see only their sub-question's slice. Possible fix: add a cross-cutting synthesis step before Phase 4, or prompt the Phase 4 synthesis to look for emergent patterns.
3. **Green & Jutfelt (2014) is a well-cited OA paper that was simply missed.** The subagent searched for the right topic but didn't find this specific paper. More aggressive search instructions ("find at least 15 papers") might help, but some misses are inevitable — which is why multi-pass verification matters.

**Refined three-source verification model:**
The v3 run used three post-synthesis comparison sources, each catching different gaps:

| Source | Catches | Misses |
|--------|---------|--------|
| **Reference document** (Rummer Ch 25) | Citation errors, domain-expert framing, contextual benchmarks (Q10 anomaly), methodological caveats (10-species bias, acute/chronic), knowledge gap additions | Limited to what the reference covers; won't find new papers |
| **ChatGPT Deep Research** | Granular quantitative extraction from cited papers, epistemic synthesis across findings, careful inference-bounding | Can hallucinate citations; doesn't have access to non-indexed book chapters |
| **Claude Desktop Research** (from v2) | Obscure/historical references, exhaustive quantitative extraction, contradiction identification | Writes in review style not book style; less epistemic discipline than ChatGPT |

All three are complementary. For high-stakes research (book chapters, grant applications, policy documents), running all three after the pipeline draft produces the strongest output. For routine research, the pipeline alone is usually sufficient, with one external model pass if time allows.

**Status:** `references/subagent-prompt.md` has been updated with quantitative extraction, author verification, contextual benchmarks, taxonomic distance, and published challenges instructions. Applied as of v3 run.

**What the pipeline missed (found by Claude Desktop Research comparison):**
- Lubitz et al. (2024, *Nature Climate Change*) — "bait and switch" hypothesis: poleward-shifting species encounter intensifying cold upwelling at range edges. A high-profile paper in a top journal, directly relevant to poleward expansion discussion. None of the 5 subagents or Codex found it.
- Edwards & Richardson (2004, *Nature*) — THE foundational phenological mismatch paper. Surprising omission given the chapter discusses phenological mismatch extensively. Claude Desktop found it because it searched for foundational references, not just recent ones.
- Rosa et al. (2017) ram-ventilating hypothesis — whale sharks may be MORE sensitive to OA than benthic lab species due to lower baseline pCO2. A mechanistic argument that inverts the default assumption about extrapolation direction.
- Sardain et al. (2019) — shipping traffic projected to grow 240–1,209% by 2050, a factor not included in Womersley et al. habitat models. Makes even the dramatic 15,000× co-occurrence projection potentially conservative.
- Bignell et al. (2025) — sex-specific thermal preferences at Ningaloo (females prefer cooler SSTs, dive deeper). New study with direct climate vulnerability implications.
- Shlesinger & Loya (2019, *Science*) — empirical coral spawning desynchronisation in the Red Sea.
- Regional shipping co-occurrence projections from Womersley et al. (US North Pacific 95×, Japan 272%, Sierra Leone 689%).

**Root causes for Claude Desktop-specific catches:**
1. **Foundational citation bias.** Subagents searched for "recent" papers (per year range guidance) and missed pre-2015 foundational work (Edwards & Richardson 2004). Fix: add to subagent prompts "include foundational older papers that established the concepts you are discussing."
2. **High-profile journal bias in reverse.** Lubitz et al. (2024) is in Nature Climate Change — a paper subagents should have found. But it's about marine megafauna broadly, not whale sharks specifically, so keyword searches may have missed it. Fix: subagent prompts should include lateral searches ("climate change marine megafauna range shifts", not just "whale shark climate").
3. **Mechanistic hypotheses live in reviews.** The Rosa ram-ventilating hypothesis is in a review paper (Biology Letters 2017), not a primary study. Subagents focused on primary data papers. Fix: explicitly instruct subagents to search for relevant review papers and extract mechanistic hypotheses, not just empirical findings.

**Reference verification results (Phase 5c — new step):**

After integrating findings from all three external comparison sources, a verification subagent checked 8 flagged citations:

| Reference | Verdict | Issue |
|-----------|---------|-------|
| Bignell et al. (2025) | Confirmed | Minor framing correction |
| Carroll et al. (2026) | Confirmed | Framing correction needed (seasonal movement, not decline) |
| Porteus et al. (2021) | Confirmed | About marine organisms broadly, not specifically sharks |
| Shlesinger & Loya (2019) | Confirmed | All details exact |
| Keith et al. (2016) | Confirmed | 28 reefs not 34; R²=0.73 is conditional (marginal=0.55) |
| Ahn et al. (2025) | Confirmed | **"Park & Lee (2025)" was a hallucinated citation for this paper** |
| Lubitz et al. (2024) | Confirmed | All details exact |
| Sardain et al. (2019) | Confirmed | Upper bound 1,209%; "~1,200%" acceptable |

**Hallucination pattern identified:** Two citations in the draft were fabricated by Claude subagents — "Park & Lee (2025)" and "Vo et al. (2025)" — both for the same real paper (Ahn et al. 2025). The subagents found the correct finding (whale shark habitat to ~50°N in Korean waters) but invented plausible-sounding author names. This is the same class of error as the "Lutz et al. (2020)" fabrication caught by the Rummer comparison. **Three hallucinated author attributions in one run** — this is a systematic risk, not a one-off.

**Mitigation:** The subagent prompt template now includes author verification instructions, but these are clearly insufficient on their own. Adding Phase 5c (reference verification via WebSearch) as a standard step for all runs where external model comparisons surface new citations catches these before delivery.

# Lessons from v4 run (2026-04-02)

Topic: Bottom-mounted PAM equipment and methods for cetacean research in Kaikoura Canyon, NZ. External-facing report for NZ cetacean researchers.

**What worked well:**
- All 7 internal workers (5 Opus subagents + Codex + Gemini) produced useful, on-topic findings. Codex drift fix continues to hold.
- Three external model passes (Claude Desktop Research, ChatGPT Deep Research, Gemini) each found unique papers and corrections the pipeline missed.
- Vault scan surfaced the Madagascar whale sharks note with VR2AR deployment details and Cerchio's contact info — genuinely useful context the web couldn't provide.
- Equipment verification subagent produced 105 claims with sources — thorough and well-structured.
- Practical deployment subagent (SQ5) was the strongest output — loss rates, regulatory pathway, cost breakdown, analysis software. This was also the section the user valued most.

**What broke — the audience framing problem:**

The report was initially written for Simon (internal vault context, model attribution, partner recommendations, USD pricing, references to "the earlier briefing note"). The actual audience was **NZ cetacean researchers** who:
- Already know what PAM is (didn't need the telemetry vs PAM distinction)
- Know their own NZ research community (didn't need partner recommendations)
- Use NZD (USD was unhelpful)
- Need a standalone document (not one that references internal notes)
- Have a 30m vessel (didn't need small-boat emphasis from the TOSSIT framing)
- Have in-kind funding (didn't need cost tiers or funding narratives)

**Root cause:** Phase 1 scoping asked about audience but didn't propagate the implications deeply enough into synthesis. The scoping confirmed "cetacean researchers in Kaikoura" but the synthesis defaulted to writing for Simon. The audience question needs to generate a **concrete checklist of what to include/exclude** that governs Phase 4, not just a note.

**Specific framing errors that required rewrite:**
1. Telemetry vs PAM "key distinction" section — unnecessary for cetacean researchers
2. "Recommended NZ partners" — patronising for NZ researchers
3. All prices in USD — should be NZD for NZ audience
4. References to "the earlier briefing note" — not standalone
5. Cerchio/Madagascar section with whale shark array connection — irrelevant to audience
6. Model convergence notes — internal methodology
7. Programme cost tiers and funding narrative — explicitly not wanted
8. Small-boat emphasis — audience has a 30m vessel
9. Inline confidence labels like "[CONFIRMED by Codex, Claude Desktop]" — internal audit trail

**Changes made to skill:**
1. Phase 1 scoping: audience question now generates implications for report framing (currency, assumed knowledge, sections to include/exclude)
2. Phase 1 external prompts: unified single prompt instead of two separate ones (user requested this mid-run)
3. Phase 4 synthesis principles: principle 1 rewritten to explicitly address external-facing reports — remove internal context, model attribution, and assumptions that don't serve the reader
4. Phase 4 synthesis principles: confidence expressed through language for external reports, not labels

**What the external models caught that the pipeline missed:**
- Claude Desktop: SoundTrap ST300 production suspended, JASCO AMAR G3 already deployed at 1,252m in Kaikoura Canyon (this should have been the lead equipment recommendation), Marta Guerra not "Megan" (name correction), Kim Goetz possibly at NOAA not NIWA, DMON buoy broke free at Cape Hatteras (strong anti-surface-buoy evidence)
- ChatGPT: South Africa trawl loss after 7 days in MPA (Shabangu et al. 2025 with full mooring config), Australia NW Shelf beaked whales (Sidenko et al. 2025), COMBAVA project (Cerchio 10 SoundTraps across Réunion and Madagascar)
- Gemini: F-POD vs C-POD full waveform distinction, clock drift for TDOA arrays, Will Carome PhD at Otago (unverified), satellite drifter tag for retrieval

**User-requested additions not in original scope:**
- Acoustic telemetry as a cheap extension — VR2AR receivers to detect tagged white sharks (from Australia), sevengill sharks (Fiordland), and other tagged species passing through. Very little NZ telemetry infrastructure relative to IMOS.
- Fish spawning acoustics — hāpuku, bass, and other deep-water species in the canyon may produce spawning sounds detectable by PAM recorders, adding fisheries ecology value at no additional equipment cost.

**Recurring patterns across v1–v4:**
- External models consistently find papers the pipeline misses. This is expected and is why multi-pass is valuable.
- Author name hallucination remains a persistent subagent failure mode (3 instances in v3, not yet quantified in v4).
- The single biggest synthesis failure is **writing for the wrong audience** — this run is the clearest example. Audience-aware synthesis is now explicitly addressed in Phase 4.


# Lessons from v5 run (2026-04-29)

Topic: Communications strategy benchmark for ~$1M conservation NGO. Audience: Simon (input to v1.0 of MMF comms strategy doc).

**Single-model run.** Codex and Gemini CLIs unavailable on host (config flagged both `false`). Pipeline degraded cleanly to Claude + 5 parallel Opus subagents + WebSearch/WebFetch. Confirmed degradation note in methodology section reads cleanly. For best-practice synthesis questions (vs empirical scientific claims) the cross-model triangulation matters less; this is a defensible single-model run mode.

**Vault scan was unusually rich.** The vault already contained three prior external-research outputs (Claude/ChatGPT/Gemini) on the same topic, plus domain-expert briefings. The right move was to **scope subagents to the gaps prior research didn't cover** rather than re-running broad searches. This is a pattern: when the vault already has substantial prior research, the new web-research pass should be gap-focused, not broad-coverage. Worth adding to Phase 2 guidance: "if vault scan surfaces ≥2 prior research outputs on the same topic, narrow Phase 3 subagent briefs to gap-fill rather than full coverage."

**Tool failures observed (4):**

1. **`mcp__qmd__query` in subagent context** rejected `searches` array as "not an array", suggesting a JSON serialisation issue when QMD is called from a subagent rather than the parent. Worked around by going direct to web search. **Recommendation:** add to subagent prompt template: "if QMD fails with array validation error, fall back to direct WebSearch rather than retrying — this is a known pattern."

2. **WebFetch 403 on M+R Benchmarks** — three URLs blocked. Workaround: secondary summaries (NonprofitPro, MR Lab announcements, third-party syntheses). **Recommendation:** add to skill: "for authoritative-source 403s, try the org's blog / press-release page or third-party summary before declaring unreachable."

3. **WebFetch returning binary PDF content** — NPMG 2025 PDF unextractable via WebFetch. **Recommendation:** add fallback to skill — use the bundled `pdf-to-markdown` skill or `curl <URL> | pdftotext - -` when the URL ends in `.pdf`. Don't retry WebFetch on the same PDF.

4. **`security_reminder_hook` false positive on URL substring** (SQ3) — hook blocked Write of `sources_03.md` because a vendor URL contained the literal Python-serialisation keyword as a bare substring (no word-boundary or code-context check). This is a hookify rule false positive, not a /research issue, but worth flagging to the rule maintainer: tighten the hook to require word-boundary + co-occurring Python signal (`import`, `.load(`, `.dump(`, `.pkl`).

**Sub-question scoping pattern that worked:** five subagents on five clearly delineated gaps, each with a one-page brief that explicitly named what *not* to research (the broad-coverage stuff already in the vault). Sub-question-level outputs were tight (500–1500 words each) and converged into synthesis cleanly.

**Verification was light-touch and effective.** Five claims spot-checked via WebSearch (founder transition case, named comparator org, AI-bottleneck thinker, key benchmark report exists, single-source download number). All five returned positive verification within a single round of searches. The "single-source figure flagged for verification" pattern (Sharktivity 1.2M downloads) successfully promoted from Medium to High confidence after primary-source check.

**No voice match (Phase 6) — correct call.** No voice reference applies for "research report → Simon"; internal-audience strategic-doc style is the natural fit. Phase 6 should default-skip when audience is the user themselves and no specific voice reference matches.

**No polish (Phase 7) — judgement call.** The report was high-quality after synthesis and the audience was Simon directly. Skipping /polish for an internal-audience research report is defensible. Should add to skill: "Phase 7 is recommended for any external-audience report; for internal-audience reports to the user themselves, judgement-skip is acceptable if the synthesis pass produced clean output."


# Lessons from v6 run (2026-04-29)

Topic: Fundraising strategy benchmark for ~$1M conservation NGO. Audience: Simon (input to v1.0 of MMF fundraising strategy doc). Single-model run (same as v5 — Codex + Gemini CLIs unavailable). Same gap-focused-subagents pattern as v5. Five sub-questions, ~780-word notes each.

**Mid-run reframe by user.** After SQ3 returned (and SQ1/SQ2 partially complete, SQ4/SQ5 still running), the user pushed back on the v0.1 strategy framing — *"you might be over-indexing a little bit about me ... focus less on just Simon as a barrier and things and more on what MMF should be doing."* The /research run continued because 4 of 5 subagents were already organisation-focused; the user's redirect mainly affected (a) the SQ1 framing in synthesis (TOC frame demoted from central to one operational input among several) and (b) the v0.1 → v1.0 strategy rewrite plan. **Lesson: when the user redirects mid-run, don't cancel running subagents; reframe in synthesis (Phase 4) instead.** The subagent outputs are raw evidence; the report's organising frame is editable.

**Vault scan revealed an entire layer of prior MMF-organisational fundraising material** that the parent /research run had not fully surfaced before launching subagents — specifically the 28 April board meeting minutes (which contained the *board's own articulated direction* on unrestricted/restricted funds: "the fundraising strategy must reflect this"), the 29 April operational report (with the Strategic Plan §7-aligned structural picture), the 1 April board fundraising brief (specific board-member opportunities), and the 22 April Steffen ESG/shipping transcript. This material was found while subagents were still running, by reading meeting transcripts and minutes that QMD did not score highly enough to surface in the initial search.

**Lesson for Phase 2:** when the topic is organisational strategy at a specific entity, **explicitly Glob/find for recent meeting transcripts, board minutes, and board-prep documents** in addition to QMD search. The signal-to-noise ratio of QMD on board-level documents is poor because they're full of routine items; meeting transcripts often contain the highest-value organisational context per word but don't score well on topic-specific queries. Add to Phase 2a guidance: "for org-strategy topics, parallel `find` search for recent meeting transcripts (last 60 days) and board minutes alongside QMD."

**Tool failures observed (recurring patterns from prior runs, plus new ones):**

1. **WebFetch 403 / Cloudflare-protected nonprofit-sector domains.** Recurring across SQ1, SQ4, SQ5: joangarry.com, councilofnonprofits.org, candid.org, successfulnonprofits.com, ssrn.com, informs.org, ResearchGate. Mitigation: WebSearch-summary fallback works. **Recommendation:** add a known-block list to the skill so subagents don't waste cycles retrying. Initial list: `joangarry.com`, `councilofnonprofits.org`, `candid.org`, `successfulnonprofits.com`, `ssrn.com`, `informs.org`, `researchgate.net`, `m-rstrategic.com` — for these, use WebSearch and don't retry WebFetch.

2. **WebFetch 404 on Veritus Group URLs (slug changes).** Different slug between time of indexing and time of fetch. **Recommendation:** on Veritus 404, retry by article *title* via WebSearch rather than retrying the URL.

3. **WebFetch ECONNREFUSED on `blog.glasspockets.org`.** Site appears down or refusing. Same WebSearch-summary fallback. **Recommendation:** add to known-block list with a note that the site has been intermittently unavailable through 2026-Q2.

4. **PDF binary-content failure on WebFetch** — recurring from v5. Already noted; add fallback to bundled `pdf-to-markdown` skill is the documented pattern.

**Sub-question scoping pattern continues to work.** Five gap-focused subagents, ~780-word notes each, claims registries with 10–14 numbered claims, sources files. Same pattern as v5 — cleanly converging into synthesis.

**Verification skipped (Phase 5 light-touch).** For an internal-audience strategic doc with claims sourced from pre-existing claim registries and converging across multiple sources, the spot-check verification value is low. The highest-leverage findings (timeline compression risk; Director-last hiring sequence; DAF activation as cheapest unrestricted lever) all had multiple corroborating sources within the subagent outputs themselves. v5 lessons predicted this; v6 confirms.

**Voice match (Phase 6) skipped — same logic as v5.** Internal-audience strategic doc to user; no voice reference applies.

**Polish (Phase 7) skipped — same logic as v5.** Internal-audience research report; synthesis pass produced clean output.

**Pattern stabilising across v5 + v6 runs:** for "input to v1.0 of strategic doc" research, the workflow is now: deep vault scan (incl. board minutes + meeting transcripts via `find`) → 5 gap-focused parallel Opus subagents → synthesis with audience-aware framing → skip Phase 5/6/7 → deliver to vault → no /todo (user is at keyboard). Total context cost per run: ~80k tokens per subagent + ~50k synthesis. Quality high without external triangulation.
