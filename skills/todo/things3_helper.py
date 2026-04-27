#!/usr/bin/env python3
"""Shared Things 3 helper — AppleScript-based task creation.

Replaces the old pattern of `subprocess.run(["open", "things:///add?..."])` which
caused multiple Things 3 instances and duplicate tasks. AppleScript targets the
running instance directly and is synchronous.

Usage (Python):
    from things3_helper import create_things3_task
    create_things3_task("Review something", notes="Details here")

Usage (shell):
    python3 /Users/simonjpierce/bin/obsidian_reviews/things3_helper.py "Task title" "Optional notes"
"""

import subprocess
import time

# Minimum gap between consecutive task creations (seconds).
# Gives Things Cloud a moment to register each task before the next.
_MIN_GAP = 0.5
_last_creation_time = 0.0


def _escape_applescript(s: str) -> str:
    """Escape a string for embedding in AppleScript double quotes.

    AppleScript double-quoted strings support the standard C-style escapes
    (\\\\, \\", \\n, \\r, \\t). Escape rather than strip so that task titles
    and notes preserve punctuation, URLs, and multi-line content verbatim.
    Backslash must be escaped first.
    """
    return (
        s.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "\\r")
        .replace("\t", "\\t")
    )


def create_things3_task(title: str, notes: str = "") -> bool:
    """Create a Things 3 task via AppleScript (Today list).

    Uses `make new to do` then `move ... to list "Today"` — the only
    reliable way to target Today via AppleScript (activation date is
    read-only).

    Returns True on success, False on failure. Never raises.
    """
    global _last_creation_time

    # Rate-limit: wait if we're creating tasks in rapid succession
    now = time.monotonic()
    elapsed = now - _last_creation_time
    if _last_creation_time > 0 and elapsed < _MIN_GAP:
        time.sleep(_MIN_GAP - elapsed)

    title_esc = _escape_applescript(title)
    notes_esc = _escape_applescript(notes)

    script = f'''
tell application "Things3"
    set newToDo to make new to do with properties {{name:"{title_esc}", notes:"{notes_esc}"}}
    move newToDo to list "Today"
end tell
'''

    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=15,
        )
        _last_creation_time = time.monotonic()

        if result.returncode != 0:
            stderr = result.stderr.strip()
            print(f"  AppleScript failed ({stderr}), falling back to URL scheme")
            return _fallback_url_scheme(title, notes)

        print(f"  Things 3 task created: {title}")
        return True

    except subprocess.TimeoutExpired:
        print(f"  Things 3 AppleScript timed out, falling back to URL scheme")
        return _fallback_url_scheme(title, notes)
    except Exception as e:
        print(f"  Things 3 task creation failed: {e}")
        return False


def _fallback_url_scheme(title: str, notes: str) -> bool:
    """Last-resort fallback using URL scheme with -g flag (no foreground)."""
    import urllib.parse
    params = {"title": title, "when": "today"}
    if notes:
        params["notes"] = notes
    url = "things:///add?" + urllib.parse.urlencode(
        params, quote_via=urllib.parse.quote
    )
    try:
        subprocess.run(["open", "-g", url], check=False, timeout=5)
        print(f"  Things 3 task created (URL fallback): {title}")
        return True
    except Exception as e:
        print(f"  Things 3 URL fallback also failed: {e}")
        return False


if __name__ == "__main__":
    import sys

    args = sys.argv[1:]
    if not args:
        print("Usage: python3 things3_helper.py TITLE [NOTES]", file=sys.stderr)
        sys.exit(1)

    # Catch help-style flags BEFORE treating them as task content.
    # A first-positional-arg starting with "-" is never a legitimate task title
    # Simon would create. The 2026-04-20 incident: `--help` was passed and a
    # "--help" task landed in Things 3 Today.
    if args[0] in ("-h", "--help", "-?", "help", "/?"):
        print(
            "Usage: python3 things3_helper.py TITLE [NOTES]\n"
            "\n"
            "Creates a task in the Things 3 Today list via AppleScript.\n"
            "Positional args only — no --title / --notes flags.\n"
            "\n"
            "Examples:\n"
            "  python3 things3_helper.py \"Review proposal\"\n"
            "  python3 things3_helper.py \"Review proposal\" \"Notes with obsidian://open URL\"\n",
            file=sys.stderr,
        )
        sys.exit(0)
    if args[0].startswith("-"):
        print(
            f"Error: first argument '{args[0]}' looks like a flag. Use positional args only.\n"
            "Usage: python3 things3_helper.py TITLE [NOTES]",
            file=sys.stderr,
        )
        sys.exit(2)

    # Detect misuse: `things3_helper.py create --title "..." [--notes "..."]`
    # Claude sometimes constructs commands this way despite instructions.
    if args[0] == "create" and len(args) > 1 and args[1].startswith("--"):
        title = ""
        notes = ""
        i = 1  # skip "create"
        while i < len(args):
            if args[i] == "--title" and i + 1 < len(args):
                title = args[i + 1]
                i += 2
            elif args[i] == "--notes" and i + 1 < len(args):
                notes = args[i + 1]
                i += 2
            else:
                i += 1
        if not title:
            print("Error: --title is required", file=sys.stderr)
            sys.exit(1)
        print("  (Note: use positional args, not create --title)", file=sys.stderr)
    else:
        # Normal positional usage: things3_helper.py "TITLE" "NOTES"
        title = args[0]
        notes = args[1] if len(args) > 1 else ""

    ok = create_things3_task(title, notes)
    sys.exit(0 if ok else 1)
