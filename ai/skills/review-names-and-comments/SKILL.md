---
name: review-names-and-comments
description: Reviews comments, docstrings, variable names, function and method names, class names, and test names against the user's rules, in any language, with a second, read-only coding agent, Codex or Claude. It runs headless by default, and `--watch` runs it in a split Herdr pane. Use when the user asks to review, check, or align names, comments, docstrings, or tests with the user's rules.
---

# Review Names and Comments

A second coding agent reviews names, comments, docstrings, and tests against
the rules in `~/Developer/vault_name/brain/rules/`, as
[references/reviewer.md](references/reviewer.md) defines. The reviewer runs
read-only. The author verifies each finding, fixes or rejects it, and reports
the result.

This skill is standalone. It does not run `adversarial-code-review` or
`review-python-code`. The `complete-code-review` skill runs all three. The
shared parts are in `~/.agents/skills/review-common/`:
[reviewers.md](../review-common/reviewers.md) selects the reviewer, and
[README.md](../review-common/README.md) documents the runner, the exit codes,
and watch mode.

## Inputs

| Input | Default | Effect |
| --- | --- | --- |
| `--watch` | off | The reviewer runs in a split Herdr pane, and the user can watch it. |
| `--model <alias or id>` | the selection rules | It selects the reviewer. See [reviewers.md](../review-common/reviewers.md). |
| Paths of files or folders | none | The reviewer reviews these files in full. |
| `--base <ref>` | the default branch | The diff holds the branch from the merge base, and the uncommitted edits. |
| `--diff <file>` and a context directory | none | The reviewer reviews the lines that this diff adds or changes. |
| `WORK` and `DIFF_FILE`, set by the caller | none | The skill uses this directory and this diff, and skips steps 1 and 2. |

With no paths and no diff, the scope is the lines that the current branch adds
or changes, from the merge base with the default branch.

## Workflow

1. Create an owned work directory. The skill deletes only a directory that it
   created.

   ```bash
   RA="$HOME/.agents/skills/review-common/scripts/review_agent.py"
   REPO_ROOT="$(git rev-parse --show-toplevel)"
   WORK="$(mktemp -d -t names-review-XXXXXX)"
   DIFF_FILE="$WORK/review.diff"
   ```

2. Set the scope. For named paths, skip the capture. Otherwise, capture the
   branch diff, and stop when it is empty.

   ```bash
   BASE="${USER_BASE:-}"   # set USER_BASE to the --base ref, when the user gives one
   [ -n "$BASE" ] || BASE="$(git -C "$REPO_ROOT" symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null)"
   for ref in main master; do
     [ -n "$BASE" ] || ! git -C "$REPO_ROOT" rev-parse -q --verify "$ref" >/dev/null || BASE="$ref"
   done
   [ -n "$BASE" ] || { echo "no default branch found; pass --base <ref>" >&2; rm -rf "$WORK"; exit 1; }
   CAP="$(python3 "$RA" capture --repo "$REPO_ROOT" --out "$DIFF_FILE" --base "$BASE")" || exit 1
   eval "$CAP"
   REVIEWED="$TREE"; N=0
   [ -s "$DIFF_FILE" ] || { echo "the diff is empty; nothing to review" >&2; rm -rf "$WORK"; exit 0; }
   ```

   For `--diff`, set `REPO_ROOT` to the context directory, and copy the file
   instead: `cp -- "<user-diff>" "$DIFF_FILE"`. For a diff of fixes, ask the
   user for it.

3. Select the reviewer with [reviewers.md](../review-common/reviewers.md). Set
   `KIND` and `MODEL`.

4. Write the [prompt](#reviewer-prompt) to `$WORK/names-prompt.md`.

5. Start the reviewer as a background job of your agent tool. The command
   blocks until the reviewer replies.

   ```bash
   RUN="$WORK/names"
   python3 "$RA" start --run "$RUN" --kind "$KIND" --model "$MODEL" \
     --cwd "$REPO_ROOT" --prompt "$WORK/names-prompt.md" --read "$WORK" \
     --read "$HOME/.agents/skills/review-names-and-comments" \
     --read "$HOME/Developer/vault_name/brain/rules"     # add --watch for --watch
   ```

6. When the job ends, read `$RUN/reply-0.md`. For an exit code other than 0, see
   the table in [README.md](../review-common/README.md).

7. Verify each finding against the rule file that it names. Reject a wrong
   finding with evidence.

8. Fix the findings that hold. Do not wait for a go, with one exception: a
   `DECISION:` finding, for example a test to delete, needs the user's choice.
   1. Rename each symbol with the language server (`lsp` rename or references),
      so that each caller changes, in every file. If no language server is
      available, find the callers with `grep` across the repo, and say so.
   2. A rename of a public name breaks callers outside the repo. Name that risk
      in the report.
   3. Run the tests and the linters that cover the changed files.

9. Send the fix delta to the same reviewer, and repeat until it reports no open
   finding. Append one line to the follow-up prompt for each finding that you
   rejected, with the reason. A rejected finding is not open. The reviewer
   reports it again only when it shows that the reason is wrong.

   ```bash
   N=$((N + 1))
   CAP="$(python3 "$RA" capture --repo "$REPO_ROOT" --out "$WORK/fix-$N.diff" --since "$REVIEWED")" || exit 1
   eval "$CAP"
   printf '%s\n' "Review only the changes in $WORK/fix-$N.diff. Verify the fixes of your earlier findings. Report each finding that is still open, and each new finding in the lines that this diff changes. The rules of the first prompt still apply." > "$WORK/names-fix-$N.prompt.md"
   python3 "$RA" resume --run "$RUN" --prompt "$WORK/names-fix-$N.prompt.md"   # background job
   REVIEWED="$TREE"
   ```

10. Report: the reviewer's tables, each change you made, each finding you
    rejected and why, each `DECISION:` finding that waits for the user, each
    check result, and the report line from
    [reviewers.md](../review-common/reviewers.md).

When the user releases the review, run `python3 "$RA" close --run "$RUN"` for a
watched reviewer, and then `rm -rf "$WORK"`.

## Reviewer Prompt

```text
You are a names and comments reviewer and not the author. Do not run a review
skill. Do not split panes, start agents, or use Herdr. Only read files. Report
your findings as text.

Read ~/.agents/skills/review-names-and-comments/references/reviewer.md and
follow it.

Scope: <one of: "only the lines that /path/of/DIFF_FILE adds or changes" | "these paths, in full: /path/one /path/two">.
Repository root: <REPO_ROOT>.
```

## Examples

**Default: a headless review of the branch.** The user says "check the names
and comments on this branch". A Claude model wrote the diff, and a codex
reviewer already works for another review, so the reviewer is Sonnet-5.5.

```bash
RA="$HOME/.agents/skills/review-common/scripts/review_agent.py"
REPO_ROOT="$(git rev-parse --show-toplevel)"
WORK="$(mktemp -d -t names-review-XXXXXX)"; DIFF_FILE="$WORK/review.diff"
CAP="$(python3 "$RA" capture --repo "$REPO_ROOT" --out "$DIFF_FILE" --base main)" || exit 1
eval "$CAP"; REVIEWED="$TREE"
KIND=claude MODEL=claude-sonnet-5-5
# write $WORK/names-prompt.md, then, as a background job:
python3 "$RA" start --run "$WORK/names" --kind "$KIND" --model "$MODEL" \
  --cwd "$REPO_ROOT" --prompt "$WORK/names-prompt.md" --read "$WORK" \
  --read "$HOME/.agents/skills/review-names-and-comments" --read "$HOME/Developer/vault_name/brain/rules"
```

**Watch the reviewer, with named files.** The user says
"review-names-and-comments --watch src/billing/". Skip the capture. Set the
scope line of the prompt to that folder, in full, and add `--watch` to `start`.

**A finding and its fix.** The reply holds the row
`| 14 | def proc(d): | code-style.md | def queue_order(order): |`. Read
`code-style.md` and confirm the rule. Rename `proc` with the language server,
run the tests, and report: "Renamed `proc` to `queue_order` in 3 files. `proc`
was public, so a caller outside the repo breaks."
