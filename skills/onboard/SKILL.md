---
name: onboard
description: First-run setup for a new Claude + Obsidian system. Detects whether the user already has Obsidian, walks them through install if not, runs a short discovery interview (5–7 questions), and writes a personalised CLAUDE.md cascade, starter MEMORY.md, log files, and kickoff note into their vault. Optional domain-folder pass. Schedules a follow-up routine in 2 weeks for the nightly self-improvement loop. Use when the user says "/onboard", "set up my vault", "walk me through this system", or pastes the README's three-step prompt.
allowed-tools: Read, Write, Edit, Bash, Glob, Skill
---

This skill is the bridge from "nothing installed" to "working Claude system." It hides the architectural detail behind a short interview — the user doesn't have to read or understand the `getting-started/00–04` docs to benefit from them.

## Preamble — read this back to the user before starting

```
Welcome. I'll walk you through setting up Claude Code + Obsidian as a working
system. About 6 quick questions, plus a few more if you want me to set up
domain folders for the different kinds of work you do — ~15 minutes total.

Strongly recommend dictating rather than typing. If you're in the Claude
Code desktop app, there's a microphone button right in the prompt area —
**press and hold** to record, release to stop, then send. That's the
fastest way to get long answers in. (If you're in a terminal instead,
macOS Fn-Fn dictation works in any text field, or ChatGPT voice mode +
paste if you have Plus.) Ramble. You don't need to give structured
answers — go off on tangents, contradict yourself, mention things that
come to mind but don't seem related, whatever's natural. I'll sort
through what you said and ask follow-ups if anything's unclear.

Two things I'll check at the start, then we'll get going.
```

## When something goes wrong

If a step fails (template path missing, vault path not writable, /schedule unavailable, etc.), update this skill BEFORE continuing the workaround. Add the failure mode and the recovery path. Don't ship friction onto future users.

## Steps

### 0. Set tab title (Ghostty only)

If `/Applications/Ghostty.app` exists, set the tab title. Otherwise skip — this is Ghostty-specific.

```bash
[ -d /Applications/Ghostty.app ] && MY_TTY=$(ps -o tty= -p $PPID 2>/dev/null | tr -d ' ') && echo "onboarding" > "/tmp/claude-title-${MY_TTY}"
```

### 1. Pre-flight — platform + auto-approval mode + Bash availability

**1a. Platform check.** This onboarding flow is currently macOS-only. Run:

```bash
[ "$(uname)" = "Darwin" ] && echo "platform OK"
```

If the result is anything other than `platform OK`, halt and tell the user:

> *"This setup flow is currently macOS-only — Windows and Linux support is on the v1 roadmap. If you're on Windows or Linux and want to run this anyway, ping Simon for a manual install."*

Do not proceed past this check on non-Darwin platforms.

**1b. Auto mode.** This system assumes Claude Code is in **Auto mode** (formerly called bypassPermissions/YOLO mode) — the highest auto-approval level. The prompt area shows a red "Auto mode" badge when it's on; the alternatives are "Accept edits" (auto-accepts file writes only — still prompts for Bash) and the default mode (prompts for everything). Auto mode is the recommended setting for this onboarding because we'll be writing 20+ files AND running shell commands; anything less makes the flow miserable.

> *"Before we go further: switch Claude Code to Auto mode so I can write files and run setup commands without stopping every few seconds for permission. In the desktop app, look at the bottom-left of the prompt area — there's a small badge that says either 'Accept edits' or 'Auto mode'. Click it once or twice until it shows red 'Auto mode'. (You can also press Shift-Tab to cycle modes.) Auto mode lets me run any shell command on your machine without asking — only enable it if you're comfortable with that. You can switch back to Accept edits or default mode any time. Tell me when it's done."*

To make Auto mode the default for every session (recommended once trust is established), add to `~/.claude/settings.json`:

```json
{
  "permissions": {
    "defaultMode": "bypassPermissions"
  }
}
```

(`bypassPermissions` is the internal name for Auto mode; `acceptEdits` is the internal name for "Accept edits".)

If the user reports a different layout (Anthropic moves these toggles between releases), suggest searching Settings for "permission" or "mode". Don't proceed past Phase 2 in default-prompt or Accept-edits mode — Bash-prompt friction will wreck the rest of the flow.

**1c. Bash availability.** The rest of this skill assumes you can run shell commands. If your tools include Bash, proceed. If you don't have a Bash tool, STOP and tell the user:

> *"I can't run shell commands or write files in this environment, which means I can't actually install the system here. Open Claude Code in the Claude Desktop app — same Pro plan you already have, just a different surface — and paste the README prompt again. I'll resume from there."*

Do not attempt the rest of the skill in a no-Bash context.

<!-- Notes for Claude (don't quote to user): Bash availability is the right pre-flight signal. Filesystem-write tests can succeed in restricted-MCP environments where the rest of the install would still fail; Bash is a stricter check. -->


### 2. Detect & route

Ask:

> *"Do you already have an Obsidian vault, or are we setting one up from scratch?"*

Numbered options:
1. Fresh (set up Obsidian and a new vault)
2. Existing (I have a vault already; point Claude at it)

Branch on the answer:

- Fresh → Phase 3 (setup logistics).
- Existing → ask for the absolute path, verify it exists with `ls`, check for an existing `CLAUDE.md` at the root (warn the user if found — offer to merge or back up before overwriting). Then jump to Phase 4.

### 3. Setup logistics (fresh-vault path only)

**3a. Obsidian install.** If they don't have Obsidian:

> *"You'll need Obsidian. It's free. Download it from `https://obsidian.md/download` — install, open, then come back here when it's running."*

Wait for them to confirm install is complete. Don't try to install Obsidian programmatically (out of scope for the skill).

**3b. Vault location.** Ask where they want the vault:

> *"Where should your vault live? Suggested: `$HOME/Documents/Obsidian Vault`. If you use iCloud / Dropbox / Google Drive sync, pick a location inside that sync folder so the vault syncs across devices."*

Numbered options:
1. `$HOME/Documents/Obsidian Vault` (default, no sync)
2. iCloud (typical path: `$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/<name>`)
3. Dropbox / Google Drive (user provides path)
4. Other (user provides path)

**3c. Sync option.** Note the sync choice for `Getting Started.md` later. Don't try to configure sync — instructional only.

**3d. Create vault folder.** Before any Bash command, normalise the chosen path to an absolute one — quoted `~` does NOT expand in shell, so a literal `~/Documents/Obsidian Vault` would create a `~` directory in the current working directory. If the user said `~/Foo`, rewrite to `$HOME/Foo` (or expand to a full absolute path). Then:

```bash
mkdir -p "$VAULT_PATH"
```

Verify writable:

```bash
touch "$VAULT_PATH/.write-test" && rm "$VAULT_PATH/.write-test"
```

If write-test fails: most common cause is iCloud Drive not enabled. Tell the user:

> *"That folder isn't writeable yet. Most common reason: iCloud Drive isn't turned on. Open System Settings → Apple ID → iCloud and check that 'iCloud Drive' is on, then tell me. Otherwise, pick a non-cloud path (your Documents folder is fine) and we can move the vault later if you want sync."*

Offer numbered options: retry the same path, switch to `$HOME/Documents/Obsidian Vault`, or specify a different path.

**3e. Register the folder as an Obsidian vault.** A `mkdir`'d folder is not yet a vault — Obsidian needs to know about it. Walk the user through:

> *"Switch to Obsidian. If you see a welcome screen, click 'Open folder as vault' and select `<chosen-path>`. If you're already inside a different vault, click the small vault-name dropdown in the top-left of the Obsidian sidebar (or press Cmd-comma to open Settings and search 'Manage vaults') → 'Open folder as vault'. The vault will open with no notes in it — that's expected; we're about to create them."*

Wait for the user to confirm the vault is open in Obsidian before proceeding. If they hit "vault not found" or a permissions prompt, troubleshoot before moving on — every later `obsidian://open?vault=<name>&file=...` link depends on Obsidian recognising this vault by name. Once confirmed, derive the URL-encoded vault name from the folder's basename for use in later steps' obsidian:// URIs.

### 4. Discovery interview

**CRITICAL CONSTRAINT — read this before anything else in this section.** Ask exactly ONE question at a time. Wait for the user's reply. Then ask the next one. Do NOT batch Q1–Q8 in a single message regardless of what the user's onboarding prompt said. Do NOT preview upcoming questions ("next I'll ask about..."). The whole point of `/onboard` is hand-holding for non-technical users — a wall-of-text interview is the single fastest way to lose a newcomer. If the user pastes their answers in batches anyway, that's their choice; you still ask one at a time.

Number-replies-OK except where genuinely free-form.

**Q1.** *"In a sentence or two — who are you, and what kinds of work will you mostly use this setup for?"*

**Q2.** *"When you switch tasks, what are the main 'modes' or 'hats' you switch between? List 2–5. Examples: 'research papers and a personal blog'; 'three different clients I consult for'; 'work + parenting + creative writing'. If you're not sure, list every distinct audience you write for — your team, your students, yourself, a funder. Better to over-list now; you can always merge folders later."*

**Q3.** *"Spelling preference — UK / US / NZ / Australian, or 'doesn't matter'? (If you're unsure: working with the MMF team in marine biology, NZ/UK is the safe default; writing for US journals or US donors, US.) And anything else about how you write — typical formality, words you avoid, emoji preferences?"*

**Q4.** *"Response style — do you prefer concise direct answers, or detailed step-by-step? And: when something's ambiguous, do you want me to ask first, or make a best-guess and let you correct me?"*

**Q5 (optional).** *"Paste a paragraph or two of writing you've done recently — email, blog post, anything — so I can match your voice. Skip if nothing's handy."*

If the user says "skip", "no", "I don't have one", "later", or anything indicating they don't want to share a sample right now, accept it and move straight to Q6 — don't push back, don't re-ask, don't suggest they find one. The voice-sample distillation just gets omitted from `{{ADDITIONAL_PREFERENCES}}`; Q6's free-text input fills that placeholder alone, which is fine. The user can refine voice later by reading any voice reference into a session, or by `/document` capturing tone-correction signal over time.

**Q6.** *"Anything specific about how you work, who you work with, or context I should keep in mind that the questions above missed?"*

**Q7.** *"What other tools do you use day-to-day that we should know about? I'm especially interested in: where do your TODOs live (Things, Todoist, Apple Reminders, a notebook, nowhere yet)? Anything else worth mentioning — calendars, AI tools, writing apps — feel free to ramble."*

Map the task-manager part of Q7 to one of: `things3`, `todoist`, `apple_reminders`, `vault_todo` (= "I'll keep a TODO.md in the vault" / "nothing yet, just the vault is fine"), or `null` (= "I have no idea / skip"). If the user names another task manager (Asana, Linear, Notion, etc.), record their answer in the free-text reply but write `vault_todo` to config — `/todo` doesn't ship routing for those yet, and a user can ask Claude later to add a branch for their tool. Hold the full free-text answer too — it goes into `~/.claude/CLAUDE.md` so future sessions know what's around.

**Q8.** *"Last one. What's the most pressing thing on your plate this week — a paper draft, a literature search, a report due, a manuscript awaiting review, a research question you've been chewing on? Doesn't have to be polished; just tell me what's on your mind. I'll suggest a concrete first task to anchor your Day 1 with the system."*

Q8 maps to a `{{DAY_1_TASK}}` block in the kickoff note (filled at step 8b after the domain pass). Map the user's answer to one of these patterns.

**Skill-install note**: starter install ships only the universal session/system skills (`/onboard`, `/document`, `/session-start`, `/update`, `/review-friction`, `/refresh-skills`). Skills marked `*` below are work-specific and need installing first via `cp -R ~/.claude/repos/mmf-claude-code/skills/<name> ~/.claude/skills/` then restarting Claude Code. Include the install line in the kickoff recommendation when you use them.

| User mentions | Day-1 recommendation |
|---|---|
| paper, draft, manuscript, writing up | "Drop your existing draft (or skeleton) into `<vault>/<domain-folder>/`. The `/science-paper`* skill sets up a lab notebook + manuscript pair and walks you through the next step. Or just ask Claude to help with the draft directly — the skill is a structured workflow, not the only path." |
| research, find, investigate, literature search, what's known about X | "Install `/research`* and run it with your question — three-model deep research (Claude + Codex + Gemini) with verified citations. For a quicker lookup, ask Claude directly without the skill." |
| review, peer review, feedback, co-author, before submission | "Drop the manuscript into `<vault>/<domain-folder>/`. Install `/red-team`* and run it — pre-submission three-model adversarial critique. See `guides/pre-submission-manuscript-review.md`." |
| citations, references, verify | "Install `/verify-citations`* and run it against your manuscript. Checks each reference against Semantic Scholar, CrossRef, and OpenAlex." |
| meeting recording, audio, transcribe, voice memo | "Drop the audio file into `<vault>/INBOX/` and ask Claude to transcribe and format it. Claude handles audio natively. (The `/transcribe`* skill adds whisper-cli speaker diarization + structured output if you install it.)" |
| TODO list, tasks, things to do | "Tell Claude to add the task to your task manager (recorded during this onboarding). The `/todo`* skill is a shorthand that routes to Things 3 / Todoist / Reminders — install it if you want the slash command, but plain English to Claude works too." |
| vague, "I'm not sure", skipped, "lots of things" | Default fallback: "Drop one note about something you're working on into `<vault>/<domain-folder>/`. Ask Claude something simple about it — 'summarise this', 'what would I need to do next', 'who else has written about this?' — to feel out the loop. Then come back and ask for help with the actual pressing thing once you've seen Claude has access." |

If the user names something not covered above (e.g. "I'm building a website" / "I need to plan a trip"), pick the closest match or use the default fallback. Substitute the chosen recommendation as `{{DAY_1_TASK}}` in step 8b.

Hold all answers in working memory for the generation phase.

### 5. Locate templates

Templates ship with the system. Look in this order:

1. `~/.claude/templates/starter-claude-config/` and `~/.claude/templates/starter-vault/` — if both exist, use these.
2. If missing, clone the repo to a stable location:

   ```bash
   STABLE_REPO="$HOME/.claude/repos/mmf-claude-code"
   if [ ! -d "$STABLE_REPO" ]; then
     mkdir -p "$HOME/.claude/repos"
     git clone --depth 1 https://github.com/marinemegafauna/mmf-claude-code.git "$STABLE_REPO"
   fi
   ```

   Templates are under `$STABLE_REPO/templates/`. Copy them into `$HOME/.claude/templates/` so future runs find them locally. (Use `$HOME`, not `~`, in any quoted Bash arg — see step 3d.)

3. If `git clone` fails (network, auth, or no `git` installed): the repo is private, so `WebFetch` against `raw.githubusercontent.com` won't work either. Halt and tell the user:

   > *"I can't reach the templates this system needs. The repo is private, and I can't fetch it without `git` and access. If you're seeing this, either: (a) you don't have access yet — message Simon with your GitHub username; (b) git isn't installed — open Terminal and run `xcode-select --install` to install Apple's Command Line Tools (a few minutes), then say 'continue'; (c) you're offline."*

### 6. Generate baseline outputs

For each template file, do **placeholder substitution then write**:

**6a. Vault root `CLAUDE.md`.** Read `~/.claude/templates/starter-vault/CLAUDE.md`. Substitute:

- `{{USER_NAME}}` → from Q1 (extract a clear name; if user gave a description, infer or ask)
- `{{USER_BIO}}` → from Q1 (the full description)
- `{{USER_PREFERENCES}}` → from Q3 + Q4 (compose a paragraph)
- `{{VAULT_STRUCTURE}}` → list of folders being created (filled from Q2 + the SYSTEM + INBOX defaults)
- `{{ADDITIONAL_PREFERENCES}}` → from Q5 (voice sample → distilled rule, e.g. "match the conversational-but-informed tone of the sample") + Q6 (anything else)
- `{{INSTALL_DATE}}` → today's ISO date

Write to `<vault>/CLAUDE.md`.

**6b. Inbox folder.**

```bash
mkdir -p "<vault>/INBOX"
```

**6c. SYSTEM folder + log files.**

```bash
mkdir -p "<vault>/SYSTEM/Processes" "<vault>/SYSTEM/templates"
```

Copy from templates:
- `Session Handoff Log.md` → `<vault>/SYSTEM/Session Handoff Log.md`
- `Decision Log.md` → `<vault>/SYSTEM/Decision Log.md`
- `Friction Log.md` → `<vault>/SYSTEM/Friction Log.md`
- `Self-Improvement Changelog.md` → `<vault>/SYSTEM/Self-Improvement Changelog.md`
- `Processes/Process Note Template.md` → `<vault>/SYSTEM/Processes/Process Note Template.md`
- `folder-CLAUDE.template.md` → `<vault>/SYSTEM/templates/folder-CLAUDE.template.md`

Each is template content as-is — examples included to show shape; user deletes when adding their first real entry.

**6d. Global `~/.claude/CLAUDE.md`.** If it doesn't already exist, copy from `~/.claude/templates/starter-claude-config/CLAUDE.md` as-is. The global CLAUDE.md template has no per-install placeholders — its `## Vault path` section instructs Claude to compute the project key at runtime (every non-alphanumeric character in the vault path replaced by a hyphen — `/Users/jane/Documents/My Vault` → `-Users-jane-Documents-My-Vault`).

If `~/.claude/CLAUDE.md` already exists with content the user didn't write this session: back it up to `~/.claude/CLAUDE.md.bak-<timestamp>` automatically, replace with the starter, then tell the user:

> *"I found an existing global Claude config from before today and saved a copy to `~/.claude/CLAUDE.md.bak-<timestamp>`. The new starter config is now live. If you remember adding rules to the old one, tell me 'merge the backup' and I'll walk through it."*

**6e. Starter `MEMORY.md`.** Compute the project key (Claude Code's dash-sanitised absolute vault path — every non-alphanumeric char replaced with a hyphen), create the directory:

```bash
mkdir -p "$HOME/.claude/projects/<project-key>/memory"
```

Copy `~/.claude/templates/starter-claude-config/MEMORY.md` to `$HOME/.claude/projects/<project-key>/memory/MEMORY.md`. Substitute `{{VAULT_PROJECT_KEY}}` and `{{VAULT_NAME_URL_ENCODED}}`.

Then copy the Tier 2 leaf examples (the `.example` files keep them dormant — they don't auto-load until the user renames them):

```bash
cp ~/.claude/templates/starter-claude-config/memory_examples/*.md.example \
   "$HOME/.claude/projects/<project-key>/memory/"
```

These ship as templates the user can adopt later — when they encounter a real piece of feedback that fits one of the patterns (email voice, tool quirks), they edit the example, drop the `.example` suffix, and add a one-line pointer in the MEMORY.md "Tier 2" section.

**6f. Defer config.json and kickoff to after the domain pass.** Do not write `config.json` or `Getting Started.md` here. Both depend on decisions made in step 7 (whether the user opted into domain folders, which domains were created, what prefix style was chosen). Hold the values you'd write — `tools.task_manager` from Q7 mapping, `tools.codex_available` / `tools.gemini_available` from `command -v` probes — in working memory and combine with step 7's outcomes during step 8.

**6g. Defer kickoff `Getting Started.md` to after the domain pass** (see step 8). The kickoff includes a `Folder-level CLAUDE.md exists for: {{DOMAIN_LIST}}` line that can't be filled correctly until step 7 has run. Hold the kickoff template content in working memory.

The kickoff template (referenced by step 8):

```markdown
# Getting Started — your first vault note

Set up by `/onboard` on {{INSTALL_DATE}}. This note is yours to edit.

## What just happened

- Your vault is at `{{VAULT_PATH}}`.
- Root CLAUDE.md is populated from your interview answers.
- Folder-level CLAUDE.md exists for: {{DOMAIN_LIST}}.
- The system is *almost* active — see "One last setup step" below.

## One last setup step — point Claude Code at your vault

You ran `/onboard` from a temporary scratch folder, so the Claude Code
session that just finished can't actually see this vault. To activate the
CLAUDE.md cascade:

1. **Quit Claude Code** (Cmd-Q in the desktop app).
2. **Reopen the Claude desktop app** and click the Code tab.
3. **Choose this folder as the project**: `{{VAULT_PATH}}`.
4. **Run `/session-start`** in that new session — it should read this
   note back to you and confirm everything's loaded.

If you skip this, Claude won't read your CLAUDE.md files and the system
behaves like vanilla Claude Code — no memory, no behavioural defaults,
no folder context. So: do it now.

## While you're here — two desktop-app tweaks

Two one-time settings that make day-to-day use much smoother. Apply now
before you quit Claude Code:

1. **Switch to Auto mode.** Look at the bottom-left of the prompt area —
   a small badge cycles between "default" / "Accept edits" / "Auto mode"
   (also via Shift-Tab). Use Auto mode. To make it default forever, add
   to `~/.claude/settings.json`:

   ```json
   { "permissions": { "defaultMode": "bypassPermissions" } }
   ```

2. **Press-and-hold the microphone button** in the prompt area to record
   voice notes. This is the fastest way to enter long answers and
   instructions — release to stop, then send. Don't structure what you
   say; ramble. Claude sorts through tangents and asks follow-ups when
   needed.

## Day 1 — try this concretely (after the relaunch)

Once you've quit Claude Code, reopened it against your vault, and run
`/session-start`, here's a specific anchor for your first real session
with the system based on what you told me is most pressing this week:

{{DAY_1_TASK}}

That's the whole loop. Notes live in Obsidian, you ask Claude, Claude reads
the same notes you do — plus all the context from your CLAUDE.md cascade.

If the suggestion above doesn't land or your priorities shifted: open
Obsidian, drop one note about anything you're thinking about into the
relevant folder, and ask Claude something simple about it ("summarise
this", "what would I need to do next"). The loop is the same regardless
of what you point it at.

## The two skills worth knowing

- **`/document`** at the end of a session — Claude records what was done so
  the next session picks up where you left off.
- **`/session-start`** at the top of a new session — Claude reads the last
  handoff and orients before any work.

The other skills surface when they're useful — Claude will mention them
in context. You don't need to learn them in advance.

- **Workflow:** `/update`, `/review-friction`, `/refresh-skills`
- **Tasks & writing:** `/todo`, `/science-paper`, `/research`, `/verify-citations`

## Two-week check-in

There's a follow-up note in your INBOX dated {{DATE_PLUS_14}}:
`INBOX/Onboarding follow-up — {{DATE_PLUS_14}}.md`. Worth opening then;
no urgency before.
```

(Substitution and write happen in step 8b after the domain pass — do not write here.)

### 7. Opt-in domain pass

If the user listed 2+ domains in Q2, ask:

> *"You named these domains: A, B, C. Want to set up folders for each with their own CLAUDE.md now? Recommended if you already know your domains; you can always add more later."*

Numbered options:
1. Yes (set up folders for all of them)
2. Just one (pick the most active for now)
3. Skip (system works fine with just the root vault; you can always add a domain folder later by saying "set up a folder for X" to Claude)

If yes (1 or 2), for each chosen domain:

**Per-domain drill (one at a time):**

> *"For the **{{DOMAIN}}** folder:*
> *D1. What's the work in this area like? (one or two lines)*
> *D2. Key people, tools, terminology, or conventions specific to this domain?*
> *D3. Anything different from your general writing voice here — more formal, more technical, more playful?"*

After their answer, generate the folder + folder-level CLAUDE.md by substituting into `~/.claude/templates/starter-vault/SYSTEM/templates/folder-CLAUDE.template.md`:

- `{{DOMAIN_NAME}}` → user's chosen folder name
- `{{ONE_PARAGRAPH_DESCRIPTION}}` → from D1
- `{{KEY_CONTEXT}}` → from D2
- `{{TONE_DIFFERENCES}}` → from D3
- `{{INSTALL_DATE}}` → today

Ask whether to use a numbered prefix (`01_<NAME>`) or unnumbered. Default suggestion: numbered if user has 4+ domains, unnumbered if fewer.

Write to `<vault>/<DOMAIN_FOLDER>/CLAUDE.md`.

### 8. Finalise config.json and kickoff (using step 7's actual outcomes)

This step exists because `config.json` and `Getting Started.md` both depend on decisions made during step 7 (domain pass). Writing them in step 6 would have meant guessing — see C13 in the third-pass red-team for the failure mode.

**8a. Per-vault `config.json`.** Read `~/.claude/templates/starter-claude-config/config.json.template`. Substitute all placeholders with values from this session. The fields that depend on step 7's outcome:

- `domains` array — one entry per domain folder actually created during step 7. If the user opted out (option 3) or the domain pass was skipped (fewer than 2 domains in Q2), write `"domains": []` and remove the placeholder block per the template's `_domains_comment`. Otherwise emit one entry per chosen folder, populating `folder_name`, `display_name`, and `claude_md_path` from the per-domain drill.
- `features.domain_folders_opted_in` — `true` only if at least one domain folder was created in step 7; `false` otherwise.
- `features.numbered_folder_prefixes` — `true` if step 7 used numbered prefixes (`01_<NAME>`), `false` if unnumbered.

The fields that don't depend on step 7 (already held in working memory from step 6f's deferred work):

- `tools.task_manager` → string from Q7 mapping (`things3`, `todoist`, `apple_reminders`, `vault_todo`) or `null` if the user wasn't sure or skipped. Quote the value if non-null; write `null` (no quotes) if null. If the user named an unsupported task manager (Asana, Linear, etc.), write `vault_todo` so /todo has a working fallback.
- `tools.codex_available` → `true` if `command -v codex >/dev/null 2>&1`, else `false`.
- `tools.gemini_available` → `true` only if `command -v gemini` AND `~/.gemini/oauth_creds.json` exists.
- `user.name` → from Q1 (extracted clear name).
- `user.role` → from Q1 (the full description / role line).
- `features.is_simon` → always `false` for newcomer installs.

Write the result to `$HOME/.claude/projects/<project-key>/config.json`. After writing, validate with `python3 -c 'import json; json.load(open("..."))'` — if parsing fails, print the offending line, fix, and rewrite. Skills downstream depend on this file being valid JSON.

**8b. Kickoff `Getting Started.md`.** Take the template held from step 6g, substitute placeholders including:

- `{{DOMAIN_LIST}}` → comma-separated list of folders created in step 7. If zero folders were created, replace the entire bullet with: `- Folder-level CLAUDE.md: none created during onboarding (root vault only — you can add domains later by saying "set up a folder for X" to Claude).`
- `{{DATE_PLUS_14}}` → today + 14 days, ISO format.
- `{{DAY_1_TASK}}` → the concrete first-task recommendation built from Q8 per the mapping table in step 4. If the user skipped Q8 or gave a vague answer, use the default fallback prose from the mapping table. The recommendation should be specific (name a skill or a concrete action), not generic ("try the system out") — the whole point of Q8 is to give them a non-empty Day-1 starting point.

Write to `<vault>/INBOX/Getting Started.md`, then open it in Obsidian:

```bash
open "obsidian://open?vault=<url-encoded-vault-name>&file=INBOX%2FGetting%20Started"
```

### 9. Write the two-week follow-up note

Compute `{{DATE_PLUS_14}}` (today + 14 days, ISO format). Write to `<vault>/INBOX/Onboarding follow-up — {{DATE_PLUS_14}}.md`:

```markdown
# Onboarding follow-up — {{DATE_PLUS_14}}

Written by `/onboard` on {{INSTALL_DATE}} as a two-week check-in. You've had
~14 days with your Claude Code setup. A couple of things worth considering
now that you've lived with it.

## The nightly self-improvement loop

Optional, but useful once friction has accumulated. It's a scheduled
automation (a macOS background task) that scans your Friction Log overnight
and proposes fixes — the system improves itself while you sleep. Setup takes
~30 minutes. To install, ask Claude:

> *"Walk me through installing the nightly self-improvement loop."*

## New domain folder?

If you've discovered a new area of work since onboarding (a project, a
client, a new role), ask Claude to set up a folder for it:

> *"Set up a folder for {{NEW_DOMAIN}}."*

Claude uses the per-domain template and walks through the same drill as
the original interview.

## How to dismiss

Read it, decide what (if anything) to do, then delete the file or move it
to your archive folder. The system doesn't watch for it.
```

Substitute placeholders. This is a static dated note, not a scheduled automation — the user encounters it whenever they next browse INBOX. The kickoff `Getting Started.md` references it explicitly so they know it's there.

### 10. Confirm and close

Brief summary:

```
Setup complete.
Vault: <path>
Root CLAUDE.md: written
Folder CLAUDE.md: <count> domains
Logs: ready at SYSTEM/
Skills installed: /onboard, /document, /session-start, /update, /review-friction, /refresh-skills, /todo, /science-paper, /research, /verify-citations
Two-week follow-up note: INBOX/Onboarding follow-up — <date>.md

⚠️ ONE LAST STEP — point Claude Code at your vault.

You ran /onboard from a throwaway folder. Your vault now exists at:

  <path>

But Claude Code is still pointed at the folder you started in, so it
can't see your vault's CLAUDE.md cascade. To finish setup:

1. Quit Claude Code (Cmd+Q).
2. Reopen the Claude desktop app and click the Code tab.
3. When it asks which folder to open, choose your vault folder above.
4. Run /session-start in that new session — it will read your kickoff
   note and confirm the cascade is loading correctly.

Your kickoff note (INBOX/Getting Started.md) is open in Obsidian for
reference. See you in the next session.
```

End. Don't chain into other skills. Don't suggest follow-on work — the user MUST quit and relaunch Claude Code against the vault, and any skill chain would happen in the wrong project root.

## Self-assessment (post-run)

Silently note: did the discovery interview produce sharp-enough answers to populate CLAUDE.md well, or did the questions need rewording? If users keep producing thin answers to a particular question, propose a SKILL.md edit to that question. Don't write to disk unless confirmed.
