# The agent fleet

A way to start each day with a team of specialist assistants — each one watching a different part of your work — that surface what's worth doing, then hand it to you one task at a time instead of as an overwhelming list.

*This is an advanced pattern — the kind of thing that emerges once your everyday setup is solid, not a day-one build. It's here to show the shape of where this can go; when you're ready, paste it into Claude Code and build the version that fits your domains.*

## The core idea

A single general-purpose AI assistant is a generalist — it knows a bit about everything you're doing but isn't deeply on top of any one area. The move here is to run several **agents** instead: each one is the *same* AI, but pointed at a single domain and given its own accumulated knowledge of it. ("Agent" just means the AI working in a defined role with its own notes — not a separate piece of software.)

So you might have a fundraising agent, a science agent, a communications agent, an admin agent — whatever your real domains are. Each keeps its own running picture of that domain: the active projects, what's stalled, what's coming up. Each afternoon, they look across your projects and propose what's worth doing *in their area* — including work they could do overnight.

The problem with a team of keen assistants is that they'd bury you. So one more agent sits on top: a **chief of staff**. It collects what every specialist is proposing, weighs it against each other, and hands you work **one task at a time** — not a wall of twenty suggestions. You do a thing, you come back, it gives you the next thing.

## The pieces

- **Domain agents** — one per real area of your work. Each is a role description plus its own knowledge file (what it has learned about that domain over time). Same AI, different hat and different notes.
- **The chief of staff** — the orchestrator. It reads what the specialists surface, removes duplication and noise, decides what actually matters today, and presents it to you in order.
- **A daily rhythm** — the specialists do their thinking the afternoon before: each proposes the work it could do overnight, and you approve or decline it in a short evening review. Overnight the coordinator re-ranks everything across all the areas. By the time you're up, the day's plan is already written; in the maintainer's setup you hear it on a morning walk, talk back about anything that needs your view, and your answers are folded in before you sit down and run the day's coaching command (`/today`).

## How it runs

The day starts with a plan already waiting: the specialists proposed their work the afternoon before, the night's work has run, and the coordinator has ranked what's live across every area. You react to it — on a walk, by voice, if you like — and your reactions reshape it. Because each agent keeps its own running notes, it isn't re-deriving everything from scratch each morning — it remembers what it flagged yesterday, what you deferred, and what's still in flight, so its picture of the domain sharpens over time instead of resetting daily. The chief of staff collates everything and hands you the first task with enough context to just *do* it. You finish, come back, get the next one. The list never lands on you all at once — that's the whole point.

Underneath, each agent reads and writes the same vault (see [the philosophy](./00-the-philosophy.md)) — so a specialist's "knowledge of its domain" is just notes in your files, getting richer over time, not a black box. And when a session does substantial work in one agent's area without updating that agent's notes, the closing routine notices and asks once whether to bring them up to date.

## Give the day a fixed shape

Left to itself, a coordinator with several specialists reporting in produces a long flat ranking — everything sorted, nothing distinguished. It works much better if the day has a shape the coordinator must fill:

- **A few quick wins** — around five small but genuinely forward-moving actions, each doable in about fifteen minutes from something that already exists (a draft, a one-line decision), and each one *your* action rather than a thread you're only copied into.
- **One big thing** — a single substantial block of focused work with the AI, picked on stakes and deadline, with its first concrete step named. Exactly one: the runner-up waits for another day, and if nothing qualifies the plan says so rather than promoting something small into the slot.
- **Everything else, below the fold** — remaining action items, replies owed, what's on the radar, specialist output. This tier is *reference*, not a queue. The coordinator doesn't walk you through it and only goes there if you ask.

The coordinator works through both top tiers before stopping, but it doesn't default to running them in the same order every day. Each morning it decides which single piece of work matters most — often the one big thing, sometimes a quick win that can't wait — names it, and leads with that; the other tier follows. Any ranking or scoring it does happens *within* a tier, never across them. One escape hatch keeps the shape workable: work from a lower-priority area can claim a top-tier slot when it carries a dated deadline in the next few days. Without a deadline it waits for the session that owns it.

## When the ranking starves a domain

Any fixed priority order will, over a long enough busy stretch, push one kind of work permanently to the bottom — often the work you'd choose for yourself if the urgent things ever stopped. The fix isn't to weaken the ordering; it's to add a **floor**. Keep track of when each protected area last had real work done on it, and if nothing has happened there for a few working days, the coordinator promotes exactly one item from it into that day's plan until something does. On weeks where that work happens naturally the floor never fires, so it doesn't fight the ordering — it only catches neglect.

Two details decide whether it helps or annoys. The "last done" marker has to be updated by *every* route that can do that kind of work, not just the daily coaching session — otherwise the floor announces weeks of neglect right after a week you spent doing exactly that. And it's an offer, not a mandate: skip it and it simply comes back tomorrow, with no guilt attached.

## Check that the coordinator actually did its job

A coordinator can fail quietly. If the step that ranks the day's incoming mail breaks partway — it ranks a handful and leaves the rest as unranked placeholders — nothing errors. The unranked items simply fall into a default bucket. The tell is the age profile: the "do this morning" list fills with the oldest backlog, while everything recent and live gets filed as later work.

So the morning routine reads the ranker's own status before trusting its output — how many items were genuinely ranked versus left as placeholders — rather than assuming the inputs being fresh means the ranking worked. If it's degraded, the plan says so at the top, keeps the list but marks its ordering as unreliable, rebuilds a sensible morning set from the raw sources, and lists the misfiled recent items visibly rather than silently claiming them. It also counts how many days in a row this has happened. The ranker itself gets fixed separately, not patched from inside the morning run.

The same habit applies to overnight work. A run record saying "nothing was produced" describes that one run, not the whole night — finished drafts may have landed through a different route. Before the plan declares work lost, it checks what actually exists on disk. Reporting finished drafts as missing is the costlier error: it re-plans work that's done and buries drafts nobody then reads.

## What this does *not* do

It doesn't decide *for* you — it surfaces and sequences; you choose. It isn't a fixed org chart you have to adopt: start with **one or two** agents for your busiest areas and add more only when you feel the generalist getting stretched. And it doesn't require a big system — the same "specialist with its own notes + something that hands you one thing at a time" shape works with two agents or ten.

## Note

This is a pattern, not a fixed team. Your domains are yours; the number of agents is yours; how hands-on the chief of staff is, is yours. The durable idea is: *specialists that each keep their own picture of one area, and one coordinator that hands you work one piece at a time.* Paste this to your AI and shape it to how your work is actually divided.

---

*Want the actual method? [The reference](../reference/the-agent-fleet.md) lays out the real, cleaned-up version — the concrete steps, the guardrails, the failure modes — minus the personal specifics. A starting point to adapt, not a drop-in.*
