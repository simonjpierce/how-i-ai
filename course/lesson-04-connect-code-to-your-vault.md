# Lesson 4 — Connect Code to your vault

Two clicks. The shortest lesson in the course.

The lesson is two clicks; the text below covers them. A short screencast will pair with it when recorded.

## What "connecting" means

Claude Code is sandboxed by default — it can only read and edit files inside one folder at a time. That folder is the **project root**. You tell Claude Code which folder to use by clicking **Select folder** in the Code tab and choosing your Obsidian vault.

Once you've done that, Claude can read every note in your vault, edit them, and create new ones. The vault is now its working directory.

## Steps

1. Open Claude Desktop. Click the **Code** tab.
2. Click **Select folder**.
3. Navigate to your Obsidian vault folder (the one you created in lesson 3) and select it.

That's the whole lesson.

## What you can do now (don't, yet)

Type a prompt at the Code tab — *"list the files in this folder"* or *"create a note called Test.md with 'hello world' in it"*. Claude can do both. You'll see Obsidian's file list update when it writes. You're now wired up.

We don't actually want you doing real work yet, though. The next lesson (`CLAUDE.md`) is the one that makes Claude useful — without it, Claude is generic and you'll spend every session re-explaining who you are. **Don't ramp up usage until lesson 5 is done.**

## A safety word about permissions

Claude Code asks for permission before each action by default. That gets tedious fast, and the system can't deliver on its promise of "get out of your way" if it's prompting you every few seconds. There's an **Auto mode** that auto-accepts everything — file edits and shell commands — covered briefly in lesson 5 when we set things up properly. Until then, the default permission prompts are fine; they're a useful introduction to what Claude is about to do.

## What's next

[Lesson 5 — Your `CLAUDE.md`](./lesson-05-your-claude-md.md). The single highest-leverage setup step. Claude will interview you for ~15 minutes and write your `CLAUDE.md` files for you.
