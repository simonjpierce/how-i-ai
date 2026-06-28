# Reference — Writing in your voice

> **What this is.** The actual method behind [the *Writing in your voice* workflow](../workflows/writing-in-your-voice.md), cleaned of the maintainer's personal specifics (real paths, names, the exact set of voice guides). It's a **starting point to adapt, not a drop-in command** — your writing and your formats are your own, so read it *with* your AI and build the version that fits. The narrative workflow says *why* and *when*; this says *how*, concretely enough that your agent doesn't have to reinvent the hard parts.
>
> Throughout, a **voice guide** means a short written spec that describes how you write for one context; "a second model" means an independent AI you can call from the command line, run read-only (the maintainer uses OpenAI's Codex CLI or Google's Gemini CLI), used here only to check that a rewrite changed nothing it shouldn't.

## Why a voice guide beats "write like me"

"Write like me" fails because it's unmeasurable — the model has nothing to aim at, so it falls back to its evenly-grey default. A voice guide fixes this by turning a feeling into a **specification**: concrete features the model can hit and you can check against. Build it once from a body of your own writing in the target format, and every later draft is held to it.

A useful guide carries both halves:

- **Measurable signature** — the spread of your sentence lengths (not "vary your sentences"), your paragraph rhythm, how often and in what words you hedge, whether you open with the point or build to it.
- **Concrete examples and banned moves** — phrases you actually use, and a "never do this" list of the AI tells you want stripped (the stock transition words, the reflexive three-part list, the em-dash in every paragraph). The banned list is the editorial spine of every rewrite.

**Keep one guide per format, not one global voice.** The way you write a formal report isn't the way you write a quick internal message or a field note. A handful of short, separate guides beats one vague master guide.

## Two moves, kept separate

The capability splits into two jobs that share the voice-guide idea but run differently. Don't blur them.

### Capture — rambling thought to a first draft that's already yours

The raw material is *you*, thinking out loud — a voice memo, a dictated stream of consciousness, a messy transcript. The move turns that into a structured first draft in the matching voice guide, so the thinking is yours from the start instead of being summarised back to you in generic AI prose.

- **Transcript is content; the voice guide is style.** Treat what you said as the source of *what* to say, and the guide as the spec for *how* to say it. Restructure freely — spoken rambling and written prose have different shapes — but keep every specific the memo named: places, people, numbers, the actual point.
- **Pick the guide by format, then read it in full before drafting.** Match the memo's purpose to a guide (a report, a supporter update, an internal note), and read the whole guide — especially its banned-moves list — before writing a word.
- **One first-pass draft, not a menu of variants.** The next pass is yours. Land it in front of you for review rather than offering three versions to choose between.

### Rewrite — an existing draft, re-voiced with the content frozen

Here the draft already exists and says what you mean; the job is to make it *sound* like you without letting the meaning drift. This is the move that needs a guard, because re-voicing prose silently nudges content — a "may" hardens to a "does", a caveat drops off a sentence's end, a number shifts — and the result reads *better*, which is exactly when you stop checking.

## The content-freeze discipline (what makes rewrite safe)

Before a re-voiced draft replaces the original, prove the rewrite changed voice and **only** voice. Two layers, because a voice pass deliberately rewords things, so a plain text-diff is useless:

- **Mechanical pass — exact tokens.** Pull every number, date, name, URL, and quoted span out of the before and the after and diff the two lists. This catches a figure or citation that slipped. Necessary, but it can't see a *paraphrased* commitment.
- **Semantic pass — the real gate.** Build a short ledger from the OLD draft of the things that must not move: the asks, offers, promises, permissions, deadlines, attributed claims, the level of certainty, and the intended audience. Hand the old draft, the new draft, and that ledger to an independent second model, read-only, and ask exactly one thing: *list any commitment or claim whose meaning changed* — a "we hope to" turned into "we will", a "preliminary results suggest" turned into "we found", an ask that became an offer, a caveat that quietly vanished. Not "is this good writing?" — the second model can't judge your voice and shouldn't try.

If the two passes disagree, or any frozen item moved, **stop and surface it** rather than auto-resolving. Then bring the human only the genuine judgement calls — a word, an emphasis, a sentence that could go two ways — for their ear to settle.

**Scale the guard to the stakes.** A low-stakes note can take a voice pass with a self-check and no second model. Reserve the full freeze for prose where a silently-drifted meaning would actually cost you — anything external-facing with commitments, facts, or a sceptical reader who'll hold it to account.

## Ghostwritten vs openly-AI — get the mode right

One distinction sits above both moves. Some writing goes out *as you*, under your name, and the prose should read like you. Other writing is openly the assistant's — a review note, an analysis you forward as AI-produced work — and must **not** impersonate you (no first-person "I read through…" as if from your desk); it only needs to be clear, warm, human writing. The voice guide is for the first mode. Getting it backwards is its own failure: ghostwriting where you owed transparency, or impersonating where the reader was told it's an assistant. (Voice is about sounding like you, not about concealment — where a journal, funder, or employer requires disclosing AI assistance, disclose it; that's fully compatible with prose that reads like you.)

## What stays yours

How many voice guides you keep and for which formats, how you build them, where they live, which second model runs the freeze check, and whether a given piece needs the full guard or just a light pass — all adapt to your setup. The human owns the final read every time: the freeze check guards *meaning*, never *quality*, so whether the draft is actually any good, and whether what it says is right, stays your call. The transferable spine is just: *a voice guide is a measurable spec, not an adjective; capture from your own raw thinking so the draft starts yours; and whenever a rewrite reworks the words, prove with an independent check that it didn't move the meaning.*
