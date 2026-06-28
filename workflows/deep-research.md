# Deep research

Point the AI at a real question and walk away — it reads widely across the open web *and* your own trusted sources, checks the claims it makes against those sources, verifies every reference against the scholarly record, and hands you a cited report instead of a chat thread you have to babysit.

This is an idea file. Paste it into Claude Code to build a version for your own work; it'll fill in the specifics (which sources, which models, where the report lands) in collaboration with you. (It has to be an agent that can create files on your machine — a plain chat assistant can't set this up.)

*What you'll need: the "search your own sources first" step works best with a searchable local mirror of your reference manager — a small one-time setup your AI can walk you through, and you can start without it and add it later. A second AI model adds breadth but is optional; with only one model the workflow still runs web-first and leans harder on the reference-database checks (which need no account — those databases are open).*

## The core idea

There's a difference between *asking* an AI a question and *commissioning* research. Asking gets you a confident paragraph that might be right, with no way to tell — and AI models, asked to cite their sources, will sometimes invent a real-looking paper that does not exist. Commissioning means the AI goes out, reads many sources, weighs what it finds, flags where the evidence is thin or sources disagree, and hands you a written report with citations you can actually follow back.

This workflow builds the second kind. You give it a question worth a few hours of digging. It gathers from your own curated library *first* — your saved papers, your notes, the material you already trust — then widens to the open web. It cross-checks the claims that matter rather than asserting them. It writes the findings up as a document that lands in your notes, where it becomes part of what you know instead of vanishing into a chat window.

Two habits make it trustworthy, and they're the whole point:

- **Breadth.** Don't lean on one source, and don't lean on one AI. Gather across many sources, and — when you can — let a *second, independent* AI model take its own pass, so the two catch each other's blind spots.
- **Verification.** The claims that carry weight get checked against real sources; every reference gets checked against the scholarly record; and anything that can't be confirmed is flagged as such — never quietly kept.

## How it runs

You frame the question as precisely as you can — a vague question gets a vague report. Then the AI works through roughly these stages, writing as it goes:

**Scope and decompose.** It restates the question back to you to make sure it has the right one, then breaks it into a handful of sharper sub-questions — each a thread it can chase independently. This is the last cheap moment to steer; a few minutes here saves a report aimed at the wrong target.

**Search your own sources first.** Before touching the open web, it searches the material you already trust — your notes, your saved papers, your reference library. The non-obvious requirement here is that those sources have to be *searchable on your own machine*, not locked inside a cloud account: the maintainer keeps a local mirror of his reference manager (Paperpile, though Zotero or any manager works the same way) — the abstracts and metadata of everything he's saved, each linked to its PDF, plus the full extracted text of any paper he's read deeply pulled in alongside as a searchable sidecar — so the AI can search across the whole library (abstracts always, full text where it's been read) and open or read the underlying paper when a hit is worth a closer look. That full-text layer grows on its own, paper by paper, as a by-product of the work rather than a big up-front job. ([The reference library](./the-reference-library.md) is how you build that mirror.) That grounding is what makes the report *yours* and not a generic web summary — it builds on what you already know, and can flag where a fresh web source contradicts it.

**Gather widely — and, ideally, with more than one model.** It runs several searches in parallel, one per sub-question, fetching and reading the promising results rather than skimming snippets. Every claim it records is tied to the source it came from — no free-floating assertions. Where a second AI is available on the command line (the Codex CLI or the Gemini CLI work well, run **read-only** so they can't change anything), that model researches the same question in parallel; the two often surface complementary findings, and where they agree it's a useful signal — not proof, but a cue worth more checking.

**Synthesise honestly.** It pulls everything into one report, attributing claims at the level of the individual finding, not the paragraph. Where sources disagree it shows *both* positions and their evidence instead of silently picking a winner. Consequential claims carry a confidence note — well-corroborated, single-source, or uncertain — so you can see how much weight each one bears.

**Verify — the load-bearing part.** This is the answer to "how do I know it isn't making things up," and it runs on two tracks:

- *Claims against sources.* The handful of claims that matter most are checked back against what the sources actually say — does the cited page exist, and does it really support the point? Anything that can't be stood up is marked, not smoothed over.
- *References against the scholarly record.* Every academic reference is checked against the public citation databases — Semantic Scholar, CrossRef, and OpenAlex — and comes back as *found*, *found-but-the-author-or-year-is-off*, or *not found*. Not-found means **possibly fabricated**: it's flagged for your eye, never auto-deleted and never silently retained. (This is [citation verification](./citation-verification.md), built once as its own small reusable step that the research workflow calls — you'll want it in other places too.)
- *(Optional) A second model on the synthesis.* Where you have that independent read-only model available, it can also cross-check the finished synthesis — catching an overstated conclusion or a claim the first model leaned on too hard. If no second model is available, the report says so plainly; it never pretends a review happened.

**Deliver.** The finished report — with its citations, its flagged uncertainties, and its verification notes — is saved into your notes so it compounds with everything else you know, rather than scrolling out of a chat.

Because it can run unattended for a stretch, this pairs naturally with [the overnight workhorse](./the-overnight-workhorse.md): queue a research question at night, read the report in the morning.

## What this does *not* do

It doesn't replace your judgement about what's true. It gathers, cross-checks, and flags — but the calls on a thin-evidence finding, a source disagreement, or a reference it couldn't confirm are yours to make, and you should read most critically exactly where it tells you the ground is soft. It won't quietly resolve a conflict, delete a citation it couldn't verify, or pretend an independent review happened when it didn't. It's not for quick lookups — that's just asking. And it's only ever as good as the question: precise scope in, useful report out.

## Why this works

Self-review is weak — a model that just wrote a claim is the worst-placed to doubt it. Checking claims back against their sources, verifying references against an independent database, and (where you have one) a *second* model reading the work catch what self-review structurally can't. And the bookkeeping that trustworthy research actually depends on — tying every finding to a source, surfacing disagreements instead of papering over them, never letting an unconfirmed reference slip through — is exactly the tedious work a person skips under time pressure and regrets later. The AI doesn't get bored doing it. The report stays trustworthy because keeping it trustworthy is nearly free.

## Note

This is a pattern, not a fixed pipeline. The parts that are yours to shape: which sources you trust enough to gather from first; whether you wire in a second AI model for breadth and an independent read of the synthesis, or run it with one model and lean harder on the database checks; how deep you let it dig; and what the finished report looks like. It assumes an agent that can search your notes and write files; if your trusted sources include published literature, the reference-check against Semantic Scholar / CrossRef / OpenAlex is the piece most worth not skipping. The durable idea is: *gather widely, verify what matters against real sources, flag what you can't confirm, and write it down where it lasts.* Paste this to your AI and build the version that fits your field.

---

*Want the actual method? [The reference](../reference/deep-research.md) lays out the real, cleaned-up version — the concrete steps, the guardrails, the failure modes — minus the personal specifics. A starting point to adapt, not a drop-in.*
