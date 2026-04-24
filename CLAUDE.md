# mmf-claude-code — notes for Claude

This repo is a mirror. The vault (`05_AI WORKFLOW/CLAUDE/Skills/`) and `~/.claude/skills/` are source of truth; the contents of `skills/`, `guides/`, and `templates/` are produced by `sync/sync-from-vault.sh`.

## When /update runs against this repo

Don't `git add` / `git commit` files in `skills/`, `guides/`, or `templates/` directly. The sync script fully replaces those directories on each run — direct commits get overwritten by the next sync.

Instead: run `./sync/sync-from-vault.sh --commit` from the repo root. Simon has confirmed (2026-04-25) that `/update` is expected to push mirror changes through this mechanism — not via direct commits.

The script stages into `/tmp/`, sanitises vault paths to `$VAULT_PATH`/`$CLAUDE_CONFIG`, scans for common credential patterns, and aborts the commit if it finds any. If the scan trips, fix the source file in the vault or `~/.claude/` and re-run — don't bypass.

## When a team member opens a PR against skills/guides/

Those PRs are **proposals**, not direct merges. The sync script would overwrite a merged PR on the next run. Workflow: review the PR → if accepted, apply the change to the vault/~/.claude/ source → next `/update` syncs it back out → close the PR as "landed via sync." See CONTRIBUTING.md for more.

PRs against other files (README, CONTRIBUTING, sync script itself, templates at the top level, LICENSE) merge normally.
