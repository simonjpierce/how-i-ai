# Research Workflow

> **Adapting this for your work.** Examples reference Simon Pierce's MMF research (whale shark essays, photo-ID, conservation strategy). The three-mode model — **deep** (the bundled `/research` skill), **inline/lightweight** (this doc), and an **automated weekly strategic sweep** — generalises across any research-driven knowledge work. The automated weekly sweep is Simon-specific infrastructure (LaunchAgent + scripts under `~/bin/`). For external use, just the deep `/research` skill and the inline/lightweight patterns are portable as-is.

Status: promoted to skill (deep mode, v2) + active process doc (inline/lightweight modes)
Owner: shared
Last reviewed: 2026-03-27
Uses: 4 (strategic plan benchmarking, 2026-03-13; whale shark essay automation integration, 2026-03-13; photo-ID V3 review — inline research during manuscript development, 2026-03-21; Claude Code system audit — deep mode run 2, 2026-03-22)

> **Deep autonomous research → use `/research`.** The full pipeline (vault scan, Phase 2d comms scan via Gmail + Slack, three-model web research via Claude + Codex + Gemini, claim verification, formal report) is now a skill. Spec: `01_PROJECTS/REVIEW QUEUE/SPECS/2026-03-22-research-skill-design.md`. This process doc covers **inline** and **lightweight** research only.

### When to use which

| Mode | When to use | Output |
|---|---|---|
| **`/research` skill** (deep) | 15+ minute investigation, three-model coverage, formal report | `01_PROJECTS/REVIEW QUEUE/RESEARCH/` |
| **This process doc** (inline/lightweight) | Quick answer mid-task, 1–2 subagents, enriching an existing document | Depends on task context |
| **Weekly strategic research** (automated) | Runs autonomously Sunday 01:00 — automated topic selection for system improvement | `05_SYSTEM/System Research/` (consumed by nightly self-improvement loop) |

The weekly strategic research (`self_improve_research.py` + LaunchAgent `nz.simon.selfimproveresearch`) is a separate automated pipeline that selects topics from friction themes, changelog trends, and bookmark signals, then runs Claude + Codex research. Its output feeds the self-improvement loop, not the review queue. See `Scheduled Automations.md` entry #20.

### Goal

Combine vault knowledge and web research to produce a structured research note on a given topic. Designed for quick background research, inline fact-checking during active work, and lightweight literature scans — not for deep autonomous research (use `/research`) or article enrichment (that's in the article pipeline, Phase 5).

### Trigger

When Simon asks for research that needs both vault context and external sources, and the question is narrow enough to handle mid-task without the full `/research` pipeline. Examples: "quickly check X for me", "what does the vault say about Y", "verify this claim", "I need a couple of sources on Z".

### Steps

#### 1. Clarify intent and scope

Before any research, confirm understanding with Simon via AskUserQuestion. Extract what you can from the request and conversation context, then fill gaps — one question at a time.

**What to confirm:**
- **Research question** — restate what you think the core question is. Ask: "Is this the right framing, or should I adjust?"
- **Scope** — time range, geographic focus, comparable organisations, sector boundaries. Propose defaults based on context (e.g. "I'd default to 2023–2026 for recency — does that work?")
- **Audience** — who will read this? Affects depth and tone. (Simon only → concise. Board → structured. Funders → evidence-heavy.)
- **Output format** — propose one based on the query type (see "Output formats" below) and confirm. E.g. "This sounds like a recommendation matrix — or would you prefer a gap analysis?"
- **Depth** — quick scan (1 round, 3 subagents, ~5 min) vs. standard (1 round, 5 subagents, ~10 min). For deep research (three-model, claim verification, formal report), suggest `/research` instead.

Skip questions where the answer is obvious from context. If Simon provided a detailed brief or cold-start prompt, most of this may already be answered — confirm rather than re-asking.

#### 2. Plan the research

Decompose the question into 3–5 specific sub-questions. Each becomes a subagent task. Decompose by sub-question (not by source type) — each subagent should own a complete research thread across all source types.

For complex or unfamiliar topics, consider the **multi-perspective approach** (from Stanford's STORM): before generating sub-questions, ask "what perspectives or angles would different experts bring to this topic?" A marine biologist, a policy advisor, and a community development specialist would each frame "how should MMF approach local ownership?" differently. Use these perspectives to generate broader sub-questions than a single viewpoint would produce.

Present the sub-questions to Simon before launching research: "Here are the 4 threads I'd research — anything to add or remove?" This is the last checkpoint before committing subagent budget.

**The plan is mutable.** If subagents discover important sub-topics not in the original plan, flag them. After the first round of results, decide whether to add a follow-up round for emerging themes — don't expand the current round mid-flight.

#### 3. Search the vault first

Before web research, check what's already known:
- **QMD semantic search** — `vec` and `lex` queries on the research topic and sub-questions
- **Grep/Glob** — targeted searches in likely folders (`02_MARINE MEGAFAUNA/`, relevant project folders)
- **Folder CLAUDE.md files** — read the domain CLAUDE.md for context

**QMD query gotchas:**
- **Hyphen negation**: Hyphens in `vec`/`hyde` queries are parsed as negation. Use "photo identification" not "photo-ID". Hyphens are fine in `lex` queries.
- **vec0 module intermittently unavailable**: `vec` and `hyde` queries may fail with "no such module: vec0" while `lex` queries work fine. If this occurs, fall back to `lex`-only QMD supplemented by Grep/Glob of likely vault folders. Do not block research on vec0 availability.

Vault sources are higher-trust than web results for MMF-specific facts. Note relevant files and pass them to subagents as context in Step 3.

**Assess coverage.** After vault search, identify which sub-questions are well-covered locally vs. which need external sources. Some sub-questions may not need web research at all.

#### 4. Parallel web research subagents

**Inline research during active work:** This workflow can also be triggered mid-task — e.g., during manuscript development, when the author flags a claim to verify or a gap to fill. In this mode, skip the formal planning steps; dispatch background agents for specific questions (e.g., "has porbeagle photo-ID been published?") and integrate findings into the working document without blocking the main conversation. Results go into the project's research notes file rather than `/tmp/research/`. This was used effectively during the Photo-ID V3 review (2026-03-21) — 6 research agents dispatched during outline development, findings compiled into a persistent research notes file alongside the manuscript.

**Standalone research mode:** Launch one subagent per sub-question (3–5 is the practical sweet spot). Each subagent gets:
- The sub-question and overall research context
- Relevant vault files identified in Step 2 (so it can build on existing knowledge and flag contradictions)
- Year range for recency filtering (e.g. 2023–2026)
- Domain-specific source guidance (see "Domain routing")
- Output format and save location

Each subagent should:
- Search for recent material from credible primary sources
- Write a 300–500 word research note to `/tmp/research/XX_topic_name.md`
- Include source URLs for **every** claim — no unsourced assertions
- Log all discovered sources (URL, title, relevance) to `/tmp/research/sources.md` (shared source registry — prevents duplicate retrieval across subagents)
- Flag anything that contradicts vault knowledge or other sources

**Subagent prompt template:**
> Research [sub-question] in the context of [overall research goal]. Search for recent ([year range]) material from [source guidance]. You have vault context on this topic: [summary of relevant vault findings, or file paths to read].
>
> Write a 300–500 word research note to `/tmp/research/XX_topic_name.md`. Every claim must cite a source URL. Flag any contradictions with the vault context or between sources. Append all discovered sources to `/tmp/research/sources.md` (title, URL, one-line relevance note).

#### 5. Synthesise

Read all research notes + relevant vault files. Write a single output document.

**Synthesis principles:**
- **Claim-level attribution.** Each finding should trace to a specific source. Don't summarise at the paragraph level — attribute at the claim level.
- **Surface conflicts explicitly.** When sources disagree, present both positions and their evidence. Don't silently pick a side.
- **Confidence scoring.** For consequential claims, indicate confidence:
  - **High** — multiple corroborating credible sources
  - **Medium** — single credible source, or multiple lower-quality sources
  - **Uncertain** — inference, extrapolation, or conflicting evidence
- **Source tiering.** Weight synthesis by source quality: peer-reviewed > institutional report > established news outlet > blog/forum. Vault notes from Simon's own research or meetings are high-trust for MMF-specific facts.

Use the output format selected in Step 1 (see "Output formats" below).

#### 6. Verify claims

For documents with consequential factual claims, spot-check the 3–5 most important via WebSearch. Report: Claim → Verdict (confirmed / partially supported / unsupported / contradicted) → Source → Note.

Also check:
- Do cited URLs actually exist and say what's attributed to them?
- Are statistics attributed to the correct species/location/time period?
- Are any claims single-source? Flag them.

#### 7. Deliver

- Save the output to the appropriate vault location (ask Simon if unclear)
- For documents that will be shared externally (board briefings, grant backgrounds, donor communications), run `/polish` before delivery — catches grammar/style issues and AI writing patterns
- Offer `/red-team` if the document is important enough to warrant adversarial review
- Offer `/todo` if follow-up action is needed
- Report: topic, sub-questions researched, output location, number of sources, any claims flagged as uncertain or conflicting

---

### Output formats

Default to **Structured Research Brief** unless the query type suggests otherwise:

| Format | Structure | Best for |
|---|---|---|
| **Structured Research Brief** (default) | Summary bullets → Findings by theme → Open questions → Sources | Quick background research, decision support, briefing docs |
| **Recommendation Matrix** | Numbered recommendations, each with Priority / Evidence / Feasibility / Change type | Strategic planning, benchmarking, plan review |
| **Evidence Table** | Rows = sources/studies, Columns = key variables | Systematic comparison (species data, gear specs, study results) |
| **Gap Analysis** | What's known (with sources) → What's missing → Priority for filling gaps | Research planning, grant proposals, identifying data needs |
| **Annotated Bibliography** | Citation + summary + relevance/quality per source | Literature surveys, building reading lists, early-stage exploration |

Simon can specify a format, or the skill infers from the query type. Multiple formats can be combined (e.g. recommendations + evidence table).

---

### Domain routing

Detect the query domain and prioritise sources accordingly:

| Domain | Primary sources | APIs/databases | Notes |
|---|---|---|---|
| **Marine biology / conservation** | Peer-reviewed literature, IUCN, NGO reports | Semantic Scholar API, IUCN Red List API v4, GBIF, OBIS, FishBase | Check vault expedition notes and fact files first |
| **Photography / gear** | Gear reviews, manufacturer specs | Web search (Backscatter, B&H, Amazon) | No programmatic APIs for gear retailers |
| **Non-profit operations** | Bridgespan, SSIR, InterAction, funder reports | OpenAlex for grey literature, web search | Ground in MMF's scale (~20 staff, <$2M) |
| **Policy / regulation** | Government databases, CITES, CMS, RFMOs | Web search for legislative tracking | Check vault policy notes first |
| **General** | Web search, credible news, institutional reports | Semantic Scholar for academic backing | Default domain if unclear |

---

### Canonical locations

- **Scratch files**: `/tmp/research/` (cleaned up on reboot)
- **Shared source registry**: `/tmp/research/sources.md` (all subagents append)
- **`/research` skill output**: `01_PROJECTS/REVIEW QUEUE/RESEARCH/Research — {Topic}.md`
- **Weekly strategic research output**: `05_SYSTEM/System Research/` (consumed by self-improvement loop)
- **Inline/lightweight output**: Depends on task context — project folder, working file, or ask Simon
- **This process doc**: `05_SYSTEM/Processes/Research Workflow.md`
- **`/research` skill**: `~/.claude/skills/research/SKILL.md` (git-backed; vault `05_SYSTEM/Skills/research/` has a reverse symlink for Obsidian browsability)
- **Design spec**: `06_ARCHIVE/Specs — Superseded/2026-03-22-research-skill-design.md`

### Checks before acting

- Is the research question clear enough to decompose into sub-questions? If not, ask.
- Am I duplicating work that's already in the vault? Check QMD first.
- Are the web sources credible and current? Prefer primary sources over aggregators.
- Does the output need to match a specific document's structure (e.g. strategic plan sections)?
- Is the scope bounded? Research expands indefinitely without constraints.

### Failure modes / gotchas

- **Subagent hallucination**: Web research subagents can fabricate URLs and misattribute statistics between related species/organisations. Source URLs are mandatory so claims can be traced. 39–55% of LLM-generated citations are fabricated when not grounded in retrieval. **Author name fabrication** is the most common sub-pattern: subagents find correct findings but invent plausible author names (3 instances in one whale shark book run — Lutz→Dziergwa, Park & Lee→Ahn, Vo→Ahn). Mitigate with author verification instructions in subagent prompts and Phase 5c reference verification in `/research`.
- **Vault staleness**: Vault files may contain outdated figures. Cross-reference web sources for anything time-sensitive.
- **QMD vec0 unavailable**: `vec` and `hyde` QMD queries intermittently fail with "no such module: vec0". `lex` queries are unaffected. Fall back to `lex`-only + Grep/Glob when this occurs. May require QMD vector index rebuild if persistent.
- **Generic advice**: The biggest risk for non-profit research is producing recommendations that apply to any nonprofit, not MMF specifically. Ground every recommendation in MMF's actual context (scale, species, geographies, existing capabilities).
- **Priority inflation**: Easy to mark everything HIGH. Limit HIGH to items where inaction has clear negative consequences.
- **Scope creep**: Stick to the sub-questions defined in Step 1. If new important topics emerge, flag them for a follow-up round rather than expanding the current research mid-flight.
- **Silent conflict resolution**: LLMs naturally pick a side when sources disagree (accuracy drops up to 65% with heterogeneous conflicting sources). The skill must actively surface conflicts, not smooth them over.
- **Attention asymmetry across source types**: When mixing vault notes, web results, and academic papers, models tend to over-weight one source type. Compensate by structuring the synthesis to consider each source type explicitly.

### Review notes

**2026-05-02 — Codex CLI current contract**:
- Current Codex CLI default is bare `gpt-5.5` with `xhigh` reasoning from `~/.codex/config.toml`; do not pass `gpt-5.5-pro`, `gpt-5.5-fast`, or older `gpt-5.4` overrides in `/research`.
- Use file-reference prompts (`codex exec "...Read /tmp/research/codex_prompt.md..."`) rather than stdin piping. Older notes below mention stdin as a fix for the then-current CLI; that is historical only.
- If Codex's configured model is unavailable, mark Codex inactive for that run and continue with available models, recording the degradation in the methodology. Do not try unverified fallback model slugs.

**2026-03-13 — First use (strategic plan benchmarking)**:
- 5 parallel subagents worked well. All completed within ~4 minutes.
- Red-team found that 3 of 21 recommendations understated what MMF already does — important accuracy check.
- Claim verification caught one overstatement (USAID "eliminated" → "froze/disrupted").
- The decomposition into sub-topics was done in advance (in the cold-start prompt). A general skill would need a topic-decomposition step.
- Total cost ~$3–5 for 5 subagents + synthesis + red-team. Budget accordingly.

**2026-03-13 — Web research on existing patterns**:
- Key architectural references: Stanford STORM (multi-perspective questioning), GPT Researcher (planner-executor-publisher), 199-biotechnologies Claude deep research skill (8-phase pipeline with credibility scoring), Perplexity (claim-level confidence scoring).
- Source verification is the critical differentiator. RAG reduces hallucination by ~71%, but claim-level attribution and confidence scoring are needed on top.
- Output format should vary by query type — one size doesn't fit all. Six formats identified; Structured Research Brief is the best default.
- Domain-specific databases (IUCN Red List v4, Semantic Scholar, GBIF, OBIS, FishBase) are available via API and could be integrated when the skill matures.
- Full research notes: `/tmp/research-skill-research/01_llm_research_patterns.md` and `/tmp/research-skill-research/02_existing_tools.md`.

**2026-03-22 — `/research` skill acceptance test 1 (whale shark connectivity Mozambique–Maldives)**:
- Full pipeline executed: scoping → vault scan (6 files, 850-word briefing) → 4 Claude Opus subagents + Codex gpt-5.4 in parallel → synthesis → verification → delivery. ~25 minutes total.
- Vault scan surfaced genetics book chapter and MMF project note — foundational context web research couldn't replicate.
- Multi-model research caught complementary findings: Codex found ISRA dossier with unpublished Maldives tracking data and corrected a vault claim about photo-ID cross-matching. Claude found eDNA microhaplotype preprint and Gujarat tracking data Codex missed. (This run predated Gemini integration.)
- Key friction: QMD rejects hyphens in vec/hyde queries (parses as negation). Codex `-q` flag doesn't exist (fixed to stdin pipe). Codex duplicates output — needs awk extraction. `/tmp/research/` can contain files from concurrent runs — need cleanup at start.
- All pass criteria met. Skill improvements applied to SKILL.md.
- Output: `01_PROJECTS/REVIEW QUEUE/RESEARCH/Research — Whale Shark Connectivity Mozambique to Maldives.md`

**2026-03-22 — `/research` skill run 2 (Claude Code + Obsidian system audit) → triggered v2 rewrite**:
- Full pipeline: scoping (1 question) → vault scan (15+ files, thorough) → 6 Claude Opus subagents + Codex gpt-5.4 → synthesis → verification (5 claims) → delivery. ~25 minutes.
- Vault scan was the most valuable phase — 15+ full documents read, rich findings that directly shaped the report. Confirmed vault as primary resource.
- Codex went off-topic (researched whale shark genetics instead of PKM systems). Root cause: "Author context: marine biologist" line in prompt template caused topic drift. Codex eventually self-corrected (~15 min wasted) and produced useful findings. Multi-model produced genuinely complementary results once both on-topic. (This run predated Gemini integration.)
- Multiple friction points: Write tool failed on new files (vault briefing), deferred tools needed ad-hoc loading (3-4 extra round-trips), Phase 2b graph expansion skipped, subagent output naming inconsistent, report finalised before Codex completed.
- Report quality was good — actionable, well-structured, 4,200 words, 45+ sources, confidence-mapped. User satisfied with output.
- **Triggered comprehensive v2 rewrite** of SKILL.md and subagent-prompt.md. See "v2 changes" below.
- Output: `01_PROJECTS/REVIEW QUEUE/RESEARCH/Research — Claude Code Obsidian System Audit.md`

### `/research` skill — promoted (2026-03-22), v2 rewrite (2026-03-22)

The deep research mode has been promoted to a `/research` skill. Design spec: `01_PROJECTS/REVIEW QUEUE/SPECS/2026-03-22-research-skill-design.md`.

Key design decisions resolved during promotion:
- **Three-model research**: Claude subagents + Codex CLI + Gemini CLI research in parallel, all informed by vault briefing (originally dual-model; Gemini added post-v2)
- **Deep vault scan**: QMD broad discovery → wikilink graph expansion (2 hops) → context packaging
- **Structured provenance**: Each subagent emits a structured claim registry, not just freeform notes
- **Adaptive report**: Reader-first structure (TL;DR → Implications → Uncertainties → Findings), audit sections in appendix
- **Source registry**: Structured from the start (claim text, source, type, date, confidence, contradiction flag)
- **Subagent briefing**: Per-sub-question excerpt + global summary, not full vault dump
- **Model agreement**: Triangulation cue, not evidence — confidence driven by source quality and verification
- **Domain routing**: Automatic detection, API integrations deferred to future iteration

**v2 changes (from run 2 retrospective):**
- **New Phase 0 (pre-flight)**: Batched ToolSearch for all deferred tools, directory cleanup, Codex pre-flight, tab title. Eliminates ad-hoc tool loading.
- **Codex prompt anchoring**: Research question leads and is repeated. Author context moved to end with "do NOT research this person's field" guard. Prevents topic drift.
- **Always wait for Codex**: Codex is never skipped. Synthesis draft can start while waiting, but report is never finalised without Codex input.
- **Codex off-topic detection + restart**: grep output for expected keywords after completion. If off-topic, restart with strengthened prompt (max 2 attempts).
- **Vault briefing via Bash**: Use heredoc/cat, not Write tool (which requires prior Read on the path).
- **Graph expansion mandatory**: Phase 2b wikilink following is required, not optional.
- **Standardised subagent naming**: `claude_{NN}_{slug}.md`, `claims_{NN}.md`, `sources_{NN}.md` — enforced in prompt template.
- **Claim registries as primary synthesis input**: Structured data first, full research notes for context.
- **Cross-model verification shortcut**: Claims cited by both Claude and Codex with consistent findings are pre-verified in Phase 5.
- **Pipeline is now 10 phases (0–9)** (was 6 at launch, 7 at v2): Phase 0 (pre-flight), Phase 6 (voice match), Phase 7 (polish), Phase 8 (delivery, was 6), Phase 9 (post-run self-assessment, was 7) added through iterative use. Phase 5 expanded with sub-steps (5a–5d).

This process doc remains the reference for inline and lightweight research. The deep pipeline lives in the skill.
