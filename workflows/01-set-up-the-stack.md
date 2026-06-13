# Set up the stack

The one thing you do before anything else: get the foundation running — somewhere to keep your notes (Obsidian), and an AI that can read and write those same notes (Claude Code). Everything else in this repo sits on top of this.

This is an idea file. Paste it into Claude Code and it'll walk you through the setup on your machine, adapted to your operating system and what you already have installed. The steps below are *the maintainer's actual setup* — copy it, or let your AI suggest equivalents.

## The core idea

Two things are essential — and that's genuinely it:

1. **Obsidian** — a free app for keeping notes on your computer. Your notes are just plain text files (markdown) in a folder; Obsidian is the friendly window onto them — it renders everything cleanly and shows the links between notes. That folder of notes is your **vault**, and it's *yours*: plain files on your own disk, nothing proprietary. → **[obsidian.md](https://obsidian.md)**

2. **An AI that can read and write those files.** This is the part most people are missing, and it's the whole unlock. The ChatGPT or Claude you use in a browser can only *talk back* — it can't touch your files. But the same models come in a more capable form that can actually open, read, and edit the files on your computer and take actions for you. For Claude — the tool this guide is written around — that's the difference between **Claude Chat** (conversation only) and **Claude Code** (reads and writes your files, runs tasks for you). The file-capable form, not a browser chatbot, is what makes everything else work. (OpenAI's **Codex** is the equivalent if you'd rather use that; the workflows are plain descriptions, so they adapt.) → **[Claude Code](https://docs.claude.com/claude-code)**

Two small files then do a lot of the quiet work, loading automatically every time the AI starts: a **standing-instructions file** (who you are, how you like to work, what to call things) and a **memory file** (what the AI has learned about you over time). You don't author these — the AI builds and updates them as you go.

Everything else — a way to talk instead of type, a second AI for cross-checks — is an add-on you bring in later (all covered below), not a day-one requirement.

## The pieces, in a bit more detail

- **Obsidian** — the editor. Free. Point it at a folder and that folder becomes your vault; back it up however you back up anything else (this setup uses git + a cloud sync). → [obsidian.md](https://obsidian.md)
- **Claude Code** — the AI with file access, and the maintainer's home base. **For most people the friendliest way in is the Claude desktop app, using its Claude Code tab** — no terminal needed. → [Claude Code](https://docs.claude.com/claude-code) · [download the Claude desktop app](https://claude.ai/download). The maintainer himself runs it in a **terminal** (a terminal app called [Ghostty](https://ghostty.org)), partly out of habit — but there's a real reason a power user might too: the terminal version is what unlocks the automation layer (hooks, scheduled overnight runs, extra integrations) that the *advanced* workflows later in this repo lean on. So start in the desktop app; reach for the terminal if and when you want that automation. Either does the everyday work identically.
- **Codex** *(the maintainer's second model)* — OpenAI's equivalent of Claude Code. The maintainer runs **Claude Code** as his everyday interface and keeps **Codex** on hand as an independent *second* model for cross-checks ("is this analysis sound?", "review this plan") — two models catching each other's mistakes beats one. (You could run Codex as your main agent instead, if you prefer it; the workflows adapt either way.) → [Codex](https://github.com/openai/codex)
- **A voice interface** *(the maintainer's single biggest speed-up)* — speaking is far faster than typing for giving the AI detailed context, so almost all detailed input here is dictated rather than typed. The simplest way: if you're in the **Claude desktop app**, press and hold the **microphone button** in the prompt area, speak, and release — your words go straight in, nothing to copy or paste. (On a Mac you can also press **Fn** twice to dictate into any text field.) One upgrade worth knowing: ChatGPT's transcription is noticeably more accurate in the maintainer's experience, so for long, detailed dictation he speaks into ChatGPT's mic, lets it transcribe, and pastes the clean text across — try whichever transcribes *you* best. (Voice is on the cheaper plans too — no premium subscription needed to start.)
- **The standing-instructions file** (`CLAUDE.md`) — loaded every session. It tells the AI who you are, how you work, your spelling and tone, where things live. The AI drafts a starter version with you during setup.
- **The memory file** (`MEMORY.md`) — also loaded every session. The durable record of what the AI has learned about working with you, so the lessons don't reset.

## Setting it up

The fastest path: paste this whole file into Claude Code and ask it to walk you through installing the tools, creating the vault, and writing a starter standing-instructions file and memory file — all built with you, adapted to your work. Even simpler: point your AI at the whole repo — `github.com/simonjpierce/how-i-ai` — and ask it to read it and set you up. That hands it this page plus every workflow downstream at once, so it understands where you're heading rather than just the first step.

**You don't have to write any of this yourself.** The AI interviews you — and the easiest way to answer is by voice (the mic methods above): just talk, stream-of-consciousness, with as much detail as comes to mind. You don't need to be careful or organised about it — a rambling monologue is exactly right. The AI pulls out what it needs, asks follow-up questions to fill the gaps, and writes the files for you. Expect setup to take a little while: it's doing real work behind the scenes, and the context you give it now is what makes the whole system effective later.

**Let it act without nagging you.** Before it starts, switch your AI to its most autonomous permission mode so it can install tools, create the vault, and write files without stopping for approval at every step — in the Claude desktop app, press **Shift-Tab** to cycle until it shows **Auto**. Otherwise setup stalls on a wall of yes/no prompts and feels broken when it isn't. You can dial it back any time.

The order that works: install the editor → create the vault folder → connect the AI to it → write a short standing-instructions file (you can grow it over time) → do one small real task to feel the loop. Don't try to set up everything at once.

## Which subscriptions (start cheap, upgrade only when you hit real limits)

You don't need the top tier of anything to begin — find your *actual* limits before paying for more.

- **ChatGPT** — the standard paid plan (around US$20/month) already includes the voice and transcription and a lot of capability; start there. The maintainer runs a higher tier, because he leans on voice heavily *and* uses Codex (OpenAI's coding agent) a lot — worth it at that volume, but only once the cheaper plan's limits actually start to bite.
- **Claude Code** — the entry plan (around US$20/month) is, honestly, fairly limiting for a serious volume of work. Most people doing a lot with it settle on the **mid plan (around US$100/month)**, which is the sweet spot — that's where the maintainer would point most people first. The top plan (around US$200/month) is only worth it if you're genuinely hitting the mid plan's limits.

*(Plan names and prices change — treat these as a rough guide and check current pricing.)*

## What this does *not* require

It doesn't require the terminal, a specific AI vendor, or any particular operating system. It doesn't require you to be technical — the AI does the fiddly parts if you let it. And it doesn't require committing to the whole system up front: the foundation is enough to be useful on day one, and you add the rest (the workflows) when a need shows up.

## Note

This is one concrete setup, not the only one. Swap any piece for an equivalent you prefer — a different editor, a different AI, a different way to back things up. The essential shape is unchanged: *files in a folder, an editor for you, an AI that can edit the same files.* Paste this to your AI and build the version that fits your machine.

---

## Next step

**→ [Teach it who you are](./02-teach-it-who-you-are.md)** — the onboarding interview: import what your current chatbot already knows about you, then let the AI interview you to fill in your standing-instructions file and set up your vault folders.
