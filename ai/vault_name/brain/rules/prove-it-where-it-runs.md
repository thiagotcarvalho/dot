---
type: rule
tags: [testing, deployment, workflow]
repo: none
created: 2026-10-01
---
# Prove It Where It Runs

A check proves only what it ran, on the system where it ran. Before you claim that a change works, run a check on the host where the change runs. The check must use the same path as the change.

## The Rules

- **Name the claim and its target first.** Write down the behavior, the host, and the path. Then choose the check that can prove the claim false on that target.
- **A manual run does not prove a scheduled run.** Prove a schedule from the timer configuration and from the recorded start time of a scheduled run.
- **A local pass does not prove the production host.** A green gate on a Mac does not prove the VM.
- **A skipped test proves nothing.** Name each path that the gate skips. Run that path against the real dependency, for example a real SQL Server.
- **A tool's report does not prove a write.** Read the written value back from the system of record.
- **A replacement must give the same results as the path that it replaces.** Keep the old path until a parity check passes. Then delete the old path in one step.
- **State the gap when you cannot run a check on the target.** Say which check ran where, and what is still unproven. Keep the deliverable unchecked, per [work-tracking](work-tracking.md).

## How to Apply

Before you call a change verified, answer these questions:

1. Which behavior does the claim cover?
2. On which host, database, and scheduler does that behavior run?
3. Which check ran on that host, along that path?

If no check ran on the target, the change is not verified. Report it as built and checked locally. Name the remaining check.

The repo gate in [git-conventions](git-conventions.md) and the review in [review-before-commit](review-before-commit.md) come before a commit. They are necessary, but they do not prove a claim about the production host.

## Related

[work-tracking](work-tracking.md) · [review-before-commit](review-before-commit.md) · [current-state-wins](current-state-wins.md) · [guarded-writes](guarded-writes.md)
