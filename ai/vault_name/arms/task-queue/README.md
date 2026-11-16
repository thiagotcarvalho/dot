# Task Queue

This folder is the arms of the vault. It holds one Markdown file for each unit of work. [work-tracking](../../brain/rules/work-tracking.md) states the standard.

The queue is the source of truth for work across sessions, agents, terminals, pull requests, deployments, or external reviews. Conversation history and model memory provide context, not task status.

The folder that contains a task file is its status:

- `Now` is active work.
- `Next` is accepted work behind the active work.
- `Waiting` needs a named external event or input.
- `Done` has every deliverable handed off and verified.

Each task links its context, usually a scope in the [spine](../../spine/README.md). The task itself holds the next action, the status, and the evidence.

Each task has a stable ID. Record an external tracker ID only when it maps to one task.

Keep authoritative links and relevant sanitized terminal output in each task. Give each log entry a readable local timestamp. Put the most recent entry first. Never retain secrets, personal data, protected data, raw client values, or sensitive local paths.

When a deliverable is complete, check its box and record its completion evidence in the same update. Leave partial work unchecked, and state the remaining condition. Before you report status or change focus, reconcile every checkbox with the recorded evidence and the authoritative linked state.

Move a task only when its real status changes. A passing narrow check, commit, workflow, or agent report does not prove completion.

An optional `Task Queue.base` can provide table, card, and list views over the same Markdown task files. It must derive status from the containing folder.
