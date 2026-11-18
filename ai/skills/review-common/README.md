# Review Common

This folder is not a skill. It holds the parts that the three review skills
share: `adversarial-code-review`, `review-python-code`, and
`review-names-and-comments`. Each skill uses these files, and no skill runs
another skill. The `complete-code-review` skill runs all three.

| File | Contents |
| --- | --- |
| [reviewers.md](reviewers.md) | The alias table, the Codex budget check, and the selection rules |
| [scripts/review_agent.py](scripts/review_agent.py) | The reviewer runner: `budget`, `capture`, `start`, `resume`, `close` |
| [scripts/split-direction.js](scripts/split-direction.js) | The split direction of a watched reviewer pane |

## The Runner

Set the path one time: `RA="$HOME/.agents/skills/review-common/scripts/review_agent.py"`.

| Command | What it does |
| --- | --- |
| `python3 "$RA" budget` | Prints `CODEX_USED` and `CODEX_ROOM`. Use it with `eval`. |
| `python3 "$RA" capture --repo R --out FILE [--base REF \| --since TREE]` | Takes a snapshot tree of the working tree, with the untracked files, and writes a diff. Prints `TREE`, `FROM`, `CHANGED`, and `HAS_PYTHON`. Keep the output and the exit code apart: `CAP="$(python3 "$RA" capture ...)" \|\| exit 1; eval "$CAP"`. A bare `eval "$(...)"` hides a failure. |
| `python3 "$RA" start --run DIR --kind K --model M --cwd R --prompt FILE [--read DIR]... [--watch] [--timeout S]` | Starts a read-only reviewer and sends the first prompt. |
| `python3 "$RA" resume --run DIR --prompt FILE [--timeout S]` | Sends a follow-up prompt to the same reviewer. The reviewer keeps its earlier findings. |
| `python3 "$RA" close --run DIR` | Closes the pane of a watched reviewer, only while the pane still holds that reviewer. A headless reviewer has no pane. |

`capture` diffs from `HEAD` by default. `--base REF` diffs from the merge base
of `REF` and `HEAD`, so the diff holds the branch and the uncommitted edits.
`--since TREE` diffs from an earlier `TREE`, which gives a fix delta. The
snapshot uses a temporary index and does not change the real index. `git add -A`
writes loose objects, and `git gc` removes them later.

`start` and `resume` block until the reviewer replies. Each writes the reply to
`DIR/reply-N.md`, and prints `REPLY=<path>` and then the reply. Run them as a
background job of your agent tool, and do other work while the reviewer works:

- omp: `bash` with `async: true`, and a `timeout` above the `--timeout` value.
- Claude Code: `Bash` with `run_in_background: true`.

The default `--timeout` is 1800 seconds. `--read DIR` names a directory outside
`--cwd` that the reviewer must read. A claude reviewer needs it. A codex
reviewer has full read access already.

| Exit code | Meaning | What to do |
| --- | --- | --- |
| 0 | The reply is written. | Read the reply. |
| 1 | A usage or setup error, or no Herdr access for `--watch`. | Read the message. Fix the call. |
| 2 | The reviewer failed or is gone, or no watched turn was seen. | Read `DIR/stderr-N.log` or the message. For "no turn was seen", read the pane: a very fast turn can end before the runner sees it. Otherwise start a new reviewer in a new run directory, and close the old pane. |
| 3 | A timeout, or a watched reviewer is blocked. | Inspect the reviewer. A blocked reviewer needs a decision from you. |
| 4 | Codex updated itself at a watched launch. | Follow the steps in the message, then run the same `start` command again. |

## Headless Mode

Headless is the default. The runner starts `codex exec` or `claude -p` as a
child process, and keeps the session id in `DIR/state.json` for `resume`.

- Codex runs with `--sandbox read-only`. The sandbox blocks file writes and the
  Herdr socket (`Operation not permitted`).
- Claude runs with `--tools Read,Grep,Glob`, `--strict-mcp-config`,
  `--disable-slash-commands`, and `--permission-mode dontAsk`. It has no tool
  that writes a file or runs a command, so it cannot run `herdr`.
- The runner removes each `HERDR_*` variable from the environment of the child.
  Without this, the Herdr hook of the child reports its state on the author
  pane. This does not isolate the reviewer. The sandbox and the tool list do.

## Watch Mode

`--watch` starts the reviewer in a split Herdr pane, so the user can watch it.
It needs Herdr. The runner checks `HERDR_ENV=1` and a read-only socket query.
A socket error `Operation not permitted` means that you run inside a sandboxed
reviewer pane, not as the author. Then stop, and do not act as the reviewer.

- The pane splits to the right on a landscape monitor, and down on a portrait
  monitor. `split-direction.js` finds the Ghostty window that shows the Herdr
  client. It needs the macOS Automation permission for Ghostty and System
  Events, and the Accessibility permission. When it fails, the split follows
  the shape of the tab area, and the runner prints a warning.
- Codex runs with `--sandbox read-only --ask-for-approval never --no-alt-screen --no-daemon`.
  `--no-daemon` stops a version difference with the shared daemon from opening
  a settings menu that blocks the reviewer.
- Claude runs with the same tool list as headless. An interactive Claude asks
  to trust each `--add-dir` directory that it has not seen. The runner accepts
  this prompt for the `--read` directories of the run, and for no other path.
- The runner sends one pointer line to the file of the prompt. The pointer line
  holds no shell metacharacter, so it fails as one harmless `command not found`
  if it reaches a shell. A prompt sent during Codex MCP startup can be lost, so
  the runner sends it again one time when no turn starts.
- The reply is the pane text after the last pointer line, from the last 1000
  lines of the pane. It holds some screen chrome. When the pointer line is no
  longer in those lines, the runner keeps all 1000 lines and prints a warning.

### Recovery After a Codex Update

Codex can update itself at launch. The updater prints `Downloading Codex CLI`,
the tracked process exits, and the updater starts Codex again outside Herdr.
That copy can run without the read-only flags. The runner then exits with code
4 and sends no prompt. Do these steps:

1. Wait until the updater finishes.
2. Send `ctrl+c` two times: `herdr pane send-keys "$PANE" ctrl+c`.
3. Confirm the shell prompt: `herdr pane read "$PANE" --source visible`.
4. Run the same `start` command again. It uses the same pane.

## The Prompt Ban

Each reviewer prompt must hold this ban: do not run a review skill, split
panes, start agents, or use Herdr. Do not remove it. `~/.codex/AGENTS.md`
points the reviewer at `~/Developer/vault_name/brain/rules/`, and
`review-before-commit.md` tells each agent to run an adversarial review.
Without the ban, the reviewer tries to start its own review.
