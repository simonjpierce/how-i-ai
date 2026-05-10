---
name: red-team
description: Red-team an important document — independent critical review using a Claude subagent, then Codex + Gemini independent opinions. Three-model architecture (Claude structured review, Codex open-ended, Gemini open-ended). For specs and process docs, automatically reviews associated implementation. Only invoke when the user explicitly says "/red-team" or "red-team this". Do NOT trigger on generic "review this" or "critique this" — this is a heavy, multi-phase process.
allowed-tools: Read, Write, Edit, Glob, Grep, Agent, AskUserQuestion, Bash, WebSearch, WebFetch, mcp__claude_ai_Gmail__gmail_search_messages, mcp__claude_ai_Gmail__gmail_read_message, mcp__claude_ai_Gmail__gmail_read_thread, mcp__claude_ai_Slack__slack_search_public_and_private, mcp__claude_ai_Slack__slack_read_thread
---

Red-team an important document. Takes a file path as `$ARGUMENTS`.

**Default flow is sequential** (Opus subagent → Gemini → Codex, with apply-passes between each reviewer). Each reviewer evaluates the post-prior-fix document so regressions introduced by earlier fixes get caught — Codex is last because it benefits most from the cascade. Validated 2026-04-28 in the v0 onboarding round (Codex's load-bearing C1 finding only existed because the subagent's H1 fix had already been applied; would have been routed-through-and-missed in parallel-then-synthesise).

Optional flags:
- `--quick` — subagent review only (Steps 0–5), skip external model opinions and ecosystem review. Use when the full pipeline would be disproportionate.
- `--parallel` — opt out of sequential mode. Run Codex + Gemini simultaneously against the post-subagent state, then reconcile via Step 7's three-way comparison. Use for routine reviews of stable documents (quick blog post, doc tone check, no associated code) where cascade value is low and clock time matters.

The review methodology (criteria, lenses, output format, examples) lives in `references/review-method.md`. Read it before constructing the subagent prompt. The external models deliberately use different, open-ended approaches — see Steps 6–7. Three models (Claude structured + Gemini open-ended + Codex open-ended) with maximum independence.

For documents with associated implementations (specs, process docs, automation docs), the skill automatically extends into an **ecosystem review** (Step 8) — checking cross-document consistency, code quality, spec-code alignment, and runtime verification. This runs without prompting when relevant assets are detected.


## When something goes wrong

When a step in this skill fails or needs a workaround, update this skill file with what you learned BEFORE continuing to the next step. Add failure modes, correct wrong assumptions, fix timing estimates. This takes 30 seconds and prevents the same friction next time.


## Steps

### 0. Pre-flight

Load deferred tools needed by later steps:
```
ToolSearch: select:WebSearch,WebFetch,AskUserQuestion
```

Set tab title:
```bash
MY_TTY=$(ps -o tty= -p $PPID 2>/dev/null | tr -d ' ') && echo "red-team: review" > "/tmp/claude-title-${MY_TTY}"
```

### 1. Read the document and gather context

Read the file at the path provided in `$ARGUMENTS`. If no path is given, ask the user which file to review.

Identify:
- **Document type:** Process doc, article draft, grant application, strategy doc, research note, etc.
- **Intended audience:** Who will read this? Be specific — "NOAA grant panel reviewers" not "scientists."

**Size check:** If the document exceeds ~8,000 words, flag it. Suggest either section-by-section review or a summary-then-deep-dive approach. For multi-file documents (e.g. a grant with budget spreadsheets), clarify what gets reviewed together vs. separately.

**For technical or domain-specific documents**, identify 2–3 domain conventions or requirements the reviewer should check against (e.g. "NOAA grants require Broader Impacts framing", "this journal requires Data Availability statements").

Then gather relevant context docs — not all are needed every time:

1. **Folder CLAUDE.md** — Read the CLAUDE.md in the document's parent folder (or nearest ancestor that has one). Contains audience, tone, and domain conventions.
2. **Voice reference** (for articles/written content) — Read the voice reference closest to the document's domain. For Planet Ocean / photography content: `05_AI WORKFLOW/CLAUDE/Voice References/Voice Reference — Simon Pierce (Planet Ocean).md`. For whale shark book content: `05_AI WORKFLOW/CLAUDE/Voice References/Voice Reference — Simon Pierce (Whale Shark Book).md`. For other domains, use the Planet Ocean reference as the general default.
3. **Comparison documents** — Use Glob/Grep to find 1–3 closely related vault files (same project, similar document type). These serve as precedent and convention references — not quality authorities. They show how similar documents are typically structured, not what "good" necessarily looks like.
4. **Current Projects** (for strategic docs) — Read `01_LIFE OS/Current Projects.md` to check alignment with current priorities.

A process doc doesn't need the voice reference. An article doesn't need Current Projects. Include only context that would sharpen the review.

5. **Communications scan** (for grants, strategy docs, specs with stakeholders) — Search Gmail and Slack for recent correspondence about the document's topic. This surfaces stakeholder constraints, prior feedback, political context, or decisions that the document itself may not reflect.
   - 2–3 Gmail queries via `mcp__claude_ai_Gmail__gmail_search_messages` (project/topic keywords + key contacts)
   - 1–2 Slack queries via `mcp__claude_ai_Slack__slack_search_public_and_private`
   - Read top 3–5 relevant threads
   - Extract: prior feedback, constraints, decisions, or context that the reviewer should know about
   - Include comms context in the subagent prompt (Step 2) so the reviewer can check whether the document accounts for known stakeholder input
   - **Skip for**: process docs, internal notes, publications, and `--quick` mode
   - **Graceful degradation**: If tools are unavailable, proceed without comms context

#### Ecosystem detection

For documents that describe implementations (process docs, specs, skill files, automation docs), detect associated assets for the ecosystem review in Step 8. This detection is silent — don't report findings to the user yet, just store them for later.

**Associated code** — search all three sources and accumulate matches (a process doc may mention the script explicitly but the LaunchAgent plist is only findable via naming conventions):
1. **Explicit paths**: Parse the document for file paths it mentions (`~/bin/...`, `~/.claude/skills/...`, LaunchAgent plist names, script references). Verify each path exists.
2. **Naming conventions**: Match the document's topic to likely code files (e.g. "Nightly Workhorse" → `~/bin/obsidian_reviews/nightly_workhorse.py`). Check `~/bin/obsidian_reviews/`, `~/.claude/skills/`, `~/scripts/`, and `~/Library/LaunchAgents/`.
3. **MEMORY.md lookup**: Search MEMORY.md for entries about the same topic — these often link specs to implementations with full paths.

Deduplicate across sources. Classify each match by confidence:
- **Exact**: file paths explicitly named in the document and verified to exist
- **Strong**: same basename or unique stem found in standard search roots
- **Weak**: MEMORY.md or related docs that link to this topic, but not directly named in the document

Auto-include Exact and Strong matches. Present Weak matches in the scope estimate for the user to confirm or dismiss.

**Related documents**: Identify docs that reference or are referenced by this document:
- MEMORY.md entries about the same topic
- `05_AI WORKFLOW/CLAUDE/Processes/Scheduled Automations.md` (if the doc describes an automation)
- The spec (if the document is a process doc) or the process doc (if the document is a spec)
- Other process docs in the same domain that share dependencies

**Automation config** (if the document describes a LaunchAgent/scheduled task):
- LaunchAgent plist path (typically `~/Library/LaunchAgents/nz.simon.*.plist`)
- Log file paths (typically `~/Library/Logs/`)
- State file path (typically `~/.config/`)

If detection finds nothing, Steps 8a–8c skip. Report this in the scope estimate so the user knows detection ran and found nothing (not that it failed silently).

**Scope estimate**: After detection, briefly report the total review scope to the user: document word count, number of associated code files (with approximate line counts), number of related documents, and whether runtime verification applies. This lets the user gauge total review time before committing. For `--quick` mode, note that ecosystem review will be skipped.

### 2. Run Claude subagent review

Read `references/review-method.md`. Use the Agent tool with a subagent to perform a critical review. The subagent gets fresh context (reduced anchoring risk, though some residual bias from shared tooling is possible).

Construct the subagent prompt:
- Include the role framing and full review sequence from `references/review-method.md`
- Include the full document text
- Include relevant context docs (with filenames as headers)
- Specify the document type, intended audience, and any domain-specific conventions identified in Step 1
- Frame as: "This is the first review pass. Be thorough — your findings will inform whether a second independent review is needed."

**Reference implementation flag:** If the document is a reimplementation of an existing tool (a spec, prototype, or code review aimed at matching a specific reference — e.g. "this R package must produce the same output as SOCPROG"), explicitly tell the subagent: *"This is a reimplementation of [reference]. A finding that claims the code deviates from standard practice is NOT a valid bug unless you have verified it against the actual reference implementation. 'Standard practice' and 'what the reference does' are different things — legacy tools often accumulate implementation choices that differ from textbook conventions. Do not flag a divergence from convention as a bug; flag only divergences from the stated reference."* This prevents AI reviewers from introducing real bugs by applying statistical/engineering best-practice expectations to code that must intentionally match a legacy implementation.

**Size/truncation check:** Before sending the subagent prompt, verify the full document text and context docs fit within the subagent's context window. If the combined prompt is too large: always include the full target document (never summarise what's being reviewed), but summarise long context docs, quote only the relevant sections of comparison documents, and strip examples from the review method unless they're needed for output format. Note what was omitted and flag this to the user when presenting results.

### 3. Assess subagent quality

Before presenting the review, check:
1. Does every issue cite a specific location in the document (quote or section name)?
2. Are the issues about the document's actual content, not generic writing advice?
3. Does the steelman demonstrate genuine understanding of the document's intent?

If any check fails, re-prompt with targeted instructions (max 2 retries total):
- Missing locations → "Re-do your review. Every issue must quote the specific text or name the exact section. No generic references to 'the introduction' or 'the middle section.'"
- Generic advice → "Your review reads like generic writing feedback. Focus on what's specific to *this* document — what would a domain expert notice?"
- Weak steelman → "Your steelman doesn't capture the core intent. Re-read the document and explain what it's actually trying to achieve before reviewing."

If the review is overall superficial (mostly "looks good" with minor wording suggestions), re-run: "Your first review was too lenient. Assume you're being paid to find real problems and propose real improvements. Go deeper — what's wrong, and what would make this genuinely better?"

If quality is still poor after 2 retries, present the best attempt to the user with a caveat: "The subagent review may be less thorough than usual — consider weighting the external review more heavily."

### 4. Verify key claims (if applicable)

Skip **web-based** fact-checking for process docs and internal notes. However, process docs often contain locally verifiable claims (commands, file paths, tool behaviour, runtime state) — verify those inline during the review rather than skipping verification entirely. Skip this step entirely only for documents with no verifiable claims at all.

For documents that make factual claims worth checking (grants, articles, strategy docs with data):

1. From the subagent review and the document itself, identify the 3 most consequential verifiable claims — facts, statistics, or assertions where being wrong would undermine the document's credibility or argument.
2. Use WebSearch to check each claim against primary sources. Look for the specific statistic, finding, or fact cited — not just general background.
3. For each claim, report: **Claim** (quote from document) → **Verdict** (confirmed / partially supported / unsupported / contradicted) → **Source** (URL or reference) → **Note** (any important caveats, e.g. the stat is correct but from 2019, not "recent").

Present verification results alongside the subagent review in Step 5. If a claim is contradicted, flag it as a High-severity issue regardless of what the subagent said.

### 4b. Citation audit (manuscripts and scientific documents only)

For documents with a References/Bibliography section (manuscripts, literature reviews, grant applications citing specific papers), run the automated citation verification script:

```bash
python3 ~/bin/verify_citations.py "DOCUMENT_PATH" -o /tmp/citation-report.md
```

This queries Semantic Scholar, CrossRef, and OpenAlex to verify each reference exists with correct author, year, and title. Takes ~1s per reference.

After the script completes, read `/tmp/citation-report.md` and:
1. **NOT_FOUND** references: WebSearch manually to determine if fabricated or just not in the APIs (book chapters and grey literature often aren't indexed)
2. **PARTIAL_MATCH** references: check whether the issue is a real error or a formatting/name variant
3. Report all citation issues as High-severity findings in Step 5

Skip this step for process docs, specs, and internal notes.

### 5. Present subagent feedback and apply improvements

Present the subagent's review reorganised by severity, followed by claim verification results (if Step 4 was run). This is the full review, reordered for readability — not filtered or softened:
1. Steelman + first impression (brief)
2. Issues by severity (High → Medium → Low)
3. Devil's advocate + "what would make you say no"
4. Enhancement opportunities
5. Strengths to preserve

Default to applying all recommended changes (issues + enhancements). Walk the user through items that require judgement one at a time — don't batch-present a menu of options.

**Before applying any edits**, create a snapshot so the user can roll back. Use the safest available method:
- If the file is in a git repo **and** there are no unrelated staged changes: `git add "path/to/file" && git commit -m "Pre-red-team snapshot: filename"` (use the file's actual repo root)
- If the repo is dirty or has unrelated staged changes: create a timestamped backup (`filename.2026-03-11T09-00.bak`) in the same directory
- If not in a git repo: create a timestamped backup in the same directory

**When applying edits, separate wording from substance:**
- Wording edits (clarity, conciseness, tone, flow) — apply as approved
- Meaning-changing edits (facts, figures, dates, commitments, citations, technical instructions) — flag each one explicitly and require individual approval before applying

Preserve the author's voice and style. Write in NZ/UK English. Improve the content without rewriting the personality out of it.

### 6. Independent model reviews (Gemini → Codex, sequential by default)

After subagent improvements have been applied, run two independent external reviews. **Default mode is sequential**: Gemini first against the post-subagent state, walk findings + apply, then Codex against the post-Gemini state, walk findings + apply. This is the gold-standard path because **each reviewer evaluates the post-prior-fix document** — Codex catches regressions introduced by Gemini's fixes (and Gemini catches what was introduced by the subagent's fixes). Validated 2026-04-28 in the v0 onboarding system round: Codex's most consequential finding (C1 — `/verify-citations` shipped without its bundled script) only existed because the subagent's H1 fix had added the skill to STARTER_SKILLS; running all three reviewers in parallel would have routed C1 through a synthesiser that might have folded it into H1 and missed the bundling gap. Three-reviewer cascade is the load-bearing pattern, not parallel-then-synthesise.

**Order rationale:** Subagent (Opus, structured rubric) → Gemini (open-ended fresh-eyes, second pass on subagent state) → Codex (deepest evaluator, traces actual code paths against post-all-prior-fixes state). Codex is last because it benefits most from the cascade — finds wiring bugs that only manifest after the document and its implementation have been edited.

**Annotated findings file convention:** Each external reviewer's findings are written to `/tmp/red-team-{gemini,codex}-findings.md` and copied to the vault as `OUTPUTS/onboarding-review-{gemini,codex}-YYYY-MM-DD.md` with an annotation header tracking which findings were applied vs deferred. This makes the audit trail durable across sessions.

**Opt-in `--parallel` mode:** For routine reviews of stable documents (quick blog post, doc tone check, no associated code) where cascade value is low and clock time matters more, the user can pass `--parallel` to run Codex + Gemini simultaneously and reconcile via Step 7's three-way comparison. Default stays sequential because the cost of missing a C1-class regression-of-a-fix is much higher than the extra clock time.

If `--quick` was specified, skip this entire step.

Proceed directly — do not ask for permission.

#### 6a. Build the Gemini prompt (sequential mode)

In `--parallel` mode, jump to Step 6e and build both prompts up-front instead.

Read the **post-subagent-fix document** (after Step 5 edits). Build a self-contained prompt file at `/tmp/red-team-gemini-prompt.md`.

**The prompt deliberately does NOT use `references/review-method.md`.** The subagent did the structured rubric review. Gemini gets an open-ended prompt — different lens catches different things.

The prompt file must include:
- The review instructions (framing block below)
- The post-subagent-fix document text in full
- Relevant context documents inline (folder CLAUDE.md, voice reference, etc.) so the reviewer has the same standards
- Document type, intended audience, and any domain conventions
- Author context: read `~/.claude/projects/<project-key>/config.json` for `user.name` + `user.role` and inject if both present; omit the line entirely if either is empty (per the same convention `/research` uses post-C7 fix). Do NOT hardcode a specific identity.
- **Do NOT include the subagent's findings or the structured rubric.** Independence means both approach and conclusions.

Use this framing at the top of the prompt file:

> This document has already been through one round of structured critical review and revision. Focus on what's still wrong — issues the first reviewer missed, problems introduced during editing, and fresh perspectives.
>
> Read the document cold. Give me your honest, unstructured reaction — what works, what doesn't, what's missing, and what would make this meaningfully better. Don't follow a checklist. Just tell me what you notice as someone reading this for the first time.
>
> Then get specific: for anything that needs fixing or improving, quote the relevant text, explain the problem, and suggest a concrete fix. For your best improvement ideas, draft replacement text showing what you mean.
>
> Rate each issue as High / Medium / Low priority.
>
> **Output your review as plain text only.** Do not edit any files or take actions beyond reading — just provide your written review.

**Pre-flight check** before executing:
- Is the document text complete (not truncated)?
- Are all referenced context documents included in full?
- Is the total prompt within Gemini's context window (~1M)?
- If anything was omitted or summarised, note it when presenting results.

#### 6b. Execute Gemini

```bash
gemini -p "" --output-format text --yolo < /tmp/red-team-gemini-prompt.md 2>&1 | tee /tmp/red-team-gemini-findings.md
```

**Timeout:** 600000ms (10 minutes). If Gemini times out, retry once. If it times out again, proceed without that reviewer (note the gap when applying findings).

**Error handling:**
- Gemini auth errors → tell the user to run `gemini` interactively to authenticate
- Model not found → try fallback, then proceed without that reviewer
- Any other error → report the error, proceed without that reviewer

Capture the full output. Copy the findings file to the vault as `<vault>/05_AI WORKFLOW/OUTPUTS/onboarding-review-gemini-YYYY-MM-DD.md` (or wherever the user keeps review outputs — read from the spec's Artifacts table if available).

#### 6c. Walk user through Gemini findings + apply

Present Gemini's findings to the user as a numbered list with one-line summaries + severity tags. Walk one at a time per the established interaction pattern (one item, recommended action, wait for user reply, advance). Apply each accepted fix immediately.

After the walk completes, write an annotation header at the top of the saved findings file (`onboarding-review-gemini-YYYY-MM-DD.md`) listing which findings were applied vs deferred (with reason for deferrals). This is the durable audit trail.

Now Codex evaluates the post-Gemini-fix state.

#### 6d. Build the Codex prompt against post-Gemini state

Read the **post-Gemini-fix document** (the document in its current state after 6c). Build the Codex prompt file at `/tmp/red-team-codex-prompt.md` with the same content rules as 6a (open-ended framing, full document text, context docs, neutral author identity from config), plus an explicit acknowledgement that Codex is the third reviewer in a sequential round:

> This document has been through structured-rubric review (subagent) and open-ended review (Gemini), with fixes applied between each. You are the third reviewer — the deepest pass. Your job is to find what the first two missed, and especially to catch any regressions that earlier fixes introduced. Trace actual code paths and implementation details if there are any associated assets — surface-level claims that "X was fixed" should be verified against the actual files.
>
> Output your review as plain text only.

#### 6e. Execute Codex

```bash
codex exec --full-auto --skip-git-repo-check --sandbox read-only "Read /tmp/red-team-codex-prompt.md and follow the review instructions exactly. Write findings incrementally to /tmp/red-team-codex-findings.md as you discover each one — do not batch." < /dev/null
```

`--sandbox read-only` enforces the guideline at the bottom of this skill (Codex must not modify files during review). `< /dev/null` closes stdin to prevent the v0.130.0 hang failure mode (see `memory/reference_codex_cli.md`).

**Model:** bare `gpt-5.5` from `~/.codex/config.toml` (the only Codex model accessible via CLI on a ChatGPT account — `-fast` and `-pro` variants return 400). xhigh reasoning also from config. Do not pass `-m` or `-c model=...`.

**Timeout:** 600000ms (10 minutes). Same error handling as 6b.

The "incremental write to findings file" instruction matters — Codex sometimes runs long, and incremental writes mean partial output is preserved if anything times out.

#### 6f. Walk user through Codex findings + apply

Same pattern as 6c: present Codex's findings as numbered list, walk one at a time, apply each accepted fix immediately, then write the annotation header on the saved findings file (`onboarding-review-codex-YYYY-MM-DD.md`).

After 6f, the document has been through three reviewer passes with apply-passes between each. Step 7 (incorporate external feedback) is largely already done inline; it only adds value in `--parallel` mode where the three-way reconciliation hasn't happened yet.

#### 6g. `--parallel` mode (opt-in fallback)

If `--parallel` was specified: skip 6a–6f. Build both prompts up front per the original convention, run them simultaneously via the standard `codex exec` and `gemini -p` commands, capture both outputs, and proceed to Step 7's three-way reconciliation. The Codex prompt does NOT include the "third reviewer in a sequential round" framing — both reviewers operate against the post-subagent-fix state independently.

#### 6c. Codex app fallback (for large or code-heavy reviews)

If the `codex exec` prompt exceeds ~100KB (common for code-heavy reviews with multiple source files), or if `codex exec` exhausts its context before producing a review, fall back to the Codex app:

1. Write the Codex prompt to `/tmp/red-team-codex-prompt.md` as usual
2. Copy to clipboard: `pbcopy < /tmp/red-team-codex-prompt.md`
3. Tell the user: "The Codex CLI prompt is too large for `codex exec`. Prompt is on your clipboard — paste it into the Codex app. Drop the response back when it's done."

The Codex app has better context management than `codex exec` and can handle larger prompts with file exploration. This is the preferred path for manuscript reviews with associated code repos.

**Manuscript mode:** For scientific manuscripts, use this journal-review prompt template instead of the standard open-ended framing:

> You are an expert peer reviewer for [target journal]. Review this manuscript as if preparing a formal referee report. Structure your review as:
> 1. **Summary** — what the paper does and its main contribution
> 2. **Major concerns** — methodological issues, overclaimed results, missing analyses, logical gaps
> 3. **Minor concerns** — clarity, presentation, missing details, inconsistencies
> 4. **Suggestions** — improvements that would strengthen the paper but aren't required
> For each issue, quote the relevant text and suggest a specific fix. Rate severity as High/Medium/Low.

This template produced substantially better manuscript reviews than the generic open-ended prompt during the Moz whale shark LIR review (4 Apr 2026).

#### 6d. Manual fallback (if both CLIs and app unavailable)

If all automated paths fail, fall back to the manual workflow:
1. Copy one prompt file to clipboard: `pbcopy < /tmp/red-team-codex-prompt.md`
2. Tell the user the prompts are on their clipboard and at `/tmp/red-team-codex-prompt.md` and `/tmp/red-team-gemini-prompt.md`
3. **Scope disclosure:** State what the reviewer will and will not be able to verify independently.
4. **Data safety reminder:** Consider whether the document contains sensitive information before pasting into an external model.
5. Ask the user to paste the responses back when they have them.

### 7. Incorporate external feedback (parallel mode only)

**Sequential mode (default):** Step 7 is largely already done — each reviewer's findings have been walked through and applied inline at 6c and 6f. Skip ahead to Step 8 (ecosystem review). The only Step 7 work that may still apply: cross-reviewer pattern observations that didn't fit any individual finding (e.g. "all three reviewers flagged audience framing — that's a structural issue worth a Decision Log entry"). Brief — most synthesis happened inline.

**Parallel mode (`--parallel`):** Run the full three-way reconciliation below, since neither external reviewer's findings have been applied yet.

Whether feedback came from automated CLI calls (Step 6b/6e), the Codex app (Step 6c), or pasted back by the user (Step 6d):

1. Present both reviews to the user in full — don't filter or soften them.

2. Compare all suggestions across the three reviewers (subagent + Codex + Gemini) and classify each:
   - **All three flagged** — highest confidence, apply directly
   - **Two of three agree** — high confidence, recommend applying
   - **Unique to one reviewer** — present with context, user decides
   - **Contradictions between models** — flag explicitly, these are the most interesting findings
   - **Enhancement ideas** — constructive suggestions from any reviewer, presented separately from issues

3. Batch low-effort, uncontroversial fixes (typos, command corrections, minor wording tweaks) and notify: "Applying these minor fixes: [list]." Apply them. This is transparent without requiring per-item approval.

4. For remaining items that need judgment, present a **triage list** using AskUserQuestion. Group items into a compact numbered list with one-line descriptions, which models flagged them, and your recommendation. Ask the user to reply with the numbers they want applied, e.g. "1, 3, 5" or "all" or "none". Example format:

   ```
   Items to triage (reply with numbers to apply, "all", or "none"):
   1. [Fix off-by-one in retry logic — all three flagged]
   2. [Add timeout to webhook call — Codex + Gemini]
   3. [Restructure intro paragraph — Gemini only, rec: consider]
   4. [Add Y section — Codex only, rec: skip, over-engineering]
   ```

   Keep descriptions to one line each. Don't explain the full reasoning unless asked — the user can read the review outputs.

5. **Before applying edits**, create a snapshot (git commit or .bak) so the user has a rollback point for the post-subagent state.

### 8. Ecosystem review

**Skip this entire step if the ecosystem detection in Step 1 found no associated code, related documents, or automation config.** When assets were detected, run all applicable sub-steps automatically — no user prompt to activate. If `--quick` was specified, skip this entire step.

**Scope guard:** If the associated code exceeds ~3,000 lines total, flag this to the user and suggest focusing on the most critical file(s) rather than reviewing everything. The ecosystem review should complement the document review, not double its duration.

**Before making any ecosystem edits**, create a snapshot (git commit or .bak) so the user has a rollback point for the post-document-review state.

#### 8a. Cross-document consistency

Read each related document identified in Step 1. Check for contradictions, stale information, or drift between the reviewed document and its related docs. Common patterns:

- MEMORY.md entry doesn't match the process doc's current description
- Spec says X but the process doc says Y (or vice versa)
- `Scheduled Automations.md` has outdated details about the automation
- A related process doc references a behaviour that has changed

**Fix drift directly.** For each inconsistency: determine which source is current (check git history, file modification dates, runtime evidence), update the stale one. Briefly note what was fixed — don't ask for approval on each fix.

If you can't determine which source is current, flag it for the user rather than guessing. Be especially careful with spec-to-code drift: a spec feature not in the code could mean "not yet implemented" (spec is correct, code is behind) rather than "outdated spec" (code moved on). Check git history and commit messages for intent before deciding which to update.

**Spec-body literal-claim check** (added 2026-04-27 after the v0 onboarding red-team caught spec drift twice in one pass — `00_INBOX` vs `INBOX`, `/schedule` mechanism still claimed in body): for each spec under review, grep the body for backtick-quoted file paths, skill names (`/foo`), and folder references. Verify each exists as described in the implementation. Flag any literal claim in the spec body that doesn't match what the implementation actually does. This catches the "implementation status section was updated but the older spec body sections still describe the original design" failure mode.

#### 8b. Implementation review

Run three parallel agents on the associated code detected in Step 1. Each agent gets the full code file(s) and the reviewed document as context.

**Evidence rule:** Any claim that something is "not wired", "not consumed", "broken", "unused", or "missing" must cite the actual code path checked, not docs-only inference. For wiring claims, read both the writer and reader sides before treating it as a finding. If the code was not checked, label it as an unverified hypothesis.

**Agent 1: Spec-code alignment (bidirectional)**
- Does the code implement everything the document describes?
- Is there code that does things the document doesn't mention? (Feature drift)
- When spec and code diverge: check `git log` on both files to determine which changed more recently. Fix the stale one — sometimes the code evolved correctly and the spec didn't keep up, sometimes the spec was updated but the code wasn't.
- For each divergence, note: what diverged, which was stale, what was fixed.

**Agent 2: Code quality**
- Redundant state or logic that duplicates existing functionality
- Copy-paste with slight variation that should be unified
- Leaky abstractions or broken encapsulation
- Unnecessary comments (explaining what, not why)
- Parameter sprawl or overly complex function signatures
- Stringly-typed code where constants or enums exist

**Agent 3: Code efficiency**
- Unnecessary work: redundant computations, duplicate API/network calls, N+1 patterns
- Missed concurrency: independent operations run sequentially when they could be parallel
- Overly broad operations: reading entire files when only a portion is needed
- Memory issues: unbounded data structures, missing cleanup
- Unnecessary existence checks (TOCTOU anti-pattern)

**Wait for all three agents to complete.** Agents research and report findings — they do not edit files directly (parallel edits to the same file will conflict). Aggregate findings from all three agents, deduplicate overlapping issues, then apply fixes sequentially. When agent recommendations conflict (e.g. one says code should match spec, another says the code has a quality issue that should be fixed differently), favour the source with more recent git history. If ambiguous, flag for the user. Summarise what was changed in a brief report to the user.

#### 8c. Runtime verification (automations only)

Skip if the document doesn't describe a LaunchAgent or scheduled automation.

Check the automation's actual runtime state:
1. **LaunchAgent status**: `launchctl list | grep <identifier>` — is it loaded? What was the last exit code?
2. **Recent logs**: Read the last 50 lines of stdout and stderr logs. Look for errors, warnings, or unexpected output.
3. **State file**: If the automation uses a state file, read it. Check last-run timestamp — is it recent enough given the schedule?
4. **Output files**: If the automation produces output files (e.g. in `01_LIFE OS/REVIEW QUEUE/`), check that recent output exists and looks reasonable.

Report discrepancies between documented behaviour and actual runtime state. Fix documentation that doesn't match reality. Flag code issues that need investigation (e.g. repeated errors in logs) — these may need the user's attention rather than an automated fix.

### 9. Done check

After all edits are applied (document review + ecosystem review), present the done criteria:
- All High severity issues resolved or explicitly accepted by the user
- Key factual claims verified via web search (Step 4) or flagged for manual verification by the user
- Final tone/voice pass completed (NZ/UK English)
- No known unexamined high-risk areas remaining
- Cross-document consistency verified (Step 8a) or no related documents found
- Implementation aligned with document (Step 8b) or no associated code found
- Runtime state matches documentation (Step 8c) or not an automation

Clean up any `.bak` snapshot files created during the review (they sync to iCloud and create clutter). Git snapshots are sufficient for rollback.

Ask the user if they consider the document ready, or if they want to iterate further.

## Guidelines

- The subagent review should be genuinely critical. The value of this process is in finding real problems, not in validation.
- Don't filter or soften the subagent's feedback before presenting it. Let the user see the raw assessment.
- The Codex and Gemini prompts must be self-contained — they should work whether executed via CLI or pasted into any capable model without vault access.
- When synthesising feedback from all three reviewers, flag disagreements explicitly. Divergent opinions are more interesting than agreements. Three-model convergence from independent reviews is the highest-confidence signal.
- **External CLIs**: The automated path is primary. Only fall back to manual clipboard when both CLIs are unavailable or fail. Use `--sandbox read-only` for Codex and `--yolo` for Gemini — reviewers should not modify files (Gemini's `--yolo` auto-approves tool calls but the prompt instructs text-only output).
- This skill works for any document type. Adapt the emphasis based on what the document is — a grant application needs different scrutiny than a process doc or a blog post.
- Use the standardised severity scale (High / Medium / Low) throughout. Do not mix in Critical / Important / Minor.
- Always create a snapshot before applying edits. The user should be able to roll back to any stage.
- **Context bundling:** Include only context docs that are genuinely relevant to the review. Don't pad prompts with irrelevant material — context should sharpen the review, not dilute it.
- **Concrete alternatives:** The best review suggestions include draft replacement text, not just "this could be better." Push all reviewers to show, not just tell.
- **Independence:** Do not leak the subagent's findings, the structured rubric, or the review methodology into the external model prompts. Do not leak one external model's prompt into the other's. The three reviewers should differ in both approach and conclusions. Convergence despite different methods — from three different models (Claude + GPT + Gemini) using different approaches (structured rubric + two independent open-ended reviews) — is the highest-confidence signal this process produces.

## Post-run improvement

After completing the task, assess skill performance across all phases:

**Document review (Steps 2–7):**
- Did any step fail, need workaround, or produce poor results?
- Were there missing steps or unclear instructions?

**Ecosystem review (Step 8):**
- **Detection accuracy**: Did the ecosystem detection in Step 1 find the right associated code, related documents, and automation config? Did it miss anything obvious? Did it find false positives?
- **Cross-document consistency**: Were the inconsistencies found genuine or false positives? Were fixes correct?
- **Implementation review**: Did the agents find real issues in the code? Were fixes appropriate? Did the bidirectional alignment correctly identify which source was stale?
- **Runtime verification**: Did the log/state checks reveal useful information? Were there runtime issues the code review missed?

**Apply fixes immediately** if patterns emerge (not one-off issues) — update this skill file, the detection heuristics, or the agent prompts. Don't just document the issue; fix it. Only defer changes that require the user's judgement.

Log genuinely surprising friction to the Friction Log.
