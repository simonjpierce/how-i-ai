#!/bin/bash
# Auto-open hook — pop newly-edited vault notes open in Obsidian.
#
# Fires on PostToolUse:Edit|Write. Looks up the vault config that owns the
# edited file and, if hooks.auto_open_obsidian is true (default), opens the
# file via the obsidian:// URL scheme. Exits silently otherwise.
#
# Opt out by setting `hooks.auto_open_obsidian: false` in
# ~/.claude/projects/<key>/config.json.

input=$(cat)

FILE_PATH=$(echo "$input" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    print(d.get('tool_input', {}).get('file_path', ''))
except Exception:
    print('')
" 2>/dev/null)

[ -z "$FILE_PATH" ] && exit 0

# Only meaningful for markdown notes. Skip other file types silently.
case "$FILE_PATH" in
    *.md) ;;
    *) exit 0 ;;
esac

# Find the matching vault config. Extract vault.path, vault.url_encoded_name,
# and hooks.auto_open_obsidian in one pass.
read VAULT VAULT_URL_NAME OPT_IN <<<"$(python3 - "$FILE_PATH" <<'EOF' 2>/dev/null
import json, glob, os, sys
fp = sys.argv[1] if len(sys.argv) > 1 else ""
best_vault = ""
best_name = ""
best_opt = "true"
for p in sorted(glob.glob(os.path.expanduser("~/.claude/projects/*/config.json"))):
    try:
        cfg = json.load(open(p))
        vp = cfg.get("vault", {}).get("path", "")
        if vp and fp.startswith(vp.rstrip("/") + "/") and len(vp) > len(best_vault):
            best_vault = vp
            best_name = cfg.get("vault", {}).get("url_encoded_name", "")
            opt = cfg.get("hooks", {}).get("auto_open_obsidian", True)
            best_opt = "true" if opt else "false"
    except Exception:
        pass
print(best_vault, best_name, best_opt)
EOF
)"

[ -z "$VAULT" ] && exit 0
[ "$OPT_IN" = "false" ] && exit 0
[ -z "$VAULT_URL_NAME" ] && exit 0

# Compute the vault-relative path (strip vault root + leading slash), then
# URL-encode it and strip the .md extension per Obsidian URL conventions.
REL_PATH="${FILE_PATH#$VAULT/}"
ENCODED=$(python3 -c "
import urllib.parse, sys
p = sys.argv[1]
if p.endswith('.md'):
    p = p[:-3]
print(urllib.parse.quote(p, safe='/'))
" "$REL_PATH" 2>/dev/null)

[ -z "$ENCODED" ] && exit 0

# macOS-only: `open` is the canonical URL launcher. On Linux/Windows users
# can extend this hook or set auto_open_obsidian: false to skip.
if command -v open >/dev/null 2>&1; then
    open "obsidian://open?vault=${VAULT_URL_NAME}&file=${ENCODED}" 2>/dev/null
fi
exit 0
