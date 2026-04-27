#!/bin/bash
# dogfood-onboard.sh — release-gate test for the v0 onboarding flow.
#
# Verifies every file the kickoff note promises actually lands when bootstrap.sh
# runs against a clean environment and /onboard's template-substitution logic is
# replayed against canned interview answers. Runs in an isolated throwaway HOME
# so it can't touch the real ~/.claude/ or any real vault.
#
# Exit 0 = release-ready. Non-zero = something is missing, mis-substituted, or
# broken. Run before any external Slack invite.
#
# Usage:
#   ./tests/dogfood-onboard.sh              # runs and reports
#   ./tests/dogfood-onboard.sh --keep       # don't delete the throwaway dirs
#                                              (for inspection after a failure)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
KEEP_ARTIFACTS=false
[[ "${1:-}" == "--keep" ]] && KEEP_ARTIFACTS=true

# --- Isolated environment -----------------------------------------------------
DOGFOOD_ROOT="$(mktemp -d -t dogfood-onboard-XXXXXX)"
FAKE_HOME="$DOGFOOD_ROOT/home"
FAKE_VAULT="$DOGFOOD_ROOT/vault"
mkdir -p "$FAKE_HOME" "$FAKE_VAULT"

cleanup() {
  if [[ "$KEEP_ARTIFACTS" == "true" ]]; then
    echo "Artifacts kept at: $DOGFOOD_ROOT"
  else
    rm -rf "$DOGFOOD_ROOT"
  fi
}
trap cleanup EXIT

PASS=0
FAIL=0
FAILURES=()

check() {
  local label="$1"
  local condition="$2"
  if eval "$condition"; then
    PASS=$((PASS + 1))
    echo "  ✓ $label"
  else
    FAIL=$((FAIL + 1))
    FAILURES+=("$label")
    echo "  ✗ $label"
  fi
}

# --- Phase 1: bootstrap.sh against fake HOME ---------------------------------
echo "Phase 1 — bootstrap.sh against isolated HOME=$FAKE_HOME"
HOME="$FAKE_HOME" bash "$REPO_ROOT/sync/bootstrap.sh" --yes >/dev/null

echo ""
echo "  Skills installed:"
for skill in onboard document session-start update review-friction refresh-skills todo science-paper research verify-citations; do
  check "skills/$skill/SKILL.md present" \
    "[[ -f '$FAKE_HOME/.claude/skills/$skill/SKILL.md' ]]"
done

echo ""
echo "  Templates installed:"
check "templates/starter-claude-config/CLAUDE.md present" \
  "[[ -f '$FAKE_HOME/.claude/templates/starter-claude-config/CLAUDE.md' ]]"
check "templates/starter-claude-config/MEMORY.md present" \
  "[[ -f '$FAKE_HOME/.claude/templates/starter-claude-config/MEMORY.md' ]]"
check "templates/starter-claude-config/config.json.template present" \
  "[[ -f '$FAKE_HOME/.claude/templates/starter-claude-config/config.json.template' ]]"
check "templates/starter-claude-config/memory_examples/ has 2 .example files" \
  "[[ \$(ls '$FAKE_HOME/.claude/templates/starter-claude-config/memory_examples/' 2>/dev/null | grep -c '\.example\$') -eq 2 ]]"
check "templates/starter-vault/CLAUDE.md present" \
  "[[ -f '$FAKE_HOME/.claude/templates/starter-vault/CLAUDE.md' ]]"
check "templates/starter-vault/INBOX/ present (gitkeep)" \
  "[[ -d '$FAKE_HOME/.claude/templates/starter-vault/INBOX' ]]"
check "templates/starter-vault/AI_WORKFLOW/CLAUDE/Session Handoff Log.md" \
  "[[ -f '$FAKE_HOME/.claude/templates/starter-vault/AI_WORKFLOW/CLAUDE/Session Handoff Log.md' ]]"
check "templates/starter-vault/AI_WORKFLOW/CLAUDE/Decision Log.md" \
  "[[ -f '$FAKE_HOME/.claude/templates/starter-vault/AI_WORKFLOW/CLAUDE/Decision Log.md' ]]"
check "templates/starter-vault/AI_WORKFLOW/CLAUDE/Friction Log.md" \
  "[[ -f '$FAKE_HOME/.claude/templates/starter-vault/AI_WORKFLOW/CLAUDE/Friction Log.md' ]]"
check "templates/starter-vault/AI_WORKFLOW/CLAUDE/Processes/Process Note Template.md" \
  "[[ -f '$FAKE_HOME/.claude/templates/starter-vault/AI_WORKFLOW/CLAUDE/Processes/Process Note Template.md' ]]"
check "templates/starter-vault/AI_WORKFLOW/templates/folder-CLAUDE.template.md" \
  "[[ -f '$FAKE_HOME/.claude/templates/starter-vault/AI_WORKFLOW/templates/folder-CLAUDE.template.md' ]]"

# --- Phase 2: bootstrap re-run safety (re-running shouldn't break anything) --
echo ""
echo "Phase 2 — bootstrap.sh re-run safety (idempotent)"
RERUN_OUTPUT=$(HOME="$FAKE_HOME" bash "$REPO_ROOT/sync/bootstrap.sh" --yes 2>&1 || true)
UNCHANGED_COUNT=$(echo "$RERUN_OUTPUT" | grep -c '^  unchanged:' || true)
# Expect 12: 2 templates + 10 skills.
if [[ "$UNCHANGED_COUNT" -eq 12 ]]; then
  PASS=$((PASS + 1))
  echo "  ✓ re-run reports 'unchanged' for all 12 entries (idempotent)"
else
  FAIL=$((FAIL + 1))
  FAILURES+=("re-run idempotency: expected 12 unchanged, got $UNCHANGED_COUNT")
  echo "  ✗ re-run did not skip identical files (saw $UNCHANGED_COUNT 'unchanged' lines, expected 12)"
fi

# --- Phase 3: simulate /onboard file-creation steps --------------------------
echo ""
echo "Phase 3 — /onboard file generation against $FAKE_VAULT"

INSTALL_DATE="2026-04-27"
INSTALL_TIMESTAMP="2026-04-27T10:00:00+13:00"
DATE_PLUS_14="2026-05-11"
USER_NAME="Test User"
USER_BIO="A dogfood test user for the v0 onboarding pipeline."
USER_PREFERENCES="UK English. Concise responses. Ask first when ambiguous."
ADDITIONAL_PREFERENCES="Match a clear, factual tone."
VAULT_NAME="$(basename "$FAKE_VAULT")"
VAULT_NAME_URL_ENCODED="$(python3 -c "import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1]))" "$VAULT_NAME")"
PROJECT_KEY="$(echo "$FAKE_VAULT" | sed 's|[^a-zA-Z0-9]|-|g')"
PROJECT_DIR="$FAKE_HOME/.claude/projects/$PROJECT_KEY"
mkdir -p "$PROJECT_DIR/memory" "$FAKE_VAULT/INBOX" "$FAKE_VAULT/AI_WORKFLOW/CLAUDE/Processes" "$FAKE_VAULT/AI_WORKFLOW/templates"

# Helper: substitute placeholders from $1 (input file) into $2 (output path).
# Implementation note: cannot use `python3 - <<EOF` AND read stdin — the
# heredoc IS stdin, so sys.stdin.read() returns empty. Pass paths as argv.
SUBSTITUTE_PY="$DOGFOOD_ROOT/substitute.py"
cat > "$SUBSTITUTE_PY" <<'PYEOF'
import sys, os, re
src, out = sys.argv[1], sys.argv[2]
with open(src) as f:
    data = f.read()
subs = {
    "{{USER_NAME}}": os.environ["USER_NAME"],
    "{{USER_BIO}}": os.environ["USER_BIO"],
    "{{USER_PREFERENCES}}": os.environ["USER_PREFERENCES"],
    "{{VAULT_STRUCTURE}}": "INBOX, AI_WORKFLOW",
    "{{ADDITIONAL_PREFERENCES}}": os.environ["ADDITIONAL_PREFERENCES"],
    "{{INSTALL_DATE}}": os.environ["INSTALL_DATE"],
    "{{VAULT_PATH}}": os.environ["FAKE_VAULT"],
    "{{VAULT_NAME}}": os.environ["VAULT_NAME"],
    "{{VAULT_NAME_URL_ENCODED}}": os.environ["VAULT_NAME_URL_ENCODED"],
    "{{VAULT_ABSOLUTE_PATH}}": os.environ["FAKE_VAULT"],
    "{{VAULT_PROJECT_KEY}}": os.environ["PROJECT_KEY"],
    "{{INSTALL_ISO_TIMESTAMP}}": os.environ["INSTALL_TIMESTAMP"],
    "{{INSTALL_DATE_PLUS_14_DAYS}}": os.environ["DATE_PLUS_14"],
    "{{DATE_PLUS_14}}": os.environ["DATE_PLUS_14"],
    "{{DOMAIN_LIST}}": "(none)",
    "{{TRUE_OR_FALSE}}": "false",
}
# Zero-domain mode: replace the whole "domains": [ ... ] array with [].
# (Per template's _domains_comment: "For zero domains, write 'domains': []
# and skip the placeholder block entirely.") Do this before the simple-replace
# pass so the embedded {{DOMAIN_FOLDER_NAME}} placeholders inside the array
# don't survive into the output.
data = re.sub(
    r'"domains"\s*:\s*\[.*?\]',
    '"domains": []',
    data,
    count=1,
    flags=re.DOTALL,
)
for k, v in subs.items():
    data = data.replace(k, v)
with open(out, "w") as f:
    f.write(data)
PYEOF

substitute_to() {
  local src="$1"
  local out="$2"
  python3 "$SUBSTITUTE_PY" "$src" "$out"
}

export USER_NAME USER_BIO USER_PREFERENCES ADDITIONAL_PREFERENCES \
       INSTALL_DATE INSTALL_TIMESTAMP DATE_PLUS_14 \
       FAKE_VAULT VAULT_NAME VAULT_NAME_URL_ENCODED PROJECT_KEY

# 6a. Vault root CLAUDE.md
substitute_to "$FAKE_HOME/.claude/templates/starter-vault/CLAUDE.md" "$FAKE_VAULT/CLAUDE.md"

# 6c. Log file copies (no substitution)
cp "$FAKE_HOME/.claude/templates/starter-vault/AI_WORKFLOW/CLAUDE/Session Handoff Log.md" \
   "$FAKE_VAULT/AI_WORKFLOW/CLAUDE/Session Handoff Log.md"
cp "$FAKE_HOME/.claude/templates/starter-vault/AI_WORKFLOW/CLAUDE/Decision Log.md" \
   "$FAKE_VAULT/AI_WORKFLOW/CLAUDE/Decision Log.md"
cp "$FAKE_HOME/.claude/templates/starter-vault/AI_WORKFLOW/CLAUDE/Friction Log.md" \
   "$FAKE_VAULT/AI_WORKFLOW/CLAUDE/Friction Log.md"
cp "$FAKE_HOME/.claude/templates/starter-vault/AI_WORKFLOW/CLAUDE/Processes/Process Note Template.md" \
   "$FAKE_VAULT/AI_WORKFLOW/CLAUDE/Processes/Process Note Template.md"
cp "$FAKE_HOME/.claude/templates/starter-vault/AI_WORKFLOW/templates/folder-CLAUDE.template.md" \
   "$FAKE_VAULT/AI_WORKFLOW/templates/folder-CLAUDE.template.md"

# 6d. Global ~/.claude/CLAUDE.md (only if not exists — bootstrap may have written it via templates path, but the CLAUDE.md template at config root is separate)
if [[ ! -f "$FAKE_HOME/.claude/CLAUDE.md" ]]; then
  cp "$FAKE_HOME/.claude/templates/starter-claude-config/CLAUDE.md" "$FAKE_HOME/.claude/CLAUDE.md"
fi

# 6e. Starter MEMORY.md
substitute_to "$FAKE_HOME/.claude/templates/starter-claude-config/MEMORY.md" "$PROJECT_DIR/memory/MEMORY.md"
cp "$FAKE_HOME/.claude/templates/starter-claude-config/memory_examples/"*.md.example "$PROJECT_DIR/memory/"

# 8a. Per-vault config.json (deferred from step 6 to step 8 so it can reflect
# the user's actual domain-pass outcomes — see Codex C13 / commit fixing it)
substitute_to "$FAKE_HOME/.claude/templates/starter-claude-config/config.json.template" "$PROJECT_DIR/config.json"

# 8b. Kickoff Getting Started.md (deferred from step 6 to step 8 — same reason
# as 8a; kickoff includes domain-list which depends on step 7 outcomes)
cat > "$FAKE_VAULT/INBOX/Getting Started.md" <<KICKOFF
# Getting Started — your first vault note

Set up by \`/onboard\` on $INSTALL_DATE. This note is yours to edit.

## What just happened

- Your vault is at \`$FAKE_VAULT\`.
- Root CLAUDE.md is populated from your interview answers.
- Logs ready at \`AI_WORKFLOW/CLAUDE/\`: Session Handoff, Decision, Friction.
- Skills installed: \`/onboard\`, \`/document\`, \`/session-start\`, \`/update\`, \`/review-friction\`, \`/refresh-skills\`, \`/todo\`, \`/science-paper\`, \`/research\`, \`/verify-citations\`.

## One last setup step — point Claude Code at your vault

Quit Claude Code (Cmd-Q), reopen, and choose \`$FAKE_VAULT\` as the project. Then run /session-start.

The two-week follow-up note: \`INBOX/Onboarding follow-up — $DATE_PLUS_14.md\`.
KICKOFF

# 9. Two-week follow-up note
cat > "$FAKE_VAULT/INBOX/Onboarding follow-up — $DATE_PLUS_14.md" <<FOLLOWUP
# Onboarding follow-up — $DATE_PLUS_14

Written by \`/onboard\` on $INSTALL_DATE as a two-week check-in.
FOLLOWUP

# --- Phase 4: verify the manifest --------------------------------------------
echo ""
echo "Phase 4 — manifest verification"
check "vault/CLAUDE.md present" "[[ -f '$FAKE_VAULT/CLAUDE.md' ]]"
check "vault/INBOX/Getting Started.md present" "[[ -f '$FAKE_VAULT/INBOX/Getting Started.md' ]]"
check "vault/INBOX/Onboarding follow-up — $DATE_PLUS_14.md present" \
  "[[ -f '$FAKE_VAULT/INBOX/Onboarding follow-up — $DATE_PLUS_14.md' ]]"
check "vault/AI_WORKFLOW/CLAUDE/Session Handoff Log.md present" \
  "[[ -f '$FAKE_VAULT/AI_WORKFLOW/CLAUDE/Session Handoff Log.md' ]]"
check "vault/AI_WORKFLOW/CLAUDE/Decision Log.md present" \
  "[[ -f '$FAKE_VAULT/AI_WORKFLOW/CLAUDE/Decision Log.md' ]]"
check "vault/AI_WORKFLOW/CLAUDE/Friction Log.md present" \
  "[[ -f '$FAKE_VAULT/AI_WORKFLOW/CLAUDE/Friction Log.md' ]]"
check "vault/AI_WORKFLOW/CLAUDE/Processes/Process Note Template.md present" \
  "[[ -f '$FAKE_VAULT/AI_WORKFLOW/CLAUDE/Processes/Process Note Template.md' ]]"
check "vault/AI_WORKFLOW/templates/folder-CLAUDE.template.md present" \
  "[[ -f '$FAKE_VAULT/AI_WORKFLOW/templates/folder-CLAUDE.template.md' ]]"
check "~/.claude/CLAUDE.md (global) present" "[[ -f '$FAKE_HOME/.claude/CLAUDE.md' ]]"
check "projects/<key>/config.json present" "[[ -f '$PROJECT_DIR/config.json' ]]"
check "projects/<key>/memory/MEMORY.md present" "[[ -f '$PROJECT_DIR/memory/MEMORY.md' ]]"
check "projects/<key>/memory/feedback_email_voice.md.example present" \
  "[[ -f '$PROJECT_DIR/memory/feedback_email_voice.md.example' ]]"
check "projects/<key>/memory/tool_quirks.md.example present" \
  "[[ -f '$PROJECT_DIR/memory/tool_quirks.md.example' ]]"

# --- Phase 5: no unsubstituted placeholders ----------------------------------
echo ""
echo "Phase 5 — no unsubstituted {{PLACEHOLDER}} in generated files"
LEAKED=$(grep -lP '\{\{[A-Z_]+\}\}' \
  "$FAKE_VAULT/CLAUDE.md" \
  "$PROJECT_DIR/MEMORY.md" 2>/dev/null \
  "$PROJECT_DIR/memory/MEMORY.md" \
  "$PROJECT_DIR/config.json" 2>/dev/null || true)
if [[ -z "$LEAKED" ]]; then
  PASS=$((PASS + 1))
  echo "  ✓ no {{PLACEHOLDER}} text in any generated file"
else
  FAIL=$((FAIL + 1))
  FAILURES+=("placeholder leak: $LEAKED")
  echo "  ✗ unsubstituted placeholders found in: $LEAKED"
fi

# --- Phase 6: config.json valid JSON -----------------------------------------
echo ""
echo "Phase 6 — config.json structural validity"
if python3 -c "import json; json.load(open('$PROJECT_DIR/config.json'))" 2>/dev/null; then
  PASS=$((PASS + 1))
  echo "  ✓ config.json parses as valid JSON"
else
  FAIL=$((FAIL + 1))
  FAILURES+=("config.json invalid JSON")
  echo "  ✗ config.json failed to parse"
  python3 -c "import json; json.load(open('$PROJECT_DIR/config.json'))" 2>&1 | head -3 | sed 's/^/    /'
fi

# is_simon must be false in starter (newcomer default)
if python3 -c "import json,sys; sys.exit(0 if json.load(open('$PROJECT_DIR/config.json')).get('features',{}).get('is_simon') is False else 1)" 2>/dev/null; then
  PASS=$((PASS + 1))
  echo "  ✓ features.is_simon = false (newcomer default)"
else
  FAIL=$((FAIL + 1))
  FAILURES+=("is_simon not false in starter")
  echo "  ✗ features.is_simon is not false in newcomer config"
fi

# tools block — populated during /onboard Q7 + step 6f. Newcomer starter
# template ships with task_manager=null and *_available=false; verify that
# (a) the keys exist, (b) types are correct.
if python3 - <<PYEOF 2>/dev/null
import json, sys
c = json.load(open("$PROJECT_DIR/config.json"))
t = c.get("tools", {})
ok = (
    "task_manager" in t
    and (t["task_manager"] is None or isinstance(t["task_manager"], str))
    and isinstance(t.get("codex_available"), bool)
    and isinstance(t.get("gemini_available"), bool)
)
sys.exit(0 if ok else 1)
PYEOF
then
  PASS=$((PASS + 1))
  echo "  ✓ tools block present with valid types (task_manager, codex_available, gemini_available)"
else
  FAIL=$((FAIL + 1))
  FAILURES+=("tools block malformed in starter config.json")
  echo "  ✗ tools block missing keys or wrong types"
fi

# user block — populated by /onboard from Q1 (USER_NAME + USER_BIO). /research
# reads name+role from here to inject author context into external-model
# prompts. Empty strings allowed (causes /research to omit the line entirely);
# missing keys not allowed.
if python3 - <<PYEOF 2>/dev/null
import json, sys
c = json.load(open("$PROJECT_DIR/config.json"))
u = c.get("user", {})
ok = (
    isinstance(u, dict)
    and "name" in u
    and "role" in u
    and isinstance(u["name"], str)
    and isinstance(u["role"], str)
)
sys.exit(0 if ok else 1)
PYEOF
then
  PASS=$((PASS + 1))
  echo "  ✓ user block present with name + role (used by /research for author context)"
else
  FAIL=$((FAIL + 1))
  FAILURES+=("user block missing or malformed in starter config.json")
  echo "  ✗ user block missing keys (name, role) or wrong types"
fi

# --- Phase 7: numbered-path leak check on bundled skills ---------------------
# H4 fix from third-pass /red-team (2026-04-27): bundled skills must not
# hardcode Simon's numbered folder prefixes (01_LIFE OS/, 02_MARINE MEGAFAUNA/,
# etc.) without a guard. Every occurrence of a numbered-prefix path on a line
# in /document, /update, or /session-start must include EITHER an explicit
# "Simon" qualifier OR cascade-resolution vocabulary (<vault>, <logs>,
# newcomer, starter, cascade, fallback). Unguarded literals leak Simon's
# vault layout into newcomer skill behaviour and the first /document silently
# misses logs. Phase 8 fails the dogfood if any unguarded leak appears.
echo ""
echo "Phase 7 — bundled skills don't leak Simon-numbered paths to newcomers"
for skill in document update session-start; do
  skill_file="$FAKE_HOME/.claude/skills/$skill/SKILL.md"
  if [[ ! -f "$skill_file" ]]; then
    FAIL=$((FAIL + 1))
    FAILURES+=("$skill SKILL.md not installed (can't check)")
    echo "  ✗ $skill: SKILL.md not installed"
    continue
  fi
  total=$(grep -cE '\b0[1-6]_[A-Z]' "$skill_file" || echo 0)
  if [[ "$total" -eq 0 ]]; then
    PASS=$((PASS + 1))
    echo "  ✓ $skill: 0 numbered-path references (clean)"
    continue
  fi
  unguarded=$(grep -nE '\b0[1-6]_[A-Z]' "$skill_file" \
    | grep -ivE '[Ss]imon|SIMON-ONLY|<vault>|<logs>|newcomer|starter|cascade|fallback|illustrative|example' \
    || true)
  if [[ -z "$unguarded" ]]; then
    PASS=$((PASS + 1))
    echo "  ✓ $skill: $total numbered-path references, all guarded"
  else
    unguarded_count=$(printf '%s\n' "$unguarded" | wc -l | tr -d ' ')
    FAIL=$((FAIL + 1))
    FAILURES+=("$skill leaks $unguarded_count unguarded numbered-path reference(s)")
    echo "  ✗ $skill: $unguarded_count unguarded numbered-path references:"
    printf '%s\n' "$unguarded" | sed 's/^/    /'
  fi
done

# --- Phase 8: sync-from-vault.sh and sync-to-vault.sh SKILLS arrays match ----
# H3 fix from third-pass /red-team (2026-04-27): /refresh-skills orchestrates
# over sync-to-vault.sh, so any skill present in sync-from-vault.sh's SKILLS
# array must also be in sync-to-vault.sh's. Otherwise upstream contributor
# improvements never flow to the affected skills on user machines.
echo ""
echo "Phase 8 — sync-from-vault and sync-to-vault SKILLS arrays match"
SYNC_FROM=$(grep -oE 'skills/[a-z-]+' "$REPO_ROOT/sync/sync-from-vault.sh" | sort -u)
SYNC_TO=$(grep -oE 'skills/[a-z-]+' "$REPO_ROOT/sync/sync-to-vault.sh" | sort -u)
if [[ "$SYNC_FROM" == "$SYNC_TO" ]]; then
  PASS=$((PASS + 1))
  echo "  ✓ SKILLS arrays match in both sync scripts ($(echo "$SYNC_FROM" | wc -l | tr -d ' ') skills)"
else
  FAIL=$((FAIL + 1))
  FAILURES+=("SKILLS array drift between sync-from-vault.sh and sync-to-vault.sh")
  echo "  ✗ SKILLS array drift between sync scripts:"
  diff <(echo "$SYNC_FROM") <(echo "$SYNC_TO") | sed 's/^/    /'
fi

# --- Phase 9: kickoff promises align with what was installed -----------------
echo ""
echo "Phase 9 — kickoff Getting Started.md promises align with installed skills"
KICKOFF_FILE="$FAKE_VAULT/INBOX/Getting Started.md"
for skill in onboard document session-start update review-friction refresh-skills todo science-paper research verify-citations; do
  if grep -q "/${skill}\b" "$KICKOFF_FILE"; then
    if [[ -f "$FAKE_HOME/.claude/skills/$skill/SKILL.md" ]]; then
      PASS=$((PASS + 1))
      echo "  ✓ kickoff promises /$skill — and SKILL.md exists"
    else
      FAIL=$((FAIL + 1))
      FAILURES+=("/$skill promised but not installed")
      echo "  ✗ kickoff promises /$skill but SKILL.md missing"
    fi
  fi
done

# --- Phase 10: bundled skills don't reference unbundled ~/bin/* dependencies --
# Auto-installed skills that call `~/bin/*.py` or similar will break for
# newcomers because those scripts only exist on Simon's machine. Catches the
# /verify-citations regression Codex flagged in the third red-team pass.
echo ""
echo "Phase 10 — bundled skills don't reference unbundled ~/bin/* dependencies"
for skill in onboard document session-start update review-friction refresh-skills todo science-paper research verify-citations; do
  skill_file="$REPO_ROOT/skills/$skill/SKILL.md"
  [[ -f "$skill_file" ]] || continue
  # Match `~/bin/foo` or `$HOME/bin/foo` — reject any reference unless prefixed
  # with `(SIMON-ONLY)` on the same line.
  bad=$(grep -nE '(~|\$HOME)/bin/' "$skill_file" | grep -v 'SIMON-ONLY' || true)
  if [[ -n "$bad" ]]; then
    FAIL=$((FAIL + 1))
    FAILURES+=("/$skill references unbundled ~/bin/* dependency: $bad")
    echo "  ✗ /$skill references unbundled ~/bin/*"
    echo "$bad" | sed 's/^/      /'
  else
    PASS=$((PASS + 1))
    echo "  ✓ /$skill: no unbundled ~/bin/* references"
  fi
done

# --- Phase 12: no hardcoded "Dr. Simon J Pierce" identity in starter skills --
# Codex red-team C7: /research's external-model prompt template hardcoded
# Simon's full identity ("Dr. Simon J Pierce — marine biologist, ED of MMF").
# When auto-installed for collaborators, this leaked into Codex/Gemini prompts
# and biased their research toward Simon's field. Now parameterised via
# config.user.{name,role}. Catch any future regression in any starter skill.
echo ""
echo "Phase 12 — no hardcoded Simon identity in starter skills + references"
for skill in onboard document session-start update review-friction refresh-skills todo science-paper research verify-citations; do
  skill_dir="$REPO_ROOT/skills/$skill"
  [[ -d "$skill_dir" ]] || continue
  bad=$(grep -rnE 'Dr\. Simon J Pierce' "$skill_dir" 2>/dev/null | grep -v 'SIMON-ONLY' || true)
  if [[ -n "$bad" ]]; then
    FAIL=$((FAIL + 1))
    FAILURES+=("/$skill hardcodes 'Dr. Simon J Pierce' identity")
    echo "  ✗ /$skill hardcodes Simon identity:"
    echo "$bad" | sed 's/^/      /'
  else
    PASS=$((PASS + 1))
    echo "  ✓ /$skill: no hardcoded Simon identity"
  fi
done

# --- Phase 15: sync-from-vault.sh has missing-source guard ------------------
# Codex red-team C10: previously --commit could silently delete repo content
# if a mapped local source went missing. The script now tracks
# missing_sources separately and aborts --commit unless --allow-missing is
# explicitly passed. Catch any future regression that removes the guard.
echo ""
echo "Phase 15 — sync-from-vault.sh has missing-source guard for --commit"
SYNC_FROM="$REPO_ROOT/sync/sync-from-vault.sh"
if grep -q "missing_sources" "$SYNC_FROM" && grep -qE "ALLOW_MISSING.*true|--allow-missing" "$SYNC_FROM"; then
  PASS=$((PASS + 1))
  echo "  ✓ sync-from-vault tracks missing_sources and supports --allow-missing"
else
  FAIL=$((FAIL + 1))
  FAILURES+=("sync-from-vault.sh missing the missing-source guard")
  echo "  ✗ sync-from-vault.sh missing the C10 guard (missing_sources + --allow-missing)"
fi
if grep -qE "ABORT:.*--commit blocked.*missing" "$SYNC_FROM"; then
  PASS=$((PASS + 1))
  echo "  ✓ sync-from-vault aborts --commit on missing sources by default"
else
  FAIL=$((FAIL + 1))
  FAILURES+=("sync-from-vault.sh doesn't abort --commit on missing sources")
  echo "  ✗ sync-from-vault.sh doesn't abort --commit when sources missing"
fi

# --- Phase 14: sync-from-vault and sync-to-vault GUIDES arrays match --------
# Codex red-team C2: sync-to-vault.sh shipped with only 1 of 8 guide
# mappings, so contributor PRs editing any other guide would silently fail
# to flow back into the canonical vault. Mirror the array; check parity here.
echo ""
echo "Phase 14 — sync-from-vault and sync-to-vault GUIDES mappings match"
# from-vault mappings: "$VAULT_PATH/...::guides/foo.md" — basename comes after the ::
# to-vault mappings:   "guides/foo.md::$VAULT_PROCESSES/..." — basename comes before
FROM_BASENAMES=$(grep -oE '::guides/[a-zA-Z0-9_-]+\.md' "$REPO_ROOT/sync/sync-from-vault.sh" 2>/dev/null | sed 's|^::||' | sort -u || true)
TO_BASENAMES=$(grep -oE '"guides/[a-zA-Z0-9_-]+\.md::' "$REPO_ROOT/sync/sync-to-vault.sh" 2>/dev/null | sed 's|^"||; s|::$||' | sort -u || true)
if diff <(echo "$FROM_BASENAMES") <(echo "$TO_BASENAMES") > /dev/null; then
  PASS=$((PASS + 1))
  echo "  ✓ GUIDES arrays match in both sync scripts ($(echo "$FROM_BASENAMES" | wc -l | tr -d ' ') guides)"
else
  FAIL=$((FAIL + 1))
  FAILURES+=("GUIDES arrays diverge between sync-from-vault and sync-to-vault")
  echo "  ✗ GUIDES arrays diverge:"
  diff <(echo "$FROM_BASENAMES") <(echo "$TO_BASENAMES") | sed 's/^/      /'
fi

# --- Phase 13: /onboard config.json + kickoff written AFTER domain pass -----
# Codex red-team C13: previously /onboard step 6f wrote config.json before
# step 7's domain-pass decisions, leaving stale domain_folders_opted_in /
# domains state. Now step 6 explicitly defers, and a new step 8 writes both
# config and kickoff using step 7's actual outcomes. Catch any future
# regression by checking the SKILL.md structure.
echo ""
echo "Phase 13 — /onboard defers config.json + kickoff to after domain pass"
ONBOARD_SKILL="$REPO_ROOT/skills/onboard/SKILL.md"
# Step 6f and 6g should both contain the word "defer" / "Defer" or "after" near the heading.
if grep -E "^\*\*6f\." "$ONBOARD_SKILL" | grep -qE "[Dd]efer|after the domain"; then
  PASS=$((PASS + 1))
  echo "  ✓ step 6f explicitly defers config.json to after domain pass"
else
  FAIL=$((FAIL + 1))
  FAILURES+=("step 6f does not defer config.json")
  echo "  ✗ step 6f does not signal deferral — config may still write before step 7"
fi
if grep -E "^\*\*6g\." "$ONBOARD_SKILL" | grep -qE "[Dd]efer|after the domain"; then
  PASS=$((PASS + 1))
  echo "  ✓ step 6g explicitly defers kickoff to after domain pass"
else
  FAIL=$((FAIL + 1))
  FAILURES+=("step 6g does not defer kickoff")
  echo "  ✗ step 6g does not signal deferral — kickoff may still write before step 7"
fi
# Step 8 should exist and reference config.json + kickoff finalisation.
if grep -qE "^### 8\..*[Ff]inalise.*config" "$ONBOARD_SKILL"; then
  PASS=$((PASS + 1))
  echo "  ✓ step 8 exists and finalises config + kickoff post-domain-pass"
else
  FAIL=$((FAIL + 1))
  FAILURES+=("step 8 missing or doesn't finalise config")
  echo "  ✗ step 8 missing or wrong heading"
fi

# --- Phase 11: /onboard hands the user off to relaunch Code in the vault -----
# After /onboard, the user's Claude Code session is still pointed at the
# throwaway scratch folder they picked at install. /onboard MUST tell them
# (a) in the terminal close, and (b) in the kickoff note, to quit and
# reopen the Code tab against the new vault. Codex red-team C4.
echo ""
echo "Phase 11 — /onboard tells user to relaunch Code against the vault"
ONBOARD_FILE="$REPO_ROOT/skills/onboard/SKILL.md"
KICKOFF_TEMPLATE="$REPO_ROOT/skills/onboard/SKILL.md"  # template lives inline in step 6g
relaunch_count=$(grep -cE "Quit Claude Code|quit Claude Code" "$ONBOARD_FILE" 2>/dev/null || echo 0)
if [[ $relaunch_count -ge 2 ]]; then
  PASS=$((PASS + 1))
  echo "  ✓ /onboard mentions 'Quit Claude Code' $relaunch_count times (terminal close + kickoff)"
else
  FAIL=$((FAIL + 1))
  FAILURES+=("/onboard missing relaunch instruction (found $relaunch_count of expected 2)")
  echo "  ✗ /onboard missing relaunch instruction (found $relaunch_count of 2)"
fi
# Generated kickoff file should also have the relaunch section after substitution.
if [[ -f "$KICKOFF_FILE" ]] && grep -q "One last setup step" "$KICKOFF_FILE" 2>/dev/null; then
  PASS=$((PASS + 1))
  echo "  ✓ generated kickoff includes 'One last setup step' section"
else
  FAIL=$((FAIL + 1))
  FAILURES+=("generated kickoff missing relaunch section ('One last setup step')")
  echo "  ✗ generated kickoff missing 'One last setup step' section"
fi

# --- Summary ------------------------------------------------------------------
echo ""
echo "================================================================"
echo "  Dogfood result: $PASS passed, $FAIL failed"
echo "================================================================"
if [[ $FAIL -gt 0 ]]; then
  echo ""
  echo "Failures:"
  for f in "${FAILURES[@]}"; do echo "  - $f"; done
  exit 1
fi
echo "Release-ready: every kickoff-promised file landed correctly."
exit 0
