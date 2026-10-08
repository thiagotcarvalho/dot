---
type: rule
tags: [workflow, tooling]
repo: none
created: 2026-10-02
---
# Vault File Layout and No Versioning

The vault keeps images and HTML pages in `diagram/` folders and code files in `scripts/` folders. The vault is not a repo ([vault-is-not-a-repo](vault-is-not-a-repo.md)), so it has no version control.

## The Rules

- **Put each image and HTML page in a `diagram/` folder.** An image (`.png`, `.svg`, `.jpg`) or an HTML page (`.html`) goes in the `diagram/` folder of its scope, for example `<scope>/diagram/`. A loose image or HTML page in an `archive/` folder goes in `archive/diagram/`.
- **Put each code file in a `scripts/` folder.** A code file goes in the `scripts/` folder of its scope, for example `<scope>/scripts/`. [vault-is-not-a-repo](vault-is-not-a-repo.md) limits which code files the vault holds.
- **Expect no version history.** The vault has no version control, such as git. Treat a deletion, a move, or a rewrite as final. The Obsidian File recovery plugin keeps short-term snapshots of notes. Do not rely on it for a restore.
- **Back up before a destructive change.** Before you delete a file or rewrite a large part of it, copy it outside the vault. Use a folder such as `~/.cache/<task-id>/`. Never copy a file that holds a credential or sensitive data. Record the backup path in the queue task.

## How to Apply

Create a `diagram/` or `scripts/` folder when its scope gets its first image, HTML page, or code file. A scope moves as one unit, with its `diagram/` and `scripts/` folders. When you move a file, update every link and path to it. A log of past output in a task keeps the old path.

Notes keep their own history, because the vault has no version control. A plan gets dated updates, and a discovery note gets dated notices. See [the spine README](../../spine/README.md).

## Why

The user wanted this rule because the spine mixed images and code files with notes, and the vault has no version control, on 2026-10-02. Later that day, the user put all HTML pages in `diagram/` folders, also the archived pages.

## Related

[vault-is-not-a-repo](vault-is-not-a-repo.md) · [note-properties](note-properties.md) · [current-state-wins](current-state-wins.md)
