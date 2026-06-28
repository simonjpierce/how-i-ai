# Citation verification

Check every reference in a piece of writing against the actual scholarly record — so a fabricated or mangled citation gets caught by you, before a co-author or a reviewer catches it for you.

This is an idea file. Paste it into Claude Code to build a version for your own work; it'll fill in the specifics (which databases, where it plugs in) in collaboration with you. It's deliberately small — a single reusable check that your other workflows call rather than each re-implementing.

*What you'll need: nothing beyond your AI and an internet connection — the scholarly databases this uses (Semantic Scholar, CrossRef, OpenAlex) are open and need no account. If you keep a [reference library](./the-reference-library.md) mirrored on your machine, the check consults that first, which is faster and catches the things you've already vetted.*

## The core idea

This is the one AI failure that is both common and quietly catastrophic: asked to support a claim, a model will sometimes produce a reference that looks completely real — plausible authors, a plausible year, a journal that genuinely exists — for a paper that was never written. It's not lying so much as pattern-completing; the citation *looks* like the citations it has seen. And a fabricated reference is formatted identically to a real one, so nothing about the text gives it away. It sails through a read-through, into a draft, toward a co-author who assumes you checked — because why wouldn't you have.

The fix is not to trust the model about its own references at all. Every citation gets checked against an independent source of truth — the public databases that catalogue the real literature — and comes back with a verdict and the evidence behind it. This is a piece of [the trust spine](./the-trust-spine.md): you verify from somewhere the model can't influence, rather than asking it to vouch for itself.

Because almost everything you write that cites literature wants this same check, it's worth building *once* as its own small step — and having the [writing](./writing-and-review.md), [research](./deep-research.md), [science](./the-science-workflow.md), and [reference-library](./the-reference-library.md) workflows all call it — rather than re-implementing it in each.

## How it runs

**Pull out the references.** The AI gathers every citation in the document — in-text and in the reference list — into a checkable list.

**Check your own library first** *(if you keep one).* Anything already in your curated [reference mirror](./the-reference-library.md) can be matched by DOI or title and treated as already-checked — *provided your library verifies citations as they're imported*, which [the reference library](./the-reference-library.md) does, so a match means the metadata was confirmed when the paper entered, not merely that you chose to save it. That clears the bulk of a typical reference list cheaply and leaves the unfamiliar ones for external lookup. One honesty caveat: curation isn't the same as correct metadata — a book chapter or a hand-entered record can still carry a wrong year — so for anything high-stakes, either re-confirm the match against the databases or mark it *found in your library, not externally re-checked*, rather than treating saved-and-real as proof.

**Check the rest against the scholarly record.** Each remaining reference is looked up across the open citation databases — **Semantic Scholar, CrossRef, and OpenAlex** (more than one, because coverage differs and a paper missing from one may be in another). The check matches on the durable identifiers — DOI where there is one, then title plus authors plus year — not on the formatting of the citation string.

**Return a verdict per reference, with evidence.** Each comes back as one of:
- **Found** — a real paper, metadata matches. Nothing to do.
- **Found, but the details are off** — the paper exists, but the author, year, title, or journal in the citation doesn't match the record. A transcription slip, usually — but it still needs fixing, and the corrected metadata is offered.
- **Ambiguous** — a partial or uncertain match; can't be confirmed or ruled out. Flagged for your eye.
- **Not found** — no matching paper anywhere. This means *possibly fabricated*, and it's the one that matters most.

**Never auto-act — flag for a human.** A not-found or mismatched citation is surfaced for *your* decision, with the evidence (what was searched, what came back). It is **never silently deleted** (it might be a real paper the databases don't index — a book chapter, a very new preprint, grey literature) and **never silently kept** (it might be invented). Both silent moves are failures; the check's job is to hand you a clear decision queue, not to resolve it for you.

## What this does *not* do

It doesn't judge whether a citation is *appropriate* — whether the paper actually supports the claim it's attached to is a separate, harder question (the [research](./deep-research.md) and [review](./reviewing-others-work.md) workflows test that). This check answers only the prior question: *does this paper exist, and is its metadata right?* It also won't catch a real paper cited for a claim it never made — that's a misattribution, not a fabrication. And a not-found result isn't a guilty verdict; some real sources genuinely aren't in the databases. It tells you where to *look*, and you decide.

## Why this works

The failure it guards against is invisible to every other kind of review — a fabricated reference is, by construction, indistinguishable from a real one until you check it against reality. An independent database lookup is the only thing that separates them, and it's nearly free to run. Building it once and calling it everywhere means the check is never the step you skipped because you were in a hurry — which is exactly when a bad citation slips through.

## Note

This is a pattern, not a fixed tool. The parts that are yours to shape: which databases you query, whether you consult a local library first, how the decision queue is presented. The load-bearing rule is the one about never auto-acting — *flag for a human, with evidence; never silently delete or silently keep.* The durable idea is: *a fabricated citation looks exactly like a real one, so check every reference against the actual record — and let a person make the call on anything that doesn't check out.* Paste this to your AI and build the small version that your other workflows can lean on.

---

*Want the actual method? [The reference](../reference/citation-verification.md) lays out the real, cleaned-up version — the concrete steps, the guardrails, the failure modes — minus the personal specifics. A starting point to adapt, not a drop-in.*
