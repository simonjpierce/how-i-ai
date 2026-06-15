# The reference library

Keep the literature you rely on *inside* your own system — mirrored into your vault as searchable notes — so your AI reaches for *your* curated library before the open web, and so a reference base you've built up doesn't quietly rot the moment you stop maintaining it.

This is an idea file. Paste it into Claude Code to build a version for your own work; it'll fill in the specifics (which reference manager, where the notes land) in collaboration with you. (It has to be an agent that can run tools and create files on your machine.)

*What you'll need: a reference manager you already curate (Paperpile, Zotero, Mendeley — any of them), and a one-time setup where your AI mirrors its library into your vault. The full-text and citation-checking pieces lean on a couple of external tools your AI can install for you; you can start with just the abstracts and add the rest later.*

## The core idea

When you ask an AI a research question, where does it look? Left to itself, the open web — which means it's working from whatever it can find, not from the literature *you've* already vetted. The fix is to give it your library as a first-class, on-machine source: a mirror of your reference manager, sitting in your vault as one searchable note per paper, that it searches *before* it reaches for the web.

That mirror also answers a second, slower problem: reference material decays. A chapter or a bibliography written three years ago is missing three years of literature, and buying the next edition just resets the clock. If your reference documents live as notes in the vault instead, they become *living* documents — read in their original form, but extensible: new papers get integrated as they appear, disagreements surfaced rather than smoothed, every added citation verified.

The thread tying both together is **curation**. You decide what enters — a paper earns its place in your library because you chose to save it. That selectivity is the quality gate; the AI's job is to work from what you've curated, not to go discover literature on its own (which is how low-quality or irrelevant sources creep in). Your judgement about what's worth keeping is the most valuable thing in the system, and this keeps it load-bearing.

## How it runs

**Mirror your reference manager into the vault.** Export your library and have your AI turn it into one markdown note per paper — title, authors, year, abstract, a link to the PDF — in a folder your search tools can reach. Make the import *additive*: re-running it adds only genuinely new papers and leaves everything already there untouched, so a refresh after you've saved a new batch is cheap and safe, never a destructive rebuild. Now your AI can search across your whole curated library by meaning, not just by what you remember saving.

**Pull in full text on demand — don't extract everything up front.** The note holds the abstract; that's enough to *find* a paper. When a paper actually gets read deeply — during research, a manuscript, an enrichment pass — extract its full text once into a sidecar file next to the note, and keep it. You're turning extraction you'd pay for anyway into a permanent, searchable artefact instead of a throwaway. Over time a full-text corpus of exactly the papers you actually use builds itself, with no speculative bulk job and no vault bloat.

**Verify citations as they come in.** A reference library is only as trustworthy as its metadata, and AI-adjacent workflows are exactly where a fabricated or mangled citation slips through. Check new additions against the public scholarly databases — Semantic Scholar, CrossRef, OpenAlex — at import time, on the new batch only, and flag mismatches for your eye rather than trusting them. (This is the same reusable [citation verification](./citation-verification.md) check the [writing](./writing-and-review.md) and [science](./the-science-workflow.md) workflows lean on.)

**Keep reference documents alive.** For longer-form reference material — your own book chapters, a teaching reference, a working bibliography — convert each to a vault note carrying its original text, then enrich it over time: as relevant new papers arrive in your library, integrate them one paper at a time into the right section, in cautious attributed language, with conflicts [surfaced rather than smoothed](./surfacing-conflicts.md) and every new citation verified. The document stays current instead of freezing at publication.

## What this does *not* do

It doesn't go *find* literature for you — that's deliberate. The library is what you've curated; the AI works from it rather than trawling the web and dragging in noise you'd have filtered out. It doesn't replace your reference manager — that stays where you read and organise; the vault mirror is the *searchable, AI-readable* copy alongside it. And it won't silently fix a bad citation or paper over a contradiction between two sources — it flags, and you decide.

## Why this works

The most valuable thing in a research library isn't the papers — it's the fact that *you chose them*. Pointing your AI at that curated set first, rather than the open web, is what makes its research yours and not generic. Mirroring it on your own machine makes it searchable by an agent; pulling full text in as you read makes that search deepen exactly where you work; verifying citations at the door keeps the whole thing honest. And because reference notes are just files, they keep growing — a library that compounds instead of one that decays.

## Note

This is a pattern, not a fixed toolchain. The parts that are yours to shape: which reference manager you mirror, how the notes are structured, whether you bother with full-text sidecars or live on abstracts, and how much living-document enrichment you do. The curation principle is the load-bearing one — *your AI works from the literature you've vetted, not from whatever the web turns up.* Paste this to your AI and build the version that fits how you keep your literature.
