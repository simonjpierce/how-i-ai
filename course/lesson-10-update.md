# Lesson 10 — `/update`

Stops your project notes from going silently stale after every working session.

The lesson reads on its own. A short screencast — me running `/update` after a session that touched a project's notes and a process doc, what it proposes to change — will pair with it when recorded.

## What it does

Scans documents associated with the work you've just done — related project notes, process docs, skills, `CLAUDE.md` files, working files — and brings them current with what just happened. It proposes the changes (so you can decline anything that's wrong) before writing.

## When to use it

- After a substantial piece of cross-cutting work — meetings, decisions, drafts that change a project's state.
- When you've edited a skill, a process doc, or an instruction file and want related docs swept.
- When `/document` surfaces decisions that should land in project files, not just the session log.

## Try it

```
/update
```

Claude lists the docs it thinks should be updated and what it proposes to change in each. You approve or decline per file. No silent edits.

## What this prevents

The slow rot where project notes stop matching reality. Without `/update`, project state lives in your head and in whatever you happened to write down at the time; with it, the notes catch up at the end of each session.

## Part 2 universal track done

Lessons 7–10 are the four skills that pay off for everyone, regardless of what you do. From here, the course splits by track:

- **Writing & research** (most of the team): [Lesson 11 — `/research`](./lesson-11-research.md).
- **Science-specific** (analysis + manuscript folks): skip ahead to [Lesson 15 — `/science-paper`](./lesson-15-science-paper.md).
- **Graduation** (you've got enough for now): the [graduation page](./graduation.md) — optional menu of advanced skills, guides, and templates.
