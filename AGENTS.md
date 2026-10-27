# Instructions for AI agents working in this repo

This repo is a Quartz digital garden about the impacts and system dynamics of data centers. Humans and agents both contribute. These rules keep the garden trustworthy and make our human–agent collaboration visible for the MACC 2027 write-up.

## Rules

1. **Never invent numbers, sources, quotes or links.** Every quantitative claim needs a source you actually opened. If you can't find one, write the claim as an open question.
2. **Agent-drafted notes are always `maturity: seedling`.** Set `drafted_by: "agent: <tool/model>"` and leave `verified_by` empty. Never set `budding` or `evergreen`, and never fill `verified_by`.
3. **Start new notes from `content/templates/note-template.md`** and put them in the right folder (`components/`, `branches/`, `loops/`, `project/`).
4. **Link, don't duplicate.** Use `[[folder/note]]` wikilinks. Inside markdown tables, escape the alias pipe: `[[folder/note\|Label]]`.
5. **Loops use Mermaid `flowchart LR`** with `+` / `−` edge labels, and each arrow needs evidence before a person can promote the note.
6. **Small pull requests.** One note or one feature per PR, with a summary of what you did and what a person should check.
7. **Log meaningful work** as a row in `content/project/human-agent-log.md`.
8. **Don't edit `quartz/`** (the engine) unless the task is explicitly about the site's code.

## Checks before you finish

```bash
npx quartz build   # must succeed with no broken-link errors
```
