# Reference — An undo button for your whole vault

> **What this is.** The actual method behind [the *An undo button for your whole vault* workflow](../workflows/an-undo-button-for-your-vault.md), cleaned of the maintainer's personal specifics. A **starting point to adapt, not a drop-in.** The maintainer's setup is macOS, an iCloud-synced Obsidian vault, GitHub, Google Drive via rclone, and `launchd` (LaunchAgents) for scheduling; the same shapes work with cron or systemd, any rclone-supported cloud, and any sync provider.

## The layers

| Layer | Schedule | What it protects against |
|---|---|---|
| Live vault, synced by iCloud | continuous | a lost or broken laptop (but sync copies mistakes instantly) |
| Git history in the vault, pushed to a private GitHub repo | twice daily (03:00, 08:00) + every mid-session save | bad edits by anyone, including an AI; "what did this say last week?" |
| Whole vault, binaries included, copied to Google Drive | nightly (03:15) | a mistake the sync has already spread; losing the Apple account |
| AI configuration (instructions, skills, hooks, settings) in its own GitHub repo | daily (05:30) | losing the machinery that makes the vault useful |
| Machine infrastructure copied into the vault | weekly (Sunday) | a rebuild that stalls on "what was installed, and how was it scheduled?" |
| Time Machine to a network drive | when the Mac is on the home network | whole-machine restore |
| Photo drives copied to Google Drive | every 4 hours, when the drives are plugged in | losing a drive of originals |

Two further copies follow the same pattern for other data: the shared team cloud folder is copied nightly to a second provider (copy-only, so a deletion on the source never propagates), and the literature library mirror has its own daily git snapshot.

## Layer 1 — version history on the vault

- `git init` at the vault root; a `.gitignore` excludes binaries (images, PDFs, video), Obsidian's workspace churn and macOS metadata. Binaries are covered by the Drive layer instead.
- The job: if files changed, `git add -A` and commit with a timestamp message. Then push to the private repo, and push even when nothing changed if any earlier commit is still waiting (`git rev-list --count @{u}..HEAD` above zero): a push that failed last run, or an AI session's own commit, otherwise sits unsent while every run reports success. Only a clean tree with nothing waiting logs "No changes to commit" and stops. Log an explicit success line (`Pushed to GitHub` / `No changes to commit`) on every good run: the health check keys on it. On a push failure, log the cause from git's `fatal:`/`error:` line and retry next run.
- **Stale lock guard**: a `.git/index.lock` older than 10 minutes is treated as left behind by a crashed process and removed; a newer one means another git process may be working, so this run is skipped. Ten minutes is a judgement call, not proof: no git operation on a notes vault should hold the lock that long, but pick a threshold that suits your own setup.
- **Size guard**: a pre-commit hook unstages text or data files over 2 MB (a content-dense note that large can crash Obsidian's indexer) and lets the rest of the commit through. Every excluded path is recorded in a small state file, and the path is dropped from it the moment it commits cleanly. Without that record, the guard warns into a log nobody reads (see failure modes).
- **AI sessions commit too.** The mid-session save and end-of-session handover each make a scoped commit of the files they touched, labelled as such, so an AI session's changes are one reversible step in the history rather than smeared across the next timed snapshot. Before changing a file that holds the human's uncommitted edits, the AI commits those first, attributed to the human.
- **Restoring**: `git log -- "<note>"` shows the history of one note; `git show <commit>:"<note>"` prints an old version; `git checkout <commit> -- "<note>"` restores it. In practice you ask the AI ("put back what this note said before yesterday's session") and it runs these.

## Layer 2 — the nightly off-site copy

- `rclone sync` of the whole vault to a Drive folder, with `--backup-dir` pointing at a dated trash folder: anything the sync would overwrite or delete is moved there instead. Trash folders older than 30 days are purged at the end of each run.
- It runs once a night deliberately. Sync services propagate a deletion within seconds; this copy doesn't see the mistake until the next nightly run, and anything that run overwrites or deletes is kept in the dated holding folder for 30 days after that.
- **Pin the destination by folder ID**, not by name (`--drive-root-folder-id`). Name-based path resolution on Google Drive once misfiled about 50 dated trash folders at the Drive root. With the root pinned, the worst possible misfile stays inside the backup folder. A guard at the end of each run counts dated folders at the Drive root and raises a task if any appear; it never deletes them.
- **Wait for the network.** A job scheduled for 03:15 often fires before the network is back after the laptop wakes. Poll until the login host resolves (up to ~3 minutes) before starting, then retry a failed sync on a widening ladder (10, 20, 40 minutes). A plain 30-second retry fails the same way the first attempt did.
- Log an explicit `Sync complete` line on success, and a failure line that says in words that no copy exists for today.

## Layer 3 — the machinery

- **AI configuration**: the configuration folder is its own git repo, committed and pushed daily after the overnight jobs finish, under a lock shared with anything else that commits there. Consecutive push failures are counted, and two in a row raise an alert.
- **Machine infrastructure**, weekly: copy into the vault the hook and settings files, the scheduled-job definitions (mirroring the live set, so retired jobs drop out), helper scripts, package lists (`brew`, `pipx`, global `npm`, the AI CLI version), the search tool's config, and the cloud-copy config **with its login tokens stripped**. Script folders that already have their own git repository are left out; a second copy of those in the vault drifted when sessions edited the copy thinking it was live. Sweep whole folders rather than hand-picked file lists (see failure modes), and exclude Python virtual environments: they rebuild from the requirements file, and a 125 MB one inside the vault crashed Obsidian.
- **The rebuild guide updates itself.** The weekly job ends by regenerating the marked sections of the new-machine guide (installed packages, skills, hooks, scheduled jobs) from the live machine, writing only when something changed. The hand-written steps around those sections (order of installs, re-authentication, verification checklist) stay prose.

## The restore drill

The piece that's easiest to skip. The scheduler starts it daily, and a small state file makes the real work monthly: each backup (GitHub and Google Drive) stays due until it has passed once that calendar month, then waits for the next. Each pass restores one sample file, so it proves the restore path works, not that every file is covered.

1. **Pick the sample.** From a short fixed list of small system notes, choose one that is under 1 MB and hasn't changed since that backup's last logged success, so a mismatch means a broken backup rather than a recent edit. For the git target it must also match the local main branch. If nothing qualifies (the files are churning), defer rather than fail.
2. **Fetch it fresh.** For GitHub: a shallow, size-guarded clone into a private scratch folder, then read the file out. For Drive: stat the object, then copy just that file down with a transfer cap. Use the same pinned folder ID the backup job writes with; a name-based path can miss the real backup.
3. **Compare.** SHA-256 of the restored bytes against the live file. Match → PASS.
4. **Report.** When both targets pass for the month, write one quiet heartbeat line to the daily log and clear any open drill alerts. Any failure gets a named status (`FAIL_AUTH`, `FAIL_MISSING`, `FAIL_MISMATCH`, `FAIL_PULL`, `FAIL_GUARD`) and a deduplicated alert that says what to do next. Network trouble is deferred, not failed, but a month still not complete after seven days raises an "overdue" alert.

Guardrails: the drill never touches the live vault or either backup; its only writes are its scratch folder, its log and its alert state. Every git and rclone command passes an allowlist; restored content lives only in a private temporary folder capped at 100 MB; a single-instance lock stops overlapping runs; the whole run has a 10-minute budget. Nothing can write to the live vault or to either backup.

## Health checks

- **Morning backup check** (10:00): for each vault backup, look for a *success* line within the last 3 days. A 3-day tolerance lets travel Wi-Fi blips heal themselves; the last line of a log can be a failed push, so "ran today" is the wrong test. It also reads the size guard's record and reports any file the git layer hasn't covered, with how long it's been. It says those files are still safe on Drive only if the Drive copy succeeded today. Problems go to one deduplicated alert on the daily intake page (see [knowing when your automations broke](../workflows/knowing-when-your-automations-broke.md)), which clears itself on the next clean run.
- **Off-machine dead man's switch**: the two vault backups and the configuration backup ping [healthchecks.io](https://healthchecks.io) on success and on known failure. If a ping doesn't arrive on schedule, the service raises the alarm itself, which catches the case no local check can: the laptop is dead, asleep for a week, or the scheduler never started the job. A failed ping is only logged; it never marks the backup itself as failed.
- **Weekly checks**: the shared-folder copy must have a finished run within 8 days and a non-empty destination; the photo backup alerts when a drive's last *successful* copy is more than 14 days old. A broader weekly infrastructure check confirms every scheduled job is loaded and its script exists.

## Failure modes (all real)

- **Ten weeks of a file silently missing from git.** The size guard unstaged an automation-rewritten log over 2 MB every night and warned into a log nobody read, while every backup run reported success. Fix: record exclusions in a state file and have the morning check report them, as above.
- **No Drive copy for a day, and nobody knew.** The sync died 25 minutes in on a DNS drop; the single 30-second retry failed identically; the health check still reassured that git-excluded files were "covered by Drive". Fix: the retry ladder, and a check that only claims cover it has confirmed today.
- **Backups landing in the wrong place.** Name-based Drive paths put about 50 dated folders at the Drive root. Fix: pin the root folder ID, plus the stray guard.
- **Uncovered scripts.** Hand-picked lists of files to copy silently missed new scripts until someone went looking. Fix: sweep whole folders with excludes.
- **Git inside a sync folder.** Sync services can evict or conflict-copy files inside a `.git` folder and corrupt it. For a repo that must live inside a synced folder, keep the git objects outside it (`GIT_DIR` elsewhere, the synced folder as the work tree).

## What stays yours

Which cloud holds the second copy, how often each layer runs, which folders count as "machinery", whether you add a whole-machine backup or the monitoring service. The transferable spine: *keep a running history of every text file and let AI sessions commit their own work as labelled steps; keep a delayed, independent off-site copy; back up the configuration as well as the notes; restore a sample from each off-site copy on a schedule and compare it byte for byte; and check for evidence of success, from off the machine as well as on it.*
