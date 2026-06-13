# Reviewing someone else's manuscript

When you're asked to review a paper — a student's thesis chapter, a collaborator's draft, a co-authored manuscript — produce a thorough, genuinely independent review *and* hand the author a warm, plain-language write-up they can actually use, instead of a few scribbled margin notes.

This is an idea file. Paste it into Claude Code to build a version for your own work; it'll fill in the specifics (folder names, exact tools) in collaboration with you. (It has to be an agent that can run tools and create files on your machine — a plain chat assistant can't wire up the review passes or fetch the document.)

*What you'll need: the second, independent reviewer — the heart of this — needs a second AI model reachable on the command line, which is a separate install and account. With only one model you can still get a fresh, hostile-prompted pass in a clean context, but weight it less.*

## The core idea

Reviewing is the mirror image of [drafting your own work](./writing-and-review.md): there, a different model attacks *your* draft before a reader does; here, you *are* the reader, and the job is to attack someone else's draft fairly, then give them something genuinely useful back. Two failure modes spoil that. One: a single AI pass is one opinion — confident, but unchecked. Two: the output reads like a machine — a wall of terse findings an early-career author finds discouraging rather than helpful.

The fix is four moves:

- **Review it more than once, independently.** Two or three different AI models read the whole manuscript separately — your main model, a second model on the command line, and a third where you have one — at least one of them especially good at statistics and at catching numbers that don't add up. Where they *agree*, you have a strong signal; where they differ, something to weigh. Two independent readers beat one; three from different model families is better still.
- **Verify the numbers yourself.** AI reviewers are good at spotting that a total doesn't match a table, but a note going to a co-author must not assert a wrong figure. So you re-check each number the review leans on — re-sum the column, re-count the rows — before it goes in.
- **Check the inference, not just the prose.** A separate pass asks whether the *analysis itself* is sound, not just whether the arithmetic adds up: are repeated measurements on the same animal treated as independent (pseudoreplication)? How many things were tested versus reported? Is a "no effect" really just too small a sample to tell? Does a label like "resident" claim more than the data show? These inferential problems are higher-stakes than any wording fix — a paper can be perfectly typeset and still be drawing the wrong conclusion.
- **Write it *for the author*.** Synthesise the passes into a single, warm review addressed to them by name: bottom line first, strengths foregrounded, every problem framed as fixable, jargon explained. Openly the output of an assistant — never pretending to be you.

## How it runs

**Get the manuscript into a clean, readable form first.** This is fiddlier than it sounds. A document shared with you by someone else often *won't* open through the tidy automated routes — the sharing is tied to a different account than your tools authenticate as, and the polished export paths quietly fail or return only the page furniture, not the text. The reliable path is the dull one: have the owner (or you, if you have edit access) download a plain Word copy, then convert that to clean text your agent can read in full. Build the fancy routes if you like, but fall back to the plain download early rather than fighting the clever ones.

**Run the reviewers.** One is your main model, reading at full effort and bringing what it knows about the field, the site, the prior literature. The other one or two are *different* models on the command line, run **read-only** so they can comment but can't touch the file, each told to be a rigorous-but-supportive journal reviewer: for every issue, give the location, the problem, how serious it is, and a concrete fix; end with the few highest-value priorities and a genuine list of strengths. Run them concurrently — while they think, write up the first.

**Check the arithmetic.** Take every count, total, and "X says one thing, Y says another" the review surfaced, and confirm it against the actual document yourself. State the confirmed ones as *verified*, not "the AI thinks". This is what lets you stand behind the note.

**Check the inference, not just the sums.** Add an explicit pass — your own, or a reviewer prompted specifically for it — on whether the *analysis* is valid: pseudoreplication, multiplicity (how many things were tested versus reported), conclusions a small sample can't support, labels that over-reach. AI reviewers tend to lead with surface fixes unless you point them straight at inferential validity, so make it its own step. It's usually the highest-value thing the whole review produces.

**Add a house-conventions pass.** Run the draft past your field's manuscript conventions — the same ones you'd apply to [your own science writing](./the-science-workflow.md): citation density (don't stack eight references on one claim), where the discussion should open, what an abstract has to carry (a compact, quantitative mini-paper that still reads for a non-specialist — not an over-long methods digest), calibrating claims to the evidence, keeping interpretation in the captions rather than on the figures themselves. This catches craft issues the correctness passes don't.

**Synthesise one note, for the author.** Combine everything into a single document — don't staple three reviews together. Lead with a short orientation: who it's for, that it's AI-assisted, and the one-line verdict. Then a bottom-line-up-front summary, the substantive sections, and an honest "what this review did *not* do". Foreground what genuinely works; calibrate "major" vs "minor" explicitly; explain every technical term in plain words. If a shareable link is useful, the note can be published to a private, unlisted web page — only ever on request, and knowing it discusses unpublished work.

## What this does *not* do

It doesn't send anything as you, and it never writes *as* you — it's openly an assistant's review, so the author knows exactly what they're reading. It doesn't replace the author's supervisors or co-authors, or your own read — it's the pass that gets the obvious objections fixed before those people spend their time. It won't decide what's safe to publish (a sensitive location, an unpublished result) — it flags; you judge. And two models agreeing is a strong signal, not a journal panel's verdict.

## Why this works

A single review is one opinion you can't easily calibrate. Two independent models, plus you checking the numbers, turns it into something you can actually stand behind — and the convergence between them tells you which findings are solid. Writing it warmly, for the named author, is not decoration: a review that reads as supportive and specific gets acted on, where a wall of terse criticism gets defended against. You end up giving what a generous senior colleague gives — a thorough, honest, kind read — at a scale you couldn't manage by hand.

## Note

This is a pattern, not a fixed tool. How adversarial you make the reviewers, how many you run, whether you add the conventions pass or the publish step — all yours, and all optional. The publish-to-a-link step only matters if you have someone to send it to; drop it otherwise. It assumes your main agent can reach a second model for the independent pass — that's the one piece worth setting up.

The mirror case is reviewing *your own* draft before submission. The same multi-model pass and number-checking apply, but instead of a warm note for someone else you fold the fixes straight into your text — and add a replication check: is the code and data behind every figure and number actually in a repository someone could re-run? Decide up front whose manuscript this is, because it changes the output (a note *for* an author, versus edits *into* your own draft).

The durable idea is: *review it independently more than once, verify the numbers and the inference yourself, then write it up warmly for the author — openly as an assistant, never as you.* Paste this to your AI and shape it to the kind of work you review.
