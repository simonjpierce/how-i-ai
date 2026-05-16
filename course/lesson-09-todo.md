# Lesson 9 — `/todo`

One command that routes a task to whatever task manager you actually use, so you stop dropping things between Claude and your real to-do list.

The lesson reads on its own. A short screencast — me adding three different tasks to Things 3 from inside a Claude session — will pair with it when recorded.

## What it does

Adds a task to your task manager. Reads the choice you made during `/onboard` (Things 3, Todoist, Apple Reminders, vault `TODO.md`) and routes appropriately. Task notes can include clickable links back into your vault, so "open the relevant project note" is one tap from the task.

## When to use it

- Anywhere in a session where you notice work that needs to land in your real task list, not in chat.
- *"Remind me to email X tomorrow."*
- *"Add to my today list: review the funder draft."*
- After a `/document` run, when there are next-step items worth capturing.

## Try it

```
/todo
```

Claude asks for the task content (or you can paste it inline: `/todo Email X about Y by Friday`). It writes the task with vault context as a note, and confirms where it landed.

## A note on task managers we don't natively route to

Asana, Linear, Notion, and others aren't natively routed yet. The fallback is the vault `TODO.md` — useful but not your real list. Ask Claude to add a routing branch for your tool if you want; it's a small skill edit.

## What's next

[Lesson 10 — `/update`](./lesson-10-update.md). After a substantial piece of work, sweep the related project notes and process docs so they reflect what just happened.
