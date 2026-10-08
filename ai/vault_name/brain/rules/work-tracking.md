---
type: rule
tags: [workflow, tooling]
repo: none
created: 2026-09-10
---
# Work Tracking

Every unit of work is tracked in the task queue. The queue is the durable, cross-session record of what work exists, what its status is, and what proves it done. It replaces the per-scope `backlog.md`. Do not use conversation history or model memory as the work ledger.

The task queue is the arms. The spine holds the context of the work in scopes: the problem, the plan, and the open questions. The arms do the work: each task holds the next action, the status, and the evidence.

The queue lives in `arms/task-queue/`. Each task is one Markdown file. The folder is the status: `Now`, `Next`, `Waiting`, or `Done`. This rule states the standard.

## The Rules

- **One task per unit of work.** Create the task before you start the work. A unit of work is one shippable effort, usually one ticket or one pull request. Put the granular steps in the task as a checklist.
- **Each task links its context.** A scope is one spine directory for one effort: a ticket directory such as `<ticket-key>/`, a workstream directory such as `<workstream>/`, or `misc/`. Link the notes that the task depends on, as wikilinks in the task. These are usually its discovery, its plan, and the scope `open-questions.md`. A per-effort note, a runbook, or another scope note can take their place. A task without a scope links a rule or a memory note, or names a repo path, until the scope exists.
- **The folder is the status.** `Now` is active work. `Next` is accepted work behind active work. `Waiting` needs a named external event or input. `Done` has every deliverable handed off and verified.
- **Status stays in the queue.** Do not copy a task status into a scope note. The backlinks of a scope note list its tasks. Name a task in a scope note by its ID, for example `PROJ-72`. Do not link the task file. A link breaks when the task file moves to another folder or changes its name.
- **Update the task at four moments.** Move it to `Now` when you start. Tick a deliverable when you finish it. Move the task to its new folder when the status changes. Reconcile every checkbox against the evidence before you report status.
- **A green check is not a done task.** A passing test, a merge, or an agent message proves only the result it covers. Move a task to `Done` only when every deliverable and completion condition is satisfied. See [prove-it-where-it-runs](prove-it-where-it-runs.md).
- **The harness todo tool is for one session.** The harness `todo` tool is the in-session step list for one work burst. The queue is the durable record across sessions. The step list feeds the queue; it does not replace it.
- **Unknowns stay in `open-questions.md`.** A question is not a task. A `Waiting` task references the scope `open-questions.md` and names the blocking question. The question stays in `open-questions.md` with its answer.

## How to Apply

When you accept work, create or update its task first. Link the task to its context and to the repo pull requests. Record the Jira key in the task when one exists. Keep the granular checklist in the task, not in a separate file.

The work moves between the arms and the spine:

1. Before the work, read the notes that the task links.
2. During the work, record the evidence and the status in the task.
3. Put each lasting fact in its home. The problem goes in the discovery. A design change is a dated update to the plan. An unknown goes in `open-questions.md`. A learned fact goes in brain memory.

The queue does not replace the Discovery and Plan cadence. The queue tracks status and deliverables. The cadence docs hold the problem and the solution.

## Sensitive Data and Vault Boundaries

A task keeps sanitized output only. Never write a secret or a raw record of private data into a task.

The queue lives in the vault at `arms/task-queue/`. A task points out to Jira and to pull requests. A repo never references the queue back. See [vault-is-not-a-repo](vault-is-not-a-repo.md).

## Why

The user wanted this rule on 2026-09-10 because the queue survives context compaction and agent handoffs, and the harness `todo` tool does not.

## Related

[vault-is-not-a-repo](vault-is-not-a-repo.md) · [state-the-problem](state-the-problem.md) · [git-conventions](git-conventions.md) · [prove-it-where-it-runs](prove-it-where-it-runs.md) · [current-state-wins](current-state-wins.md)
