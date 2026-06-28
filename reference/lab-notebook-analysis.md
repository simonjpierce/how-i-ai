# Reference — Lab-notebook analysis

> **What this is.** The actual method behind [the *Lab-notebook analysis* workflow](../workflows/lab-notebook-analysis.md), cleaned of the maintainer's personal specifics (real paths, study names, machine state). It's a **starting point to adapt, not a drop-in command** — your field, your data, and your tools are shaped differently, so read it *with* your AI and build the version that fits. The narrative workflow says *why* and *when*; this says *how*, concretely enough that your agent doesn't reinvent the careful parts.
>
> Throughout, "the notebook" means one markdown file that is the authoritative record of an analysis; "a second model" means an independent AI you call from the command line, run read-only so it can't change anything (the maintainer uses the Codex CLI). "The scientist" is the person whose judgement leads — the AI scaffolds, it does not decide.

## The spine: a notebook plus a two-model gate

Two disciplines, run together on every meaningful step:

- **The notebook (continuous).** The AI keeps one markdown file *as it works* — the step-by-step account of what was done, what was found, what it means, and where each output lives. It's written during the work, one step at a time, never reconstructed afterwards from the chat.
- **The gate (per step).** Each step that produces a result is checked by an independent second model — once *before* it runs (is this the right method?) and once *after* (do the numbers actually say what you're about to claim?). Nothing unverified is allowed into the notebook.

The rule that holds both together: **log every step before moving on, and never let an unverified number become part of the record.**

## Why a notebook, not a chat

The default way to analyse data with an AI is one long conversation: paste the data, talk through the tests, copy the results out at the end. The failure is reliable — forty messages in, the model quietly contradicts a decision it made earlier, you've lost track of which approach you settled on, and the numbers in the write-up have drifted from what the code produced. The conversation was the record, and conversations are lossy.

The notebook fixes this by making the *file* the record, not the chat. Each entry captures: **what was done** (method, parameters, the script), **what was found** (the key numbers, tables, stats), **what it means** (interpretation, next step), **where the outputs live** (file paths), and the outcome of the two checks below. Written this way, you never re-derive what you already did, and anyone — including a reviewer, or you in six months — can trace every claim back to the step that produced it.

## The gate, step by step

A "step" is any operation that produces a result: cleaning data, a statistical test, fitting a model, a comparison, an interpretation. Each one runs the same small loop: *propose the method → review it independently → run it → verify the numbers → write the notebook entry.*

- **Before — method review.** State the approach explicitly: what you're doing, the method, why that method, its assumptions, the expected output. Hand that, plus the relevant prior notebook and the data structure, to the second model and ask it to **reason from scratch** — what would *it* do here? — then critique the plan: what assumption is buried, what diagnostic is missing, what confound is ignored. It returns a plain verdict: *aligned*, *aligned with a caveat*, or *divergent*. A caveat or a disagreement **pauses for the scientist's call** — it is never smoothed over. This catches the errors a numerical check never can: the wrong test, the biased subset, the missing prerequisite.
- **(When the step writes code) — code review.** If the step adds or changes an analysis script, run the second model read-only over the *actual code* before trusting the output. This is a different catch from the method review: it finds the off-by-one, the mis-attached covariate, the unit error, the bug introduced while folding the method-review's suggestions in. The plan can be right and the code still wrong.
- **After — numbers check.** State the exact numbers you're about to write (sample sizes, p-values, estimates, intervals). The second model locates each one in the real output file, quotes the source line, and confirms it — or returns a discrepancy that pauses the work until it's resolved. A bare "looks right" with no quoted output counts as a *failed* check, not a pass. Two guards earn their keep here: confirm the output file is actually **fresh** (newer than the script that made it — a number verified against a stale output is not verified), and when a step tunes a model to hit a real-world target, **check it hit the target**, not only the downstream metrics that can look fine while the target is missed by half.

Then the notebook entry is written — including one line on each check (the method verdict and how a caveat was resolved; that the numbers passed and against which output). That line is what makes the two-model collaboration auditable later.

**Settle the foundation before you model.** One rule sits above the per-step gate: before fitting any structural model or running a simulation, pin down *what is actually being estimated* and whether the method's assumptions hold — against both the data and the underlying reality — and get the scientist to confirm it. A simulation can validate a model rigorously and still be validating the *wrong* model; stating the question and the assumptions first is cheap insurance against a precise answer to the wrong question.

**Mark exploratory work as exploratory.** When you're just poking around, you can skip the gate for a stretch — but the skip is *logged in the notebook with the reason*. Rigour is never dropped silently, only ever deliberately and on the record. And at any point where a result really matters, you can pause and aim a deliberately *hostile* review at the whole analysis — a fresh pass at the second model's highest effort, plus an agent told to try to *break* the result rather than confirm it. Run it occasionally and on purpose; a heavy adversarial pass on every step just trains you to tune it out.

## The boundary: the AI scaffolds, it doesn't invent

This is the line that matters most. The method does **not** choose your statistics or design your analysis — picking the model, the test, the framing is the scientist's job, and it's field-specific. It does not replace domain expertise: the calls on a flagged caveat, a model disagreement, or a citation that came back *possibly fabricated* are all the scientist's. And it never invents a result. If no second model is available, the notebook *says so* rather than faking a review; if a step has no output file to check against, it's marked unverifiable rather than waved through. The AI's job is the tedious, reliable scaffolding — keeping the record, running the checks, refusing to let an unverified number graduate — which is exactly the work people skip under time pressure and pay for later. The science stays human.

(Where work cites literature, the same spirit applies to references: each one is checked against the scholarly databases and comes back found, not-found, or ambiguous. Not-found means *possibly fabricated* — flagged for the scientist, never auto-deleted.)

## What stays yours

Where projects live and how you back up analysis code; whether the work involves code at all (for a review or synthesis, "the output" the checks read against is your auditable record — extraction tables, screening logs, source PDFs with page references — not a script log); which second model and command-line tool you use; and how heavily to lean on the rigour for a quick exploration versus a publication result. The transferable spine is just: *the notebook is the record, written as you go; an independent second model checks the first, before and after each step; and nothing unverified is allowed in.*
