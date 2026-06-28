# Lab-notebook analysis

Run an analysis session the way a careful scientist keeps a lab book — every step recorded as you go, checked by an independent second model before and after, so the record never drifts from what the code actually did and you can trust the result enough to build a paper on it.

This is an idea file. Paste it into Claude Code to build a version for your own work; it'll fill in the specifics (folder layout, which second model) in collaboration with you. It's the first stage of [the science workflow](./the-science-workflow.md) — the analysis that a manuscript is later drafted from — and it's where [the trust spine](./the-trust-spine.md) does its most important work.

*What you'll need: the per-step cross-check leans on a second AI model on the command line (the Codex CLI or the Gemini CLI), run read-only — a separate install and account, and central here rather than optional. Without one you still get the notebook discipline and the citation checks, but not the independent check that answers "how do I know it's right," and a faithful build says so plainly rather than faking it.*

## The core idea

The usual way to analyse data with an AI is one long chat: paste the data, talk through the tests, copy the results into a document at the end. The failure mode is familiar — forty messages in, the model quietly contradicts a decision it made earlier, you've lost track of which approach you actually settled on, and the numbers in the write-up have drifted from what the code produced. The conversation was the record, and conversations are lossy.

The fix is to stop treating the chat as the record. Instead the AI keeps a **lab notebook** as it works — one markdown file that is the authoritative, step-by-step account of the analysis: what was done, what was found, what it means, where each output lives. It's written *during* the work, one step at a time, not reconstructed afterwards. And every step that produces a result is checked, by an independent model, before the next one starts. The discipline that holds it together: **log every step before moving on, and never let an unverified number become part of the record.**

It works for any kind of analysis — a primary statistical model, a simulation, an evidence synthesis, a literature review. There's always a method of some description and always decisions about what to include; that's the part this makes disciplined.

## How it runs

**Set up the project.** The AI creates a project folder — the notebook, a manuscript scaffold for later, and (if there's code) a version-controlled repository for it — then keeps the notebook as you work. After every meaningful step it records, before moving on: what was done (method and parameters), the key numbers, what they mean, where the outputs live, and the outcome of the two checks below.

**Settle the foundation before you model.** One sequencing rule sits above everything else: before fitting any structural model or running a simulation, the AI pins down *what is actually being estimated* and whether the model's assumptions hold — against both the data and the biology — and gets you to confirm it. A simulation can validate a model rigorously and still be validating the *wrong* model; settling the question, the estimand, and the assumptions first is cheap insurance against a precise answer to the wrong question.

**The two checks — the heart of it.** Each significant step runs a small loop: *propose the method → review it independently before running → run it → verify the numbers after → write the notebook entry.* These two checks are [the trust spine](./the-trust-spine.md) applied to analysis:

- **An independent second-model cross-check.** The skill dispatches to a *second AI model in its own command-line tool*, separate from the model doing the analysis, and **read-only** so it can't change anything. *Before* the step, it's given what it needs to judge — the relevant prior notebook, the data or source structure, the planned method, its assumptions, the expected output — and proposes its own method, returning a clear verdict: agree, agree-with-a-caveat, or disagree. A caveat or disagreement pauses for your call rather than being smoothed over. *After* the step, it checks each number against the actual output, quoting the source line; anything it can't confirm is a discrepancy that pauses the work until it's resolved or explicitly noted. If no second model is available, the notebook says so — it never pretends a review happened.

- **Citation verification.** Where the work cites literature, every reference is checked against the scholarly databases and comes back found, not-found, or ambiguous, with the evidence. Not-found means *possibly fabricated* — flagged, never auto-deleted. (This is the reusable [citation check](./citation-verification.md) the other workflows share.)

**Mark exploratory work as exploratory.** By default every result-producing step goes through the checks. When you're just poking around, you can mark a stretch "exploratory" to skip them — but the skip is *logged in the notebook with the reason*, so rigour is never dropped silently, only ever deliberately and on the record.

**Scale the rigour to the work.** A quick exploratory pass needs far less than a result headed for publication. For non-code work — a review or synthesis — "the actual output" the checks read against isn't a script log but your auditable record: extraction tables, screening logs, database exports, the source PDFs themselves with page references. Same discipline, different evidence.

**Turn the check up, on demand.** The per-step checks run continuously and lightly. Alongside them, at any point where a result really matters, you can pause and aim a deliberately *hostile* review at the whole analysis — a fresh pass by the second model at its highest reasoning effort, plus a separate agent told to try to *break* the result rather than confirm it. Running it is your call, not automatic: a heavy adversarial pass on every step just trains you to tune it out, while an occasional deliberate one stays sharp. (For that review to mean anything, the analysis has to be reproducible from the repository alone — see [the replication audit](./the-replication-audit.md), which is the standing habit that makes the hostile review possible.)

## What this does *not* do

It doesn't choose your statistics or design your analysis — picking the model, the test, the framing is yours, and it's field-specific. What it gives you is a session structure and a record-keeping discipline that work the same whether you do mark–recapture, phylogenetics, a meta-analysis, or field tallies. And it doesn't replace your judgement on what it surfaces: the calls on a flagged caveat, a model disagreement, or a possibly-fabricated citation are yours. It won't quietly fix a discrepancy or pretend an independent review happened when it didn't. Keep your own methods; let the notebook keep the record honest.

## Why this works

Self-review is weak — a model that just made an error is the worst-placed to catch it. An independent second model, run read-only against the actual output, catches what self-review can't. And the bookkeeping that rigour really depends on — logging every decision, keeping results tied to outputs, never letting an unverified number into the write-up — is exactly the tedious work people skip under time pressure and pay for later. The AI doesn't get bored doing it, and the step-gate makes skipping it the harder path. The notebook stays trustworthy because keeping it trustworthy is nearly free, and the paper that comes later is only ever as strong as what's traceable underneath it.

## Note

This is a pattern, not a fixed implementation. The parts that are yours to shape: where projects live and how you back up analysis code; whether the work involves code at all; which second model and CLI you use for the independent check; and how heavily to lean on the rigour. It assumes Claude Code as the main driver. The durable idea is: *the notebook is the record, written as you go; a second model checks the first, before and after each step; and nothing unverified is allowed in.* Paste this to your AI and build the version that fits how you work. Once the notebook is solid, [the science workflow](./the-science-workflow.md) drafts the paper from it.

---

*Want the actual method? [The reference](../reference/lab-notebook-analysis.md) lays out the real, cleaned-up version — the concrete steps, the guardrails, the failure modes — minus the personal specifics. A starting point to adapt, not a drop-in.*
