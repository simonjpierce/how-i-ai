# Reference — The model panel

> **What this is.** The actual method behind [the *Model panel* workflow](../workflows/the-model-panel.md), cleaned of the maintainer's personal specifics (real paths, names, machine state). It's a **starting point to adapt, not a drop-in command** — your tools and your work are shaped differently, so read it *with* your AI and build the version that fits. The narrative workflow says *why* and *when*; this says *how*, concretely enough that your agent doesn't have to reinvent the hard parts.
>
> Throughout, "your main model" is the agent driving the run (the maintainer uses Claude/Opus); "the panel members" are independent reviewers blind to each other — at least one from a different model family reachable from the command line (here, OpenAI's Codex CLI, run read-only on its own account), with a fresh, independent instance of the main model providing its review seat. A third reviewer can be added where the task warrants it; manuscript review keeps three. For plans and specs, the heaviest model is reserved for the single final audit of keystone changes; "the synthesiser" is one model — usually your main one — that reads all the answers and reconciles them.

## The two modes — and when each is right

One engine, two jobs. Getting them the wrong way round is the classic mistake.

- **Fresh assessment (the panel, no iteration).** A question answered *once* — a decision, a cross-check, "what do the models, taken together, think about X?" All members hit the **same frozen input** in parallel; the synthesiser reconciles; you stop. The whole value is maximally independent perspectives on one input. Never mutates the input.
- **Document review (panel once, fold once).** A plan, spec or draft gets one independent check and one fix pass. The reviewers read the same frozen version; the synthesiser reconciles the findings; the builder folds the verified fixes once and proceeds. No re-review by default.

Both modes begin with independent reads of the same frozen input. Fresh assessment ends with a synthesis; document review adds one fold. Repeated loops mostly found very unlikely edge cases.

## The panel (both modes)

**All members read the same frozen input, in parallel, blind to one another.** Independence is the entire point — genuinely separate reads, not an echo chamber. Write one shared prompt and send the identical text to each member: state the input, the question, the per-member task, and the output shape you want back. Tell each member it is one independent reviewer that cannot see the others, to reason from scratch, to cite a concrete reference (file-and-line, a data point) for every claim, and to return a single structured object (JSON works well) rather than prose — structure makes the reconciling step mechanical instead of interpretive.

**Run the command-line members read-only.** They can read everything and comment, but cannot change a file — so a panel member can never quietly edit your document. A different-family member (here, Codex) runs on its own account and quota, so leaning on it doesn't drain your main model's budget; additional Claude reviewers share the main account's limits. Dispatch all members concurrently, then validate each response: non-empty, parses, and carries the fields you asked for. A member that fails after one retry is dropped (see degradation) and the panel proceeds with the survivors.

**Keep the main-model reviewer separate from the orchestrator.** The orchestrator merges the findings; a fresh instance of its model supplies the independent review. If the model coordinating the run also writes panel findings, you've collapsed three perspectives into two.

## The synthesis and the confidence gate

**The synthesiser reads every member's answer and writes a structured merge:** what they agree on (consensus), where they contradict each other (adjudicated against the cited evidence), what only one of them raised (unique), and what *none* of them caught but is now visible reading all the answers together (blind spots). Most of the method's lift comes from this step — forcing the disagreements into the open and weighing them, not just from having more models.

**The confidence gate is what prevents fix-churn.** Several models surface a *lot* of findings, much of it low-value. So act on a finding only if **two of the members agree on it, OR a single member raised it and the synthesiser independently verified it against the actual source.** Everything else is recorded but not acted on. Without that bar you'd churn a working document chasing noise — one model's confident guess dressed up as a finding. In fresh-assessment mode, the gated synthesis *is* the deliverable; you stop here.

## One fold (document mode only)

**Snapshot the document first** (a recovery anchor), then fold only the verified fixes into it in one pass. Record rejected findings with their evidence and park anything that needs a human judgement call. The work then proceeds without re-review.

**Three exceptions keep one closing re-check after the fix:** anything that runs unattended and changes your notes, task queue, calendar or money; numbers in scientific outputs, which get an independent re-count; and keystone changes with wide reach, which get one final audit by the heaviest model. Keep that check to one pass, not a loop until it settles.

## Graceful degradation

**Never hard-fail on a missing model.** A panel with one member down is still a panel. If a command-line model is unavailable — its quota's exhausted, or it's sandboxed away from the files this particular task needs — drop it and run with the survivors, and note the degradation in the synthesis so the result carries its own caveat. If the only command-line model is down, fall back to running your main model a second, independent time to fill that slot: weaker (one family, shared quota) but still a structured second read. The floor that matters isn't *three models* — it's *more than one independent look, reconciled deliberately.*

## What stays yours

Which second and third models you add (or whether you start with just your main model run twice), where you set the bar for "this is high-stakes enough to convene the panel," and the exact shape of the structured output. The transferable spine is just: *on anything that matters, ask several independent models the same frozen question, reconcile them deliberately, act only on what clears the agreement-or-verified bar — and, for a document you're improving, fold the verified fixes once, with a closing re-check only for the three exceptions above.*
