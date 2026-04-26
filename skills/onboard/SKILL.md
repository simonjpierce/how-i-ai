---
name: onboard
description: First-run setup for a new Claude + Obsidian system. Detects whether the user already has Obsidian, walks them through install if not, runs a short discovery interview (5–7 questions), and writes a personalised CLAUDE.md cascade, starter MEMORY.md, log files, and kickoff note into their vault. Optional domain-folder pass. Schedules a follow-up routine in 2 weeks for the nightly self-improvement loop. Use when the user says "/onboard", "set up my vault", "walk me through this system", or pastes the README's three-step prompt.
allowed-tools: Read, Write, Edit, Bash, Glob, Skill
---

This skill is the bridge from "nothing installed" to "working Claude system." It hides the architectural detail behind a short interview — the user doesn't have to read or understand the `getting-started/00–04` docs to benefit from them.

## Preamble — read this back to the user before starting

```
Welcome. I'll walk you through setting up Claude Code + Obsidian as a working
system in about 10–15 minutes. This is an interview, not an essay — short
answers are fine.

If you'd rather dictate than type, ChatGPT's voice transcription (desktop or
iOS app) is currently the cleanest tool for this — speak into ChatGPT, copy
the text, paste here.

Two things I'll check at the start, then we'll get going.
```

## When something goes wrong

If a step fails (template path missing, vault path not writable, /schedule unavailable, etc.), update this skill BEFORE continuing the workaround. Add the failure mode and the recovery path. Don't ship friction onto future users.

## Steps

### 0. Set tab title

```bash
MY_TTY=$(ps -o tty= -p $PPID 2>/dev/null | tr -d ' ') && echo "onboarding" > "/tmp/claude-title-${MY_TTY}"
```

### 1. Pre-flight — auto-approval mode + filesystem write capability

**1a. Auto-approval mode.** This system assumes Claude Code is in auto-approval mode — too many permission prompts kills the experience. If you can detect the current mode, do; otherwise ask:

> *"Quick check: is Claude Code set to auto-approval mode? (Settings → Permissions → Auto-approve.) The system works much better that way — without it, I'll be interrupting you with a permission prompt for every file write, which gets old fast."*

If they say no or don't know, walk them through enabling it before continuing. Don't proceed past Phase 2 in default-prompt mode — friction will wreck the rest of the flow.

**1b. Filesystem write capability.** Try to write a small test file to `/tmp/onboard-test.txt`. If it succeeds, full filesystem mode — proceed normally. If it fails (e.g. running in Claude Chat web with no filesystem access), STOP and tell the user:

> *"I can't write files in this environment, which means I can't actually install the system here. You'll want to either (a) open this conversation in Claude Code in the Claude Desktop app — same prompt, real filesystem access — or (b) for an in-Claude.ai alternative, switch to Cowork. Once you're there, paste the README prompt again and I'll resume."*

Do not attempt the rest of the skill in a no-filesystem context.

### 2. Detect & route

Ask:

> *"Do you already have an Obsidian vault, or are we setting one up from scratch?"*

Numbered options:
1. Fresh — set up Obsidian and a new vault
2. Existing — I have a vault already, point Claude at it

Branch on the answer:

- Fresh → Phase 3 (setup logistics).
- Existing → ask for the absolute path, verify it exists with `ls`, check for an existing `CLAUDE.md` at the root (warn the user if found — offer to merge or back up before overwriting). Then jump to Phase 4.

### 3. Setup logistics (fresh-vault path only)

**3a. Obsidian install.** If they don't have Obsidian:

> *"You'll need Obsidian. It's free. Download it from `https://obsidian.md/download` — install, open, then come back here when it's running."*

Wait for them to confirm install is complete. Don't try to install Obsidian programmatically (out of scope for the skill).

**3b. Vault location.** Ask where they want the vault:

> *"Where should your vault live? Suggested: `~/Documents/Obsidian Vault`. If you use iCloud / Dropbox / Google Drive sync, pick a location inside that sync folder so the vault syncs across devices."*

Numbered options:
1. `~/Documents/Obsidian Vault` (default, no sync)
2. iCloud (typical path: `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/<name>`)
3. Dropbox / Google Drive (user provides path)
4. Other (user provides path)

**3c. Sync option.** Note the sync choice for `Getting Started.md` later. Don't try to configure sync — instructional only.

**3d. Create vault folder.**

```bash
mkdir -p "<chosen-path>"
```

Verify writable:

```bash
touch "<chosen-path>/.write-test" && rm "<chosen-path>/.write-test"
```

If write-test fails (e.g. iCloud not yet synced), explain and offer alternative paths.

### 4. Discovery interview

Ask the questions one at a time. Number-replies-OK except where genuinely free-form.

**Q1.** *"In a sentence or two — who are you, and what kinds of work will you mostly use this setup for?"*

**Q2.** *"When you switch tasks, what are the main 'modes' or 'hats' you switch between? List 2–5. Examples: 'research papers and a personal blog'; 'three different clients I consult for'; 'work + parenting + creative writing'."*

**Q3.** *"Spelling — UK / US / NZ / Australian / other? And anything else about how you write — typical formality, words you avoid, emoji preferences?"*

**Q4.** *"Response style — do you prefer concise direct answers, or detailed step-by-step? And: when something's ambiguous, do you want me to ask first, or make a best-guess and let you correct me?"*

**Q5 (optional).** *"Paste a paragraph or two of writing you've done recently — email, blog post, anything — so I can match your voice. Skip if nothing's handy."*

**Q6.** *"Anything specific about how you work, who you work with, or context I should keep in mind that the questions above missed?"*

Hold all answers in working memory for the generation phase.

### 5. Locate templates

Templates ship with the system. Look in this order:

1. `~/.claude/templates/starter-claude-config/` and `~/.claude/templates/starter-vault/` — if both exist, use these.
2. If missing, clone the repo to a temp directory:

   ```bash
   TMP_REPO="/tmp/mmf-claude-code-onboard-$(date +%s)"
   git clone --depth 1 https://github.com/marinemegafauna/mmf-claude-code.git "$TMP_REPO"
   ```

   Templates are under `$TMP_REPO/templates/`. Copy them into `~/.claude/templates/` so future runs find them locally.

3. If git is unavailable, fall back to fetching individual template files via WebFetch from `https://raw.githubusercontent.com/marinemegafauna/mmf-claude-code/main/templates/...`. This is slower; only use if git fails.

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
mkdir -p "<vault>/AI_WORKFLOW/CLAUDE" "<vault>/AI_WORKFLOW/templates"
```

Copy from templates:
- `Session Handoff Log.md` → `<vault>/AI_WORKFLOW/CLAUDE/Session Handoff Log.md`
- `Decision Log.md` → `<vault>/AI_WORKFLOW/CLAUDE/Decision Log.md`
- `Friction Log.md` → `<vault>/AI_WORKFLOW/CLAUDE/Friction Log.md`
- `folder-CLAUDE.template.md` → `<vault>/AI_WORKFLOW/templates/folder-CLAUDE.template.md`

Each is template content as-is — examples included to show shape; user deletes when adding their first real entry.

**6d. Global `~/.claude/CLAUDE.md`.** If it doesn't already exist, copy from `~/.claude/templates/starter-claude-config/CLAUDE.md`. Substitute:

- `{{VAULT_PROJECT_KEY}}` → URL-encoded vault path (the project subdirectory key Claude Code uses)

If `~/.claude/CLAUDE.md` already exists, ASK the user whether to overwrite, append, or skip — don't silently clobber existing customisations.

**6e. Starter `MEMORY.md`.** Compute the project key (Claude Code's URL-encoded vault path), create the directory:

```bash
mkdir -p "$HOME/.claude/projects/<project-key>/memory"
```

Copy `~/.claude/templates/starter-claude-config/MEMORY.md` to `$HOME/.claude/projects/<project-key>/memory/MEMORY.md`. Substitute `{{VAULT_PROJECT_KEY}}` and `{{VAULT_NAME_URL_ENCODED}}`.

**6f. Per-vault `config.json`.** Read `~/.claude/templates/starter-claude-config/config.json.template`. Substitute all placeholders with values from this session. Write to `$HOME/.claude/projects/<project-key>/config.json`.

**6g. Kickoff `Getting Started.md`.** Generate a personalised note. Approximate template:

```markdown
# Getting Started — your first vault note

Set up by `/onboard` on {{INSTALL_DATE}}. This note is yours to edit; treat
it as your map for the first week.

## What just happened

- Your vault is at `{{VAULT_PATH}}`.
- Root CLAUDE.md is populated with your identity, preferences, and domains.
- Folder-level CLAUDE.md exists for: {{DOMAIN_LIST}}.
- Logs are ready at `AI_WORKFLOW/CLAUDE/`: Session Handoff, Decision, Friction.

## Things to try this week

1. **Format a real meeting** — record audio, drop the file in here, run
   `/transcribe`. The skill produces a clean speaker-labelled transcript and
   extracts TODOs and IDEAs into your daily note.
2. **Draft an email** — ask Claude to "draft a reply to <person> about <topic>",
   pointing at relevant project notes if you have them. The CLAUDE.md cascade
   means your voice and conventions apply automatically.
3. **End a session with `/document`** — when you wrap up, ask Claude to record
   what was done and what's next. The next session reads it first and picks
   up where you left off.

## Meeting capture

Capturing meetings as text the vault can read is one of the highest-value
practices in this system. There's no perfect tool yet, but options include:

- **Audio Hijack** ($60, macOS) — what the system author uses; produces
  highest-quality recordings.
- **ChatGPT voice mode** — decent quality, free with a Plus plan; handy on the
  go.
- **Otter.ai** — meeting-focused, generates transcripts directly; web app.
- **Phone voice memos** — universal fallback; quality varies but works.

Once you have audio, run `/transcribe` to format it.

## Friction is welcome

When something feels harder than it should, tell Claude — corrections become
permanent. The Friction Log captures these for review. Run `/review-friction`
weekly (it takes ~5 minutes).

## Contributing back

If you find something that could work better — a skill that needs a tweak,
a step that's confusing, a workflow worth adding — you don't need to know
git, branches, or pull requests to contribute. Just describe what you want
to Claude Code:

> *"Add a step to /transcribe that strips out filler words."*
>
> *"The kickoff note should mention X."*
>
> *"This rule in MEMORY.md fires too often — can we narrow it?"*

Claude will edit the relevant files in a local clone of `mmf-claude-code`,
commit with attribution, push to a branch, and open a pull request. The
mechanics of contribution are no harder than describing the improvement.

## More skills

This system ships with five core skills (`/onboard`, `/document`,
`/session-start`, `/update`, `/review-friction`). The
[`mmf-claude-code` repo](https://github.com/marinemegafauna/mmf-claude-code)
has more — `/transcribe`, `/red-team`, `/verify-citations`,
`/pdf-to-markdown`, `/mmf-brand`. Add them as you hit work that benefits.

## Self-improvement loop

In about two weeks, Claude will check in to ask whether you'd like to install
the nightly self-improvement automation — a scheduled process that scans your
Friction Log overnight and proposes fixes. By then your log will have enough
content for it to be useful. You can decline or defer when the time comes.
```

Substitute placeholders. Write to `<vault>/INBOX/Getting Started.md`.

Open it in Obsidian:

```bash
open "obsidian://open?vault=<url-encoded-vault-name>&file=INBOX%2FGetting%20Started"
```

### 7. Opt-in domain pass

If the user listed 2+ domains in Q2, ask:

> *"You named these domains: A, B, C. Want to set up folders for each with their own CLAUDE.md now? Recommended if you already know your domains; you can always add more later."*

Numbered options:
1. Yes — set up folders for all of them
2. Just one — pick the most active for now
3. Skip — root CLAUDE.md only is fine for now

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

### 8. Schedule self-improvement follow-up

Invoke the `/schedule` skill (or use its underlying mechanism) to create a one-shot routine for **14 days from today**, prompt:

> *"You've been using your Claude Code setup for two weeks now. Your Friction Log has had time to accumulate entries. Want me to walk you through installing the nightly self-improvement loop? It scans the log overnight and proposes fixes — about 30 minutes to set up, then runs without you. You can also defer or decline."*

Confirm to the user that the follow-up is scheduled. If `/schedule` isn't available, fall back to writing a System housekeeping entry in the Daily Log dated 14 days out.

### 9. Confirm and close

Brief summary:

```
Setup complete.
Vault: <path>
Root CLAUDE.md: written
Folder CLAUDE.md: <count> domains
Logs: ready at AI_WORKFLOW/CLAUDE/
Skills installed: /onboard, /document, /session-start, /update, /review-friction
Follow-up scheduled: <date> (self-improvement loop check-in)

Your kickoff note is open in Obsidian — start there.
```

End. Don't chain into other skills. Don't suggest follow-on work. The user has their kickoff note; they'll take it from here.

## Self-assessment (post-run)

Silently note: did the discovery interview produce sharp-enough answers to populate CLAUDE.md well, or did the questions need rewording? If users keep producing thin answers to a particular question, propose a SKILL.md edit to that question. Don't write to disk unless confirmed.
