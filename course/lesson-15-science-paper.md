# Lesson 15 — `/science-paper`

Two modes: a lab notebook that enforces good analytical hygiene, and a manuscript drafter that turns a completed notebook into a first journal-ready draft.

> **Video** *(placeholder):* `<https://loom.com/...>` — me opening a lab-notebook session on a real analysis, then later drafting the manuscript from a different completed notebook.

## What it does

**Lab notebook mode** — activated at the start of an analysis session. Enforces the discipline of recording every decision (model choice, parameter, exclusion, sanity check) as you make it. Includes an "update-after-each-step" gate so the notebook stays current with the analysis. Output: a complete lab notebook in your vault that captures what you did and why, before any results are written up.

**Manuscript mode** — drafts a paper in standard journal format (Abstract, Introduction, Methods, Results, Discussion, References) from a completed analysis notebook plus your reference list. The manuscript is a separate document from the notebook — compressed, formal, journal-shaped. It cites the notebook for provenance but doesn't replicate its structure.

The separation is load-bearing: lab notebook is the authoritative record (detail is a feature), manuscript is for readers (detail is friction).

## When to use it

- **Lab notebook mode**: at the start of any data analysis session that will produce publishable results. Activate it before you open the dataset.
- **Manuscript mode**: after the lab notebook is complete and you're ready to write the paper.

## Try it

Lab notebook mode at the start of an analysis session:

```
/science-paper lab notebook mode
```

Manuscript mode once the notebook is complete:

```
/science-paper manuscript mode, drafted from <path-to-notebook.md>
```

## Why the two-mode split

Most analysis sessions slip toward "write the methods as you go" — which sounds efficient but mixes provenance with prose. The lab notebook holds *everything that happened*. The manuscript draws from it but is shaped for the reader. Two separate documents. Two separate modes.

The deep version of this workflow is in [`guides/ai-assisted-scientific-analysis.md`](../guides/ai-assisted-scientific-analysis.md) — required reading before your first publishable analysis.

## Optional dependencies

GitHub CLI (`gh`) authenticated, to push the analysis repo to GitHub. Without it, the skill creates a local-only git repo and tells you how to add a remote later.

## What's next

[Lesson 16 — `/red-team`](./lesson-16-red-team.md). Three independent critical reviewers turned loose on your manuscript before submission.
