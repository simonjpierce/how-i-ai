# Lesson 14 — `/verify-citations`

Catches fabricated citations before they end up in something you submit.

The lesson reads on its own. A short screencast — me running `/verify-citations` on a manuscript with one deliberately fake reference, what the report looks like, how to act on it — will pair with it when recorded.

> **First time using this skill?** It's an on-demand install, not part of the starter pack. From the Claude Code prompt, run `/install-skill verify-citations`, then quit and reopen Claude Code so the new skill is discovered.

## What it does

Reads the reference list (or in-text citations) of a manuscript and checks each one against Semantic Scholar, CrossRef, and OpenAlex. Flags:

- **Fabricated papers** — the citation doesn't exist anywhere.
- **Wrong authors or years** — the paper exists but the metadata you have is off.
- **Missing DOIs** — papers that should have one but don't, so you can chase the canonical reference.

Consults your local Paperpile mirror (DOI-based) before going to external sources, so cached metadata is used where available.

## When to use it

- **Mandatory** before submitting any manuscript that was drafted with AI assistance. Fabricated citations are the failure mode AI tools are most prone to.
- Before sending a literature review to a co-author for review.
- When you've come back to an old draft and the reference list might have drifted.

## Try it

```
/verify-citations /path/to/manuscript.md
```

Output: a structured report listing each citation, its verification status, and any discrepancies. Spend ten minutes acting on the flags; you've just prevented an embarrassing reviewer comment.

## Dependencies

Python 3 + the `requests` library. The skill checks and tells you if anything's missing.

## What's next

That's the writing & research track. From here:

- **Science-specific work**: [Lesson 15 — `/science-paper`](./lesson-15-science-paper.md). Lab notebook discipline + manuscript drafting.
- **Done for now**: [graduation page](./graduation.md). Optional menu of advanced skills, guides, templates.
