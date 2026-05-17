#!/bin/bash
# Stop hook — enforce verification-before-completion.
# Fires on Stop events. Exit 0 (allow) or exit 2 (block with reminder).
#
# Failure mode addressed: multi-output work claimed complete when outputs
# were silently partial (e.g. a report's Excel tab + chart + text all stale,
# autonomous task runners marking themselves done before all subtasks
# returned, batch processing missing fields on some items).
#
# Logic:
#   1. Skip if already blocked once (stop_hook_active) — avoid infinite loop.
#   2. If last assistant message contains strong completion language AND
#      the session touched multiple files OR ran computation,
#      AND the message lacks a verification block (file:line evidence),
#      then block with a reminder.

INPUT=$(cat)

# Break infinite loops — if we already blocked once, let the agent complete.
STOP_ACTIVE=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('stop_hook_active', False))" 2>/dev/null)
if [ "$STOP_ACTIVE" = "True" ]; then
    exit 0
fi

# Extract last_assistant_message and transcript_path. Strip fenced code blocks,
# inline code, and quoted citations before pattern matching — the completion
# patterns ("all done", "handover complete", etc.) false-positive when quoted
# in meta-discussion or shown as examples.
MSG=$(echo "$INPUT" | python3 -c "
import json, re, sys
d = json.load(sys.stdin)
text = d.get('last_assistant_message', '')
text = re.sub(r'\`\`\`.*?\`\`\`', '', text, flags=re.DOTALL)
text = re.sub(r'\`[^\`\n]*\`', '', text)
text = re.sub(r'\"[^\"\n]*\"', '', text)
text = re.sub(r\"'[^'\n]*'\", '', text)
print(text)
" 2>/dev/null)

# ORIG_MSG keeps the message un-stripped — used ONLY for the evidence-pattern
# check below. Stripping is correct for completion-language matching (avoid
# false-positives on quoted patterns) but WRONG for evidence matching: real
# verification blocks cite file:line inside backticks (the standard citation
# format), and stripping inline-code spans would remove that evidence.
ORIG_MSG=$(echo "$INPUT" | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(d.get('last_assistant_message', ''))
" 2>/dev/null)

TRANSCRIPT=$(echo "$INPUT" | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(d.get('transcript_path', ''))
" 2>/dev/null)

[ -z "$MSG" ] && exit 0

# Strong completion language — phrases that claim work is finished.
# Deliberately stricter than "done" alone to avoid false positives on
# conversational "done" ("done — want me to look at X?").
COMPLETION_PATTERNS=(
    "all done"
    "all complete"
    "task complete"
    "work complete"
    "now complete"
    "is complete"
    "are complete"
    "fully complete"
    "handover complete"
    "all set"
    "all shipped"
    "ready for (review|merge|ship|release)"
    "everything is (done|ready|in place)"
    "successfully (completed|finished|updated|migrated)"
    "complete\. (the|all|each)"
    "finished\. (the|all|each)"
)

FOUND_CLAIM=""
for pattern in "${COMPLETION_PATTERNS[@]}"; do
    if echo "$MSG" | grep -qiE -- "$pattern"; then
        FOUND_CLAIM="$pattern"
        break
    fi
done

[ -z "$FOUND_CLAIM" ] && exit 0

# Count tool uses from the transcript to decide if this was a multi-output task.
# Small tasks (single-file edit, simple answer) shouldn't require a verification block.
EDIT_COUNT=0
BASH_COMPUTE_COUNT=0

if [ -n "$TRANSCRIPT" ] && [ -f "$TRANSCRIPT" ]; then
    COUNTS=$(python3 <<EOF 2>/dev/null
import json, re
edit_count = 0
bash_compute = 0
try:
    with open("$TRANSCRIPT", "r") as f:
        for line in f:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            msg = entry.get("message", {})
            content = msg.get("content", [])
            if not isinstance(content, list):
                continue
            for item in content:
                if not isinstance(item, dict):
                    continue
                if item.get("type") == "tool_use":
                    name = item.get("name", "")
                    inp = item.get("input", {}) or {}
                    if name in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
                        edit_count += 1
                    elif name == "Bash":
                        cmd = inp.get("command", "")
                        if re.search(r"\b(python3?|Rscript|jupyter|bq |duckdb|psql|sqlite3|awk|sed)\b", cmd):
                            bash_compute += 1
except Exception:
    pass
print(f"{edit_count} {bash_compute}")
EOF
)
    EDIT_COUNT=$(echo "$COUNTS" | awk '{print $1}')
    BASH_COMPUTE_COUNT=$(echo "$COUNTS" | awk '{print $2}')
fi

EDIT_COUNT=${EDIT_COUNT:-0}
BASH_COMPUTE_COUNT=${BASH_COMPUTE_COUNT:-0}

# Threshold: multi-file (2+ edits) OR any computation.
# Below this, the task is small enough that verification friction isn't justified.
if [ "$EDIT_COUNT" -lt 2 ] && [ "$BASH_COMPUTE_COUNT" -lt 1 ]; then
    exit 0
fi

# Check for verification evidence in the final message.
# Evidence = explicit file paths with line numbers, a Verification section,
# or a proof-of-completion block. If any present, allow.
EVIDENCE_PATTERNS=(
    "[A-Za-z0-9_./-]+\.(md|py|R|sh|js|ts|json|yaml|yml|txt|csv):[0-9]+"
    "## Verification"
    "### Verification"
    "\*\*Verification[:[:space:]]*\*\*"
    "Verified:"
    "Verification block:"
    "Proof of completion:"
    "Evidence:"
    "- \[x\] .*\.(md|py|R|sh|xlsx|csv|json)"
    "verified (by|via|that|against) "
    "confirmed (by|via|that) "
    "checked (by|via|that) "
)

HAS_EVIDENCE=""
for pattern in "${EVIDENCE_PATTERNS[@]}"; do
    # Run against ORIG_MSG (not MSG) so file:line cites inside backticks
    # — the standard citation format — count as evidence.
    if echo "$ORIG_MSG" | grep -qE -- "$pattern"; then
        HAS_EVIDENCE="yes"
        break
    fi
done

[ -n "$HAS_EVIDENCE" ] && exit 0

# Completion claimed, substantive work done, no verification block — block.
cat >&2 <<EOF
⚠️ Verification-before-completion gate triggered.

Detected completion language ("$FOUND_CLAIM") after $EDIT_COUNT file edits + $BASH_COMPUTE_COUNT computation calls, but no verification block in the final message.

== How to generate the block in ONE turn ==

Scan your last ~10 tool calls. For each file edited or significant Bash computation, add a line:

    - \`path/to/file.ext:LINE\` — <short excerpt proving the change>

Template:

    **Verification:**
    - \`file1.md:42\` — "the new heading I added"
    - \`file2.py:117-120\` — new function signature \`def foo(x): ...\`
    - Bash: \`pytest tests/\` → \`8 passed, 0 failed\`

OR explicitly state "no verification needed because [reason]" if the work is genuinely verification-free (e.g. pure explanation, single-line edit).

Do NOT just restate what you did — the block requires file paths + line numbers + short excerpts proving each change is actually present.

If you've already verified and just omitted the block, add it now and continue.
EOF
exit 2
