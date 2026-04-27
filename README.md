# MMF Claude Code

A complete **Claude Code + Obsidian** system for thinking knowledge work — memory across sessions, behavioural defaults, log-driven self-customisation. Two apps wired together: Claude Code does the work, Obsidian is where your notes live. Built up by Simon over the past year and shared here for the MMF team and close collaborators. Block 30 minutes total: ~10 minutes downloading both apps, then a 10–15 minute interview where Claude asks you questions. **No reading required.**

**Currently macOS-only.** Windows and Linux support is on the v1 roadmap. If you're on Windows or Linux and want to set this up anyway, ping Simon for a manual install — `/onboard` will halt cleanly otherwise.

## How to set this up

You don't need to read this repo to use it. Three steps:

1. **Install [Claude Desktop](https://claude.com/download).** Claude Code is included on a Pro plan ($20/month) and any higher tier. **MMF science team:** Simon should have added you to the MMF org plan before sending this link — if you sign in and the Code tab still says "upgrade," DM him your GitHub username + the email you signed in to Claude with. **Close collaborators outside MMF:** Pro is the right plan; the higher tiers aren't necessary.
2. **Click the "Code" tab** in the desktop app (you'll see Chat, Cowork, and Code tabs). Despite the name, "Code" isn't just for programming — it's the only tab that can read and write files on your Mac. Click **Select folder** and pick any folder for now (your Documents folder is fine). This is a temporary "scratch" folder just to run the install. At the end of `/onboard`, Claude will tell you to quit and relaunch the Code tab pointed at your new vault — that's where all your real work happens.
3. **Paste this prompt** into the Code tab:

   ```
   Walk me through setting up the system at github.com/marinemegafauna/mmf-claude-code on my machine. I'm new to all of this — please hand-hold me through it, asking me one question at a time.
   ```

Claude takes it from there — a short interview (~10–15 min) and you end up with a working vault, a personalised CLAUDE.md cascade, behavioural defaults, log files, and a kickoff note in your inbox. **Dictation strongly recommended over typing** — in the Claude Code desktop app, **press and hold the microphone button** in the prompt area, talk, release to send. (Terminal users: macOS Fn-Fn dictation works anywhere, or ChatGPT voice mode with Plus + paste.) Ramble is fine — unstructured monologues, tangents, contradictions are all welcome. Claude will sort through what you said and ask follow-ups if anything's unclear.

## Already using Claude Code?

If you have an existing setup and want to browse rather than reinstall:

- **The big picture and philosophy** — [`getting-started/00-how-simon-ais.md`](./getting-started/00-how-simon-ais.md). Architectural overview; ~10 min read.
- **Browse skills** — [`skills/`](./skills/). Each `SKILL.md` has a one-line description. Two-command install: see [`getting-started/04-adopting-skills.md`](./getting-started/04-adopting-skills.md).
- **Deeper workflow docs** — [`guides/`](./guides/).
- **Contribute** — [`CONTRIBUTING.md`](./CONTRIBUTING.md). Small improvements welcome; large changes best discussed first.

## Who this is for

The MMF science team and close collaborators — the people working with Simon on research, writing, and operations who use (or want to use) Claude Code in that work.

This is **not** a public resource. The content references MMF projects, funders, and internal workflows, and assumes you have context from working with Simon.

If you want to read the architecture before/instead of running `/onboard`:

- `00-how-simon-ais.md`, `01-install-claude-code.md`, `02-use-code-not-chat.md` are written for humans — they explain what Claude Code is and why this setup is shaped the way it is.
- `03-your-first-skill.md`, `04-adopting-skills.md`, `05-set-up-your-vault.md` are written for Claude to follow during onboarding — you can read them, but they're scripts, not explainers.

## Repository map

```
mmf-claude-code/
├── getting-started/    Numbered onboarding guides + tactical setup doc Claude reads during /onboard
├── skills/             Installable Claude Code skills (one folder per skill)
├── guides/             Deeper-dive workflow docs — Ghostty setup, lab notebook, manuscript review
├── templates/          Starter vault and `~/.claude/` templates that ship with /onboard
└── sync/               The script Simon uses to mirror his vault's skills and templates into this repo
```

## Available skills

Skills are markdown files Claude reads to know how to handle specific tasks. The `/onboard` flow auto-installs ten of these (marked ★ below); the rest ship in [`skills/`](./skills/) — ask Claude to install any of them when you want it (e.g. *"install /transcribe for me"* — Claude will check the dependencies, brew-install anything missing, and copy the skill). You don't need to memorise slash-command names; plain-English requests work too.

### Core onboarding & workflow

- **`/onboard`** ★ — first-run setup: discovery interview, personalised CLAUDE.md cascade, starter logs, kickoff note. Run once per machine.
- **`/session-start`** ★ — orient at the start of a session: reads recent handoff, surfaces stale friction, checks open threads.
- **`/document`** ★ — end-of-session handover: records what was done so the next session picks up cleanly.
- **`/update`** ★ — bring all docs current: scans related process docs, project notes, skills, CLAUDE.md files.
- **`/refresh-skills`** ★ — pull contributor improvements from this repo into your local `~/.claude/`, walking through any conflicts.
- **`/review-friction`** ★ — walk through `[OPEN]` Friction Log entries one at a time, marking each resolved/deferred/skip.

### Writing & research

- **`/research`** ★ — three-model deep research (Claude + Codex + Gemini), claim verification, formal report. *Optional: Codex CLI + Gemini CLI logged in. Without them, runs Claude-only.*
- **`/science-paper`** ★ — lab-notebook discipline during analysis sessions; manuscript drafting from a completed notebook.
- **`/todo`** ★ — add a task to your task manager (Things 3, Todoist, Apple Reminders, or a vault `TODO.md`). Routes based on the choice you made during `/onboard`. Other task managers (Asana, Linear, Notion) aren't natively routed yet — fall back to `vault_todo` or ask Claude to add a routing branch for your tool.
- **`/polish`** — grammar and style checks via LanguageTool + Vale, then apply fixes. *Requires LanguageTool + Vale installed locally.*
- **`/verify-citations`** ★ — verify scientific citations against Semantic Scholar, CrossRef, OpenAlex. *Requires Python 3 + the `requests` library.*

### Ingestion

- **`/transcribe`** — transcribe audio or format raw transcripts; runs whisper-cli with speaker labels and topic sections. *Requires whisper-cli; speaker diarization needs pyannote.*
- **`/pdf-to-markdown`** — convert a PDF into clean markdown for Obsidian. *Requires `marker_single` (preferred) or `pdftotext` + `pandoc` as fallback.*

### Independent review

- **`/red-team`** — three-model independent critical review of an important document. *Optional: Codex + Gemini CLIs for second/third opinions; without them, runs as a Claude-subagent-only review.*

### MMF-only

- **`/mmf-brand`** — apply Marine Megafauna Foundation brand identity (colours, typography, logos, layout) to MMF-facing artifacts. Most useful if you produce MMF materials.

## The stack

**Required:**

- **[Claude Code](https://docs.claude.com/claude-code)** — the underlying tool, available as a desktop app or CLI. Skills are markdown files loaded from `~/.claude/skills/` and work identically in either. The `/onboard` flow defaults to the desktop app for newcomers; the terminal CLI is the path for advanced users wanting hooks and shell-tool integration (see [`guides/ghostty-setup.md`](./guides/ghostty-setup.md)).
- **[Obsidian](https://obsidian.md)** — where notes live. Most guides reference Obsidian workflows, but the skills themselves don't require it. `/onboard` walks you through Obsidian install if you don't have it yet.

**Optional (install later if you want them):**

- **[Codex CLI](https://github.com/openai/codex)** — ChatGPT's equivalent, useful for a second-opinion peer review from inside Claude Code. `/red-team` uses it when available.
- **[Gemini CLI](https://github.com/google-gemini/gemini-cli)** — free for 1,000 requests/day. Used as a third reviewer by `/red-team`.

Individual skills document their own dependencies in their `SKILL.md`.

## Living repo disclaimer

This repository mirrors a real, evolving setup. Things change. If something looks broken, stale, or contradicts another doc, open an issue or PR — that's how we keep it current.

## Licence

- **Code** (scripts, skills, hook configs): [MIT](./LICENSE).
- **Prose** (guides, README, templates): [CC-BY-4.0](./LICENSE-CC-BY-4.0).

Private repository; licence terms apply in the event that content is later extracted and shared externally.
