# The agent fleet

A way to start each day with a team of specialist assistants — each one watching a different part of your work — that surface what's worth doing, then hand it to you one task at a time instead of as an overwhelming list.

*This is an advanced pattern — the kind of thing that emerges once your everyday setup is solid, not a day-one build. It's here to show the shape of where this can go; when you're ready, paste it into Claude Code and build the version that fits your domains.*

## The core idea

A single general-purpose AI assistant is a generalist — it knows a bit about everything you're doing but isn't deeply on top of any one area. The move here is to run several **agents** instead: each one is the *same* AI, but pointed at a single domain and given its own accumulated knowledge of it. ("Agent" just means the AI working in a defined role with its own notes — not a separate piece of software.)

So you might have a fundraising agent, a science agent, a communications agent, an admin agent — whatever your real domains are. Each keeps its own running picture of that domain: the active projects, what's stalled, what's coming up. Each morning, they look across your projects and surface what's worth your attention *in their area*.

The problem with a team of keen assistants is that they'd bury you. So one more agent sits on top: a **chief of staff**. It collects what every specialist is proposing, weighs it against each other, and hands you work **one task at a time** — not a wall of twenty suggestions. You do a thing, you come back, it gives you the next thing.

## The pieces

- **Domain agents** — one per real area of your work. Each is a role description plus its own knowledge file (what it has learned about that domain over time). Same AI, different hat and different notes.
- **The chief of staff** — the orchestrator. It reads what the specialists surface, removes duplication and noise, decides what actually matters today, and presents it to you in order.
- **A daily trigger** — the thing you run in the morning that sets the fan-out going. In the maintainer's setup this is a command (`/today`) kicked off after a morning walk and a quick voice note about what's on your mind, so the agents plan around your actual head-space that day.

## How it runs

You start the day by saying what's on your mind (typed, or spoken and pasted in). The trigger fans the work out to the specialist agents; each reviews its domain and proposes. Because each agent keeps its own running notes, it isn't re-deriving everything from scratch each morning — it remembers what it flagged yesterday, what you deferred, and what's still in flight, so its picture of the domain sharpens over time instead of resetting daily. The chief of staff collates everything and hands you the first task with enough context to just *do* it. You finish, come back, get the next one. The list never lands on you all at once — that's the whole point.

Underneath, each agent reads and writes the same vault (see [the philosophy](./00-the-philosophy.md)) — so a specialist's "knowledge of its domain" is just notes in your files, getting richer over time, not a black box.

## What this does *not* do

It doesn't decide *for* you — it surfaces and sequences; you choose. It isn't a fixed org chart you have to adopt: start with **one or two** agents for your busiest areas and add more only when you feel the generalist getting stretched. And it doesn't require a big system — the same "specialist with its own notes + something that hands you one thing at a time" shape works with two agents or ten.

## Note

This is a pattern, not a fixed team. Your domains are yours; the number of agents is yours; how hands-on the chief of staff is, is yours. The durable idea is: *specialists that each keep their own picture of one area, and one coordinator that hands you work one piece at a time.* Paste this to your AI and shape it to how your work is actually divided.

---

*Want the actual method? [The reference](../reference/the-agent-fleet.md) lays out the real, cleaned-up version — the concrete steps, the guardrails, the failure modes — minus the personal specifics. A starting point to adapt, not a drop-in.*
