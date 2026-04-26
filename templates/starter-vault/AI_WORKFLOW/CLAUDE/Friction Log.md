# Friction Log

Things that are harder than they should be. The point is to surface recurring annoyances so the system can be improved — write-only friction logs don't help anyone.

**Status tags:**

- `[OPEN]` — unresolved, needs review
- `[STUCK]` — no autonomous path forward; needs your judgement
- `[RESOLVED]` — fixed, kept here for searchable lessons
- `[WONTFIX]` — accepted as a platform limitation or out-of-scope

New entries default to `[OPEN]`.

**The review loop:** run `/review-friction` weekly (or whenever `/session-start` flags stale `[OPEN]` entries) to walk through the open list and update statuses. Without review, this file becomes write-only and loses meaning fast.

## Format

```
## [STATUS] YYYY-MM-DD: One-line title

- **Symptom:** What went wrong, observably. What you noticed.
- **Root cause:** Why it happened, once understood.
- **Why this matters:** (optional) The cost of leaving it unfixed.
- **Fix applied:** (or "Fix planned: ...") What was done about it.
- **Lesson:** The takeaway for future sessions — the rule or pattern that
  prevents the same trap next time.
```

---

<!-- EXAMPLE ENTRY — delete when adding your first real one -->

## [RESOLVED] 1970-01-01: Claude kept asking permission for every file edit

- **Symptom:** During the first hour of using Claude Code, every file edit and bash command surfaced a permission prompt. Made the system feel laborious rather than helpful.
- **Root cause:** Claude Code was running in default permission mode. The starter setup assumes auto-approval mode; without it, the proactive-skill-invocation pattern breaks down (every offered action requires two clicks instead of one).
- **Fix applied:** Switched Claude Code to auto-approval mode in settings. Friction disappeared immediately.
- **Lesson:** The permission mode is a load-bearing assumption of this whole system. If the system feels laborious in the first day, check this *first* before reorganising files or skills.
