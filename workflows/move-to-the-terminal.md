# The terminal (optional)

Running the AI in a terminal instead of the desktop app. This used to be the gateway to the automation layer; it isn't any more — the desktop app now does the things the terminal used to be needed for. So this page is mostly here to say *you probably don't need this*, and to cover the one genuinely useful bit that survives: how to think about your context window.

This is an idea file, and an *advanced* one — not a day-one move. If you do want the terminal, paste this into Claude Code and it'll set up the equivalent on your machine, adapted to your taste.

## Do you need it? Probably not

For a long time the honest answer was "yes, eventually" — the command-line version was the only one that ran **hooks** (small scripts that fire on events) and **scheduled, unattended work**, and that automation layer is what [the agent fleet](./the-agent-fleet.md), [the overnight workhorse](./the-overnight-workhorse.md), and [the self-improvement loop](./the-self-improvement-loop.md) are built on.

As of mid-2026 the Claude desktop app covers all of that:

- it reads the same settings files as the terminal version, so hooks work in the app;
- skills, plugins, and external integrations (MCP servers) are all installable from inside the app;
- its **Routines** page runs *local scheduled tasks* — a fresh session at a time you choose, on your own machine, against your own files, with a permission mode you set per task. You can create one just by asking in any session ("set up a daily review at 9 am"). The one constraint is that the app has to be open and the machine awake (there's a "keep computer awake" setting, and a missed run gets one catch-up when you're back);
- it shows your context usage in a ring next to the model picker — so the custom context meter that used to be the best reason to move is no longer needed;
- and it has a terminal pane built in for the odd command.

The maintainer still lives in a terminal (a terminal app called [Ghostty](https://ghostty.org)) — partly habit, partly because his overnight jobs are *scripts* that drive Claude in "headless" mode (`claude -p`, no interactive session at all) from the operating system's own scheduler, which is a step beyond a scheduled prompt. If you reach the point where you want code to orchestrate the AI rather than a prompt on a timer, that's the terminal's remaining real job. Otherwise: stay in the app.

## If you do use the terminal

- **A terminal.** Ghostty is fast, simple, nicely themed; any terminal works (iTerm, the built-in macOS Terminal). A reasonable starting Ghostty config is just a theme and a readable monospace font, and optionally a `working-directory` set to your vault so every new tab opens there.
- **Notification sounds and tab titles** *(optional polish)*. Hooks that play a sound when the AI finishes or needs you, and set the tab's title to what it's working on. Genuinely nice when you step away mid-task; pure convenience.
- **A context status line.** Only if you want a permanent one-line meter (`Context: 42% used`) rather than checking `/context`; the app's usage ring makes this moot there.

## Managing your context window

Wherever you run it, the AI can only hold so much of the conversation at once. When it fills, the AI **compacts** — summarising older turns to make room. A few things are worth knowing (current as of mid-2026; this area changes fast):

- **Auto-compaction is good now.** It's fast, it keeps your actual requests and key material, and it has a safeguard against looping. You don't need to hover over it or compact pre-emptively.
- **The real lever isn't compaction — it's your files.** What gets lost in a compaction is older *conversation* detail; what survives is anything written down — your vault notes and your standing-instructions file (it auto-loads every session). So when context gets tight, the move that matters is **capturing the work into your notes** (if you've set up a session-handoff step, run it), *not* manually compacting. The files outlive the conversation — which is the whole point of this system.
- **Use `/compact focus on <thing>`** only when you have something specific you know must survive the next compaction.
- **If a session feels degraded** after a compaction, just start a fresh one — because your notes and standing-instructions carry the context, you lose nothing.

## What this does *not* do

It doesn't make the terminal necessary — everyday work, hooks, skills, and scheduled tasks all run in the desktop app now. It won't manage your context *for* you beyond what auto-compaction already does; the discipline of writing things down is yours. And the terminal setup itself — theme, fonts, sounds — is all taste; none of it is load-bearing.

## Note

The durable idea is small: *the terminal is optional; scripts driving the AI headlessly are its one remaining real use; and a glance at your context plus good notes is all the "context management" you really need.* Tool capabilities move fast — if this page and the app disagree, believe the app.
