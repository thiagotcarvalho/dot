---
type: reference
tags: [workflow, tooling]
repo: none
created: 2026-07-17
---
# This Is the Brain

How agents *behave*. This is the stable identity layer: the standards agents are held to and the facts they have learned. It is the counterpart to the [spine](../spine/README.md), which is what agents *produce and interact with* (repo/ticket work-product). The arms are the task queue in `arms/task-queue/`, and they do the work.

Everything here is plain Markdown so any agent tool can read it. See [How Tools Load the Brain](#how-tools-load-the-brain).

## The Story the Rules Tell

The rules describe the life of one unit of work:

1. **Take the work.** Take a task from the queue. Read the context that it links, usually a scope in the spine.
2. **Understand it.** State the problem before the solution. Check each remembered fact against the current state.
3. **Design it.** Choose the simplest design that meets the current requirement. Give each module one reason to change. Keep one source for each fact. Guard each write to a system of record.
4. **Build it.** Write code to the code standards.
5. **Write it.** Write notes and messages to the prose standards.
6. **Prove it.** Prove the change where it runs. Get an adversarial review from another agent.
7. **Hand it off.** Give the work to the user with a commit subject. The user decides each outward action, and an agent acts only after an explicit go.

Two boundaries hold at every step. Each outward action waits for an explicit go. The vault stays out of every repo.

## The Two Bins

**[rules/](rules/): authored standards.** Deliberately-written principles and policies, stable and curated. The litmus: *would you hand this to a new hire as "how we work here"?* The table follows the story above.

| Stage | Rule | Description |
| --- | --- | --- |
| Always | [explicit-go-for-outward-actions](rules/explicit-go-for-outward-actions.md) | Draft, then wait for an explicit go before any outward action |
| Always | [vault-is-not-a-repo](rules/vault-is-not-a-repo.md) | Personal vault, untracked; never referenced from any repo |
| Always | [vault-file-layout](rules/vault-file-layout.md) | Images and HTML pages in diagram/, code in scripts/; no version control, so back up before a destructive change |
| Always | [skills-are-tools](rules/skills-are-tools.md) | Install skills by copy, trimmed and checked; a skill must not collide with a rule |
| 1. Take the work | [work-tracking](rules/work-tracking.md) | The task queue is the arms; each task links its context, usually a scope |
| 2. Understand it | [state-the-problem](rules/state-the-problem.md) | State the problem and success criteria before designing the solution |
| 2. Understand it | [current-state-wins](rules/current-state-wins.md) | Verify remembered facts; the repo and the running system decide |
| 3. Design it | [keep-it-simple-stupid](rules/keep-it-simple-stupid.md) | Prefer the simplest design that works |
| 3. Design it | [you-arent-gonna-need-it](rules/you-arent-gonna-need-it.md) | Build only what the current requirement demands |
| 3. Design it | [dont-repeat-yourself](rules/dont-repeat-yourself.md) | One authoritative representation for each piece of knowledge |
| 3. Design it | [solid-principles](rules/solid-principles.md) | One reason to change; extend without edits; a port where a fake or a second adapter exists |
| 3. Design it | [guarded-writes](rules/guarded-writes.md) | Dry run first; write only a proven change to exactly one target |
| 4. Build it | [ponytail-baseline](rules/ponytail-baseline.md) | Write code through the ponytail skill; simplicity always wins |
| 4. Build it | [code-style](rules/code-style.md) | Google pyguide; self-documenting names, one case per test |
| 4. Build it | [flat-is-better-than-nested](rules/flat-is-better-than-nested.md) | Max 1-2 levels of nesting per function; refactor deeper code |
| 4. Build it | [comments-and-docstrings](rules/comments-and-docstrings.md) | Google pyguide §3.8, minimal, explain why not what |
| 5. Write it | [writing-style](rules/writing-style.md) | Fewer em-dashes, plain tone, no hard-wrapped prose, TOC on docs |
| 5. Write it | [simplified-technical-english](rules/simplified-technical-english.md) | ASD-STE100 for all prose: short sentences, active voice, one meaning per word |
| 5. Write it | [note-properties](rules/note-properties.md) | Every hand-authored brain/spine note carries a controlled YAML block |
| 6. Prove it | [prove-it-where-it-runs](rules/prove-it-where-it-runs.md) | A check proves only what it ran, on the host where it ran |
| 6. Prove it | [review-before-commit](rules/review-before-commit.md) | Adversarial review by another agent gates every commit |
| 6. Prove it | [pr-reviews-to-terminal](rules/pr-reviews-to-terminal.md) | Deliver reviews in chat, never as a saved file |
| 7. Hand it off | [git-conventions](rules/git-conventions.md) | Never commit/push; no AI attribution; short subjects |

A rule can end with a Why section. It has one or two sentences in this shape: "The user wanted this rule because <reason> on <date>." When only one bullet has a recorded reason, name that bullet in place of "this rule". Put incident detail in the task records and the spine, not in the rule.

**[memory/](memory/MEMORY.md): accreted facts.** Specific, learned context that grows over time (environment quirks, project state, references). The litmus: *did this get captured because it came up mid-session?* Indexed in [memory/MEMORY.md](memory/MEMORY.md), which is auto-loaded by Claude Code every session.

A memory note records what was true on a date, so [current-state-wins](rules/current-state-wins.md) governs its use. When a memory states a standard, propose a rule to the user. After the user accepts the rule, remove the standard from the memory. Keep the memory only for the case detail that the rule does not hold.

## The Skills View

**`skills/`: a read-only view, not a bin.** The dir holds three symlinks to the real skill roots, so Obsidian shows every skill in the file explorer. It stores no content of its own. This view is optional. The template does not include it, because the link targets are specific to each machine.

| Link        | Target                          | Content                              |
| ----------- | ------------------------------- | ------------------------------------ |
| `authored`  | `~/.agents/skills`              | My own skills, the tool-neutral root |
| `installed` | `~/.local/share/agent-skills`   | Skills a separate installer manages  |
| `plugins`   | `~/.claude/plugins/cache`       | Skills a marketplace plugin supplies |

The `plugins` link points at the cache root and not at one version dir. A plugin upgrade changes the version dir, so a deeper link would break.

Three cautions apply:

- A file under `skills/` is the real file. An edit or a delete in Obsidian changes the source. When `promptDelete` is `false` in the vault, a delete gives no warning.
- Obsidian Sync does not follow a symlink. Another device does not get this view.
- macOS file events do not cross a symlink. Reload the vault if an external change does not appear.

## How Tools Load the Brain

The canonical entry point is the vault's [`AGENTS.md`](../AGENTS.md), which points at both bins, the spine, and the arms. Each agent tool needs at most a one-line pointer:

- **Claude Code:** the memory dir `~/.claude/projects/<project>/memory/` is a symlink to `memory/` here, so `MEMORY.md` auto-loads and new auto-saved memories land directly in the brain. `~/Developer/CLAUDE.md` carries a pointer to `rules/` so rules surface every session. The language standard is wired separately, because output styles are injected verbatim and cannot be a read-hop: `~/.claude/settings.json` sets `"outputStyle": "ASD-STE100"` and `~/.claude/output-styles/ASD-STE100.md` defines it, naming [simplified-technical-english](rules/simplified-technical-english.md) as authoritative. A named style with no file in that directory is silently inert.
- **Codex:** `~/.codex/AGENTS.md` is the global instruction file and carries the pointer. `~/.codex/config.toml` holds no instruction text, so the pointer cannot live there.
- **Any other tool:** point its config file (its own `AGENTS.md`, a global rules file, etc.) at `../AGENTS.md`. That is the entire adapter. Do not copy the brain into a tool; point at it. A tool with its own output-style or persona mechanism also gets the [simplified-technical-english](rules/simplified-technical-english.md) wiring, because a language standard must arrive with the prompt.

A pointer only tells an agent where the brain is. The `frankenstein` skill loads it. The real skill lives in `~/.agents/skills/frankenstein/`, which Codex and other runtimes read directly, and `~/.claude/skills/frankenstein` is a relative symlink to it. That is the same one-real-copy pattern the memory symlink uses. Invoke it as `/frankenstein` when an agent must hold the whole brain, and not just know its address.
