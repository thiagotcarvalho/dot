---
type: rule
tags: [workflow, decision]
repo: none
created: 2026-10-01
---
# Current State Wins

A memory note or a spine note records what was true on a date. The repo, the running system, and the database show what is true now. When the two disagree, the current state wins.

## The Rules

- **Verify a remembered fact before you rely on it.** Read the file, run the command, or query the system. Do this before you act on a path, a count, a branch, a version, or a server name.
- **Never invent a path or a name.** If a file is not where a note says, report that. Do not construct a likely name.
- **Correct the note where it lives.** Update the memory file. Add a dated update to the discovery note or the plan. Tell the user when a rule is out of date.
- **Withdraw what depends on a wrong premise.** In a plan, append a dated update that withdraws the earlier text. In a discovery note, put a dated notice at the top of the affected section. Mark each conclusion that used the premise as withdrawn. Keep the findings that still hold.
- **Update every copy of a changed decision.** When a decision changes, find each artifact that restates it: code, tests, runbooks, task records, handoffs, and memory. Correct each one.

## How to Apply

A fact in a note tells you where to look. It does not prove what is there now. A note does not change when the system changes, so a deleted script or a renamed server leaves the note as it was. Do the check before each use of the fact.

The spine already keeps the history. A plan gets an appended, dated update, and nobody rewrites it silently. A discovery note grows. A resolved question keeps its answer in `open-questions.md`. See [the spine README](../../spine/README.md) for the cadence.

## Why

The user wanted this rule because notes kept out-of-date facts, such as a deleted script path that a rule still named on 2026-09-30.

## Related

[prove-it-where-it-runs](prove-it-where-it-runs.md) · [state-the-problem](state-the-problem.md) · [dont-repeat-yourself](dont-repeat-yourself.md) · [work-tracking](work-tracking.md)
