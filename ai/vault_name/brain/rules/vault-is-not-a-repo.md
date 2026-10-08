---
type: rule
tags: [workflow, git]
repo: none
created: 2026-08-14
---
# The Vault Is Not a Repo

`~/Developer/vault_name` is the user's personal Obsidian vault. It has no `.git`, it is not a submodule, and it is not tracked by any repo under `~/Developer/`. It exists on the user's machine only, so nothing outside it may point at it.

## The Rule

- **Never reference the vault from inside a repo.** No vault paths (`~/Developer/vault_name/...`, `spine/...`, `brain/...`, `arms/...`) and no wikilinks to vault notes in code, comments, docstrings, tests, fixtures, README or `docs/` content, commit subjects, PR descriptions, GitHub issues, Jira, or Confluence. Every one of those is read by someone who does not have the vault, so the reference is a dead link on arrival and it exposes the user's private workspace layout.
- **The link direction is one-way.** Spine notes cite repo paths, commits, and PR URLs freely. Repo artifacts never cite back.
- **Do not make it a repo.** Never `git init` it, never add it to another repo's tree, never commit it. Its being untracked is the intent, not an oversight to fix.
- **Do not run git from inside it.** There is no repo there. Per [git-conventions](git-conventions.md), target a repo explicitly with `git -C <repo-path>`.
- **Keep code out of it.** The vault holds documents. Do not add scripts, patches, or generated files such as `__pycache__` or `.ruff_cache`. The user allows `.sql` files for now, and [vault-file-layout](vault-file-layout.md) says where they go. Later, they also move out of the vault. A change for review stays in its repo worktree, per [git-conventions](git-conventions.md).
- **Run vault code without cache folders.** Python and ruff write cache folders, such as `__pycache__` and `.ruff_cache`, into the vault. Set `PYTHONDONTWRITEBYTECODE=1` when you run Python on a vault file, for example `PYTHONDONTWRITEBYTECODE=1 uv run python <script>`. Add `--no-cache` when you run ruff on a vault file, for example `uvx ruff check --no-cache <file>`.
- **Carry the substance, not the citation.** When a repo artifact, PR body, or ticket needs what a spine note says, restate the reasoning inline. A spine note is agent work-product, not a source.

## How to Apply

Before writing anything that leaves the vault (a code change, a PR description, a commit subject, or a Jira comment), check it for vault paths and wikilinks and strip them. The usual leak is convenience: an agent that just wrote `plan.md` cites it in the PR body. Restate the two sentences that matter instead.

The reverse case is fine and expected: a spine doc links to `<repo>/src/...`, to a commit SHA, or to a PR, because those resolve for anyone.

## Why

The user wanted this rule on 2026-08-13 because the vault is personal, so a vault path in a repo is a dead link. On 2026-10-02, the user also limited code files to `.sql` and asked for the cache flags, because the vault is not a codebase.

## Related

[git-conventions](git-conventions.md) · [pr-reviews-to-terminal](pr-reviews-to-terminal.md) · [vault-file-layout](vault-file-layout.md)
