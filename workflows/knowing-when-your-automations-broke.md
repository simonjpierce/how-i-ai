# Knowing when your automations broke

Once you have jobs running on their own — overnight, hourly, on a schedule — the failure that hurts isn't the one that crashes loudly. It's the one that reports success for ten weeks while quietly doing nothing. This is how to make sure you find out.

This is an idea file. Paste it into your AI agent — Claude Code or Codex — to build a version for your own work; it'll fill in the specifics in collaboration with you. (It has to be an agent that can create files on your machine — a plain chat assistant can't set this up.)

## The core idea

A scheduled job on your own machine has no one watching it. If it fails, the operating system writes a line to a log you will never open. If it half-works — commits most files but silently skips the large one, runs but writes to the wrong place, starts and hangs — it may not even fail. The maintainer runs about thirty of these and learnt each of the following the expensive way: a backup that reported success nightly while a key file had been silently excluded for ten weeks; a crash-loop hidden among "known broken" items nobody looked at; a log that captured 4 of 312 errors because each new session overwrote the archive.

The fix is not more monitoring dashboards. It is three plain habits: **every job writes one line to one shared page** when it has something to say; **the AI reads that page first thing** when you open a session, and separates *new* problems from *known* ones; and **each health check tests the outcome**, not whether the job ran.

## The pieces

- **One intake page, five sections.** A single note in your vault — the maintainer calls it the Daily Log — that every automation appends to through one shared helper, never by hand-editing. Five fixed sections: *Decisions needed* (only you can resolve it), *For review* (an output landed, glance at it), *Alerts* (something failed), *Auto-fixed* (the system repaired something and is telling you), *Completed*. Each line carries a category tag, a creation date the helper stamps automatically, and where possible the path of the thing it's about — so a later pass can check whether the underlying item is resolved and age the line out.
- **The AI reads it before you do.** At session start a fast hook (under two seconds, filesystem checks only) prints a pre-flight: which scheduled jobs exited with an error since last time, which expected outputs are missing or stale, which symlinks are broken, whether the memory file is near its cap. Silent when healthy.
- **New versus known.** The pre-flight's one clever bit: it cross-references each failure against your open friction entries. A failure that matches an *open* entry prints second, dimmed, as "known, deferred". Anything unmatched — or unmatchable — prints first under "requires investigation", and a non-empty block there makes triage the session's first job. Safe by default: an item is demoted to "known" only on a positive match; unknowns stay loud. The origin failure was a 30-second crash loop hidden for days among broken symlinks everyone had learnt to ignore.
- **Test the outcome, not the run.** The backup check that said "ran today" was worthless; the check that says "a success line exists *and* today's copy exists in the second tier *and* no file was excluded by the size guard" is what caught the ten-week gap. Each health check names the specific evidence a real success leaves behind and looks for that. Tolerate transient blips (a travel-WiFi failure that self-heals tomorrow) by alerting on the third consecutive miss, not the first.
- **Alerts that clear themselves.** An alert line is keyed so the same failure doesn't append a duplicate every day, and it resolves automatically on the next successful run. You see a problem once, and you see it disappear.
- **A weekly deep check.** Sunday or Monday, one slower script validates the whole substrate: every scheduled job is loaded and its script exists, every hook file it points to is present, credentials haven't expired, the search index is healthy, disk usage of the things that grow. Writes a report only on failure and raises a task in your to-do app; silent otherwise.
- **Guard the shared log itself.** Anything many sessions write concurrently needs an atomic append and a lock. The 4-of-312 error-log failure was a race: session A read the archive, session B appended, A wrote its copy back over B's. A lock directory (`mkdir` is the portable atomic test-and-set on macOS) with stale-lock reclaim fixed it.

## What this does *not* do

It doesn't fix anything on its own beyond the narrow auto-restores (a zero-byte file restored from git, a stale alert cleared). It's a detection layer: its job is to make sure a broken job is in front of the AI, classified, at the start of your next session, so triage is a decision rather than an archaeology exercise. It also doesn't replace testing the job before you schedule it — a health check tells you it broke, not that it was ever right.

## Why this works

Failures on an unattended machine are invisible by default, and "it ran" is the wrong signal — the dangerous jobs are the ones that run fine and do the wrong thing. Routing everything into one page the AI reads first turns dozens of log files nobody opens into a single triage the session can't skip; and separating new from known is what stops the page becoming wallpaper you scroll past, which is how the crash loop hid.

## Note

This is a pattern, not a fixed toolkit. How many sections your intake page has, what counts as "stale", whether the deep check runs weekly or monthly — all yours. The durable idea is: *every automation reports to one page the AI reads at session start, new problems are kept visually apart from known ones, and every health check looks for the evidence a real success leaves behind rather than the fact that the job ran.* Paste this to your AI and build the version that fits how you work.

---

*Want the actual method? [The reference](../reference/knowing-when-your-automations-broke.md) lays out the maintainer's real version — the intake-page contract, the pre-flight check, the outcome-based health checks, the failure modes — cleaned of personal specifics. A starting point to adapt, not a drop-in.*
