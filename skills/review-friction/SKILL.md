---
name: review-friction
description: Walk through `[OPEN]` Friction Log entries one at a time, mark each as resolved / defer / wontfix / skip, and update the log inline. Use when the user says "/review-friction", "review my friction log", "go through the open frictions", or when `/session-start` flags overdue entries. Run weekly or whenever the open list grows beyond 5–6 items.
allowed-tools: Read, Edit, Bash
---

The Friction Log is only useful if it's read. Without periodic review, it becomes a write-only document and entries drift past their relevance window. This skill is the lightweight manual review loop — walk the open list, decide on each.

## When something goes wrong

If the Friction Log file isn't where the config says it is, or the parsing breaks, fix the skill or the config BEFORE continuing the workaround. Add the failure mode here.

## Steps

### 0. Set tab title (Ghostty only)

If `/Applications/Ghostty.app` exists, set the tab title. Otherwise skip — this is Ghostty-specific.

```bash
[ -d /Applications/Ghostty.app ] && MY_TTY=$(ps -o tty= -p $PPID 2>/dev/null | tr -d ' ') && echo "review friction" > "/tmp/claude-title-${MY_TTY}"
```

### 1. Locate the Friction Log

Read `~/.claude/projects/<vault-key>/config.json` to find the vault path and the logs folder. Friction Log is at `<vault>/<logs_relative>/Friction Log.md` (default `<vault>/AI_WORKFLOW/CLAUDE/Friction Log.md`).

If the config doesn't exist, ask the user where the Friction Log lives and offer to create the config.

### 2. Parse open entries

Read the Friction Log. Find all entries beginning with `## [OPEN]` or `## [STUCK]`. For each, capture:

- Status tag, date, title from the H2 line
- The bullet body (Symptom, Root cause, Fix planned, etc.)

Skip `[RESOLVED]` and `[WONTFIX]` entries — they're archived.

### 3. Acknowledge briefly

One short sentence: "Found N open friction entries — walking through one at a time."

If N is 0: "Friction log is clean — no `[OPEN]` or `[STUCK]` entries to review." Exit.

### 4. Walk entries one at a time

For each open entry:

1. **Restate the entry** — title, age (days since the date), status tag, and a 1–2 sentence recap of the symptom and any fix already planned. Self-contained — don't assume the user remembers it.
2. **Recommendation** — based on the entry content, which option is most likely.
3. **Numbered options:**

   ```
   1. Resolved — fix has landed, mark [RESOLVED]
   2. Wontfix — accepted as platform limitation or out-of-scope, mark [WONTFIX]
   3. Defer — not now, but revisit on a specific date (you'll be asked for the date)
   4. Stuck — needs my judgement, mark [STUCK] (auto-tagged after 3 days anyway)
   5. Skip — leave [OPEN], we'll see it again next review
   ```

4. **Wait** for the user's reply.
5. **Apply the change inline** by editing the entry's status tag and (for defer) appending a "Defer to YYYY-MM-DD" line. Use the Edit tool — preserve everything else verbatim.
6. **Brief confirmation** — one sentence — and move to the next entry.

**Kill switch:** if the user says `done`, `stop`, `enough`, or signals fatigue mid-list, exit cleanly. Skip remaining entries; close.

### 5. Close

One short summary:

```
Friction log review complete.
Resolved: N | Wontfix: M | Deferred: K | Skipped (still open): S | Stuck: T
```

Don't suggest follow-on work. Don't chain into other skills. Done.

## Self-assessment (post-run)

After close, silently note: did any entries reveal a pattern that should be promoted to a Tier 1 MEMORY rule, or to a process-doc fix? If a pattern emerges over 2–3 review passes, surface it next session.
