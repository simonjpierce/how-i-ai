# Lesson 2 — The idea

The README gave you the short version. This is the longer one. No video for this lesson — it's reading. If you skipped here from lesson 1, that's fine; there's no setup yet.

The point of this lesson is to land the conceptual model. Most of the rest of the course is mechanical (clicks, installs, file paths). Those are easy. Knowing *why* you're doing them is what makes the system stick once you're past the install.

## A quick note before we start

Despite the name, **Claude Code isn't a tool just for coders.** It's a chat-like interface that happens to also be able to read and edit files on your computer. The "Code" in the name refers to the fact that it *can* work with programming code if you need it to, not that programming is required. Most of the day-to-day work Simon does with it is reading and writing research notes, meeting transcripts, manuscripts, and donor reports — not code.

If that already put you off, push past it. The tool is named badly. You're not the audience the name was chosen for.

## Why this setup exists

If you've used Claude Chat or ChatGPT for any length of time, you've probably noticed a pattern: every conversation starts from zero. Yesterday's three-hour working session leaves nothing behind except a chat window you'll never scroll back to. The AI's memory of you is thin, whatever personalisation you've set up hits a ceiling fast, and your chats don't really function as documents you can edit and build on. You're always starting fresh.

The workaround — the reason this whole setup exists — is to **give the AI files it can read and edit, and to let those files live on your computer**.

Your notes, your projects, your research all live in a folder of plain-text (markdown) documents. You work on them normally, edit them in Obsidian (a free markdown editor and file-management app), and Claude reads and edits the same files when asked. Conversations come and go; the documents accumulate and improve over time.

Markdown is plain text with light formatting — easy for you to read and edit, easy for AI to parse, and nothing locks you in to any one tool. The files are tiny (a whole research project might be a few hundred KB), live locally by default, and sync wherever you want (iCloud, Dropbox, Google Drive, mobile devices). The combined effect: your AI gets dramatically more useful because it has access to your actual knowledge, and your knowledge gets dramatically better because the AI can help you maintain it.

That's the core trade — a little bit of setup in exchange for a working memory that doesn't reset.

## Obsidian as external memory

The load-bearing idea is that **Obsidian is the external memory for the AI, not just for you**.

Everything lives in a folder of markdown files. Meeting transcripts, research notes, manuscript drafts, grant applications, project plans, daily notes. Simon's vault is roughly 3,000 files across six numbered domain folders:

```
00_INBOX            — Landing pad for daily notes, transcripts, clippings
01_PROJECTS        — Cross-cutting: roles, goals, priorities, reviews
02_MARINE MEGAFAUNA — MMF research, grants, operations
03_PLANET OCEAN     — Photography, websites, travel content
04_PERSONAL         — Finances, health, non-work
05_SYSTEM           — AI tooling, automation, process docs
06_ARCHIVE          — Completed or inactive
```

Numbered prefixes control sort order and keep domains visually separated. Standard Obsidian advice is to skip folders and rely on links and tags — that works if your notes are mostly one type of thing. Vaults that span research, photography, finances, team management, and personal life tend to need clearer domain boundaries.

Whatever structure you choose, when you work on a task, Claude reads the same notes you read. There's no separate "AI context folder"; there's one set of documents, and both human and AI consult it.

**You don't need 3,000 files to start.** You need one folder that you actually write in, and a `CLAUDE.md` at its root describing what you do and how you work. That's the minimum viable setup. Everything else grows from there.

## You don't have to build this alone

Before we go further into layers and skills and structure: this *looks* like a lot of machinery if you imagine having to build it all yourself up front. **You don't.**

Most of the setup is created by Claude *as you work*. You don't sit down on day one to write a perfect `CLAUDE.md` and ten skills.

- You start using Claude Code normally, on real work.
- When you mention a preference in conversation — *"actually, can you always spell things in NZ English?"* — ask Claude to add that to your `CLAUDE.md`.
- When you correct Claude on something — *"stop batching up multiple questions, ask them one at a time"* — ask it to save that to memory so you don't have to correct it again.
- When you've walked through a workflow a couple of times and don't want to re-explain it the third time, ask Claude to turn it into a skill. It'll write the file for you.

You work normally; the system grows underneath you. What's described in the rest of this lesson is what Simon's setup has become after a year of that incremental growth — not a list of things you need to build before you can start.

## What a session actually looks like

Less abstract: a typical morning might include several of these in sequence.

- *"Format this meeting transcript."* Claude reads the raw Whisper output, applies speaker labels and topic headings, extracts TODOs and IDEAs, and flags information that updates an existing project note.
- *"What's the current state of the Madagascar MPA paper?"* Claude searches the vault, reads the relevant project notes, and reports back: who's writing what, the submission deadline, outstanding items.
- *"Draft a response to this email about the ship-strike project."* Claude reads the project context and notes from the last meeting, then writes a draft you edit and send.
- *"Help me debug why the weekly review bundler is producing empty files."* Claude reads the script, checks the log output, identifies the issue, and either fixes it or walks you through the fix.

These aren't separate sessions — they happen in one. Context accumulates as the morning goes on, so by the third task Claude already knows what's been worked on that day. At the end of the session (or when the conversation gets long), the `/document` skill writes a structured summary back to the vault: what was done, decisions made, current state, open threads. Tomorrow's session reads that file first.

## Five layers of context

The system works because Claude doesn't start each session from zero. There are five layers of context, from always-on to on-demand:

1. **Instruction files (`CLAUDE.md`)** — load automatically when Claude works in that directory tree. A global file for cross-cutting preferences (NZ/UK English, concise responses, no emoji). A vault-level file describing you and your work. Folder-level files for each domain, with context specific to that area (species names, staff names, project list, funder conventions). Claude reads the nearest `CLAUDE.md` automatically — you write it once, it applies forever.

2. **Auto-memory** — a distilled knowledge base that loads every session. Accumulates across conversations: tool quirks to avoid, workflow shortcuts that work, corrections given, infrastructure details. Correct Claude once (*"don't batch questions — ask them one at a time"*) and the correction persists to every future session.

3. **Vault notes** — loaded on demand. Your markdown files are the primary knowledge store. Claude reads them as needed, guided by the current task.

4. **Semantic search** — Simon runs a local search engine (QMD) that indexes the entire vault with both keyword and vector search. Claude queries it by meaning (*"how do we handle whale shark photo-ID in Mozambique?"*) and gets the relevant notes without needing to remember file paths. Optional but transformative at vault scale.

5. **Session continuity** — by default, each Claude Code conversation starts fresh; it doesn't remember the previous one. The workaround: at the end of each session, Claude writes a short summary to a file — what you did, what's still open, what was decided. The next session reads that file first and picks up where you left off. Paired with a decision log (non-obvious choices and why they were made, so past decisions don't get re-litigated in later sessions) and a friction log (things that were harder than expected, so recurring friction eventually gets fixed rather than silently endured).

All five serve double duty: useful to you as documentation, useful to Claude as context. **Same files, two readers.**

## How `CLAUDE.md` files actually work

The single bullet above lumps `CLAUDE.md` into one item, but in practice how the cascade works is the most important customisation lever in the whole setup, so it's worth more space.

**You can have many `CLAUDE.md` files, not just one.** Claude reads the *nearest* one automatically, walking up the folder tree from wherever it's working. A vault-root `CLAUDE.md` applies to every session. A folder-level one only applies when Claude is working inside that folder. They stack: when working in a subfolder, Claude reads root + folder + (deeper) automatically, in that order. You don't pick which to load — the structure picks it for you.

Concretely: when Simon asks Claude to draft a grant report for an MMF project, Claude reads the **root `CLAUDE.md`** (NZ/UK English, no emoji, identity, writing voice), then **`02_MARINE MEGAFAUNA/CLAUDE.md`** (species naming conventions, current staff, funder-specific formatting, project list), then a **role note for "Executive Director — MMF"** (current strategic priorities). When he switches to editing a photography article, Claude picks up `03_PLANET OCEAN/CLAUDE.md` instead, with photography tone, gear references, and partner conventions. Same Claude session, automatically different context.

This is *why* the vault uses domain-based folders rather than the more common alternatives (PARA, lifecycle stages, or "skip folders entirely"). Mixing domains in a single folder breaks the cascade — there's no clean place for domain-specific context to live. Domain folders give you the layered behaviour for free.

**What goes at each level:**

- **Root `CLAUDE.md`** — cross-cutting preferences that apply to *all* your work: spelling and grammar conventions, identity (who you are, what you do), general tone, vault-wide naming. ~100–300 lines is comfortable.
- **Folder-level `CLAUDE.md`** — domain-specific context: key people in that area, terminology, conventions, current priorities. Keep under ~80 lines — this file reloads on every file read inside the folder. If it grows past that, link out to canonical notes instead of inlining content.
- **Role notes** *(advanced, optional)* — deepest layer, linked from folder `CLAUDE.md`. Holds context that changes often (active projects, near-term goals). A good setup can run on just root + folder files; role notes are a polish-pass.

**What does *not* belong in `CLAUDE.md`:**

- Content that changes more than monthly → point to a canonical note instead.
- Anything more than ~150 words that could live as a normal note.
- Information already visible in the vault structure (Claude can just read the files).
- Lists of tasks, decisions, or active state — those belong in daily notes or project files.

The `CLAUDE.md` layer is where you tell Claude *how* you work. The rest of the vault is *what* you're working on. Keep that line clean and the cascade stays useful.

## Skills — the reusable building blocks

A **skill** is essentially a repeatable prompt — a markdown file at `~/.claude/skills/<name>/SKILL.md` that encodes a workflow Claude can invoke by name (you type `/<name>` at the prompt), and that you can improve over time.

The easy way to end up with one: when you've done something with Claude a couple of times, ask it to "make this a skill" and it'll write the file for you. Don't worry about writing skills from scratch on day one.

Skills compose. A single project can use several: `/transcribe` for a meeting, `/update` afterwards to bring project notes current, `/document` to hand off at session end.

This repo's `skills/` directory ships a starter set. Copy only the ones you'll actually use this week; come back for more when you hit a task that would benefit. Part 2 of this course walks through them one at a time.

## Hooks and automations — when friction turns into infrastructure

Beyond skills, the setup has two deeper layers that most users won't need on day one but should know exist:

- **Hooks** — shell commands that run automatically at specific moments (session start, file edit, Claude stops). Simon has around 14 hooks handling things like auto-committing vault changes after edits, opening created notes in Obsidian, and updating the terminal tab title to show the current task. Hooks live in `~/.claude/settings.json`. When you notice recurring friction, a hook is often the right fix.

- **Automations** — Claude Code running on a schedule without anyone at the keyboard. Simon has around 21 nightly and scheduled automations: a nightly workhorse that clears queued tasks, a morning briefing pipeline, an IDEA exploration loop, a self-improvement process that scans its own friction logs and proposes fixes. This is the deep end. Out of scope for v1 of this repo — ask Simon directly if you want to go there.

The general pattern: notice friction → fix it as a hook or automation → the friction goes away permanently. Every improvement is additive and persistent.

## Philosophy

Four pillars, in order of what matters most:

**Maximise memory.** The richer and better-structured Claude's context is, the less you repeat yourself, the more personalised the output, the less likely it is to produce generic AI sludge. Every correction, preference, workflow, and decision should live somewhere Claude can find — `CLAUDE.md` files, memory, process docs, project notes. Effort invested in documentation compounds.

**Enable personalisation.** Claude at baseline is competent but generic. Specific instructions — *"I write in NZ English", "my staff are X, Y, Z", "when summarising research, match peer-reviewed marine biology style"* — transform output quality. The investment is front-loaded: spend thirty minutes writing a good `CLAUDE.md` and every subsequent session benefits.

**Customise continuously.** The system is never "done." When you notice friction, write a hook. When a workflow stabilises after three uses, promote it to a skill. When a skill fails in a way you haven't seen before, update it *right there in the moment* so it doesn't catch you again. The system you use every day gets better slowly, day after day. The system you mean to improve later stays broken.

**Continuous system improvement.** The manual version is the habit of updating process docs at the moment of friction rather than "later". The automated version — the nightly self-improvement loop that scans friction logs and implements fixes autonomously — is further down the road and out of scope for v1.

One principle runs underneath all four: **don't delegate understanding.** The AI handles maintenance, first drafts, research synthesis, format conversion. *You* decide what matters, what's true, what gets published. The review is machine-generated; the priorities are yours.

## Where it works, and where it doesn't

The tasks Claude handles best are formatting and conversion — meeting transcripts, PDFs to markdown, raw data into structured notes. Anything where the information already exists and just needs reorganising. It's also strong on vault maintenance: finding stale notes, cross-referencing across files, proposing updates after meetings. The kind of work that's important but never urgent enough to do by hand.

First drafts are the highest-value use. Because Claude has access to the vault — past writing, project notes, voice references — it's synthesising from your own material rather than generating from nothing. Research synthesis works the same way: a useful triage layer over a large body of sources, not a replacement for reading the papers.

Code is in scope, even if you're not a developer. Simon isn't a software engineer, but maintains a fair amount of Python and shell scripting for the automations described above. Claude writes most of it and fixes it when it breaks. You don't need to be able to write the code from memory — only to understand what it does and notice when it's wrong.

What Claude *can't* do is have the idea in the first place. Ideas come from daily notes, conversations, walks, time underwater. The machine explores them; it doesn't generate them. AI-written prose also has tells — important pieces should be edited and run through a voice check before publishing. The AI does the legwork; you make the calls.

## If you're already using Claude Chat

The migration path is short, and every step is optional and reversible:

1. **Keep using Claude web/chat for quick questions.** No migration needed for trivial things.
2. **Install the Claude Desktop app** and switch to the Code tab. Point it at your Obsidian vault or whatever folder you write in. Ask it to help with a real task — a meeting transcript to format, a PDF to extract notes from, a draft to review.
3. **Write one `CLAUDE.md`** at the root of your working folder. Three or four paragraphs is enough to start: who you are, what you work on, how you like to write. Claude will read it automatically on every subsequent session.
4. **Adopt one skill** from this repo and try it on something real.
5. **Iterate.** Add folder-level `CLAUDE.md` files as you work in different domains. Write your first skill when a workflow stabilises. Enable hooks when recurring friction annoys you enough.

The rest of the course walks you through steps 2–4. Step 5 is the rest of your life with the system.

## What's next

[Lesson 3 — Install the stack](./lesson-03-install-the-stack.md). Claude Desktop + Obsidian, on your Mac.
