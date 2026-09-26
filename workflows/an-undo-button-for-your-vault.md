# An undo button for your whole vault

Letting an AI edit your notes is only reasonable if you can get back what it changed. This is how to keep a running history of the vault, so an edit by you, a plugin or an AI can be seen and reversed, and how to keep copies that survive a lost laptop, a bad sync or a mistake nobody noticed for a week.

This is an idea file. Paste it into your AI agent — Claude Code or Codex — to build a version for your own work; it'll fill in the specifics (folder names, exact tools) in collaboration with you. (It has to be an agent that can create files on your machine — a plain chat assistant can't set this up.)

## The core idea

Once an AI is writing into your vault (tidying notes, updating project pages, filing transcripts overnight), mistakes stop being rare events you'd notice. A session misreads an instruction and rewrites the wrong section. An overnight job empties a file. You delete a folder you thought was a duplicate. And the sync service that keeps your notes on every device makes this worse, because iCloud, Dropbox and the rest are *sync*, not *backup*: they copy a deletion to every device within seconds, faithfully.

The fix is to treat the vault like a codebase. **The vault keeps a running history, so an edit can be undone**, and separate copies live in places that don't share a failure. The one principle underneath it: *a backup you have never restored from is a hope, not a backup.* So the system restores from its own backups on a schedule and checks that what comes back matches.

## The pieces

- **Version history on the vault itself.** The vault is a git repository: git is the version-tracking tool programmers use, and it works just as well on a folder of notes. A scheduled job records a snapshot of every changed text file twice a day and pushes it to a private GitHub repository. "What did this note say last Tuesday?" and "undo everything that session did to this file" each become one request to the AI. The maintainer's AI sessions also record a snapshot when they save progress mid-session, so an AI's changes arrive as their own labelled step in the history, easy to find and easy to reverse.
- **Keep your changes and the AI's apart.** If you've been editing a file the AI is about to change, the AI first records your edits that aren't yet in the history as their own snapshot, clearly labelled as yours, and only then makes its change. Undoing the AI's edit later can't take your work with it.
- **A second, independent copy every night.** A nightly job copies the whole vault, images and PDFs included, to Google Drive using rclone, a command-line tool for copying files to cloud storage. It runs once a night on purpose: a mistake that iCloud spreads within seconds doesn't reach this copy until the next nightly run. Files it would overwrite or delete are set aside in a dated holding folder for 30 days rather than lost.
- **The machinery gets backed up too.** Your notes aren't the only thing you'd have to rebuild. The AI's own configuration (its instructions, skills, hooks and settings) is committed and pushed to its own GitHub repository every morning. A weekly job copies the scheduled-job definitions, the helper scripts and a list of every installed tool into the vault, so they ride along with the vault's own backups.
- **A rebuild guide that keeps itself current.** A step-by-step guide to rebuilding the whole setup on a new computer sits in the vault. The same weekly job regenerates its lists (installed tools, scheduled jobs, skills, hooks) from the live machine, so those lists always match the machine as it is now. For whole-machine restores the maintainer also runs Apple's Time Machine to a network drive at home.
- **The restore drill.** Once a month a job picks a small note that hasn't changed since the last backup, fetches it fresh from both GitHub and Google Drive into a private scratch folder, and compares it byte for byte with the live file. A match is logged as a quiet pass; a mismatch, a missing file or an expired login raises an alert. The drill never writes to the vault or to either backup. It checks a sample, not every file, so it proves the restore path works rather than that every file is covered.
- **Checks that look for success, not activity.** Each morning a health check looks for an actual success line from each backup within the last three days (so a hotel-WiFi blip doesn't cry wolf), and reports any file the version history has been quietly skipping. Separately, the backups ping an outside monitoring service ([healthchecks.io](https://healthchecks.io)) each time they run. If the laptop is dead or the job never starts, the silence itself raises the alarm, from a service that doesn't depend on the machine that failed.

## What this does *not* do

It doesn't decide what to restore. When something goes wrong, you and the AI look at the history together and choose what to take back; nothing rolls itself back automatically. It doesn't make the AI careful, either. The point is that a careless change becomes something you can recover from, not that careless changes stop happening. And it isn't an archive of everything: very large files are kept out of the version history (they're covered by the nightly Drive copy instead), and the vault backups stay private, because a vault holds things you'd never publish.

## Why this works

Most backup setups fail quietly: the job runs every night and reports success while leaving out the one file that mattered, or the login behind it expired months ago. Layers that fail for different reasons (a local history, a nightly copy with a delay built in, a separate copy of the machinery) make it unlikely that one fault takes out everything, and the monthly drill turns "we have backups" from an assumption into something checked. That is also what makes it reasonable to hand the AI real write access: when its changes can be seen and reversed, a mistake is an inconvenience, not a loss.

## Note

This is a pattern, not a fixed implementation. Which cloud holds the second copy, how often the snapshots run, whether you add a whole-machine backup, how far you take the drill: all yours, and the layers are independent, so start with the version history alone and add the rest as you rely on the system more. The durable idea is: *keep a running history so changes can be undone, keep copies that don't fail together, and prove the backups work by restoring from them on a schedule.* Paste this to your AI and build the version that fits how you work.

---

*Want the actual method? [The reference](../reference/an-undo-button-for-your-vault.md) lays out the maintainer's real version — the layers and their schedules, the size guard, the restore drill, the health checks, the failure modes — cleaned of personal specifics. A starting point to adapt, not a drop-in.*
