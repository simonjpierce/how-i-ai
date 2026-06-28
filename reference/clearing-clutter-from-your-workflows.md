# Reference — Clearing clutter from your workflows

> **What this is.** The actual method behind [the *Clearing clutter from your workflows* workflow](../workflows/clearing-clutter-from-your-workflows.md), cleaned of the maintainer's personal specifics (real paths, names, machine state). It's a **starting point to adapt, not a drop-in command** — your system is shaped differently, so read it *with* your AI and build the version that fits. The narrative workflow says *why* and *when*; this says *how*, concretely enough that your agent doesn't have to reinvent the hard parts.
>
> Throughout, "your skills directory" means wherever your AI keeps its reusable commands; "a second model" means an independent AI you can call from the command line (the maintainer uses OpenAI's Codex CLI, read-only).

## When it fires

Two distinct jobs, kept separate:

- **The capture habit (continuous, automatic).** When a command fails mid-task and you find a workaround, the fix is appended to that command immediately — failure mode, the correction, what to do instead. This is debt-on-purpose: it's correct at capture time and is left exactly as written.
- **The distillation pass (periodic, deliberate, supervised).** The repayment. Run on **one** command at a time, never in bulk, never autonomously — it rewrites something the rest of your system depends on, so a human drives it.

## The four layers (the core sort)

Read the bloated command and classify it at the **sentence/clause** level — a single paragraph usually mixes several of these:

1. **Method + branching** — the actual instructions and legitimate case-handling. *Keep; tighten only.*
2. **A real rule wrapped in a story** — a genuine guardrail told as an anecdote ("the tool failed silently on most files that day, so always verify the output exists"). *Keep the rule as a plain imperative; drop the date/quote.*
3. **Pure history** — a dated incident note with no live instruction of its own. *Move it to a companion changelog, leaving at most a one-line origin tag.*
4. **Hyper-niche lore** — correct but only relevant inside one rare mode. *Move it to an appendix the command points to at the moment that mode comes up* — so it's reachable when needed without taxing every run.

The preservation rule that makes this safe: an operative rule must survive in the **new body** (or an appendix the body points to). A changelog is history, **not** a home for a live rule — "it exists somewhere" is not the same as "it'll be loaded when needed."

## The do-no-harm check (the part that makes pruning safe)

Before the trimmed version replaces the original, prove no operative rule was lost. Two passes, because step 2 deliberately paraphrases, so a plain text-diff is useless:

- **Mechanical pass — exact tokens.** Pull every concrete command, flag, path, and literal must/never line out of the old version and confirm each still appears in the new body (or appendix). This is necessary but not sufficient — it can't see a *paraphrased* rule.
- **Semantic pass — the real gate.** Hand the old version, the new body, and the relocated files to an independent second model and ask exactly one thing: *list any behaviour-changing rule present in the old version whose behaviour is not preserved in the new body or a pointed-to appendix; the changelog holds history only and does not count.* This is the pass that catches a rule that got smoothed away in a rewrite.

If the two passes disagree, or any rule has no live home, **stop and ask a human.** Never auto-resolve, never silently drop. In practice the semantic pass earns its keep — on a real run of this over a dozen commands, it caught genuine dropped rules in about half of them that the mechanical pass alone missed.

## The bloat detector (how the "raise its hand" half works)

A light periodic scan flags candidates — detection only, it never edits. Useful signals:

- **Size** — the command's body is approaching the length where it no longer fits in a single read. A real cost anchor, not an arbitrary cap.
- **Growth since last cleanup** — record the commit hash at each distillation in the companion changelog; flag a command that's grown by more than ~150 net lines since then.
- **A broken baseline** — if a recorded "last cleaned at" reference can't be found in history any more, the growth signal silently goes dark; surface *that* as its own flag rather than letting the command fall off the radar.

Throttle it to the top couple of candidates per run so the report doesn't flood. A command drops off the list once it's been distilled and records a fresh baseline.

**Tune it from real behaviour, don't guess.** Log whether each flagged command actually got cleaned up or got ignored. A command flagged three times and never touched means the threshold is too low (or it isn't worth cleaning) — that's the signal to adjust, instead of guessing the cut-off.

## Two failure modes worth pre-empting

- **The empty-file trap.** When stamping the "last cleaned at" reference into the changelog with a script, read the file into a variable *first*, then write — never `open(p,'w').write(open(p).read()...)` in one breath, because the write-mode open truncates the file before the read runs, and you silently save an empty file. Assert the file is non-empty before you commit it. (This one actually shipped an empty file before it was caught — hence the assertion.)
- **Treating size as the enemy.** It isn't. A command that's long because its *method* is genuinely large is healthy and stays long. The target is history-per-instruction, not line count.

## What stays yours

The whole shape of your skills directory, whether you keep a formal changelog or an inline comment, which second model you call, the exact thresholds — all adapt to your setup. The transferable spine is just: *capture cheaply in the moment; prune deliberately later, one command at a time, with an independent check that proves nothing load-bearing left with the history.*
