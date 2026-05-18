#!/usr/bin/env python3
"""Tools Registry — portable CLI dependency inventory generator.

Scans installed brew/pipx/npm tools, cross-references against installed Claude
Code skills, and writes a human-readable markdown registry to the user's vault.

v1 scope (this file): inventory + skill callers + possibly-unused detection.
v2 will add upstream release tracking + use-case-aware Opus relevance pass
on new releases (requires per-tool github_repo metadata enrichment from
brew/npm registries, which is its own project).

Usage:
    python tools_registry.py [--vault PATH] [--dry-run]

Defaults:
    --vault : read from ~/.claude/projects/<active>/config.json's vault.path,
              else ~/Obsidian Vault if present, else error.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

HOME = Path.home()
SKILLS_DIR = HOME / ".claude" / "skills"
STATE_FILE = HOME / ".claude" / "tools_registry_state.json"
REGISTRY_FILENAME = "Tools — Dependencies.md"

TODAY = datetime.now().strftime("%Y-%m-%d")
NOW = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

NEVER_REMOVE_NAMES = {
    "brew", "git", "gh", "ssh", "vim", "nvim", "tmux", "tree", "wget", "curl",
    "make", "cmake", "node", "ruby", "mas", "coreutils", "gnu-sed", "gawk",
    "findutils", "gnu-tar", "openssh", "ca-certificates", "readline", "xz",
    "zstd", "python", "pip", "pipx", "npm", "npx", "claude", "codex", "rg",
    "ripgrep", "fzf", "jq", "yq", "bat", "fd",
}
NEVER_REMOVE_PREFIXES = ("font-", "lib", "python@", "openssl@", "pcre", "icu4c")

_SUBPROCESS_INDICATORS = (
    "subprocess.run", "subprocess.Popen", "subprocess.check_call",
    "subprocess.check_output", "os.system", "os.popen",
)
_WHICH_INDICATORS = ("which ", "command -v ", "type ", "exec ")


def run(cmd, timeout=30):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        return -1, "", str(e)


def resolve_vault_path(explicit=None):
    if explicit:
        p = Path(explicit).expanduser()
        if p.exists():
            return p
    projects_dir = HOME / ".claude" / "projects"
    if projects_dir.exists():
        for proj in projects_dir.iterdir():
            cfg = proj / "config.json"
            if cfg.exists():
                try:
                    data = json.loads(cfg.read_text())
                    vp = data.get("vault", {}).get("path") or data.get("vault_path")
                    if vp and Path(vp).exists():
                        return Path(vp)
                except (json.JSONDecodeError, OSError):
                    continue
    fallback = HOME / "Obsidian Vault"
    if fallback.exists():
        return fallback
    raise SystemExit(
        "Could not resolve vault path. Pass --vault PATH or set vault.path in "
        "~/.claude/projects/<active>/config.json."
    )


def enumerate_installed():
    """Return (items, status). items: {namespaced_key: True}. status: per-manager ok|failed."""
    items = {}
    status = {}

    rc, out, _ = run(["/opt/homebrew/bin/brew", "list", "--installed-on-request"])
    if rc == 0:
        status["brew_formula"] = "ok"
        for line in out.splitlines():
            if line.strip():
                items[f"brew/{line.strip()}"] = True
    else:
        status["brew_formula"] = "failed"

    rc, out, _ = run(["/opt/homebrew/bin/brew", "list", "--cask"])
    if rc == 0:
        status["brew_cask"] = "ok"
        for line in out.splitlines():
            if line.strip():
                items[f"brew-cask/{line.strip()}"] = True
    else:
        status["brew_cask"] = "failed"

    rc, out, _ = run(["/opt/homebrew/bin/pipx", "list", "--json"], timeout=30)
    if rc == 0 and out:
        try:
            data = json.loads(out)
            status["pipx"] = "ok"
            for pkg_name in data.get("venvs", {}).keys():
                items[f"pipx/{pkg_name}"] = True
        except json.JSONDecodeError:
            status["pipx"] = "failed"
    else:
        status["pipx"] = "failed"

    rc, out, _ = run(["/opt/homebrew/bin/npm", "list", "-g", "--depth=0", "--json"], timeout=20)
    if rc == 0 and out:
        try:
            data = json.loads(out)
            status["npm"] = "ok"
            for pkg_name in data.get("dependencies", {}).keys():
                items[f"npm/{pkg_name}"] = True
        except json.JSONDecodeError:
            status["npm"] = "failed"
    else:
        status["npm"] = "failed"

    return items, status


def installed_version(key):
    """Best-effort fetch of installed version for a namespaced key."""
    kind, _, bare = key.partition("/")
    if kind == "brew" or kind == "brew-cask":
        rc, out, _ = run(["/opt/homebrew/bin/brew", "info", "--json=v2", bare], timeout=15)
        if rc != 0 or not out:
            return None
        try:
            data = json.loads(out)
        except json.JSONDecodeError:
            return None
        for f in data.get("formulae", []):
            installed = f.get("installed", [])
            if installed:
                return installed[0].get("version")
        for c in data.get("casks", []):
            return c.get("version")
        return None
    if kind == "pipx":
        rc, out, _ = run(["/opt/homebrew/bin/pipx", "list", "--json"], timeout=20)
        if rc != 0 or not out:
            return None
        try:
            data = json.loads(out)
        except json.JSONDecodeError:
            return None
        venv = data.get("venvs", {}).get(bare)
        if venv:
            return venv.get("metadata", {}).get("main_package", {}).get("package_version")
        return None
    if kind == "npm":
        rc, out, _ = run(["/opt/homebrew/bin/npm", "ls", "-g", bare, "--json"], timeout=15)
        if rc != 0 or not out:
            return None
        try:
            data = json.loads(out)
        except json.JSONDecodeError:
            return None
        deps = data.get("dependencies", {})
        pkg = deps.get(bare)
        if pkg:
            return pkg.get("version")
    return None


def scan_skills_for_tool(tool_name, skills_dir=SKILLS_DIR):
    """Find skill files (SKILL.md, scripts) invoking `tool_name` in command context.
    Returns sorted list of relative paths.

    Short tool names (<= 2 chars) are NOT scanned via bare-name pattern — they
    produce too many false positives (`r` matches Python variable `r = ...`,
    `go` matches docs prose, etc.). Only absolute-path matches are accepted
    for short names.
    """
    if not skills_dir.exists():
        return []
    short_name_only_abs = len(tool_name) <= 2
    escaped = re.escape(tool_name)
    abs_pattern = re.compile(
        rf"(?:/opt/homebrew/bin/{escaped}|/usr/local/bin/{escaped}|/usr/bin/{escaped})\b"
    )
    bare_pattern = re.compile(rf"\b{escaped}\b")

    callers = set()
    for path in skills_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in (".md", ".py", ".sh", ".js", ".ts"):
            continue
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        if abs_pattern.search(content):
            callers.add(str(path.relative_to(skills_dir.parent)))
            continue

        if short_name_only_abs:
            # Skip bare-name pattern for short tool names — too noisy
            continue

        for m in bare_pattern.finditer(content):
            line_start = content.rfind("\n", 0, m.start()) + 1
            line_end = content.find("\n", m.end())
            if line_end == -1:
                line_end = len(content)
            raw_line = content[line_start:line_end]  # unstripped — offsets stay aligned
            offset_in_line = m.start() - line_start
            stripped = raw_line.strip()
            first_token = (stripped.split()[0] if stripped else "").strip("`\"'(")
            if first_token == tool_name:
                callers.add(str(path.relative_to(skills_dir.parent)))
                break
            before = raw_line[max(0, offset_in_line - 80):offset_in_line]
            if any(ind in before for ind in _SUBPROCESS_INDICATORS):
                callers.add(str(path.relative_to(skills_dir.parent)))
                break
            if any(ind in before[-30:] for ind in _WHICH_INDICATORS):
                callers.add(str(path.relative_to(skills_dir.parent)))
                break
            # Backtick / shell command-sub prefix — character immediately before
            # the match is ` or ( (and not a continuation of a longer identifier)
            if offset_in_line > 0 and raw_line[offset_in_line - 1] in ("`", "("):
                callers.add(str(path.relative_to(skills_dir.parent)))
                break

    return sorted(callers)


def is_never_remove(inventory_key):
    _, _, bare = inventory_key.partition("/")
    if "/" in bare:
        bare = bare.split("/")[-1]
    bare = bare.lstrip("@")
    if bare in NEVER_REMOVE_NAMES:
        return True
    return any(bare.startswith(p) for p in NEVER_REMOVE_PREFIXES)


def load_state():
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def render_registry(items, status, tool_callers, versions, state):
    today_dt = datetime.strptime(TODAY, "%Y-%m-%d")
    baseline = state.get("inventory_baselined_at", TODAY)
    try:
        baseline_dt = datetime.strptime(baseline, "%Y-%m-%d")
    except ValueError:
        baseline_dt = today_dt
    in_baseline_window = (today_dt - baseline_dt).days < 14

    sections = [
        "---",
        f"generated: {NOW}",
        f"generator: ~/.claude/skills/tools-registry/scripts/tools_registry.py",
        f"inventory_baselined_at: {baseline}",
        "manager_status:",
    ]
    for m, s in sorted(status.items()):
        sections.append(f"  {m}: {s}")
    sections.extend([
        "---",
        "",
        "# Tools — Dependencies",
        "",
        "Snapshot of CLI tools installed on this machine and which Claude Code skills invoke them. Generated by `/tools-registry`. Re-run anytime for a fresh snapshot — there's no daily automation.",
        "",
        "## Tools used by your installed skills",
        "",
    ])

    by_kind = [
        ("brew/", "Homebrew formulae"),
        ("brew-cask/", "Homebrew casks"),
        ("pipx/", "pipx packages"),
        ("npm/", "npm globals"),
    ]
    any_used = False
    for prefix, title in by_kind:
        used_in_bucket = [k for k in sorted(items.keys())
                          if k.startswith(prefix) and tool_callers.get(k)]
        if not used_in_bucket:
            continue
        any_used = True
        sections.append(f"### {title}")
        sections.append("")
        sections.append("| Tool | Installed | Used by |")
        sections.append("|---|---|---|")
        for key in used_in_bucket:
            _, _, bare = key.partition("/")
            installed = versions.get(key, "?")
            callers = tool_callers.get(key, [])
            used = ", ".join(callers[:3])
            if len(callers) > 3:
                used += f" (+{len(callers) - 3})"
            sections.append(f"| {bare} | `{installed or '?'}` | {used} |")
        sections.append("")
    if not any_used:
        sections.append("_No skill callers detected for any installed tool._")
        sections.append("")

    # Possibly unused
    sections.append("## Possibly unused")
    sections.append("")
    if in_baseline_window:
        days_remaining = 14 - (today_dt - baseline_dt).days
        sections.append(
            f"_First snapshot taken {baseline}. Treat detections as provisional for {days_remaining} more day(s) — "
            "right now, recently-installed tools you intend to use may appear here as false positives until skills referencing them are also installed._"
        )
        sections.append("")
    possibly_unused = []
    for key in sorted(items.keys()):
        if is_never_remove(key):
            continue
        if tool_callers.get(key):
            continue
        _, _, bare = key.partition("/")
        possibly_unused.append((bare, key.partition("/")[0]))
    if possibly_unused:
        sections.append("| Tool | Kind | Note |")
        sections.append("|---|---|---|")
        for name, kind in possibly_unused:
            sections.append(
                f"| {name} | {kind} | No installed skill invokes this. Could be interactive-only, exploration leftover, or a tool whose skill was uninstalled. |"
            )
        sections.append("")
        sections.append("_Verify before removing: tools used only interactively (run by hand at the CLI) will appear here as false positives._")
    else:
        sections.append("_None detected._")
    sections.append("")

    failed = [m for m, s in status.items() if s != "ok"]
    if failed:
        sections.append("## ⚠️ Manager enumeration failures")
        sections.append("")
        for m in failed:
            sections.append(f"- `{m}`")
        sections.append("")
        sections.append("_These package managers couldn't be queried; sections under their namespaces may be incomplete. Common cause: the manager isn't installed (no `pipx`, no `npm`). Safe to ignore if you don't use that manager._")
        sections.append("")

    return "\n".join(sections)


def main():
    parser = argparse.ArgumentParser(description="Generate Tools — Dependencies registry")
    parser.add_argument("--vault", help="Vault path override")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print to stdout, don't write the registry file")
    args = parser.parse_args()

    vault = resolve_vault_path(args.vault)
    print(f"Vault: {vault}", file=sys.stderr)

    state = load_state()
    if "inventory_baselined_at" not in state:
        state["inventory_baselined_at"] = TODAY

    print("Enumerating installed packages...", file=sys.stderr)
    items, status = enumerate_installed()
    enum_ok = sum(1 for s in status.values() if s == "ok")
    print(f"  {len(items)} packages found across {enum_ok} of 4 managers", file=sys.stderr)

    print("Scanning skills for tool invocations...", file=sys.stderr)
    tool_callers = {}
    for key in items:
        if is_never_remove(key):
            continue
        _, _, bare = key.partition("/")
        scan_name = bare.split("/")[-1].lstrip("@") if "/" in bare else bare.lstrip("@")
        callers = scan_skills_for_tool(scan_name)
        if callers:
            tool_callers[key] = callers
    print(f"  {len(tool_callers)} of {len(items)} packages have skill callers", file=sys.stderr)

    print("Resolving versions for skill-invoked tools...", file=sys.stderr)
    versions = {}
    for key in tool_callers:
        versions[key] = installed_version(key)

    registry_md = render_registry(items, status, tool_callers, versions, state)

    if args.dry_run:
        print(registry_md)
        return 0

    registry_path = vault / REGISTRY_FILENAME
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    registry_path.write_text(registry_md, encoding="utf-8")
    print(f"Registry written: {registry_path}", file=sys.stderr)

    save_state(state)
    return 0


if __name__ == "__main__":
    sys.exit(main())
