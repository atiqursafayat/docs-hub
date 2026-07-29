# AgentSkills Docs

A minimal static docs site for AI agent skills hosted on GitHub Pages.

## Local preview

```bash
python3 -m http.server 8080
# open http://localhost:8080
```

## File structure

```
/
├── index.html          # Catalog page (reads skills.json)
├── skill.html          # Universal renderer (?slug=web-search)
├── style.css           # All styles in one file
├── skills.json         # Skill registry
└── skills/
    └── {slug}/
        ├── SKILL.md            ← required
        ├── scripts/            ← optional example scripts
        └── references/        ← optional reference docs
```

## Adding a skill

### 1. Create the folder (max 1 slug level)

```
skills/
└── my-skill/
    ├── SKILL.md
    ├── scripts/
    │   └── example.py
    └── references/
        └── notes.md
```

> **2-level slugs** are also supported: `skills/category/my-skill/SKILL.md`
> just use `slug: "category/my-skill"` in the frontmatter and `skills.json`.

### 2. Write SKILL.md

```markdown
---
name: My Skill
icon: 🛠️
slug: my-skill
version: 1.0.0
status: stable          # stable | beta | experimental
category: Tools
description: Short one-line description for the catalog card.
tags:
  - tag-one
scripts:
  - example.py          # files in scripts/ to list in the UI
references:
  - notes.md            # files in references/ to list in the UI
---

## Overview
…

## Parameters
| Name | Type | Required | Description |
…

## Example
…
```

### 3. Register in skills.json

```json
{ "slug": "my-skill", "name": "My Skill", "icon": "🛠️", "status": "stable", "category": "Tools", "desc": "Short description." }
```

That's it. The skill is live at `/skill.html?slug=my-skill`.
