# Lesson 5 — Your `CLAUDE.md`

This is the lesson that makes Claude useful for *you* specifically, not generic-anyone. It's also the longest single lesson in the course (mostly because Claude is doing the work, not you — you just answer questions).

The lesson below has every step. A short screencast of `/onboard` running on a fresh vault — what the interview looks like, what files get written — will pair with it when recorded.

## What we're about to do

In lesson 2 you read about the `CLAUDE.md` cascade — a root file with cross-cutting preferences, folder-level files with domain context. You could write all those files by hand. Don't. Claude will write them for you, faster and better, based on a short interview.

This is what the `/onboard` skill does:

1. Asks you a handful of questions about yourself, your work, and how you like to write.
2. Writes a personalised `~/.claude/CLAUDE.md` (global behavioural defaults), a vault-root `CLAUDE.md` (who you are, what you do), and starter log files.
3. Optionally walks you through your top-level domain folders and writes a folder-level `CLAUDE.md` for each.
4. Drops a `Getting Started.md` kickoff note in your vault's `00_INBOX/` so the next session has somewhere to land.

You answer questions. Claude does the writing. You edit afterwards if anything's off.

## Steps

### 1. Paste the bootstrap prompt

Open Claude Desktop, Code tab, vault selected (from lesson 4). Paste this prompt:

```
Walk me through setting up the system at github.com/marinemegafauna/mmf-claude-code on my machine. I'm new to all of this — please hand-hold me through it, asking me one question at a time.
```

Claude will clone the repo into `~/.claude/repos/mmf-claude-code/`, install the starter skills (`/onboard`, `/session-start`, `/document`, `/update`, a few others) into `~/.claude/skills/`, and tell you to **quit and restart Claude Code** so it picks them up. Do that.

### 2. Run `/onboard`

After the restart, type `/onboard` in the Code tab. The skill begins the interview.

The questions cover:

- **Who you are** — your name, what you do, organisation.
- **How you write** — spelling conventions (NZ/UK English vs US), tone, what you care about ("evidence-based", "measured claims", "no overstatement").
- **What you work on** — the broad domains you split your time across (research, writing, ops, photography, personal — whatever it is for you).
- **Your task manager** — Claude records which one you use (Things 3, Todoist, Apple Reminders, Asana, etc.). Some optional skills (like `/research`'s follow-up task) reference it. The `/todo` skill that routes tasks into it is in the graduation page's personal-workflow section — install it later if you want it.
- **Optional: per-domain context** — for each top-level folder you flag as important, Claude offers to write a `CLAUDE.md` with domain-specific terminology, key people, project lists.

Just answer in plain English. **Ramble if you want.** Don't structure your answers — Claude sorts through tangents and asks follow-ups if anything's ambiguous.

**Use the microphone button.** Speaking is faster than typing for anything longer than a sentence. The Claude Desktop prompt area has a mic button on the right; **press and hold** to record, release to send.

### 3. Review what got written

When `/onboard` finishes, your vault has:

- `~/.claude/CLAUDE.md` — global behavioural defaults (cross-cutting preferences).
- `<vault>/CLAUDE.md` — vault-root file: who you are, what you work on, how you write.
- `<vault>/<DOMAIN>/CLAUDE.md` for each domain folder you opted into.
- `<vault>/MEMORY.md` — the auto-memory file (starts mostly empty; fills up as you correct Claude over time).
- `<vault>/00_INBOX/Getting Started.md` — your kickoff note.

Open each in Obsidian. Read them. **Edit anything that's wrong.** Claude's draft is a starting point, not a contract. If the writing voice is off, fix it. If the project list missed something, add it.

### 4. Switch to Auto mode

Per lesson 4: the default permission prompts get tedious fast. To stop them:

1. In Claude Desktop's Code tab, look at the bottom-left of the prompt area. There's a small badge that cycles between three modes: **default**, **Accept edits**, and **Auto mode**.
2. Click the badge (or press Shift-Tab) until it shows **Auto mode**.

That's the per-session toggle. To make Auto mode the default for every session, ask Claude in the chat: *"Add Auto mode to my settings as the default."* Claude will edit `~/.claude/settings.json` and explain what it changed.

Trade-off: Auto mode lets Claude run any shell command without asking. You're trusting it to act on your machine. If you're not comfortable with that, keep using **Accept edits** mode instead — it still prompts before shell commands but lets file edits through.

## Common things to fix immediately after `/onboard`

- **Spelling drift.** If you said "NZ English" but the draft uses "organization" anywhere, search-and-replace.
- **Project list staleness.** Anything you mentioned that's no longer active — remove it now so Claude doesn't keep referencing it.
- **Tone mismatch.** If Claude's draft of "how you write" sounds wrong, rewrite that section in your own voice. Even a paragraph or two is fine — quality over quantity.

## What's next

[Lesson 6 — Your first real task](./lesson-06-your-first-real-task.md). Pick something on your plate, do it the new way. The course ends here for the universal track, then Part 2 covers core skills.
