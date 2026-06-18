# Writing in your voice

Get the AI to write things that actually sound like *you* — built from the measurable features of your own writing, not a vague "be more casual" — and let it rework your prose hard without the meaning quietly drifting while it does.

This is an idea file. Paste it into Claude Code to build a version for your own work; it'll fill in the specifics (which of your writing to learn from, where the guide lives) in collaboration with you.

*What you'll need: a sample of your own writing for the AI to learn from — papers, essays, past emails, whatever format you're targeting. The fidelity check that protects meaning during a rewrite leans on a second AI model on the command line, run read-only (the maintainer uses the Codex CLI or the Gemini CLI); worth setting up, but you can start with just the voice guide and add the check later.*

## The core idea

AI prose has a tell. Even when it's correct and well-organised, it's evenly grey — every sentence about the same length, a stock set of transition words, a three-part list whenever it can manage one, an em-dash in every paragraph. It reads like a competent stranger, not like you. And the usual fix — telling it "write more like me" or "be warmer" — barely moves the needle, because the instruction is too vague to act on.

Two ideas fix this, and they're separable.

The first: a **voice guide** describes how you write in terms a model can actually hit — *measurable* features, not adjectives. Not "be conversational" but how much your sentence lengths vary, how often and how you hedge, the words you never use, whether you open with the point or build to it. Built once from your own writing, it becomes a calibration target every later draft is held against.

The second: when AI reworks prose for flow, it reliably nudges the *content* too — a "may" hardens to a "does", a caveat falls off the end of a sentence, a number shifts. The writing improves while the meaning silently drifts. So a serious voice rewrite needs a **fidelity check** underneath it — an independent guard that the science (or the facts, or the argument) didn't move while the words did. This is [the trust spine](./the-trust-spine.md) applied to prose: the thing doing the rewriting can't be trusted to confirm it changed nothing.

## How it runs

**Build the voice guide from your own writing.** Point the AI at a body of your work in the target format and have it extract the measurable signature: the spread of your sentence lengths, your paragraph rhythm, how you hedge (and how often), your stock moves and the ones you avoid, whether you lead with the conclusion. (The maintainer's was distilled from his own papers and book chapters, down to a target spread of sentence lengths.) The output is a short reference document — not prose advice, a *specification* — that lives in your vault and gets reused. You'll likely keep more than one: the way you write a paper isn't the way you write a funder email or a field note, so a voice guide is per-format.

**Know which mode you're in: ghostwritten, or openly AI.** A real distinction worth making explicit. Some writing goes out *as you*, under your name — an email, a donor note, a paper — and the *prose* should read like you, not like a model. (That's a point about voice, not concealment: where a journal, a funder, an employer, or a collaborator has a rule on disclosing AI assistance, follow it — writing that sounds like you and disclosing that AI helped produce it are not in tension, and this guide is about the first, never about hiding the second.) Other writing is openly the assistant's — a review note, an analysis you're forwarding as AI-produced work — and must *not* impersonate you (no first-person "I read through…" as if it came from your desk); it just needs to be clear, warm, human writing. The voice guide is for the first mode. Getting this backwards is its own failure: ghostwriting where you should be transparent, or impersonating where the reader was told it's an assistant. (This repo itself is the second mode — written *about* the maintainer, not *as* him.)

**Rewrite to the guide, then check fidelity — the loop that matters.** For anything where the content is load-bearing, the rewrite runs as a guarded loop: the AI rewrites a section to your voice guide; then a *second* model, read-only, checks the rewrite against the original — not "is this good writing?" (it can't judge your voice and shouldn't try) but *"did the rewrite quietly change anything it shouldn't?"* — a number that moved, a citation that drifted, a hedge that hardened. Beneath that, a blunt mechanical check pulls every number out of the before and the after and diffs the two lists, so anything that slipped is caught before you see the draft. Only then does the AI bring you the few genuine judgement calls — a word, an emphasis, a sentence that could go two ways — for your ear to settle.

**For lighter writing, skip the guard.** Not everything carries numbers and citations that must not move. A blog post or an internal note can take a voice pass without the full fidelity loop — apply the guide, read it yourself, done. Reserve the belt-and-braces for prose where a silently-drifted meaning would actually cost you: a manuscript, a grant, anything a sceptical reader will hold to account.

## What this does *not* do

It doesn't invent a voice for you — it learns the one you already have, so it needs real samples of your writing to work from. It won't make a hollow draft worth reading; voice is the finish, not the substance, and a well-voiced empty argument is still empty (the substance comes from [drafting on real material and reviewing it](./writing-and-review.md)). And the fidelity check guards *meaning*, not quality — it confirms the rewrite didn't change what you said, not that what you said was right. Those are your calls.

## Why this works

"Write like me" fails because it's unmeasurable; a voice guide works because it turns a feeling into targets a model can actually aim at and you can actually check against. And the fidelity guard exists for a failure that's easy to miss precisely because the output looks *better*: prose reworked for flow reads more smoothly, so you're inclined to trust it — exactly when a caveat has quietly gone missing. An independent check with a number-for-number diff under it is what lets the writing be improved hard without the meaning moving an inch.

## Note

This is a pattern, not a fixed tool. The parts that are yours to shape: how many voice guides you keep and for which formats, how you build them, whether a given piece needs the fidelity loop or just a light pass. The load-bearing ideas are two: *a voice guide is a measurable spec, not an adjective*, and *a rewrite that touches meaning needs an independent check that it didn't.* The durable idea is: *learn your real voice from your real writing, write to that target, and guard the meaning whenever the words get reworked.* Paste this to your AI and build the version that fits how you write.
