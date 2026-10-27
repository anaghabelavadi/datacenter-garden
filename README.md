# 🌱 Data Center Digital Garden

An open, growing map of one data center: what it is made of, what it affects, and how those effects feed back on each other. Built as a digital garden with [Quartz](https://quartz.jzhao.xyz/), and our entry to [Project MACC 2027](https://mit-orcd.github.io/macc2027/).

**Live site:** https://anaghabelavadi.github.io/datacenter-garden (after the first deploy)

## Contribute in 10 minutes

You don't need to install anything. Edit any file under `content/` on GitHub, start a pull request, and fill in the checklist. Full guide: [`content/project/start-here.md`](content/project/start-here.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md).

Using an AI tool? Read [`AGENTS.md`](AGENTS.md) first.

## What's in here

| Path | What it is |
| --- | --- |
| `content/` | All garden notes (markdown). This is where almost all work happens. |
| `content/static/explorer.htm` | Clickable building explorer (plain HTML + SVG, no build step) |
| `content/templates/note-template.md` | Copy this to start a new note |
| `quartz.config.yaml` | Site settings (title, base URL, plugins) |
| `.github/workflows/deploy.yml` | Builds and publishes the site on every push to `main` |
| `quartz/` | The Quartz engine. Don't edit unless you mean to. |

## Run it locally (optional)

Needs Node.js 22+.

```bash
npm ci
npx quartz plugin install --from-config
npx quartz build --serve   # http://localhost:8080
```

## One-time setup for the repo owner

1. Create an empty GitHub repo named `datacenter-garden` (no README or license).
2. From this folder: `git remote set-url origin https://github.com/<you>/datacenter-garden.git` then `git push -u origin main`.
3. On GitHub: **Settings → Pages → Source: GitHub Actions**.
4. **Settings → Collaborators** (or an org team): add teammates.
5. **Settings → Branches**: protect `main` so changes come through reviewed pull requests.
6. If the repo lives somewhere other than `anaghabelavadi/datacenter-garden`, update `baseUrl` and the footer link in `quartz.config.yaml`.

## License

Code: MIT (inherited from Quartz, see `LICENSE.txt`). Content license: to be decided by the team (open source is required for MACC prizes).
