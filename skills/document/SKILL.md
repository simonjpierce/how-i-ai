---
name: document
description: End-of-session handover. Summarises the session, captures decisions and lessons, and updates vault logs. Invoke proactively when the conversation is getting long, a substantial task is complete, or the session is winding down. Also use when the user says "wrap up", "save progress", "checkpoint", or signals goodbye.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

Perform an end-of-session handover. Review the full conversation and write updates to the vault.

**Proactive invocation**: Do not wait for the user to ask. Invoke this skill when a substantial task is complete, the session is naturally winding down, or the user signals goodbye/thanks. This is a safety net — continuous mid-session documentation (Decision Log, Friction Log entries written as work happens) is the primary mechanism. This skill catches anything that fell through the cracks.


## When something goes wrong

When a step in this skill fails or needs a workaround, update this skill file with what you learned BEFORE continuing to the next step. Add failure modes, correct wrong assumptions, fix timing estimates. This takes 30 seconds and prevents the same friction next time.


## Steps

### Pre-flight: load config + MEMORY.md health check

Before step 1, run:

```bash
# Derive Claude Code's per-vault project key from the current working
# directory. Claude Code sanitises any non-alphanumeric character in the
# absolute vault path to a hyphen, so /Users/.../Simon's Vault becomes
# -Users-...-Simon-s-Vault.
PROJECT_KEY=$(pwd | sed 's|[^a-zA-Z0-9]|-|g')
PROJECT_DIR="$HOME/.claude/projects/$PROJECT_KEY"
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

   Determine the logs folder by trying these in order — first that exists wins:
   - `<vault>/AI_WORKFLOW/CLAUDE/` (starter-vault convention)
   - `<vault>/05_AI WORKFLOW/CLAUDE/` (Simon's vault numbering)

   Reuse this resolved path (referred to below as the **logs folder**) for every log read/write in this skill. Don't hardcode `05_AI WORKFLOW/` (Simon's prefix) or any other numbered prefix in subagent prompts or substeps — pass the resolved path through. If neither folder exists, this isn't a CLAUDE-managed vault — flag and stop.

   Read the three current logs to understand their format and latest entries: `Session Handoff Log.md`, `Friction Log.md`, `Decision Log.md` (each inside the logs folder).

2. **Check for prior entries from this session**. Search the Session Handoff Log for today's date and a matching topic. If a handoff entry for this session's work already exists (from a mid-session checkpoint), update it in place rather than appending a duplicate.

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

   (Suggested improvements — moved to step 16b so they can incorporate findings from the verification subagent, log maintenance, and archival sweeps. Generating them here produces shallower, pre-subagent output.)

5. **Prepend to the Session Handoff Log** with today's date and a brief topic label. Newest entries go to the top of the file (immediately below the intro/`## Format` section), separated from earlier entries by a `---` line. `/session-start` reads from the top, so prepending is what makes the most recent session's context the first thing the next session sees.
   - What was done
   - Current state (complete, or what's pending)
   - **Post-compaction focus** — a `> POST-COMPACTION FOCUS — read first.` blockquote banner immediately after the Framing block (or What was done if there's no separate Framing). Whatever length is needed to orient the next session — usually 1–4 sentences — naming the immediate next action(s) the post-compaction session should land on, including any context the next session needs to act (e.g. "Simon will paste Codex output post-compaction"; "rebuild from `<file>`'s frontmatter"; "the failing test is at `<path>:<line>`"). Default to elevating the topmost item from What's next; refine if Simon has explicitly named a focus during the session ("focus post-compaction on X"). Always include the banner — even if compaction never happens, it's cheap; when it does happen, it's the first thing the next session reads. Subsequent /document runs in the same long session refresh the banner on the new entry. Omit only if there is genuinely no continuing work (e.g. one-shot question session, all threads resolved).
     - **The banner is scoped to its own session.** It lives inside its handoff entry, which carries the existing `<!-- session:topic-slug -->` marker for concurrent-session disambiguation. **Post-compaction Claude must only act on a banner that belongs to its own session.** If a sibling session's entry happens to be at the top of the handoff log (because it was written more recently than yours), scan down past sibling-marker entries until you find your own session's entry and read THAT banner. Treat banners from other session markers as background context, not as instructions for you. The session you belong to is the one whose handoff entry's content matches the work-in-progress you remember from before compaction; if that's ambiguous, ask the user before acting on a banner.
   - Follow-up on prior session's "What's next" (addressed / still open / dropped)
   - What the next session should do or read first
   - **(SIMON-ONLY)** **Offer Things 3 tasks for deferred items**: If `IS_SIMON=true`, for each actionable item in "What's next" that Simon needs to take or review (not "continue work on X" session context), ask whether he wants a `/todo` created for it. List the items and let him pick. Skip this entire bullet if `IS_SIMON=false` — non-Simon users may not have Things 3 installed.

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

   **8f. Voice reference sweep**: Scan the conversation for any long-form external-facing writing drafted this session — emails, essays, newsletter sections, donor/funder comms, student-facing responses, supporter updates. For each draft, confirm: (a) was the voice guide declared in the first response per the CLAUDE.md Interaction Style rule, and (b) was a voice reference file (in `<logs folder>/Voice References/` — Simon's lives at `05_AI WORKFLOW/CLAUDE/Voice References/`; newcomer vaults don't ship one by default — skip silently if the folder doesn't exist) actually Read before the prose was written?

   - If any drafts were produced without a declared + read voice guide, include them in the handoff entry under a `## Voice reference gaps` subsection. Format: `- Drafted [type] without reading [applicable guide]`. Name the specific voice file that should have been consulted.
   - If the voice guide was correctly declared and read, don't include the subsection (zero is the desired state).
   - If the user corrected the tone of any draft this session (voice calibration feedback), that's a stronger signal — log to Friction Log per step 8c classification, not just the handoff subsection.

   For trivial sessions with no errors, corrections, divergences, or writing drafts, skip this step entirely.

9. **Update relevant process docs and skills**:
   - Identify 3–5 keywords from the session's work (tools used, workflows touched, domain topics).
   - Grep `<logs folder>/Processes/` for those keywords (Simon: `05_AI WORKFLOW/CLAUDE/Processes/`; newcomer: `AI_WORKFLOW/CLAUDE/Processes/`). Also check folder CLAUDE.md files in the user's top-level domain folders if the session touched those domains.
   - For each match, read the doc and check whether the session's work **changes, refines, or invalidates** anything in it. Update in place if so.
   - **Proactively flag improvements**: After checking for invalidation, also ask: "Did this session produce any reusable workflow patterns, conventions, or lessons learned that should be added to an existing process doc or skill?" Examples: a new convention discovered (e.g., unpublished data citation rules), a workflow step that proved valuable (e.g., citation quality audit), a tool integration pattern (e.g., checking org emails for authoritative figures). Flag these to the user with the specific doc/skill that should be updated and what should be added.
   - Don't create new process docs during handover — just flag if one should be created.

10. **Document update sweep** — verify all associated docs are current, using the `/update` skill's logic. This catches documents beyond process docs and skills (project notes, CLAUDE.md files, Artifacts tables, role notes, working files).

    - Extract 3–8 keyword seeds from the session (same as step 9, reuse them).
    - Check for an `## Artifacts` section in any primary project/analysis note touched this session. If present, iterate its rows — each listed file is a candidate. If the Artifacts table is incomplete (session created files not listed), update it.
    - If no Artifacts section, search: project notes in the user's top-level domain folders (Simon: `02_MARINE MEGAFAUNA/`, `03_PLANET OCEAN/`, `01_LIFE OS/`; newcomer: whatever folders were created during `/onboard`'s domain pass); folder CLAUDE.md files for domains touched; role notes if role-relevant work was done; Scheduled Automations if any automation changed.
    - For each candidate, read and check: is anything **stale**, **missing**, or **inconsistent** with this session's work? Skip docs already updated in step 9.
    - **Auto-update** mechanical changes (paths, statuses, cross-refs, dates) without asking.
    - **Flag for review** any content-level changes (rewrites, removals, scope changes) — present these to the user in step 16's report rather than blocking the handover.
    - If the session was trivial (quick question, single-file edit), skip this step.

11. **Update Current Projects**: Read the Current Projects file — try `<vault>/01_LIFE OS/Current Projects.md` first (Simon), then `<vault>/Current Projects.md` (newcomer). Skip this step if neither exists (the starter vault doesn't ship one). Based on the session analysis (step 4), make targeted edits:
   - **Remove** items that were completed this session (don't strikethrough — clean them out).
   - **Update status** of items that progressed (e.g., "draft started" → "v0.4 in review").
   - **Add** new priorities that emerged, if they're significant enough for a cross-domain orientation note (not every task — only things that change what matters right now).
   - **Don't touch** protected sections: Life razor, Patterns I'm noticing, What I'm avoiding, Idea explorations.
   - Update the "Last updated" date.
   - Skip if the session didn't materially change any Current Projects priorities.

12. **Verify log completeness and sweep for missed items** — after writing to the Session Handoff Log, Decision Log, and Friction Log (steps 5–7), spawn a sonnet verification subagent.

   **Skip threshold (narrower than it looks).** Skip ONLY when the session truly was trivial: a quick question with no file edits, a single-line read-and-explain, or a one-line cosmetic edit. Anything involving multi-file edits, log/changelog entries, commits, cleanup operations (file deletions, task deletions), skill/process-doc updates, or substantive Bash computation is NOT trivial — run the subagent. The subagent's gap-analysis pass (unacted-on recommendations, logical gaps, missing self-improvement loops, unsurfaced action items) is exactly what catches the issues a tired-end-of-session inline review misses. Confirmed 2026-04-26: a 2-file-edit + 6-deletion + 1-commit session was wrongly judged "borderline trivial" and skipped this step; the resulting Suggested improvements (step 16b) were shallow enough that Simon flagged it.

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
   > - **System housekeeping (Daily Log)** — a deferred check or action that Claude can perform autonomously on or after a specific date: "verify filter fired after N runs", "delete backup file X on YYYY-MM-DD", "confirm automation healthy after stability window". Route to the Daily Log if one exists (Simon: `05_AI WORKFLOW/OUTPUTS/Daily Log.md`; newcomer vaults don't ship one — fall back to "Note for next session" instead). The `System housekeeping → Daily Log` MEMORY rule applies for Simon's setup — do NOT create a Things 3 task for autonomous checks.
   > - **Note for next session** — not urgent but should be captured in the handoff log's "What's next" section.
   >
   > Test for routing: "Can Claude assess this without Simon's input, given enough time?" If yes → System housekeeping. If no → Create TODO.
   >
   > Report findings grouped by classification. Be selective — only flag items that genuinely matter. Don't flag things that were explicitly deferred with reasoning, or trivial style suggestions.

   Review the subagent's report and act on it:
   - **Apply now** items: make the changes directly.
   - **(SIMON-ONLY)** **Create TODO (Things 3)** items: if `IS_SIMON=true`, create Things 3 tasks with vault links and clear descriptions. If `IS_SIMON=false`, downgrade these items to "Note for next session" (next bullet).
   - **(SIMON-ONLY)** **System housekeeping (Daily Log)** items: if `IS_SIMON=true`, append to `05_AI WORKFLOW/OUTPUTS/Daily Log.md` under `## System housekeeping — Claude-managed` with `check-after: YYYY-MM-DD`, a description, a named verification check, AND a `[created: YYYY-MM-DD]` tag (today's date) so the F3 Daily Log lifecycle can age the entry out cleanly after the check action lands. Format: `- **[topic — check after YYYY-MM-DD]** description ... [created: YYYY-MM-DD]`. Claude picks these up on future sessions after the check-after date. If `IS_SIMON=false`, append the deferred check to the handoff entry's "What's next" instead — the user's vault doesn't have a Daily Log file by default.
   - **Note for next session** items: add to the "What's next" section of the handoff entry (update step 5 entry if already written).
   - Report all items and actions taken to the user in step 18.

13. **Distil to MEMORY.md**: Review what was learned this session and check whether any patterns should be promoted to auto-memory. The convention changed 2026-04-20 to a two-tier model (see `Processes/CLAUDE.md and MEMORY.md Maintenance.md` for the full convention):

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

14. **Log maintenance** — keep the active sections lean:
   - **Session Handoff Log**: If >800 lines, archive entries >30 days old:
     1. Determine archive file name: `Session Handoff Log - Archive YYYY-H#.md` (H1 = Jan–Jun, H2 = Jul–Dec)
     2. Create the archive file if it doesn't exist (with a `# Session Handoff Log — Archive` header)
     3. Move entries with dates >30 days old from the active log to the archive (append at top of archive, remove from active log)
     4. **Expected state, not prescriptive:** after step 3, typically ~20 recent entries remain in the active log. This is *descriptive* — do NOT archive additional young (<30 days) entries to force the count down to 20. Young entries from sibling sessions (look for `<!-- session:slug -->` markers) must stay in the active log regardless of count, so concurrent-session handoff rollups keep working.
     5. Report: "Archived N entries to [filename]"
     This runs automatically when the threshold is hit — don't ask for permission.
   - **Decision Log**: Move entries >2 months old that have no future "Revisit by" date to the `## Archived decisions` section. Compress archived entries to 1-3 lines.
   - **Friction Log**: Move entries marked ✓ to the `## Resolved` section. Compress to one-line summaries.

14b. **(SIMON-ONLY)** **Sync `~/.claude/` changes to the contributor repo (default-on)**: Skip this step entirely if `IS_SIMON=false` — newcomer users don't have the `mmf-claude-code` contributor repo and shouldn't be pushed to. If `IS_SIMON=true`:

   **Default behaviour: run the sync as part of /document's session-end work.** Simon's design choice (2026-04-29 evening): the trigger's job is "is the work stable enough to ship?", not "is the change broadly relevant?" — that latter question is the sync script's job (the script filters Simon-personal files; the trigger doesn't need to). Asking every session whether to sync produces the same answer almost every time, so default-on respects that.

   **Opt-out:** if `$ARGUMENTS` contains `--no-sync` (or the user invoked `/document --no-sync`), skip this step and note in the step 17 report that sync was deferred per the user's flag. Use this when a particular skill change isn't ready to ship — e.g. WIP, experimental, or Simon wants to refine before pushing.

   **Detection:** look for `sync-from-vault.sh` (or similar named sync script) in any cloned repo under `~/repos/`. The canonical example is `~/repos/mmf-claude-code/sync/sync-from-vault.sh`. If no sync script found, skip silently — the user isn't a contributor and this step doesn't apply. **Do not** invent a sync target or push to a repo the user hasn't established a sync flow with.

   **Sync flow when default-on:**
   1. Check `git status` in `~/.claude/` — confirm any session-modified skills/templates/CLAUDE.md are committed (per the pre-authorised commit class for `~/.claude/` infrastructure).
   2. Run the sync script with the **`--commit` flag** so it actually applies, commits, and pushes (default behaviour without the flag is dry-run only): `cd ~/repos/mmf-claude-code && ./sync/sync-from-vault.sh --commit`. The script asserts the repo is on `main`, pulls latest, reads from `~/.claude/` filesystem state, applies its own filtering (Simon-personal references, hooks, settings stay local), stages mapped changes (skills/, guides/, templates/), and — when there are staged changes — commits with the message `sync: mirror from vault (<date>)` and pushes explicitly to `origin main`.
   3. **Capture the script's output and report it in step 17.** The script prints either "No changes to commit." (when only Simon-personal files were touched), or "Committed and pushed to origin/main: sync: mirror from vault (<date>)" (when something synced). Don't run a second commit / push — the script owns that path.
   4. **`--commit` aborts if mapped sources are missing locally.** Pass `--allow-missing` only when the user has explicitly OK'd pruning; otherwise an aborted sync usually means a recent vault rename/delete that needs investigating before pushing.
   5. **Surface in step 17 report** under a `## Sync to mmf-claude-code` subsection (or similar): list the synced files with one-line each ("voice-capture skill (new)", "research skill v6 lessons", etc.), and the script's final line (commit message + push confirmation, or "No changes to commit."). If sync produced nothing, say so explicitly.

   **Failure mode handling:** if the sync script errors (branch assertion fails because repo is on a side branch, filter breaks, file conflict, push rejected, missing-source abort), do NOT roll back — surface the error in step 17 and let Simon decide how to recover. Sync failure is not a /document failure; the rest of the handover should still complete.

15. **Flag completed notes for archiving**: If any vault notes worked on this session are now complete (plans executed, audits finished, process docs promoted to skills), note them for archival to the user's archive folder (Simon: `06_ARCHIVE/`; newcomer vaults don't ship one by default — flag for the user to create one or skip). Move them if Simon has given standing approval, or list them for confirmation.

16. **Evaluate skill candidates**: If any process doc has been used 3+ times with stable steps, note it as a candidate for skill promotion.

16b. **Generate Suggested improvements** (2–4 ideas → Opus filter pass → final list shown to Simon): Now — AFTER the verification subagent (step 12), document-update sweep (step 10), log maintenance (step 14), and archival/skill-candidate evaluation (steps 15–16). Generating suggestions at this point lets them incorporate everything that came out of those steps (gaps the verification subagent flagged, patterns surfaced by archival, missing retrospective loops, etc.) instead of shallow pre-subagent guesses.

   **Hard dependency on step 12.** If step 12 was skipped (trivial session opt-out), do NOT generate Suggested improvements — they must be informed by the verification subagent's gap analysis. In that case, omit the Suggested improvements section entirely from the step 17 report, or state explicitly "Suggested improvements skipped — verification subagent did not run." Inline self-review without the subagent produces shallow, premature-feeling suggestions and misses the gap classes the subagent is designed to catch (unacted-on recommendations, logical gaps, missing self-improvement loops, unsurfaced action items). Confirmed 2026-04-26: meeting-prep-filter-fix session skipped step 12 as borderline-trivial; the suggestions generated felt premature to Simon, who flagged that improvements should always wait for the verification agents to finish.

   The corollary: if you are tempted to generate Suggested improvements, you should also be running step 12. Resist the "trivial session" opt-out unless the session genuinely involved zero file edits and zero substantive computation. Skill modifications, multi-file edits, log entries, commits, and cleanup operations are NOT trivial — run the subagent.

   **Two-phase generation:**

   **Phase A — internal draft (2–5 ideas).** Think about the workflows, skills, and processes touched this session. What enhancements, extensions, or adjacent improvements would you suggest if Simon asked "what else could we do here?" These should be ideas that weren't discussed during the session — things Simon might not think to ask about. Consider: missing integrations, underused data sources, automation opportunities, quality improvements, workflow gaps, and anything the verification subagent surfaced as a logical-gap pattern worth generalising. Be specific and actionable, not generic. Generate the internal draft in your scratch — do NOT show this version to Simon.

   **Phase B — Opus filter pass.** Spawn an Opus subagent (`subagent_type: "general-purpose"`, `model: "opus"`) with the internal draft and a brief framing of the session. The subagent's job is to be a hard gatekeeper:

   > You are reviewing draft "Suggested improvements" before they are shown to Simon. The bar is high: Simon already gets a steady stream of good suggestions and wants the noisy ones cut. Your job is to filter and improve.
   >
   > For each draft suggestion:
   > 1. **Cut it** if any of the following apply: too narrow / one-off value; covered by an existing skill, process doc, or memory entry; shallow rephrasing of work already done this session; speculative ("might be useful"); too low-stakes vs. the implementation cost; symptom-only when the underlying root cause is unaddressed; would generate noise (false positives, log spam); **scope inflation** (the proposed mechanism is larger than the actual problem — e.g. "sweep all skills" when the real scope is the four shipped in the starter bundle); **mechanism over-engineering** (new script / automation / process doc proposed for a problem an existing mechanism already covers — e.g. a new spec-lint script when /red-team already does this); **conceptual muddle** (the proposed change applies to a context the proposer hasn't actually validated — e.g. shipping a sync-script hook to a vault that has no sync scripts).
   > 2. **Sharpen it** if the idea is good but the framing is fuzzy — make the implementation concrete, name files/functions, state the value clearly, identify the failure mode it prevents. Also: validate the scope (count the actual targets) and pressure-test the mechanism (does an existing skill/hook/process already cover this?) before letting it through.
   > 3. **Recommend a verdict** per surviving suggestion: **Apply now** (cheap + high-confidence, do it in the next turn) / **Apply soon** (worth a Things 3 task or housekeeping check) / **Defer** (real value but needs more thought or signal to fire) / **Cut** (do not surface).
   >
   > Return ONLY the surviving suggestions, in order of strongest-first, with for each: a tight title, 2–4 sentences of substance, and a verdict line. If fewer than 2 suggestions survive, that's fine — under-suggesting is preferred to over-suggesting. If zero survive, return "No suggestions worth surfacing this session" and explain in one line why the drafts didn't clear the bar.

   Pass the subagent the full internal draft text plus 3–5 sentences of session context.

   **Phase B verdicts are inputs, not authoritative.** After the Opus filter returns, re-read each surviving suggestion + verdict and check it against your own first-principles read of the underlying evidence. Opus operates from the framing you gave it; if you disagree with a verdict (e.g. it says Defer but the evidence supports Apply now, or vice versa), surface your own assessment alongside the Opus verdict rather than rendering the filter output verbatim. The most common failure mode: Opus calling for a `--flag` opt-in when the evidence supports flipping the default outright (or vice versa). Calibration source: 2026-04-28 onboarding round — Opus filter recommended a `--sequential` opt-in flag for /red-team Step 6; Simon pushed back ("sequential did show value here?") and the C1 catch (regression-of-a-fix that only sequential would have caught) supported flipping the default rather than keeping parallel. Don't make Simon do that re-evaluation — do it before surfacing.

   **Pressure-test surviving suggestions against the Cut criteria — Opus often passes through a draft that Phase B says to cut.** The Phase B prompt lists "symptom-only when the underlying root cause is unaddressed", "scope inflation", and "mechanism over-engineering" as Cut criteria, but Opus may still let one through if the framing in your draft makes it look high-confidence. Before surfacing each surviving suggestion, ask three questions explicitly:

   1. **Does this fix the cause or just the symptom?** A one-off action that the same warning could trigger again next session is symptom-only. Look for an existing housekeeping/investigation entry that addresses the root cause — if one exists, the better-scoped action is to let that entry fire, not to do the workaround.
   2. **Is this in scope for the current run?** /document is wrap-this-session. Heavy multi-file restructures, MEMORY.md sweeps, or dependency-chasing belong in their own session, even if the spec for that work already exists elsewhere in the system.
   3. **Does executing this now respect prior deliberate state?** If the suggestion involves reclassifying entries that were previously classified by Simon (or a prior /document run), the prior classification was probably deliberate. Autonomous reversal needs strong evidence, not a "lean Tier 2" default.

   If any of the three trips, downgrade Apply now → Defer or Cut, and surface your own reasoning alongside Opus's verdict. Calibration source: 2026-04-29 — Opus filter passed "trigger MEMORY.md compression sweep as part of this /document" as Apply now (recommended) for the talk-import session; Simon flagged it on review with three-point reasoning (symptom-only vs investigation entry on Daily Log line 313; scope inflation against /document being a wrap-this-session run; deliberate Tier 1 classification not respected). The fix isn't to let Opus catch this — it's to do this pressure-test BEFORE surfacing.

   **Step 17 output format.** Render the Opus-reviewed list under the **Suggested improvements** heading as a numbered list (`1.`, `2.`, `3.`) with the verdict inline so Simon can reply with just a number to apply one. Format per item:

   ```
   1. **Title.** 2–4 sentences. **Verdict:** Apply now (recommended).
   2. **Title.** 2–4 sentences. **Verdict:** Apply soon — worth a Things 3 task.
   3. **Title.** 2–4 sentences. **Verdict:** Defer — wait for [signal].
   ```

   Add a one-line offer at the end: "Reply with a number to apply, or `none` to skip all." This is the easy-pick mechanism — Simon should be able to act on a recommendation without having to retype anything.

16c. **Lightweight self-improvement sweep — scan `[OPEN]` friction entries for now-obvious fixes.** Distinct from 16b: 16b generates *new* improvement ideas; 16c looks at the *existing* Friction Log for entries that have become mechanically fixable since they were logged.

   Read the Friction Log. For each entry tagged `[OPEN]` (or unmarked) that is older than this session, ask:
   - Is the root cause now understood (e.g. logged with a workaround that has since stabilised)?
   - Is the fix mechanical and non-detrimental (a path correction, a docs update, a guardrail, a one-line skill edit)?
   - Does an existing skill/script/process now cover it (so the entry can be marked `✓` and closed)?

   Cap the sweep at 5 entries — this is a lightweight pass, not a full friction review (use `/review-friction` for that). Skip entries that need Simon's judgement (design choices, scope decisions) or that aren't yet fixable (waiting on external state, missing tool).

   **Action per surviving entry**: include in the Step 17 report under a `## Open friction — mechanical fixes available` subsection, with the entry number/title, a one-line proposed fix, and a verdict (`Apply now` / `Apply soon` / `Cut — already resolved`). Simon's reply applies the chosen fixes; "none" skips.

   **Skip threshold**: If the Friction Log has fewer than 5 `[OPEN]` entries total, or if all open entries are recently logged this session, skip 16c entirely (nothing to sweep).

17. **Report to the user**: **IMPORTANT: Do not run this step until ALL background subagents (verification, archival) have completed and their findings have been acted on.** Never declare "handover complete" while agents are still running — present interim status ("steps 1–N done, waiting on X") instead.

   **Required section order in the final report** (Simon flagged 2026-04-27 — recurring failure mode):

   1. Brief summary of what was logged, MEMORY.md changes, document update sweep results (step 10 — auto-updates applied and any review items pending), log maintenance performed, notes flagged for archival, and any skill candidates.
   2. **`**Verification:**` block** per the global CLAUDE.md proactive-verification rule. Either list each new file edited this /document run with `path:line` + short excerpt, OR — if this is a checkpoint /document where the handoff entry was updated in place and earlier edits were already verified inline — explicitly state `**Verification:** no verification needed because checkpoint /document made no new edits — all session work was verified inline at the time of each change`. Without this block the `stop-verification-check` hook will fire on the closing-line completion language. Confirmed 2026-04-25: hook fired three times in one session on `Handover complete` despite the work being captured.
   3. **Suggested improvements** from step 16b under a clear heading — these are ideas Simon can act on, defer, or dismiss. **MUST come AFTER the Verification block, not before.** Reason: Simon evaluates suggestions against a known-clean baseline of what was actually verified, and the Suggested improvements section is the one he acts on — putting it last means the easy-pick mechanism (reply with a number) is the very last thing in the message, where his eye lands.
   4. Closing line.

   Wrong order (Simon flagged this): Suggested improvements → Verification → closing. The Suggested improvements appearing before Verification reads as if work is being recommended before the work-just-done has been confirmed clean.

   End with: **"Handover complete — you are now clear to close or compact this session."**

18. **Suggest compaction if appropriate**: If the conversation is long or context usage is high, suggest running `/compact` after the handover. The pattern is: `/document` → `/compact` → re-read vault files to restore context. Only suggest this if there's remaining work — if the session is ending, just complete the handover.

## Guidelines
- Be concise in log entries. A few lines per section, not paragraphs.
- Use the same date/topic heading format as existing entries.
- Don't duplicate — if something was already logged earlier in the session (mid-session continuous documentation), reference it rather than re-writing it. The handover catches gaps, not repeats.
- If the session was trivial (quick question, no real work done), say so and skip the logs.
- If a log file doesn't exist, create it with a brief header (e.g., `# Session Handoff Log`) before appending.
- All vault paths are relative to the vault root recorded in `~/.claude/projects/<project-key>/config.json` under `vault.path`. Don't hard-code a vault path here — derive it at runtime so the skill survives a vault rename.
- The auto-memory directory is at `~/.claude/projects/.../memory/`. MEMORY.md is the index; individual memory files live alongside it. **(SIMON-ONLY)** Simon's vault has a copy at `05_AI WORKFLOW/CLAUDE/MEMORY (auto-memory).md` symlinked to the auto-memory MEMORY.md — edits to either location propagate. Newcomer vaults don't have this symlink; skip the assumption.

## Post-run improvement

After completing the task, briefly assess skill performance:
- Did any step fail, need workaround, or produce poor results?
- Were there missing steps or unclear instructions?

If patterns emerge (not one-off issues), update this skill file with fixes. Log genuinely surprising friction to the Friction Log.
