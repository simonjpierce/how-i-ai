---
name: session-start
description: Session orientation. Reads recent context, surfaces stale friction, checks open threads, and presents a brief summary before work begins. Run at the start of each session, when context seems stale, or when the user says "orient me", "catch me up", "what was I working on", or "where did we leave off".
allowed-tools: Read, Write, Glob, Grep, Bash
---

Orient for the current session. Read recent context, surface anything that needs the user's attention, and present a brief summary so the user can confirm orientation happened.


## When something goes wrong

When a step in this skill fails or needs a workaround, update this skill file with what you learned BEFORE continuing to the next step. Add failure modes, correct wrong assumptions, fix timing estimates. This takes 30 seconds and prevents the same friction next time.


## Steps

0. **Set tab title (Ghostty only)** — if `/Applications/Ghostty.app` exists, silently set the Ghostty tab title to reflect the session task (or "session start" if no task yet). Otherwise skip — this is a Ghostty-specific affordance and writing the temp file is wasted I/O on terminals that don't watch for it:
   ```bash
   [ -d /Applications/Ghostty.app ] && MY_TTY=$(ps -o tty= -p $PPID 2>/dev/null | tr -d ' ') && echo "session start" > "/tmp/claude-title-${MY_TTY}"
   ```
   Update this later when the task becomes clear.

1. **Locate the logs folder.** Prefer `<vault>/AI_WORKFLOW/CLAUDE/` (starter convention). Fall back to `<vault>/05_AI WORKFLOW/CLAUDE/` (Simon's vault numbering). The first one that exists is the logs folder — reuse this path for steps 4–5. If neither exists, this isn't a CLAUDE-managed vault — skip steps 4–5 silently and just orient on Current Projects + MEMORY.md.

2. **Read Current Projects** if it exists — try `01_LIFE OS/Current Projects.md` first, then `Current Projects.md` at the vault root. This is the most important orientation context. Skip silently if neither exists (the starter vault doesn't ship one).

3. **Note MEMORY.md context** — MEMORY.md is auto-loaded into the conversation. Scan the loaded content for feedback entries, infrastructure details, and references relevant to the current task. Don't re-read the file unless you need a section that was truncated.

4. **Read the most recent 2–3 entries** in `<logs>/Session Handoff Log.md`. Read from the top of the file (newest entries are prepended). Stop after the third `---` separator. Skip any entry preceded by `<!-- EXAMPLE ENTRY -->` (the starter template ships with one — it's not a real handoff). Skip silently if the file doesn't exist, has no real entries, or only the example entry remains.

5. **Surface stale friction** — read `<logs>/Friction Log.md`. Find all `## [OPEN]` and `## [STUCK]` entries; from each H2 line, extract the first date matching the regex `[0-9]{4}-[0-9]{2}-[0-9]{2}` (the format Friction Log entries use; tolerates whatever delimiter comes after — colon, em-dash, etc.). For any entry whose date is more than 7 days ago, capture the title and age in days. Skip `[DEFERRED]`, `[RESOLVED]`, and `[WONTFIX]` entries entirely — `[DEFERRED]` entries have a `**Defer to:** YYYY-MM-DD` line in the body and the user re-tags them `[OPEN]` themselves when they want to revisit.
   - If 1+ stale entries exist, list them numbered in the orientation summary and offer: "These haven't been reviewed in N+ days. Run `/review-friction` to walk through them?"
   - If an entry's H2 line has no parseable date, skip it with a one-line warning to the user (don't halt the skill — the friction log shouldn't be a blocker).
   - If 0 stale entries, skip silently.
   - If the file doesn't exist or has no `[OPEN]`/`[STUCK]` entries, skip silently.

6. **Scan for task-relevant context** — if the user has already stated what they want to work on, check:
   - The Decision Log for prior decisions on the same topic
   - The Friction Log for known issues in the same area
   - Process docs in `<logs>/Processes/` if a relevant workflow exists
   - Skip this step if the user hasn't stated a task yet.

7. **Check automation health (optional)** — run each check ONLY if its directory exists. Skip silently if the directory is missing — that means the user doesn't run that automation, not that something's broken.
   - **Weekly review:** `ls -lt "01_LIFE OS/REVIEW QUEUE/Weekly Reviews/" | head -3` — flag if newest file >10 days old.
   - **Nightly workhorse:** `ls -lt "01_LIFE OS/REVIEW QUEUE/NIGHTLY WORKHORSE/" | head -3` — flag if newest file >3 days old.
   - **Self-improvement loop:** `ls -lt "01_LIFE OS/REVIEW QUEUE/IMPROVEMENTS/" | head -3` — flag if newest file >3 days old.
   - These are vault-specific automations. Absence of the directory means the user doesn't run them; absence is silent, not an error.

8. **Present an orientation summary** — output a brief block (max 10 lines) covering:
   - What the last session worked on and its status
   - Any stale friction entries from step 5 — numbered, with a "/review-friction?" prompt
   - Any prior decisions or known friction relevant to the stated task
   - Any automation-health flag from step 7 (if triggered)
   - End with: "Ready to start." or a specific question if something needs clarification.

## Guidelines
- Keep the summary concise. This is a quick orientation, not a report.
- **Don't rediscover what's already documented.** Infrastructure details live in MEMORY.md and process docs. Check those before exploring.
- If MEMORY.md or the handoff log don't exist or are empty, say so — that itself is useful information.
- This skill is read-only — no files are written.

## Post-run improvement

After completing the task, briefly assess skill performance:
- Did any step fail, need workaround, or produce poor results?
- Were there missing steps or unclear instructions?

If patterns emerge (not one-off issues), update this skill file with fixes. Log genuinely surprising friction to the Friction Log.
