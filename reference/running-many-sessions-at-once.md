# Reference — Running many sessions at once

> **What this is.** The actual method behind [the *Running many sessions at once* workflow](../workflows/running-many-sessions-at-once.md), cleaned of the maintainer's personal specifics. A **starting point to adapt, not a drop-in.** Assumes git and a Unix-like shell; the maintainer's terminal is Ghostty on macOS.

## The collision guard (advisory, three hooks)

State: a folder of marker files, one per live session, named by session id, containing the repo path and a timestamp.

- **`SessionStart`** — if the working folder is inside a tracked git repo, write this session's marker; list other markers for the same repo fresher than the live window (the maintainer uses ~30 minutes); if any, print one line: *"⚠️ another Claude session is live in `<repo>` (started HH:MM). Work in a worktree; re-verify parked steps."* Exit 0 always.
- **`Stop`** (each assistant turn) — refresh this session's marker timestamp if one exists. Never creates one, never warns. Without this, a long session ages out of the window and becomes invisible to a sibling's check.
- **`CwdChanged`** — late registration for a session that started outside a tracked repo and moved into one. Same warning logic as session start.

Ordering between parallel session-start hooks isn't guaranteed; don't depend on the warning appearing before or after the handoff text.

## Tab titles

A per-terminal file (`/tmp/claude-title-<tty>`) holds a 3–6 word label. The session writes it at start and whenever the task changes:

```bash
MY_TTY=$(ps -o tty= -p $PPID | tr -d ' ') && echo "short task summary" > "/tmp/claude-title-${MY_TTY}"
```

A tiny background daemon (started by the session-start hook if not running) reads the file every two seconds and sets the terminal title with an OSC escape. It's a daemon rather than a hook because the harness's own redraws overwrite a title set from inside a hook. The status line also reads the same file, so the label appears beside the context meter. Some harness versions offer a native session-title setting; the daemon is kept because it supports mid-session changes and a "✅ done" flip.

## The worktree convention

Two repos get written from many sessions: the automations repo and the AI config repo. Rule: **any write/build session works in a dedicated worktree, never the shared base tree.**

```bash
cd <repo>
git worktree add <repo>_<task> -b <task-branch>   # own folder, own branch
cd <repo>_<task>                                  # build, test, commit HERE
# when done: merge to main serially (re-verify first), then
git worktree remove <repo>_<task>
```

- The base tree stays **parked on main**, because nightly automations commit from it. If you find it on a feature branch, return it to main once that branch's work is committed.
- Fallback if you must share the base tree: one writer at a time; if overlapping, each on its own branch, merged serially. And if the base tree's index already holds *another session's* staged files (`git status` shows `A`/`AM` entries you didn't create), a plain `git add <file> && git commit` sweeps them into your commit — commit by pathspec.
- **Fetch before you fast-forward a second tree** of the same repo: "Already up to date" against a stale remote-tracking ref is a lie, not a no-op.
- Honest limit: automations still commit to main from the base tree, so contention remains at the instant an interactive branch merges — a brief serialised op, low risk.

What went wrong before the rule (one day, four sessions on one main): a revert war that took a live bug-fix as collateral; a review from a worktree branched off stale main flagging the sibling's commits as regressions (two wasted rounds); uncommitted edits lost to a sibling's `git clean`.

## The branch check and the push rules

- **Before any commit, in any repo**, check `git branch --show-current`. Multi-session repos are routinely left on stale feature branches by background work; a commit there never reaches `origin/main`. If not on main: cherry-pick to main, push main, then `git reset --hard HEAD~1` on the feature branch *only if* that commit wasn't pushed there (`git log origin/<branch>..HEAD` non-empty). A `PreToolUse Bash` hook on `git commit` can enforce the check.
- **Never suppress a push's stderr, never chain a fallback onto a push**: `git push -q … 2>/dev/null || git push <alt>` ate a double non-fast-forward rejection and the session reported "pushed". After any push that matters, verify the remote head advanced (`git rev-parse origin/main` after `git fetch`). A hook flags the suppressed-push shape.

## Stale parked instructions

Before acting on any "What's next" from a handoff, a State of Play, or a queue:

1. `git status` — files you never touched mean a sibling or job has been here.
2. `git log --oneline -5` — recent authors and messages; has main moved?
3. Look for the artefact the step would produce — does it already exist?

Handoff-log conventions that make this cheap: every entry opens with an HTML comment naming the session (`<!-- session:<slug> -->`); every new entry has a **"Follow-up on prior What's next"** paragraph stating what each sibling's open items came to (done / orthogonal / superseded) before listing its own. Newest entries at the top, so the session-start hook prints the right one.

## Locks on shared files

One helper for every read-modify-write on a file many writers touch (logs, ledgers, queues, the intake page, state JSON):

- Exclusive `flock` on a lock file in a **private lock folder** (not beside the target — cloud sync would replicate the locks). Where `flock` is unavailable, `mkdir` is the portable atomic test-and-set; reclaim locks older than ~60 s.
- Read under the lock; caller mutates in memory; **commit** writes a temp file, `fsync`, `os.replace`.
- **Optimistic check**: hash the bytes read under the lock, re-hash from disk immediately before the replace; mismatch → abort with a named error rather than overwrite. Never retry or merge automatically — the lock is prevention; the check is the signal that prevention failed.
- An environment-variable bypass for rollback if the locking itself misbehaves.

The concrete failure: the session-error archive held 18 rows from one morning against 329 failures in the week. Cause one: rotation was a plain `mv` (single slot, each start clobbered the last). Cause two, after fixing that: an unlocked append-then-prune raced across ~90 daily session starts. Both looked, from the outside, like "the writer hooks are broken".

## Reading a scary notification

A background job sweeps your uncommitted edits into its commit; the harness shows "file modified by user or linter" with a diff rendered in `<<<<<<< / ======= / >>>>>>>` style. Before touching anything:

1. `grep -rln '^<<<<<<< \|^>>>>>>> \|^=======$' <files>` — no hits means **no live conflict**; the rendering was an artefact.
2. Compare `git log --oneline -1 HEAD` with the HEAD you remember — a move means something committed under you.
3. `git log -S '<a symbol you just added>'` names the commit that absorbed your edits (often mislabelled).
4. Run the tests. Green means your work is intact; check it also reached the remote.

## What stays yours

Marker window, tab-label mechanism, how strict the worktree rule is for one-line edits, which files get the lock helper. The transferable spine: *make other sessions visible; give each writer its own tree; check the branch before every commit and never hide a push's errors; verify live state before acting on a parked step; lock the few files everyone shares.*
