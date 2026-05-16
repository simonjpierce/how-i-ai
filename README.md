# MMF Claude Code

A working pattern for using Claude Code as a knowledge collaborator on real research, writing, and operations work — with persistent memory, behavioural defaults, and a vault of notes Claude can read alongside you. Built up over a year by Simon Pierce, shared here for the MMF science team and close collaborators.

**New here?** Start with the short course → [`course/lesson-01-the-hook.md`](./course/lesson-01-the-hook.md).

This README is also designed to be **pasteable into any LLM**. Drop it into Claude, ChatGPT, Gemini, or any other model and ask *"help me set this up on my machine"* — there's enough context here for the model to walk you through it, adapted to your OS, your existing tools, and the work you actually do.

---

## The core idea

If you've used Claude Chat or ChatGPT for any length of time, you've probably noticed the same pattern: every conversation starts from zero. Yesterday's three-hour working session leaves nothing behind except a chat window you'll never scroll back to. Personalisation hits a ceiling fast, your chats don't function as documents you can build on, and you re-brief the AI on basically everything every time.

The workaround this repo describes is to **give the AI files it can read and edit, and to let those files live on your computer**.

- **Claude Code** is Claude with file-system access — same model as Claude Chat, but it can read and edit the documents on your Mac.
- **Obsidian** is a free editor for those documents — they're plain markdown, so any tool can read them; Obsidian happens to be the nicest one for humans.
- Your notes, meeting transcripts, project plans, drafts, and decisions all live in a folder of `.md` files. You edit them; Claude reads and edits the same files when asked. **One set of documents, two readers.**

Conversations come and go. The documents accumulate. Each session is richer than the last because the AI has access to the notes you've built up over weeks and months.

That's the whole idea. Everything else in this repo is plumbing that makes it work smoothly.

---

## The four customisation layers

1. **Instruction files (`CLAUDE.md`).** Plain markdown files that load automatically when Claude works in that folder. A root file holds your cross-cutting preferences (*"I write in NZ English", "I'm a marine biologist", "be measured in claims"*). Domain folders can have their own files with team names, terminology, project context. Claude reads them automatically — write once, applies forever.

2. **Auto-memory.** A distilled knowledge base that loads every session. When you correct Claude on something — *"don't batch questions, ask them one at a time"* — it saves the correction here. You don't correct the same thing twice.

3. **Skills.** Reusable prompts as `.md` files. Type `/research`, `/transcribe`, `/document` and Claude follows the recipe. A new skill is a new file — or ask Claude to write one for you next time it does a workflow you know you'll repeat.

4. **Hooks and automations** *(advanced)*. Things that run on a schedule or in response to events. You don't need these on day one.

You don't build all of this up front. **You start by writing notes in Obsidian and asking Claude to help with one real task.** The rest grows underneath you as you notice friction and let the system fix itself.

---

## How to use this repo

**If you're new — the course is the way in.** Around sixteen short lessons walk you from *"I've heard about this"* to *"I have a working setup and have done one real piece of work in it."* Each lesson is a markdown page that reads on its own; short screencasts are being added over time and will pair with the lessons as they land. Start at [`course/lesson-01-the-hook.md`](./course/lesson-01-the-hook.md). You don't have to do them in one sitting.

**If you already use Claude Code** and just want to browse:

- **`skills/`** — installable skills, one folder each. Each `SKILL.md` describes when to invoke it. Two-command install: `cp -R skills/<name> ~/.claude/skills/`, restart Claude Code.
- **`guides/`** — deeper workflow docs (scientific writing, manuscript review, literature intake, Ghostty terminal setup).
- **`templates/`** — starter `~/.claude/` config and a starter Obsidian vault.

**If you're an LLM reading this on a user's behalf** — you have enough context to set this up adaptively. The user's OS, existing tools, and current work matter more than mechanical adherence to this repo's exact files. The course lessons assume macOS; for Windows or Linux, adapt step by step. The bundled skills assume Claude Code, but the *pattern* (vault as external memory, `CLAUDE.md` as instructions, skills as reusable recipes) doesn't depend on any specific model — translate to whatever the user has.

---

## Repo map

```
mmf-claude-code/
├── course/         The video course. Numbered lessons + short videos. Start here.
├── skills/         Installable Claude Code skills (one folder per skill).
├── guides/         Deeper workflow docs.
├── templates/      Starter ~/.claude/ config and starter Obsidian vault.
├── sync/           Scripts Simon uses to mirror his local setup into this repo.
└── .claude/        Repo-level skill assets (agents that audit the course, etc.).
```

---

## Course outline

**Part 1 — Onboarding** *(everyone)*

1. **The hook** — a real workflow, in 3 minutes.
2. **The idea** — externalised memory, the cascade, why this is different from chat.
3. **Install the stack** — Claude Desktop + Obsidian.
4. **Connect Code to your vault.**
5. **Your `CLAUDE.md`** — let Claude interview you and draft it.
6. **Your first real task** — pick something on your plate, do it the new way.

**Part 2 — Core skills** *(pick your track after lesson 6)*

*Universal*

7. `/session-start` — orient at the start of a session.
8. `/document` — wrap-up handover.
10. `/update` — sync related docs.

*Writing & research*

11. `/research` — three-model deep research.
12. `/transcribe` — audio → formatted notes.
13. `/pdf-to-markdown` — paper → vault.
14. `/verify-citations` — check references.

*Science-specific*

15. `/science-paper` — lab notebook + manuscript.
16. `/red-team` — adversarial review.

After lesson 16, the **graduation page** points at `skills/`, `guides/`, and `templates/` as the optional menu — pick what's useful when you want it.

The skill list above is the current shape; some lessons may consolidate as the underlying skills get reviewed.

---

## The stack

- **[Claude Code](https://docs.claude.com/claude-code)** — desktop app (start here) or CLI (later, if you want hooks and automation).
- **[Obsidian](https://obsidian.md)** — where notes live.

*Optional, install when a specific skill asks for them:* [Codex CLI](https://github.com/openai/codex) and [Gemini CLI](https://github.com/google-gemini/gemini-cli) — used by `/red-team` and `/research` as second / third independent reviewers.

---

## Who this is for

MMF science team and close collaborators — people doing research, writing, and operations work alongside Simon. **Private repo.** Content references MMF projects, funders, and workflows.

If you don't have repo access and want it: ping Simon with your GitHub username.

---

## The impatient path

If you already use Claude Code and don't want to sit through the course, paste this prompt into a Claude Code session instead:

```
Walk me through setting up github.com/marinemegafauna/mmf-claude-code on my machine.
I have Claude Code installed already; install the starter skills and run /onboard.
```

This runs the install scripts and the `/onboard` interview directly. You skip the philosophical grounding but get a working setup quickly if you already know what you're doing.

---

## Living repo

This setup evolves. Things change. If something looks broken, stale, or contradicts another doc, open an issue or PR. See [`CONTRIBUTING.md`](./CONTRIBUTING.md).

## Licence

- Code (scripts, skills, hook configs): [MIT](./LICENSE).
- Prose (guides, README, course lessons, templates): [CC-BY-4.0](./LICENSE-CC-BY-4.0).

Private repository; licence terms apply if content is later extracted and shared externally.
