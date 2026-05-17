---
name: document
description: End-of-session handover. Summarises the session, captures decisions and lessons, and updates vault logs. Invoke proactively when the conversation is getting long, a substantial task is complete, or the session is winding down. Also use when the user says "wrap up", "save progress", "checkpoint", or signals goodbye.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, Skill
---

Perform an end-of-session handover. Review the full conversation and write updates to the vault.

**Proactive invocation**: Do not wait for the user to ask. Invoke this skill when a substantial task is complete, the session is naturally winding down, or the user signals goodbye/thanks. This is a safety net — continuous mid-session documentation (Decision Log, Friction Log entries written as work happens) is the primary mechanism. This skill catches anything that fell through the cracks.


## When something goes wrong

When a step in this skill fails or needs a workaround, update this skill file with what you learned BEFORE continuing to the next step. Add failure modes, correct wrong assumptions, fix timing estimates. This takes 30 seconds and prevents the same friction next time.


## Steps

### Pre-flight: load config + MEMORY.md health check

Before step 1, run:

```bash
# Resolve the per-vault project dir. Claude Code sanitises any non-alphanumeric
# character in the absolute vault path to a hyphen, so /Users/.../Simon's Vault
# becomes -Users-...-Simon-s-Vault. BUT pwd can drift below the vault root
# (e.g. cd'd into a subfolder mid-session), which would derive a key for a
# project dir that doesn't exist. So: first scan known project configs for one
# whose vault.path is pwd or an ancestor of pwd; only fall back to pwd-derived
# if no ancestor match. Confirmed 2026-05-17 — pre-flight failed in /document
# when cwd was 02_MARINE MEGAFAUNA rather than the vault root.
PROJECT_DIR=$(python3 -c '
import json, glob, os, sys
cwd = os.getcwd()
for p in glob.glob(os.path.expanduser("~/.claude/projects/*/config.json")):
    try:
        vp = json.load(open(p)).get("vault", {}).get("path")
        if vp and (cwd == vp or cwd.startswith(vp.rstrip("/") + "/")):
            print(os.path.dirname(p))
            sys.exit()
    except Exception:
        pass
# fallback: pwd-derived key
key = "".join(c if c.isalnum() else "-" for c in cwd)
print(os.path.expanduser(f"~/.claude/projects/{key}"))
' 2>/dev/null)
PROJECT_KEY=$(basename "$PROJECT_DIR")
CONFIG_FILE="$PROJECT_DIR/config.json"
MEMORY_FILE="$PROJECT_DIR/memory/MEMORY.md"

# Read is_simon feature flag. is_simon is a MACHINE property, not a per-vault
# property. pwd can drift mid-session (e.g. cwd in ~/repos/<repo> rather than
# the vault), so try pwd-derived first then fall back to a union scan across
# all known project configs. If ANY config has is_simon=true, this is Simon's
# machine. Newcomer machines union to false. Confirmed 2026-04-27: /update
# from inside ~/repos/mmf-claude-code returned is_simon=false on Simon's
# machine because pwd-derived path missed the vault project dir.
IS_SIMON=false
if [ -f "$CONFIG_FILE" ] && command -v python3 >/dev/null 2>&1; then
  IS_SIMON=$(python3 -c 'import json,sys; print(str(json.load(open(sys.argv[1])).get("features", {}).get("is_simon", False)).lower())' "$CONFIG_FILE" 2>/dev/null || echo false)
fi
if [ "$IS_SIMON" = "false" ] && command -v python3 >/dev/null 2>&1; then
  IS_SIMON=$(python3 -c '
import json, glob, os
for p in glob.glob(os.path.expanduser("~/.claude/projects/*/config.json")):
    try:
        if json.load(open(p)).get("features", {}).get("is_simon", False):
            print("true"); raise SystemExit
    except SystemExit: raise
    except Exception: pass
print("false")
' 2>/dev/null || echo false)
fi
echo "is_simon=$IS_SIMON"

[ -f "$MEMORY_FILE" ] || { echo "MEMORY.md not found at $MEMORY_FILE — skipping pre-flight"; }
LINES=$([ -f "$MEMORY_FILE" ] && wc -l < "$MEMORY_FILE" || echo 0)
BYTES=$([ -f "$MEMORY_FILE" ] && wc -c < "$MEMORY_FILE" || echo 0)
echo "MEMORY.md: $LINES lines, $BYTES bytes (caps: 200 / 25600)"
```

The `IS_SIMON` value above gates several Simon-personal sections later in this skill — they're flagged with `**SIMON-ONLY**` headers. If `IS_SIMON=false` (the default for newcomer installs), skip those sections entirely.

If `$LINES > 150` or `$BYTES > 20000`, flag this at the top of the handover entry so step 13 (Distil to MEMORY.md) knows to route new rules to Tier 2 leaves rather than Tier 1 inline. See `Processes/CLAUDE.md and MEMORY.md Maintenance.md` for the two-tier convention.

If within budget, proceed silently — no need to report the numbers.

### Numbered steps

1. **Locate the logs folder and read the current logs.**

   Read `~/.claude/projects/<project-key>/config.json` and resolve the logs folder from `folders.logs_relative` (default `SYSTEM`). The logs folder is `<vault>/<logs_relative>/`. If the config doesn't exist or the folder doesn't exist, this isn't a CLAUDE-managed vault — flag and stop.

   Reuse this resolved path (referred to below as the **logs folder**) for every log read/write in this skill. Don't hardcode `SYSTEM/` or any other prefix in subagent prompts or substeps — pass the resolved path through.

   Read the three current logs to understand their format and latest entries: `Session Handoff Log.md`, `Friction Log.md`, `Decision Log.md` (each inside the logs folder).

2. **Check for prior entries from this session**. Search the Session Handoff Log for today's date and a matching topic. If a handoff entry for this session's work already exists (from a mid-session checkpoint), update it in place rather than appending a duplicate.

   **EXCLUSION rule (paused-thread entries).** Handoff entries whose `## YYYY-MM-DD — ...` heading contains `[PAUSED]` OR whose `<!-- session:... -->` marker slug ends in `-paused` are EXEMPT from the same-day-matching-topic update-in-place heuristic. These are paused-thread siblings (written by `/do-this-later` Phase 5a) and represent in-flight work that must not be overwritten by a different session's `/document` run. Skip past them when searching for "your" handoff entry; if your topic matches one, write a fresh entry rather than updating the paused one in place.

3. **Check "What's next" from recent sessions** (concurrent-session-aware). Simon often runs multiple Claude sessions in parallel, so "the most recent prior entry" may belong to a DIFFERENT session whose work is orthogonal to yours. Read the last 2–3 handoff entries (anything dated within the last 3 days, up to 3 entries max). For each, note which of its "What's next" items were addressed by THIS session's work, which are still open, and which belong to a sibling session (orthogonal — leave to that session's owner). Include the follow-up in your handoff entry.

   **Session marker convention** (added 2026-04-20): Each new handoff entry should carry an HTML comment immediately after the `## YYYY-MM-DD — topic` heading in the form `<!-- session:topic-slug -->` where `topic-slug` is a kebab-case short identifier unique to the session's work (e.g. `meta-fixer`, `memory-restructure`, `thailand-lir`). This lets a concurrent `/document` disambiguate entries when rolling up open items. When writing your own entry, add the marker. When reading prior entries, treat entries with different markers as sibling sessions (their open items are NOT yours to close or drop).

   **Rollup rule**: When writing your "Follow-up on prior What's next" section, reconcile across all 2–3 recent entries — union of unresolved items, minus anything THIS session addressed. Do NOT silently drop items from a sibling session's What's next just because they weren't in the immediately-prior entry.

4. **Analyse the conversation** and identify:
   - What was worked on (brief summary)
   - Current state of any in-progress work (what's done, what's next, any blockers)
   - Non-obvious decisions made and their reasoning (check: were any already written to the Decision Log mid-session?)
   - Friction encountered (check: was any already written to the Friction Log mid-session?)
   - Lessons learned or reusable patterns discovered
   - Any process docs that were created or should be updated
   - Any recurring bottleneck that could be removed by a skill, script, or automation

   (Improvement candidates — emitted by the verification subagent's Pass 2 in step 11, then routed to the IMPROVEMENTS queue + Daily Log `[Self-improve]` by step 13. NOT surfaced inline in the step 19 report — that user-facing "Suggested improvements" pattern was removed 2026-05-17 in favour of async L6 self-improvement queue routing.)

5. **Prepend to the Session Handoff Log** with today's date and a brief topic label. Newest entries go to the top of the file (immediately below the intro/`## Format` section), separated from earlier entries by a `---` line. `/session-start` reads from the top, so prepending is what makes the most recent session's context the first thing the next session sees.
   - What was done
   - Current state (complete, or what's pending)
   - **Post-compaction focus** — a `> POST-COMPACTION FOCUS — read first.` blockquote banner immediately after the Framing block (or What was done if there's no separate Framing). Whatever length is needed to orient the next session — usually 1–4 sentences — naming the immediate next action(s) the post-compaction session should land on, including any context the next session needs to act (e.g. "Simon will paste Codex output post-compaction"; "rebuild from `<file>`'s frontmatter"; "the failing test is at `<path>:<line>`"). Default to elevating the topmost item from What's next; refine if Simon has explicitly named a focus during the session ("focus post-compaction on X"). Always include the banner — even if compaction never happens, it's cheap; when it does happen, it's the first thing the next session reads. Subsequent /document runs in the same long session refresh the banner on the new entry. Omit only if there is genuinely no continuing work (e.g. one-shot question session, all threads resolved).
     - **The banner is scoped to its own session.** It lives inside its handoff entry, which carries the existing `<!-- session:topic-slug -->` marker for concurrent-session disambiguation. **Post-compaction Claude must only act on a banner that belongs to its own session.** If a sibling session's entry happens to be at the top of the handoff log (because it was written more recently than yours), scan down past sibling-marker entries until you find your own session's entry and read THAT banner. Treat banners from other session markers as background context, not as instructions for you. The session you belong to is the one whose handoff entry's content matches the work-in-progress you remember from before compaction; if that's ambiguous, ask the user before acting on a banner.
   - Follow-up on prior session's "What's next" (addressed / still open / dropped)
   - What the next session should do or read first
   - **(SIMON-ONLY)** **Offer Things 3 tasks for deferred items**: If `IS_SIMON=true`, for each actionable item in "What's next" that Simon needs to take or review (not "continue work on X" session context), ask whether he wants a `/todo` created for it. List the items and let him pick. Skip this entire bullet if `IS_SIMON=false` — non-Simon users may not have Things 3 installed.
   - **Per-entry size check** (plumbing item #2, 2026-05-12). After writing the entry, count physical lines from the `## YYYY-MM-DD ...` heading to the next `---` divider (or end of file). If >80 lines:
     1. Check whether the entry already carries `<!-- size_accepted: YYYY-MM-DD -->` — if yes, skip the marker append (Simon has accepted it as-is).
     2. Otherwise append a single-line HTML comment immediately before the `---` divider:
        `<!-- size_warning: N_lines, threshold=80, options=[trim,manual,accept] -->`
     3. Do NOT append a visible warning block inside the entry — that consumes the same scarce `/session-start` read budget the limit is meant to protect (Codex finding 2026-05-11 under-reported gap #4).
     4. The nightly `apply_handoff_log_lifecycle()` aggregates oversized entries into a single Daily Log "For review" entry listing them with options (trim / manual-trim / accept). Simon picks per entry from there.

6. **Append to the Decision Log** if any non-obvious choices were made this session that haven't already been logged mid-session. Skip if none. For decisions that are provisional or context-dependent, add a `**Revisit by:** YYYY-MM-DD` line so future sessions know when to reassess.

7. **Append to the Friction Log** if anything was harder than expected that hasn't already been logged mid-session. Skip if none.

   **Canonical entry format (mandatory).** New entries MUST use the H2 status-tagged form so all consumers (`/session-start`, `/review-friction`, nightly `self_improve.py:scan_friction_log` + `age_friction_items`) can parse them:

   ```markdown
   ## [OPEN] YYYY-MM-DD: Short title (no markdown bold/italic in the heading)

   Body paragraph(s) describing the friction, what was tried, what the workaround was, and what the systemic fix would be.
   ```

   Status tags: `[OPEN]` (active), `[STUCK]` (active but blocked — auto-promoted by `age_friction_items` after 3 days), `[RESOLVED]` (terminal — moved to `## Resolved` section), `[WONTFIX]` (terminal). Plain-prose entries (no `## ` prefix, or markdown-formatted titles like `[OPEN] **YYYY-MM-DD — title**`) are silently invisible to all parsers — confirmed by the 2026-05-11 friction-log-parser-mismatch fix Codex review.

   **Insertion point:** new entries go at the top of the file (above other open entries), NOT inside the `## Resolved` section. The `## Resolved` heading is a section divider that splits open entries from the resolved archive.

   **Resolved-marker scan (legacy):** Also scan existing entries: prefix clearly-resolved entries with `✓` (e.g. `✓ Glob on ~ times out`) so they aren't re-reviewed in future sessions. Or, more cleanly, retag the heading from `## [OPEN]` to `## [RESOLVED]` and move the entry under `## Resolved`. Leave entries without a clear resolution unmarked.

8. **Session friction scan** — automated capture of tool failures and verbal corrections that weren't logged mid-session.

   **8a. Tool failure patterns**: Read `~/.claude/session-errors.jsonl` (if it exists and is non-empty). Group entries by tool name. Flag patterns: same tool failing 3+ times, or any MCP/tool hard failure. For each pattern, draft a Friction Log entry (root cause if identifiable, workaround used, systemic fix needed).

   **8b. Verbal corrections**: Scan the conversation transcript for moments where the user corrected the approach — patterns like "no don't", "stop", "that's wrong", "not what I asked", "I said", "why did you", "that's not right", "use X instead", "I told you", pushback on tool/method choices. Also look for repeated failed attempts at the same operation (Claude trying something, it failing, trying again with the same approach).

   **8c. Classify each finding**:
   - **Friction log entry** — the tool, skill, or process is broken and needs a systemic fix (e.g., "MCP times out", "skill uses wrong method"). Write to Friction Log.
   - **Feedback memory** — behavioural rule for future sessions (e.g., "don't use MCP for Things 3", "always confirm before sending emails"). Write to auto-memory.
   - **Already captured** — was logged mid-session or matches an existing friction/memory entry. Skip.
   - **Ambiguous** — present to the user and ask which category fits.

   **8d. Clear the error log** after processing: `rm ~/.claude/session-errors.jsonl` (the previous session's archive at `session-errors-prev.jsonl` is kept for reference).

   **8e. Instruction divergence scan**: Review the conversation for moments where the user gave an explicit tool, method, or approach instruction (e.g. "use Paperpile", "via the browser extension", "step by step", "Chrome not Brave", "do it with X"), and check whether the immediately following Claude actions honoured that instruction. Also flag any apology-without-behaviour-change pattern ("sorry", "you're right" followed by the same behaviour recurring).

   - If any divergences are found, include them in the handoff entry as a `## Instruction divergence` subsection. Format each as: `> "quoted instruction from the user"` followed by a bullet `- Diverged by: [what I did instead and when]`. This gives the next session explicit signal about where the pattern recurred.
   - If no divergences, do NOT include the subsection (signal: zero divergence is the desired state).
   - Divergence findings are ALSO relevant to step 8c classification: a divergence that matches an existing feedback memory means the rule wasn't followed (friction log entry, not new memory); a divergence on a novel trigger may warrant a new behavioural rule. Classify by frequency: **always-on → Tier 1 inline** in MEMORY.md's Feedback & instructions — Tier 1 section; **context-triggered (specific activity/domain) → new or existing Tier 2 leaf** (`memory/feedback_*.md`) with an explicit READ trigger in MEMORY.md's Tier 2 index. See `Processes/CLAUDE.md and MEMORY.md Maintenance.md` for the convention.

   **8f. Voice reference sweep**: Scan the conversation for any long-form external-facing writing drafted this session — emails, essays, newsletter sections, donor/funder comms, student-facing responses, supporter updates. For each draft, confirm: (a) was the voice guide declared in the first response per the CLAUDE.md Interaction Style rule, and (b) was a voice reference file (in `<logs folder>/Voice References/` — Simon's lives at `05_SYSTEM/Voice References/`; newcomer vaults don't ship one by default — skip silently if the folder doesn't exist) actually Read before the prose was written?

   - If any drafts were produced without a declared + read voice guide, include them in the handoff entry under a `## Voice reference gaps` subsection. Format: `- Drafted [type] without reading [applicable guide]`. Name the specific voice file that should have been consulted.
   - If the voice guide was correctly declared and read, don't include the subsection (zero is the desired state).
   - If the user corrected the tone of any draft this session (voice calibration feedback), that's a stronger signal — log to Friction Log per step 8c classification, not just the handoff subsection.

   For trivial sessions with no errors, corrections, divergences, or writing drafts, skip this step entirely.

9. **Doc-currency sweep via `/update`** — invoke the `/update` skill to handle all doc-update logic in one place (this replaces the prior steps 9 + 10 which duplicated `/update`'s discovery/classification/execution).

   ```
   Skill(skill: "update", args: "<derived scope from session>")
   ```

   Derive the scope argument from the session: a project name, topic, or comma-separated file paths the session touched. If session context is ambiguous, pass an empty string — `/update` will infer scope from context.

   **`/update` IS interactive when it has review items.** Per `~/.claude/skills/update/SKILL.md` step 7, `/update` will WAIT for the user's approval on judgement-call content changes (review items) before continuing. `/document`'s invocation of `/update` therefore blocks until `/update` completes its full pass — including any inline review-item walk with the user. This is the desired behaviour: review items are content judgements the user needs to resolve inline; the new step 20 report records counts only (the user already decided on each item during `/update`'s walk).

   **Skip `/update` if it already ran on the same scope earlier in this session.** Mirror `/do-this-later`'s skip rule — `/update` has no cross-invocation memory, and re-running it when vault state hasn't materially changed since the prior call is wasteful and risks duplicate Daily Log housekeeping entries. If `/update` was invoked earlier in the session on the same or overlapping scope, skip the `Skill` call and note the skip in the step 20 report.

   **If `/update` aborts** (e.g. its Codex dispatch fails on a 9+ doc scope), continue with the rest of `/document`'s steps and surface the abort in the step 20 report. Close-out is not gated on `/update` succeeding.

   After `/update` returns, read its natural-language Phase 4 summary and capture counts (auto-updates applied, review items resolved/pending, docs checked but not changed) for inclusion in the step 20 report.

10. **Update Current Projects**: Read the Current Projects file — try `<vault>/01_PROJECTS/Current Projects.md` first (Simon), then `<vault>/Current Projects.md` (newcomer). Skip this step if neither exists (the starter vault doesn't ship one). Based on the session analysis (step 4), make targeted edits:
   - **Remove** items that were completed this session (don't strikethrough — clean them out).
   - **Update status** of items that progressed (e.g., "draft started" → "v0.4 in review").
   - **Add** new priorities that emerged, if they're significant enough for a cross-domain orientation note (not every task — only things that change what matters right now).
   - **Don't touch** protected sections: Life razor, Patterns I'm noticing, What I'm avoiding, Idea explorations.
   - Update the "Last updated" date.
   - Skip if the session didn't materially change any Current Projects priorities.

11. **Verify log completeness and sweep for missed items** — after writing to the Session Handoff Log, Decision Log, and Friction Log (steps 5–7), spawn a sonnet verification subagent.

   **Skip threshold (narrower than it looks).** Skip ONLY when the session truly was trivial: a quick question with no file edits, a single-line read-and-explain, or a one-line cosmetic edit. Anything involving multi-file edits, log/changelog entries, commits, cleanup operations (file deletions, task deletions), skill/process-doc updates, or substantive Bash computation is NOT trivial — run the subagent. The subagent's gap-analysis pass (unacted-on recommendations, logical gaps, missing self-improvement loops, unsurfaced action items) is exactly what catches the issues a tired-end-of-session inline review misses. Confirmed 2026-04-26: a 2-file-edit + 6-deletion + 1-commit session was wrongly judged "borderline trivial" and skipped this step; the resulting improvement-draft routing (step 13) is also skipped when this step is skipped (hard dependency).

   The subagent performs two passes:

   **Pass 1 — Log completeness** (existing):

   > Scan the full conversation transcript. Independently list:
   > 1. **Decisions** — any non-obvious choice or trade-off made during the session (tool selection, approach, scope).
   > 2. **Friction** — anything that was harder than expected, failed unexpectedly, or required a workaround.
   > 3. **Open threads** — work that was started but not finished, or next steps that were identified.
   >
   > Then read the entries just appended to the logs (paths supplied below by the parent skill — `<LOGS_PATH>/Session Handoff Log.md`, `<LOGS_PATH>/Decision Log.md`, `<LOGS_PATH>/Friction Log.md`; the parent resolves `<LOGS_PATH>` from the cascade lookup in step 1). Read each one's most recent entry.
   >
   > Also read the Current Projects file (`<CURRENT_PROJECTS_PATH>` — supplied by parent; may be unset if the user's vault doesn't have one) and check whether any session completions or new priorities are missing from it.
   >
   > Report any **genuine gaps** — decisions, friction, open threads, or Current Projects updates in the conversation that weren't captured. Don't flag style differences or minor omissions.

   **Pass 2 — Unacted-on recommendations sweep**:

   > Scan the full conversation transcript again. Identify:
   >
   > 1. **Unacted-on recommendations** — suggestions or improvements proposed by either party (Claude or Simon) during the session that were acknowledged or discussed but never implemented, converted to a TODO, or explicitly deferred. Include the context of what was suggested and why it matters.
   > 2. **Logical gaps** — things that logically follow from the work done but weren't addressed. Examples: "we built X but didn't test it", "we updated the skill but not the process doc that references it", "we added a new automation but didn't add it to Scheduled Automations.md."
   > 3. **Missing self-improvement loops** — any skill, process doc, or automation that was created or substantially modified this session but lacks a retrospective, self-assessment, or feedback mechanism. Check whether the file has a post-run improvement section (for skills) or a lessons-learned prompt (for process docs).
   > 4. **Unsurfaced action items** — things that need Simon's review or manual action but weren't created as Things 3 tasks or otherwise flagged. This includes: review queue items without corresponding tasks, files that need manual review, external actions (emails to send, people to contact), and configuration changes that require Simon's credentials.
   >
   > For each item found, classify as one of:
   > - **Apply now** — can be fixed in this session without Simon's judgement (e.g., updating a cross-reference, adding a self-assessment section to a skill).
   > - **Create TODO (Things 3)** — needs Simon to take an action only he can take (send an email, review a proposal, make a scope/design decision, run an interactive command, apply credentials). If Claude can verify/act on it autonomously on a future date, DO NOT pick this — use System housekeeping instead.
   > - **System housekeeping (Daily Log)** — a deferred check or action that Claude can perform autonomously on or after a specific date: "verify filter fired after N runs", "delete backup file X on YYYY-MM-DD", "confirm automation healthy after stability window". Route to the Daily Log if one exists (Simon: `05_SYSTEM/OUTPUTS/Daily Log.md`; newcomer vaults don't ship one — fall back to "Note for next session" instead). The `System housekeeping → Daily Log` MEMORY rule applies for Simon's setup — do NOT create a Things 3 task for autonomous checks.
   > - **Note for next session** — not urgent but should be captured in the handoff log's "What's next" section.
   >
   > Test for routing: "Can Claude assess this without Simon's input, given enough time?" If yes → System housekeeping. If no → Create TODO.
   >
   > Report findings grouped by classification. Be selective — only flag items that genuinely matter. Don't flag things that were explicitly deferred with reasoning, or trivial style suggestions.

   **Pass 2 also emits an `Improvement candidates` block** as the formatting bridge to step 13 (improvement-draft routing). This is in addition to the gap-classification report above.

   > Additionally, identify any **improvement candidates** for the L6 self-improvement queue — workflow patterns, skill enhancements, automation opportunities, or quality improvements that surfaced during the session and would benefit from being proposed as a durable IMPROVEMENT (not just a fleeting note). For each candidate, emit the following block (matching the canonical `~/bin/obsidian_reviews/self_improve.py:4384-4395` producer contract):
   >
   > ```
   > ### Candidate: <Short title>
   > - **Rationale:** <1-3 sentences — why this is valuable>
   > - **Current state:** <what exists today>
   > - **Proposed change:** <specific, concrete change>
   > - **Affected files:** <vault-relative or absolute paths>
   > - **Cold-start prompt:** <a complete Claude Code prompt that could implement this in a fresh session>
   > ```
   >
   > Be selective. Phase A drafting upper bound: 2–4 candidates per session. If nothing surfaces, return zero. Do NOT include candidates that duplicate existing IMPROVEMENT files (a quick `Glob` of `01_PROJECTS/REVIEW QUEUE/IMPROVEMENTS/` and `06_ARCHIVE/IMPROVEMENTS/` is appropriate).

   The verification subagent's structured output now has TWO sections: the existing gap-classification report AND the Improvement candidates block. Step 13 consumes the latter.

   Review the subagent's report and act on it:
   - **Apply now** items: make the changes directly.
   - **(SIMON-ONLY)** **Create TODO (Things 3)** items: if `IS_SIMON=true`, create Things 3 tasks with vault links and clear descriptions. If `IS_SIMON=false`, downgrade these items to "Note for next session" (next bullet).
   - **(SIMON-ONLY)** **System housekeeping (Daily Log)** items: if `IS_SIMON=true`, call `daily_log_helper.append_system_housekeeping()` rather than raw-editing `05_SYSTEM/OUTPUTS/Daily Log.md`. The helper acquires the Daily Log lock + writes atomically (per spec `2026-05-17-internal-loop-write-concurrency-safety.md`), produces the canonical entry format, and includes the `[created: YYYY-MM-DD]` tag automatically. Invocation:
     ```bash
     PYTHONPATH="$HOME/bin/obsidian_reviews" python3 -c "
     from daily_log_helper import append_system_housekeeping
     append_system_housekeeping(
         topic_slug='<short-slug>',
         check_after='YYYY-MM-DD',
         description='Brief observation + why it matters',
         check_action='named verification command + if-A-then-X else-escalate branch',
     )
     "
     ```
     Renders: `- **[<topic-slug> — check after YYYY-MM-DD]** description. **Check action:** ... [created: YYYY-MM-DD]`. Claude picks these up on future sessions after the check-after date.
     DO NOT use raw `Edit` on Daily Log for housekeeping appends — bypasses the lock + risks concurrent-write data loss with /tomorrow, /update, healthchecks, and the nightly. If `IS_SIMON=false`, append the deferred check to the handoff entry's "What's next" instead — the user's vault doesn't have a Daily Log file by default.
   - **Note for next session** items: add to the "What's next" section of the handoff entry (update step 5 entry if already written).
   - **Improvement candidates** are NOT acted on here — they feed step 13's routing.
   - Report all items and actions taken to the user in step 19 (the report).

12. **Distil to MEMORY.md**: Review what was learned this session and check whether any patterns should be promoted to auto-memory. The convention changed 2026-04-20 to a two-tier model (see `Processes/CLAUDE.md and MEMORY.md Maintenance.md` for the full convention):

   - **Feedback memories — classify by firing frequency:**
     - **Tier 1 (always-on) → inline in MEMORY.md's `## Feedback & instructions — Tier 1` section.** Rules that fire every session regardless of task (interaction style, filing defaults, execute-now rules, Things 3 rules, meta). Format: `**Rule title.**` heading + compressed body (critical Why/How only — anecdotes belong in a leaf or process doc, not inline).
     - **Tier 2 (context-triggered) → `memory/feedback_*.md` leaf file** with `type: feedback` frontmatter. Rules scoped to a specific activity, domain, or file type (email drafting, scientific analysis, newsletter, exec-coach, etc.). Add a one-line index entry under `## Feedback & instructions — Tier 2` in MEMORY.md with an explicit "READ before [trigger]" directive so Claude loads the leaf on demand.
     - When in doubt, start as Tier 2 (smaller blast radius if miscategorised) and promote to Tier 1 if the rule is firing late in practice.
   - **Reference / tool-quirk / user-context / infrastructure memories → leaf file** (e.g. `reference_example.md`, `tool_quirks.md` appended entry, `user_photo_gear.md`) with typed frontmatter. Add a one-line pointer in MEMORY.md's relevant section.
   - To update an existing Tier 1 rule, edit the inline block in MEMORY.md directly.
   - To update an existing Tier 2 rule or reference leaf, edit the leaf and update the MEMORY.md index line if the description/trigger changed.

   Read the current `MEMORY.md`, then apply these heuristics:
   - Infrastructure facts and user preferences: promote immediately (factual, not judgmental).
   - Friction/tool quirks: promote after 2+ encounters or when a stable workaround exists.
   - Workflow patterns: promote after successful use in 2+ sessions.
   - Behavioural corrections from Simon: classify by frequency (see above) and add to the correct tier immediately if the correction is specific and actionable.
   - Update existing entries if this session refined or corrected them.
   - Remove entries that turned out to be wrong or are no longer relevant.
   - **Expiry check**: For each entry, ask: "Is this still accurate?" Specific cadences:
     - *Tool quirks*: If the tool was used successfully without hitting the quirk, note it may be outdated. Flag for removal if unconfirmed for 3+ months.
     - *Infrastructure / Vault conventions / Workflow patterns*: Spot-check any entry that feels stale. Remove if confirmed outdated.
   - **Budget**: MEMORY.md has a hard cap of 200 lines / 25 KB (the loader truncates past this). Target ≤150 lines to preserve headroom. If MEMORY.md is approaching the cap, move context-triggered rules from Tier 1 to Tier 2 leaves rather than compressing Tier 1 rules past the point of usefulness.
   - Skip this step if the session was trivial or nothing new was learned.

13. **Improvement-draft routing** — replaces the old user-facing "Suggested improvements" section. Take the verification subagent's Improvement candidates block (from step 11's Pass 2) and route surviving items to the L6 self-improvement queue.

   **Hard dependency on step 11.** If step 11 was skipped (trivial session), step 13 is skipped too. No draft generation outside the verification-subagent path.

   **Backlog gate (BLOCKING, live-queue-scoped).** Before doing anything else, scan `01_PROJECTS/REVIEW QUEUE/IMPROVEMENTS/*.md` for live unreviewed proposals (files whose `## Decision` heading is missing or empty per `~/bin/obsidian_reviews/self_improve.py:1709`'s `_extract_decision_section()` check). Compute count and max age (filename date parsed via `self_improve.py:1697-1700`). If `len(unreviewed) > 3 AND oldest > 14 days` (matching the existing gate at `self_improve.py:1755-1758`), DO NOT write new proposals this run. Surface a single one-line handoff-log note: `Improvement-draft routing skipped — backlog gate triggered (N unreviewed, oldest M days). Walk via /system-upgrade before queueing more.` Skip the rest of step 13. The gate is recomputed live each call — not session-scoped.

   **Inline Cut-criteria check** (mandatory; lifted from the previous Phase B prompt to preserve the bar).

   Cut criteria — drop the candidate if ANY apply:
   1. Too narrow / one-off value; covered by an existing skill, process doc, or memory entry.
   2. Shallow rephrasing of work already done this session.
   3. Speculative ("might be useful") rather than concretely valuable.
   4. Too low-stakes vs. the implementation cost.
   5. Symptom-only when the underlying root cause is unaddressed.
   6. Would generate noise (false positives, log spam).
   7. **Scope inflation** — the proposed mechanism is larger than the actual problem.
   8. **Mechanism over-engineering** — a new script/automation/process doc proposed for a problem an existing mechanism already covers.
   9. **Conceptual muddle** — the proposed change applies to a context not actually validated.

   Three pressure-test questions (mandatory for each surviving candidate):
   1. **Does this fix the cause or just the symptom?** A one-off action that the same warning could trigger again next session is symptom-only. If an existing housekeeping/investigation entry addresses the root cause, let it fire instead.
   2. **Is this in scope for the current run?** /document is wrap-this-session. Heavy multi-file restructures, MEMORY.md sweeps, or dependency-chasing belong in their own session.
   3. **Does executing this now respect prior deliberate state?** If the suggestion reclassifies entries previously classified by Simon (or a prior /document run), the prior classification was probably deliberate. Autonomous reversal needs strong evidence.

   If any of the three pressure-test questions trips, drop the item. The bar is high — under-surface preferred to over-surface.

   **Write the IMPROVEMENT proposal file** for each surviving candidate, using the canonical `~/bin/obsidian_reviews/self_improve.py:4384-4395` producer template:

   - **Filename:** `Improvement — YYYY-MM-DD — <slug>.md` where `YYYY-MM-DD` is today's date and `<slug>` is a short kebab-case description. The dated filename is REQUIRED — `self_improve.py`'s age parser at `:1697-1700` defaults missing-date files to today's age, silently masking aging across the queue.
   - **Body sections (in order):** `# <Title>` heading; `## Rationale`; `## Current state`; `## Proposed change`; `## Affected files`; `## Cold-start prompt`. **No `## Decision` heading at write time** — its absence is the "undecided" signal for `_extract_decision_section()`. `/system-upgrade` Source #1 surfaces files that lack a populated `## Decision`; the empty heading is added later when the decision is made.
   - **Frontmatter (recommended):** `title:`, `date:`, `category:`, `priority:`, `source: /document` (or `/do-this-later`). The `source:` field distinguishes manual-writer proposals from nightly `self_improve.py` proposals.
   - **Path:** write to `01_PROJECTS/REVIEW QUEUE/IMPROVEMENTS/` (current canonical per `self_improve.py:57`). DO NOT use the legacy `01_LIFE OS/REVIEW QUEUE/IMPROVEMENTS/` path that appears in older Daily Log entries — pre-migration drift.

   **Surface via Daily Log** using `daily_log_helper.log_entry()` with the explicit `source=rel_path` kwarg. Since /document runs from the vault, use the PYTHONPATH shell form (no editable install):

   ```bash
   PYTHONPATH="$HOME/bin/obsidian_reviews" python3 -c "
   from daily_log_helper import log_entry
   log_entry('For review', 'Self-improve', '<Title>. \`<rel_path>\`', source='<rel_path>')
   "
   ```

   This renders: `- [ ] **[Self-improve]** <Title>. \`<rel_path>\` [created: YYYY-MM-DD] [source: <rel_path>]`. The bold token is `**[Self-improve]**` ONLY — NOT `**[For review][Self-improve]**`. `## For review` is the section heading, not part of the bold token.

   **Dedupe before appending (three-tier fallback chain).** Before appending the Daily Log entry, search the existing `## For review` section in this priority order:
   1. **Primary key:** `[source: <rel_path>]` exact match (post-2026-05-17 entries from both writers).
   2. **Fallback 1:** Backticked path `` `<rel_path>` `` in the description body (pre-fix entries from `self_improve.py` or any other writer).
   3. **Fallback 2:** Normalised title match (case-insensitive substring on the IMPROVEMENT title — covers entries lacking both source metadata and backticked paths).

   If any tier matches, update the matched entry's `[created:]` date in place rather than appending a duplicate. If none match, append a fresh entry.

   **No Opus subagent dispatch.** The previous Phase B Opus filter is removed entirely; the inline Cut-criteria check above replaces it. If the inline check is too lax in practice and `/system-upgrade` reports noise, the fix is to tighten the inline check, NOT to re-introduce the filter subagent.

14. **Log maintenance** — keep the active sections lean:
   - **Session Handoff Log** (plumbing item #2, 2026-05-12). Canonical archival lives in `self_improve.py:apply_handoff_log_lifecycle()` — runs unconditional, strict-date (≥30 days), idempotent in the nightly 03:30 cycle. The foreground bridge for /document is:
     ```bash
     python3 ~/bin/obsidian_reviews/self_improve.py --handoff-only  # SIMON-ONLY
     ```
     Run this in step 14 so /document and the nightly converge on the same archival pass. If `IS_SIMON=false`, skip — newcomer machines don't have the obsidian_reviews script installed; the nightly automation owns archival.
   - **Decision Log**: Move entries >2 months old that have no future "Revisit by" date to the `## Archived decisions` section. Compress archived entries to 1-3 lines.
   - **Friction Log**: Move entries marked ✓ to the `## Resolved` section. Compress to one-line summaries.

15. **(SIMON-ONLY)** **Sync `~/.claude/` changes to the contributor repo (default-on)**: Skip this step entirely if `IS_SIMON=false` — newcomer users don't have the `mmf-claude-code` contributor repo and shouldn't be pushed to. If `IS_SIMON=true`:

   **Default behaviour: run the sync as part of /document's session-end work.** Simon's design choice (2026-04-29 evening): the trigger's job is "is the work stable enough to ship?", not "is the change broadly relevant?" — that latter question is the sync script's job (the script filters Simon-personal files; the trigger doesn't need to). Asking every session whether to sync produces the same answer almost every time, so default-on respects that.

   **Opt-out:** if `$ARGUMENTS` contains `--no-sync` (or the user invoked `/document --no-sync`), skip this step and note in the step 19 report that sync was deferred per the user's flag. Use this when a particular skill change isn't ready to ship — e.g. WIP, experimental, or Simon wants to refine before pushing.

   **Detection:** look for `sync-from-vault.sh` (or similar named sync script) in any cloned repo under `~/repos/`. The canonical example is `~/repos/mmf-claude-code/sync/sync-from-vault.sh`. If no sync script found, skip silently — the user isn't a contributor and this step doesn't apply. **Do not** invent a sync target or push to a repo the user hasn't established a sync flow with.

   **Sync flow when default-on:**
   1. Check `git status` in `~/.claude/` — confirm any session-modified skills/templates/CLAUDE.md are committed (per the pre-authorised commit class for `~/.claude/` infrastructure).
   2. **Capture `PRE_SYNC_HEAD`** before the sync runs so the course sweep (step 6) can diff what actually changed:
      ```bash
      cd ~/repos/mmf-claude-code
      PRE_SYNC_HEAD=$(git rev-parse HEAD)
      ```
   3. Run the sync script with the **`--commit` flag** so it actually applies, commits, and pushes (default behaviour without the flag is dry-run only): `./sync/sync-from-vault.sh --commit`. The script asserts the repo is on `main`, pulls latest, reads from `~/.claude/` filesystem state, applies its own filtering (Simon-personal references, hooks, settings stay local), stages mapped changes (skills/, guides/, templates/), and — when there are staged changes — commits with the message `sync: mirror from vault (<date>)` and pushes explicitly to `origin main`.
   4. **Capture `POST_SYNC_HEAD`** and the script's output for step 19:
      ```bash
      POST_SYNC_HEAD=$(git rev-parse HEAD)
      ```
      The script prints either "No changes to commit." (when only Simon-personal files were touched), or "Committed and pushed to origin/main: sync: mirror from vault (<date>)" (when something synced). Don't run a second commit / push — the script owns that path.
   5. **`--commit` aborts if mapped sources are missing locally.** Pass `--allow-missing` only when the user has explicitly OK'd pruning; otherwise an aborted sync usually means a recent vault rename/delete that needs investigating before pushing.
   6. **Run the course sweep.** After the sync returns (whether it committed or was a no-op), follow the protocol at `~/repos/mmf-claude-code/sync/course-sweep-protocol.md`. Pass: `REPO_ROOT=~/repos/mmf-claude-code`, `CALLER="document"`, the captured `PRE_SYNC_HEAD`, and `POST_SYNC_HEAD`. The protocol detects modified / new / deleted skills, proposes lesson edits one at a time, scaffolds lessons for new local skills that should ship, and archives lessons for retired skills. **Exits silently if there's nothing to sweep** (the common case for short sessions that didn't touch a starter skill). Surface the protocol's "Course sweep" summary block in step 19 if it ran.
   7. **Surface in step 19 report** under a `## Sync to mmf-claude-code` subsection (or similar): list the synced files with one-line each ("voice-capture skill (new)", "research skill v6 lessons", etc.), and the script's final line (commit message + push confirmation, or "No changes to commit."). Add the course-sweep summary block if step 6 produced output. If sync produced nothing AND the sweep was a no-op, say so explicitly.

   **Failure mode handling:** if the sync script errors (branch assertion fails because repo is on a side branch, filter breaks, file conflict, push rejected, missing-source abort), do NOT roll back — surface the error in step 19 and let Simon decide how to recover. Sync failure is not a /document failure; the rest of the handover should still complete.

16. **Flag completed notes for archiving**: If any vault notes worked on this session are now complete (plans executed, audits finished, process docs promoted to skills), note them for archival to the user's archive folder (Simon: `06_ARCHIVE/`; newcomer vaults don't ship one by default — flag for the user to create one or skip). Move them if Simon has given standing approval, or list them for confirmation.

17. **Evaluate skill candidates**: If any process doc has been used 3+ times with stable steps, note it as a candidate for skill promotion.

<!--
Old step 16b ("Generate Suggested improvements" — Phase A draft + Phase B Opus filter pass + inline render in report)
was REMOVED 2026-05-17 per spec 2026-05-17-session-closeout-skills-refactor.
Improvement-draft routing is now step 13 — writes proposals to IMPROVEMENTS queue + Daily Log [Self-improve],
consumed by /system-upgrade. The report (step 19) no longer carries a user-facing "Suggested improvements" section.
-->

18. **Autonomous-fix gate — close the friction-log loop.** This is the closure mechanism that prevents the Friction Log from becoming write-only. Replaces the older surface-proposed-fixes pattern: instead of reporting proposed fixes for Simon to act on later, this step *applies* mechanical fixes silently and walks judgement items with the user one-at-a-time in-session.

   Read the Friction Log. For each entry tagged `[OPEN]` or `[STUCK]` that is older than this session (skip entries just written in step 7 to avoid double-handling), classify:

   - **Mechanical** — entry contains enough information to fix without judgement:
     - Stale path / file reference with the corrected path stated (or trivially inferable)
     - Single-file typo, config update, or rename
     - Known dependency missing with a known install command
     - Workaround documented + the workaround IS the actual fix that should land in the source per the #1 rule
     - Reference to a renamed file/function (mechanical search-replace)
   - **Judgement** — anything affecting scope, design, voice, content, or that needs Simon's call. **Default to JUDGEMENT when uncertain** — never auto-fix on ambiguous classification.

   **For each Mechanical entry:**

   1. Apply the fix using available tools (Edit, Bash). Auto mode is on, no prompts.
   2. Retag the entry's H2 heading from `## [OPEN]` (or `## [STUCK]`) to `## [RESOLVED]` and append a brief note inline: `Auto-fixed YYYY-MM-DD — see Self-Improvement Changelog.` Move the entry under the `## Resolved` section per step 7's convention.
   3. Append a one-line entry to the Self-Improvement Changelog at `<vault>/<logs_relative>/Self-Improvement Changelog.md` (create the file with a brief header if missing):
      ```
      ## YYYY-MM-DD
      - **Friction:** *<entry title>* — auto-fixed in /document. <one-line summary of what changed>. Source: `<file:line>`.
      ```

   **For each Judgement entry:**

   1. Surface to the user one-at-a-time. Present:
      - Entry title, age (days since the entry's date), current status tag (`[OPEN]`/`[STUCK]`)
      - 1–2 sentence recap of the symptom and any fix-plan already noted in the entry
      - **Proposed action** — best-guess fix you'd apply if user approves, or "no clear fix — your call" if the entry is purely a decision
      - **Numbered options:**
        ```
        1. Resolved — apply the proposed fix (or describe an alternative)
        2. Defer — leave [OPEN], revisit on YYYY-MM-DD (provide a date)
        3. Won't fix — accepted limitation, mark [WONTFIX]
        4. Skip — leave [OPEN], we'll see it again next /document
        ```
   2. Wait for the user's reply.
   3. Apply the chosen action:
      - **Resolved**: apply the fix (or user-specified alternative), retag entry to `[RESOLVED]`, move under `## Resolved`, append to Self-Improvement Changelog as above.
      - **Defer**: append `**Defer to:** YYYY-MM-DD` line to the entry body. `/session-start` will skip deferred entries until the date.
      - **Won't fix**: retag to `[WONTFIX]`. Move under `## Resolved` (terminal status).
      - **Skip**: leave entry unchanged.
   4. **Kill switch**: if the user says "done", "stop", "enough", or signals fatigue mid-list, exit cleanly. Remaining judgement entries stay `[OPEN]` for the next `/document` run.

   **Cap**: no per-session cap on mechanical fixes (they're silent and git-reversible). No hard cap on judgement walks — the kill switch is always available. The autonomous-fix gate is *intentionally* willing to do a lot of work when there's a lot of accumulated friction.

   **Skip threshold**: if no eligible `[OPEN]` or `[STUCK]` entries exist (older than this session), skip step 18 entirely.

   **Append summary line** to the Step 19 report:
   `Friction sweep: auto-fixed N; resolved M with you; deferred D; wontfix W; skipped S.` Skip the line if no entries were processed.

19. **Report to the user**: **IMPORTANT: Do not run this step until ALL background subagents (verification, archival) have completed and their findings have been acted on.** Never declare "handover complete" while agents are still running — present interim status ("steps 1–N done, waiting on X") instead.

   **Required section order in the final report** (Simon flagged 2026-04-27 — recurring failure mode):

   1. Brief summary of what was logged, MEMORY.md changes, document update sweep results (step 9 — `/update` invocation: counts of auto-updates applied / review items resolved / docs checked-but-not-changed; OR skip note if /update was skipped because it already ran this session OR /update aborted), log maintenance performed, notes flagged for archival, and any skill candidates.
   2. **`**Verification:**` block** per the global CLAUDE.md proactive-verification rule. Either list each new file edited this /document run with `path:line` + short excerpt, OR — if this is a checkpoint /document where the handoff entry was updated in place and earlier edits were already verified inline — explicitly state `**Verification:** no verification needed because checkpoint /document made no new edits — all session work was verified inline at the time of each change`. Without this block the `stop-verification-check` hook will fire on the closing-line completion language. Confirmed 2026-04-25: hook fired three times in one session on `Handover complete` despite the work being captured.
   3. **One-line Improvements queued summary** from step 13 — one of:
      - `**Improvements queued:** N proposals written to \`01_PROJECTS/REVIEW QUEUE/IMPROVEMENTS/\` and surfaced via Daily Log \`[Self-improve]\`. /system-upgrade will walk them next Saturday.` (when N ≥ 1)
      - `**Improvement-draft routing skipped:** backlog gate (N unreviewed, oldest M days). Walk existing queue via /system-upgrade.` (when the backlog gate fired)
      - Omit the line entirely when no candidates surfaced (the common case) OR when step 11 was skipped (trivial session).

      NO user-facing "Suggested improvements" section. Removed 2026-05-17 per spec 2026-05-17-session-closeout-skills-refactor. The previously inline-rendered improvement ideas now ride the L6 self-improvement queue (IMPROVEMENTS files + Daily Log `[Self-improve]`) and are walked by `/system-upgrade` weekly. This keeps the close-out report focused on what just happened, not what should happen next.
   4. Closing line.

   End with: **"Handover complete — you are now clear to close or compact this session."**

20. **Suggest compaction if appropriate**: If the conversation is long or context usage is high, suggest running `/compact` after the handover. The pattern is: `/document` → `/compact` → re-read vault files to restore context. Only suggest this if there's remaining work — if the session is ending, just complete the handover.

## Guidelines
- Be concise in log entries. A few lines per section, not paragraphs.
- Use the same date/topic heading format as existing entries.
- Don't duplicate — if something was already logged earlier in the session (mid-session continuous documentation), reference it rather than re-writing it. The handover catches gaps, not repeats.
- If the session was trivial (quick question, no real work done), say so and skip the logs.
- If a log file doesn't exist, create it with a brief header (e.g., `# Session Handoff Log`) before appending.
- All vault paths are relative to the vault root recorded in `~/.claude/projects/<project-key>/config.json` under `vault.path`. Don't hard-code a vault path here — derive it at runtime so the skill survives a vault rename.
- The auto-memory directory is at `~/.claude/projects/.../memory/`. MEMORY.md is the index; individual memory files live alongside it. **(SIMON-ONLY)** Simon's vault has a copy at `05_SYSTEM/MEMORY (auto-memory).md` symlinked to the auto-memory MEMORY.md — edits to either location propagate. Newcomer vaults don't have this symlink; skip the assumption.

## Post-run improvement

After completing the task, briefly assess skill performance:
- Did any step fail, need workaround, or produce poor results?
- Were there missing steps or unclear instructions?

If patterns emerge (not one-off issues), update this skill file with fixes. Log genuinely surprising friction to the Friction Log.
