# mmf-claude-code — notes for Claude

This file is `CLAUDE.md` at the root of a Git repo. Depending on why you're here, jump to the right place:

- **A user pasted the impatient-path prompt** (*"Walk me through setting up github.com/marinemegafauna/mmf-claude-code on my machine. I have Claude Code installed already; install the starter skills and run /onboard."*) → **follow the impatient-path install below**, then run `/onboard`. (Inline because this is a tight enough flow that a separate file was overkill.)

  ```bash
  # 1. Platform check
  [ "$(uname)" = "Darwin" ] || { echo "Setup is currently macOS-only. Halting."; exit 1; }

  # 2. Prereq check
  command -v git >/dev/null 2>&1 || { echo "ERROR: git not installed. Install Xcode Command Line Tools first: xcode-select --install"; exit 1; }
  command -v bash >/dev/null 2>&1 || { echo "ERROR: bash not available"; exit 1; }

  # 3. Clone the repo to a stable location (not /tmp/, which gets cleaned at reboot)
  mkdir -p ~/.claude/repos
  if [ -d ~/.claude/repos/mmf-claude-code ]; then
    git -C ~/.claude/repos/mmf-claude-code pull --quiet
  else
    git clone --depth 1 https://github.com/marinemegafauna/mmf-claude-code.git ~/.claude/repos/mmf-claude-code
  fi

  # 4. Run bootstrap (--yes on first install, interactive on re-run)
  if [ -d ~/.claude/skills/onboard ]; then
    bash ~/.claude/repos/mmf-claude-code/sync/bootstrap.sh
  else
    bash ~/.claude/repos/mmf-claude-code/sync/bootstrap.sh --yes
  fi
  ```

  If the `git clone` fails with `fatal: repository not found`, the user doesn't have access — the repo is private. Tell them: *"Looks like you need GitHub access to the `marinemegafauna/mmf-claude-code` repo. The simplest path is `gh auth login` if you have the GitHub CLI installed (or run `brew install gh` first), then I'll re-run the clone. If you don't have a GitHub account at all, ask Simon to add your account."*

  After bootstrap succeeds, tell the user: *"I've installed the starter skills (`/onboard`, `/document`, `/session-start`, `/update`, `/review-friction`, `/refresh-skills`). To finish, restart Claude Code: in the desktop app choose Claude → Quit (Cmd-Q), then reopen it from your Applications folder. Click into the chat input and type `/onboard` — that picks up where we left off."*

  `/onboard` is self-contained from there.
- **A user pasted the [README](./README.md) into you and asked for help setting up** → the README is self-contained. Adapt to their OS / existing tools / actual work. If they're on macOS and want the canonical install path, you can either walk them through the course (`course/`) lesson by lesson, or skip to the impatient path above.
- **The user is new and you're walking them through the course** → start at [`course/lesson-01-the-hook.md`](./course/lesson-01-the-hook.md). Each lesson is self-contained; the user does them in order.
- **You're working on the repo itself, or running `/update` for Simon** → the rest of this file applies.

The README addresses humans + LLMs + contributors directly; this file is for LLMs operating *inside* the repo (during onboarding, contribution review, or sync runs).

---

## What this repo is

A two-way mirror of Simon Pierce's local Claude Code setup, packaged for the MMF science team and close collaborators. Three canonical locations on Simon's Mac (these paths are Simon's vault layout; contributors don't need to mirror it — the sync scripts only reach into them when run from his machine):

- **Skills** — `~/.claude/skills/`. The vault's `05_SYSTEM/Skills/` has symlinks back there for Obsidian visibility (renamed from `05_AI WORKFLOW/CLAUDE/Skills/` in 2026-05).
- **Templates** — `~/.claude/templates/` (added 2026-04-26). Houses `starter-claude-config/` and `starter-vault/`, the file skeletons `/onboard` installs into newcomers' machines.
- **Guides** — sourced from individual vault process docs at `05_SYSTEM/Processes/`, mapped explicitly per-file via the `GUIDES` array in `sync-from-vault.sh`.

The repo's `skills/`, `guides/`, and `templates/` directories synchronise with these canonical locations via two scripts.

## The sync scripts

- **`sync/sync-from-vault.sh`** — pushes Simon's local changes out to the repo. Pulls `origin/main` first (so recently merged PRs aren't overwritten), sanitises paths, scans for credentials, then commits. Dry-run by default; `--commit` to apply and push.
- **`sync/sync-to-vault.sh`** — pulls merged PRs from the repo back into Simon's local `~/.claude/`. Dry-run by default; `--apply` to copy. Pulls `origin/main` first.

## When /update runs against this repo

Follow this exact sequence. **Do not** run plain `git add` / `git commit` on files in `skills/`, `guides/`, or `templates/` — always go through the sync scripts so the canonical sources stay authoritative.

1. **Pull merged PRs into Simon's local copy.** Run `./sync/sync-to-vault.sh` (dry-run) from the repo root. If anything has merged into the repo that isn't yet in `~/.claude/`, the script lists the differences. Surface the count to Simon in a single line ("N items differ between repo and `~/.claude/` — apply?"). If he agrees, re-run with `--apply`. If he declines or is unsure, stop and let him investigate.
2. **Push Simon's local changes to the repo.** Run `./sync/sync-from-vault.sh --commit` from the repo root. The script pulls `origin/main` first, then copies `~/.claude/` into the repo, commits, and pushes.

Simon has confirmed (2026-04-25) that `/update` runs both steps in order when operating on this repo.

Either script's credential scanner will abort if it detects a token-like pattern in staged content. Fix the offending source file in `~/.claude/` and re-run — do not bypass.

## When a team member opens a PR

Direct merges are fine for any file, including `skills/`, `guides/`, and `templates/`. Review the PR, merge in GitHub's UI. Git history carries the contributor as author.

The `sync-to-vault.sh` script is what brings the merged PR into Simon's local `~/.claude/` so his Claude Code instance picks up the improvement. Either he runs it manually, or `/update` does it next time.

## Conflict case (rare)

If Simon has been editing a skill locally at the same time a contributor has a PR open on the same file, git will flag a merge conflict the next time either sync direction tries to cross. Resolve via standard git workflow (git merge, or edit both sources to converge), then re-run whichever sync was attempting to apply.
