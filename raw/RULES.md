# Source archive rules

`raw/` preserves what the owner or an outside source actually said, supplied or showed.
Current interpretation lives in `me/`, `areas/` or `ops/`. The operating authority is
[AGENTS.md](../AGENTS.md).

## What goes here

- Interviews, voice-note transcripts, original instructions, official documents,
  exports and faithful summaries of external sources, each with provenance.
- Not agent recommendations, strategy or polished reports. Those go in maintained pages.
- Dated filenames: `<slug>-YYYY-MM-DD.md`. Keep Markdown line-citable where practical.
- The owner's committed statements are immutable. Record a correction as a new dated
  source and update the maintained page; never rewrite an old answer silently.

## Routing

| Incoming source | Archive location | Maintained understanding |
|---|---|---|
| The owner's context, interviews, preferences | `raw/self/<domain>/` | `me/` |
| Useful external research | `raw/external/<domain>/` | The relevant area or report |
| Original files for an area | `areas/<area>/raw/` | That area's pages |

Create a domain folder only when there is content for it.

## Provenance

```yaml
---
source_type: interview | voice-note | user-brief | official-doc | web-capture | export | research-note
captured: YYYY-MM-DD
captured_by: owner | <agent name>
verbatim: true | false
privacy: repo-safe | sensitive | local-only | never-store
---
```

A summary is `verbatim: false`. Anything under a `local/` folder here is ignored by Git;
use it for sources that must never leave the machine.
