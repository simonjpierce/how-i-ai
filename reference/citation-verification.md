# Reference — Citation verification

> **What this is.** The actual method behind [the *Citation verification* workflow](../workflows/citation-verification.md), cleaned of the maintainer's personal specifics (real paths, the local script, machine state). It's a **starting point to adapt, not a drop-in command** — your writing and your tools are shaped differently, so read it *with* your AI and build the version that fits. The narrative workflow says *why* and *when*; this says *how*, concretely enough that your agent doesn't have to reinvent the hard parts.
>
> Throughout, a "DOI" is the permanent identifier most journal articles carry (the `10.xxxx/…` string that resolves at `doi.org`); "your reference library" means whatever curated, on-machine store of papers you keep, if any.

## The one principle that shapes everything

**This is a deterministic lookup, not a job for a language model — and that's the whole point.** The failure you're catching is a model inventing a citation that *looks* real: plausible authors, a plausible year, a journal that genuinely exists, for a paper that was never written. Handing that same class of tool the job of *checking* the citation just invites it to hallucinate a confirmation as confidently as it hallucinated the reference. You'd be asking the fox to audit the henhouse.

So the verification step does **no** language-model reasoning about whether a paper exists. It queries authoritative bibliographic databases — catalogues of the real published record — and compares what comes back, field by field, against what the citation claims. Every verdict traces to a database response the model can't influence, not to the model's own judgement. If you remember one thing from this page: **the lookup must be mechanical; the model's opinion of its own references is worth nothing here.**

## The method

**Pull the references into a checkable list.** Gather every citation — in-text and in the reference list — and parse each into structured fields: authors, year, title, journal, and DOI where present. This parsing step is the one place a model helps, and even here you verify its output (a mangled parse produces false alarms downstream).

**Check your own library first, if you keep one.** Anything already in a curated reference store you maintain can be matched by DOI (or title) and treated as already-vetted — *provided that store confirms metadata on import*, so a match means "checked when it entered," not merely "I chose to save it." This clears the bulk of a typical list cheaply. Honesty caveat: a hand-entered record can still carry a wrong year, so for high-stakes work either re-confirm against the databases or mark the result *found in my library, not externally re-checked*.

**Look up the rest across more than one database.** Query the open bibliographic services — **Semantic Scholar, CrossRef, and OpenAlex**. Use several, not one, because coverage genuinely differs: a paper missing from one is often present in another, so a single-source "not found" produces false alarms. Treat them as a fallback chain — try the next service when the first returns nothing — and rate-limit politely (a short pause between queries) so you don't get throttled.

**Match on durable identifiers, not on the citation string.** Prefer the DOI; absent that, match on title plus authors plus year. Never match on how the citation is *formatted* — formatting varies harmlessly, and a fabricated reference is formatted identically to a real one.

**Check that the details actually agree.** Existence isn't enough. For each found paper, confirm the cited title, first author, year, and journal match the database record. A real DOI attached to the *wrong* paper, or a real paper cited with the wrong year, is a distinct and common error — usually a transcription slip, but one that still has to be fixed.

**Return a verdict per reference, with the evidence:**
- **Found, matches** — a real paper, metadata agrees. Nothing to do.
- **Found, details off** — the paper exists but author/year/title/journal disagrees with the record. Offer the corrected metadata.
- **Ambiguous** — a partial or low-confidence match that can't be confirmed or ruled out. Flag it.
- **Not found in any database** — no match anywhere. This is the one that matters most: *possibly fabricated.*

## The rule that makes it safe

**Never auto-act — flag for a human, with the evidence.** A not-found or mismatched citation is surfaced for a person to decide, showing what was searched and what came back. It is **never silently deleted** (it might be a real source the databases don't index — a book chapter, a brand-new preprint, a government report) and **never silently kept** (it might be invented). Both silent moves are failures. The check's job is to hand over a clear decision queue, not to resolve it.

Two honest limits to build in from the start, so a verdict isn't over-trusted:
- **Not-found is not a guilty verdict.** Grey literature, book chapters, and very recent papers have thin database coverage. A not-found result tells you where to *look*, not what to conclude.
- **A no-DOI match is the weak case.** When matching falls back to title-plus-author word overlap, it produces both false positives (latching onto an unrelated paper) and false negatives (a truncated title that no longer matches). Spot-check *every* no-DOI result by eye — confirm the returned record really is the cited paper — rather than trusting the status.

## What stays yours

Which databases you query and in what order, whether you consult a local library first, how the decision queue is presented, how parsing is done — all adapt to your setup. The transferable spine is just this: *a fabricated citation looks exactly like a real one, so verify every reference against the real record with a mechanical database lookup — never a language model's say-so — and let a person make the call on anything that doesn't cleanly check out.*
