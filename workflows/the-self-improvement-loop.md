# The self-improvement loop

A way for the system to get better at working with you over time — noticing what's clunky, proposing fixes, and folding the good ones in — so the rough edges sand themselves down instead of annoying you forever.

*This is an advanced pattern — it pays off once you're using the system daily and friction is accumulating, not on day one. The simplest useful version is just one log file you actually add to; when you're ready for more, paste it into Claude Code and grow it from there.*

## The core idea

Any system you use daily has friction: a step that's fiddlier than it should be, a thing the AI keeps getting wrong, a preference you've had to repeat five times. Normally that friction just *persists* — you work around it and move on, and nothing improves.

The move here is to make the system watch itself and improve. It rests on a few cheap habits:

- When something is harder than it should be, it gets written down — a one-line note in a **friction log**.
- When you make a non-obvious choice, the reasoning gets written down — in a **decision log** — so you (and the AI) don't re-litigate it later.
- Periodically, something reviews those logs, spots the patterns ("this has come up three times"), and **proposes a fix**.
- Before a meaningful fix lands, a **second model checks it** — an independent review that catches the holes in the first model's plan.
- Approved fixes get **implemented** — often overnight by [the workhorse](./the-overnight-workhorse.md) — and the lesson is folded into the AI's standing instructions or memory so it actually sticks.

The result: the system you use in three months is noticeably smoother than the one today, without you running an improvement project. The improvements ride along on work you were doing anyway.

## The pieces

- **A friction log** — what hurt, what you worked around, what needs a real fix. Append-only; cheap to add to.
- **A decision log** — non-obvious choices and *why*, so they're not second-guessed later.
- **A review step** — a second, independent AI model that pressure-tests a proposed fix before it's built. Two models disagreeing productively beats one model confidently wrong.
- **An implementer** — the thing that actually makes the approved change (in the maintainer's system, the overnight workhorse plus a nightly "improve the system" pass).
- **A home for the lesson** — the standing-instructions and memory files, so the fix changes future behaviour, not just one session.

## How it runs

You (or the AI) jot friction and decisions as they happen — seconds, not a chore. On a regular cadence, the system reviews the logs, surfaces recurring patterns, and proposes fixes. You approve the ones that matter; a second model reviews anything substantial; the approved fixes get implemented and the lessons land where they'll fire next time. The tedium of *remembering* and *implementing* improvements — the reason people abandon this kind of thing — is carried by the AI.

## What this does *not* do

It is not the system silently rewriting itself behind your back. You approve the changes that matter; the loop just removes the friction of capturing, reviewing, and applying them. And you don't need the full machinery to start — a single friction log you actually add to, reviewed now and then, already beats letting the same annoyances persist. Add the review step and the auto-implementation later.

## Note

This is a pattern, not a fixed pipeline. What you log, how often you review, whether you wire in a second model or auto-implementation — all yours, and all optional. The durable idea is: *capture friction cheaply, review it on a cadence, and let the AI carry the cost of actually improving things.* Paste this to your AI and start with the smallest version that fits.
