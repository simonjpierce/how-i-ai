# Can we trust the machines? Avoiding the T-1000 scenario

The challenge: how can we trust an AI to do real scientific work? The idea is always to verify. Eventually, hopefully, we'll be able to hand these systems bigger and more complex jobs, and to be able to have a high level of confidence in the results. I don't think we're completely 'there' yet – at least, I'm not – but we're also closer than most people think. 

This is an idea file. Paste it into Claude Code to build a version for your own work; it'll fill in the specifics (which second model, which databases) in collaboration with you. It's also the concept the science workflows all lean on, so it's worth reading even if you build it piecemeal through them rather than all at once.

*What you'll need: the independent-second-model check — the backbone of the whole thing — needs a second AI model reachable on the command line (the Codex CLI or the Gemini CLI), which is a separate install and account. The citation and number checks work with one model. Set the second model up before you lean on any of this for work headed out the door.*

## The core idea

The single thing that stops people trusting an AI with serious work is this: it is *confidently* wrong sometimes, and from the outside a confident right answer and a confident wrong one look identical. A fabricated citation is formatted exactly like a real one. A number that drifted from the analysis sits in the sentence as plainly as the correct one would. So either you re-check everything yourself — at which point the AI saved you nothing — or you don't, and you ship its mistakes under your name.

The way out isn't a better model or a cleverer prompt. It's to stop *trusting* the output and start *structurally verifying* it — with a small set of always-on checks that run underneath all the other work. Call it the **trust spine**: not a workflow you run, but a discipline that runs through every workflow. Its founding assumption is that **the model that did the work is the worst-placed thing to check it** — the same blind spot that let an error in is the one that hides it on a re-read. So verification has to come from somewhere *independent* of the thing being checked.

This is the answer to the two questions everyone asks the first time they hand an AI something that matters — *how do I know it's right?* and *how do I know it isn't making things up?* — and once it's in place, it's also what lets you safely delegate more: the overnight work, the autonomous analysis, the draft you didn't watch being written. You can let go of the wheel exactly as far as the verification underneath will catch a crash.

## The pieces

The spine is a handful of independent checks. Each is cheap; together they cover the failure modes that actually bite.

- **An independent second model, read-only.** The most important vertebra. A *different* AI model — reached through its own command-line tool, and run **read-only** so it can comment but never quietly edit your work — checks what the first model produced. Not "is this good?" but "where is this wrong?" Different model families fail differently, so the one checking has no stake in the one that wrote. When they agree, you have a strong signal; when they don't, you have something to look at. Where no second model is available, the check *says so plainly* — it never fakes a review (see the honesty rule below).

- **Every number re-verified against the actual output.** No quantitative claim enters a deliverable on the model's say-so. Each key figure is checked back against the thing that produced it — the script log, the data table, the source line — and quoted from it. A number that can't be confirmed is a discrepancy that stops the work until it's resolved, not a rounding issue to wave through. This is the cheapest check and the one that prevents the most embarrassing failures, because numbers drift silently and nobody notices until a reviewer does.

- **Every citation checked against the scholarly record.** AI models invent realistic-looking references — plausible authors, a plausible year, a real journal, a paper that was never written. So every reference gets checked against the public citation databases before it goes anywhere. Found, found-but-the-details-are-off, or not-found — and not-found means *possibly fabricated*: flagged for your eye, never auto-deleted, never silently kept. ([Citation verification](./citation-verification.md) is this check built as its own reusable step, which the writing, research, and science workflows all call.)

- **Never declare done from memory.** When the AI says something is finished — the numbers match, the tests pass, the fix works — it re-derives that claim from the *artefact*, not from its recollection of having done it. "I updated the three files" is checked by reading the three files; "the results agree" by re-reading both. The chat is not evidence. This catches the quiet gap between *having intended* to do something and *having done* it correctly.

- **Honesty when a check can't run.** The discipline is worthless if the AI papers over a missing check. If there's no second model, it says so. If a number couldn't be verified, it's marked unverified, not assumed fine. If two sources disagree, [the disagreement is surfaced](./surfacing-conflicts.md), not smoothed into false confidence. An honest "this is unchecked" is worth more than a confident sentence hiding a guess — because the whole point is a record you can *trust*, and one faked check poisons that.

- **An independent cross-check after the system changes itself** *(advanced)*. When the AI modifies its own setup — a new automation, a changed script — the same principle applies one level up: an independent pass re-derives whether the change actually does what was claimed, from the changed files, before it's trusted. (See [growing your own capabilities](./growing-your-own-capabilities.md) and [the self-improvement loop](./the-self-improvement-loop.md).)

## How it shows up

You rarely build the spine as one thing. It's already threaded through the other workflows, and the easiest way in is to notice it there and make it explicit:

- in [the science workflow](./the-science-workflow.md) and [lab-notebook analysis](./lab-notebook-analysis.md), as the two-model gate on every analysis step;
- in [deep research](./deep-research.md), as claims checked against sources and references against the record;
- in [writing and review](./writing-and-review.md), as a different model attacking your draft before a reader does;
- in reviewing a manuscript — [your own](./reviewing-your-own-manuscript.md) or [someone else's](./reviewing-others-work.md) — as independent reviewers plus your own re-check of the numbers;
- in [the self-improvement loop](./the-self-improvement-loop.md), as a second model vetting a fix before it lands.

Each is the same spine, applied to a different kind of work. Building any one of them builds a vertebra; naming the spine is what lets you reuse it deliberately everywhere else.

## What this does *not* do

It doesn't make the AI infallible — it makes its mistakes *visible* before they reach anyone else, which is the achievable goal. It doesn't replace your judgement: the checks *surface* a flagged citation, a model disagreement, a number that won't reconcile — the call on each is yours. And it isn't bureaucracy you run on everything; the rigour scales to the stakes. A throwaway exploratory pass needs almost none; a result headed for publication needs all of it. Dialling it to maximum on trivial work just trains you to tune the alarms out — keep it proportionate so the checks stay sharp where they matter.

## Why this works

Self-review is structurally weak, not just lazy: a system that just produced an answer is primed to defend it. Independence is the whole lever — a different model, a hard re-read of the actual output, an external database — has no investment in the answer being right, so it catches what the producer can't. And the bookkeeping the spine depends on — re-checking every number, verifying every reference, never declaring done from memory — is precisely the tedious work people drop under deadline and regret later. The AI doesn't get bored doing it, and a check that runs by default makes verifying the *easy* path rather than the heroic one. Trust stops being a leap of faith and becomes a property of the system, because keeping it honest is nearly free.

## Note

This is a pattern, not a fixed tool. The parts that are yours to shape: which second model you reach for, how many checks you wire in, how hard you lean on them for a given piece of work. The one vertebra worth not skipping is the independent second model — it's the piece that turns "the AI says so" into "a different AI, with no stake in the answer, agrees." The durable idea is: *the thing that did the work can't be the thing that checks it — so verify from somewhere independent, every time it matters, and never fake a check you couldn't run.* Paste this to your AI and build the version that fits the work you need to trust.

---

*Want the actual method? [The reference](../reference/the-trust-spine.md) lays out the real, cleaned-up version — the concrete steps, the guardrails, the failure modes — minus the personal specifics. A starting point to adapt, not a drop-in.*
