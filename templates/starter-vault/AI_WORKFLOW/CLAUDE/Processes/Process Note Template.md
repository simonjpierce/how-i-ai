# Process Note Template

> **Delete this template when adding your first real process doc**, or copy it as a starting point. Process docs live alongside this file in `AI_WORKFLOW/CLAUDE/Processes/`.

A *process doc* is a written record of how you (or you and Claude) handle a recurring kind of work. It's lighter than a skill — no slash command, no auto-discovery — but heavier than a one-line memory entry. Process docs answer "what's the right way to do X around here?" so the answer doesn't get lost between sessions.

When a process doc has been used 3+ times and the steps are stable, it's a candidate for promotion to a skill in `~/.claude/skills/`. The doc stays as the human-readable reference; the skill becomes the executable form.

---

## Standard shape

Copy this scaffold for new process docs. Trim ruthlessly — most process docs should fit on one screen.

```markdown
# <Process name>

<One-sentence purpose: what this process produces and for whom.>

## Status

<Active / Draft / Paused>. Optional: link to spec or supersession history.

## Trigger

When does this run?
- A specific event (e.g. "after every meeting where action items were captured")
- A schedule (e.g. "weekly, Sunday morning")
- A user phrase (e.g. "when the user says 'wrap this up'")

## Steps

1. <First step — what Claude or the user does, with enough specificity that it's reproducible. Cite file paths in `code formatting` so they're greppable later.>
2. <Second step.>
3. <Third step.>

## Failure modes

What goes wrong, and what to do about it. Capture each one as it happens — don't try to predict them all up front.

- **<Symptom>:** <Why it happens. What to do.>

## Post-run improvement

What to check after running this process:
- Did any step fail or need a workaround? If yes, update the relevant step here BEFORE next run.
- Did the output match expectations? If not, where's the gap?

If a pattern emerges over 2–3 runs, promote the fix into the steps above instead of leaving it in the post-run notes.
```

---

## Tips

- **Lead with the trigger.** A process doc with no clear trigger is just notes — it never fires.
- **Append, don't rewrite.** When you learn something new, add to the failure-modes section. Don't restructure the doc unless the structure is genuinely broken.
- **One process per file.** If two related workflows are tangled together, split them — they'll evolve at different speeds.
- **Cite file paths.** When a step touches a specific file, write the path in backticks. Future-you (and future-Claude) will grep for it.

---

*This template is a starter. Replace it with your first real process doc, or delete it once you have a few real ones in this folder.*
