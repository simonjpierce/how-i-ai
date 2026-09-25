# The interview loop

A way to close the gap in a system of specialist assistants: instead of only *you* asking *them*, they ask *you* — the questions only you can answer, put to you when you've got the spare attention to answer well — and your answers set work going straight away.

This is an advanced pattern — it only makes sense once you're running specialist agents (see [the agent fleet](./the-agent-fleet.md)) and have noticed them making calls they don't quite have the context for. When you're ready, paste it into your AI agent — Claude Code or Codex — and it'll build the version that fits your setup with you. (It has to be an agent that can create files on your machine — a plain chat assistant can't set this up.)

## The core idea

Give a specialist agent its own domain and it will, sooner or later, hit the edge of what it knows about you. It has to decide something — how hands-on you want to be with a task, which of two priorities wins, what you'd actually recommend — and its notes just aren't deep enough to call it the way you would. The usual outcome is that it guesses, or quietly does the task and never surfaces the gap. Either way the gap persists, and the agent stays a generalist wearing a specialist's hat.

The fix is to build a **question channel that runs the other way**. Early each morning, each agent looks at its current priorities and asks: what would let this move if I had your view on it? It first tries to answer each question from your own notes and drops any it can. Only questions that need your opinion, direction or taste survive — not facts you'd have to look up, and nothing that needs a screen — and they wait in one shared place, tagged with which agent asked and what answering would unblock. An agent can also add one mid-task when it hits a decision only you can make, rather than guessing.

Then they get asked at the one moment you can answer them richly without eating into your working day: **when you're out walking**, and you answer the easy way — by talking. A rambling two-minute spoken answer carries far more than a desk-bound yes/no: the reasoning, the caveats, the "well, it depends on…". That spoken answer starts the work it unblocks right away, while you keep walking, and gets filed into the asking agent's notes, so its judgement compounds in *your* voice — and next time it can ask a sharper follow-up. It's a slow, asynchronous conversation between you and your own assistants.

## How it runs

**The agents gather questions — and throw most of them away.** Early each morning, before the walk, each agent works from its current priorities and drafts what it would need your view on to move them. Then comes the filter that stops this turning into idle chatter: every question is checked against your notes first, and anything the notes already answer is dropped. What survives has to be a decision that's yours (scope, priority, preference, angle), name what answering it unblocks, and be phrased so a spoken, off-the-cuff answer is a good answer. The point is to push your work forward, not to fill the agents' knowledge gaps for their own sake.

**They ask while you walk.** Your phone drives a session running on the Mac — the maintainer uses Claude Code's remote control or Codex's voice mode — so the files stay where they live. The walk opens with the day's plan, but only the items where a couple of minutes of your thinking lets the assistant start something real; then come the agents' questions. The full numbered list appears once, then three at a time, with the questions that start the longest jobs first, so that work runs while you're still out. Answer however suits: a voice memo (hit record, ramble, done), dictated text, or talking live. Results that land during the walk are saved for the desk and read back to you there, because nobody reads replies on a walk.

**The answers file themselves.** Each answer gets transcribed and routed: the substance lands in the asking agent's notes, and the question is marked answered. If an answer opens up an obvious next question, the agent is allowed to chain a follow-up for a later walk. A question that got read out but didn't get answered simply resurfaces next time rather than being lost.

## What this does *not* do

It doesn't let the agents interrupt you. The whole point is that questions *wait* for a good moment — they never nag mid-task. It doesn't answer anything *for* you or invent your preferences; a gap it can't fill just stays a gap until you fill it. And "answered" doesn't mean "finished" — early on, your answers are first-pass and an agent is expected to come back and drill deeper into the same topic later, layer by layer. That's the system catching up on who you are, which is exactly what you want it doing.

## Why this works

The bottleneck in teaching an assistant about your work isn't the assistant's memory — it's *your* time and attention to explain things. This pattern makes that effort much easier to fit in: it batches the questions until they're worth a single pass, and collects the answers during time you were spending anyway (walking), in the lowest-effort form there is (talking). The transfer rides along on something you were doing regardless — the same trick that makes [the self-improvement loop](./the-self-improvement-loop.md) work.

## Note

This is a pattern, not a fixed implementation. The shared queue, the walk read-out, the voice-to-notes routing, how hard you filter the questions — all yours to shape, and all optional; the simplest version is one shared question file your agents write to and you read on a walk. The durable idea is: *let your specialists ask you what they can't work out on their own, batch it to a moment that costs you nothing, and answer by talking.* Paste this to your AI and build the version that fits how you work.
