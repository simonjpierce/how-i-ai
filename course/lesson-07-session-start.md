# Lesson 7 — `/session-start`

The first thing you run at the start of every Claude Code session. About thirty seconds of work for an enormous amount of "where was I, what's open, what should I do next" clarity.

> **Video** *(placeholder):* `<https://loom.com/...>` — me opening a fresh session and running `/session-start`; what it reports and how I use the report.

## What it does

Reads recent context — the last few session handover notes, your friction log, your decision log, current daily note — and gives you a short briefing. Surfaces stale `[OPEN]` items, flags overdue threads, tells you what was happening last time you sat down.

## When to use it

- First thing each time you open Claude Code, before you ask it to do any real work.
- When context feels stale: *"wait, what was I doing in this project again?"*
- After a few days away: *"catch me up."*

## Try it

```
/session-start
```

Read the report. If anything in the friction log is overdue, that's a hint that `/review-friction` should be your next move. If a session-handover entry mentions a thread that hasn't progressed, that's a hint of what to work on today.

## What's next

[Lesson 8 — `/document`](./lesson-08-document.md). The bookend of `/session-start` — the wrap-up handover that the *next* session's `/session-start` will read.
