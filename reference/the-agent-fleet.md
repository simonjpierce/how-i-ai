# Reference — The agent fleet

> **What this is.** The actual method behind [the *agent fleet* workflow](../workflows/the-agent-fleet.md), cleaned of the maintainer's personal specifics (real domains beyond a few examples, file paths, names, machine state). It's a **starting point to adapt, not a drop-in command** — your work divides up differently, so read it *with* your AI and build the version that fits. The narrative workflow says *why* and *when*; this says *how*, concretely enough that your agent doesn't have to reinvent the hard parts.
>
> Throughout, an **"agent"** is just the same AI pointed at one area of your work and given its own notes — not a separate program. An agent's **"state"** is those notes: a few plain files it reads at the start of every run and writes back to over time.

## Why specialised-and-stateful beats one generalist

One general assistant knows a little about everything and isn't deeply on top of any one thing. A fleet splits the work so each agent owns a single area — fundraising, communications, science, admin, whatever your real areas are — and, crucially, **each keeps its own memory of that area**. That memory is the whole point: an agent that has watched its domain for weeks remembers what's stalled, what you deferred, what corrections you've already made, so it sharpens instead of resetting to zero each morning. A generalist re-derives all of that from scratch every time.

The cost is coordination — a roomful of keen specialists would bury you. So one extra agent sits on top as an **orchestrator** that collates, de-duplicates, and hands you work one piece at a time.

## What an agent actually is — its files

Give each agent a small, fixed set of notes in its own folder. The maintainer's set, generalised:

- **An identity / ownership file** — read first. It states the agent's goal, which areas and files it owns, its sibling agents, and (for anything that writes external-facing prose) which voice guide to use. This is the agent's "you are this expert" brief.
- **A current-priorities list** — its live, capped set of active items. Read in full each run.
- **A corrections log** — the durable, learned judgement: facts you fixed, approaches you rejected, scope calls ("that's the other agent's job"). This is what makes the agent feel like it *knows* the domain.
- **A domain-knowledge file** — accumulated context, paged rather than dumped if it grows large.
- **A candidate backlog** — raw items waiting to be triaged into priorities.
- **In-flight state** — per-item progress for work that spans sessions.

The load rule is **bounded**: read the identity, priorities, and corrections in full (they're small and load-bearing); skim or page the big knowledge and backlog files. Don't pull the entire domain into context every run.

## How an agent is invoked — three shapes

Summoning an agent means *the AI reads that agent's files and acts as it* for the rest of the exchange. Parse what you asked for into one of three shapes:

- **Enter the domain (bare).** No task given → the agent loads its state and shows you its current priorities and anything in flight, then asks what to work on. A standing "bring me up to speed on X" door.
- **Hand it a task.** A clear instruction ("draft the funder update", "review this") → the agent does that work using its own notes as the substrate, in its own voice, one step at a time.
- **File a document into it.** An ingest verb plus a document ("add this contract to the fundraising agent") → the agent classifies the material — is it an action, background context, a raw idea? — and **proposes** where to file it, writing only on your OK.

A useful refinement: let the same summons work *without* a special command — an ordinary sentence that names the agent ("use the science agent to outline the methods") routes the same way. But a passing **mention** ("that's really a science question") is not a summons; when intent is unclear, confirm in one line before acting.

## The orchestrator — for whole-system work

The top agent isn't a domain expert; it's the coordinator. Summon it for the cross-cutting jobs no single specialist owns: "what's the state of everything?", a sweep for work that's fallen through the cracks, deciding which agent an ambiguous item belongs to, reconciling the overall plan. Its standing rule is **delegate, don't hoard** — when a task is squarely one domain's, it hands it to that domain agent rather than doing it itself. Its job is that nothing is orphaned: every live work-item has a responsible agent, and it's the catch-all owner of last resort.

## The line the agents don't cross

The agents **propose and sequence; you decide.** They surface what's worth doing and prepare the work — but the guardrails are non-negotiable and inherited by every agent:

- **Drafts only for anything that leaves your hands.** External messages (donors, funders, collaborators, anyone outside your team) are written to a file for you to review and send yourself. The AI never sends them.
- **No invented specifics.** Figures, quotes, dates, names that aren't sourced get flagged for verification, never fabricated.
- **One thing at a time.** The fleet's reason to exist is to *prevent* the wall of twenty suggestions — so the output is always the single highest-leverage item, then the next.
- **Corrections feed back.** When you correct an agent mid-session, that correction is captured into its corrections log so the same mistake doesn't recur — the mechanism by which the agent's judgement actually improves.

## What stays yours

Your domains, the number of agents, which notes each one keeps, how hands-on the orchestrator is — all adapt to how your work is actually divided. Start with **one or two** agents for your busiest areas and add more only when you feel the generalist getting stretched; the same shape works with two agents or ten. The transferable spine is just: *specialists that each keep their own growing picture of one area, one coordinator that hands you work a piece at a time, and a firm line that they propose while you decide.*
