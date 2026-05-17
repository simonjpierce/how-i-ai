# Self-Improvement Changelog

Append-only log of system improvements made — by Claude (auto-fix gate in `/document`), by you during `/review-friction` walks, or by hand when you fix something mid-session and want to record it.

Why this file exists: without a closing mechanism, the Friction Log becomes write-only — entries accumulate, nothing acts on them, the system stays broken in the same ways. This changelog is the receipt for *what got better*, so the loop closes visibly.

## Format

```
## YYYY-MM-DD
- **Friction:** *<entry title>* — <what was done>. Source: `<file:line>` if applicable.
- **Improvement:** <what changed and why> if it didn't come from a friction entry.
```

Newest entries at the top.

## What writes here

- **`/document`'s autonomous-fix gate** (Step 16c): silently appends one line per mechanical friction fix it applies at session end.
- **`/review-friction`** when you resolve an entry: appends a line for each resolved item.
- **You** when you fix something mid-session and want it recorded.

Read this when you want to remember what's improved over time, or when you want a sense of whether the system is converging or churning.

---

## Example entry (replace below with real ones)

## 2026-05-17
- **Friction:** *Stale path reference in /transcribe* — auto-fixed in /document. Updated `~/bin/transcribe.sh:42` from `/old/path` to `/new/path`. Source: `~/.claude/skills/transcribe/SKILL.md:42`.
