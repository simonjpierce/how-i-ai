# Lesson 3 — Install the stack

Two apps. Both free to download; Claude Code needs a paid Claude plan to actually use.

The lesson below stands alone — every click is in the text. A short screencast of the install (both apps end-to-end) will pair with the lesson when recorded.

## What you need

- **A Mac.** macOS Ventura 13.0 or later. *(Windows and Linux support is on the roadmap. If you're on either, ping Simon — a manual install path exists, but it's not what this lesson covers.)*
- **A paid Claude plan.** Pro ($20/month) is enough. **MMF science team:** Simon should have added you to the MMF org plan before sending you this course — if you sign in and the Code tab still says "upgrade," DM him your GitHub username + the email you signed in with. **Outside MMF:** Pro is the right plan; the higher tiers (Max, Team, Enterprise) aren't necessary.

## Step 1 — Claude Desktop

1. Go to [claude.com/download](https://claude.com/download) and run the installer.
2. Drag Claude to your Applications folder.
3. Launch Claude. Sign in with your Anthropic account.
4. You'll see three tabs at the top: **Chat**, **Cowork**, **Code**. Click **Code**.

If Code prompts you to upgrade, your account isn't on a paid plan yet — check the plan note above.

### Why "Code" if you're not coding?

The name is bad. **Code** is the only tab that can read and edit files on your Mac, regardless of whether those files are code, prose, transcripts, spreadsheets, or anything else. The other tabs:

- **Chat** is the closest thing to claude.ai — handles attachments and `@filename` references, but doesn't have full file-system access.
- **Cowork** runs autonomous background agents in a cloud VM. Useful for chunky, well-scoped tasks you want to delegate-and-review. We come back to this in an advanced lesson; you can ignore it for now.

For this course you live in **Code**.

## Step 2 — Obsidian

1. Go to [obsidian.md](https://obsidian.md) and download the Mac version.
2. Drag Obsidian to your Applications folder.
3. Launch it. On first run it asks you to either open an existing vault or create a new one. **Create a new vault.** Call it whatever you want — your name, "Notes", "Vault", whatever. Put it somewhere you'll find it (Documents folder is fine).

That's it. The vault is just a folder of `.md` files; you can move it later if you want.

## Sanity check

- **Claude Desktop:** click into the Code tab. Type `/` and pause. You should see a list of slash commands (`/help`, `/clear`, `/model`, …). If you do, Code is working.
- **Obsidian:** open your new vault. Create a note ("Test"). Type "hello". Save. The note is now a `hello.md` file in your vault folder. Done.

Both apps run quietly in the background; you'll be in them most days.

## What's next

[Lesson 4 — Connect Code to your vault](./lesson-04-connect-code-to-your-vault.md). The two apps don't know about each other yet; that's the next ~2 clicks.

## If something breaks

- **Desktop app won't launch** ("unidentified developer"): System Settings → Privacy & Security → "Open Anyway".
- **Code tab shows 403 or asks you to upgrade**: your account isn't on a paid plan yet. Sign in to claude.com in a browser, confirm the plan, then restart Claude Desktop.
- **Sign-in loop**: make sure your browser isn't blocking redirects from `auth.anthropic.com`.
- **Anything else**: message Simon on Slack with the exact error text (screenshot is fine).
