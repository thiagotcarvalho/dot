---
type: reference
tags: [workflow, tooling]
repo: none
created: 2026-08-12
---
Auto-loaded every session. This is the index of the [brain](../README.md): **rules** (authored standards, apply them) and **memory** (learned facts). One line per entry; the linked file holds the detail.

## Rules
> Authored standards, apply to the relevant work. This list mirrors the stage order of the rule table in brain/README.md, which is authoritative.

- [Explicit go for outward actions](../rules/explicit-go-for-outward-actions.md) — "draft" means draft; posts, commits, deploys, production writes, and shared settings each need their own explicit go
- [Vault is not a repo](../rules/vault-is-not-a-repo.md) — personal vault, untracked; never referenced from any repo
- [Vault file layout](../rules/vault-file-layout.md) — keep images and HTML pages in `diagram/` and code files in `scripts/`; back up before a destructive change, because the vault has no version control
- [Skills are tools](../rules/skills-are-tools.md) — install skills by copy, trimmed and checked; a skill must not collide with a rule
- [Work tracking](../rules/work-tracking.md) — the task queue in arms/task-queue is the arms; each task links its context, usually a scope; it replaces per-scope backlog.md
- [State the problem](../rules/state-the-problem.md) — problem + success criteria before the solution
- [Current state wins](../rules/current-state-wins.md) — verify remembered facts against the repo and the running system; correct stale notes in place
- [KISS](../rules/keep-it-simple-stupid.md) — simplest design that works
- [YAGNI](../rules/you-arent-gonna-need-it.md) — build only what the current requirement demands
- [DRY](../rules/dont-repeat-yourself.md) — one authoritative representation per piece of knowledge
- [SOLID](../rules/solid-principles.md) — one reason to change; extend by data or new code, not edits; one contract test per port; a port only where a fake or a second adapter exists
- [Guarded writes](../rules/guarded-writes.md) — dry run by default; write only a proven change to exactly one target; protected text stays
- [Ponytail baseline](../rules/ponytail-baseline.md) — write code through the ponytail skill; simplicity always wins
- [Code style](../rules/code-style.md) — Google pyguide; self-documenting names, one case per test
- [Flat is better than nested](../rules/flat-is-better-than-nested.md) — max 1-2 levels of nesting per function; refactor deeper code
- [Comments and docstrings](../rules/comments-and-docstrings.md) — Google pyguide §3.8, minimal, why not what; plus the nine Stack Overflow rules
- [Writing style](../rules/writing-style.md) — fewer em-dashes, plain tone, no hard-wrapped prose, TOC on docs, let diagrams carry the explanation
- [Simplified Technical English](../rules/simplified-technical-english.md) — ASD-STE100 for all prose: short sentences, active voice, one meaning per word
- [Note properties](../rules/note-properties.md) — every hand-authored brain/spine note carries a controlled YAML properties block
- [Prove it where it runs](../rules/prove-it-where-it-runs.md) — a check proves only what it ran, on the host where it ran; a manual run does not prove a schedule
- [Review before commit](../rules/review-before-commit.md) — adversarial review by another agent gates every commit
- [PR reviews to terminal](../rules/pr-reviews-to-terminal.md) — deliver reviews in chat, not a saved file
- [Git conventions](../rules/git-conventions.md) — never commit/push; no AI attribution; ≤50-char subjects; no commit body

## Memory
> Learned facts

<!-- Add one line for each memory note in this folder: - [Title](note.md) — what the note holds -->
