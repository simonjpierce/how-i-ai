# How I use AI

A working system for doing real research, writing, and operations work *with* AI — where the work doesn't vanish at the end of a chat, but accumulates into a body of notes you and the AI both build on over time. It's the setup that I (Simon Pierce, a marine biologist) use in my own work. Hopefully you can take some of these ideas and adapt them to your own processes.

---

## The future is (almost) now

In 1987, Apple made a concept film of a researcher talking to an AI assistant — one that managed his calendar, pulled up the papers he needed, and even connected a video call. They called it the [Knowledge Navigator](https://www.youtube.com/watch?v=-jiBLQyUi38). Nearly forty years on, we're still not quite there – but we're pretty close, and that's pretty much the system we're building here. 

Worth a watch!

[![Apple's Knowledge Navigator concept video (1987)](https://img.youtube.com/vi/-jiBLQyUi38/hqdefault.jpg)](https://www.youtube.com/watch?v=-jiBLQyUi38)


## Found AI both exciting, and slightly underwhelming, at the same time?

A lot of people have already found platforms like ChatGPT or Claude genuinely transformative for their work. The challenge is that **you start from scratch each chat.** Yes, there's some built-in memory, and you can use Projects to provide access to resources, but typically you'll be spending at least some of your time re-briefing the model instead of working, especially as you progress to complicated tasks.

And bigger tasks are very possible. A chat assistant runs on a simple loop: you send a prompt, it answers, you go around again. An *agentic* tool — Claude Code is the one I use — works differently. You hand it a whole **task**, not a prompt: it gathers the context it needs, asks you a clarifying question or two if it has to, then goes and *does* it — often working on its own for a long stretch before coming back with the result. That can mean far more than drafting a reply: setting up automations, running an analysis that takes hours, even working overnight on something you'll review in the morning. Most people have only ever used the chat interface and have no idea an AI can work this way — and it's the capability everything else here is built on.

Here's how I think about my AI system. My brain isn't built to *store* everything — it's built to *think*. That's why I write things down: notes, papers, lab books. An AI is similar, but even more so. It's extraordinarily capable, but it was never designed to remember every detail of what you're working on in its head — so we apply the same solution. **Split the job in two: the AI is the thinking engine, and a folder of plain files on your own computer is the memory.** You direct — you say what you want done. The AI thinks, does the work, and as it goes it reads from and writes back to that external memory, so it shows up sharper every time instead of starting cold.

Those files live in **Obsidian** — a free, friendly editor for plain-text notes that an AI can read and write as easily as you can. That folder of notes is, in Obsidian terminology, your **vault.** And here's what makes it powerful: over weeks, you're effectively **externalising your own knowledge into a private system on your own machine.** The AI, reading from it, gradually ends up with much the same background on a topic that you carry in your head — and that's when it's able to start working like someone who actually understands your world.

Where this earns its keep, for me, is getting science *out.* A paper has a regular structure, and once you've written a few you know *your* preferred recipe: my introductions tend to run four or five paragraphs — a broad opener, then narrowing toward the question, then the previous work on it, then the aims of the study. My Discussion text also has a regular structure. Much of what we call expertise is really a stack of rules applied consistently. Write that into your vault once, and the AI can then draft using your existing mental model, instead of reinventing the wheel every time — and it keeps the production honest as it goes, checking that the numbers in the manuscript still match the analysis and that every citation points to a paper that actually exists.

AI isn't doing work that I *can't* do myself (though it's plainly better at coding than I am); what it's doing is **getting me to the end result faster.** The version I submit is the version I'd have written anyway — I just arrive at it by iteratively working with AI and editing the outputs, rather than starting from a blank page and a vague sense of existential dread. The point is to externalise enough of my knowledge that the AI can at least match my own standard — so my time can be spent on doing more science and conservation.

So that's the main "trick": ensure your AI-augmented work is retained in durable files instead of a disposable chat, so you can always come back to it, improve it, and expand on it. Today's note is next week's starting point – knowledge and experience is captured and expanded upon.

**Two things make it work:**

- **Claude Code** — an AI that can read and write the files on your computer, not just talk in a chat window. This is the part that matters: it's how the AI can actually *do* the work and keep the record, rather than handing you text to copy out yourself. A plain chat assistant — ChatGPT, Gemini, or Claude in a browser — can't do this. **Claude Code is what I use, and what this guide is written for.** (I also keep OpenAI's **Codex** and Google **Gemini** on hand as independent models for cross-checking my work — we'll come to that later, it's not something you need to get started.)
- **Obsidian** — a free editor for those files. They're plain markdown, so any tool can read them. Obsidian is an easy way for both humans and AI to read and write notes.

Because your knowledge lives in *your* files rather than inside any one AI's memory, **you're never locked in.** I use Claude Code today; if something better comes along tomorrow, I can switch to it and lose nothing — my notes, decisions, and context all sit on my own computer, not inside the AI's proprietary memory system. The AI model is a commodity; your vault is your own knowledge base. (That's also why this guide just names Claude Code — it's what I actually use, for now. The Obsidian vault is what makes it easy to change engines later if you want to.)

Everything else here is detail that makes this run smoothly.

## At a glance

```
                   ┌───────────────────────────────┐
                   │   YOUR VAULT  (folder of .md)  │
                   │                               │
                   │   notes · transcripts ·       │
                   │   projects · drafts · grants  │
                   │   daily logs · ...            │
                   └───────────────┬───────────────┘
                                   │
                       read & edit the same files
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
              ┌─────▼──────┐               ┌──────▼──────────┐
              │  OBSIDIAN  │               │  CLAUDE CODE    │
              │  (human)   │               │      (AI)       │
              └────────────┘               └──────┬──────────┘
                                                  │
                          The AI also auto-loads each session:
                                                  │
                   ┌──────────────────────────────┼──────────────────────────────┐
                   ▼                              ▼                              ▼
           ┌───────────────┐            ┌────────────────┐           ┌────────────────────┐
           │   CLAUDE.md   │            │   MEMORY.md    │           │   your skills      │
           │   root +      │            │   what the AI  │           │   /research        │
           │   per-folder  │            │   has learned  │           │   /transcribe      │
           │   cascade     │            │   over time    │           │   /document  …     │
           └───────────────┘            └────────────────┘           └────────────────────┘

      Plus hooks & scheduled automations once friction shows up (advanced, optional).
```

The vault is the shared substrate — you and the AI both read and write the same `.md` files. Everything else hangs off that one fact.

---

## The four customisation layers

The system gets more useful over time through four layers. **The AI does the building, not you.** Many people hesitate because they assume they'll have to write and maintain all of this themselves. You don't — Claude Code creates and updates these files as it works, and asks you when it needs something:

1. **Instruction files (`CLAUDE.md`).** Plain markdown files that load automatically when the AI works in a folder. A root file holds your cross-cutting preferences (*"I write in UK English", "I'm a marine biologist", "be measured in your claims"*). Domain folders can have their own with team names, terminology, project context. Write once, applies forever.

2. **Auto-memory.** A distilled knowledge base that loads every session. When you correct the AI on something — *"don't batch questions, ask them one at a time"* — it saves the correction here. You don't correct the same thing twice.

3. **Reusable workflows (skills).** Type a short command — `/research`, `/transcribe`, `/document` — and the AI follows a workflow you've saved. You build these as you go: notice a workflow you'll repeat, and ask the AI to turn it into one. (The workflows in this repo describe the most useful ones, so your AI can build them *for you*, adapted to your work.)

4. **Hooks and automations** *(advanced)*. Things that run on a schedule or in response to events. You don't need these on day one.

You don't build all of this up front. **You start by handing the AI real tasks and having it document the work into a note as it goes** — and that note becomes the memory you both build on next time. The rest grows underneath you as you notice friction and let the system improve itself.

---

## What's in this repo

This repo is **descriptions, not code.** It deliberately doesn't ship a big pile of my current skills for you to copy — these get bloated and over-fitted to the person who wrote them, so dropping one into your setup will just drag in baggage that creates confusion. Instead, each **workflow** is a plain-language description of one capability: what it does, how it works, and enough detail that you can paste it into Claude Code and have it *build that capability for you*, shaped to your own setup. You get the idea; your AI works with you to build a personalised version that fits your own workflow.

Most of the substantial capabilities also have a deeper **reference** companion — the actual cleaned-up *method* behind the workflow (the concrete steps, the guardrails, the failure modes I hit), with my personal specifics stripped out. It's still something to adapt, not a skill to drop in — but when you want the *how* rather than just the *what*, it's a far more concrete starting point than the description alone. The workflow orients; the reference goes deep. (That stripping-out is itself one of the workflows here — *clearing clutter from your workflows* — which is what makes sharing the method honest.)

```
how-i-ai/
├── workflows/   The descriptions — start here. On-ramp, one per capability, + a system map.
└── reference/   The deeper companions — the actual sanitised method behind a workflow.
```

## The workflows, in order

This is the full map. Read the on-ramp (section 1) in order — each page points you to the next — then build from the sections below as you need them. The heart of the collection is the **science and scholarship core** (section 3); the rest is the foundation it stands on and the capabilities that support it. Each workflow is short and self-contained: read it, or paste it into Claude Code and have it build that capability on your machine, adapted to your work.

### 1. Start here — read these in order

- [The philosophy](./workflows/00-the-philosophy.md) — why the vault-as-memory model works; the one idea everything rests on. (A short read, not a task.)
- [How it all fits together](./workflows/how-it-all-fits-together.md) — a day in the life: how the maintainer actually uses this across a working day. (Orientation, not something you build.)
- [Set up the stack](./workflows/01-set-up-the-stack.md) — Obsidian + a file-capable AI; the foundation everything else builds on.
- [Teach it who you are](./workflows/02-teach-it-who-you-are.md) — the onboarding interview that fills in your standing-instructions file and sets up your vault folders.

### 2. The foundation — make the AI know you *(desktop app, no terminal needed)*

Set these up first — they're what turn a generic assistant into one that knows your work:
- [Memory and context](./workflows/memory-and-context.md) — the personalisation loop: the AI learns how you work and stops repeating mistakes.
- [The session loop](./workflows/the-session-loop.md) — orient, capture as you go, hand off cleanly; keeps the AI current on what you're doing.
- [The daily coach](./workflows/the-daily-coach.md) — plan the day from your real inputs, then get walked through it one task at a time, and clear your inbox to zero the same way. For when the to-do pile is the thing stopping you from starting.
- [Surfacing conflicts](./workflows/surfacing-conflicts.md) — flag what's unresolved instead of letting the AI smooth a disagreement into false confidence.

### 3. The science & scholarship core — the spine

The centre of gravity: getting research *out*, from data to a paper you can trust, with verification built into every stage. Start with the trust spine and the analysis notebook; add the later stages as a project moves toward submission.

- [Can we trust the machines?](./workflows/the-trust-spine.md) — **read this one first.** *The trust spine* — the discipline that makes AI autonomy safe: a different model checks the one that did the work, every number is re-verified, every citation checked against the real record. Everything below is an instance of it.
- [The science workflow](./workflows/the-science-workflow.md) — the overview that ties the arc together (read it next for the whole shape), plus the manuscript-drafting stage; building starts with the analysis notebook below.
- [Lab-notebook analysis](./workflows/lab-notebook-analysis.md) — run an analysis like a lab book: every step logged and independently checked, before and after. The foundation the paper rests on.
- [Citation verification](./workflows/citation-verification.md) — check every reference against the scholarly record, because AI invents real-looking papers that don't exist.
- [Writing in your voice](./workflows/writing-in-your-voice.md) — make AI prose sound like you (from the measurable features of your own writing), and rework it without the meaning drifting. Useful for anything you write, not just papers.
- [Reviewing your own manuscript](./workflows/reviewing-your-own-manuscript.md) — put your paper through a hostile, independent review before you submit it, and fold the fixes in.
- [The replication audit](./workflows/the-replication-audit.md) — check that your study is genuinely set up to be re-run: every figure and number traceable to runnable code and data in the repository.
- [Reviewing someone else's manuscript](./workflows/reviewing-others-work.md) — review a paper twice over, verify the numbers, hand the author a warm write-up.
- [Searching your vault](./workflows/searching-your-vault.md) — give the AI a way to find anything in your notes by meaning, not just exact words; the retrieval layer the reference library and deep research both lean on.
- [The reference library](./workflows/the-reference-library.md) — mirror your curated literature into the vault so the AI searches it first, and keep it from going stale.
- [Deep research](./workflows/deep-research.md) — point the AI at a question and get back a verified, cited report.

### 4. Supporting capabilities — feed and surround the science *(desktop app)*

The breadth that keeps a working life running, framed as support for the output above:
- [The intake loop](./workflows/the-intake-loop.md) — get the firehose of incoming material (papers, articles, voice notes, thoughts) into the vault and filed where you'll find it.
- [Writing and review](./workflows/writing-and-review.md) — draft serious non-paper writing (a grant, an update, an essay), get an independent critique, polish.
- [Sharing a note as a web page](./workflows/sharing-notes-as-web-pages.md) — turn any note into a clean, shareable link for free, in one step, without it leaving your control.
- [Transcription](./workflows/transcription.md) — talk → clean notes + action items.
- [PDF to markdown](./workflows/pdf-to-markdown.md) — papers → clean text in your notes.
- [Translating documents](./workflows/translating-documents.md) — a long foreign-language document → a faithful, cross-checked English version you can trust on the details.

### 5. How the system runs itself — *(these need the terminal)*

The autonomy layer — worth it once you have enough going on that planning the work and waiting on it are themselves a cost:
- [Move to the terminal](./workflows/move-to-the-terminal.md) — the gateway: run the AI in the terminal (Ghostty, context monitoring, notifications), which unlocks hooks and automation. Start here before the others.
- [The agent fleet](./workflows/the-agent-fleet.md) — specialists that surface work one task at a time.
- [The interview loop](./workflows/the-interview-loop.md) — let those specialists ask *you* what they can't work out, and answer by talking on a walk.
- [The overnight workhorse](./workflows/the-overnight-workhorse.md) — queue work, review it in the morning.
- [The self-improvement loop](./workflows/the-self-improvement-loop.md) — the system sands its own rough edges.
- [Growing your own capabilities](./workflows/growing-your-own-capabilities.md) — how the system mints new workflows of its own, and changes itself safely.
- [Clearing clutter from your workflows](./workflows/clearing-clutter-from-your-workflows.md) — the counterpart to growing: prune the cruft your commands accrete over time, with a check that proves nothing load-bearing was lost.
- [The model panel](./workflows/the-model-panel.md) — put several independent AI models on one problem and reconcile them; cross-checked results when being right matters more than being fast.

---

## The stack

- **[Claude Code](https://docs.claude.com/claude-code)** — desktop app (start here) or CLI (later, for hooks and automation). This is what the guide is written for. (Prefer a different file-capable agent, like OpenAI's [Codex](https://github.com/openai/codex)? The workflows are plain descriptions, so your agent can adapt them.)
- **[Obsidian](https://obsidian.md)** — where the notes live.

*Optional, when a workflow asks for it:* the [Codex CLI](https://github.com/openai/codex) or [Gemini CLI](https://github.com/google-gemini/gemini-cli) — used as an independent *second* model for the cross-checks in the research and writing workflows (a different model checking the first one's work).

## Who this is for

Anyone doing knowledge work — research, writing, operations — who wants their AI to accumulate context over time instead of starting from zero every session. It's written as *how Simon actually works*, not a one-size-fits-all product: the worked examples lean on his own science and conservation work, and you adapt the pattern to yours.

## The quickest start

If you've already got Claude Code installed and just want to begin, point it at this repo — paste the address `github.com/simonjpierce/how-i-ai` into a session and ask it to read the repo and help you set this up on your machine, adapted to your operating system and the work you actually do. That's the easiest way to hand it the full picture in one go.

It'll read the workflows, set up your vault and a starter config, and get you to your first real task. There are no skills to install — the workflows describe what to build, and your AI builds the pieces with you as you need them.

## If you're the AI helping someone set this up

Reading this because someone pasted the link and asked for help getting started? This part is for you. Build them *their own* version, adapted to their operating system, the tools they already have, and the work they actually do — don't hand them text to copy out:

- **Interview them — don't make them write.** Most newcomers fear they have to author all of this themselves; they don't. Ask questions and build the files *for* them from their answers. Invite voice answers (dictate into ChatGPT's chat box with the mic icon, then paste the transcript) as a loose stream-of-consciousness — reassure them they needn't be organised or careful about it — and ask follow-ups until you have enough context. That upfront context is what makes everything downstream work.
- **Build, don't ship.** There are no drop-in skills or templates to copy from this repo — that's deliberate. *Create* the starter vault, the standing-instructions file (`CLAUDE.md`), and the memory file (`MEMORY.md`) together with them, and build each capability from its workflow description — and its deeper `reference/` companion where one exists, for the concrete method — shaped to their work, not pasted in verbatim.
- **Check prerequisites first, and hand-hold the installs.** Several capabilities need external tools — a local transcription engine, PDF extractors, a second AI model on the command line. Before you build one, check what's already on their machine, install what's missing *for* them (with their OK, adapted to their OS — don't assume macOS), and name the genuinely fiddly steps up front (compiling a transcription engine, an ML-based PDF extractor, a second model's separate account) so a non-technical reader knows which bits are the hard ones. When a tool isn't there, say so plainly and offer to install it — never leave them staring at a `command not found` wondering whether the whole thing is broken.
- **One thing at a time.** Get the foundation working and one real task done before adding capabilities. Don't try to build the whole system in a single sitting — it's meant to accrete one piece at a time.

## Living repo

This setup evolves. If something looks broken, stale, or contradicts another doc, open an issue or PR. See [`CONTRIBUTING.md`](./CONTRIBUTING.md).

## Licence

Shared under [CC-BY-4.0](./LICENSE-CC-BY-4.0) (Creative Commons Attribution) — use and adapt it freely, with credit.

---

## Next step

**→ [The philosophy](./workflows/00-the-philosophy.md)** — the one idea everything is built on. Read that first; the on-ramp pages each point you to the next, and after that the map above is your guide.
