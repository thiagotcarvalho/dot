---
name: watchtower
description: >
  Use when the user asks to watch a pull request, for example "watch PR 342" or
  "watch <PR URL> --watch". A poll waits with no model tokens. When another person
  posts feedback, the agent checks each request against the code. It drafts the
  reply and the fix, and it waits for the user's go.
---

# Watchtower

This skill watches one or more pull requests for feedback from other people. `scripts/pr_wait.py` polls GitHub about once a minute and uses no model. It exits when it finds a new review or comment by another person. It also exits when the pull request is merged or closed, or after 5 failed reads in sequence. The agent runs it as a background job, so the agent can end its turn while it waits.

The rules in `~/Developer/vault_name/brain/rules/` keep their authority over this skill. The rules that apply most are `explicit-go-for-outward-actions.md`, `review-before-commit.md`, `git-conventions.md`, `write-on-the-users-behalf.md`, and `work-tracking.md`.

## Examples

Watch in the current session:

```text
User: watch PR 7
Agent: I watch acme/widgets#7. I will tell you when another person posts feedback.
```

Watch in a new herdr pane:

```text
User: watch https://github.com/acme/widgets/pull/7 --watch
Agent: The watch runs in pane w5:p9, as agent watch-pr7.
```

This is one `feedback` output of `pr_wait.py wait`:

```json
{"event": "feedback",
 "items": [{"kind": "review_comments", "id": 9, "author": "reviewer", "time": "2026-11-25T16:00:00Z",
            "url": "https://github.com/acme/widgets/pull/7#discussion_r9", "path": "app.py", "line": 12,
            "in_reply_to_id": null, "state": null, "body": "Please rename this."}],
 "ack": "3f9c2a7b1d04"}
```

The other outputs are `{"event": "closed", "merged": true}` and `{"event": "error", "detail": "<gh error>"}`.

This is the table that the agent shows on a wake:

```markdown
| Item | Verdict | Draft reply |
| --- | --- | --- |
| [reviewer on app.py:12](https://github.com/acme/widgets/pull/7#discussion_r9) | Valid: `app.py:12` names a list `data`. | I renamed it to `claims` in [`abc1234`](https://github.com/acme/widgets/commit/<full sha>). |
```

## Start a Watch

1. Get the pull request from the user's words. A number uses the repo of the current directory (`gh repo view --json nameWithOwner`). A URL gives the repo and the number.
2. Without `--watch`, go to step 4.
3. With `--watch`, do these steps, and then stop. The new agent continues from step 4.
   1. Check that the session runs inside herdr: `test "${HERDR_ENV:-}" = 1`. If it does not, tell the user, and stop.
   2. Read the layout with `herdr pane layout --pane "$HERDR_PANE_ID"`. Split to the right when the pane width is at least twice its height. Otherwise split down.
   3. Run `herdr pane split --current --direction <right|down> --cwd <repo checkout> --no-focus`. Read the new pane ID from `.result.pane.pane_id`.
   4. Run `herdr agent start watch-pr<number> --kind omp --pane <pane id>`.
   5. Run `herdr agent prompt watch-pr<number> "Use the watchtower skill to watch <pull request URL>. You run in the watch pane."`.
   6. Tell the user the pane ID and the agent name.
4. Read the pull request once: the title, the body, the head SHA, and the open review threads. This gives the context for the next wake.
5. Start the poll as a background bash job with `async` and `timeout: 0`:

   ```bash
   python3 "$HOME/.agents/skills/watchtower/scripts/pr_wait.py" wait <owner/repo> <number>
   ```

   On the first run, the script records the IDs of all current items, so the watch starts from now.
6. Tell the user that the watch runs. End the turn.

## Handle a Wake

The job output is one JSON object.

- For `closed`, tell the user that the pull request is merged or closed. Do not start the poll again.
- For `error`, show the detail to the user. Start the poll again only when the user says so.
- For `feedback`, do the steps below.

1. Create or update the worktree `~/Developer/<repo>-wt-pr<number>` at the head of the pull request branch. Use `git -C`. Do not change the branch before the user's go.
2. For each item, give a verdict: valid, not valid, or a question. Cite the evidence as `file:line`, a test, or a command output.
3. Draft each reply in the first person, per `write-on-the-users-behalf.md`:
   - For an inline comment (`review_comments`), reply in its thread.
   - For a review body or a top-level comment, quote the part that the reply answers. Tag the author with `@<login>`.
   - Link each commit as a short SHA. Write each time in ET.
4. For a valid change, make the fix in the worktree. Do not commit. Run the narrow checks of the repo for the changed code.
5. Show the table from [Examples](#examples), and the diff under it.
6. Record that the user saw the items of this wake. Use the `ack` value from the output of this wake:

   ```bash
   python3 "$HOME/.agents/skills/watchtower/scripts/pr_wait.py" ack <owner/repo> <number> <ack value>
   ```

7. Record the round as dated evidence in the queue task whose `Links` name the pull request. When no task links it, tell the user.
8. Start the poll again, as in step 5 of [Start a Watch](#start-a-watch). End the turn.

## Act on a Go

Each post, commit, and push needs its own explicit go. Agreement with a draft is not a go.

1. Before the first commit of a fix, run the adversarial review of the worktree diff with the `adversarial-code-review` skill. Report each finding and its disposition.
2. On a go to commit, commit in the worktree with a short subject and no body.
3. On a go to push, push the branch.
4. On a go to post a reply, post only the reply that the go names. Then read it back with `gh api`.
   - For an inline comment, post to `repos/<owner/repo>/pulls/<number>/comments/<root id>/replies`. The root ID is `in_reply_to_id` when the item has one. Otherwise, it is the item `id`. GitHub does not accept a reply to a reply.
   - For a quote reply, post to `repos/<owner/repo>/issues/<number>/comments`.

## Stop or Change a Watch

- "Stop watching PR 342": end the background job of that poll.
- "Also watch PR 365": start the steps of [Start a Watch](#start-a-watch) from step 1 for that pull request. Each pull request has its own job and its own seen marker.
- With `--watch`, the user closes the pane to stop all of its watches.

The seen marker of each pull request is `~/.local/state/watchtower/<owner>_<repo>_<number>.json`. Delete it to start a watch from now again.
