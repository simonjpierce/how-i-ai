---
name: tools-registry
description: Generate a markdown registry of CLI tools installed on the machine, cross-referenced against installed Claude Code skills. Surfaces which tools each skill invokes, plus possibly-unused tools no skill calls. Writes to `<vault>/Tools — Dependencies.md`. Use when the user says "/tools-registry", "what tools do my skills depend on", "audit my dependencies", or "what's installed but unused".
allowed-tools: Bash, Read
---

Snapshot what CLI tools are installed via Homebrew / pipx / npm, and which Claude Code skills actually invoke them. Writes a human-readable registry to your vault.

This is the v1 of a tooling dependency view. v2 will add upstream-release tracking and use-case-aware relevance assessment on new versions — see "Roadmap" at the bottom.

## Adapting this for your work

This skill ships ready-to-use. It assumes:
- **Homebrew** at `/opt/homebrew/bin/brew` (Apple Silicon Macs; adjust paths in `scripts/tools_registry.py` for Intel Macs or Linux).
- **pipx** at `/opt/homebrew/bin/pipx` (optional — missing pipx is a non-fatal "manager enumeration failure" in the output).
- **npm** at `/opt/homebrew/bin/npm` (optional — same fallback).
- Vault path comes from `~/.claude/projects/<active>/config.json` per the standard `/onboard` setup. You can override with `--vault PATH`.

The output filename is `Tools — Dependencies.md` (em-dash for Obsidian visual consistency; if your editor doesn't handle em-dashes well, rename inside the script).

## When something goes wrong

When a step fails or needs a workaround, update this skill file with what you learned BEFORE continuing. Add failure modes, correct wrong assumptions. This takes 30 seconds and prevents the same friction next time.

## Steps

### 0. Set tab title (Ghostty only)

```bash
[ -d /Applications/Ghostty.app ] && MY_TTY=$(ps -o tty= -p $PPID 2>/dev/null | tr -d ' ') && echo "tools registry" > "/tmp/claude-title-${MY_TTY}"
```

### 1. Locate the script

The script lives alongside this SKILL.md:

```bash
SCRIPT="$HOME/.claude/skills/tools-registry/scripts/tools_registry.py"
if [ ! -f "$SCRIPT" ]; then
  echo "Script not found at $SCRIPT. Run /install-skill tools-registry to (re-)install."
  exit 1
fi
```

### 2. Run the registry generator

Standard run — writes to `<vault>/Tools — Dependencies.md`:

```bash
python3 "$SCRIPT"
```

Dry-run preview without writing the file:

```bash
python3 "$SCRIPT" --dry-run
```

Override the vault path (rare — only if `/onboard` didn't capture it):

```bash
python3 "$SCRIPT" --vault "/path/to/your/vault"
```

### 3. Walk the output

Open the file in Obsidian:

```bash
VAULT_NAME=$(basename "$VAULT_PATH" | python3 -c "import sys, urllib.parse; print(urllib.parse.quote(sys.stdin.read().strip()))")
open "obsidian://open?vault=$VAULT_NAME&file=Tools%20%E2%80%94%20Dependencies.md"
```

The user reviews three sections:

1. **Tools used by your installed skills** — installed tools that at least one skill invokes (organised by package manager). Quick visual confirmation of what your skills actually depend on.
2. **Possibly unused** — installed tools that NO skill invokes. Could be (a) interactive-only tools you use manually, (b) leftovers from skills you've uninstalled, (c) tools you installed to evaluate and didn't end up using. Verify before removing.
3. **Manager enumeration failures** (only if present) — package managers that couldn't be queried. Common cause: you don't have that manager installed. Safe to ignore unless you DO use it.

For each "Possibly unused" entry, offer one-at-a-time:

1. **(recommended) Keep — interactive use.** No action.
2. **Uninstall.** Run the appropriate command:
   - `brew uninstall <name>` for brew/brew-cask
   - `pipx uninstall <name>` for pipx
   - `npm uninstall -g <name>` for npm globals
3. **Document the interactive use case.** Add a one-liner to your vault (e.g. in a "Tools I use interactively" note) so future-you remembers why it's installed.

### 4. State is persisted

The script stamps `inventory_baselined_at` in `~/.claude/tools_registry_state.json` on first run. The "Possibly unused" section is treated as provisional for 14 days after baseline — recently-installed tools may appear there before their corresponding skill is installed.

After the 14-day window, "Possibly unused" detections are more reliable: if a tool is listed AND you don't recognise the interactive use case, it's worth investigating.

## Known limitations (v1)

- **Brew formula vs binary name mismatch.** Some brew formulae install binaries under different names. The canonical example: `poppler` installs `pdftotext`, `qpdf`, `pdfinfo`, `pdftoppm`. The scanner looks for the FORMULA name, so a skill that uses `pdftotext` won't surface `poppler` in the "Tools used by your installed skills" section — `poppler` will appear in "Possibly unused" even though it IS being used (via one of its sibling binaries). Workaround: keep a mental allowlist of multi-binary formulae you know you depend on. v2 will use `brew info --json=v2` to enumerate each formula's binaries and scan for all of them.
- **Short tool names (≤ 2 chars) skip the bare-name scan.** Tools like `r` (R language), `rg` (ripgrep), `fd`, `jq`, `go` won't be detected via bare-name pattern — too many false positives in script files (Python variable names, English words). They're still detected if invoked via absolute path (`/opt/homebrew/bin/jq`).
- **Skills outside `~/.claude/skills/` aren't scanned.** If you have scripts in `~/bin/` that invoke CLI tools, those callers aren't picked up. Open an issue if this matters for your workflow.

## Roadmap (v2)

The current version is inventory + skill cross-reference only. Planned additions:
- **Upstream release tracking** — for each tool with skill callers, fetch latest GitHub release and flag when installed lags upstream.
- **Use-case-aware relevance assessment** — on each new release, send (tool + skill callers + release notes) to Claude Opus and tag verdict `adopt / consider / skip / breaking`. Surfaces upstream improvements actually relevant to how your skills use the tool.
- **Interactive-use tracking** — count invocations of "possibly unused" candidates in `~/.zsh_history` to escalate confidently-dead candidates (zero script callers + zero interactive use for 60 days).

These features exist in Simon Pierce's personal infrastructure (`~/bin/obsidian_reviews/external_tools_check.py`) tied to a daily LaunchAgent. Porting them to mmf-claude-code requires per-tool `github_repo` metadata enrichment (probe brew/npm/pypi registries) and is its own work-package.

## Post-run improvement

After completing a run, briefly assess:
- Did any package manager fail to enumerate? If yes and you use that manager, fix the path in `scripts/tools_registry.py`.
- Were any "Possibly unused" detections genuine false positives (tool used by a non-skill script outside `~/.claude/skills/`)? Consider extending `scan_skills_for_tool` to also scan `~/bin/` if you keep scripts there.
- Was any tool you actively use missing from the "Tools used by your installed skills" section? That means the skill's reference doesn't match the command-context filter — surface as a bug for `scan_skills_for_tool` refinement.

If patterns emerge (not one-off issues), update this skill file with fixes per the #1 rule.
