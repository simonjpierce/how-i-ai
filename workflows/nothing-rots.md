# Nothing rots

A rule for every "I'll pick that up later": it names who will act, where it will reappear, and when — or it isn't a deferral, it's a loss. This is how a system with hundreds of moving parts stops quietly dropping things.

This is an idea file. Paste it into your AI agent — Claude Code or Codex — to build a version for your own work; it'll fill in the specifics in collaboration with you. (It has to be an agent that can create files on your machine — a plain chat assistant can't set this up.)

## The core idea

Working with an AI generates deferrals at a rate no human workflow ever did. Every session ends with a "What's next". Every review produces "worth doing later". Every decision has a "revisit this in a month". The AI writes them all down, faithfully — and then nothing reads them. A note in a handoff log that no future session happens to open is not a plan; it's a polite way of forgetting.

The maintainer's rule, stated once and then built into the system: **every open loop names three things — an owner, a surface, and a trigger.** Owner: who or what acts (you, a named agent, the overnight worker, an external party with a named chaser). Surface: the *existing* place it will show up — an agent's backlog, your to-do app, a dated decision entry, a queue. Trigger: when — the next evening review, next Saturday's system walk, a due date, "when they reply, plus a seven-day chase check". Lacking any one of the three is the defect. And a deferral that can't be given all three should be dropped explicitly instead, because *dropping is a disposition and forgetting is not.*

## The pieces

- **Say it inline, in the same breath.** The habit the AI carries: any time it defers something, the same sentence names the path — *"parked the migration → resurfaces at the next evening review (owner: you)."* If it isn't actually a loop, say so with a reason: *"no open loop — this was an option, not an intent."* The distinction between a stated intent and a mentioned possibility is the one that matters; only intents are loops.
- **A routing table, not a new inbox.** Each kind of loop has a default home that already exists: a dated action for you → the to-do app with a due date; an undated one → the owning agent's backlog, walked at the daily review; a deferred build → the overnight queue; a pending decision → ask now, or a pending-decisions note the evening review walks; waiting on someone → a "waiting" line with a chase date (and no chase without evidence they're actually stuck); a parked thread → a State of Play doc (see [Parking a thread](./parking-a-thread.md)). Deviations are allowed but must be said out loud. The rule is *add no new surfaces* — a new place to look is a new place to forget.
- **Decisions carry a revisit date.** Every entry in the decision log that might age gets `Revisit by: <date>`. A weekly walk finds the ones past due, pre-assesses each (still right / superseded / needs your call) and either extends the date with a reason or closes it. A decision that's never revisited is just the first thing someone thought of.
- **Code catches the ones the habit misses.** Three layers under the prose rule. A stop-time hook reads the AI's final message each turn for a first-person deferral with no path and blocks once, asking for one — and logs every deferral it sees to a ledger. The close-out command merges that ledger into its "what's next" walk, so a mid-session deferral reaches the end of the session even if nobody remembered it. And a weekly sweep finds any ledger entry still pathless after 48 hours and surfaces it as its own item. The prose names the *right* owner and surface; the hooks make sure *some* path was named.
- **Friction is a loop too.** When something goes wrong and can't be fixed on the spot, it's logged with an `[OPEN]` tag. A periodic walk goes through the open entries one at a time — resolved, deferred with a date, won't fix, or skip — and the session-start pre-flight uses the same tags to tell new failures from known ones.

## What this does *not* do

It doesn't make the loops close themselves. It guarantees they *come back* to a moment where you or the AI decide; the deciding is still work. It also isn't a to-do system for everything — pre-existing verify-later flags scattered across your notes, recurring work already owned by a scheduled job, and ideas floated but never adopted are all deliberately out of scope, because sweeping them would bury the signal. And it can't see a deferral the AI made mid-turn and never repeated; that falls back on the close-out habit, which is why both layers exist.

## Why this works

The cost of a deferral is paid when it's forgotten, not when it's made — so the moment to attach the path is the moment of deferral, while the context is loaded and the sentence is being written anyway. Naming an existing surface rather than a new one means the loop rides a review that was going to happen regardless. And making the AI carry the rule, backed by a hook, means it applies on the two-hundredth deferral of the week exactly as it did on the first.

## Note

This is a pattern, not a fixed pipeline. Your surfaces, your cadences, whether you build the hook layers or just adopt the sentence — all yours. The durable idea is: *a deferral without an owner, a surface and a trigger is a loss dressed as a plan; name all three inline, route to a place you already look, and let a periodic walk enforce the dates.* Paste this to your AI and build the version that fits how you work.

---

*Want the actual method? [The reference](../reference/nothing-rots.md) lays out the maintainer's real version — the loop taxonomy, the routing table, the revisit-date walk, the hook layers — cleaned of personal specifics. A starting point to adapt, not a drop-in.*
