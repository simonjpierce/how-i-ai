---
audience: advanced-user
note: For users who want to install skills manually rather than through `/onboard`. Most readers should run `/onboard` and let it copy the starter skills — this doc is for the rest.
---

# 04 — Adopting skills from this repo

The pattern for installing a skill from this repo into your own Claude Code setup. Skills live in `~/.claude/skills/` and work the same way whether you use the desktop app or the CLI.

```bash
cd /path/to/mmf-claude-code
cp -R skills/<skill-name> ~/.claude/skills/
```

Or drag `skills/<skill-name>` into `~/.claude/skills/` in Finder if you'd rather avoid the terminal.

Then restart Claude Code — skills added mid-session aren't discovered until restart. In the desktop app: close and reopen. In the CLI: `/exit`, then `claude` again.

That's it.

## Keeping it up to date

This repo is a mirror of Simon's setup and updates over time. To pull the latest:

```bash
cd /path/to/mmf-claude-code
git pull
cp -R skills/<skill-name> ~/.claude/skills/   # re-copy any skills you've been using
```

There's no automatic sync — if you want a newer version, re-copy. If you've customised your local copy of a skill and don't want to lose that, diff before copying:

```bash
diff -ur ~/.claude/skills/<skill-name> skills/<skill-name>
```

## Adopt once; diverge gracefully

Your local copy of a skill is yours. You can:

- Use it as-is.
- Modify it for your needs (change defaults, add steps, remove things you don't use).
- Write variants with different names (`transcribe-long`, `transcribe-meeting`).

None of that affects the repo. If your modifications would help the rest of the team, open a proposal PR (see `CONTRIBUTING.md`).

## Don't install all of them

The repo ships a starter set of skills. You probably don't want all of them — install what you'll actually use this week; come back for more when you hit a task that would benefit. See `skills/` for the current list.

## What's next

You're through the onboarding sequence. From here:

- `skills/` — individual `SKILL.md` files to browse.
- `guides/` — deeper workflow explainers (lab notebook, CMR, manuscript review).
- `CONTRIBUTING.md` — the workflow for submitting your own changes.

If you have thirty minutes and want to go deeper fast, the highest-leverage next step is `guides/lab-notebook-workflow.md` (if you're doing analysis) or `guides/manuscript-pre-submission.md` (if you're writing a paper).
