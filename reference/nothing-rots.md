# Reference — Nothing rots

> **What this is.** The actual method behind [the *Nothing rots* workflow](../workflows/nothing-rots.md), cleaned of the maintainer's personal specifics. A **starting point to adapt, not a drop-in** — your surfaces (to-do app, review commands, queues) differ; the contract is what transfers.

## The taxonomy

**A loop** is anything that survives past the turn or session that created it and expects a later action:

| Type | Example |
|---|---|
| Outstanding human action | "you'll need to approve X"; an unsent draft |
| Deferred or queued build | specced-not-built; "worth building later" |
| Pending decision | an unanswered open-decisions block |
| Waiting on an external party | a collaborator's reply; a grant result |
| Parked thread | "park this / pick it up later" |
| A verify-later flag created *this* session | one whose resolution is expected, not merely possible |
| Any first-person "I'll do X later" in the AI's own output | |

**Not a loop** (the detector must not flag these): completed work; items *explicitly dropped* ("decided not to"); options mentioned but never adopted as intent; recurring work already owned by a scheduled job; pre-existing verify-later flags across the vault.

## The contract

Every loop names three elements, inline, in the same turn:

1. **Owner** — you, a named agent, the overnight worker, or an external party *with a named chaser*.
2. **Surface** — a specific *existing* place (routing table below). Never a new one.
3. **Trigger / cadence** — next evening review; Saturday system walk; a dated to-do; the nightly queue; "when X replies + 7-day chase check".

Form: *"parked the migration → resurfaces at the next evening review (owner: you)."* Not a loop: *"no open loop — [reason]"* or *"standing flag — [reason]."*

One carve-out worth copying: **a gap in an observer is not a deferrable loop.** If you build a tracker, ledger or detector that doesn't yet capture the real events, or captures them but reaches no action, that gap may not be parked under this rule — it's an incomplete build and gets finished or explicitly scoped out in the same run. Otherwise "the observer half is done" becomes a permanent state.

## The routing table

| Loop type | Owner | Surface | Trigger |
|---|---|---|---|
| Human action, undated | you | the owning agent's backlog / top-10 | daily or evening review walk |
| Human action, dated | you | to-do app, via the to-do command | due date |
| Build changing the AI's skills, hooks or scripts | unattended second-model worker where its permissions allow; otherwise you + AI | queue entry with declared targets, or an INTERACTIVE item for restricted files (settings, credentials, memory) | nightly run; evening or weekly review for restricted work |
| Other deferred build | overnight worker | queue entry / spec status | nightly run; weekly backstop |
| Pending decision | you | ask *now*; else a pending-decisions note | this turn, else the evening review |
| Waiting on external | external + chaser | a "waiting" line in the agent backlog or a dated to-do | chase date — only with evidence they're stuck |
| Parked thread | you + AI | State of Play doc | evening review if parked for it; otherwise the weekly walk |
| Verify-later flag created this session | per content | the note itself + a line in the close-out | next session on that topic, or "standing flag" |

Deviations allowed; must be stated.

## Decision-log revisits

Each decision entry that might age carries `**Revisit by:** YYYY-MM-DD`. The weekly system walk:

1. Finds entries whose date is past. Cap the walk (the maintainer uses 5) so it doesn't flood.
2. Pre-assesses each from evidence before asking: mechanism still in force? superseded by a later entry? measurement available? Writes a one-line verdict under the entry (`**Revisited:** <date> — <finding>`).
3. Asks only where the verdict needs a human: extend (with a reason and a new date), close, or reverse.

The maintainer's log holds ~900 revisit dates; the walk is what makes them real.

## The enforcement layers

Prose names the *right* owner and surface — no hook can supply that. Code ensures *some* path was named:

- **L1 — Stop hook.** Reads the model's final message each turn. A first-person deferral (`I'll … later`, `worth picking up`, `parked`) with no owner/surface/trigger pattern nearby → block once with "name the resurfacing path". Every deferral seen, pathless or not, is appended to a per-session JSONL ledger (`open-loop-ledger.jsonl`: timestamp, session, excerpt, path-named yes/no). Known limit: it sees only each turn's *final* message; a deferral stated mid-turn and never repeated is invisible to it.
- **L2 — close-out.** The session-end command reads the session's ledger rows and merges them into its "what's next" disposition walk, so a mid-session deferral reaches the gate even if memory missed it. It also reconciles *named* against *routed*: a claimed "queued" is checked against the real queue entry.
- **L3 — weekly backstop.** A script gathers ledger rows still pathless after 48 hours and surfaces each as one obligation in the weekly system walk.
- **L4 — the convention doc.** This table, in your process docs, is what L1–L3 point to.

Subagents don't see the convention; a parent that dispatches one forwards the one-line rule in the prompt.

## Friction as a loop

A friction log with tagged headers: `## [OPEN] date — title`, `[STUCK]`, `[RESOLVED]`, `[DEFERRED]`, `[WONTFIX]`. A periodic walk command steps through `[OPEN]` entries one at a time and rewrites the tag in place. The session-start pre-flight (see [Knowing when your automations broke](./knowing-when-your-automations-broke.md)) uses the same tags to demote known failures. One log, two readers.

## What stays yours

Your surfaces, cadences and caps; whether you build the hook layers at all. The transferable spine: *owner + surface + trigger, inline, at the moment of deferral; route to a place you already look; date every decision and walk the dates; let code check that a path was named and prose decide which.*
