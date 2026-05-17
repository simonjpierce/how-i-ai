#!/usr/bin/env python3
"""Non-destructive merge of a Claude Code settings.json template into a user's
existing ~/.claude/settings.json.

Design:
  - Top-level keys in the template (permissions, hooks) are merged with the
    user's settings; keys the template doesn't mention (statusLine,
    enabledPlugins, mcpServers, env, etc.) are preserved untouched.
  - For `hooks`, the merge respects Claude's nested schema:
        hooks: {<EventName>: [ {matcher?: str, hooks: [ {type, command, timeout} ] } ] }
    Template entries are matched against existing entries by (event, matcher).
    If an existing entry with the same (event, matcher) exists, the template's
    inner `hooks` items are appended unless a hook with the same `command`
    string is already present (de-duplication is by command path).
    If no existing entry matches, the template entry is appended whole.
  - `permissions` is shallow-merged: template keys overwrite user keys; user-only
    keys are preserved. Reasonable for the small permissions object.
  - A backup of the user's settings is written to settings.json.bak.<TS> before
    the merge so users can revert manually.

Usage:
    merge-settings-json.py [--template PATH] [--target PATH] [--revert] [--dry-run]

Defaults:
    --template  alongside this script: ../settings.json.template
    --target    $HOME/.claude/settings.json

Exit codes:
    0  success (merge applied or revert applied or dry-run reported no changes)
    1  argument error or template missing
    2  target settings.json malformed JSON (no backup written; aborts)
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time
from pathlib import Path


# ---------------------------------------------------------------------------
# Hooks merge primitives


def hook_signature(entry: dict) -> tuple[str | None, str | None]:
    """Identify a hooks-array entry by its (matcher, first-event-key) tuple.

    Returns just the matcher — entries are keyed within an event array by
    matcher (with None being a distinct slot for "no matcher specified").
    """
    return entry.get("matcher")


def merge_hooks(template_hooks: dict, user_hooks: dict) -> dict:
    """Merge template's `hooks` dict into the user's `hooks` dict.

    For each event present in the template:
      - Look up each template matcher-entry by its `matcher` field.
      - If an existing entry with the same matcher exists in user_hooks[event],
        append each of the template entry's inner hooks unless a hook with the
        same `command` string is already present.
      - Otherwise, append the whole template entry to user_hooks[event].

    User-only events (events present only in the user's settings) are preserved.
    """
    result = {ev: list(entries) for ev, entries in user_hooks.items()}

    for event, template_entries in template_hooks.items():
        if event not in result:
            result[event] = []
        existing = result[event]
        # Index existing entries by matcher for fast lookup.
        by_matcher: dict[str | None, dict] = {}
        for e in existing:
            by_matcher[hook_signature(e)] = e

        for tmpl_entry in template_entries:
            sig = hook_signature(tmpl_entry)
            if sig in by_matcher:
                # Merge inner hook arrays, de-duping by `command`.
                existing_inner = by_matcher[sig].setdefault("hooks", [])
                existing_commands = {
                    h.get("command") for h in existing_inner if isinstance(h, dict)
                }
                for h in tmpl_entry.get("hooks", []):
                    if not isinstance(h, dict):
                        continue
                    if h.get("command") in existing_commands:
                        continue
                    existing_inner.append(h)
                    existing_commands.add(h.get("command"))
            else:
                # No matching entry — append the whole template entry.
                existing.append(json.loads(json.dumps(tmpl_entry)))
                by_matcher[sig] = existing[-1]
    return result


def revert_hooks(template_hooks: dict, user_hooks: dict) -> dict:
    """Reverse of merge_hooks: remove every command path the template added.

    Removes the command entries; drops emptied matcher-entries; drops emptied
    event arrays. Preserves anything the template didn't add.
    """
    template_commands_by_key: dict[tuple[str, str | None], set] = {}
    for event, entries in template_hooks.items():
        for entry in entries:
            sig = hook_signature(entry)
            template_commands_by_key.setdefault((event, sig), set()).update(
                h.get("command") for h in entry.get("hooks", []) if isinstance(h, dict)
            )

    result: dict = {}
    for event, entries in user_hooks.items():
        new_entries: list = []
        for entry in entries:
            sig = hook_signature(entry)
            to_remove = template_commands_by_key.get((event, sig), set())
            if not to_remove:
                new_entries.append(entry)
                continue
            kept = [
                h
                for h in entry.get("hooks", [])
                if not (isinstance(h, dict) and h.get("command") in to_remove)
            ]
            if kept:
                new_entry = dict(entry)
                new_entry["hooks"] = kept
                new_entries.append(new_entry)
            # else: drop the matcher-entry entirely (its hooks were all ours)
        if new_entries:
            result[event] = new_entries
        # else: drop the event (it was all ours)
    return result


# ---------------------------------------------------------------------------
# Top-level merge


def deep_merge_permissions(template_perm: dict, user_perm: dict) -> dict:
    """Shallow merge — template overwrites user for the keys it sets.

    `allow` and `deny` arrays, if present in both, are unioned (de-duped).
    """
    merged = dict(user_perm)
    for k, v in template_perm.items():
        if k in ("allow", "deny") and isinstance(v, list) and isinstance(merged.get(k), list):
            seen = set()
            new_list: list = []
            for item in merged[k] + v:
                key = json.dumps(item, sort_keys=True) if not isinstance(item, str) else item
                if key not in seen:
                    new_list.append(item)
                    seen.add(key)
            merged[k] = new_list
        else:
            merged[k] = v
    return merged


def revert_permissions(template_perm: dict, user_perm: dict) -> dict:
    """Best-effort permissions revert: for keys the template set, drop them
    from the user's permissions. If `defaultMode` was set, restore to "default"
    so the system has an explicit value rather than implicit behaviour.
    """
    result = dict(user_perm)
    for k in template_perm:
        if k == "defaultMode":
            result["defaultMode"] = "default"
        elif k in ("allow", "deny") and isinstance(template_perm[k], list) and isinstance(result.get(k), list):
            keys_to_drop = {
                json.dumps(i, sort_keys=True) if not isinstance(i, str) else i
                for i in template_perm[k]
            }
            result[k] = [
                item for item in result[k]
                if (json.dumps(item, sort_keys=True) if not isinstance(item, str) else item)
                not in keys_to_drop
            ]
            if not result[k]:
                del result[k]
        else:
            result.pop(k, None)
    return result


def apply_merge(template: dict, user: dict) -> dict:
    """Merge template into user; return the new settings dict."""
    result = dict(user)
    if "permissions" in template:
        result["permissions"] = deep_merge_permissions(
            template["permissions"], user.get("permissions", {})
        )
    if "hooks" in template:
        result["hooks"] = merge_hooks(template["hooks"], user.get("hooks", {}))
    # Any other top-level keys in the template: take template's value if user
    # doesn't have one; otherwise leave user's untouched.
    for k, v in template.items():
        if k in ("permissions", "hooks"):
            continue
        if k not in result:
            result[k] = v
    return result


def apply_revert(template: dict, user: dict) -> dict:
    """Reverse the merge — drop the template's contributions from user."""
    result = dict(user)
    if "permissions" in template and "permissions" in user:
        reverted = revert_permissions(template["permissions"], user["permissions"])
        if reverted:
            result["permissions"] = reverted
        else:
            result.pop("permissions", None)
    if "hooks" in template and "hooks" in user:
        reverted = revert_hooks(template["hooks"], user["hooks"])
        if reverted:
            result["hooks"] = reverted
        else:
            result.pop("hooks", None)
    for k in template:
        if k in ("permissions", "hooks"):
            continue
        # Drop only if value matches exactly what we'd have inserted.
        if result.get(k) == template[k]:
            result.pop(k, None)
    return result


# ---------------------------------------------------------------------------
# CLI


def main(argv: list[str]) -> int:
    script_dir = Path(__file__).resolve().parent
    default_template = script_dir.parent / "settings.json.template"
    default_target = Path(os.path.expanduser("~/.claude/settings.json"))

    parser = argparse.ArgumentParser(description="Merge a Claude Code settings template into the user's settings.json")
    parser.add_argument("--template", type=Path, default=default_template,
                        help=f"Template path (default: {default_template})")
    parser.add_argument("--target", type=Path, default=default_target,
                        help=f"Target settings.json (default: {default_target})")
    parser.add_argument("--revert", action="store_true",
                        help="Reverse the merge — drop the template's contributions")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print the merged result to stdout; don't write")
    args = parser.parse_args(argv)

    if not args.template.exists():
        print(f"ERROR: template not found: {args.template}", file=sys.stderr)
        return 1

    with args.template.open() as f:
        template = json.load(f)

    if args.target.exists():
        try:
            with args.target.open() as f:
                user = json.load(f)
        except json.JSONDecodeError as e:
            print(f"ERROR: existing settings.json is malformed JSON: {e}", file=sys.stderr)
            print(f"Refusing to overwrite. Please fix or move {args.target} and re-run.", file=sys.stderr)
            return 2
    else:
        user = {}

    if args.revert:
        result = apply_revert(template, user)
        action = "reverted"
    else:
        result = apply_merge(template, user)
        action = "merged"

    if result == user:
        print(f"No changes — settings already {action} (no-op).")
        return 0

    if args.dry_run:
        print(json.dumps(result, indent=2))
        return 0

    # Back up before writing.
    if args.target.exists():
        ts = time.strftime("%Y%m%d-%H%M%S")
        backup = args.target.with_suffix(f".json.bak.{ts}")
        shutil.copy2(args.target, backup)
        print(f"Backed up existing settings to: {backup}")

    args.target.parent.mkdir(parents=True, exist_ok=True)
    with args.target.open("w") as f:
        json.dump(result, f, indent=2)
        f.write("\n")
    print(f"{action.capitalize()} {args.template.name} into {args.target}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
