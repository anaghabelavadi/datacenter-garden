---
title: "Start here"
description: "How to add or edit a note in about 10 minutes, with or without Git."
---

Everything in the garden is a markdown file in the `content/` folder of the GitHub repo. Edit a file, open a pull request, and the site rebuilds once it is merged.

## The 10-minute way (no installs)

1. Open the repo on GitHub and go to the note you want to change, for example `content/components/cooling.md`.
2. Click the pencil icon, make your edit, and choose **Create a new branch and start a pull request**.
3. Fill in the short pull request checklist. Someone else reviews and merges.

To add a new note, copy `content/templates/note-template.md` into the right folder and rename it.

## The comfortable way (Obsidian)

1. Clone the repo and open the `content/` folder as an Obsidian vault.
2. Write with `[[wikilinks]]`; Quartz turns them into links and backlinks.
3. Commit and push to a branch, then open a pull request.

## The rules that keep the garden trustworthy

- **Every number has a source**, with year and region.
- **Maturity is honest.** New notes start as 🌱 `seedling`. Only a person who has checked the sources can move a note to 🌿 `budding` and add their name to `verified_by`.
- **Agents draft, people verify.** If an AI tool drafted a note, write `drafted_by: "agent: <tool>"`. See `AGENTS.md` in the repo.
- **Disagreement is content.** If sources conflict, list both under Open questions.

## Where things go

| Folder | What goes there |
| --- | --- |
| `content/components/` | Physical parts of the data center |
| `content/branches/` | The eight impact branches |
| `content/loops/` | Feedback loops, drawn with Mermaid |
| `content/project/` | Team pages: roadmap, contest, reading list, logs |
| `content/templates/` | Templates (not published) |
| `content/static/` | Images and the building explorer page |
