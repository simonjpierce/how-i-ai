# Running many sessions at once

Once the AI is useful you stop running one conversation and start running five — a research thread here, a build there, an overnight job, a scheduled review — all reading and writing the same notes and the same config. This is how to keep them from trampling each other.

This is an idea file. Paste it into your AI agent — Claude Code or Codex — to build a version for your own work; it'll fill in the specifics in collaboration with you. (It has to be an agent that can create files on your machine — a plain chat assistant can't set this up.)

## The core idea

Everything in this system rests on shared files: the vault, the instruction files, the saved commands, the git repos that hold the automations. That's the strength — and with several sessions live at once, plus scheduled jobs starting on their own (the maintainer sees about ninety session starts a day), it becomes the hazard. The failures are all the same shape: two writers, one file, no coordination. A session reverts a sibling's commits as "leaked" and takes a real bug-fix with them. A reviewer diffs against a stale main and flags the *sibling's* work as regressions. A parked "next step" gets done by one session while another, resuming from the handoff, does it again. An error log holds four of three hundred entries because each new session overwrote the archive.

None of these need a clever fix. They need four plain rules: **know who else is live; never build in the shared tree; treat every parked instruction as possibly stale; and lock anything many writers touch.**

## The pieces

- **Know who else is live.** A session-start hook registers a marker for this session (if the working folder is a tracked repo) and prints a one-line warning if another session's marker is fresh: *"another session is live in this repo."* A second hook refreshes the marker each turn so a long session doesn't age out and go invisible; a third registers late if a session wanders into a tracked repo after starting. Advisory only — it warns, never blocks — but the warning changes what the session does next.
- **Name your tabs.** Each terminal tab shows a three-to-six-word task label set by the session itself at start and when the task changes, alongside the context meter. With five tabs open, "which one was the migration?" is a glance, not a hunt. The maintainer runs this as a tiny daemon reading a per-terminal file, because the harness redraws the title too often for a hook to set it directly.
- **Build in a worktree, never the shared tree.** Any session that writes code or config works in its own git worktree on its own branch — a separate folder with its own checkout of the same repo. The shared base tree stays parked on main, so the nightly automations (which commit from the base tree) always land on main and never on someone's feature branch. Merge back serially, re-verifying first. This one rule removed most of the collisions; the residual contention is a brief, serialised git operation, which is survivable.
- **Check the branch before every commit.** Check you're on the branch intended for this task. Planned feature work belongs on its own worktree branch; the danger is a *shared* tree that sessions and background jobs have left on a stale branch, where a commit "succeeds" and never reaches main. If your work landed on a branch it wasn't meant for, inspect the commits first, cherry-pick yours to main, push, and only then tidy the stale branch — never reset a branch merely because it differs from main. A hook can do the check for you. And never suppress a push's error output or chain a fallback onto it — one chained push swallowed a double rejection and the session reported success.
- **Treat parked instructions as possibly stale.** A "What's next" from a prior session or a handoff entry may already have been done by a sibling, or main may have moved underneath it. Before acting: current git status, the last few commits and who made them, and any files in the working tree you never touched. The handoff format helps here — each entry carries a session marker, and each new entry has a "follow-up on prior what's next" line that says what the sibling sessions' items came to.
- **Lock what many writers share.** Logs, ledgers, queues and the intake page are appended to by sessions and jobs alike. Every such write goes through one helper: exclusive lock in a private lock folder, read under the lock, atomic replace, and a check that the file didn't change between read and write (abort rather than overwrite). Four of three hundred errors surviving was the price of one unlocked read-modify-write at session start.
- **Read a scary notification before reacting.** When a background job sweeps your uncommitted edits into its commit, the harness shows a diff that can render in conflict-marker style and look like a broken merge. Check the file on disk for real markers first; no hits means no conflict. Then find which commit absorbed your edits and run the tests. Prevention is the worktree rule; this is for when you're already in the shared tree.

## What this does *not* do

It doesn't serialise your sessions or stop you running many — that's the point of having them. It doesn't make the shared vault safe for two sessions editing the *same note* at the same moment; the vault auto-commits on a schedule and the last write wins, so the discipline there is one topic per session. And the collision guard is advisory: it tells the session someone else is here; what to do about it is judgement.

## Why this works

Every collision is two writers and one file. Worktrees give each interactive writer its own file. Locks serialise the few files that genuinely must be shared. The marker and the tab label make the other writers *visible*, which is what turns a silent collision into a decision. And the habit of re-verifying before acting on a parked step covers the one case files can't: two sessions holding the same plan.

## Note

This is a pattern, not a fixed toolkit. How you label tabs, whether you build the marker hooks or just check the process list, how strict you are about worktrees for tiny edits — all yours. The durable idea is: *many sessions on shared files is normal, so make the other sessions visible, give each writer its own tree, lock the few files that must be shared, and never trust a parked instruction without checking live state first.* Paste this to your AI and build the version that fits how you work.

---

*Want the actual method? [The reference](../reference/running-many-sessions-at-once.md) lays out the maintainer's real version — the collision hooks, the worktree convention, the branch check, the lock helper, the stale-instruction check — cleaned of personal specifics. A starting point to adapt, not a drop-in.*
