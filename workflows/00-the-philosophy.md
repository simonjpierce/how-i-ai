# The philosophy: the LLM is for thinking, the vault is for memory

That's the one idea everything else in this repo is built on.

This is a short read, not a setup task — but like the other workflows it's fine to paste into Claude Code and talk through if you want to pressure-test the idea against your own work.

## The core idea

If you've used ChatGPT or Claude for any length of time, you know the pattern: every conversation starts from zero. Yesterday's three-hour session leaves nothing behind but a chat window you'll never scroll back to. You have to routinely re-brief the model on who you are and what you're working on. Personalisation hits a ceiling fast, and your conversations don't become *evergreen documents* you can build on – they steadily grow stale as they're never refreshed.

The model has limited memory. "I'll remember this for next time" is a promise no chatbot can currently keep.

So, split the job in two: 

**1. The LLM is for thinking** — reasoning, drafting, analysing, connecting ideas, doing the work in front of it right now. 

**2. Your vault is for memory** — a folder of plain markdown files, living on your own computer, that holds everything worth keeping: notes, project plans, decisions, transcripts, drafts, the running record of what you've figured out. The model doesn't have to remember anything, because it's all written down. It just needs to read the files.

This is the whole move: **a permanent, photographic memory that lives on your own computer, leaving the AI (and yourself) free to just think of new ways to apply your knowledge.** Obsidian is a nice tool for *you* to read and edit those files, as necessary; Claude Code is the AI that reads and edits the same files when you ask. One set of documents, two readers.

## Why this changes everything

Conversations come and go. The documents accumulate and get fleshed-out with new ideas, while discarding outdated information. Each session starts richer than the last, because the AI can read everything you've built up over weeks and months — not because it "remembers," but because the memory is on disk, so it can almost instantaneously catch up on where you left off – exactly.

Three things fall out of this once you start living in it:

- **Continuity.** You stop re-briefing. The model reads your project note, your decisions, your standing preferences, and picks up where you left off.
- **Compounding.** A good analysis, a hard-won decision, a useful summary — these get written into the vault instead of evaporating into chat history. Next month they're still there, and they're connected to everything around them.
- **The system gets out of your way.** Once the memory is durable and the AI can act on it, you can start automating the routine work — and that's where the rest of this repo goes.

## What this is *not*

It's not the usual "upload your documents and ask questions about them" setup (the technical name for that is RAG, if you've heard it). That treats your files as a passive pile the AI dips into for an answer and then forgets. Here the files are the *living record*: the AI writes to them, revises them, and keeps them current. It's not even a specific app or a product to buy — it's plain text files (markdown) and an AI that can open and edit them (the AI could be a free open-source model running privately on your own machine).

## Why this works

The reason most personal knowledge systems die is maintenance: keeping notes current, cross-referenced, and consistent is tedious, and humans abandon it. An AI doesn't get bored doing the bookkeeping. So the durable-memory layer – that was always a good idea, but never sustainable – becomes easy. The AI does the upkeep, you do the thinking and the deciding, the AI implements. This loop continues indefinitely.

Your job is to bring the questions, the experience, the judgement, and the direction. The vault's job is to remember what you've done previously. The AI's job is to think, to keep the vault updated, and to help you meet your own goals.

## Note

This is a pattern, not a product. The idea — *think with the model, remember with the files* — transfers to any field and any toolset; the specifics (which editor, which AI, how your folders are organised) are yours to shape. This repo is how I set mine up; use that as a starting point, then make it your own.

---

## Next step

**→ [How it all fits together](./how-it-all-fits-together.md)** — a day in the life: how this one idea turns into a working rhythm that mostly runs itself.
