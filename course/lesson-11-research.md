# Lesson 11 — `/research`

Three models, primary literature, a formal report you can read later. The lazy way to do deep research.

> **Video** *(placeholder):* `<https://loom.com/...>` — me kicking off `/research` on a real topic; what the pipeline does and where the report lands.

## What it does

Runs a parallel deep-research pipeline. In order:

1. **Paperpile mirror scan** — if you have a Paperpile (or any curated bibliography) mirror locally, seeds the search with your curated literature first.
2. **Vault scan** — pulls anything relevant you've already written in your own notes.
3. **Three-model web research** — Claude, Codex, and Gemini investigate independently. Multiple perspectives, fewer blind spots.
4. **Claim verification** — fact-checks specific assertions against primary sources.
5. **Formal report** — a single markdown file in your review-queue folder with citations, summary, open questions.

You walk away while it runs.

## When to use it

- *"I want a comprehensive briefing on X."*
- Before a grant application or paper section where you need to know the current state of a field.
- *"Investigate this thoroughly."*
- Comparative analysis ("how do other organisations handle X?").

**Not for** quick mid-task lookups — those are ad-hoc questions in Claude Code, not this skill. `/research` is the heavyweight option for when you genuinely need a report.

## Try it

```
/research the current evidence base for [your topic here]
```

Claude clarifies scope in a short interview (which models to use, depth, what your bibliography mirror covers), then runs. Output: a single markdown report you can edit, cite from, or build on.

## Optional dependencies

`/research` works best with [Codex CLI](https://github.com/openai/codex) and [Gemini CLI](https://github.com/google-gemini/gemini-cli) installed and logged in. Without them it runs Claude-only — still useful, but you lose the multi-model cross-check.

## What's next

[Lesson 12 — `/transcribe`](./lesson-12-transcribe.md). Audio → structured notes; the fastest way to get a meeting out of your head and into a project file.
