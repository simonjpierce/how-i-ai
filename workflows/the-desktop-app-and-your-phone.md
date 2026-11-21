# The desktop app and your phone

Run everything from one place, the Claude desktop app on your computer, and pick up the same sessions from your phone when you're away from the desk, with your files never leaving the machine.

This is an idea file. Paste it into Claude Code and it'll help you set up the equivalent on your machine, adapted to how you work. (It has to be an agent that can create files on your machine — a plain chat assistant can't set this up.)

*What you'll need: the Claude desktop app, a paid Claude plan (Remote Control, the phone link described below, is on the Pro, Max, Ultra, Team, and Enterprise plans; on Team and Enterprise an owner has to switch it on first), and the Claude mobile app on your phone, signed in to the same account.*

## The core idea

The AI that knows your work lives on your computer, because that's where your notes are. The Claude app on your phone is, by default, a separate chat that can't see any of them. So the thinking you do away from the desk, on a walk or between meetings, either waits until you're back or lands somewhere else and has to be carried across by hand.

The fix is one home and one window onto it. The home is the desktop app's **Code tab**, where sessions read and write your vault. The window is your phone: through a Claude Code feature called **Remote Control**, the Claude mobile app connects to a session that's running on your computer, so you're talking to the same session, with the same files, from wherever you are.

That is now the maintainer's whole set-up: the desktop app at the desk, the mobile app connected to it when he's away. It used to involve a terminal, a separate dictation service, and a second voice app; it doesn't any more, and it's much more self-contained for it.

## The pieces

- **The desktop app as the home.** Everything in this guide runs there. It reads the same settings as any other version of Claude Code, so hooks (small scripts that fire on events) work; skills, plugins, and connections to other services install from inside the app; and its **Routines** page runs scheduled tasks on your own machine, against your own files, at times you choose. You can create one just by asking in any session ("set up a daily review at 9 am"). It shows how full the conversation is as a ring next to the model picker (see [managing your token budget](./managing-your-token-budget.md)), and one session can start other sessions and hear back from them (see [one session that runs the others](./one-session-that-runs-the-others.md)). There's a terminal pane built in too, but the AI runs commands itself, so you can ignore it.
- **Remote Control: the phone as a window.** In a session's prompt box, type `/remote-control` (or `/rc`). The session then appears in the Claude mobile app's list of sessions, and at claude.ai/code in a browser. To make every new session reachable without typing anything, turn on **Connect new sessions to Remote Control** in the app's settings, under Code. Everything still runs on your computer: the files, the tools, and the connections stay there, and the phone only sends your messages and shows the replies. The conversation stays in step across both, so you can start something at the desk and carry on from the phone, or the other way round. You can also attach a photo or a file from the phone; the session gets it on your computer.
- **Talk, don't type.** The mobile app has a microphone button that turns your speech into text and sends it as an ordinary message. Claude's transcription is now good enough that the maintainer uses nothing else for it. His morning walk is exactly this: talking into his phone, into a session on his Mac, which reads him the day's questions and acts on his answers while he keeps walking (see [the interview loop](./the-interview-loop.md), and [transcription](./transcription.md) for what happens to longer recordings).
- **Answer from the phone.** When the session needs your permission for something, or asks you a question, it waits for your answer rather than timing out, so you can deal with it from the phone.
- **Keep the computer on.** The phone is a window, not a second computer. Your machine has to stay on and the app has to stay open. If the laptop sleeps or the network drops, the session reconnects by itself once the machine is back online; quitting the app takes it offline until you open it again. The app's *keep computer awake* setting helps here, and it matters for scheduled tasks too: they only run while the app is open and the machine is awake, and a missed run gets one catch-up when you're back.

## What this does *not* do

It doesn't put your work in the cloud. If your computer is off, nothing runs, and the phone can't reach your files on its own. It's also not quite the full desk experience: in the maintainer's set-up, a session driven from the phone can't always start new sessions of its own, so the walk writes the brief down and the main session on the Mac starts the work. And it doesn't replace reading at the desk. Long results are better saved for when you're back than read on a phone screen mid-walk.

## Note

This is one concrete set-up, not the only one. Whether you connect every session or only the one you'll want on a walk, and how much you do from the phone at all, are yours to choose. The durable idea is: *one home on your computer, where the files are, and your phone as a window onto it, so nothing you think of away from the desk lands anywhere else.* Feature names and menus change quickly, so if this page and the app disagree, believe the app.
