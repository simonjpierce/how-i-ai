---
name: refresh-skills
description: Pull contributor improvements from `mmf-claude-code` into the user's local `~/.claude/`. Two modes — `universal` syncs the 7 starter skills (plus templates and guides) with conflict-walk; `review-installed` diffs each installed on-demand skill against the repo and writes per-skill review reports to the vault inbox (no auto-apply — user triages with their own LLM). Bare `/refresh-skills` runs both. Use when the user says "/refresh-skills", "pull updates", "check for upstream changes", "update my skills", or asks how to get the latest from the team repo.
allowed-tools: Read, Edit, Bash
---

The user-side counterpart to `/onboard`: pull contributor improvements from the public `mmf-claude-code` repo. Two layers, two policies:

- **Universal sync** (the 7 starter skills, plus templates and guides). These came from the same install as everyone else's; upstream improvements should usually land. Same interactive conflict-walk as before — never silently overwrite local edits.
- **Review-installed** (work-specific skills the user installed via `/install-skill`). These often get customised. Upstream changes here are *proposals*, not patches — the skill writes a per-skill diff report to the vault inbox so the user can triage with their own LLM, fold in selectively, and never lose a tweak they wanted to keep.

This skill is a thin orchestrator over `sync-to-vault.sh --filter universal` plus a small diff-report writer for the work-specific side.

The 7 starter skills: `/onboard`, `/document`, `/session-start`, `/update`, `/review-friction`, `/refresh-skills`, `/install-skill`.

## When something goes wrong

If `sync-to-vault.sh` fails for a reason this skill doesn't handle, update this file with what you learned BEFORE continuing the workaround. Add the failure mode, correct wrong assumptions.

## Steps

### 0. Set tab title (Ghostty only)

```bash
[ -d /Applications/Ghostty.app ] && MY_TTY=$(ps -o tty= -p $PPID 2>/dev/null | tr -d ' ') && echo "refresh skills" > "/tmp/claude-title-${MY_TTY}"
```

### 1. Parse mode

The user invocation determines which branch:

- `/refresh-skills universal` → run only the universal sync (steps 3–6)
- `/refresh-skills review-installed` → run only the review-installed report (step 7)
- `/refresh-skills` (no arg) → run both, universal sync first then review-installed report

If the user types an unrecognised mode, list the three options and ask them to pick.

### 2. Locate the repo clone (shared by both modes)

```bash
REPO="$HOME/.claude/repos/mmf-claude-code"
if [ ! -d "$REPO/.git" ]; then
  echo "No clone found at $REPO."
  exit 1
fi
```

If the clone isn't there, ask the user where they cloned it (or offer to clone it at the default location). Don't proceed without a working clone.

### 3. Pull the latest

```bash
cd "$REPO" && git pull --quiet origin main
```

If `git pull` fails (auth, network, divergent), surface the error and stop. Don't try to force-resolve. Branch on mode for what comes next.

---

## Universal sync (mode: `universal` or empty)

### 4. Dry-run with filter

```bash
bash "$REPO/sync/sync-to-vault.sh" --filter universal
```

This prints `[SKILLS]`, `[TEMPLATES]`, `[GUIDES]` sections with `Changed:` and `New:` mappings. SKILLS is narrowed to the 7-skill starter set; templates and guides still sync as usual. Capture the output.

### 5. Triage the diff

Three states:

**State A — No changes** (`"Local paths are in sync with the repo."`)
Tell the user "Universal layer is up to date." Move to the review-installed phase if running combined mode, otherwise exit.

**State B — Only `New:` mappings, no `Changed:`**
No conflict possible. Tell the user the count + names ("3 new things to pull: X, Y, Z. Apply?"). On yes:

```bash
bash "$REPO/sync/sync-to-vault.sh" --filter universal --apply
```

**State C — `Changed:` mappings present**
The user has edited a starter skill / template / guide locally AND the upstream version moved. Walk one at a time per the system's interaction style:

For each conflict:
1. Restate the file: `path` and category.
2. Show the diff (use `diff -u`, cap ~30 lines per file — if longer, summarise and offer "show full diff").
3. Ask with numbered options:
   - **1. Take the repo version** (recommended unless you have edits worth preserving) — back up local copy first
   - **2. Keep my version** — skip in the apply
   - **3. Auto-merge** — invoke the `sync-conflict-merger` subagent (defined at `.claude/agents/sync-conflict-merger.md` in the cloned repo). Produces a merged proposal at `<target>.merge-proposal-<ts>` for human review.
   - **4. Hand-merge later** — back up both versions, skip apply, give the user the comparison paths
4. Apply immediately, then next.

Use `<target>.bak-$(date +%Y%m%d-%H%M%S)` in the same directory for backups.

### 6. Apply resolved set

After all conflicts are resolved:

```bash
bash "$REPO/sync/sync-to-vault.sh" --filter universal --force
```

Files the user chose "Keep my version" for need to be restored from temp save before the `--force` runs (or the apply path can be done per-file via `cp` instead). Verify post-apply that "Keep my version" files match what the user wanted.

---

## Review-installed report (mode: `review-installed` or empty)

The on-demand skills the user installed via `/install-skill` are often customised. Don't sync them. Instead, surface upstream changes as a structured review report for each installed skill that differs from the repo.

### 7. Build the review reports

```bash
STARTER=(onboard document session-start update review-friction refresh-skills install-skill)
INSTALLED_DIR="$HOME/.claude/skills"
REPO_SKILLS="$REPO/skills"
VAULT_INBOX=""   # populated from per-vault config — see step 7a

# Determine vault inbox: read folders.inbox from per-vault config.json,
# default "INBOX". Then VAULT_INBOX="<vault.path>/<folders.inbox>".
```

**7a. Resolve the vault inbox path** from `~/.claude/projects/<key>/config.json`:

```bash
read VAULT_ROOT INBOX_REL <<<"$(python3 - <<'PYEOF' 2>/dev/null
import json, glob, os
for p in sorted(glob.glob(os.path.expanduser("~/.claude/projects/*/config.json"))):
    try:
        cfg = json.load(open(p))
        v = cfg.get("vault", {}).get("path", "").strip()
        if v:
            i = cfg.get("folders", {}).get("inbox", "INBOX")
            print(v, i)
            break
    except Exception:
        pass
PYEOF
)"
VAULT_INBOX="$VAULT_ROOT/$INBOX_REL"
mkdir -p "$VAULT_INBOX"
```

If no config has a vault path, ask the user where to write reports. Don't write to repo or to `~/.claude/`.

**7b. Iterate installed work-specific skills**:

```bash
TODAY=$(date +%F)
REPORTS_WRITTEN=()
for skill_dir in "$INSTALLED_DIR"/*/; do
  name="$(basename "$skill_dir")"
  # Skip starter skills (handled by universal sync above).
  is_starter=false
  for s in "${STARTER[@]}"; do [[ "$s" == "$name" ]] && is_starter=true && break; done
  $is_starter && continue
  # Skip skills that don't exist in the repo (user authored locally, not a fork).
  [[ -f "$REPO_SKILLS/$name/SKILL.md" ]] || continue
  # Skip skills with no diff.
  if diff -rq "$skill_dir" "$REPO_SKILLS/$name/" >/dev/null 2>&1; then
    continue
  fi
  # Write report.
  REPORT="$VAULT_INBOX/skill-review-$name-$TODAY.md"
  {
    echo "# Skill review — /$name — $TODAY"
    echo ""
    echo "Upstream \`mmf-claude-code\` has changes to \`/$name\` since you installed it. **This report is for human + LLM review — don't apply blindly.** The skill ships with your customisations; upstream improvements may or may not be worth folding in."
    echo ""
    echo "## How to review"
    echo ""
    echo "Open this file in your Claude Code session and ask:"
    echo ""
    echo "> *Read this diff. Which upstream changes look like genuine improvements I should fold into my local \`~/.claude/skills/$name/SKILL.md\`, and which would break workflows I've customised? Propose specific edits for the changes worth taking.*"
    echo ""
    echo "Then apply the fold-ins manually, or ask Claude to apply specific changes."
    echo ""
    echo "## Files"
    echo ""
    echo "- Local: \`~/.claude/skills/$name/SKILL.md\`"
    echo "- Repo: \`$REPO_SKILLS/$name/SKILL.md\`"
    echo "- Latest repo commit touching this skill:"
    echo ""
    echo "  \`\`\`"
    (cd "$REPO" && git log -1 --format='  %h  %ad  %s' --date=short -- "skills/$name/") 2>/dev/null
    echo "  \`\`\`"
    echo ""
    echo "## Diff"
    echo ""
    echo '```diff'
    diff -ur "$skill_dir" "$REPO_SKILLS/$name/" 2>/dev/null | head -400
    echo '```'
    echo ""
    echo "_Diff capped at 400 lines. If you need to see more, run \`diff -ur ~/.claude/skills/$name/ $REPO_SKILLS/$name/\` directly._"
  } > "$REPORT"
  REPORTS_WRITTEN+=("$REPORT")
done
```

**7c. Summarise to the user**:

If `REPORTS_WRITTEN` is empty:

> *"No installed on-demand skills have upstream changes. Nothing to review."*

If non-empty:

> *"Wrote {N} skill review reports to your inbox. Open the first one in Obsidian, paste the suggested prompt into a fresh Claude Code session, and triage with the LLM. Fold in or skip per-change."*

List each report with the wikilink:

```bash
for r in "${REPORTS_WRITTEN[@]}"; do
  rel="${r#$VAULT_ROOT/}"
  echo "  - obsidian://open?vault=...&file=$(python3 -c 'import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1].rsplit(".md",1)[0], safe="/"))' "$rel")"
done
```

Open the first one in Obsidian via `open obsidian://open?vault=...` for immediate visibility.

---

## Combined mode (no arg)

Run universal sync (steps 3–6), then review-installed report (step 7). Final summary covers both.

## Guidelines

- **Universal layer is for upstream improvements; work-specific layer is for user customisation.** The two policies reflect that.
- **Never silently overwrite a work-specific skill.** Diff reports for human + LLM triage; never auto-apply.
- **Never silently overwrite a starter skill either.** Conflict-walk gives the user control even on the universal layer.
- **The dry-run is read-only and safe to re-run any time.**
- If `git pull` produces merge conflicts in the repo clone itself (rare), surface and stop. User resolves with standard git workflow.

## Post-run improvement

After a refresh, briefly assess:
- Did any conflict prompt confuse the user? Better wording?
- Was the 30-line per-file diff cap right, or did the user need more context?
- Did the per-skill review report's suggested-prompt phrasing actually help the user's downstream Claude session, or did they need to rewrite it?
- Did `sync-to-vault.sh` produce any unexpected output the skill should learn to handle?

Update this skill if patterns emerge.
