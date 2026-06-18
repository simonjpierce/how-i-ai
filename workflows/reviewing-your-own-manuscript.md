# Reviewing your own manuscript

Put your own paper through a hostile, independent review *before* you submit it — several models attacking it, every number and citation re-checked, the analysis pressure-tested — and fold the fixes straight into your draft, so it arrives at the journal having already survived the objections a reviewer would have raised.

This is an idea file. Paste it into Claude Code to build a version for your own work; it'll fill in the specifics (folder layout, which models) in collaboration with you. It's the mirror of [reviewing someone else's manuscript](./reviewing-others-work.md) — same machinery, pointed at yourself — and the last gate of [the science workflow](./the-science-workflow.md) before a paper goes out.

*What you'll need: the independent reviewers — the heart of this — need a second AI model (ideally two) reachable on the command line, run read-only — the maintainer uses the Codex CLI and the Gemini CLI. A separate install and account. With only your main model you still get a fresh hostile pass in a clean context, but weight it less and lean harder on the number and citation checks.*

## The core idea

Reviewing your own draft is the mirror image of [reviewing someone else's](./reviewing-others-work.md): there, you're the outside reader attacking their work fairly; here, you have to attack *your own* — and you are the worst-placed person in the world to do it. You know what you meant, so you read what you meant rather than what's on the page. You believe the result, so you don't probe it. The same investment that got the paper written is what hides its weak points from you on a re-read. That's the exact blind spot [the trust spine](./the-trust-spine.md) exists to cover: the thing that produced the work can't be trusted to check it, and that includes you.

So you borrow independence you don't have. Different AI models, run separately and read-only, attack the draft as a hostile-but-fair reviewer would; you re-verify every number and the inference yourself; and — because it's *your* paper, not someone else's — the output isn't a warm note for an author, it's a set of fixes you fold straight into the text. The point is to spend a reviewer's objections on yourself first, in private, where they're cheap to fix, instead of discovering them in a rejection letter months later.

## How it runs

**Freeze the inputs.** The manuscript, the [lab notebook](./lab-notebook-analysis.md) behind it, and the analysis code are pinned as the reviewed state, so every reviewer reads the same version and you know exactly what the fixes apply to.

**Run several independent reviewers.** Your main model reads at full effort, bringing what it knows of the field, the site, the prior literature. One or two *different* models on the command line, run **read-only**, each play a rigorous-but-supportive journal reviewer: for every issue, the location, the problem, how serious it is, and a concrete fix. Run them concurrently. Where they agree, you have a strong signal; where they differ, something to weigh. Different model families spot different weaknesses — anything two of them flag is almost certainly real.

**Re-verify every number yourself.** Take each count, total, and "X in the table doesn't match Y in the text" the review surfaced, and confirm it against the actual outputs and the notebook — re-sum the column, re-read the source line. A number going into a submitted paper must not rest on a model's say-so. This is the cheapest high-value check there is.

**Verify every citation against the record.** Run [citation verification](./citation-verification.md) over the reference list — each reference checked against the scholarly databases, because a fabricated or mangled citation is exactly the kind of thing that survives your own re-reading and that a co-author will assume you checked. Not-found means *possibly fabricated*: corrected or removed on your call, never silently kept.

**Check the inference, not just the arithmetic.** A separate pass asks whether the *analysis itself* is sound, not just whether the sums add up: are repeated measurements on the same animal treated as independent (pseudoreplication)? How many things were tested versus reported (multiplicity)? Is a "no effect" really just too small a sample to tell? Does a label like "resident" claim more than the data show? AI reviewers lead with surface fixes unless you point them straight at inferential validity, so make this its own step — it's usually the highest-value thing the whole review produces.

**Audit reproducibility.** Run [the replication audit](./the-replication-audit.md): is the code and data behind every figure and number actually in a repository someone could re-run? Submission is the moment this stops being optional — a reviewer may ask, and you want the answer to already be yes.

**Apply a house-conventions pass.** Run the draft past your field's manuscript conventions — citation density, where the discussion should open, what the abstract must carry, calibrating claims to the evidence, keeping interpretation out of the figures. This catches craft issues the correctness passes don't.

**Fold the fixes in — don't staple reviews together.** Because this is your own paper, the accepted fixes go *into* the manuscript, not into a note for someone else. The mechanical and clearly-correct ones the AI applies directly; the genuine judgement calls — a contested interpretation, a framing choice, how hard to defend a result — it brings to you to settle. Reject what you disagree with, with a reason; this is still your paper. And when a fix calls for a *different* method, pull worked examples just as the [external review](./reviewing-others-work.md) does — two or three published papers that applied that method in a comparable setting, verified, and used as recipes for your own revision instead of reconstructing the implementation from scratch.

## What this does *not* do

It doesn't replace your real co-authors, supervisors, or the journal's reviewers — it's the pass that gets the *obvious* objections fixed before those people spend their attention, so their time goes on the hard stuff. Two or three models agreeing is a strong signal, not a peer-review verdict. It won't decide what's safe to publish — a sensitive location, an unpublished result borrowed from a collaborator — it flags; you judge. And it doesn't get to overrule you on your own science: it surfaces and recommends; the paper is yours, and so are the calls.

## Why this works

The hardest draft to review honestly is your own, for a structural reason that has nothing to do with skill: you can't un-know what you meant. A different model, with no investment in the result and no memory of your intentions, reads only what's actually on the page — and that's precisely what catches the unsupported leap, the number that drifted, the claim the data won't quite carry. Re-checking the numbers and the inference yourself turns the models' suspicions into things you can stand behind. You end up arriving at the reviewer's desk having already been your own toughest reviewer — which is the cheapest possible place to take the hit.

## Note

This is a pattern, not a fixed tool. The parts that are yours to shape: how many models you run and how adversarial you make them, whether you add the conventions pass, how much you let the AI fold directly versus bring to you. The one piece worth not skipping is the second independent model — it's the only thing that supplies the distance you structurally can't have on your own work. The durable idea is: *you can't review your own paper honestly, so borrow independence — different models attacking it, every number and citation re-checked — and fold the fixes in before a real reviewer finds them.* Paste this to your AI and shape it to how your field submits.
