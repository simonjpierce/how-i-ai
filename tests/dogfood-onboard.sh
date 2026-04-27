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
for skill in onboard document session-start update review-friction refresh-skills todo science-paper research; do
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
# Expect 11: 2 templates + 9 skills.
if [[ "$UNCHANGED_COUNT" -eq 11 ]]; then
  PASS=$((PASS + 1))
  echo "  ✓ re-run reports 'unchanged' for all 11 entries (idempotent)"
else
  FAIL=$((FAIL + 1))
  FAILURES+=("re-run idempotency: expected 11 unchanged, got $UNCHANGED_COUNT")
  echo "  ✗ re-run did not skip identical files (saw $UNCHANGED_COUNT 'unchanged' lines, expected 11)"
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

# 6f. Per-vault config.json
substitute_to "$FAKE_HOME/.claude/templates/starter-claude-config/config.json.template" "$PROJECT_DIR/config.json"

# 6g. Kickoff Getting Started.md (inlined from /onboard skill)
cat > "$FAKE_VAULT/INBOX/Getting Started.md" <<KICKOFF
# Getting Started — your first vault note

Set up by \`/onboard\` on $INSTALL_DATE. This note is yours to edit.

## What just happened

- Your vault is at \`$FAKE_VAULT\`.
- Root CLAUDE.md is populated from your interview answers.
- Logs ready at \`AI_WORKFLOW/CLAUDE/\`: Session Handoff, Decision, Friction.
- Skills installed: \`/onboard\`, \`/document\`, \`/session-start\`, \`/update\`, \`/review-friction\`, \`/refresh-skills\`, \`/todo\`, \`/science-paper\`, \`/research\`.

The two-week follow-up note: \`INBOX/Onboarding follow-up — $DATE_PLUS_14.md\`.
KICKOFF

# 8. Two-week follow-up note
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

# --- Phase 7: kickoff promises align with what was installed -----------------
echo ""
echo "Phase 7 — kickoff Getting Started.md promises align with installed skills"
KICKOFF_FILE="$FAKE_VAULT/INBOX/Getting Started.md"
for skill in onboard document session-start update review-friction refresh-skills todo science-paper research; do
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
