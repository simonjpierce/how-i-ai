# The interview loop

A way to close the gap in a system of specialist assistants: instead of only *you* asking *them*, they ask *you* — pooling the questions they can't answer from their own notes and putting them to you when you've got the spare attention to answer well. Their picture of your work fills itself out over time, in your words.

This is an advanced pattern — it only makes sense once you're running specialist agents (see [the agent fleet](./the-agent-fleet.md)) and have noticed them making calls they don't quite have the context for. When you're ready, paste it into Claude Code and build the version that fits your setup.

This is an idea file. Paste it into your AI agent — Claude Code or Codex — to build a version for your own work; it'll fill in the specifics (folder names, exact tools) in collaboration with you. (It has to be an agent that can create files on your machine — a plain chat assistant can't set this up.)

## The core idea

Give a specialist agent its own domain and it will, sooner or later, hit the edge of what it knows about you. It has to decide something — how hands-on you want to be with a task, which of two priorities wins, what you'd actually recommend — and its notes just aren't deep enough to call it the way you would. The usual outcome is that it guesses, or quietly does the task and never surfaces the gap. Either way the gap persists, and the agent stays a generalist wearing a specialist's hat.

The fix is to build a **question channel that runs the other way**. Each agent, whenever it notices a genuine gap — a decision only you can make, or a piece of knowledge it's missing — writes the question down in one shared place instead of guessing or forgetting it. The questions just accumulate there, tagged with which agent asked and what answering it would unblock.

Then they get asked at the one moment you can answer them richly and at no cost to your day: **when you're out walking.** The agents read their top few questions out to you at the start of a walk, and you answer them the easy way — by talking. A rambling two-minute spoken answer carries far more than a desk-bound yes/no: the reasoning, the caveats, the "well, it depends on…". That spoken answer flows back through transcription and gets filed into the asking agent's notes, so its expertise compounds in *your* voice — and the next day it can ask a sharper follow-up. It's a slow, asynchronous conversation between you and your own assistants.

## How it runs

**The agents accumulate questions.** Whenever an agent is working and hits something it can't resolve from its own notes, it appends a question to one shared queue — not a live interruption, just a note for later. Two kinds count: *decisions* that are genuinely yours (scope, priority, preference), and *knowledge gaps* where the agent knows its picture is too thin to call something at your level. There's a quality bar so this doesn't turn into idle chatter: each question has to name what answering it unblocks, and be phrased so a spoken, off-the-cuff answer is a good answer. A per-agent cap stops any one of them hogging the channel.

**They ask while you walk.** The maintainer runs this through the Claude mobile app driving a session on the Mac over remote control — so the assistant reads the questions out to your phone and hears your answers, but the actual work (reading and writing your files) happens back on the machine that has them. You answer with the iOS Voice Memos app: hit record, ramble, done. Several memos across one walk is fine. Unlike the usual one-thing-at-a-time coaching, the questions come as a single batch up front — because you answer a batch in one continuous monologue, not one message at a time.

**The answers file themselves.** Each voice memo gets transcribed and routed: the substance lands in the asking agent's notes, and the question is marked answered. If an answer opens up an obvious next question, the agent is allowed to chain a follow-up for a later walk. A question that got read out but didn't get answered simply resurfaces next time rather than being lost.

## What this does *not* do

It doesn't let the agents interrupt you. The whole point is that questions *wait* for a good moment — they never nag mid-task. It doesn't answer anything *for* you or invent your preferences; a gap it can't fill just stays a gap until you fill it. And "answered" doesn't mean "finished" — early on, your answers are first-pass and an agent is expected to come back and drill deeper into the same topic later, layer by layer. That's the system catching up on who you are, which is exactly what you want it doing.

## Why this works

The bottleneck in teaching an assistant about your work isn't the assistant's memory — it's *your* time and attention to explain things. This pattern spends neither: it batches the questions until they're worth a single pass, and it collects the answers during time you were spending anyway (walking), in the lowest-effort form there is (talking). The knowledge transfer rides along on something you were doing regardless — the same trick that makes [the self-improvement loop](./the-self-improvement-loop.md) work.

## Note

This is a pattern, not a fixed implementation. The shared queue, the walk read-out, the voice-to-notes routing, how many questions an agent may bank — all yours to shape, and all optional; the simplest version is one shared question file your agents write to and you read on a walk. The durable idea is: *let your specialists ask you what they can't work out on their own, batch it to a moment that costs you nothing, and answer by talking.* Paste this to your AI and build the version that fits how you work.
