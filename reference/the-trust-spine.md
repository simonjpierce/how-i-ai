# Reference — The trust spine, applied to your own system

> **What this is.** The actual review machinery behind [the *trust spine* workflow](../workflows/the-trust-spine.md), narrowed to its hardest case: the checks an AI runs on **changes it makes to its own setup** — a new automation, a rewritten command, a changed script. It's cleaned of the maintainer's personal specifics (real paths, names, machine state) and is a **starting point to adapt, not a drop-in command** — your system is wired differently, so read it *with* your AI and build the version that fits. The narrative workflow says *why* independence beats self-review; this says *how*, concretely enough that your agent doesn't have to reinvent the two gates.
>
> Throughout, "a second model" means an independent AI you can call from the command line — the maintainer uses OpenAI's Codex CLI, run **read-only** so it can comment but never quietly edit. "A spec" means the short written plan for a change before it's built. "Acceptance criteria" are the checkable promises that plan makes about what *done* looks like.

## The shape: two gates around every self-change

When the system changes itself, the same principle as the rest of the spine applies one level up — *the thing that did the work can't be the thing that checks it.* Here that becomes two independent gates, one on each side of the build:

- **Gate A — before the change ships:** a second model pressure-tests the *plan*. Is the design sound? Does it describe the code that actually exists?
- **Gate B — after the change ships:** a second model re-derives, from the *shipped files alone*, whether each promise the plan made was actually kept.

Neither gate trusts the agent that wrote the plan or the code. That's the whole point: the author's blind spot is the same one that hides the mistake on a re-read.

## Gate A — pressure-test the plan (a converging review loop)

This is not a single "review this" pass. It's a loop that runs until it stops finding things:

- **Round 1 — pre-flight.** Confirm the input is actually a plan/spec, not hand-written prose you'd be destroying by editing in place. Snapshot the original before touching it — the loop edits the plan as it goes, so keep a recovery copy.
- **Round 2 — the second model reviews (lower effort first).** Hand the plan to the second model read-only and ask the sharp question — not "is this good?" but **"for every file and line this plan cites, read the actual file and tell me where the plan's claims don't match reality."** Plans drift from the code they describe; this catches a design built on a stale mental model.
- **Round 3 — arbitrate, don't rubber-stamp.** This is the discipline that makes the loop trustworthy. Each finding gets sorted into one of three buckets:
  - **Fold** — the reviewer is right and the evidence holds (a cited file doesn't exist, an edge is miswired). Fix the plan in place.
  - **Reject** — the reviewer is wrong or unevidenced (a style preference, a naming opinion, a pattern borrowed from elsewhere that doesn't fit here). Log *why* you rejected it, with evidence, and move on.
  - **Judgement call** — a real decision the reviewer can't settle (a scope expansion, two valid architectures, anything that removes content). Park it for a human.
  - The non-negotiable: **re-verify each finding yourself by reading the cited file** before folding it. Don't fold on the reviewer's say-so any more than you'd ship on the author's.
- **Round 4 — re-review at higher effort.** Run the second model again, this time at maximum reasoning, on the *revised* plan, told what was already folded and rejected so it hunts new ground: did the folds introduce fresh contradictions? Are the new safeguards well-formed?
- **Round 5 — final fold + converge.** Apply the same arbitration to the second pass. The loop ends when a pass stops surfacing changes — not at a fixed round count. If more than a handful of genuine judgement calls pile up, that's a signal the plan *wasn't ready for review* — stop and reframe it rather than shipping with a stack of open decisions.

Everything parked as a judgement call lands in an **Open decisions** list for the human. The loop folds the mechanical findings autonomously; it never folds a scope or design choice.

## Gate B — re-derive the result from the shipped files

A plan that passed Gate A and got built still isn't verified. The only signal most systems have is the *implementer's own* "done" note — and the agent that wrote the code wrote that note too. Gate B is the independent second opinion:

- **Read only what shipped.** Resolve the exact set of files the change actually touched, and hand the second model *those files plus the acceptance criteria* — with an explicit instruction to **ignore the implementer's self-assessment and re-derive each criterion from scratch.** The self-report is exactly the thing being checked; feeding it in defeats the gate.
- **Split static from runtime.** For each criterion the reviewer returns one of: **MET / NOT_MET / PARTIAL** (statically confirmable — the edit is there and the logic matches, or it isn't), or **NEEDS_RUNTIME** (genuine behaviour you cannot confirm without actually running it — a lock firing, a dedupe triggering, a second event producing a second record). The reviewer must **not guess "met" for a runtime-only criterion.** The honest output of a static check is often "the code looks right; here are the seven things only a live run can prove."
- **Verify the verifier.** Don't trust the second model blindly either. Re-read the cited lines for every NOT_MET and every claimed bug before acting on them — a false NOT_MET would wrongly condemn a good build. Spot-check the passes and anything that decides the overall outcome.
- **Never auto-approve.** This gate **never flips the change to "verified" on its own.** A clean static pass leaves the change marked *unverified* and hands the human a short, exact live-run checklist — the few things they must exercise themselves. Verified status is the human's call after that run, not the machine's. A confirmed defect flips the change to *needs-revision* and raises a *visible* flag (a silent status change nobody sees is no safeguard at all).

## Why an independent reader catches more

Self-review is structurally weak, not just lazy: a system that just produced an answer — a plan, a diff, a "done" note — is primed to defend it, and the same gap that let the mistake in is the one that reads right past it on review. A *different* model, reading the actual artefact with no stake in it being correct, has no such investment. Running the reviewer read-only keeps it honest in the other direction too — it can flag, but never quietly "fix" and thereby launder its own opinion into your work. And when the two models *disagree*, that disagreement is itself the finding: it's the precise spot worth a human's eye.

## What stays yours

Which second model you reach for, how many rounds you allow before calling a plan "not ready," where the unverified/needs-revision states live, how loud the remediation flag is — all adapt to your setup. The human stays in the loop at both gates by design: the loop parks judgement calls instead of deciding them, and the post-build gate hands over a checklist instead of a verdict. The transferable spine is just this: *put one independent check before a self-change and one after; let the machine fold the mechanical findings but never the judgement calls; re-verify every finding against the actual files; and never let the system bless its own work — the last word on "verified" is a human running it for real.*
