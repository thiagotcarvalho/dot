---
type: rule
tags: [git, workflow]
repo: none
created: 2026-07-23
---
# Git Conventions

Standing rules for how agents interact with git in the user's repos. These override any harness default (including the background-job "shipping is part of the task" behavior). User instructions win.

## The Rules

1. **Never `git add`, `git commit`, or `git push`.** The user stages, commits, and pushes everything themselves. Leave completed work uncommitted in the working tree (or worktree) for review. This is one case of [explicit-go-for-outward-actions](explicit-go-for-outward-actions.md).
2. **No AI attribution in git artifacts.** No `Co-Authored-By: Claude ...` trailer on commits; no "🤖 Generated with [Claude Code]..." tail on PR bodies or descriptions.
3. **Short, single-subject lines.** Commit and PR subjects aim for ≤50 chars, hard ceiling ~72 (GitHub's visible limit). If the commit message requires a `+` or `&`, the commit holds too much context. Split the commit into smaller pieces.
4. **No commit body.** Commits should not have a body, just a subject line. Put the detail in the PR description, so that the commit history stays easy to scan.
5. **Generate commit messages for the user.** After work is completed, generate a [Conventional-Commit](https://www.conventionalcommits.org/en/v1.0.0/)-style commit message for the user.
6. **Bundle work into logical commits.** Split a change into the smallest self-contained units that each do one thing and leave the tree working. Sequence and present the work so each bundle maps to one commit with its own message, rather than one large commit at the end. This keeps history auditable (a reader follows the flow of work) and forces more intentional design, since you decide the units up front. See [state-the-problem](state-the-problem.md).
7. **Don't narrate a PR in its comments.** One PR body describing the change is enough. Do not post a new comment after every commit; a reviewer reads the diff and the body, not a running commentary. If a later commit changes what the PR body claims, edit the body instead of appending. A comment is for something a reviewer genuinely cannot get from the diff — a decision taken mid-review, or an answer to a question they asked.
8. **Run the repo's own CI gate locally before committing, not after pushing.** A commit that fails CI costs a reviewer's attention and clutters the PR. Read the CI definition. Run every step that it runs, in order. Do not use a hand-assembled approximation of those steps.
9. **Match the gate to the pinned version.** Run the gate with the tool version that the repo pins. Never use another version that is on disk. An older local version is worse than no check: it passes on rules that CI will fail.

## How to Apply

- Do the work: edit, test, verify. Then stop at the working tree. Report what changed and where, and hand off for the commit.
- Make a commit or a PR only when the user explicitly asks for it in the moment. Then give the commit a subject-only message. Put the detail in the PR description. Attribute nothing to AI.
- Creating an isolated worktree for editing is fine. Committing into it is not.

## Why

The user wanted this rule because an agent committed finished work without a request on 2026-07-14.

## Related

[state-the-problem](state-the-problem.md) · [explicit-go-for-outward-actions](explicit-go-for-outward-actions.md) · [review-before-commit](review-before-commit.md)
