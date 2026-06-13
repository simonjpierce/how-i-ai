# Move to the terminal

The step into "advanced": run your AI in the terminal instead of the desktop app — which is what unlocks the automation layer everything else in this section depends on — and set it up so you can see your context filling up and get nudged when the AI needs you.

This is an idea file, and an *advanced* one — not a day-one move. Paste it into Claude Code once you're ready, and it'll set up the equivalent on your machine, adapted to your taste. Treat the specifics below as the maintainer's actual setup, not a prescription.

## Why bother — what the terminal unlocks

For the everyday loop (reading and writing your notes, running workflows) the desktop app is genuinely fine, and friendlier. The reason to move to the terminal is that the command-line version of the AI can run **hooks** (small scripts that fire on events — the AI finishing, asking a question, needing permission) and **scheduled, unattended work**. That automation layer is what the advanced workflows — [the agent fleet](./the-agent-fleet.md), [the overnight workhorse](./the-overnight-workhorse.md), [the self-improvement loop](./the-self-improvement-loop.md) — are built on. You can't really do those from the desktop app.

So: come here when you want the automation, or when you're living in the system daily and want finer control. Not before.

## The pieces (the maintainer's setup — adapt freely)

- **A terminal.** The maintainer uses **[Ghostty](https://ghostty.org)** — fast, simple, nicely themed — but any terminal works (iTerm, the built-in macOS Terminal, etc.). A reasonable starting Ghostty config is just a theme and a readable monospace font:
  ```
  theme = Andromeda
  font-family = Source Code Pro
  font-size = 14
  ```
  Optionally set `working-directory` to your vault so every new tab opens there.

- **A context status line** *(the single most useful addition)*. Claude Code can render a custom status line, and a small script can read its context-usage data and show you, at a glance, how full the window is — e.g. `Context: 42% used | 58% remaining`, escalating to `COMPACT SOON` and then `COMPACTING IMMINENTLY` as it fills. Ask your AI to build it; it reads Claude Code's status-line feed (using a small helper called `jq`) and prints one line. This turns "how much room is left?" from a guess into a glance — see the context section below for why that matters less than it used to, but still helps.

- **Notification sounds and tab titles** *(optional polish)*. Hooks that play a sound when the AI finishes, asks you a question, or needs permission — and set the terminal tab's title to whatever it's working on (with a ✓ when it's done). Genuinely nice when you step away mid-task. Your AI can build these from Claude Code's hook system; they're pure convenience, so add them only if you want them.

## Managing your context window

Your AI can only hold so much of the conversation at once. When it fills, the AI **compacts** — summarising older turns to make room. A few things are worth knowing (current as of mid-2026; this area changes fast):

- **Auto-compaction is good now.** It's fast, it keeps your actual requests and key code, and it has a safeguard against looping. You don't need to hover over it or compact pre-emptively the way you used to.
- **There's no reliable automatic context meter** — that's why the status line above is worth setting up. You can also check any time with the `/context` command.
- **The real lever isn't compaction — it's your files.** What gets lost in a compaction is older *conversation* detail; what survives is anything written down — your vault notes (they persist) and your standing-instructions file (it auto-loads every session). So when context gets tight, the move that matters is **capturing the work into your notes** (if you've set up a session-handoff step, run it), *not* manually compacting. The files outlive the conversation — which is the whole point of this system.
- **Use `/compact focus on <thing>`** only when you have something specific you know must survive the next compaction.
- **If a session feels degraded** after a compaction, just start a fresh one — because your notes and standing-instructions carry the context, you lose nothing.

(Whatever the tool, the files-not-conversation principle is identical — your durable record is the notes, not the chat, so a compaction never costs you the work.)

## What this does *not* do

It doesn't make the terminal mandatory — your everyday work runs perfectly well in the desktop app, and this is purely about unlocking the automation layer when you want it. It won't manage your context *for* you beyond what auto-compaction already does; the discipline of writing things down is yours. And the exact setup — terminal, theme, fonts, sounds — is all taste; none of it is load-bearing.

## Note

This is the maintainer's real terminal setup, lightly de-personalised — a starting point to adjust, not a standard to match. Paste it into Claude Code and have it build the equivalent on your machine, then change whatever you like. It assumes macOS + Ghostty; on Linux or Windows, or in another terminal, the same pieces (a custom status line, event hooks) exist — your AI will map them across. The durable idea is small: *the terminal is where the automation lives, and a glance at your context plus good notes is all the "context management" you really need.*
