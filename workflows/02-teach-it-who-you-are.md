# Teach it who you are

Once the stack is running, the next step is to teach the AI who you are — so it stops working like a stranger and starts working like someone who knows your job. By the end you'll have a real standing-instructions file (`CLAUDE.md`) the AI loads every session, and a vault with a sensible folder structure to grow into.

This is an idea file. Paste it into Claude Code and it'll run this as an interview with you, writing the files as it goes — you don't fill anything in by hand.

**One setup tweak first.** So the AI can actually create those files without stopping to ask permission at every step, switch it to its most autonomous mode — in the Claude desktop app, press **Shift-Tab** to cycle the permission setting until it shows **Auto**. Otherwise the interview keeps halting on yes/no prompts and feels broken when it's really just being cautious. You can switch it back any time.

## The core idea

The standing-instructions file is the single highest-leverage thing in this whole system. It loads automatically at the start of every session and tells the AI who you are, what you do, how you like to work, what to call things, where things live. Get it even roughly right and you stop re-briefing the AI forever.

You don't *write* it — you *teach* it, two ways that stack: hand the AI what your current chatbot has already learned about you, then let it interview you to fill in the rest. Most people aren't starting from a blank page, and this step makes sure you don't act like you are.

## Start from what your current AI already knows

If you've been using ChatGPT or Claude in a browser for a while, it has quietly built up a picture of you — your work, your projects, how you write. You can hand that straight over as a starting point instead of rebuilding it from scratch.

Ask your current chatbot something like: *"Write out everything you know about me — my work, my role, my projects, how I like you to respond — as a single document I can copy."* (In ChatGPT this draws on its Memory; Claude can do the same.) Copy what it gives you, paste it into your Claude Code session, and say *"use this to start my standing-instructions file."* In thirty seconds you've seeded the file with months of accumulated context.

No history to draw on? Skip this — the interview below covers it.

## The interview

Now the AI fills the gaps by asking you. The easiest way to answer is by voice — talk, stream-of-consciousness, as much detail as comes to mind (the mic-and-paste method from [set up the stack](./01-set-up-the-stack.md)). You don't need to be organised about it; a rambling answer is exactly right, and the AI pulls out what it needs and asks follow-ups.

It's trying to learn the things it would otherwise get wrong every session:

- **Who you are and what you do** — your role, your field, the work that fills your weeks.
- **How you like to work** — concise or detailed, how much it should check with you before acting, pet peeves.
- **The surface stuff that's annoying to correct repeatedly** — spelling and date conventions, tone, names and terms specific to your world.
- **What recurs** — the projects, people, and obligations that come up again and again, so it recognises them next time.

As you answer, it writes the standing-instructions file. You can read it, change anything, and keep going — and it'll keep growing as you correct the AI over the following weeks (that ongoing learning is the [memory and context](./memory-and-context.md) loop, the next step).

Have it create your memory file (`MEMORY.md`) at the same time, as the pair to your standing-instructions file — your AI knows where its own memory file needs to live, so let it put the file there rather than guessing a location yourself. Nothing goes in it yet — but it's where the AI will start saving what it learns from your very next session, so it's worth creating now rather than arriving at the next step without one.

## Set up your vault folders

While it's learning who you are, have it lay out your vault — a structure that matches *your* life, proposed from what it just learned in the interview. Two kinds of folder:

- **A system folder** — one folder (call it `SYSTEM`, or whatever you like) that the AI explains as it creates: *this is where the notes I generate and maintain on my own live* — the running logs, the memory file, the outputs of scheduled jobs. You rarely need to open it; it's the AI's own workspace, kept tidy autonomously so it doesn't clutter the folders you actually work in.
- **Domain folders** — one per area of your life or work, mirroring how you actually think about it (the maintainer has separate folders for his science, his photography, the foundation he runs, and personal life). These are where your real notes live, and later each can carry its own small standing-instructions file so the AI picks up the right context automatically when it's working in that corner.

You don't have to get this perfect. A couple of sensible folders now is plenty; the structure grows as the work does.

## What this does *not* do

It doesn't lock anything in — the standing-instructions file and the folder layout are living things you and the AI revise constantly. It doesn't require the imported chatbot summary; that's a shortcut, not a dependency. And nothing here is sent anywhere: it's all plain files on your own machine.

## Note

A few minutes teaching the AI who you are is the difference between an assistant that starts cold every morning and one that already knows your job. It's the smallest-effort, highest-return step in the whole setup — and it only gets richer from here.

---

## Next step

**→ [Memory and context](./memory-and-context.md)** — the personalisation loop: how the AI keeps learning how you work, so you never have to correct the same thing twice.
