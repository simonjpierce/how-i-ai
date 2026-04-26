---
audience: user
---

# 02 — Three Claudes

The desktop app gives you three Claude tabs side by side: **Chat**, **Cowork**, and **Code**. They share the same engine but have different sweet spots — and picking the wrong one for the job costs hours. Install the desktop app and get familiar with all three; that's the minimum bar. The CLI sits above this for people who want keyboard-driven workflows or to wire Claude into automation, but it's optional and a real step up in setup.

## Why not just use claude.ai in a browser?

Browser chat at claude.ai is fine for "what's the scientific name for spinner dolphin?" but falls down fast for research work. No file access, no project context, no persistence between sessions. The desktop app's Chat tab handles attachments, drag-and-drop, and `@filename` references — you can actually work with your documents. Cowork and Code don't exist in the browser at all. If you find yourself copying text from a vault note into a claude.ai tab, stop and open the desktop app instead.

## The three tabs

- **Chat.** Conversational, with file access. Drop a PDF in, attach a vault note, or `@filename` into the prompt. Closest analogue to claude.ai but actually capable of working with your documents. Use for: questions about a paper, summarising a transcript, drafting a paragraph from a brief.
- **Cowork.** An autonomous background agent that runs in a cloud VM with its own environment. You give it a well-scoped task, it grinds through while you do other things, then reports back. Sweet spot for chunky-but-bounded work — "go through these 200 PDFs and pull out species records", "draft section 3 of this grant from these source notes". May actually be the right home base if you prefer to delegate-and-review rather than work side-by-side with Claude.
- **Code.** Interactive analysis and editing with direct access to your local files. You review and approve each change in real time. Sweet spot: iterating on something where you want to see what's happening as it happens — analysis, writing, code, anything where you'll want to interrupt and steer.

## Rule of thumb

- Want to ask questions or have a back-and-forth that touches a few files? **Chat.**
- Have a chunky task that's well-scoped and can run while you do other things? **Cowork.**
- Doing analysis, writing, or coding where you'll iterate step-by-step? **Code.**

If you're not sure which one fits, **Code** is the safest default — it can handle anything the others can, you just trade off some convenience.

## The CLI is optional

The terminal version of Claude Code is what Simon uses, and it's powerful for scripting, hooks, and automation. It's also a real step up in setup and learning curve, and the desktop app covers most of what most people need. Don't feel like you have to use the CLI to be doing this "properly". Get comfortable with the desktop app first; reach for the CLI later, if at all.

## One more thing: agreement bias

Plain browser chat at claude.ai is reflexively agreeable. You'll say "what if we did X?" and it'll say "great idea, here's why X works!" — and ten minutes later when you've found X is actually bad, it'll say "correct, Y makes X untenable." Code (and to a lesser extent Cowork and desktop Chat) is noticeably more willing to push back and flag problems with an approach, partly because being able to look at the actual files makes it harder to just rubber-stamp an idea. Not perfect, but better.

When you want a real second opinion on a plan, ask in the desktop app — Code if you want it to dig into your files, Chat if you just want it to engage with the argument — and ask the question without telegraphing your preferred answer.

## What's next

`03-your-first-skill.md` — we'll use one of the skills in this repo on a real task.
