# Reference — The intake loop

> **What this is.** The actual method behind [the *Intake loop* workflow](../workflows/the-intake-loop.md), for the specific case of an incoming *document* — a grant application, a report, a media item, a project update — cleaned of the maintainer's personal specifics (real paths, names, the projects involved). It's a **starting point to adapt, not a drop-in command** — your filing conventions and your domains are your own, so read it *with* your AI and build the version that fits. The narrative workflow says *why* and *when*; this says *how* a single document gets in without landing in a pile.
>
> Throughout, "your notes vault" means wherever your AI reads from; "the right project folder" means whatever filing convention you already use; "a domain owner" means whoever (a person, or an AI agent you've set up per area) is responsible for acting on that kind of material.

## The job in one line

A document arrives. The point is that it lands as **structured, findable, routed** content — never as a raw attachment in a downloads folder that you'll mean to deal with and won't. Three moves, in order: **extract** what matters, **file** it by a convention, **route** it to whoever acts on it.

## Extract — turn the document into facts, not an attachment

Read the document fully (for PDFs, run a text extractor first — the maintainer uses `pdftotext`, or an ML-based extractor for anything with tables or figures — because a raw read often can't pull the text reliably). Then pull out what a future you would actually need:

- **Key facts** — what it's about, who's involved, the numbers that matter (amounts, dates, sample sizes, locations).
- **Obligations** — anything it commits you to: a report due, a condition attached, a promise made.
- **Deadlines** — every date that has a "by when" attached to it.

Write these into a **short structured note**, not a copy of the document. The note is the thing your AI will read later; the original file is just the citation behind it. Capturing the obligations and deadlines *as fields in the note* — rather than leaving them buried in the PDF's body — is the whole point: it's the difference between a deadline your system knows about and one that's technically "in there somewhere" and therefore lost.

Keep a link back to the original (the file on your drive, the email thread, the web URL) on the note, so provenance is one click away. If the original lives somewhere fragile, copy it somewhere durable first and link to your own copy.

## File — one convention, so it's findable

Put the note where that *kind* of thing always goes — the matching project folder, the matching domain. The rule that matters is **consistency, not cleverness**: a predictable location you can guess from the document beats a smart one you have to search for. If the right home doesn't exist yet, create it from your standard template rather than inventing a one-off shape.

Two safeguards worth building in:

- **Check for duplicates before filing.** The same report often arrives twice (forwarded, re-sent, a v2). Search your existing record for the title, the sender, or a file ID before adding it again — and keep a lightweight registry of what's already been ingested so the check works *across* sessions, not just within one.
- **Don't overwrite — accumulate.** A newer document adds detail to a note; it doesn't replace what's there. If the new material genuinely *contradicts* what the note already says, don't silently resolve it — leave a visible `TODO/REVIEW` marker naming both versions and move on. Conflicts are flagged for a human, not auto-decided.

## Route — file *with a next action*, to a named owner

Filing without routing is just a tidier pile. The last move is to hand the document to **whoever acts on it, with a concrete next step attached** — "this funder report needs a reply by the 14th" beats "filed under that funder." Decide the domain (research, fundraising, operations, whatever your areas are), and route to that domain's owner — a person, or the AI agent you've set up for that area.

If the next action has a real deadline, also push it onto your actual task list, not just into the note — a marker inside a file you might not reopen for weeks isn't a reminder. Title the task after the *decision or action*, not the document, and link it back to the note.

## The human stays in the loop

The AI does the legwork — extract, draft the note, propose the filing and the route. **A human confirms the calls that matter:** which project this really belongs to when it's ambiguous, whether a flagged conflict is resolved one way or the other, and any routing decision that needs judgement. Run it two ways depending on the moment: **interactive** (it proposes the classification and the changes, you approve before it writes) for one document you care about; **autonomous** (it files what it safely can and queues the judgement calls for later) for an overnight batch. Either way, the genuinely-judgement decisions surface to a person rather than getting silently decided.

## What stays yours

Your filing convention, your set of domains and who owns each, whether a "domain owner" is a person or an AI agent, which extractor you run on PDFs, how aggressively you let the overnight pass file unsupervised — all adapt to your setup. The transferable spine is just: *don't let a document rest as a raw file — extract its facts and obligations into a structured note, file it where its kind always goes, and route it to a named owner with a next action — and keep the judgement calls in front of a human.*
