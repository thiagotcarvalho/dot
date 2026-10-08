---
type: rule
tags: [workflow, tooling]
repo: none
created: 2026-10-07
---
# Ponytail Is the Baseline for Code

Simplicity always wins. Write the least code that meets the requirement. The ponytail skill is the tool for this standard, and every agent uses it as its baseline for code.

## The Rules

- **Load ponytail before you write code.** This applies to new code, a fix, a refactor, a design, a code review, and the choice of a dependency. It does not apply to prose or notes.
- **Use the shared copy.** The skill is in `~/.agents/skills/ponytail/`. Every agent loads it from there. Claude Code loads it through the link in `~/.claude/skills/`.
- **Give the baseline to each subagent.** When a subagent writes code, name this rule and the `ponytail` skill in its task.

## How to Apply

Read the task and the code that it touches first, as [state-the-problem](state-the-problem.md) and [current-state-wins](current-state-wins.md) require. Then use the ponytail ladder to choose the solution.

When a code review is part of the task, add a `ponytail-review` pass for over-engineering. That pass does not find defects, so the adversarial review in [review-before-commit](review-before-commit.md) still runs. When the user asks for a whole-repo audit, use `ponytail-audit`. When the user asks for the list of `ponytail:` markers, use `ponytail-debt`.

## Why

The user wanted this rule because agents often write too much code when little code is needed, on 2026-10-07. Simplicity always wins: over-engineering is necessary only for space software, and this work is not space software.

## Related

[keep-it-simple-stupid](keep-it-simple-stupid.md) · [you-arent-gonna-need-it](you-arent-gonna-need-it.md) · [code-style](code-style.md) · [review-before-commit](review-before-commit.md)
