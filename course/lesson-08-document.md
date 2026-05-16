# Lesson 8 — `/document`

The skill that makes tomorrow's session start with context instead of confusion.

The lesson reads on its own. A short screencast — me running `/document` at the end of a real session, what gets written and where — will pair with it when recorded.

## What it does

Summarises the current session — what was done, what decisions were made, what's still open — and writes a structured entry to the session handover log in your vault. Optionally captures lessons learned and updates relevant logs (decision log, friction log).

The next `/session-start` will read that entry first.

## When to use it

- End of a working session, before you close the window.
- When the conversation has gotten long enough that a fresh context would be useful.
- When you say *"wrap up", "save progress", "checkpoint"* — `/document` is what those phrases mean.
- Before `/compact` — the handover is a safer way to summarise than letting Claude compact mid-thought.

## Try it

```
/document
```

Claude proposes a summary, decisions, and open threads. Review it, edit if anything's off, accept. Done.

If the session involved decisions worth remembering ("we decided to switch from X to Y because Z"), the skill prompts you to add them to the decision log.

## What's next

[Lesson 10 — `/update`](./lesson-10-update.md). After a substantial piece of work, sweep the related project notes and docs so they reflect what just happened.

If `/document` surfaced tasks you want to capture, the optional `/todo` skill (see the [graduation page](./graduation.md)) routes them to Things 3 / Todoist / Apple Reminders if you use one of those. It's a personal-workflow skill, not part of the core course.
