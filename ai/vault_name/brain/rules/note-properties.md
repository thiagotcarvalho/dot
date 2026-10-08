---
type: rule
tags: [tooling, workflow]
repo: none
created: 2026-09-09
---
# Note Properties

Every hand-authored note in `brain/rules/` and `spine/` carries an Obsidian properties block. The block is YAML frontmatter at the top of the file, between `---` fences. Properties tag a note and connect it to related notes.

This rule covers `brain/rules/`, `spine/` notes, and the vault root files. It does not cover these places:

- `brain/memory/`, because the memory subsystem manages that frontmatter.
- `brain/skills/`, because it holds external skill stores, which the vault index excludes.
- `arms/task-queue/`, because a task file uses its own frontmatter.

## The Rule

Each note starts with this block:

```yaml
---
type: <one type>
tags: [<zero or more facets>]
repo: <one repo>
created: <YYYY-MM-DD>
status: <one status>   # spine notes only
---
```

Key values are controlled. Use only the values below.

| Key | Applies to | Allowed values |
|---|---|---|
| `type` | all | `rule`, `memory`, `discovery`, `plan`, `reference`, `scratch`; `recap` only on a note from before 2026-10-02 |
| `tags` | all | facets from the vocabulary below; lowercase, kebab-case |
| `repo` | all | a repo name from [the repo table](../../AGENTS.md#repos-in-the-workspace), or `none` |
| `created` | all | the file creation date, `YYYY-MM-DD` |
| `status` | spine only | `active`, `archived`, `superseded` |

Rules for values:
- `type` follows the note role. A ticket note is `discovery` or `plan`. A standing note is `rule`, `memory`, or `reference`. A personal note is `scratch` or `reference`. The cadence has no recap phase, so `recap` stays only on the older recap notes.
- `repo` names the code repository the note is about, or `none` for a note that spans repos or belongs to no repo. The repo table in `AGENTS.md` is the only list of repo names. Add a new repo to that table first. Its name is then a valid value.
- `status` marks the spine note lifecycle. A note under an `archive/` directory is `archived`. Set `superseded` by hand when a newer note replaces this one.
- `tags` are topic facets, not a copy of `type` or `repo`. Add a facet only when the note is really about it.

## Tag Vocabulary

Pick tags from this flat list. Add a new tag only for a whole topic that the list does not cover, in the same lowercase kebab-case style.

- Technology: `sql`, `sql-server`, `sqlalchemy`, `python`, `docker`, `ci`
- Process: `git`, `decision`, `postmortem`, `deployment`, `runbook`, `testing`, `jira`, `architecture`, `workflow`, `tooling`
- Personal: `cli`, `neovim`, `dotfiles`, `glossary`, `onboarding`

## How to Apply

A new note gets the block as its first content, before the title heading. Derive `type`, `repo`, and `status` from the note role and its path. Set `created` to the current date. Choose the tags after you write the note, from the vocabulary.

Do not duplicate the note's links into a property. The body links already connect the notes. Properties add the tag facets and the typed fields.

## Why

The user wanted this rule because 118 notes had no metadata on 2026-09-09, so no tag could group related notes across repos.

## Related

[vault-is-not-a-repo](vault-is-not-a-repo.md) · [writing-style](writing-style.md)
