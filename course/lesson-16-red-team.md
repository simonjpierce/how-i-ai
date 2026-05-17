# Lesson 16 — `/red-team`

Three independent critical reviewers, none of whom were involved in writing your document, turned loose on it before you submit.

The lesson reads on its own. A short screencast — me red-teaming a manuscript draft, how each model approaches it differently, what the consolidated report looks like — will pair with it when recorded.

> **First time using this skill?** It's an on-demand install, not part of the starter pack. From the Claude Code prompt, run `/install-skill red-team`, then quit and reopen Claude Code so the new skill is discovered.

## What it does

Runs three independent reviews of an important document:

1. **Claude subagent** — structured review against a defined rubric. Predictable shape, comprehensive coverage.
2. **Codex CLI** — open-ended critique. Tends to surface different angles than Claude.
3. **Gemini CLI** — open-ended critique. Third perspective; useful for diverging takes.

Each model reviews the document fresh, without seeing the others' findings. Then the skill consolidates the three reports into a single structured output: areas of agreement (high-confidence issues), divergent flags (one model raised it, others didn't), and recommendations ordered by severity.

For specs and process documents, the skill automatically also reviews the *associated implementation* (the code, scripts, or other artefacts the document is meant to govern). For manuscripts, it reviews only the document itself.

## When to use it

- Before submitting a manuscript to co-authors or a journal.
- Before sending a grant application.
- Before committing to a substantial spec or process change.
- When a document feels finished and you want to find out where it isn't.

**Don't trigger on generic** *"review this"* **or** *"critique this"* — those should be lighter-weight checks. `/red-team` is heavy and slow; use it when stakes are real.

## Try it

```
/red-team /path/to/document.md
```

The skill takes a while — three full reviews aren't instant. You can walk away. Output is a single consolidated report in your review queue.

## A note on disagreement

When two of the three reviewers agree on a finding, take it seriously. When only one flags something, treat it as "worth a look" — the model might be right or wrong, but it's signal worth checking.

## Optional dependencies

Codex + Gemini CLIs are the second and third reviewers. Without them, `/red-team` runs as a Claude-subagent-only review — still useful, just less varied.

## What's next

You've finished the course. **Congratulations.** The [graduation page](./graduation.md) is the optional menu — advanced skills, deeper guides, templates to adopt when you want them.
