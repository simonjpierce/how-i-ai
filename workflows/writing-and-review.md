# Writing and review

Draft serious writing — a grant, a funder update, an essay, a strategy memo — and have it genuinely *stress-tested* before it goes out, instead of just spell-checked.

This is an idea file. Paste it into Claude Code to build a version for your own work; it'll fill in the specifics (folder names, exact tools) in collaboration with you. (It has to be an agent that can run tools and create files on your machine — a plain chat assistant can't wire up the review passes.)

*What you'll need: the independent critic — the heart of this — needs a second AI model reachable on the command line, which is a separate install and account. If you only have one model, the review degrades toward a model grading its own homework; you can still get value from a fresh, hostile-prompted pass in a clean context, but weight it less and lean on the citation check. Set up the second model when you can — here it's worth it.*

## The core idea

Most people use AI for writing in one of two thin ways: it writes a first draft they then fix, or it proofreads something they already wrote. Both leave the most valuable step on the table — having the work *challenged* before a real reader (a reviewer, a funder, a sceptic) challenges it for you.

The pattern here has three moves, in this order, and the middle one is the point:

- **Draft** — get a first version down, grounded in your actual material — your notes, your data, your earlier writing — and in your own voice, rather than spun from thin air.
- **Review — adversarially.** Hand the draft to an AI told to *attack* it: find the weak claim, the unsupported leap, the place a reviewer will object, the citation that won't hold up, the section that doesn't earn its length. The catch is that the model which wrote the draft is the worst-placed to find its flaws — it tends to admire its own work. So the review is done by a *different* model, running separately, with no power to quietly rewrite the thing. This is the step that turns a plausible draft into a defensible one.
- **Polish** — only once the substance holds, do the final pass for grammar, tone, concision, and voice.

The order matters: there's no point polishing prose you're about to gut, and no point fixing wording when the argument is what's broken.

One carve-out: a *scientific manuscript* headed for peer review wants a heavier, dedicated version of this — one that also re-checks that every number and citation actually reproduces. Same draft → attack → verify → polish shape, just more rigour; see [the science workflow](./the-science-workflow.md) for writing one, and [reviewing a manuscript](./reviewing-others-work.md) for the review side.

## How it runs

**Draft from real material.** Point the AI at your sources first — prior drafts, data, notes, a past piece in the same format as a template — and have it draft from those rather than from a blank prompt. Tell it the audience and the voice you're aiming for. Grounded drafts need far less rescuing later.

**Review with a genuinely independent critic.** This is the heart of it, and the part worth building carefully.

- **A second, independent model.** The reviewer is a *different* AI model from the one that wrote the draft, reached through its own command-line tool — the Codex CLI and the Gemini CLI both work well for this — and run **read-only**, so it can comment but can't silently edit your document. It's told to play hostile reviewer: not "is this good?" but "where will a real reader attack this, and why?" It returns specifics — the exact claim, the exact line, the objection — not vibes. For high-stakes work, run two such models and compare: each architecture spots different weaknesses, and anything both flag is almost certainly real. The independence is what gives this its value; a model grading its own homework mostly tells you it did well.
- **You decide what to fix.** The review surfaces problems; acting on them is yours. The whole step only pays off if you actually work through what it finds rather than nodding past it.

**Verify any citations against the real record.** Where the writing leans on published literature, every reference is checked against the scholarly databases — Semantic Scholar, CrossRef, and OpenAlex — and comes back as found, not-found, or ambiguous, with the supporting evidence. *Not-found means possibly fabricated.* AI models do invent realistic-looking references — plausible authors, a plausible year, a journal that exists, a paper that doesn't — and a flagged citation is held for your attention, never silently kept or silently deleted. This is worth building as its own small reusable check that the review step calls, so anything you write can lean on it.

**Polish last.** Once the substance holds, a light final pass cleans grammar, tightens wordy passages, and smooths tone — without flattening your voice into generic AI prose. A good polish step even scans for the tells of AI writing (overused stock words, formulaic three-part lists, an em-dash in every paragraph) and strips them out, so the result reads like you wrote it rather than a model. Keep this gentle and keep it last. (For a manuscript, where the content carries numbers and citations that must not move, this final pass grows heavier: it rewrites to a voice guide built from your own published writing, and independently checks that nothing in the science drifted while the prose was reworked — see [the science workflow](./the-science-workflow.md).)

## What this does *not* do

It doesn't write *as* you on autopilot — the draft is grounded in your material and your voice precisely so you don't ship something hollow, and the review exists to catch what a fluent-but-empty draft slips past. It's not a substitute for a real expert reader on genuinely high-stakes work; it's how you arrive at that reader's desk having already fixed the obvious objections. And it won't make your decisions for you: which flagged objection matters, whether a not-found citation is a typo or a fabrication, how hard to push back on the critic — those calls are yours. It surfaces; you judge.

## Why this works

Self-review is the weakest kind. A model that just produced a draft is primed to defend it, not dismantle it — the same blind spot that let an error in is the one that hides it on a re-read. A *different* model, run read-only and pointed at the work like an opponent, has no such investment, and catches what self-review structurally can't. The citation check covers the one failure that's both common and quietly catastrophic: a confident, well-formatted reference to a paper that was never written. Put together, you get the thing a good colleague gives you — an honest second pair of eyes before the real audience weighs in — without having to borrow their afternoon.

## Note

This is a pattern, not a fixed tool. What you draft, how adversarial you make the review, how many models you put on it, where you draw the line on polish — all yours, and all optional. The citation check only earns its place if your writing cites literature; drop it if it doesn't. It assumes Claude Code as the driver, with a separate command-line model as the independent critic — whichever one you don't write with. The durable idea is: *draft from real material, have a different model attack it before a reader does, verify what it cites, then polish last.* Paste this to your AI and shape it to what you write.
