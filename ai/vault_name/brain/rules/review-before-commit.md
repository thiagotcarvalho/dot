---
type: rule
tags: [workflow, git, testing]
repo: none
created: 2026-08-17
---
# Review Before Commit

Every change gets an adversarial code review before it is committed. The review is a gate, not a courtesy pass at the end.

## The Rules

0. **NEVER commit without explicit permission, reviewed or not.** A clean review is not permission. Passing tests are not permission. The only thing that authorises a commit is the user asking for one, in the moment, for this change. Review is a gate the work passes *before* it is offered for commit; it never becomes the reason to commit. Same for `git add`, `git push`, and any PR. See [explicit-go-for-outward-actions](explicit-go-for-outward-actions.md) and [git-conventions](git-conventions.md).
1. **Uncommitted work is reviewed work.** Before handing a change off for commit, run an adversarial review of the working-tree diff. Report the findings, what was fixed, and what was rejected with the reason. A change outside a git repo gets the same review, for example an authored skill in `~/.agents/skills/` or a rule in the vault:
   - Before you edit, copy the files to `~/.cache/<task-id>/review-base/`.
   - Diff the changed files against that copy. A new file has no copy, so diff it as a new file.
   - Run the review before you report the change as done.
2. **The reviewer is not the author.** Use a separate agent, given the diff and the settled decisions it must not re-litigate. The default is a read-only Codex or Claude Code reviewer that runs headless, started by the `adversarial-code-review` skill. With `--watch`, the same reviewer runs in a `herdr` pane. A `reviewer` subagent also counts. An agent reviewing its own work grades its own homework.
3. **Verify every finding before acting on it.** Reproduce it. A finding that cannot be reproduced is reported as unverified, not fixed on faith. A finding that is wrong is rejected with evidence, not accepted to be agreeable. See the `receiving-code-review` skill.
4. **Fix what the review finds, then re-run the gate.** The repo's own checks (formatter, type checker, tests) pass after the fixes, not before them.
5. **Say what the review said.** The commit hand-off names the findings, their severity, and their disposition. "Reviewed, clean" is only acceptable when a reviewer actually ran and actually found nothing.

## How to Apply

Sequence: finish the work, run the repo gate, dispatch the review, verify each finding, fix or reject with reasons, re-run the gate, then hand off for commit. Batch the review with other waiting work rather than idling on it.

Scope it: give the reviewer the diff, the intent behind it, and the list of decisions already made, so the session is spent hunting defects instead of reopening settled questions.

## Why

The user wanted this rule because two review rounds each found a real defect that the author had missed on 2026-08-14. On 2026-11-18, the user extended it to changes outside a repo, after a separate review of the review-skill rework found a high defect in skill text.

## Related

[git-conventions](git-conventions.md) · [explicit-go-for-outward-actions](explicit-go-for-outward-actions.md) · [prove-it-where-it-runs](prove-it-where-it-runs.md) · [pr-reviews-to-terminal](pr-reviews-to-terminal.md)

Skills: `adversarial-code-review` (this rule's review), `complete-code-review` (the adversarial, Python, names-and-comments, ponytail, and security reviews together), `requesting-code-review`, `receiving-code-review`, and `verification-before-completion` (the superpowers plugin).
