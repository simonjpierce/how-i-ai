# Reference — The model panel

> **What this is.** The actual method behind [the *Model panel* workflow](../workflows/the-model-panel.md), cleaned of the maintainer's personal specifics (real paths, names, machine state). It's a **starting point to adapt, not a drop-in command** — your tools and your work are shaped differently, so read it *with* your AI and build the version that fits. The narrative workflow says *why* and *when*; this says *how*, concretely enough that your agent doesn't have to reinvent the hard parts.
>
> Throughout, "your main model" is the agent driving the run (the maintainer uses Claude/Opus); "the panel members" are independent models reachable from the command line (here, OpenAI's Codex CLI and Google's Gemini CLI, each run read-only on its own account); "the synthesiser" is one model — usually your main one — that reads all the answers and reconciles them.

## The two modes — and when each is right

One engine, two jobs. Getting them the wrong way round is the classic mistake.

- **Fresh assessment (the panel, no iteration).** A question answered *once* — a decision, a cross-check, "what do the models, taken together, think about X?" All members hit the **same frozen input** in parallel; the synthesiser reconciles; you stop. The whole value is maximally independent perspectives on one input. Never mutates the input.
- **The loop (panel, then iterate to convergence).** A document improved over *rounds* — a plan, a spec, a draft being hardened. The panel runs once to find the problems, the high-confidence fixes get folded into the document, and then the **edited** document goes back through a model to check whether a fix broke anything. This half is deliberately sequential — each pass must see what the last fold did — and repeats until it stops finding real problems.

Running a parallel panel on a document you're iterating loses the catch-the-regression benefit; looping a one-shot question just wastes effort. The panel is for breadth; the loop is for settling.

## The panel (both modes)

**All members read the same frozen input, in parallel, blind to one another.** Independence is the entire point — three genuinely separate reads, not an echo chamber. Write one shared prompt and send the identical text to each member: state the input, the question, the per-member task, and the output shape you want back. Tell each member it is one independent reviewer that cannot see the others, to reason from scratch, to cite a concrete reference (file-and-line, a data point) for every claim, and to return a single structured object (JSON works well) rather than prose — structure makes the reconciling step mechanical instead of interpretive.

**Run the command-line members read-only.** They can read everything and comment, but cannot change a file — so a panel member can never quietly edit your document. They also run on their *own* accounts and quotas, so leaning on them doesn't drain your main model's budget. Dispatch all members concurrently, then validate each response: non-empty, parses, and carries the fields you asked for. A member that fails after one retry is dropped (see degradation) and the panel proceeds with the survivors.

**Use the synthesiser as a separate instance, not the orchestrator wearing two hats.** If the same model that's coordinating the run also writes panel findings, you've collapsed three perspectives into two. Spin the main-model panelist up as its own independent reviewer.

## The synthesis and the confidence gate

**The synthesiser reads every member's answer and writes a structured merge:** what they agree on (consensus), where they contradict each other (adjudicated against the cited evidence), what only one of them raised (unique), and what *none* of them caught but is now visible reading all the answers together (blind spots). Most of the method's lift comes from this step — forcing the disagreements into the open and weighing them, not just from having more models.

**The confidence gate is what prevents fix-churn.** Several models surface a *lot* of findings, much of it low-value. So act on a finding only if **two of the members agree on it, OR a single member raised it and the synthesiser independently verified it against the actual source.** Everything else is recorded but not acted on. Without that bar you'd churn a working document chasing noise — one model's confident guess dressed up as a finding. In fresh-assessment mode, the gated synthesis *is* the deliverable; you stop here.

## The loop (document mode only)

**Snapshot the document first** (a recovery anchor), then fold only the gate-passed fixes into it in place; park anything that needs a human judgement call. **Then bounce the edited document back through one command-line model**, asking a narrow question: did these folds introduce any new problem, contradiction, or regression? Scope that pass to the previous version plus the change you just made — it's a delta-check, not a fresh full review, so keep it cheap unless the fold touched something load-bearing (a data format, a security boundary, a numeric calculation, or structure many later sections lean on), in which case spend more reasoning on it.

**Reconcile each round** — fold the verified mechanical fixes, log-and-reject the wrong ones with a reason, park the genuine judgement calls — and **repeat until it converges:** a pass comes back with nothing real, or every remaining point is a logged rejection. There's no fixed round count; healthy reviews legitimately run several passes. Two backstops run after *every* round, not just at the end: if the same finding keeps reappearing after being folded, or the count stops trending down, that's oscillation (fix A breaks B, fix B breaks A) or a deeper design fault — **pause and ask a human** rather than looping forever. And if parked judgement calls pile up past a handful, stop and say so — the document wasn't ready.

## Graceful degradation

**Never hard-fail on a missing model.** A panel with one member down is still a panel. If a command-line model is unavailable — its quota's exhausted, or it's sandboxed away from the files this particular task needs — drop it and run with the survivors, and note the degradation in the synthesis so the result carries its own caveat. If the only command-line model is down, fall back to running your main model a second, independent time to fill that slot: weaker (one family, shared quota) but still a structured second read. The floor that matters isn't *three models* — it's *more than one independent look, reconciled deliberately.*

## What stays yours

Which second and third models you add (or whether you start with just your main model run twice), whether you bother with the convergence loop or only ever use the one-shot panel, where you set the bar for "this is high-stakes enough to convene the panel," and the exact shape of the structured output. The transferable spine is just: *on anything that matters, ask several independent models the same frozen question, reconcile them deliberately, act only on what clears the agreement-or-verified bar — and, for a document you're improving, keep looping until it stops finding real problems.*
