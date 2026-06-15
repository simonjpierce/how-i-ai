# The intake loop

Get the steady firehose of incoming material — papers, saved articles, voice notes, a passing thought — *into* your vault and filed where you'll find it again, instead of scattered across a reading app, a downloads folder, and your own memory.

This is an idea file. Paste it into Claude Code to build a version for your own work; it'll fill in the specifics (which apps, where things land) in collaboration with you. (It has to be an agent that can create files on your machine — a plain chat assistant can't set this up.)

*What you'll need: nothing special to start — the simplest version is just a quick-capture habit and somewhere for things to land. The richer pieces (pulling in saved reading automatically, transcribing voice notes) lean on tools the other workflows already set up; add them as you feel the need.*

## The core idea

A research life runs on a constant inflow: the paper a colleague sends, the article you saved to read later, the half-formed idea on a walk, the PDF you'll need next month, the thing you must remember to do. Most of it lands somewhere that isn't your system — a reading app, an inbox, a notes pile, your head — and "somewhere that isn't your system" is where things go to be forgotten. The cost isn't just lost items; it's that your vault, the thing your AI reads from, is missing exactly the material that would make it useful, and your specialist workflows have a thinner substrate to work on than they should.

The fix is to treat **capture and routing as a first-class loop**: a low-friction way to get *anything* in, and a reliable way for it to end up in the right place. The discipline has two halves that matter equally — **capture has to be nearly effortless** (any friction and you won't do it in the moment, and the moment is when it's cheap), and **routing has to be reliable** (captured-but-misfiled is barely better than lost). Get both right and the vault stays current as a by-product of normal life, rather than through a filing session you never quite get to.

## How it runs

The loop has a few intake channels, all ending the same way — material, in the vault, where it belongs.

**Quick capture — for thoughts and to-dos.** A single, frictionless way to throw something into the system the instant it occurs: a one-line note, an idea, a task. It lands in an inbox, and later — or automatically — gets *routed* to where it belongs: a task to your task manager, an idea to wherever ideas live, a note to the relevant project. The rule is capture first, sort later; making capture cost a decision ("where does this go?") is what kills it. Let it land somewhere dumb and route it afterwards.

**Spoken capture — for thinking out loud.** The fastest input of all is talking. A voice note on a walk, a thought into your phone, becomes a written, filed input rather than a recording you'll never replay — [transcription](./transcription.md) is the channel that handles this, and a morning voice note is a natural way to feed the day's planning. Treat it as part of intake, not a separate thing: it's the same loop, with speech as the source.

**Reading and reference — for the literature and the web.** Two streams worth keeping current. Papers you save go into your [reference library](./the-reference-library.md), the curated literature your AI searches first. Articles, posts, and pages you save to read later get pulled in and filed too — the difference being that *you curate the literature deliberately* (it's the quality gate), while general reading can flow in more loosely and be triaged down. The key discipline is the same one that runs through the whole system: the AI files what *you chose to save*; it doesn't go trawling the web dragging in noise you'd have filtered out.

**Documents — for the PDFs and the rest.** A paper, a report, a scanned letter becomes [clean markdown in the vault](./pdf-to-markdown.md), so its content is searchable and quotable rather than locked in a file you have to open to read.

**Let it run while you sleep.** Once the channels exist, most of the filing wants no supervision — it's the kind of low-judgement bookkeeping that's perfect for [overnight automation](./the-overnight-workhorse.md). New material that came in during the day gets pulled in and filed overnight, so by morning the vault is current and what's left for you is the deciding, not the sorting. (Routing that needs a judgement call still waits for you; the loop files what it safely can and surfaces the rest.)

## What this does *not* do

It doesn't decide what's *worth* keeping — that's your curation, and it's the most valuable thing in the system; the loop moves and files what you chose, it doesn't choose for you (especially for the reference library, where loosening that gate lets in noise). It isn't a replacement for your reading app or your task manager — those stay where you capture and organise; intake is the bridge that gets their contents *into* the vault where your AI can use them. And reliable routing is the hard half: a channel that captures eagerly but files unreliably will quietly bury things, so the filing logic is the part worth getting right.

## Why this works

The vault only compounds if material actually reaches it, and material only reaches it if getting it there is cheaper than not bothering. Frictionless capture wins the moment; reliable routing wins the week; overnight automation removes the filing chore that would otherwise be the thing you skip. Together they keep the shared memory current without a maintenance ritual — which matters more than it sounds, because every other workflow here is only as good as what's in the vault for it to read.

## Note

This is a pattern, not a fixed toolchain. The parts that are yours to shape: which capture channels you actually use, where each kind of thing is routed, how much you automate versus file by hand. Start with one channel — quick capture, or voice notes — and add the others as the inflow they handle starts to pile up. The durable idea is: *make getting things in nearly effortless and getting them filed reliable, so your vault stays current as a by-product of working, not as a chore.* Paste this to your AI and build the version that fits what flows into your day.
