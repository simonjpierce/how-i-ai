# Managing CLI dependencies

> **Adapting this for your work.** This guide walks through the `/tools-registry` skill — a manual snapshot of what CLI tools your installed Claude Code skills actually depend on. The skill is portable. The advanced "daily refresh" + use-case-aware release assessment described in the appendix is Simon Pierce's personal infrastructure (`~/bin/obsidian_reviews/external_tools_check.py` + LaunchAgent), not part of the standard kit.

Status: skill (`/tools-registry`)
Owner: shared
Last reviewed: 2026-05-18

## Why this exists

Claude Code skills depend on CLI tools installed on your machine — `whisper-cli` for `/transcribe`, `vale` and `languagetool` for `/polish`, `pdftotext` and `qpdf` for `/pdf-to-markdown`, and so on. These tools live outside the skills repo: you install them via Homebrew, pipx, or npm.

Over time three forms of drift accumulate:

1. **Tools installed but no longer used.** You install something to evaluate (`wrangler`, a Cloudflare deploy CLI; `openhue-cli`, a smart-light controller), decide against it, and never uninstall. Six months later it's sitting on disk consuming nothing in particular except mental load when you `brew list`.
2. **Skills that reference missing tools.** A skill you install assumes a CLI is present that isn't (`gemini` for the `/research` skill's three-model triangulation, say). The skill degrades gracefully — usually — but you wouldn't know you're getting the degraded version unless you check.
3. **Upgrades that quietly happened.** `brew upgrade` ran, a tool's CLI changed in a way that broke a skill's invocation, and you don't notice until the skill fails three weeks later when you next use it.

`/tools-registry` addresses (1) and (2). It doesn't yet address (3) — that's the v2 roadmap.

## What `/tools-registry` does

Run `/tools-registry` and the skill:

1. Enumerates every installed package across Homebrew (formulae + casks), pipx, and npm globals. On a typical setup that's 30–60 packages.
2. Scans every installed Claude Code skill (`~/.claude/skills/`) for CLI tool invocations — looking for subprocess calls, absolute paths to binaries, backtick command substitutions, and shell commands starting with the tool name.
3. Cross-references the two: which tools are invoked by at least one skill, which tools sit installed with no skill caller.
4. Writes the result to `<your vault>/Tools — Dependencies.md`.

The output has two sections worth reviewing:

- **Tools used by your installed skills** — your dependency surface. If you uninstall everything in this section, your skills break.
- **Possibly unused** — installed packages that NO installed skill invokes. Three common reasons each entry can show up:
  - Tool you use interactively (run by hand at the CLI, never via a skill).
  - Leftover from a skill you've uninstalled.
  - Tool you installed to evaluate and didn't end up using.

The skill does NOT auto-uninstall anything. Reviewing the "Possibly unused" list is a manual decision.

## When to run it

There's no daily automation. Reasonable triggers:

- After installing several new skills via `/install-skill`.
- After uninstalling a skill — check whether its tools went into "Possibly unused".
- Quarterly, as part of broader system maintenance.
- When `brew list` makes you think "what is half of this stuff doing here?"

## What the limitations are

`/tools-registry` v1 has known gaps documented in the skill's `Known limitations` section. The main ones:

- **`poppler`-style multi-binary formulae.** Brew installs `pdftotext`, `qpdf`, `pdfinfo`, `pdftoppm` under the single `poppler` formula. The scanner looks for `poppler` (the formula name) in skill files but skills reference the binaries by name. So `poppler` shows up as "Possibly unused" even when one of its binaries is heavily used. Workaround: keep a mental list of multi-binary formulae you depend on, or wait for v2.
- **Short tool names (≤ 2 chars) only match absolute paths.** `jq`, `rg`, `fd`, `r`, `go` are too noisy to scan via bare-name pattern — Python variables, English words, regex flags all create false positives. Skills that invoke these via `/opt/homebrew/bin/jq` are still detected; ones that just run `jq` aren't.
- **Only scans `~/.claude/skills/`.** If you keep scripts in `~/bin/` that invoke tools, they won't be cross-referenced. Open an issue if this affects you.

## Appendix — going further (Simon-specific)

The portable `/tools-registry` skill is the entry point. Simon's personal infrastructure extends this in three directions, none of which ship as part of mmf-claude-code:

- **Daily LaunchAgent refresh** at 07:30, so the registry is always current without manual invocation.
- **Upstream release tracking** for each watched tool — fetches GitHub release notes daily, applies a breaking-change keyword scan, surfaces alerts in the registry.
- **Use-case-aware Opus relevance assessment** — on each new release, sends (tool + caller list + release notes) to Claude Opus, gets back a 1–2 sentence assessment with verdict `adopt | consider | skip | breaking`. The "Upstream improvements worth knowing" section of his registry is populated by this. Costs a few cents per week on a personal account.
- **Interactive-use tracking** via `~/.zsh_history` scanning — counts invocations of "possibly unused" candidates per day, so tools genuinely never run get escalated to a "Confident removal candidates" section after 60 days of zero use.

If you want any of these on your setup, the implementation is in `external_tools_check.py` in Simon's `obsidian-automations` repo. Porting them to mmf-claude-code as a shared feature would need each tool's `github_repo` metadata enriched from package-manager registries (brew formula homepage, npm `repository.url`, PyPI metadata) — that's its own work-package and would be welcome as a PR.

The lighter manual `/tools-registry` is enough for most workflows. The automation tier is for users who want a continuously-maintained dependency view, not a "I'll run it when I notice friction" snapshot.
