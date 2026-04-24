# 02 — Use Code, not Chat

Anthropic offers three different Claude interfaces, and they are not equivalent. Choosing the wrong one for research work costs hours.

## The three Claudes

- **Claude Code** — `claude` in the terminal. What this repo is about. Full access to your local filesystem and tools. Can read and write files, run commands, use MCP servers, work persistently across a whole session. Best for: research, analysis, writing, anything that touches multiple files or external tools.
- **Cowork** — in the Claude web app (claude.ai). Code-like, but sandboxed. No direct filesystem access, safety rails engaged. Fine for quick one-offs when you don't want to leave the browser, but consistently less capable than Code.
- **Chat** — claude.ai and mobile apps. One message at a time, no tool access, no file access, no persistence. Good for quick factual questions. Bad for anything involving data, documents, or iteration.

## Rule of thumb

If your work involves any of the following, use **Code**:

- Reading or writing local files (markdown notes, R scripts, CSVs, PDFs, images).
- Running commands or scripts (R, Python, bash, git).
- Analysis of a dataset, even a small one.
- Iterating on a document that references other files.
- Anything you'd normally do in RStudio, VS Code, or a terminal.

Use **Cowork** if you're in a meeting and can't be bothered opening a terminal, or for a quick sanity check on a small thing.

Use **Chat** only for "what's the scientific name for spinner dolphin" questions.

## One more thing: agreement bias

Chat is the worst of the three for another reason: it is reflexively agreeable. You'll say "what if we did X?" and it'll say "great idea, here's why X works!" — and then ten minutes later when you've found that X is actually bad, it'll say "correct, Y makes X untenable." Code is noticeably more willing to push back, disagree, and flag problems with an approach. Not perfect, but better.

When you want a real second opinion on a plan, ask in Code, and ask the question without telegraphing your preferred answer.

## What's next

`03-your-first-skill.md` — we'll use one of the skills in this repo on a real task.
