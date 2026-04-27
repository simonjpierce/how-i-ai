---
name: todo
description: Add a to-do to the user's task manager. Reads the task-manager choice from config.json (set during /onboard Q7) and routes to Things 3, Todoist, Apple Reminders, or a vault TODO.md depending on what's configured. Use when the user says "/todo", "add a todo", "add a task", "remind me to", or "add to my today list".
allowed-tools: Bash, Glob, Grep, Read, Edit
---

Add a task to the user's chosen task manager. The entry is a **human-readable reminder** — what the task is, why it matters, and a Claude Code prompt to resume cleanly in a fresh session.


## Adapting this for your work

This skill ships ready-to-use but routes to whatever you set up during `/onboard` Q7 (recorded as `tools.task_manager` in your per-vault `config.json`):

- **`things3`** (macOS only) — uses the bundled `things3_helper.py` (AppleScript). Requires Things 3 installed and Automation permission granted to your terminal.
- **`apple_reminders`** (macOS only) — uses AppleScript against Reminders.app. Requires Automation permission.
- **`todoist`** — uses the Todoist REST API. Requires `TODOIST_API_TOKEN` exported in your shell.
- **`vault_todo`** — appends to `<vault>/TODO.md`. No external tool needed; works for everyone. This is the default fallback if nothing else is configured.
- **`null`** / unrecognised — same fallback as `vault_todo`.

To change your task manager later: edit `~/.claude/projects/<project-key>/config.json` and update `tools.task_manager`.


## When something goes wrong

When a step in this skill fails or needs a workaround, update this skill file with what you learned BEFORE continuing to the next step. Add failure modes, correct wrong assumptions, fix timing estimates. This takes 30 seconds and prevents the same friction next time.


## Steps

### 1. Load config

Derive the project key from the absolute vault path (every non-alphanumeric char replaced with a hyphen) and read `~/.claude/projects/<project-key>/config.json`. Extract:

- `vault.path` — absolute path to the user's vault
- `vault.url_encoded_name` — for `obsidian://` URIs
- `tools.task_manager` — string or null

If config can't be read or parsed, fall back to `vault_todo` and warn the user that config is missing or malformed.

### 2. Parse the request

Extract the task title and details from the user's message (args or preceding conversation). If there are multiple **unrelated** items, create separate tasks (run through these steps once per task). Related subtasks belong in a single task — describe them in the notes, not as checklist items.

### 3. Find relevant documentation

Search the vault for the most relevant file(s) using Glob/Grep. Prefer files in the user's domain folders (whatever they set up during `/onboard`) and `<vault>/AI_WORKFLOW/CLAUDE/Processes/` for process docs.

If the task relates to something in the current conversation, reuse the files already referenced.

### 4. Write the notes — three sections

**Context** (1–3 lines): What the task is and why it matters. Written for the user reading it without opening Claude.

**Vault link**: Obsidian URI to the most relevant file:

```
obsidian://open?vault={{VAULT_URL_ENCODED_NAME}}&file=RELATIVE_PATH_WITHOUT_EXTENSION
```

URL-encode spaces as `%20`. No `.md` extension. Skip if no relevant file exists.

**Claude Code prompt**: A ready-to-paste prompt that lets a fresh Claude session pick up the task cold. Rules:
- **Self-contained** — a future session has no context from this conversation.
- **Full vault paths** — not just file names.
- **Action-oriented** — specify what to do, not just what to look at.
- **Reference docs** — include paths to relevant process docs, CLAUDE.md files, voice references.
- **Scale to complexity** — simple reminders (email someone, buy something) don't need a Claude prompt. Only include one when Claude Code would actually be useful.

Format the prompt section as:

```
Claude Code prompt:
[the prompt text]
```

### 5. Route based on `tools.task_manager`

If the value matches one of the branches below (`things3`, `todoist`, `apple_reminders`, `vault_todo`), follow that branch. If the value is `null`, missing, or unrecognised (e.g. `asana`, `linear`, `notion`, or any other string this skill hasn't been extended for yet), fall back to **5d (`vault_todo`)** and tell the user: *"Your config says `task_manager: <value>` but `/todo` doesn't have a routing branch for that yet. Falling back to vault `TODO.md`. Ask Claude to add a branch (or open a PR to `mmf-claude-code/skills/todo/`) if you'd like first-class routing."*

#### 5a. `things3` (macOS, Things 3 installed)

```bash
/opt/homebrew/bin/python3 "$HOME/.claude/skills/todo/things3_helper.py" "TITLE" "NOTES"
```

Use double quotes around each argument. Escape any literal double quotes inside the title or notes as `\"`. For multi-line notes, use a heredoc:

```bash
/opt/homebrew/bin/python3 "$HOME/.claude/skills/todo/things3_helper.py" "Task title" "$(cat <<'NOTES'
Context line 1
Context line 2

obsidian://open?vault=Vault%20Name&file=path%20here

Claude Code prompt:
Do the thing. Read the file at /full/path.
NOTES
)"
```

The helper takes **positional arguments only** — no `create`, `--title`, or `--notes` flags. It uses AppleScript (`osascript`) to target the running Things 3 instance and falls back to the URL scheme with `-g` if AppleScript fails.

If the helper exits non-zero, check:
- Is Things 3 running? (`pgrep -x Things3`)
- Is Automation permission granted? (System Settings → Privacy & Security → Automation → your terminal → Things 3)

#### 5b. `apple_reminders` (macOS, default Reminders.app)

```bash
osascript -e 'tell application "Reminders"
  tell default list
    make new reminder with properties {name:"TITLE", body:"NOTES"}
  end tell
end tell'
```

Same escaping rules as Things 3. Requires Automation permission for Reminders.app.

#### 5c. `todoist` (REST API)

```bash
curl -s -X POST "https://api.todoist.com/rest/v2/tasks" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$(python3 -c 'import json,sys; print(json.dumps({"content": sys.argv[1], "description": sys.argv[2], "due_string": "today"}))' "TITLE" "NOTES")"
```

If `TODOIST_API_TOKEN` is unset, abort and tell the user to add `export TODOIST_API_TOKEN=...` to their shell profile.

#### 5d. `vault_todo` (default, works everywhere)

Append to `<vault>/TODO.md` using Edit. Format:

```markdown
- [ ] TITLE — added YYYY-MM-DD
  - Context: [1–3 lines]
  - Link: obsidian://open?vault=...&file=...
  - Claude Code prompt: [the prompt]
```

If `<vault>/TODO.md` doesn't exist, create it with a one-line H1 header:

```markdown
# TODO

```

then append the entry.

### 6. Confirm

Tell the user:
- Task title
- Where it landed (Things 3 / Reminders / Todoist / TODO.md)
- The Claude Code prompt (so they can see what future-Claude will get)
- Any warnings (notes truncation, no relevant file found, etc.)


## Guidelines

- **Today by default.** All routes target the user's "today" or active list:
  - Things 3 helper: `when=today` is the default
  - Apple Reminders: default list, no due date (acts as "today" inbox)
  - Todoist: `due_string: "today"`
  - vault_todo: appended at the bottom; user triages from the file
- **Keep titles concise** (under 60 chars).
- **No checklists.** If a task has multiple parts, describe them in the notes as prose, not as a checklist.
- **Multiple tasks**: rate-limit yourself to one task per ~0.5s when calling external APIs — Todoist rate-limits, Things Cloud needs a beat to register, AppleScript is best run sequentially.


## Failure modes

- **Things 3 not running**: AppleScript fails, helper falls back to URL scheme. If both fail, the helper exits non-zero — fall back to `vault_todo` and warn the user.
- **Automation permission denied**: macOS shows a permission prompt the first time. If denied, the helper / AppleScript will fail silently. Tell the user where to grant it (System Settings → Privacy & Security → Automation).
- **Vault path missing or wrong**: if `<vault>/TODO.md` can't be written, abort with a clear error pointing to the config.

## Post-run improvement

After completing the task, briefly assess skill performance:
- Did any step fail, need workaround, or produce poor results?
- Were there missing steps or unclear instructions?

If patterns emerge (not one-off issues), update this skill file with fixes.
