# Reference — Knowing when your automations broke

> **What this is.** The actual method behind [the *Knowing when your automations broke* workflow](../workflows/knowing-when-your-automations-broke.md), cleaned of the maintainer's personal specifics. A **starting point to adapt, not a drop-in.** The maintainer's scheduler is macOS `launchd` (LaunchAgents); the same shapes apply to cron, systemd timers, or the desktop app's scheduled routines.

## The intake page

One note (`Daily Log.md`), single persistent file — not date-rotated — with five H2 sections in fixed order: `Decisions needed`, `For review`, `Alerts`, `Auto-fixed`, `Completed`.

**Line contract**, enforced by a shared helper every writer imports (no automation edits the file directly):

```
- [ ] **[Category]** description [created: YYYY-MM-DD] [source: path/to/thing.md]
```

- The `[created:]` stamp is appended by the helper, never by the caller. It is what the ageing pass keys on, so a date mentioned *inside* the description isn't mistaken for the entry's own date. The helper escapes any literal `[created:` a caller puts in prose.
- `[source:]` is optional but recommended: the lifecycle pass checks whether the source file still exists or has changed status to decide an entry is resolved.
- Alerts are **dedupe-keyed** (the helper takes a key; the same key updates in place rather than appending) and a job that succeeds calls the resolve function for its key, so the alert disappears on its own.

**Lifecycle** (nightly): checked `For review` / `Alerts` older than 30 days are archived verbatim to a dated shard; `Completed` is pruned; stray sections are folded back into the five. Nothing is deleted, only moved, with a byte-count check.

Who reads it: the AI. Your daily briefing skill (see [the daily coach](./the-daily-coach.md)) consumes `Decisions needed` and `For review`; the session-start pre-flight consumes `Alerts`; you read the briefing, not the log.

## The session-start pre-flight

A `SessionStart` hook calls `lib/preflight-check.sh`. Constraints: filesystem-only, under two seconds, silent when healthy. Checks:

- **Scheduled jobs**: for each registered job, the last exit status from the scheduler (`launchctl list` shows it; `launchctl print` gives more), the age of its `.out`/`.err` log, and — where the job has an expected output file — whether that output is fresher than the last scheduled run.
- **Symlinks** under the config directory resolve to non-empty targets (cloud-synced folders can silently replace a file with an empty one).
- **Credentials** with a known lifetime: warn at an age threshold.
- **Open items**: undecided high-priority proposals older than N days.

**Triage tiering** — the part worth copying. Two output blocks:

```
⚠️ Pre-flight — REQUIRES INVESTIGATION:
  - LaunchAgent `<name>` failed (exit 1)
Pre-flight — known open (deferred; cross-referenced to Friction Log):
  - LaunchAgent `<other>` failed — [OPEN] 2026-08-14
```

An issue is demoted to "known" only if its key (the job label, the symlink name) appears *inside an entry whose header is `[OPEN]` or `[STUCK]`* in the friction log — an entry-aware scan, so a mention inside a `[RESOLVED]` entry does not count. Anything unclassifiable (no key, log missing, parse error) stays in the loud block. Safe direction: a real failure must never hide among accepted noise.

Suppress the whole pre-flight for machine-spawned sessions (an environment variable the runner sets): a batch job doesn't need orientation, and the handoff text was once treated as the task by a spawned agent.

## Outcome-based health checks

Each check names the evidence a real success leaves. Examples from the maintainer's set:

- **Backup ran** → wrong. **Backup succeeded**: the log contains an explicit success line for today (the last line can be a "push failed" warning), *and* the second tier (cloud copy) produced today's file, *and* the pre-commit size guard did not unstage anything — that guard "warns to a log nobody reads" and had excluded the same large file every night for ten weeks while every run reported success. Alert on the third consecutive miss (travel blips self-heal).
- **Skill files intact**: every skill path resolves to a non-empty file; a zero-byte file is restored from git automatically and the restore is logged as `Auto-fixed`.
- **Weekly infrastructure check** (Monday): every registered job's plist loads and its script exists; every hook referenced in `settings.json` exists and is executable; MCP servers respond; credential files present; cloud sync not stuck; search index healthy and under a size ceiling (the maintainer's grew to 15GB, 85% dead data). Writes a vault report only on failure and creates a to-do; silent otherwise.
- **Run-log hygiene**: every job logs to its own `.out`/`.err` pair with the date in each line, and a wrapper appends a one-line result to the intake page only when there's something to say.

## Concurrency on shared files

Many sessions and jobs append to the same few files. Two rules:

- **Atomic replace, always**: write to a temp file, `fsync`, `os.replace`. Never open the target for writing before you've finished reading it (the classic `open(p,'w').write(open(p).read()…)` truncates first and saves an empty file).
- **Lock the read-modify-write**: a private lock directory; `mkdir` as the atomic test-and-set where `flock` isn't available; reclaim locks older than ~60s so a killed process can't wedge it; failing to take the lock is a clean no-op that the next run retries. Add an optimistic check — hash the bytes read under the lock, re-hash immediately before the replace, abort on mismatch rather than silently overwrite the other writer.

The failure this prevents: the session error archive captured 4 of 312 failures across a week because each session start rotated it with a plain `mv`, and later because two starts raced the append. Both fixes were mechanical; the *symptom* looked like "the writer hooks don't work" and cost a long investigation before anyone checked the archive step.

## What stays yours

Your scheduler, how many sections the page has, the staleness thresholds, which checks run daily versus weekly. The transferable spine: *one intake page every job writes to through one helper; a fast pre-flight the AI reads first, with new failures kept apart from known ones; health checks that look for the evidence of success rather than the fact of running; and locks on anything many writers share.*
