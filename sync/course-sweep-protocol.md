# Course-sweep protocol

Followed by Claude when `/update` or `/document` reach their post-sync step. Keeps the `course/` folder in lockstep with the `skills/` folder: when a starter skill changes, propose lesson edits; when a new local skill ships, scaffold a lesson; when a skill is retired, archive the lesson.

This is a **documented protocol**, not a shell script — too much branching, prompting, and cross-doc updating for shell to be the right substrate.

## When this fires

`/document` and `/update` both invoke `mmf-claude-code/sync/sync-from-vault.sh --commit` when they detect uncommitted skill / template / guide changes in `~/.claude/`. The caller wraps the sync with HEAD capture and then invokes this protocol with four inputs:

- `REPO_ROOT` — absolute path to the local `mmf-claude-code` clone (typically `~/.claude/repos/mmf-claude-code/` or `~/repos/mmf-claude-code/`).
- `CALLER` — `"update"` or `"document"` (used in the sweep summary).
- `PRE_SYNC_HEAD` — `git rev-parse HEAD` captured BEFORE `sync-from-vault.sh --commit` ran.
- `POST_SYNC_HEAD` — `git rev-parse HEAD` captured AFTER the sync returned (may equal `PRE_SYNC_HEAD` if there was nothing to sync).

If `PRE_SYNC_HEAD == POST_SYNC_HEAD` AND there are no new local skills not yet in sync mappings AND no skills marked for deletion, exit silently — no sweep work to do.

## Detection — three signals

```bash
# (a) Modified or deleted mapped skills, from PRE/POST diff:
if [ "$PRE_SYNC_HEAD" != "$POST_SYNC_HEAD" ]; then
  CHANGED_SKILLS=$(git -C "$REPO_ROOT" diff --name-status \
    "$PRE_SYNC_HEAD..$POST_SYNC_HEAD" -- 'skills/*/SKILL.md')
  # Yields lines like: M skills/research/SKILL.md, D skills/old-thing/SKILL.md
fi

# (b) New local skills not yet in sync mappings.
MAPPED_SKILLS=$(awk '/^SKILLS=\(/,/^\)/' "$REPO_ROOT/sync/sync-from-vault.sh" \
  | grep -oE '\$CLAUDE_CONFIG/skills/[a-z0-9-]+' \
  | sed 's|.*/skills/||' \
  | sort -u)

LOCAL_SKILLS=$(find "$HOME/.claude/skills" -mindepth 2 -maxdepth 2 -name SKILL.md \
  | xargs -n1 dirname \
  | xargs -n1 basename \
  | sort -u)

# Filter out previously-declined skills
PROJECT_KEY=$(pwd | sed 's|[^a-zA-Z0-9]|-|g')
DECLINED=$(jq -r '.course.declined_local_skills // [] | .[]' \
  "$HOME/.claude/projects/$PROJECT_KEY/config.json" 2>/dev/null | sort -u)

NEW_LOCAL=$(comm -23 <(echo "$LOCAL_SKILLS") <(echo "$MAPPED_SKILLS"))
NEW_LOCAL=$(comm -23 <(echo "$NEW_LOCAL") <(echo "$DECLINED"))

# (c) Newly added mapped skills (status A from PRE/POST diff) are handled
# by signal (a) above; no separate detection needed.
```

The `find` filter at depth 2 ensures only directories containing a `SKILL.md` count as skills; dot-directories and caches are excluded.

`origin/main` is not used for detection — `sync-from-vault.sh` pushes to `origin/main` itself, so post-push `origin/main` matches `HEAD`.

## Modified skill flow (`M`)

Mapped skills don't all have one-to-one course lessons. Current state: 16 mapped skills (`sync-from-vault.sh` SKILLS array) — `transcribe`, `red-team`, `pdf-to-markdown`, `update`, `document`, `verify-citations`, `mmf-brand`, `onboard`, `review-friction`, `session-start`, `refresh-skills`, `polish`, `todo`, `science-paper`, `research`, `install-skill`. 10 numbered course lessons currently exist; skills without lessons (`mmf-brand`, `polish`, `refresh-skills`, `review-friction`, `install-skill`) appear elsewhere (graduation page, lesson-05's `/onboard` reference) or are pure infrastructure with no user-visible course surface.

For each `M`-status skill `<name>`:

**Branch 1 — course lesson exists** (`course/lesson-NN-<name>.md`):
- Read both the current SKILL.md and the lesson.
- Diff the skill against the pre-sync HEAD to identify substantive changes (new behaviour, dropped behaviour, new prerequisite, new failure mode).
- Propose specific lesson edits inline. Surface one at a time for the user's per-prompt decision (per the system's interaction style — never bundle).
- On substantive update, add a staleness marker to the lesson's video block (top of file, matching the existing pattern at `course/lesson-10-update.md:3-5`): *"(video may be out of date — re-record if substantive change)"*.

**Branch 2 — listed in graduation's optional-skills section** (`course/graduation.md`):
- Read the skill diff. If the description, dependencies, or invocation changed in ways affecting the graduation entry, propose updating that entry. Otherwise skip silently.

**Branch 3 — lesson-05 references it as part of `/onboard`** (only the `onboard` skill itself):
- Propose updating `course/lesson-05-your-claude-md.md` if the user-visible behaviour described in the lesson has changed.

**Branch 4 — infrastructure with no user-visible course surface** (`refresh-skills`, `review-friction`, `polish` when not in graduation, `install-skill` when not in graduation):
- Skip with reason logged to the sweep summary. No user prompt. These skills don't have a course representation.

Stage and commit each updated file with explicit pathspec (one commit per branch-1 lesson; one commit covering graduation + lesson-05 if those branches fire).

## New local skill flow (signal b)

**Critical about sync commit scope**: `sync-from-vault.sh --commit` stages only `skills/`, `guides/`, `templates/` target dirs and pushes that commit. **It does not stage `sync/*.sh` edits.** Mapping additions must be committed separately by the sweep, BEFORE re-running the sync.

Order of operations:

1. For each new local skill not in mappings and not in `course.declined_local_skills`:

   Prompt: *"`/<name>` is a new local skill (at `~/.claude/skills/<name>/`). Want to ship it via the team repo?"*

   - **If no**: append `<name>` to `~/.claude/projects/<key>/config.json`'s `course.declined_local_skills` list. Skip to next new skill.
   - **If yes**: continue to step 2.

2. Propose the exact lines to add to `sync-from-vault.sh`'s and `sync-to-vault.sh`'s `SKILLS` arrays. Show as diff. On user approval, edit both files.

3. **Commit the mapping edits first**, with explicit pathspecs:

   ```bash
   cd "$REPO_ROOT"
   git add sync/sync-from-vault.sh sync/sync-to-vault.sh
   git commit -m "Add /<name> to sync mappings"
   git push origin main
   ```

4. **Re-invoke `sync-from-vault.sh --commit`** to ship the new skill itself. Capture the new POST_SYNC_HEAD; the new skill should appear as `A` in the diff against the original PRE_SYNC_HEAD.

5. Prompt: *"Want a course lesson for `/<name>`?"* Options:
   - `1. Universal (Part 1)` — fits the starter system-management track
   - `2. Writing/research (Part 2)` — fits the work-specific writing/research track
   - `3. Science (Part 2)` — fits the analysis/manuscript track
   - `4. No lesson — just list in graduation`

6. Scaffold or update appropriately:

   **Lesson branch** (options 1–3):
   - Scaffold `course/lesson-NN-<name>.md` (NN = current max + 1, append-only) from `course/lesson-template.md`.
   - Update `course/README.md` TOC (add under the chosen track's visual grouping, even though NN > 16).
   - Update root `README.md` TOC mirror similarly.
   - Update `course/graduation.md` if the new skill displaces an item previously in optional-skills.
   - Update predecessor-lesson navigation: the last lesson in the chosen track has a "What's next" pointer that needs to include the new lesson.

   **No-lesson branch** (option 4):
   - Skip lesson creation.
   - Update `course/graduation.md` to add `<name>` to the relevant "Optional skills (not in the course)" section.

7. Commit with explicit pathspec:

   Lesson branch:
   ```bash
   git add course/lesson-NN-<name>.md course/README.md README.md course/graduation.md \
           course/lesson-<prev_in_track>-*.md
   git commit -m "Add course/lesson-NN for new /<name> skill"
   git push origin main
   ```

   No-lesson branch:
   ```bash
   git add course/graduation.md
   git commit -m "Add /<name> to graduation optional skills"
   git push origin main
   ```

## Deleted skill flow (`D`)

`sync-from-vault.sh` aborts `--commit` if a mapped source is missing unless `--allow-missing` is passed. The default sync path won't fire this flow; the user must explicitly run with `--allow-missing` when they've removed a skill locally.

When `--allow-missing` was used (or when the protocol is invoked specifically to retire a skill):

1. For each `D`-status entry in the PRE/POST diff: locate the orphaned lesson at `course/lesson-NN-<name>.md` if it exists.

2. Prompt: *"`/<name>` has been removed. Archive the lesson and clean up sync mappings?"*

3. If yes:
   - `mkdir -p course/_archived/` (creates the folder on first deleted-skill flow if absent)
   - `git mv course/lesson-NN-<name>.md course/_archived/` (if lesson exists)
   - Remove `<name>` line from `sync-from-vault.sh`'s `SKILLS` array.
   - Remove `<name>` line from `sync-to-vault.sh`'s `SKILLS` array.
   - Update `course/README.md`, root `README.md`, `course/graduation.md` to remove references.
   - Update predecessor-lesson navigation if the archived lesson was the target of a "What's next" pointer.

4. Stage and commit with explicit pathspecs:

   ```bash
   git add sync/sync-from-vault.sh sync/sync-to-vault.sh \
           course/_archived/lesson-NN-<name>.md course/README.md README.md course/graduation.md \
           course/lesson-<prev_in_track>-*.md
   git commit -m "Retire /<name>: archive lesson and remove sync mappings"
   git push origin main
   ```

## Commit policy

Course-sweep work produces multiple commits, each with **explicit pathspecs** (never `git add .` or `git add course/`). One commit per logical change:

- Modified-skill lesson update: one commit per affected lesson.
- New-skill mapping addition: one commit (`sync/*.sh` only).
- New-skill ship: handled by `sync-from-vault.sh --commit` (one auto-commit for the new `skills/<name>/`).
- New-skill lesson creation: one combined commit covering `course/lesson-NN-*.md` + TOCs + predecessor-lesson nav.
- New-skill no-lesson classification: one commit (`graduation.md` only).
- Deleted-skill retirement: one combined commit (mapping removal + lesson archive + TOC updates + predecessor nav).

After all sweep commits land, push to `origin/main` (or batch a final push if the sweep ran multiple commits — same effect).

## Numbering policy

**Append-only at the end of the overall list.** Tracks (Part 1 universal, Part 2 writing/research, Part 2 science) become loose visual groupings in `course/README.md` rather than contiguous numbered ranges. Existing cross-links don't break.

When a new lesson lands at NN:
- Update `course/README.md`'s TOC to show it under the chosen track visual grouping.
- Update root `README.md`'s TOC mirror similarly.
- Update the LAST lesson in the chosen track's "What's next" pointer to include the new lesson option.

When a lesson at NN is archived:
- Remove from TOCs.
- If predecessor lesson(s) reference it in "What's next", update those references (point to the next-in-track lesson, or to graduation if archived lesson was end-of-track).

## Configuration

`~/.claude/projects/<key>/config.json` gains the key:

```json
{
  "course": {
    "declined_local_skills": []
  }
}
```

Populated by the new-skill flow when the user says no. The sweep filters this array out of `NEW_LOCAL` on subsequent runs so declined skills don't re-prompt.

If a user later changes their mind, they edit the array directly in `config.json` (remove the entry), or ask Claude to ship a previously-declined skill explicitly.

## Final summary

After the sweep completes, surface a single-block summary in the caller's report:

```
Course sweep ($CALLER):
- Modified skills processed: N (M=branch-1 lesson updates, K=skipped infrastructure)
- New local skills: N (shipped + scaffolded), N (declined and recorded)
- Deleted skills retired: N
- Total commits this sweep: N
```

If the sweep was a no-op (silent exit per "When this fires"), don't add this section.

## Out of scope (v2)

- `guides/`, `templates/` sweeps. Add if `skills/` sweep proves valuable in practice.
- Heuristic classification of substantive-vs-cosmetic skill changes — user's per-prompt decision IS the gate.
- Automatic backlog of declined personal skills — sweep records the declined name and moves on; user re-engages by editing `config.json` or asking Claude to.
- Hooks that fire the sweep on every file save. Sweep runs only when `/update` or `/document` runs.
