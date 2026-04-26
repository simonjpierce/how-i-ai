---
name: session-start
description: Session orientation. Reads recent context, checks open threads, and presents a brief summary before work begins. Run at the start of each session, when context seems stale, or when the user says "orient me", "catch me up", "what was I working on", or "where did we leave off".
allowed-tools: Read, Write, Glob, Grep, Bash
---

Orient for the current session. Read recent context and present a brief summary so Simon can confirm orientation happened.


## When something goes wrong

When a step in this skill fails or needs a workaround, update this skill file with what you learned BEFORE continuing to the next step. Add failure modes, correct wrong assumptions, fix timing estimates. This takes 30 seconds and prevents the same friction next time.


## Steps

0. **Set tab title** — silently set the Ghostty tab title to reflect the session task (or "session start" if no task yet):
   ```bash
   MY_TTY=$(ps -o tty= -p $PPID 2>/dev/null | tr -d ' ') && echo "session start" > "/tmp/claude-title-${MY_TTY}"
   ```
   Update this later when the task becomes clear.

1. **Read Current Projects** — read `01_LIFE OS/Current Projects.md` for current priorities, what Simon is focused on, and what he's avoiding. This is the most important orientation context.

2. **Note MEMORY.md context** — MEMORY.md is auto-loaded into the conversation. Scan the loaded content for feedback entries, infrastructure details, and references relevant to the current task. Don't re-read the file unless you need a section that was truncated.

3. **Read the most recent 2–3 entries** in `05_AI WORKFLOW/CLAUDE/Session Handoff Log.md`. Read from the top of the file (newest entries are prepended). Stop after the third `---` separator.

4. **Scan for relevant context** — if the user has already stated what they want to work on, check:
   - The Decision Log for prior decisions on the same topic
   - The Friction Log for known issues in the same area
   - Process docs in `05_AI WORKFLOW/CLAUDE/Processes/` if a relevant workflow exists
   - Skip this step if the user hasn't stated a task yet.

5. **Check automation health** — use Bash to verify key automations are producing output:
   - **Weekly review:** Run: `ls -lt "01_LIFE OS/REVIEW QUEUE/Weekly Reviews/" | head -3` (from the vault directory). If the most recent file is >10 days old, flag: "Weekly review automation may not be running — latest output is [date]."
   - **Nightly workhorse:** Run: `ls -lt "01_LIFE OS/REVIEW QUEUE/NIGHTLY WORKHORSE/" | head -3`. If the most recent file is >3 days old, flag it.
   - **Self-improvement loop:** Run: `ls -lt "01_LIFE OS/REVIEW QUEUE/IMPROVEMENTS/" | head -3`. Check recency as a signal the loop is running.
   - If all checks pass, skip silently.
   - This prevents the "documentation-reality gap" — automations documented but not actually running.

   **If the cadence check triggers a review pass**, here's what to do (propose to Simon, don't execute silently):
   - Check for path drift: are vault paths in process docs and scripts still correct?
   - Check for stale assumptions: do process docs match current behaviour?
   - Check for duplicate or conflicting instructions across files.
   - Verify key automations produced recent output (backups, reviews, aggregation).
   - Update `Last reviewed` dates on docs that were checked.

6. **Cross-session review (weekly)** — check whether a review has been done in the last 7 days:
   - Use Bash: `ls -t "05_AI WORKFLOW/CLAUDE/Session Reviews/"*.md 2>/dev/null | head -1` (from the vault directory).
   - If a review exists from the last 7 days, read it and note any proposed improvements to surface in the summary.
   - If no review exists (or the directory is empty/missing), run one now:
     1. Read: Session Handoff Log (last 5 entries), Friction Log (last 10 entries), Decision Log (last 10 entries), MEMORY.md (full file).
     2. Analyse for: recurring friction patterns, stale MEMORY.md threads, up to 3 proposed improvements (what to change, why, exact file path), and signs of automation/documentation drift.
     3. Write the review to `05_AI WORKFLOW/CLAUDE/Session Reviews/YYYY-MM-DD.md` with YAML frontmatter (`type: session-review`, `date`, `generated-by: session-start (inline)`).
     4. Keep the review under 100 lines. Use NZ/UK English.
   - This replaces a planned LaunchAgent automation — runs inline to avoid separate API billing.

7. **Present an orientation summary** — output a brief block (max 10 lines) covering:
   - What the last session worked on and its status
   - Any open threads that are stale (>2 weeks) or relevant to today
   - Any prior decisions or known friction relevant to the stated task
   - Any self-review cadence flag from step 5 (if triggered)
   - Any proposed improvements from the cross-session review (step 6) — keep to 1–2 lines, e.g. "Weekly review flagged: [improvement]. Apply this session?"
   - End with: "Ready to start." or a specific question if something needs clarification.

## Guidelines
- Keep the summary concise. This is a quick orientation, not a report.
- **Don't rediscover what's already documented.** Infrastructure details live in MEMORY.md and `Processes/Scheduled Automations.md`. Check those before exploring.
- If MEMORY.md or the handoff log don't exist or are empty, say so — that itself is useful information.
- The only file this skill writes is the cross-session review note (step 6). All other steps are read-only.
- All vault paths are relative to: `$VAULT_PATH`

## Post-run improvement

After completing the task, briefly assess skill performance:
- Did any step fail, need workaround, or produce poor results?
- Were there missing steps or unclear instructions?

If patterns emerge (not one-off issues), update this skill file with fixes. Log genuinely surprising friction to the Friction Log.
