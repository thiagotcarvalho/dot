---
type: reference
tags: [architecture, tooling]
repo: none
created: 2026-08-06
status: active
---
# This Is the Spine

What agents *produce and interact with*: all agent work-product (plans, architecture, discovery, runbooks, analysis). The counterpart to the [brain](../brain/README.md), which is how agents behave. The task queue in [`arms/task-queue/`](../arms/task-queue/README.md) is the arms. The scopes hold the context, and the arms do the work.

All work-product lives under this `spine/` directory: one subdirectory per repo, plus shared `archive/` and `personal/` areas. Each effort lives in one scope: a ticket directory such as `spine/<repo>/PROJ-123/`, a workstream directory such as `spine/<repo>/<workstream>/`, or the `misc/` directory of a repo. The workspace entry point [`../AGENTS.md`](../AGENTS.md) lists the repos and states the rule against touching them.

`archive/` holds cross-repo or non-ticket material not tied to a single repo or ticket. `personal/` is the user's own workspace: do not touch it unless the user asks.

## Spine Layout

```text
vault_name/
├── AGENTS.md                 ← canonical entry point
├── brain/                    ← how agents behave (rules + memory)
├── arms/                     ← the arms
│   └── task-queue/           ← the durable work ledger
│       └── Now/, Next/, Waiting/, Done/             ← one task file per unit of work
└── spine/                    ← all agent work-product (this directory)
    ├── README.md             ← this file
    ├── <repo-name>/          ← one dir per repo worked in (mirrors ~/Developer/<repo-name>)
    │   ├── <scope>/          ← one dir per ticket or workstream (e.g. PROJ-123, <workstream>)
    │   │   ├── discovery.md, plan.md                ← the first effort; a later effort adds an <effort>- prefix
    │   │   ├── open-questions.md                    ← running doc, live for the scope's life
    │   │   ├── diagram/                             ← the scope's images and HTML pages (.png, .svg, .jpg, .html)
    │   │   └── scripts/                             ← the scope's code files, such as .sql
    │   └── misc/             ← non-ticket work for that repo
    ├── archive/              ← cross-repo / non-ticket material
    └── personal/             ← the user's own workspace (do not touch)
```

- Each repo touched gets a matching directory under `spine/`.
- A ticket gets a scope named for its key, for example `PROJ-123/`. A workstream that spans tickets gets a named scope, for example `<workstream>/`. Other work goes in the `misc/` scope, `spine/<repo-name>/misc/`.
- Create these directories lazily, when the work actually starts.
- A scope keeps its images and HTML pages in `diagram/` and its code files in `scripts/`. [vault-file-layout](../brain/rules/vault-file-layout.md) states this, and it says to back up before a destructive change.

## Rules

The behavioral rules live in [brain/rules/](../brain/rules/) and are indexed in [brain/README.md](../brain/README.md). The load-bearing ones for this workspace are:

- **Never modify a repo under `~/Developer/` unless the user explicitly says to.** Each repo is an independent git project with its own conventions.
- **Never `git add`, `git commit`, or `git push`** in any repo unless the user explicitly says to. See [git-conventions](../brain/rules/git-conventions.md) and [explicit-go-for-outward-actions](../brain/rules/explicit-go-for-outward-actions.md). After the work is complete, give the user a short Conventional-Commits subject with no body. The user commits.
- Keep agent artifacts in the spine, not in repo working trees.
- Each repo is its own git context. Never run git for one project from another's directory; use `git -C <project-path>`, and never combine `cd` and `git` in one compound command.

## Coding Style

See [code-style](../brain/rules/code-style.md). Prose style is separate and lives in [writing-style](../brain/rules/writing-style.md): writing is not coding.

## Ticket/Work Cadence: Discovery → Plan

Every ticket/unit of work moves through two phases, each with its own doc in the scope folder (`<repo-name>/<scope>/`). The first effort in a scope uses `discovery.md` and `plan.md`. Each later effort in the same scope adds its name as a prefix: `<effort>-discovery.md` and `<effort>-plan.md`. When a later effort starts, the first effort keeps its plain names, so no link breaks. An existing file keeps its name, also when the name does not follow this rule.

Every document carries a table of contents so readers can jump around. The cadence has no recap phase. The dated updates of the plan and the evidence in the queue task record the result.

### 1. Discovery (`discovery.md`)

The **what** and the **why** of the problem. A living document: it evolves and grows as we dig deeper. It captures the problem itself, not the solution.

### 2. Plan (`plan.md`)

The solution: **how** it is implemented and **how** it solves the problem. This doc stays static once written. If the solution changes, do not silently rewrite it; record the change as an explicit, dated update appended to the plan, so the doc tracks the evolution of the approach.

Two parts:
1. The high-level plan: the solution, the expected outcome, and how it will be accomplished.
2. The technical specification: a deeper explanation of how it will be built, with relevant code changes. Code here can be pseudo-code, to allow for the changes that are sure to happen.

## Work Tracking and Open Questions

Actionable work lives in the task queue, not in a per-scope file. The queue is the durable, cross-scope ledger at `arms/task-queue/`. It holds one task per unit of work, and the folder (`Now`, `Next`, `Waiting`, `Done`) sets the status. The standard lives in [work-tracking](../brain/rules/work-tracking.md).

The queue is the arms. Each task links its context, which is usually its scope in the spine. Status stays in the task, so a scope note does not copy it.

Unknowns live in `open-questions.md`, one per scope. This is the running doc that lives for the scope's whole life. A question needs an answer from someone else: a decision, an SME answer, anything that comes from outside the work.

Do not invent a per-scope tracker file (`todos.md`, `checklist.md`, `backlog.md`). Actionable work goes in the queue. The split is the test of where an item goes: an actionable item is a queue task, and an item that needs an outside answer is an open question. A resolved question often becomes a queue task.

### How to Keep open-questions.md

- **A question is a bullet with a bold lead-in** naming it (`**Q14 (part).**`). It is not a checkbox, because a question is not something you tick.
- **Keep answered questions, with the answer.** Mark the question `RESOLVED <date>` in place and record the answer, plus the commit or doc that acted on it. The answer is why the question was worth asking. Delete a question only when it turns out to be moot. When the file gets long, move the resolved block to the scope `archive/`.
- **Create it lazily**, when a real unknown appears. An empty file is noise.
- **No table of contents.** This file is exempt from the TOC rule in [writing-style](../brain/rules/writing-style.md).
- **Scope-local only.** There is no global open-questions file.
- **Link to it path-qualified**, as `[[<repo>/<scope>/open-questions|open questions]]`. Every scope has a file by this name, so a bare `[[open-questions]]` is ambiguous across the vault.
