# Reference — The overnight workhorse

> **What this is.** The actual method behind [the *Overnight workhorse* workflow](../workflows/the-overnight-workhorse.md), cleaned of the maintainer's personal specifics (real paths, names, machine state). It's a **starting point to adapt, not a drop-in command** — your queue, your runner, and your evening habit are shaped differently, so read it *with* your AI and build the version that fits. The narrative workflow says *why* and *when*; this says *how*, concretely enough that your agent doesn't have to reinvent the hard parts.
>
> Throughout, the **worker** is one autonomous AI session that picks up a single task and runs it with no human watching; the **queue** is a plain text file of tasks waiting for tonight; "your skills directory" means wherever your AI keeps its reusable commands.

## The shape of it

Three moments, kept separate:

- **Evening** — you decide what's worth running unattended and write it into the queue.
- **Overnight** — a runner works through the queue task by task, then stops when it's empty (it does **not** invent its own work).
- **Morning** — you review the drafts as starting points, keep what's good, redirect what isn't.

The hard-won part is none of those three — it's **scoping**: the rules that decide what can safely run while no one's there to answer a question. Get the scoping right and the rest is plumbing.

## The queue entry (write for a worker with no context)

The worker never saw your conversation. It has only the queue entry and whatever's already in your files, so the entry has to brief someone who has never seen the task before. Every entry carries:

- **Source** — exactly where the inputs are (full paths, folder IDs, file counts). Not "the report" — *the* file.
- **Output** — where results go, with a naming convention and an example filename.
- **Method** — step-by-step instructions, specific to the point of naming the exact tool calls and parameters, not just "look it up."
- **Done means** — the quality bar and what to verify once it's written.

**Specificity is the whole game.** A vague entry produces vague autonomous work, and you only find out in the morning when it's too late to clarify. Before queuing, actually confirm the worker can *reach* the inputs — list the folder, check the files exist, spot-check one URL — rather than assuming. Your AI can help you draft the entry; have it read the inputs back to you so gaps surface at the desk, not at 2am.

## The scope limit (the heart of it)

A single task has to be small enough to **finish in a bounded time** — think roughly ten minutes of agent work, with headroom under whatever idle-timeout your runner enforces. This is the rule everything else hangs off, because an over-scoped task fails in a particular, demoralising way: it doesn't error, it **degrades** — running low on room, the worker stops doing the real work and starts re-emitting its own input as if that were the deliverable. You wake up to a file that looks finished and contains nothing. So when an entry implies more than that bounded slice of work, you don't queue it — you split it.

Two split patterns cover almost everything:

- **One section per task for anything multi-section.** A report with named sections (summary, highlights, finances, risks…), a proposal with parts — each section is its own entry with its own worker. Never bundle several into one task; bundled sections are the classic over-scope.
- **Read-then-write for heavy synthesis.** When a task has to digest more than a handful of source files before writing, split it in two: a **gather** task that reads everything and produces a plain outline (no prose), then a **draft** task that writes from *that outline only* and never re-opens the originals. Name them so the pairing is obvious. This keeps each half inside the time bound and stops the worker drowning in sources.

## What NOT to send

Some work simply isn't a fit for an unattended worker, and queuing it anyway burns the night — it crash-loops, times out, or hands you noise. Route these to a supervised, interactive path instead:

- **Anything needing a live login.** If the task has to reach a logged-in mail, drive, or browser-gated service, the headless worker doesn't have that session and can't get one at 2am.
- **Anything that edits the AI's own configuration.** Changes to your skills directory or the assistant's own settings are gated behind interactive approval by design — a worker can't (and shouldn't) self-modify unattended.
- **Cohesive code builds that need a real test gate.** A change that has to land green across one codebase fails the model two ways: split across parallel workers they collide on the same file; run as one big task it over-scopes — and you can't trust an unwatched worker's word that the tests actually passed. Hand coding to a supervised path where a human (or a separate review pass) holds the gate.

The through-line: if completing the task needs *judgement or a credential as it happens*, it belongs in your day, not the queue.

## What stays yours

How you trigger the run, where the queue file lives, how much you let it do unattended, the exact time bound, whether you split by section or by read-then-write — all adapt to your setup. The transferable spine is just: *queue only work that's well-scoped and needs no one watching; keep each task small enough to finish clean; split what's too big; and keep login-gated, self-modifying, and gate-needing work on a supervised path.*
