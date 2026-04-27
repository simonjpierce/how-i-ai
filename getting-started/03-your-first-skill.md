---
audience: advanced-user
note: For users who want to understand or build skills manually. The default onboarding path is `/onboard`, which installs starter skills automatically — most readers won't need this.
---

# 03 — Your first skill

A **skill** is a reusable instruction set for Claude. It lives as a markdown file in `~/.claude/skills/`. When you type `/<skill-name>` at the Claude Code prompt, Claude reads the skill file and follows its instructions.

Skills make repetitive work fast. Instead of typing "transcribe this meeting audio, format it with speaker labels, extract the action items, save it to the inbox" every time, you type `/transcribe` and Claude does all of that.

## Copy a skill into your setup

Skills live in `~/.claude/skills/` regardless of which interface you use — desktop app or CLI both load from the same place. Either copy via terminal:

```bash
cd /path/to/mmf-claude-code
cp -R skills/transcribe ~/.claude/skills/
```

Or, if you don't want to touch a terminal, drag the `skills/transcribe` folder into `~/.claude/skills/` in Finder (use `Cmd+Shift+G` and paste the path to navigate there).

The `-R` is recursive — some skills have supporting files alongside `SKILL.md`, and you want all of them.

Then **restart Claude Code**. Skills added mid-session aren't discovered until restart. In the desktop app: close and reopen. In the CLI: `/exit`, then `claude` again.

## Use it on something real

Pick a real task, not a toy one. A meeting audio file you've been meaning to transcribe. A short team meeting recording. Something where the output will be useful either way.

At the prompt — desktop Code tab or CLI, doesn't matter — type:

```
/transcribe /path/to/your/audio.m4a
```

Claude reads the skill, follows its steps (convert audio to wav, run whisper, format speakers, extract action items), and saves the result to your vault.

## What to watch for

- **Claude narrates what it's doing.** This is useful — if it's about to do something you don't want, interrupt with Ctrl-C and correct it. Nothing is permanent until Claude has run it.
- **Dependencies may be missing.** The `/transcribe` skill needs `ffmpeg` and `whisper-cpp` (both via Homebrew). If Claude says "command not found" for either, install them (`brew install ffmpeg whisper-cpp`) and re-run.
- **Output goes where the skill says.** For `/transcribe`, check the inbox folder configured in your vault — the skill prints its output path to the chat when it finishes.

## When the output is wrong

Skills aren't infallible. Small issues (speaker labels swapped, a mis-heard word) — tell Claude what's wrong in the same session: "the speaker labels are reversed, swap them." It'll edit in place.

Larger issues (the skill is genuinely buggy, misses a step, does the wrong thing) — that's worth a proposal PR to this repo. See `CONTRIBUTING.md` for the workflow.

## What's next

`04-adopting-skills.md` — the two-command pattern for installing more skills as you need them.
