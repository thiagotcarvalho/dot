---
name: frankenstein
description: >
  Use when the user runs /frankenstein, says "load the brain", "load the vault",
  "load brain and spine", "load my standards", or "wake up". Also use when an
  agent must apply the user's standards but has not read ~/Developer/vault_name in
  this session, or when it does not know which rules and cadence govern the work.
---

# Frankenstein

Assemble the organism. The brain is how agents behave. The spine holds the context of the work. The arms are the task queue in `arms/task-queue/`, and they do the work. All three live in the Obsidian vault at `~/Developer/vault_name`.

This skill works in any agent and any working directory. Use the absolute paths below. Do not assume that a context file already loaded the vault. A pointer is not the content.

## What to Load

Read these five items:

1. `~/Developer/vault_name/AGENTS.md` — the canonical entry point and the repo table.
2. `~/Developer/vault_name/brain/README.md` — the rule index and the per-tool adapter list.
3. Every `.md` file in `~/Developer/vault_name/brain/rules/`. List that directory, then read every file the listing returns. The rule set grows, so never work from a fixed list of names.
4. `~/Developer/vault_name/brain/memory/MEMORY.md` — the index of learned facts.
5. `~/Developer/vault_name/spine/README.md` — the layout, the Discovery-Plan cadence, and the running-docs convention.

The list order is not the read order. Only the rule files depend on an earlier result, the directory listing. Use two batches of parallel calls:

- Batch 1:
  - Read items 1, 2, 4, and 5.
  - List `brain/rules/`.
  - Run the two queue commands from [After the Load](#after-the-load).
- Batch 2: read every rule file that the listing returns.

If your tool runs one call at a time, make the same calls in sequence.

## Read in Full, Not by Index

Read each rule file completely. An index line names a rule. It does not state the rule. An agent that reads only the index will miss the constraints that matter, for example the exact git clauses.

At load time, read only the memory index, item 4. Each memory file covers one narrow topic. Read one memory file when its topic appears in the work. Do not load them all at the start.

Read a spine scope only when the work names it. A queue task links its context. `spine/personal/` is the user's own workspace, so do not read it or write in it without a direct request.

## After the Load

Apply the loaded standards immediately. They are active for the rest of the session, and they outrank your default behavior.

Read the arms before you start work. Run these two queue commands:

```
find ~/Developer/vault_name/arms/task-queue/Now ~/Developer/vault_name/arms/task-queue/Next ~/Developer/vault_name/arms/task-queue/Waiting -name '*.md'
for d in Now Next Waiting; do echo "$d $(find ~/Developer/vault_name/arms/task-queue/$d -name '*.md' | wc -l | tr -d ' ')"; done
```

The first command lists every open task. The `Now`, `Next`, and `Waiting` tasks are the open work. The second command counts the tasks in each folder.

The Arms line of the inventory is a count, not a queue status report. Copy the three counts from the second command. For the count, do not open the task files.

Read `~/Developer/vault_name/brain/rules/work-tracking.md` before you change the queue or report its status. Before you work a task, read the notes that it links.

Report the inventory in this shape, so the user can see what arrived:

```
Brain: I read <N> rule files and indexed <M> memory entries.
Spine: I read the layout and the cadence.
Language: ASD-STE100 is active.
Arms: <A> tasks are in Now, <B> are in Next, and <C> are in Waiting.
Repo: The work is in <repo>.
Open conflicts: <one sentence for each open conflict>
```

`<N>` is the number of rule files that you read. `<M>` is the number of entries in the Memory section of `MEMORY.md`. Count both. Do not estimate.

If the user names no repo, write "Repo: No repo is named." If no open conflict exists, write "Open conflicts: There are none."

An open conflict is one of two things:

- Two loaded sources disagree, and no rule names the winner.
- An action in this session breaks a loaded rule, for example a commit without a request.

Report a disagreement between two sources only when you noticed it during the reads. Do not search for one. Do not compare the sources with each other or with your defaults. Report each earlier action in this session that a loaded rule forbids. A rule that overrides a default is not a conflict, because the rule wins.

Name both sides of each open conflict in one sentence. Do not investigate a conflict during the load. Before you rely on a conflicting fact, follow `~/Developer/vault_name/brain/rules/current-state-wins.md`. Do not change a harness memory store outside the vault without a request from the user.

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| The agent reads `brain/README.md` and stops. | The index is not the rules. Read every file in `brain/rules/`. |
| The agent reads all memory files. | Read `MEMORY.md`. Read a detail file on demand. |
| The agent reports "loaded" with no counts. | Report the counts. The count is the proof. |
| The agent writes a note into a code repo. | The spine holds agent work-product. The rules state the exceptions. |
| The agent keeps its default prose style. | ASD-STE100 governs every sentence after the load. |
| The agent works a task without its context. | Read the notes that the task links before the work starts. |
| The agent reads one file in each turn, but its tool can run parallel calls. | Read the independent files in one batch of parallel calls. |
| The agent lists each rule that overrides a default as a conflict. | Report only open conflicts. A rule that wins over a default is not a conflict. |
| The agent compares every source to prove that no conflict exists. | Report only the disagreements that you noticed during the reads. Report each rule break in this session. |
