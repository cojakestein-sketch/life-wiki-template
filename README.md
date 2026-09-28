# Life Wiki template

A plain-Markdown context layer that several AI agents share. Claude Code, Codex, Gemini
CLI and whatever comes next all read the same operating contract and the same sourced
pages about you, instead of each keeping its own half-remembered chat memory.

This is the empty structure of the system I run my own agents on. It holds no
personal content.

## How it works

```
CLAUDE.md ─┐
GEMINI.md ─┼─▶ AGENTS.md ─▶ me/profile · me/preferences · me/now ─▶ index.md ─▶ deeper pages
(Codex) ───┘   one contract   loaded every session                  the map      only when needed
```

- **One contract.** [AGENTS.md](AGENTS.md) says where things go, how to save context
  and what agents may not do. Tool-specific files only point to it.
- **Sources, then synthesis.** What you actually said goes in `raw/`, dated and
  immutable. Maintained pages summarize it and cite it. Agents label their own
  inferences instead of promoting them into your beliefs.
- **Privacy that git enforces.** Every maintained page declares a privacy level.
  `local-only` files must be matched by `.gitignore`, and
  [scripts/check_privacy.py](scripts/check_privacy.py) fails the commit if one is
  tracked, uncovered or holds something that looks like a secret.
- **Live systems win.** A cached page is a dated observation. For calendars, course
  sites or accounts, agents query the live system.

## Layout

| Path | Holds |
|---|---|
| `AGENTS.md` | The operating contract |
| `me/` | Profile, preferences, now; deeper personal topics |
| `areas/` | One folder per job, class or project |
| `raw/` | Original sources with provenance ([rules](raw/RULES.md)) |
| `ops/` | The single todo list, reports, plans, runbooks, inbox |
| `index.md`, `log.md` | The map and the change log |

## Quick start

1. Click **Use this template** and create a **private** repository. `repo-safe` means
   safe for your private remote, not safe to publish.
2. Clone it and turn on the pre-commit check:
   ```bash
   git config core.hooksPath .githooks
   ```
3. Start a session with your agent and ask it to interview you. Save the transcript
   under `raw/self/`, then have the agent fill in `me/` with citations to it.
4. Add areas as real work arrives. Keep `ops/todos.md` as the only task list.

The privacy check also runs in GitHub Actions on every push. Run it by hand with
`python3 scripts/check_privacy.py`, and its tests with `python3 -m unittest discover tests`.
It uses only the Python standard library.

## Privacy levels

| Level | Meaning |
|---|---|
| `repo-safe` | Fine for your private remote |
| `sensitive` | Private remote, handled with care: money, health, identity, other people |
| `local-only` | Never leaves the machine; must be covered by `.gitignore` |
| `never-store` | Discussed live, never written down |

---

Built by [Jake Stein](https://cojakestein-sketch.github.io). MIT licensed.
