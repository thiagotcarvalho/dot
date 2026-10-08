---
type: rule
tags: [workflow, git, jira, deployment]
repo: none
created: 2026-10-01
---
# Explicit Go for Outward Actions

An outward action is an action that other people can see, or an action that changes a shared system. Git staging and commits also count, because the user owns the history of each repo. Only the user decides when an outward action happens. An agent prepares the action, asks for an explicit go, and waits.

## The Rules

- **Draft means draft.** Prepare the comment, the message, or the change in chat or in the [spine](../../spine/README.md). Keep a review or a review comment in chat, per [pr-reviews-to-terminal](pr-reviews-to-terminal.md). Then stop.
- **A go is a direct instruction.** "Post it", "send it", and "go ahead" are a go. Agreement with the draft is not a go.
- **A content requirement is not a go.** "I want to post actual results" tells you what the draft must contain. It does not authorize the post.
- **One go covers one action.** Ask for the go when the action is ready. Name the action and its target. A go for one comment does not cover the next comment.
- **A clean review is not a go.** A green gate, a finished task, and a merged dependency are not a go either. See [review-before-commit](review-before-commit.md).
- **Check before a destructive or shared change.** Put the result of the pre-check in the request for the go.
- **Read back after the change.** Read the result from the system. Report it to the user.

## Which Actions Are Outward

| Class | Examples |
| --- | --- |
| Publish | A Jira comment or edit, a Confluence page, a Slack message, a GitHub issue, a pull request, a review comment |
| Git | `git add`, `git commit`, `git push`, a merge, a tag. [git-conventions](git-conventions.md) holds the git detail. |
| Deploy | A release to a shared host, a timer or a schedule that you enable, a restart of a shared service |
| Shared data | A write to a production database, a migration |
| Shared settings | Branch protection, rulesets, repository settings, secrets, CI configuration |
| Destructive | A branch deletion, a force push, a rewrite of shared history |

## How to Apply

Present the draft and the pre-check. Ask for the go. Then wait for the answer.

Use these pre-checks:

- Before a branch deletion, read `git branch -vv` and the default branch. Read the upstream of the branch and its unmerged and unpushed commits.
- Before a production write or a migration, count the rows that the write changes, with aggregates only. Confirm that the target table exists.

The tools that we build follow the same boundary. A report-only tool proposes a change, and a person approves it. See [guarded-writes](guarded-writes.md).

## Why

The user wanted this rule because an agent posted a draft to a live Jira ticket without a go on 2026-08-12.

## Related

[git-conventions](git-conventions.md) · [review-before-commit](review-before-commit.md) · [pr-reviews-to-terminal](pr-reviews-to-terminal.md) · [guarded-writes](guarded-writes.md)
