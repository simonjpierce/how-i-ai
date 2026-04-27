#!/usr/bin/env python3
"""Sanitise Obsidian-only markdown syntax for GitHub rendering.

Converts:
  - `[[Page]]`              → plain text `Page` (vault-only refs lose brackets)
  - `[[Page|Display]]`      → plain text `Display` (vault-only refs lose brackets)
  - `[[Page]]` where Page maps to a shipped guide → `[Page](./shipped-guide.md)`
  - `[[Page|Display]]` where Page maps to a shipped guide → `[Display](./shipped-guide.md)`

Rationale: wikilinks render as literal `[[brackets]]` on GitHub, which looks
broken when newcomers click into guides from the README. Vault-only
references can't be linked anywhere meaningful from the repo, so dropping
the brackets keeps the prose readable. Refs to other shipped guides become
proper relative links.

Idempotent: re-running on already-sanitised content produces no changes.

Called from sync-from-vault.sh's sanitise() helper. Operates in place.
"""
import re
import sys
from pathlib import Path

# Vault-side basename (without .md, before any |Display) → repo-side relative target
# from the guides/ directory. Keep in sync with sync-from-vault.sh GUIDES array.
SHIPPED_GUIDES = {
    "Ghostty Setup Guide for Claude Code": "./ghostty-setup.md",
    "Inviting Collaborators to mmf-claude-code": "./inviting-collaborators.md",
    "AI-Assisted Scientific Analysis — Process Guide": "./ai-assisted-scientific-analysis.md",
    "AI-Assisted Scientific Writing – Process Guide": "./ai-assisted-scientific-writing.md",
    "AI-Assisted Writing — Reports, Manuscripts & Analysis": "./ai-assisted-writing.md",
    "Literature Intake & Integration Workflow": "./literature-intake-and-integration.md",
    "Pre-Submission Manuscript Review – Prompt Template": "./pre-submission-manuscript-review.md",
    "Research Workflow": "./research-workflow.md",
}

# Match `[[Target|Display]]` or `[[Target]]`. Target can contain anything but `|]`.
# Display can contain anything but `]`.
WIKILINK_RE = re.compile(r"\[\[([^|\]]+?)(?:\|([^\]]+?))?\]\]")


def _normalise_target(target: str) -> str:
    """Strip path prefixes and anchors so 'Processes/Foo|Foo' → 'Foo'."""
    target = target.strip()
    # Drop any path prefix: "Processes/Foo" → "Foo"
    target = target.split("/")[-1]
    # Drop any anchor / heading reference: "Foo#section" → "Foo"
    target = target.split("#")[0]
    return target.strip()


def _replace(match: re.Match) -> str:
    target = match.group(1)
    display = match.group(2) or target
    normalised = _normalise_target(target)
    if normalised in SHIPPED_GUIDES:
        return f"[{display}]({SHIPPED_GUIDES[normalised]})"
    # Vault-only reference: drop the brackets, leave the display text inline.
    return display


def sanitise_text(text: str) -> str:
    return WIKILINK_RE.sub(_replace, text)


def sanitise_file(path: Path) -> bool:
    """Returns True if the file was modified."""
    original = path.read_text()
    sanitised = sanitise_text(original)
    if sanitised != original:
        path.write_text(sanitised)
        return True
    return False


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: sanitise_wikilinks.py <file.md> [<file.md> ...]", file=sys.stderr)
        return 2
    changed = 0
    for arg in sys.argv[1:]:
        path = Path(arg)
        if not path.is_file():
            print(f"skip (not a file): {arg}", file=sys.stderr)
            continue
        if sanitise_file(path):
            changed += 1
    return 0 if changed >= 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
