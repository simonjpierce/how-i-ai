# Reference — Parking a thread

> **What this is.** The actual method behind [the *Parking a thread* workflow](../workflows/parking-a-thread.md), cleaned of the maintainer's personal specifics. A **starting point to adapt, not a drop-in.** The maintainer's task app is Things 3; any app with a notes field and a due date works, and a plain `TODO.md` is the fallback.

## The document contract

Filename: `<Topic> — State of Play.md`. No date in the name — the topic is the stable identifier.

Frontmatter:

```yaml
---
title: <Topic> — State of Play
date: <created — preserved across updates>
last-active: <most recent touch>
status: active — in progress | paused — awaiting <condition> | active reference — <what> | resolved | promoted — <process doc>
hub: true                    # set false at close-out
related-files:
  - <vault-relative path, with extension, exact case>
purpose: Pickup notes + collation for the <topic> thread. Resume-from-cold reference.
---
```

Body, required sections in order:

1. `## What this is` — 1–3 sentences: the topic, why it matters, high-level state.
2. `## Where we got to` — dated entries, most recent first; decisions and artefacts, not narrative.
3. `## What's next` — numbered; item 1 is the first action a fresh session takes.
4. `## Open questions` — pending decisions or research, with an owner each where relevant.
5. `## Where everything lives` — asset → path table.
6. `## Pickup prompt` — a self-contained prompt for a cold session: full paths, first concrete action, no jargon. **Must name only still-open work.** A staleness check compares the prompt's first action against the `Where we got to` entries and flags a contradiction for mechanical repair.

Optional sections below those.

## Status vocabulary and who reads what

| `status:` | Meaning | Surfaced by |
|---|---|---|
| `active — in progress` | being worked in the live stream; the initial state | nothing (you're on it); the currency script may write to it |
| `paused — awaiting <condition>` | parked | weekly system walk; the evening review only when the condition *is* that review |
| `active reference — <what>` | a living collation doc, not a task tracker | nothing; outside this lifecycle |
| `resolved` | done; terminal | archived at close-out |
| `promoted — <doc>` | content moved to a process doc; original kept as a pointer; terminal | — |

Keep this vocabulary separate from any spec-status vocabulary you use; merging them was tried and confused both.

## Filing

- Domain-specific thread → the relevant domain folder.
- Cross-cutting or homeless → a `PAUSED THREADS/` folder in your review-queue area.
- **Never** into the stable process-docs folder (that's for promotion at close-out only) and never into the spec backlog.
- Close-out: *archive* mirrors the source subfolder under your archive root; *promote* creates or reshapes the process doc.

## The composer command

`/do-this-later [topic]` — a thin composer of owners that already exist:

1. **Scope.** Take the topic from the argument or infer the thread being parked (not the whole session). Confirm in one line only if ambiguous.
2. **Discover.** Vault-wide search for an existing State of Play on the topic, matching title pattern *and* frontmatter status together. Live match → resume-and-re-pause in place. Archived or terminal match → numbered reopen-vs-new question. None → new doc. Use one shared index script for this; never a hand-rolled find.
3. **Sync.** Run the mid-session save on the related docs (flagged so its own checkpoint phase doesn't run twice).
4. **Write.** Hand to the State of Play owner command: create or refresh the doc, set `status: paused — awaiting <condition>`.
5. **Remind.** Create the to-do with the `## Pickup prompt` in its notes, due date from the condition where it has one.
6. **Checkpoint.** Flush handoff and logs; scoped commit.

Redundancy the maintainer removed: the park command once carried its own document-writing logic (284 lines); now 109 lines composing three owners. If two commands both know the document's shape, they drift.

## Automatic currency

A script run by the save and close-out commands checks the session's edit set against every live State of Play's `related-files:`. On overlap: bump `last-active:`, append a dated one-liner under `Where we got to`. This is why the doc outranks the handoff log — it's kept current without anyone remembering to.

## Failure modes seen

- **Title overload.** "State of Play" gets used for non-paused collation docs; match on status too.
- **Duplicate reminders on resume-and-re-pause.** Most task apps can't update a to-do from a script; a second park creates a second reminder. Say so in the confirmation so the old one can be deleted.
- **Ambiguous topic in a multi-threaded session.** Ask with numbered candidates; don't guess.
- **Intent was end-of-session, not park.** Route to the goodbye command instead.
- **Doc already current.** If `last-active` is today and the canonical sections still hold, skip the rewrite — don't churn a file to bump a date.
- **Task app unavailable.** Fall back to a vault `TODO.md`; surface the failure; the doc is the primary recovery artefact so don't abort.

## What stays yours

Section names, folder layout, task app, whether the currency script exists. The transferable spine: *one living doc per thread with a numbered next step and a verbatim pickup prompt; a reminder that fires; resume in place rather than duplicating; explicit close-out to archive or promote.*
