---
name: update
description: Update all documents associated with the current work to reflect current state. Scans for related process docs, project notes, skills, CLAUDE.md files, and working files, then brings them current. Use when the user says "/update", "update the docs", "bring docs current", or "sync the documentation".
allowed-tools: Read, Write, Edit, Glob, Grep, Agent, Bash
---

Bring all documentation associated with the current project or session up to date. This skill exists because associated documents (process docs, project notes, skills, cross-references) silently drift out of date during interactive work. A single invocation audits and updates them all.

**Arguments**: Optional — a project name, topic, or file path to scope the update. If omitted, infers scope from the current session context (files read/edited, topics discussed).


## When something goes wrong

When a step in this skill fails or needs a workaround, update this skill file with what you learned BEFORE continuing to the next step. Add failure modes, correct wrong assumptions, fix timing estimates. This takes 30 seconds and prevents the same friction next time.


## Steps

### Pre-flight: MEMORY.md health check

Before any steps, run:

```bash
MEMORY_FILE="$HOME/.claude/projects/-Users-simonjpierce-Library-Mobile-Documents-iCloud-md-obsidian-Documents-Simon-s-Vault/memory/MEMORY.md"
LINES=$(wc -l < "$MEMORY_FILE")
BYTES=$(wc -c < "$MEMORY_FILE")
echo "MEMORY.md: $LINES lines, $BYTES bytes (caps: 200 / 25600)"
```

If `$LINES > 150` or `$BYTES > 20000`, warn Simon: "MEMORY.md approaching loader cap — any new rules added this session should go in Tier 2 leaves (`memory/feedback_*.md`), not Tier 1 inline." See `Processes/CLAUDE.md and MEMORY.md Maintenance.md` for the two-tier convention.

If within budget, proceed silently — no need to report the numbers unless asked.

### Phase 1 — Scope and discover

1. **Determine scope**. One of:
   - **Explicit argument** — the user passed a project name, topic, or file path. Use it as the primary search seed.
   - **Session context** — no argument. Scan the conversation for: files read/edited, topics discussed, decisions made, tools/workflows mentioned. Extract 3–8 keyword seeds.

2. **Check for an `## Artifacts` section** in the primary process/analysis note for this work. If present, this is the **authoritative checklist** — iterate its rows as the document list. The Artifacts table is a maintained index of all related docs, scripts, repos, folders, and other artifacts. Trust it over ad-hoc scanning.

   **If no Artifacts section exists**, fall back to the category search below.

   **If an Artifacts section exists but seems incomplete** (e.g., the session created files not listed), update the Artifacts table first, then use the updated list.

3. **Find associated documents** (fallback when no Artifacts section). Using the seeds from step 1, search for related docs across these categories:

   | Category | Where to look | What to check |
   |----------|--------------|---------------|
   | Process docs | `05_AI WORKFLOW/CLAUDE/Processes/` | Grep for seed keywords |
   | Skills | `05_AI WORKFLOW/CLAUDE/Skills/*/SKILL.md` | Grep for seed keywords |
   | Project notes | `02_MARINE MEGAFAUNA/`, `03_PLANET OCEAN/`, `01_LIFE OS/` | QMD lex query or Grep |
   | CLAUDE.md files | Folder-level CLAUDE.md files in relevant domains | Read if domain was touched |
   | Role notes | `01_LIFE OS/Roles/` | If role-relevant work was done |
   | Working files | Paths from conversation context | Files actively being developed |
   | Scheduled Automations | `05_AI WORKFLOW/CLAUDE/Processes/Scheduled Automations.md` | If any automation was changed |
   | MEMORY.md | Auto-memory index | If a remembered fact was invalidated |
   | Current Projects | `01_LIFE OS/Current Projects.md` | If project status changed |

   Use parallel searches (Grep/Glob/QMD) to build the candidate list quickly. Include files from the conversation that were edited but might have upstream/downstream docs.

4. **Read each candidate**. For each document found, read it and assess:
   - Is anything **stale** (describes old state, wrong paths, outdated status)?
   - Is anything **missing** (new information from this session that belongs here)?
   - Is anything **inconsistent** (contradicts what was just done or decided)?
   - Is any cross-reference **broken** (links to moved/renamed/deleted files)?

   Skip documents that are already current — don't update for the sake of updating.

### Phase 2 — Classify and present

4. **Classify each update** into one of two categories:

   **Auto-update** (just do it) — mechanical changes that don't require judgement:
   - Fixing file paths, cross-references, and wikilinks
   - Updating status fields (e.g., "draft" → "complete")
   - Adding new entries to lists (e.g., a new automation to Scheduled Automations)
   - Correcting factual errors (dates, versions, tool names)
   - Removing references to deleted/archived content
   - Updating "Last updated" dates

   **Review** (pause for Simon) — content changes that involve judgement:
   - Rewriting descriptions or explanations
   - Removing content (even if it seems outdated)
   - Changing scope, priorities, or strategic framing
   - Adding new sections or substantially expanding a document
   - Modifying tone, voice, or audience targeting
   - Anything where reasonable people might disagree on the right update

   **When in doubt, classify as Review.** The cost of asking is low; the cost of an unwanted content change is high.

5. **Present the hit list**. Show Simon a compact summary:

   ```
   ## Documents to update

   ### Auto-updates (will apply now)
   - `Processes/Foo.md` — update file path from old → new
   - `Skills/bar/SKILL.md` — add step for new edge case discovered
   - ...

   ### For your review
   - `Project Note X.md` — status section describes Phase 1 as "in progress" but it's now complete. Proposed: rewrite status to reflect Phase 2 start.
   - ...

   ### Already current (no changes needed)
   - `CLAUDE.md` (02_MARINE MEGAFAUNA) — checked, nothing stale
   - ...
   ```

   If there are no review items, skip straight to execution. If there are only 1–2 auto-updates and no review items, just do them and report — don't present a menu for trivial updates.

### Phase 3 — Execute

6. **Apply auto-updates**. Use Edit for targeted changes. For documents that need multiple changes, read the full file first to avoid conflicts. If a document needs more than ~5 edits, consider whether a rewrite is cleaner (but still use Edit, not Write, to preserve surrounding content).

7. **Handle review items**. Present each review item one at a time with:
   - The current text (relevant excerpt)
   - The proposed change
   - Why the change is needed

   Wait for Simon's approval, modification, or rejection before proceeding to the next item. Apply approved changes immediately.

8. **Cross-reference check**. After all updates are applied, do a quick sweep:
   - Did any update change a file path or heading that other docs link to?
   - Did any update change a process that a skill references?
   - If so, cascade the fix.

9. **Code backup check**. If the session created or modified scripts, analysis code, or data outputs:
   - Check `git status` in each relevant repo for uncommitted changes.
   - Check whether the repo has a GitHub remote (`git remote -v`).
   - **If scripts/outputs exist outside any repo** (e.g., on Desktop, in a project folder): assess whether a GitHub repo would be useful. It is if there are ≥2 scripts or the analysis is non-trivial. If so, **create a private repo** on Simon's GitHub (`gh repo create simonjpierce/<name> --private`), initialize locally, add relevant files (scripts, cleaned data, outputs — not raw data from third-party papers), commit, push, and update the Artifacts table with the new repo path.
   - **If repo exists but has uncommitted or unpushed changes**: stage, commit with a descriptive message, and push. /update is an implicit request to bring everything current — that includes the repo.
   - **Mixed authorship — split commits**: If the staging area mixes your edits with pre-existing uncommitted Simon edits (files changed before this session started, or files Simon edited mid-session that you didn't touch), split into TWO commits before pushing — his changes first with a clear attribution (no `Co-Authored-By: Claude` line, short descriptive message), then yours (with the `Co-Authored-By` line). This keeps `git blame` clean and respects the Commit authorisation section of global CLAUDE.md. Identify his edits by running `git diff --stat` on the staged files and asking: did the session touch this file? If no, it's his.
   - **Figure sync**: If the repo has a `sync_figures.sh` script (created by `/science-paper`), run it to copy figures from `outputs/` to the vault figures folder and Google Drive. Do this before committing so the vault copy is current.
   - Repos to check: any path mentioned in the session's Artifacts tables or file edits under `~/repos/`.
   - **`~/.claude/` repo**: If the session modified skills, hooks, or settings in `~/.claude/`, commit and push to `simonjpierce/claude-code-config`. This is infrastructure — don't wait for the 05:30 catch-up push. Run: `cd ~/.claude && git add -A && git diff --cached --quiet || git commit -m "auto: [brief description]" && git push origin main`.
   - **Check current branch before committing.** Run `git branch --show-current` in each repo first. If HEAD is NOT on `main`, a naïve commit lands on the side branch (e.g. a `workhorse/regression-*` branch from a recent workhorse run) and your fix never ships. Default flow: stash ALL pending working-tree changes with bare `git stash push -u -m "tmp"` (do NOT pass `-- <path>` — partial stash leaves other dirty tracked files that will block `git checkout main`, and a later `stash pop` will hit merge conflicts when main has moved on for the same paths), `git checkout main`, stage your file and commit there, push, `git checkout <original-branch>`, `git stash pop`. Failure history: 2026-04-21 /update + /document, 2026-04-24 (this turn) — all hit the same wrong-branch landing.
     - **Cherry-pick salvage.** If you've already committed on the wrong branch before noticing, recover with: stash any conflicting working-tree changes (bare `git stash push -u`), `git checkout main`, `git cherry-pick <hash>`, push, return to the original branch, pop the stash, drop the now-redundant stash on the old branch. Tonight's run did this twice — works but adds friction. Better: check the branch first.
     - **Mixed-authorship + wrong-branch combo.** If pre-existing dirty files in the working tree are Simon's (not from this session), and a bare stash would lump them in with yours, use the split-stash dance: (1) `git stash push -m "claude" -- <your-file>`; (2) `git stash push -m "simon"` for the rest; (3) `git checkout main`; (4) `git stash pop stash@{1}` (yours, now at index 1); (5) commit + push; (6) `git checkout <original-branch>`; (7) `git stash pop stash@{0}` to restore Simon's work. Verify with `git stash list` between pops — the index shifts. Only needed when authorship matters; for ordinary cleanup the bare-stash flow above is simpler.

### Phase 4 — Report

10. **Summary**. Brief report of what was updated:
   - Count of auto-updates applied
   - Review items: approved/modified/skipped
   - Any cascading fixes from cross-reference check
   - Documents checked but not changed

   Keep it to 5–10 lines unless the update was large.


## Scaling behaviour

- **Small scope** (1–3 docs): Do everything inline, no subagents needed.
- **Medium scope** (4–8 docs): Use parallel reads but update sequentially.
- **Large scope** (9+ docs): Spawn sonnet subagents for parallel scanning in Phase 1, then update sequentially in Phase 3.


## Guidelines

- **Don't update for the sake of updating.** Only change docs where the content is actually wrong or missing. "Could be better" is not a reason to edit during an /update pass.
- **Preserve voice and style.** Match the existing document's tone when adding content. Don't homogenise.
- **Append, don't rewrite.** Prefer adding to existing text over restructuring, unless the structure is genuinely broken.
- **Timestamp awareness.** If a document has a "Last updated" or "Status" field, update it. If it doesn't, don't add one just because.
- **Don't create new documents.** This skill updates existing docs. If a new doc is needed, flag it to Simon.
- **Respect protected sections.** Some docs have sections that shouldn't be touched (e.g., Current Projects' "Life razor" section). Check folder CLAUDE.md files for any such rules.
- **Maintain the Artifacts section.** If the primary note has an `## Artifacts` table, check whether any files created or modified during this session are missing from it. Add them. If the note doesn't have an Artifacts section yet but has 5+ related files, consider adding one (classify as Review — let Simon decide). The Artifacts table is the contract between interactive work and /update: work adds rows, /update reads them. Include cross-cutting docs (skill specs, process docs) that are being refined alongside the project, not just project-specific files.


## Post-run integrity checks

Before declaring the update complete, verify:
- **Commit landing site.** For every repo committed this run, did the commit land on `main` (`git log --oneline -1 main | grep <hash>`)? If it landed on a side branch, cherry-pick to main and push before reporting done.
- **Cross-reference cascade.** Did any path/heading changes made this run need to propagate to other docs that weren't in the candidate list? Quick grep over the session's edited-path seeds.
- **New failure modes.** Did anything fail in a way not already documented in this skill? If yes, add a new sub-bullet under the relevant step BEFORE reporting done (per the #1 rule).

## Post-run improvement

After completing the update pass, briefly assess:
- Were any documents missed that should have been found?
- Did the classification (auto vs review) feel right, or was Simon surprised by anything?
- Were the search seeds effective, or did important docs slip through?

If patterns emerge, update this skill with better search heuristics or classification rules.
