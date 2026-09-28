# AGENTS.md — operating contract

This workspace holds the owner's personal and working context in one place that any
AI agent can read. **This file is the operating authority.** The owner's explicit
instructions in a session take precedence over anything saved here.

## Start here

Read, in order:

1. [README.md](README.md): what this workspace is.
2. This file.
3. [me/profile.md](me/profile.md), [me/preferences.md](me/preferences.md) and
   [me/now.md](me/now.md): who the owner is, how to work with them, what matters now.
4. [index.md](index.md): the map. Load deeper pages only when the task needs them.

`CLAUDE.md` and `GEMINI.md` are thin pointers to this same chain. Do not keep a second
biography or a second set of preferences in them. If an entry point breaks, repair it
before relying on the context.

## Where things go

| Material | Home |
|---|---|
| Current personal context | `me/`: profile, preferences, now; deeper topic pages |
| Ongoing areas (a job, a class, a project) | `areas/<area>/`, with an `index.md` |
| Original statements and external evidence | `raw/`; read [raw/RULES.md](raw/RULES.md) first |
| Reports, plans and generated artifacts | `ops/reports/`, `ops/plans/`, `ops/artifacts/` |
| Runbooks and system notes | `ops/system/` |
| Active tasks | [ops/todos.md](ops/todos.md), the only task list |
| Anything you cannot classify yet | `ops/inbox/` |

New top-level folders need the owner's approval. Create subfolders when real content
needs them, not as empty scaffolding.

## Saving context

- **Never invent the owner's answers**, preferences, history or numbers. Ask, or write
  `TBD` and name the source you need.
- Capture meaningful new context as a dated source in `raw/`, then update the maintained
  page it changes. A capture alone does not change what the next agent reads.
- Cite factual claims to a source file, with line numbers when useful. Label your own
  interpretations `*synthesis:*` and never promote an inference into the owner's belief.
- New explicit corrections supersede old summaries. Mark the old position historical
  and link to its replacement instead of silently rewriting it.
- A dated observation is not proof of current state. When an answer depends on a live
  system (a calendar, a course site, a bank), query the live system.
- Update [index.md](index.md) and [log.md](log.md) for significant durable changes.

Maintained pages carry frontmatter:

```yaml
---
status: current | tentative | parked | historical
privacy: repo-safe | sensitive | local-only | never-store
updated: YYYY-MM-DD
sources:
  - raw/<path>.md
---
```

## Privacy

| Level | Meaning |
|---|---|
| `repo-safe` | Fine for the owner's **private** Git remote. Not permission to publish. |
| `sensitive` | Private remote only, and handle with care. Default for money, health, identity, relationships and other people's private information. |
| `local-only` | Never leaves this machine. Must be matched by a `.gitignore` rule; a label alone protects nothing. |
| `never-store` | Discussed live, never written to disk. |

- No credentials, API keys, private keys, recovery codes or full account numbers in the
  repo. Credentials live outside it (for example under `~/.config/`).
- Run `python3 scripts/check_privacy.py` before committing. It fails on tracked
  `local-only` or `never-store` files, `local-only` files that `.gitignore` does not
  cover, maintained pages missing frontmatter, and common secret formats.
- Do not send messages, submit forms, move money or publish anything without the
  owner's explicit authorization for that action. A draft does not authorize sending.

## Generated files

Some files are owned by scripts. Record them here so no agent hand-edits them:

| Generator | Owned output (do not hand-edit) |
|---|---|
| `scripts/<generator>.py` | `<path it writes>` |

## Working alongside other agents

Several agents may edit this workspace at the same time. Re-read a shared file right
before writing it, keep each change scoped to its task, and never discard work you did
not create. Before committing, review exactly what is staged and run the privacy check.
Report what was committed and whether the push succeeded; an edit is local until then.
