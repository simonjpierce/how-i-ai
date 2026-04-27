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
Short answers are fine.

If you'd rather dictate than type: macOS's built-in dictation works (press Fn
twice in any text field). ChatGPT's voice mode is also good if you have a
Plus account.

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

**1b. Auto-approval mode.** This system assumes Claude Code is in auto-approval mode — too many permission prompts kills the experience. Tell the user what it is, what it affects, and how to turn it on, before asking anything:

> *"Before we go further: Claude Code asks for permission every time it writes a file unless you turn on auto-approve. For this setup we'll be writing 20+ files, so the prompts get old fast. Auto-approve only affects this app — it can't run anything outside the folders you've pointed it at, and you can turn it off again any time."*
>
> *"To enable it: in the Claude desktop app, click the Claude menu in the top-left of your screen → Settings → Permissions tab → toggle 'Auto-approve file edits' on. Tell me when it's done."*

If the user reports a different layout (Anthropic moves these toggles between releases), suggest searching Settings for "auto-approve" or "permission". Don't proceed past Phase 2 in default-prompt mode — friction will wreck the rest of the flow.

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

Ask the questions one at a time. Number-replies-OK except where genuinely free-form.

**Q1.** *"In a sentence or two — who are you, and what kinds of work will you mostly use this setup for?"*

**Q2.** *"When you switch tasks, what are the main 'modes' or 'hats' you switch between? List 2–5. Examples: 'research papers and a personal blog'; 'three different clients I consult for'; 'work + parenting + creative writing'."*

**Q3.** *"Spelling preference — UK / US / NZ / Australian, or 'doesn't matter'? (If you're unsure: working with the MMF team in marine biology, NZ/UK is the safe default; writing for US journals or US donors, US.) And anything else about how you write — typical formality, words you avoid, emoji preferences?"*

**Q4.** *"Response style — do you prefer concise direct answers, or detailed step-by-step? And: when something's ambiguous, do you want me to ask first, or make a best-guess and let you correct me?"*

**Q5 (optional).** *"Paste a paragraph or two of writing you've done recently — email, blog post, anything — so I can match your voice. Skip if nothing's handy."*

**Q6.** *"Anything specific about how you work, who you work with, or context I should keep in mind that the questions above missed?"*

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
- `{{VAULT_STRUCTURE}}` → list of folders being created (filled from Q2 + the AI_WORKFLOW + INBOX defaults)
- `{{ADDITIONAL_PREFERENCES}}` → from Q5 (voice sample → distilled rule, e.g. "match the conversational-but-informed tone of the sample") + Q6 (anything else)
- `{{INSTALL_DATE}}` → today's ISO date

Write to `<vault>/CLAUDE.md`.

**6b. Inbox folder.**

```bash
mkdir -p "<vault>/INBOX"
```

**6c. AI_WORKFLOW folder + log files.**

```bash
mkdir -p "<vault>/AI_WORKFLOW/CLAUDE/Processes" "<vault>/AI_WORKFLOW/templates"
```

Copy from templates:
- `Session Handoff Log.md` → `<vault>/AI_WORKFLOW/CLAUDE/Session Handoff Log.md`
- `Decision Log.md` → `<vault>/AI_WORKFLOW/CLAUDE/Decision Log.md`
- `Friction Log.md` → `<vault>/AI_WORKFLOW/CLAUDE/Friction Log.md`
- `Processes/Process Note Template.md` → `<vault>/AI_WORKFLOW/CLAUDE/Processes/Process Note Template.md`
- `folder-CLAUDE.template.md` → `<vault>/AI_WORKFLOW/templates/folder-CLAUDE.template.md`

Each is template content as-is — examples included to show shape; user deletes when adding their first real entry.

**6d. Global `~/.claude/CLAUDE.md`.** If it doesn't already exist, copy from `~/.claude/templates/starter-claude-config/CLAUDE.md`. Substitute:

- `{{VAULT_PROJECT_KEY}}` → Claude Code's per-vault project key. **Computed by replacing every non-alphanumeric character in the absolute vault path with a hyphen** (NOT URL-encoded — Claude Code uses dash-sanitisation). Bash: `PROJECT_KEY=$(echo "$VAULT_PATH" | sed 's|[^a-zA-Z0-9]|-|g')`. Example: `/Users/jane/Documents/My Vault` → `-Users-jane-Documents-My-Vault`.

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

**6f. Per-vault `config.json`.** Read `~/.claude/templates/starter-claude-config/config.json.template`. Substitute all placeholders with values from this session. Write to `$HOME/.claude/projects/<project-key>/config.json`.

**6g. Kickoff `Getting Started.md`.** Generate a personalised note. Approximate template:

```markdown
# Getting Started — your first vault note

Set up by `/onboard` on {{INSTALL_DATE}}. This note is yours to edit.

## What just happened

- Your vault is at `{{VAULT_PATH}}`.
- Root CLAUDE.md is populated from your interview answers.
- Folder-level CLAUDE.md exists for: {{DOMAIN_LIST}}.
- Logs ready at `AI_WORKFLOW/CLAUDE/`: Session Handoff, Decision, Friction.
- Skills installed: `/onboard`, `/document`, `/session-start`, `/update`, `/review-friction`, `/refresh-skills`.

## Day 1 — settle in

The system is set up. There's nothing you have to do today besides:

1. Open Obsidian and look around your folder structure.
2. If you have existing notes, drop them into the appropriate folders.
3. Try a simple Claude interaction — ask any question, point at a file you have, see how it feels.

The cascade is active. Anything you ask Claude inside this vault now uses
the rules you set up. You don't need to invoke any skill specifically;
Claude reads the CLAUDE.md cascade automatically.

## When you have actual work

The starter skills handle the most common workflows:

- **`/document`** — when you wrap up a session, ask Claude to record what
  was done. The next session reads it first and picks up where you left off.
- **`/session-start`** — at the top of a new session, this orients Claude
  on what was happening and surfaces any stale Friction Log entries.
- **`/update`** — keeps related notes current after substantial work in
  one area.
- **`/review-friction`** — weekly walk through your Friction Log, marking
  entries resolved / deferred / wontfix.

Use them as the work calls — there's no required order.

## Friction is welcome

When something feels harder than it should, tell Claude — corrections
become permanent. The Friction Log captures these. Run `/review-friction`
weekly (about 5 minutes once you're in the habit).

## Meeting capture

Capturing meetings as text the vault can read is one of the highest-value
practices in this system. There's no perfect tool yet, but options include:

- **Audio Hijack** ($60, macOS) — what Simon uses; produces highest-quality
  recordings.
- **ChatGPT voice mode** — decent quality, free with a Plus plan; handy on the
  go.
- **Otter.ai** — meeting-focused, generates transcripts directly; web app.
- **Phone voice memos** — universal fallback; quality varies but works.

Once you have an audio file or text transcript in your vault, ask Claude to
clean it up and extract TODOs.

## Contributing back

If you find something that could work better — a step that's confusing, a
rule that fires too often, a workflow worth adding — describe what you want
to Claude:

> *"The kickoff note should mention X."*
>
> *"This rule in MEMORY.md fires too often — can we narrow it?"*

Claude can edit the relevant files in a local clone of `mmf-claude-code`,
commit with attribution, push, and open a pull request. You don't need to
know git, branches, or PR workflow — just describe the improvement.

## Two-week check-in

There's a follow-up note in your INBOX dated {{DATE_PLUS_14}}:
`INBOX/Onboarding follow-up — {{DATE_PLUS_14}}.md`. By that point your
Friction Log will have a few entries; the note prompts you to consider
whether you want the nightly self-improvement loop set up. Open it in two
weeks (or sooner if you're curious).
```

Substitute placeholders (including `{{DATE_PLUS_14}}` = today + 14 days, ISO format). Write to `<vault>/INBOX/Getting Started.md`.

Open it in Obsidian:

```bash
open "obsidian://open?vault=<url-encoded-vault-name>&file=INBOX%2FGetting%20Started"
```

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

After their answer, generate the folder + folder-level CLAUDE.md by substituting into `~/.claude/templates/starter-vault/AI_WORKFLOW/templates/folder-CLAUDE.template.md`:

- `{{DOMAIN_NAME}}` → user's chosen folder name
- `{{ONE_PARAGRAPH_DESCRIPTION}}` → from D1
- `{{KEY_CONTEXT}}` → from D2
- `{{TONE_DIFFERENCES}}` → from D3
- `{{INSTALL_DATE}}` → today

Ask whether to use a numbered prefix (`01_<NAME>`) or unnumbered. Default suggestion: numbered if user has 4+ domains, unnumbered if fewer.

Write to `<vault>/<DOMAIN_FOLDER>/CLAUDE.md`.

### 8. Write the two-week follow-up note

Compute `{{DATE_PLUS_14}}` (today + 14 days, ISO format). Write to `<vault>/INBOX/Onboarding follow-up — {{DATE_PLUS_14}}.md`:

```markdown
# Onboarding follow-up — {{DATE_PLUS_14}}

Written by `/onboard` on {{INSTALL_DATE}} as a two-week check-in. By the time
you're reading this, you've had ~14 days with your Claude Code setup and your
Friction Log will have a few entries.

## Worth considering now

- **Have you been running `/review-friction` weekly?** If the friction log
  has accumulated 5+ `[OPEN]` entries, give it a read.
- **Would the nightly self-improvement loop be useful?** It's a scheduled
  automation (LaunchAgent on macOS) that scans your Friction Log overnight
  and proposes fixes. Setup takes ~30 minutes. Ask Claude:
  *"Walk me through installing the nightly self-improvement loop."*
- **Domain folders.** If you skipped the domain pass during onboarding or
  have added domains since, ask Claude to walk through the per-domain drill
  for any new folder using the `folder-CLAUDE.template.md` template at
  `<vault>/AI_WORKFLOW/templates/`.
- **Voice references.** As you correct Claude's email/writing voice,
  capture those rules in `<vault>/Voice References/<context>.md` for re-use.

## How to dismiss

Read it, decide what (if anything) to do, then delete the file or move it
to `06_ARCHIVE/`. The system doesn't watch for it.
```

Substitute placeholders. This is a static dated note, not a scheduled automation — the user encounters it whenever they next browse INBOX. The kickoff `Getting Started.md` references it explicitly so they know it's there.

### 9. Confirm and close

Brief summary:

```
Setup complete.
Vault: <path>
Root CLAUDE.md: written
Folder CLAUDE.md: <count> domains
Logs: ready at AI_WORKFLOW/CLAUDE/
Skills installed: /onboard, /document, /session-start, /update, /review-friction, /refresh-skills
Two-week follow-up note: INBOX/Onboarding follow-up — <date>.md

Your kickoff note is open in Obsidian — start there.
```

End. Don't chain into other skills. Don't suggest follow-on work. The user has their kickoff note; they'll take it from here.

## Self-assessment (post-run)

Silently note: did the discovery interview produce sharp-enough answers to populate CLAUDE.md well, or did the questions need rewording? If users keep producing thin answers to a particular question, propose a SKILL.md edit to that question. Don't write to disk unless confirmed.
