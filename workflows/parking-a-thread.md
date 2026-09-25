# Parking a thread

A clean way to stop working on something for a while — a week, a month — so that a future session that knows nothing about it can pick it up cold in one move.

This is an idea file. Paste it into your AI agent — Claude Code or Codex — to build a version for your own work; it'll fill in the specifics in collaboration with you. (It has to be an agent that can create files on your machine — a plain chat assistant can't set this up.)

## The core idea

[The session loop](./the-session-loop.md) handles the end of a *session*: a handoff note so tomorrow's session starts where today's ended. But real work has a second kind of stop: a *thread* you're abandoning mid-flight — a migration waiting on a reply, a manuscript on hold until the data comes in, a build you've decided is next month's problem. A handoff note is the wrong tool for that. It's session-scoped, it gets buried under a dozen later entries, and it assumes the reader remembers roughly what was going on.

What the parked thread needs is a **single living document that a stranger could resume from** — its own plan of record — plus a **reminder that will actually fire**. The maintainer calls the document a State of Play. Neither half works alone: a document without a reminder is forgotten; a reminder without a document has no context.

## The pieces

- **One document per thread, with a fixed shape.** *What this is* (three sentences); *Where we got to* (dated, most recent first — decisions and artefacts, not narrative); *What's next* (numbered, item 1 is the first thing a fresh session does); *Open questions*; *Where everything lives* (an asset → path table); and a *Pickup prompt* — a self-contained paragraph a cold session can be given verbatim: full paths, first concrete action, no jargon. Frontmatter carries a status (`active`, `paused — awaiting <condition>`, `resolved`, `promoted`), a created date, and a last-active date.
- **Park in one move.** A single command composes the pieces: save the session state as usual; write or refresh the State of Play and set it to `paused — awaiting <condition>`; create a to-do in your task app whose notes *are* the pickup prompt, with a due date if the condition has one. The parking command just calls the existing save, document and reminder routines, so a change to any of them is made in one place — the maintainer rebuilt it that way after finding the park command had grown its own copy of the document logic.
- **Resume, don't duplicate.** Before writing, look for an existing document on the topic — vault-wide, by title pattern *and* status together, because "State of Play" tends to get used for other collation notes too. A live match is resumed and re-paused in place. An archived one triggers a reopen-or-new question, never a silent edit.
- **Keep it current automatically.** When any later session touches files the document lists, a small script bumps its last-active date and appends a dated "where we got to" line. Whatever is in the document outranks the handoff log when they disagree — the doc is the thread's memory; the log is the session's.
- **Surface the paused ones.** A thread parked "awaiting the evening review" comes up at that night's review; every other paused thread is swept weekly in the system walk, where it's resumed, kept parked or closed. Close-out is explicit: *resolved* (archive it) or *promoted* (its content became a process doc; the original stays as a pointer). One check the maintainer had to add: the pickup prompt must name only still-open work — a "first action" the document itself records as done is a contradiction, and gets repaired mechanically.
- **Anchor the cluster.** A parked thread usually has satellites — a pre-read, a draft, a research note. Mark the State of Play as the hub and list those files in its frontmatter; give each satellite a one-line pointer back. That's what lets close-out machinery find every document the thread owns.

## What this does *not* do

It isn't a mid-session save (that's the checkpoint) and it isn't an end-of-session goodbye (that's the handoff); it parks *one thread* and leaves the session free for something else. It doesn't decide when to resume — the condition and the reminder do. And it deliberately refuses to spawn a second tracker: if a thread already has a plan-of-record document, new phases anchor into it. Parallel roadmaps are how threads get lost.

## Why this works

Resuming cold is the expensive moment — reconstructing what was decided, where things are and what's actually next, from a dozen scattered notes, is where abandoned work stays abandoned. Paying that cost once, at the moment of parking while everything is loaded, in a shape a stranger can read, turns "should I pick that up?" into a five-minute read and a first action. The reminder ensures the question gets asked.

## Note

This is a pattern, not a fixed toolkit. Your section names, your task app, whether the currency script exists or you bump the date by hand — all yours. The durable idea is: *a parked thread gets one living document a stranger could resume from, with a numbered next step and a verbatim pickup prompt, paired with a reminder that will fire — and never a second tracker.* Paste this to your AI and build the version that fits how you work.

---

*Want the actual method? [The reference](../reference/parking-a-thread.md) lays out the maintainer's real version — the document contract, the status vocabulary, the filing rules, the composer command — cleaned of personal specifics. A starting point to adapt, not a drop-in.*
