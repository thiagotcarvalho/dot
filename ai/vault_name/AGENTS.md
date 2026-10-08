---
type: reference
tags: [workflow, tooling]
repo: none
created: 2026-07-17
---
# AGENTS.md

This file provides guidance to AI systems working in this workspace. It is the canonical entry point: any agent tool should be pointed here.

## The Organism: Brain, Spine, and Arms

`~/Developer/vault_name` is an Obsidian vault that holds three parts, kept deliberately separate: the brain, the spine, and the arms.

- **[brain/](brain/README.md)**: how agents *behave*. Authored [rules](brain/rules/) (standards agents are held to) and accreted [memory](brain/memory/MEMORY.md) (facts agents have learned). This is the stable identity layer, not tied to any one ticket.
- **[spine/](spine/README.md)**: what agents *produce and interact with*. All agent work-product: plans, architecture, discovery notes, runbooks, scratch analysis. Prefer Markdown and `[[wikilinks]]`, since this is an Obsidian vault.
- **[arms/task-queue/](arms/task-queue/README.md)**: the *arms*, the task queue. It holds one task for each unit of work, in `Now`, `Next`, `Waiting`, and `Done`. Each task links its context, usually a scope in the spine. The task itself holds the next action, the status, and the evidence.

## The Brain

Read [brain/README.md](brain/README.md) for the behavior layer.

> How agents *behave*. This is the stable identity layer: the standards agents are held to and the facts they have learned. It is the counterpart to the [spine](spine/README.md), which is what agents *produce and interact with* (repo/ticket work-product). The arms are the task queue in `arms/task-queue/`, and they do the work.

**Language standard:** every agent writes in Simplified Technical English (ASD-STE100), in chat responses and in every file. [simplified-technical-english](brain/rules/simplified-technical-english.md) is authoritative and lists the per-tool wiring.

## The Spine

Read [spine/README.md](spine/README.md) for the interaction layer.

> **All work agents produce lives in the spine.** Agents do not write into the actual code repos. The repos under `~/Developer/` are read/edit targets only when the user explicitly asks to work in one; notes about that work stay in the spine.

## The Arms

Read [work-tracking](brain/rules/work-tracking.md) for the standard. The `Now`, `Next`, and `Waiting` tasks in [arms/task-queue/](arms/task-queue/README.md) are the open work.

> The spine gives each task its context. The arms do the work, and they keep the status and the evidence.

## Repos in the Workspace

| Repo (`~/Developer/<name>`) | What it is | Spine dir |
| --- | --- | --- |
| `<repo>` | One sentence about the repo. Name its default branch. | `spine/<repo>/` |
