# Reviewer Selection

The review skills `adversarial-code-review`, `review-python-code`, and
`review-names-and-comments`, and the `ponytail-review` and `security-review`
passes of `complete-code-review`, select the reviewer with this file. The
reviewer is a separate agent, never the author.

## Alias Table

`GPT-6.1-Sol` is the default. The reviewer kind must be `codex` or `claude`,
because only these have a read-only mode in `scripts/review_agent.py`.

| Alias       | Kind   | Model id (after `--model`) | When to use it                                                                                        |
| ----------- | ------ | -------------------------- | ----------------------------------------------------------------------------------------------------- |
| GPT-6.1-Sol | codex  | `gpt-6.1-sol`              | This is the default. A Claude model wrote the diff, and the Codex window has room.                    |
| GPT-6-Astra | codex  | `gpt-6-astra`              | Only when the user names it. It costs 5 to 10 times more than GPT-6.1-Sol.                            |
| Sonnet-5.5  | claude | `claude-sonnet-5-5`        | A Codex model wrote the diff. Or the Codex window has no room, and Sonnet 5.5 did not write the diff. |
| Opus-5.5    | claude | `claude-opus-5-5`          | The Codex window has no room, and Sonnet 5.5 wrote the diff.                                          |
| Fable-5.1   | claude | `claude-fable-5-1`         | Only when the user names it. Its input and output cost 5 times more than Sonnet-5.5.                  |

## Budget Check

All Codex models share one 5-hour limit. A different Codex model does not move
the review to a different quota. It only changes the cost. Run the check before
each codex reviewer. Keep the first value in `CODEX_USED_BEFORE` for the report.

```bash
RA="$HOME/.agents/skills/review-common/scripts/review_agent.py"
eval "$(python3 "$RA" budget)"          # sets CODEX_USED and CODEX_ROOM
: "${CODEX_USED_BEFORE:=$CODEX_USED}"
```

`CODEX_ROOM=yes` only when less than 60% of the window is used. An empty
`CODEX_USED` means that the usage report failed, and then `CODEX_ROOM=no`.

## Selection Rules

1. If the user names an alias or a model id, use it. If its kind is codex and
   `CODEX_ROOM=no`, tell the user, and run it only when the user confirms.
2. If the user names no model, test the "When to use it" cases in this order:
   Opus-5.5, Sonnet-5.5. Use the first row whose case matches. If no case
   matches, use GPT-6.1-Sol. The author is usually the agent that runs the
   skill. When omp reaches the Codex limit, it sends Codex work to Sonnet 5.5,
   so a Sonnet 5.5 subagent can also be the author.
3. Run one codex reviewer at a time. Two parallel codex reviewers can fill the
   window before a check runs. When a codex reviewer already works, select the
   next reviewer as if `CODEX_ROOM=no`.
4. Always pass `--model`. The local codex config sets `model = "gpt-6-astra"`,
   and that default does not select the reviewer. Set `KIND` and `MODEL` from
   the row, and quote them in every command.

The rules choose a reviewer from a different vendor than the author when one
can run. Otherwise, they choose a different model from the author. A reviewer
that uses the same model can miss the same defects. Sonnet-5.5 has the same
list price as GPT-6.1-Sol. Opus-5.5 costs twice as much, so it runs only when
Sonnet 5.5 wrote the diff.

For Claude, the short aliases `sonnet`, `opus`, and `fable` select the latest
model and survive version bumps. Replace the pinned ids with these aliases if
you prefer auto-latest.

## Report Line

Name the reviewer model in the report. For a codex reviewer, run the budget
check again after the review, and give `CODEX_USED_BEFORE` and the new
`CODEX_USED`.

Example: `Reviewer: GPT-6.1-Sol (codex). Codex window: 0.31 before, 0.36 after.`
