# 00 — How Simon AIs

The overview document. If you read only one thing before touching any of this, read this. It covers how the whole setup fits together, why it looks the way it does, and where you can plug in without adopting all of it.

**Quick clarification, before anything else.** Despite the name, Claude Code isn't a tool just for coders. You use it with ordinary prose and ordinary questions — it's a chat-like interface that happens to also be able to read and edit files on your computer. The "Code" in the name refers to the fact that it *can* work with programming code if you need it to, not that programming is required. Most of the day-to-day work Simon does with it is reading and writing research notes, meeting transcripts, and manuscripts — not code.

## TL;DR

- **Claude Code** (Anthropic's tool) does the work. It runs either in the **Claude desktop app** or in a **terminal** (Simon uses Ghostty). Same tool, same capability — pick by comfort.
- **Obsidian** is the external memory. Every note, transcript, analysis, draft, decision, and project plan lives in a folder of plain markdown files. Claude reads the same files you do. One set of documents, two readers.
- **Skills, CLAUDE.md files, hooks, and memory** are the customisation layers. They let Claude start every session knowing who you are, what you're working on, and how you like to work — so you don't re-brief it from scratch each time.
- **The philosophy** — maximise memory, enable personalisation, customise continuously, keep improving the system. Every correction is remembered. Each session leaves the system better than it found it.

You can adopt any one layer without the others and still get value. The rest is additive.

## Why this exists

If you've been using Claude Chat or ChatGPT, you've probably noticed a pattern: every conversation starts from zero. Yesterday's great three-hour working session leaves nothing behind except a chat window you'll probably never scroll back to. The AI's memory of you is thin, whatever personalisation you've set up hits a ceiling fast, and your chats don't really function as documents you can edit and build on. You're always starting fresh.

Simon's workaround — the reason this whole setup exists — is to **give the AI files it can read and edit, and to let those files live on your computer**. Your notes, your projects, your research all live in a folder of plain-text (markdown) documents. You work on them normally, edit them in Obsidian (a free markdown editor and file-management app), and Claude reads and edits the same files when asked. Conversations come and go; the documents accumulate and improve over time.

Markdown is just plain text with light formatting — easy for you to read and edit, easy for AI to parse, and nothing locks you in to any one tool. The files are tiny (a whole research project might be a few hundred KB), live locally by default, and sync wherever you want (iCloud, Dropbox, Google Drive, mobile devices). The combined effect: your AI gets dramatically more useful because it has access to your actual knowledge, and your knowledge gets dramatically better because the AI can help you maintain it. That's the core trade — a little bit of setup in exchange for a working memory that doesn't reset.

## Two starting points

Claude Code has two frontends, both with the full feature set:

- **Claude desktop app** (Mac/Windows). If you're coming from Claude web/chat and the terminal feels foreign, start here. One-click install, familiar GUI, handles sign-in and configuration with minimal setup. You still get everything: files, tools, skills, CLAUDE.md, memory.
- **A terminal** — Simon uses [Ghostty](https://ghostty.org/). This is the more flexible frontend: easier integration with hooks, keyboard shortcuts, and other CLI tools (`git`, `jq`, `ffmpeg`, `whisper-cpp`, and so on). Simon's Ghostty config will be linked here once the repo is live.

Skills and CLAUDE.md files work identically in both frontends. Hooks (advanced) are easiest to configure via the terminal but not strictly required. Neither is "better" — choose by where you already spend time.

If you're a Claude web user who hasn't tried Claude Code yet, the lowest-friction migration is: install the desktop app, point it at your Obsidian vault (or wherever your working files live), and ask it to help with a real task. You don't need a custom setup on day one — the tool starts useful.

## Obsidian as external memory

The load-bearing idea in Simon's setup is that **Obsidian is the external memory for the AI, not just for Simon**.

Everything lives in a folder of markdown files. Meeting transcripts, research notes, manuscript drafts, grant applications, project plans, daily notes. Roughly 3,000 files across six domain folders (MMF, Photography, Life OS, Personal, AI Workflow, Archive). When Simon works on a task, Claude reads the same notes Simon reads. There's no separate "AI context folder"; there's one set of documents, and both human and AI consult it.

This is why markdown matters. If Obsidian shut down tomorrow, the vault is still just a folder of text files — any AI model can still read them. Lock-in is low; portability is high.

You don't need 3,000 files to start. You need **one folder that you actually write in, and a CLAUDE.md at its root describing what you do and how you work**. That's the minimum viable setup. Everything else grows from there.

## You don't have to build this alone

Before we get into the layers and the skills and the structure: this *looks* like a lot of machinery if you imagine having to build it all yourself up front. **You don't.**

Most of the setup is created by Claude *as you work*. You don't sit down on day one to write a perfect CLAUDE.md and ten skills. You start using Claude Code normally, on real work. When you mention a preference in conversation — "actually, can you always spell things in NZ English?" — ask Claude to add that to the CLAUDE.md file. When you correct Claude on something — "stop batching up multiple questions, ask them one at a time" — ask it to save that to memory so you don't have to correct it again. When you've walked through a workflow a couple of times and don't want to re-explain it the third time, ask Claude to turn it into a skill — it'll write the file for you.

You work normally; the system grows underneath you. The descriptions below are what Simon's setup has become after a year of that incremental growth — not a list of things you need to build before you can start.

## Five layers of context

The system works because Claude doesn't start each session from zero. It has five layers of context, from always-on to on-demand:

1. **Instruction files (CLAUDE.md)** — load automatically when Claude works in that directory tree. A global file for cross-cutting preferences (NZ/UK English, concise responses, no emoji). A vault-level file describing you and your work. Folder-level files for each domain, with context specific to that area (species names, staff names, project list, funder conventions). Claude reads the nearest CLAUDE.md automatically — you write it once, it applies forever.
2. **Auto-memory** — a distilled knowledge base that loads every session. Accumulates across conversations: tool quirks to avoid, workflow shortcuts that work, corrections given, infrastructure details. Correct Claude once ("don't batch questions — ask them one at a time") and the correction persists to every future session.
3. **Vault notes** — loaded on demand. Your markdown files are the primary knowledge store. Claude reads them as needed, guided by the current task.
4. **Semantic search** — Simon runs a local search engine (QMD) that indexes the entire vault with both keyword and vector search. Claude queries it by meaning ("how do we handle whale shark photo-ID in Mozambique?") and gets the relevant notes without needing to remember file paths. Optional but transformative at vault scale.
5. **Session continuity** — by default, each Claude Code conversation starts fresh; it doesn't remember the previous one. The workaround: at the end of each session, Claude writes a short summary to a file — what you did, what's still open, what was decided. The next session reads that file first and picks up where you left off. Paired with a decision log (non-obvious choices and why they were made, so past decisions don't get re-litigated in later sessions) and a friction log (things that were harder than expected, so recurring friction eventually gets fixed rather than silently endured).

All five serve double duty: useful to you as documentation, useful to Claude as context. **Same files, two readers.**

## Skills — the reusable building blocks

A **skill** is essentially a repeatable prompt — a markdown file at `~/.claude/skills/<name>/SKILL.md` that encodes a workflow Claude can invoke by name (you type `/<name>` at the prompt), and that you can improve over time as you notice what works and what doesn't. The easy way to end up with one: when you've done something with Claude a couple of times, ask it to "make this a skill" and it'll write the file for you. Don't worry about writing skills from scratch on day one.

Skills compose. A single project can use several: `/transcribe` for a meeting, `/update` afterwards to bring project notes current, `/document` to hand off at session end.

This repo's `skills/` directory has six skills you can copy into your own setup. Copy only the ones you'll actually use this week; come back for more when you hit a task that would benefit.

## Skills useful for scientists

The following skills are in this repo and are most useful for research work. Each has its own `SKILL.md` — the summaries below are just the hook.

- **`/science-paper`** — the most load-bearing research skill in Simon's setup. Structures analysis sessions around a **lab notebook file** (the authoritative record — data, methods, decisions, results, interpretation; detail is a feature) and a **manuscript file** drafted from the completed lab notebook. The two-file discipline keeps exploratory analysis and final writing separate, enforces that every analytical step is documented before proceeding to the next, and produces better drafts because the lab notebook has already captured the hard thinking. Two modes: *lab notebook* (activate at session start for interactive analysis) and *manuscript* (draft the paper from a completed notebook). See `skills/science-paper/SKILL.md`.

- **`/transcribe`** — meeting audio → speaker-labelled transcript with action items extracted. Uses Whisper locally (no data leaves your machine). Fits directly into a daily-note workflow.

- **`/red-team`** — critical review of an important document (grant, manuscript, report) by three independent reviewers (Claude subagent + Codex CLI + Gemini CLI). The reviewers don't share the drafting session's assumptions, so they catch what it missed.

- **`/verify-citations`** — manuscript reference check against Semantic Scholar, CrossRef, and OpenAlex. Flags fabricated papers (common in AI-assisted drafts), wrong authors, missing DOIs.

- **`/pdf-to-markdown`** — clean markdown extraction from PDFs for literature notes.

- **`/update`** — brings associated documents current after a work session (process docs, project notes, skills, cross-references). Prevents silent drift.

- **`/document`** — end-of-session handover. Writes the structured summary that tomorrow's session reads first.

Detailed guides for the highest-leverage workflows (lab notebook → manuscript pipeline, manuscript pre-submission review) live in `guides/`.

## Hooks and automations — when friction turns into infrastructure

Beyond skills, Simon's setup has two deeper layers that most users won't need on day one but should know exist:

- **Hooks** — shell commands that run automatically at specific moments (session start, file edit, Claude stops). Simon has ~14 hooks handling things like auto-committing vault changes after edits, opening created notes in Obsidian, and updating the terminal tab title to show the current task. Hooks live in `~/.claude/settings.json`. When you notice recurring friction, a hook is often the right fix.
- **Automations** — Claude Code running on a schedule without anyone at the keyboard. Simon has ~21 nightly/scheduled automations: a nightly workhorse that clears queued tasks, a morning briefing pipeline, an IDEA exploration loop, a self-improvement process that scans its own friction logs and proposes fixes. This is the deep end. Out of scope for v1 of this repo — ask Simon directly if you want to go there.

The general pattern: notice friction → fix it as a hook or automation → the friction goes away permanently. Every improvement is additive and persistent.

## Philosophy

Four pillars, in order of what matters most:

**Maximise memory.** The richer and better-structured Claude's context is, the less you repeat yourself, the more personalised the output, the less likely it is to produce generic AI sludge. Every correction, preference, workflow, and decision should live somewhere Claude can find — CLAUDE.md files, memory, process docs, project notes. Effort invested in documentation compounds.

**Enable personalisation.** Claude at baseline is competent but generic. Specific instructions — "I write in NZ English", "my staff are X, Y, Z", "when summarising research, match peer-reviewed marine biology style" — transform output quality. The investment is front-loaded: spend thirty minutes writing a good CLAUDE.md and every subsequent session benefits.

**Customise continuously.** The system is never "done." When you notice friction, write a hook. When a workflow stabilises after three uses, promote it to a skill. When a skill fails in a way you haven't seen before, update it *right there in the moment* so it doesn't catch you again. The system you use every day gets better slowly, day after day. The system you mean to improve later stays broken.

**Continuous system improvement.** The manual version of this is the habit of updating process docs at the moment of friction rather than "later". The automated version — the nightly self-improvement loop that scans friction logs and implements fixes autonomously — is further down the road and out of scope for v1.

One principle runs underneath all four: **don't delegate understanding.** The AI handles maintenance, first drafts, research synthesis, format conversion. You decide what matters, what's true, what gets published. The review is machine-generated; the priorities are yours.

## If you're a Claude user but not a Claude Code user yet

Migration path, easiest to fullest. Every step is optional and reversible:

1. **Keep using Claude web/chat for quick questions.** No migration needed for trivial things.
2. **Install the Claude desktop app.** Point it at your Obsidian vault or your main working folder. Ask it to help with a real task — a meeting transcript to format, a PDF to extract notes from, a draft to review.
3. **Write one CLAUDE.md** at the root of your working folder. Three or four paragraphs is enough to start: who you are, what you work on, how you like to write. Claude will read it automatically on every subsequent session.
4. **Copy one skill** from this repo into `~/.claude/skills/` and try it on something real (see `04-adopting-skills.md`).
5. **Iterate.** Add folder-level CLAUDE.md files as you work in different domains. Write your first skill when a workflow stabilises. Enable hooks when recurring friction annoys you enough.

The system is additive. No step depends on doing the next one.

## A practical note on voice input

For longer inputs — describing a project, documenting a decision, drafting a long message — Simon dictates rather than typing. As of early 2026, ChatGPT's voice transcription (available in the ChatGPT iOS and desktop apps) is still materially better than Claude's own voice transcription. The workflow: dictate into ChatGPT, copy the resulting text, paste it into Claude Code.

Use whichever voice-to-text tool produces the cleanest output for you at the time you read this. The point is just that for anything longer than a paragraph, speaking is usually faster than typing — and Claude Code accepts pasted text at any length.

## Where to go next

- **01 → 04** in this folder — the tactical onboarding sequence (install Claude Code, pick the right interface, run your first skill, adopt more skills).
- **`skills/`** — the SKILL.md for each of the six v1 skills, in detail.
- **`guides/`** — deeper workflow explainers (coming).
- **CONTRIBUTING.md** — the workflow for submitting your own improvements.

When in doubt: start by writing notes in Obsidian. The rest grows from that.
