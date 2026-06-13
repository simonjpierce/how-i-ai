# The session loop

Make every working session start where the last one ended and leave the record better than it found it — so you stop re-briefing the AI from scratch, and stop losing what you worked out.

This is an idea file. Paste it into Claude Code to build a version for your own work; it'll fill in the specifics (folder names, exact tools) in collaboration with you. (It has to be an agent that can create files on your machine — a plain chat assistant can't set this up.)

## The core idea

The single biggest waste in working with an AI is the cold start. Every session you re-explain who you are, what you're working on, and where you left off. And at the end, the decisions and the small things you figured out that day evaporate — they lived in the chat, and the chat is gone tomorrow. The conversation was the record, and conversations are lossy.

The fix is to stop treating the chat as the record and instead keep a small set of durable notes that the work flows through. Three light habits do it:

- **Orient at the start.** Before doing anything, the AI reads where you actually left off — the most recent handoff note, the current state of the thing you're working on, and your standing preferences. You begin from context, not from zero.
- **Capture as you go.** Decisions (and *why* you made them), things that turned out to be friction, and useful results get written down *during* the work — not reconstructed from memory at the end.
- **Hand off at the end.** A short closing pass writes a plain "here's where this stands and what's next" note, distils any lasting lesson into the AI's longer-term memory, and brings the related documents back into agreement.

Tomorrow's session reads today's handoff and starts warm. That's the whole trick: the loop is what turns a pile of disconnected chats into one continuous body of work.

## The pieces

**A start-of-session orientation.** A short routine the AI runs before you both dive in. It reads, in order: the last couple of entries in a running **handoff log**, the current state of the active project, and a small always-on instructions file (who you are, how you like things done). It then gives you a two-line "here's where we are" before any work begins. The cost is a few seconds; the payoff is never re-explaining your context again.

**In-flight capture.** As the work happens, three kinds of thing get written down where they'll be found again:
- **Decisions** — what you chose and the reasoning, so a future session doesn't silently re-open a settled question or contradict it.
- **Friction** — anything that went wrong, took a workaround, or wasted time, kept in a running log so the same snag doesn't bite twice.
- **Open questions** — when something is unverified or two sources disagree, the AI leaves a consistent, searchable marker in the note (a short tag like `TODO/VERIFY:` works well) and writes in cautious, attributed language rather than guessing. It never quietly picks a version and moves on — an honest "this is still open" beats a confident sentence hiding a guess. Resolved markers get cleared promptly, so a stale "still open" tag never erodes trust in the record.

There's also a way to **park a whole sub-thread mid-stream** — not just jot a quick note, but set down a half-finished piece of work cleanly: capture where it got to, what's left, and a self-contained "pick this up cold" brief, plus a reminder pointing back to it. A fresh session — even on another machine — can then resume it from a standing start, instead of you holding it in your head or losing it when the chat ends.

**An end-of-session handoff.** A short closing routine that does three things: writes a "state + next step" entry to the handoff log (what got done, what's still open, what to do first next time); distils any durable lesson — a preference, a gotcha, a thing that worked — into the AI's longer-term memory so it sticks across sessions; and runs a quick sweep to bring the related documents current, because a decision made in one place usually needs to ripple to two or three others.

One small detail earns its keep on long projects: that handoff entry opens with a one-line *read this first* pointer to the immediate next action — so if the AI's working memory is ever compacted or reset mid-thread (long sessions do hit that limit), the next session lands on the right thing instead of the top of a generic log.

**A sync sweep, made precise by an artifacts list.** That closing sweep works far better if your main project note carries a small **artifacts list** — a few lines naming every document, folder, or output that belongs to the project and where each lives. With that list, the AI knows exactly which files to reconcile instead of guessing from a search; it walks the list, fixes the mechanical drift itself (a stale status, a renamed path, a number that changed), and pauses to ask you about anything that needs judgement (rewriting a description, removing content, changing scope). Keeping the list current is the one bit of upkeep that makes every future sweep reliable.

## What this does *not* do

It isn't heavy ceremony — orienting and handing off are a minute or two each, not a ritual, and if they ever feel like a tax you've made them too elaborate. It doesn't replace your own sense of where things are; it makes that sense durable across sessions and machines. And it only pays off if the capture is honest: a handoff that papers over the messy bits, or a "resolved" marker on a question that's still open, makes the next session worse, not better. The point is a record you can trust, not a tidy-looking one.

## Why this works

The work people skip under time pressure — logging a decision, writing down why, noting the thing that broke, clearing a resolved flag — is exactly the work that makes tomorrow cheap. It's tedious, so humans drop it; the AI doesn't get bored, and a step that runs every session by default makes keeping the record honest the easy path rather than the heroic one. The notebook stays trustworthy because keeping it trustworthy is nearly free.

## Note

This is a pattern, not a fixed routine. The parts that are yours to shape: where the handoff log and the logs live, what counts as worth capturing, how formal the closing pass is, and which marker token you use for open questions. It assumes an AI agent that can read and write files on your machine, with Claude Code as the driver. The durable idea is: *start from where you left off, capture as you go, hand off cleanly — so the work is continuous and nothing you learned is lost.* Paste this to your AI and build the version you'll actually keep up.
