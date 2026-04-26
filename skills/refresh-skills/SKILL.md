---
name: refresh-skills
description: Pull contributor improvements from `mmf-claude-code` into the user's local `~/.claude/`. Walks through any conflicts with their own local edits, never silently overwrites. Use when the user says "/refresh-skills", "pull updates", "check for upstream changes", "update my skills", or asks how to get the latest improvements from the team repo.
allowed-tools: Read, Edit, Bash
---

The user-side counterpart to `/onboard`: pull down contributor improvements from the public `mmf-claude-code` repo into the user's local `~/.claude/skills/` and `~/.claude/templates/` without losing their personalisations. The hard part is conflict handling — when both the user and a contributor have edited the same file, the user decides what to do.

This skill is a thin orchestrator over `sync-to-vault.sh`. The script does the actual work; this skill makes the conflict-halt path navigable for the user.

## When something goes wrong

If `sync-to-vault.sh` fails for a reason this skill doesn't handle, update this file with what you learned BEFORE continuing the workaround. Add the failure mode, correct wrong assumptions.

## Steps

### 0. Set tab title (Ghostty only)

```bash
[ -d /Applications/Ghostty.app ] && MY_TTY=$(ps -o tty= -p $PPID 2>/dev/null | tr -d ' ') && echo "refresh skills" > "/tmp/claude-title-${MY_TTY}"
```

### 1. Locate the local clone

The default location is `~/.claude/repos/mmf-claude-code/` (set by `/onboard`'s bootstrap step).

```bash
REPO="$HOME/.claude/repos/mmf-claude-code"
if [ ! -d "$REPO/.git" ]; then
  echo "No clone found at $REPO."
  exit 1
fi
```

If the clone isn't there, ask the user where they cloned it (or offer to clone it for them at the default location). Don't proceed without a working clone.

### 2. Pull the latest

```bash
cd "$REPO" && git pull --quiet origin main
```

If `git pull` fails (auth issue, network, divergent branches), surface the error and stop. Don't try to force-resolve.

### 3. Dry-run sync-to-vault to surface diffs

```bash
bash "$REPO/sync/sync-to-vault.sh"
```

This prints `[SKILLS]`, `[TEMPLATES]`, `[GUIDES]` sections with `Changed:` and `New:` mappings. Capture the output; you'll use it to drive the next step.

### 4. Triage the diff

Three states:

**State A — No changes ("Local paths are in sync with the repo").**
Tell the user "You're already up to date. No upstream changes to pull." Exit. Done.

**State B — Only `New:` mappings, no `Changed:`.**
These are skills, templates, or guides that don't exist locally yet — no conflict possible. Tell the user the count and the names ("3 new skills available: X, Y, Z. Apply?"). On yes, run:

```bash
bash "$REPO/sync/sync-to-vault.sh" --apply
```

Tell the user to restart Claude Code so the new skills are discovered.

**State C — `Changed:` mappings present.**
These are files the user has edited locally AND that have moved upstream. The script's `--apply` mode will halt on these by design. Walk the user through them **one at a time** per the system's interaction style:

For each conflict:
1. Restate the file: `path:N` and what category (skill, template, guide).
2. Show the diff between the user's local copy and the repo version. Use `diff -u` for context, but cap at ~30 lines per file — if longer, summarise and offer "show full diff" as an option.
3. Ask the user which to take, with these numbered options:
   - **1. Take the repo version** (recommended unless the user has unique local edits worth preserving) — back up the user's copy first, then accept the upstream version
   - **2. Keep my version** — skip this file in the apply
   - **3. Hand-merge later** — back up both versions to a known location, skip the apply, give the user paths to compare
4. Apply the choice immediately for that file, then move to the next.

For backups, use `<target>.bak-$(date +%Y%m%d-%H%M%S)` in the same directory.

### 5. Apply the resolved set

After all conflicts are resolved, run the script with `--force` (since the user has explicitly accepted each "take theirs" decision):

```bash
bash "$REPO/sync/sync-to-vault.sh" --force
```

The script copies the staged content into `~/.claude/`. Files the user chose "Keep my version" for were never staged because the user's local copy still differs from staged — `--force` would clobber them. So before running `--force`, restore the user's local copy of any "Keep my version" files from a temp save (alternative: copy the user's local file over the staged version in a temp dir before invoking the script). Whichever mechanism you use, verify post-apply that "Keep my version" files match what the user wanted.

If this gets fiddly, the safer fallback is per-file `cp`: after dry-run, manually copy the staged-and-desanitised content into place for "Take theirs" files, leave "Keep my version" alone. The script's `apply_mapping` function shows the path mapping if needed.

### 6. Confirm and close

Brief summary:

```
Refresh complete.
Pulled: <N commits since last refresh>
Applied: <count> upstream updates
Kept local: <count> files unchanged
Backed up: <count> .bak files saved
```

Tell the user to restart Claude Code so any new or updated skills are discovered.

## Guidelines

- This skill is portable — same behaviour for Simon and for newcomers. There is no `is_simon` gate here; both pull from the same public repo.
- Never silently overwrite. Every "take theirs" decision is the user's, made one file at a time.
- The dry-run is read-only and safe to re-run any time. Use it freely.
- If `git pull` produces merge conflicts in the repo clone itself (rare — only if the user has been editing the cloned repo directly), surface those and stop. The user resolves with standard git workflow.

## Post-run improvement

After completing a refresh, briefly assess:
- Did any conflict-resolution prompt confuse the user? Better wording?
- Were the diffs the right size to digest, or was the 30-line cap too restrictive?
- Did `sync-to-vault.sh` produce any unexpected output the skill should learn to handle?

Update this skill if patterns emerge over multiple refreshes.
