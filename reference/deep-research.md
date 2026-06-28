# Reference — Deep research

> **What this is.** The actual method behind [the *Deep research* workflow](../workflows/deep-research.md), cleaned of the maintainer's personal specifics (real paths, names, machine state). It's a **starting point to adapt, not a drop-in command** — your sources, your field, and your tools are shaped differently, so read it *with* your AI and build the version that fits. The narrative workflow says *why* and *when*; this says *how*, concretely enough that your agent doesn't have to reinvent the hard parts.
>
> Throughout, "your reference library" means your own curated collection of saved papers/sources (the maintainer uses Paperpile, but Zotero or any manager works the same way); "your notes" means whatever knowledge base your AI can search (a local semantic search over markdown, here QMD); "a second model" means an independent AI you can call from the command line (Semantic Scholar and the open citation databases need no account; the maintainer also wires in OpenAI's Codex CLI and Google's Gemini CLI, run read-only).

## The shape of the run

A research run is a pipeline, not a single prompt: **scope → search your own library first → gather widely → synthesise → verify → deliver**. Each stage writes its output to a working file so a long run survives interruption and the next stage reads from disk, not from a fragile chat history. Below are the parts that actually carry the weight.

## Curated library first — the load-bearing principle

Before the AI touches the open web, it searches **the sources you've already vetted** — the papers you deliberately saved, the notes you wrote. This beats web-first for a concrete reason: a generic web search returns whatever ranks, vetted or not, while your library is full text you already trust. Grounding the answer in that *first* means the report builds on what you know rather than starting from the median of the internet — and a fresh web source that contradicts your library becomes a flagged signal instead of silently overwriting it.

The non-obvious requirement: those sources have to be **searchable on your own machine**, not locked inside a cloud account. The pattern that works:

- **A local mirror of your reference manager** — the abstract and metadata of everything you've saved, each linked to its source.
- **A full-text sidecar for papers you've read deeply** — the extracted body text of a paper, pulled in alongside its metadata as a searchable file. This layer grows on its own, one paper at a time, as a by-product of the work; it's never a big up-front job.
- **A coverage gate.** Count the *distinct* relevant sources the library search surfaces. Above a threshold (the maintainer uses ~6), treat the topic as well-covered by your own material and run the broad web pass as an independent quality check rather than the primary source. Below it, the few hits still go in — labelled as a curated subset — and the web carries more of the load. One caution: relevance scores often saturate near the top, so judge coverage by *count of distinct sources that survive a relevance read*, not by raw score.

## Decompose so it doesn't time out

A broad topic researched as one giant prompt either times out or returns mush. Split it:

- **Restate the question back first** — the last cheap moment to steer. A vague question in gets a vague report out.
- **Break it into a handful of sharper sub-questions**, each a thread the AI can chase independently. For a genuinely large topic, go one level further: write a short **plan note** naming the chapters, run **one research unit per chapter** (each its own scoped pass with its own gather-and-verify), then a final **synthesis pass** that stitches the chapters together. Chaptering is what keeps a big topic inside the limits — each unit is small enough to finish, and the plan note is the through-line that stops the chapters from drifting apart.

## Gather widely — and, where you can, with a second model

Run several searches in parallel, one per sub-question, **fetching and reading the promising results** rather than skimming snippets. Two habits make the gather trustworthy:

- **Tie every claim to its source** as it's recorded — no free-floating assertions. A short structured "claim → source" registry per thread is the source of truth that synthesis reads from later.
- **Let an independent model take its own pass** where you have one available on the command line, run **read-only** so it can't change anything. Two architecturally different models catch each other's blind spots; where they agree it's a useful cue (not proof). If no second model is available, the run still works — it leans harder on the citation-database checks below, and says so plainly. It never pretends a second pass happened.

## Cite everything, flag what you couldn't verify

This is the answer to "how do I know it isn't making things up," and it runs on two tracks:

- **Claims against sources.** The handful of claims that carry the conclusion get checked back against what the cited source actually says — does the page exist, does it really support the point? Anything that can't be stood up is marked, not smoothed over.
- **References against the scholarly record.** Every academic reference is checked against the open citation databases — Semantic Scholar, CrossRef, OpenAlex — and comes back *found*, *found-but-author-or-year-is-off*, or *not found*. Not-found means **possibly fabricated**: flag it for a human, never auto-delete and never silently keep. (The most common failure is a real finding wearing an invented author name, so author- and species/subject-level attribution needs checking, not just "does a paper by roughly this name exist.")

Build the reference check **once as its own small reusable step** the research run calls — you'll want it in other places too.

## Synthesise honestly

Pull everything into one report, attributing claims at the level of the **individual finding, not the paragraph**. Where sources disagree, show *both* positions and their evidence instead of silently picking a winner. Give consequential claims a confidence note — well-corroborated, single-source, or uncertain — so a reader sees how much weight each one bears. And **write for the audience, not the audit trail**: if someone other than you reads this, strip the internal scaffolding (model attributions, "as the earlier briefing said") and make it a standalone document. Model agreement is a triangulation cue, not extra evidence — if two models assert the same thing, look at the underlying source rather than counting the agreement as confidence.

## Deliver where it lasts

Save the finished report — citations, flagged uncertainties, verification notes and all — **into your notes**, not into a chat window that scrolls away. There it compounds with everything else you know, and a follow-up reminder to act on it keeps it from rotting. Because the whole run can go unattended, it pairs naturally with an overnight queue: ask the question at night, read the report in the morning.

## What stays yours

Which sources you trust enough to gather from first; whether you wire in one second model or two (or none, and lean on the database checks); how deep you let it dig; how many chapters a big topic earns; and what the finished report looks like — all adapt to your setup. The transferable spine is just: *search your own vetted library before the open web; split a broad topic into chapters so it finishes; tie every claim to a source and verify the ones that matter against real databases; flag what you couldn't confirm instead of dropping or keeping it silently; and write the result down where it lasts.*
