# The philosophy: the LLM is for thinking, the vault is for memory

The one idea everything else in this repo is built on. Read this first; the rest will make sense once it lands.

This is a short read, not a setup task — but like the other workflows it's fine to paste into Claude Code and talk through if you want to pressure-test the idea against your own work.

## The core idea

If you've used ChatGPT or Claude for any length of time, you know the pattern: every conversation starts from zero. Yesterday's three-hour session leaves nothing behind but a chat window you'll never scroll back to. You re-brief the model on who you are and what you're working on, every time. Personalisation hits a ceiling fast, and your conversations never become *documents* you can build on.

The trap is asking the model to be your memory. It isn't one, and it was never going to be — its working memory only holds so much, each chat is disposable, and "remember this for next time" is a promise no chatbot can keep.

So split the job in two. **The LLM is for thinking** — reasoning, drafting, analysing, connecting ideas, doing the work in front of it right now. **Your vault is for memory** — a folder of plain markdown files, living on your own computer, that holds everything worth keeping: notes, project plans, decisions, transcripts, drafts, the running record of what you've figured out. The model doesn't have to remember anything, because the files remember for it.

This is the whole move: **a memory that lives on your own computer, that the AI reads and writes — sitting beside an AI that's now free to just think.** Obsidian is the nicest tool for *you* to read and edit those files; Claude Code is the AI that reads and edits the same files when you ask. One set of documents, two readers.

## Why this changes everything

Conversations come and go. The documents accumulate. Each session starts richer than the last, because the AI can read everything you've built up over weeks and months — not because it "remembers," but because the memory is on disk where it belongs.

Three things fall out of this once you start living in it:

- **Continuity.** You stop re-briefing. The model reads your project note, your decisions, your standing preferences, and picks up where you left off.
- **Compounding.** A good analysis, a hard-won decision, a useful summary — these get written into the vault instead of evaporating into chat history. Next month they're still there, and they're connected to everything around them.
- **The system gets out of your way.** Once the memory is durable and the AI can act on it, you can start automating the bookkeeping — and that's where the rest of this repo goes.

## What this is *not*

It's not the usual "upload your documents and ask questions about them" setup (the technical name is RAG, if you've heard it). That treats your files as a passive pile the AI dips into for an answer and then forgets. Here the files are the *living record*: the AI writes to them, revises them, keeps them current. It's also not a specific app or a product to buy — it's plain text files (markdown) and an AI that can open and edit them. Everything else is plumbing.

## Why this works

The reason most personal knowledge systems die is maintenance: keeping notes current, cross-referenced, and consistent is tedious, and humans abandon it. An AI doesn't get bored doing the bookkeeping. So the durable-memory layer that was always a good idea but never sustainable becomes sustainable — the AI does the upkeep, you do the thinking and the deciding.

Your job is to bring the questions, the judgement, and the direction. The vault's job is to remember. The AI's job is to think, and to keep the vault honest.

## Note

This is a pattern, not a product. The idea — *think with the model, remember with the files* — transfers to any field and any toolset; the specifics (which editor, which AI, how your folders are organised) are yours to shape. Read on for one concrete way to set it up, then make it your own.

---

## Next step

**→ [How it all fits together](./how-it-all-fits-together.md)** — a day in the life: how this one idea turns into a working rhythm that mostly runs itself.
