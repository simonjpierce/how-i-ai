# The science workflow

Run a research project end to end — from the analysis through to a paper ready for submission — with the AI doing the drafting while you steer and check, and with verification built into every stage. It's the spine this whole repo is organised around: the answer to the two questions everyone asks the first time they trust an AI with serious work — *how do I know it's right?* and *how do I know it isn't making things up?*

This is an idea file, and also a map: the science arc is several capabilities that interlock, and this page is the overview that ties them together. Paste it into Claude Code to build the manuscript stage described here, and follow the links to build the others.

*What you'll need: the rigour running through every stage leans on a second AI model on the command line (the Codex CLI or the Gemini CLI), run read-only — a separate install and account, and central here rather than optional. Without one you still get the record-keeping discipline and the citation checks, but not the independent cross-check that answers "how do I know it's right" — and a faithful build says so plainly rather than faking a review. Worth setting up before you lean on this for anything headed for publication.*

## The core idea

Getting science *out* — from data to a paper someone can trust and build on — is a pipeline with a regular shape, and most of what we call expertise is a stack of rules applied consistently along it: how you settle a model before you fit it, how your introductions are structured, how you calibrate a claim to its evidence. Write those rules into your vault once, and the AI can do the heavy lifting at each stage — the drafting, the bookkeeping, the checking — while you bring the judgement and the direction. The AI isn't doing science you couldn't do yourself; it's getting you to the end result faster, so the version you submit is the one you'd have written, reached by editing rather than from a blank page.

The thread that makes it trustworthy is [the trust spine](./the-trust-spine.md): at every stage, the model that did the work is checked by something independent of it — a second model, a re-verified number, a citation checked against the real record. That's what lets you hand the AI more of the pipeline without handing it your credibility.

## The arc

Each stage is its own buildable capability; together they're the pipeline from data to submission.

- **Analysis, kept like a lab notebook.** The work itself — run as a disciplined session where every step is logged as it happens and checked by an independent model before and after, so the record never drifts from what the code did. This is the foundation everything downstream rests on. → [lab-notebook analysis](./lab-notebook-analysis.md)
- **The manuscript, drafted from the notebook.** The paper is a *derivative* of the notebook, not a fresh composition — which is what keeps it honest. This stage is described in full below.
- **Citation integrity.** Every reference checked against the scholarly record, because AI invents real-looking papers that were never written. → [citation verification](./citation-verification.md)
- **Your own voice, without breaking the science.** A verified draft can still read like a machine; the final pass fixes that under one hard rule — the prose may change, the science may not. → [writing in your voice](./writing-in-your-voice.md)
- **An independent review before you submit.** Several models attack your own paper, the numbers and inference re-checked, the fixes folded in — the reviewer's objections spent on yourself first, in private. → [reviewing your own manuscript](./reviewing-your-own-manuscript.md)
- **A reproducibility check.** Could a stranger with your repository link re-run it and land on the same numbers? The test that makes the review mean something. → [the replication audit](./the-replication-audit.md)

You don't build all of this at once. The [analysis notebook](./lab-notebook-analysis.md) is the place to start — it's where the rigour lives and what the rest depends on. Add the manuscript stage when you have a notebook to draft from, and the review and replication stages as a paper nears submission.

## Manuscript mode — drafting the paper from the notebook

This is the stage this page builds. Once the [analysis notebook](./lab-notebook-analysis.md) is solid, the AI drafts the paper *from it*.

The methods and results come first, because they follow fairly directly from the analysis decisions already recorded in the notebook — the AI can largely write them itself. For the introduction and discussion it *interviews you*, asking what it needs to draft that text *with* you rather than expecting you to write it cold. To set the shape, it asks up front whether there's a paper whose structure you're aiming for, and uses that as the manuscript scaffold. And as your own habits accumulate in the vault — the shape your introductions tend to take, the way you report results, the small house rules down to whether you use Oxford commas — it drafts to *your* structure rather than a generic one. That's the quiet payoff of keeping the record this way: you're editing from your own externalised mental model instead of starting from a blank page.

Before anything is shared, manuscript mode runs the checks that catch the usual errors: every result traces to a method and every method to a result; every key number matches across notebook, manuscript, and outputs; key estimates carry uncertainty or a stated limitation; language stays no stronger than the evidence; and [every citation is verified](./citation-verification.md) before it goes to a co-author or reviewer. Then the [voice pass](./writing-in-your-voice.md) makes it read like you wrote it, under the rule that the science can't move while the prose does — and, as submission nears, the [independent review](./reviewing-your-own-manuscript.md) and [replication audit](./the-replication-audit.md) close it out.

## What this does *not* do

It doesn't choose your statistics or design your analysis — picking the model, the test, the framing is yours, and it's field-specific. What it gives you is a pipeline structure and a record-keeping discipline that work the same whether you do mark–recapture, phylogenetics, a meta-analysis, or field tallies. And it doesn't replace your judgement on what it surfaces: the calls on a flagged caveat, a model disagreement, or a possibly-fabricated citation are yours to make. It won't quietly fix a discrepancy or pretend an independent review happened when it didn't. Keep your own methods; let the workflow keep the record honest.

## Why this works

A paper is only ever as strong as what's traceable underneath it. Keeping the analysis as a notebook, drafting the manuscript as a derivative of that notebook, and checking every number and citation against something independent means the chain from data to claim never breaks silently — which is the failure that quietly sinks otherwise-good work. The bookkeeping this depends on is exactly what people skip under deadline; the AI doesn't get bored doing it, so the rigour that was always a good idea finally becomes sustainable.

## Note

This is a pattern, not a fixed implementation. The parts that are yours to shape: where projects live, whether the work involves code at all (a review may not), which second model you use for the independent checks, and how heavily to lean on the rigour. It assumes Claude Code as the main driver. The durable idea is: *the notebook is the record, the paper is a derivative of it, a second model checks the first at every stage, and the paper is only ever as strong as what's traceable underneath it.* Paste this to your AI and build the version that fits how you work.
