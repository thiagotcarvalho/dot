#!/usr/bin/env python3
"""Run a read-only code reviewer for the review skills.

The reviewer is Codex or Claude. It runs headless by default. With --watch it
runs in a split Herdr pane, so the user can watch it. Each turn blocks until
the reviewer replies, and writes the reply to a file in the run directory.

Commands:
  budget   Print CODEX_USED and CODEX_ROOM for the Codex 5-hour window.
  capture  Snapshot the working tree and write a diff. Print TREE, FROM, CHANGED.
  start    Start a reviewer in a run directory and send the first prompt.
  resume   Send a follow-up prompt to the reviewer of a run directory.
  close    Close the Herdr pane of a watched reviewer.

Exit codes: 0 reply written, 1 usage or setup error, 2 reviewer failed or gone,
3 timeout or blocked reviewer, 4 Codex updated itself at a watched launch.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
CODEX_LIMIT = 0.60
DEFAULT_TIMEOUT_SECONDS = 1800
SHELL_READY_ATTEMPTS = 10
TRUST_QUIET_SECONDS = 3
TRUST_TIMEOUT_SECONDS = 30
HERDR_WAIT_SLICE_MS = 240_000
PROMPT_START_TIMEOUT_MS = 10_000
LATE_START_SECONDS = 10
STOP_GRACE_SECONDS = 10
WATCH_READ_LINES = 1000
TRUST_SESSION_ONLY_TEXT = "Your answer holds for this session"
POINTER_START = "You are a read-only code reviewer"
CLAUDE_READ_ONLY_FLAGS = [
    "--tools", "Read,Grep,Glob",
    "--strict-mcp-config",
    "--disable-slash-commands",
    "--permission-mode", "dontAsk",
]
CODEX_UPDATER_MARKERS = ("Downloading Codex CLI", "Installing standalone package")
POINTER_PATH_PATTERN = re.compile(r"[A-Za-z0-9/._-]+")


class ReviewError(Exception):
    def __init__(self, message: str, exit_code: int = 1) -> None:
        super().__init__(message)
        self.exit_code = exit_code


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True, **kwargs)


def git(repo: str, *args: str, env: dict[str, str] | None = None) -> str:
    result = run(["git", "-C", repo, *args], env=env)
    if result.returncode != 0:
        raise ReviewError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def cmd_budget(_: argparse.Namespace) -> None:
    run(["omp", "usage", "invalidate", "--provider", "openai-codex"])
    result = run(["omp", "usage", "--provider", "openai-codex", "--json"])
    used = None
    if result.returncode == 0:
        try:
            fractions = [
                float(limit["amount"]["usedFraction"])
                for report in json.loads(result.stdout).get("reports", [])
                for limit in report.get("limits", [])
                if limit.get("id") == "openai-codex:primary"
            ]
            used = max(fractions) if fractions else None
        except (ValueError, KeyError, TypeError):
            used = None
    if used is None:
        print("budget check failed: no Codex usage report, so the window has no room", file=sys.stderr)
    room = used is not None and used < CODEX_LIMIT
    print(f"CODEX_USED={'' if used is None else used}")
    print(f"CODEX_ROOM={'yes' if room else 'no'}")


def snapshot(repo: str) -> tuple[str, str]:
    """Return (seed, tree): a tree of the whole working tree, untracked files included.

    The snapshot starts from HEAD, so a tracked file that matches an ignore rule
    stays in it. It uses a temporary index and never changes the real index.
    """
    if run(["git", "-C", repo, "rev-parse", "--verify", "-q", "HEAD"]).returncode == 0:
        seed = git(repo, "rev-parse", "HEAD")
    else:
        seed = git(repo, "hash-object", "-w", "-t", "tree", "/dev/null")
    with tempfile.TemporaryDirectory(prefix="review-snap-") as tmp:
        env = {**os.environ, "GIT_INDEX_FILE": str(Path(tmp) / "index")}
        git(repo, "read-tree", seed, env=env)
        git(repo, "add", "-A", env=env)
        tree = git(repo, "write-tree", env=env)
    return seed, tree


def count_changed_lines(diff: str) -> int:
    return sum(
        1
        for line in diff.splitlines()
        if line.startswith(("+", "-")) and not line.startswith(("+++ ", "--- "))
    )


def cmd_capture(args: argparse.Namespace) -> None:
    repo = git(args.repo, "rev-parse", "--show-toplevel")
    seed, tree = snapshot(repo)
    if args.since:
        diff_from = args.since
    elif args.base:
        diff_from = git(repo, "merge-base", args.base, "HEAD")
    else:
        diff_from = seed
    # Fixed flags, so a user diff setting cannot change the prefixes or add color.
    diff = run(["git", "-C", repo, "diff", "--no-color", "--no-ext-diff", "--no-textconv", "--no-relative",
                "--src-prefix=a/", "--dst-prefix=b/", diff_from, tree])
    if diff.returncode != 0:
        raise ReviewError(f"git diff failed: {diff.stderr.strip()}")
    # Deleted files do not count: a diff that only removes Python code has nothing to review.
    names = run(["git", "-C", repo, "diff", "--name-only", "-z", "--no-relative", "--diff-filter=d",
                 diff_from, tree])
    if names.returncode != 0:
        raise ReviewError(f"git diff --name-only failed: {names.stderr.strip()}")
    has_python = any(name.endswith(".py") for name in names.stdout.split("\0"))
    Path(args.out).write_text(diff.stdout)
    print(f"TREE={tree}")
    print(f"FROM={diff_from}")
    print(f"CHANGED={count_changed_lines(diff.stdout)}")
    print(f"HAS_PYTHON={'yes' if has_python else 'no'}")


class RunState:
    """The state of one reviewer, kept in <run>/state.json."""

    def __init__(self, run_dir: Path) -> None:
        self.run_dir = run_dir
        self.path = run_dir / "state.json"
        self.data: dict = json.loads(self.path.read_text()) if self.path.exists() else {}

    def save(self) -> None:
        self.path.write_text(json.dumps(self.data, indent=2) + "\n")

    def next_reply_path(self) -> Path:
        turn = self.data.get("turns", 0)
        return self.run_dir / f"reply-{turn}.md"


def reviewer_env() -> dict[str, str]:
    """Drop the HERDR_* variables, so a headless reviewer never reports to the author pane."""
    return {key: value for key, value in os.environ.items() if not key.startswith("HERDR_")}


def run_headless_turn(state: RunState, prompt: Path, timeout: int) -> str:
    data = state.data
    turn = data.get("turns", 0)
    reply_path = state.next_reply_path()
    stdout_path = state.run_dir / f"output-{turn}.{'jsonl' if data['kind'] == 'codex' else 'json'}"
    stderr_path = state.run_dir / f"stderr-{turn}.log"
    session = data.get("session")
    if data["kind"] == "codex":
        if session:
            cmd = ["codex", "exec", "resume", session, "--model", data["model"],
                   "-c", 'sandbox_mode="read-only"']
        else:
            cmd = ["codex", "exec", "--model", data["model"], "--sandbox", "read-only", "-C", data["cwd"]]
        cmd += ["--skip-git-repo-check", "--json", "-o", str(reply_path), "-"]
    else:
        cmd = ["claude", "-p", "--model", data["model"], *CLAUDE_READ_ONLY_FLAGS, "--output-format", "json"]
        for read_dir in data["reads"]:
            cmd += ["--add-dir", read_dir]
        if session:
            cmd += ["--resume", session]

    with open(prompt, "rb") as stdin, open(stdout_path, "wb") as stdout, open(stderr_path, "wb") as stderr:
        process = subprocess.Popen(cmd, cwd=data["cwd"], env=reviewer_env(), stdin=stdin,
                                   stdout=stdout, stderr=stderr, start_new_session=True)
        returncode = wait_for_reviewer(process, timeout, stderr_path)
    if returncode != 0:
        raise ReviewError(f"the reviewer exited with code {returncode}; see {stderr_path}", 2)

    if data["kind"] == "codex":
        if not session:
            data["session"] = codex_thread_id(stdout_path)
        if not reply_path.exists():
            raise ReviewError(f"codex wrote no reply; see {stdout_path}", 2)
        reply = reply_path.read_text()
    else:
        try:
            result = json.loads(stdout_path.read_text())
        except ValueError as error:
            raise ReviewError(f"the claude output is not JSON; see {stdout_path}", 2) from error
        if not isinstance(result, dict):
            raise ReviewError(f"the claude output is not a JSON object; see {stdout_path}", 2)
        if result.get("is_error"):
            raise ReviewError(f"claude reported an error; see {stdout_path}", 2)
        data["session"] = result.get("session_id")
        reply = result.get("result", "")
        reply_path.write_text(reply)
    if not data.get("session"):
        print(f"review_agent: no session id in {stdout_path}; a follow-up cannot resume", file=sys.stderr)
    return reply


def wait_for_reviewer(process: subprocess.Popen, timeout: int, stderr_path: Path) -> int:
    """Wait for the reviewer. Stop its process group on a timeout, and when this runner is stopped.

    The reviewer runs in its own process group, so that a stop reaches each child
    process. A runner that dies with SIGKILL cannot stop the group.
    """

    def stop_and_exit(signum: int, _frame: object) -> None:
        stop_process_group(process)
        sys.exit(128 + signum)

    stop_signals = (signal.SIGTERM, signal.SIGINT, signal.SIGHUP)
    previous = {signum: signal.signal(signum, stop_and_exit) for signum in stop_signals}
    try:
        return process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        stop_process_group(process)
        raise ReviewError(f"the reviewer gave no reply in {timeout} s; see {stderr_path}", 3) from None
    finally:
        for signum, handler in previous.items():
            signal.signal(signum, handler)


def stop_process_group(process: subprocess.Popen) -> None:
    """Send SIGTERM to the group, and then SIGKILL to each process that is still in it.

    The group leader can exit before a child does, so SIGKILL goes to the group
    after the grace period also when the leader is gone.
    """
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        process.wait(timeout=STOP_GRACE_SECONDS)
    except subprocess.TimeoutExpired:
        pass
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        return
    process.wait()


def codex_thread_id(events_path: Path) -> str | None:
    for line in events_path.read_text().splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if event.get("type") == "thread.started":
            return event.get("thread_id")
    return None


def herdr(*args: str) -> subprocess.CompletedProcess[str]:
    return run(["herdr", *args])


def herdr_json(*args: str) -> dict:
    result = herdr(*args)
    if result.returncode != 0:
        raise ReviewError(f"herdr {' '.join(args)} failed: {(result.stderr or result.stdout).strip()}")
    return json.loads(result.stdout)


def check_inside_herdr() -> None:
    if os.environ.get("HERDR_ENV") != "1":
        raise ReviewError("--watch needs Herdr, and this agent does not run inside Herdr")
    current = herdr("pane", "current", "--current")
    if current.returncode != 0:
        detail = (current.stderr or current.stdout).strip()
        if "Operation not permitted" in detail:
            raise ReviewError("the Herdr socket is blocked: you are a sandboxed reviewer, not the author. Stop.")
        raise ReviewError(f"no Herdr socket access: {detail}")


def split_direction() -> str:
    script = SCRIPTS_DIR / "split-direction.js"
    result = run(["osascript", "-l", "JavaScript", str(script)])
    direction = result.stdout.strip()
    if result.returncode == 0 and direction in ("right", "down"):
        return direction
    area = herdr_json("pane", "layout", "--current")["result"]["layout"]["area"]
    direction = "right" if area["width"] >= 2 * area["height"] else "down"
    print(f"The monitor is unknown, so the split follows the tab shape: {direction}", file=sys.stderr)
    return direction


def pane_exists(pane_id: str) -> bool:
    return herdr("pane", "get", pane_id).returncode == 0


def agent_status(name: str) -> str | None:
    result = herdr("agent", "get", name)
    if result.returncode != 0:
        return None
    return json.loads(result.stdout)["result"]["agent"]["agent_status"]


def trust_prompt_directory(pane: str) -> str | None:
    """Return the directory in the Claude prompt "Adding a new directory:", or None.

    A long path wraps on the screen, so the lines up to the next sentence join.
    Claude can show a path below the home directory with "~". When the prompt
    does not offer the one-session answer "Yes, add it", the return value is ""
    so that no caller answers a prompt that it does not know.
    """
    lines = [line.strip() for line in herdr("pane", "read", pane, "--source", "visible").stdout.splitlines()]
    if "Adding a new directory:" not in lines:
        return None
    yes_index = lines.index("Yes, add it") if "Yes, add it" in lines else -1
    one_session_answer = (yes_index > 0 and lines[yes_index - 1].endswith("No, exit")
                          and TRUST_SESSION_ONLY_TEXT in " ".join(lines))
    if not one_session_answer:
        print("review_agent: the Claude trust prompt changed; answer it in the pane yourself", file=sys.stderr)
        return ""
    parts = []
    for line in lines[lines.index("Adding a new directory:") + 1:]:
        if not line.startswith("/") and parts and " " in line:
            break
        parts.append(line)
    return os.path.expanduser("".join(parts))


def trust_owned_directories(data: dict) -> bool:
    """Accept the Claude trust prompt for each --add-dir directory of this run, and no other.

    An interactive Claude asks to trust each --add-dir directory that it has not
    seen before. Herdr then reports the start as blocked. The next prompt can
    show after a gap, and Herdr can report "idle" during that gap, so the check
    ends only after the screen shows no prompt for TRUST_QUIET_SECONDS.
    """
    pane = data["pane"]
    answered: set[str] = set()
    quiet_since = None
    deadline = time.monotonic() + TRUST_TIMEOUT_SECONDS
    while time.monotonic() < deadline:
        directory = trust_prompt_directory(pane)
        if directory is None:
            quiet_since = quiet_since or time.monotonic()
            if time.monotonic() - quiet_since >= TRUST_QUIET_SECONDS:
                return agent_status(data["name"]) == "idle"
        else:
            quiet_since = None
            if directory not in data["reads"]:
                return False
            if directory not in answered:
                herdr("pane", "send-keys", pane, "down", "enter")
                answered.add(directory)
        time.sleep(0.5)
    return False


def start_watched_reviewer(state: RunState) -> None:
    data = state.data
    check_inside_herdr()
    created_pane = False
    if not (data.get("pane") and pane_exists(data["pane"])):
        split = herdr_json("pane", "split", "--current", "--direction", split_direction(),
                           "--cwd", data["cwd"], "--no-focus")
        data["pane"] = split["result"]["pane"]["pane_id"]
        created_pane = True
    data["name"] = "reviewer-" + data["pane"].replace(":", "-").lower()
    state.save()

    if data["kind"] == "codex":
        extra = ["--sandbox", "read-only", "--ask-for-approval", "never", "--no-alt-screen", "--no-daemon"]
    else:
        extra = list(CLAUDE_READ_ONLY_FLAGS)
        for read_dir in data["reads"]:
            extra += ["--add-dir", read_dir]
    # A new pane needs a moment before its shell prompt is available.
    for _ in range(SHELL_READY_ATTEMPTS):
        started = herdr("agent", "start", data["name"], "--kind", data["kind"], "--pane", data["pane"],
                        "--", "--model", data["model"], *extra)
        if "agent_pane_busy" not in started.stderr + started.stdout:
            break
        time.sleep(1)
    ready = started.returncode == 0 or (
        data["kind"] == "claude"
        and "agent_not_ready" in started.stderr + started.stdout
        and trust_owned_directories(data)
    )
    if not ready:
        if created_pane:
            herdr("pane", "close", data["pane"])
            data.pop("pane", None)
            state.save()
        raise ReviewError(f"herdr agent start failed: {(started.stderr or started.stdout).strip()}", 2)

    # Codex can update itself at launch. The tracked process then exits, and the
    # updater starts Codex again outside Herdr, maybe without the read-only flags.
    time.sleep(5)
    screen = herdr("pane", "read", data["pane"], "--source", "visible").stdout
    if agent_status(data["name"]) is None or any(marker in screen for marker in CODEX_UPDATER_MARKERS):
        raise ReviewError(
            f"the tracked read-only reviewer is not running in pane {data['pane']}. Do not prompt it. "
            "Wait until the updater finishes. Send ctrl+c two times with "
            f"`herdr pane send-keys {data['pane']} ctrl+c`. Confirm the shell prompt with "
            f"`herdr pane read {data['pane']} --source visible`. Then run the same start command again; "
            "it reuses the pane.",
            4,
        )


def pointer_line(prompt: Path) -> str:
    """Return the one line that points a watched reviewer to its prompt file.

    If the line reaches a shell, it fails as one harmless "command not found",
    so the path must hold no shell metacharacter.
    """
    prompt_path = str(prompt.resolve())
    if not POINTER_PATH_PATTERN.fullmatch(prompt_path):
        raise ReviewError(f"the prompt path holds a character that is not safe in a pointer line: {prompt_path}")
    return (f"{POINTER_START} and not the author. Do not run a review skill, "
            f"split panes, start agents, or use Herdr. Read {prompt_path} and follow it.")


def run_watched_turn(state: RunState, prompt: Path, timeout: int) -> str:
    data = state.data
    name = data["name"]
    prompt_path = str(prompt.resolve())
    pointer = pointer_line(prompt)

    def send() -> subprocess.CompletedProcess[str]:
        return herdr("agent", "prompt", name, pointer, "--wait", "--until", "working",
                     "--until", "blocked", "--timeout", str(PROMPT_START_TIMEOUT_MS))

    def recent_screen(lines: int) -> str:
        return herdr("agent", "read", name, "--source", "recent-unwrapped", "--lines", str(lines)).stdout

    sent = send()
    if sent.returncode != 0:
        # A prompt sent during Codex MCP startup can be lost. Re-send once, only
        # when the reviewer still exists and its screen does not show the prompt.
        if agent_status(name) is None:
            raise ReviewError("the reviewer is gone; start a new reviewer", 2)
        if prompt_path not in recent_screen(60):
            sent = send()
    if sent.returncode != 0:
        # A slow start can begin after the wait of the prompt command ends. The
        # screen cannot prove that a turn ran, so a turn that ends before a poll
        # sees "working" fails here; the caller inspects the pane.
        deadline = time.monotonic() + LATE_START_SECONDS
        while agent_status(name) not in ("working", "blocked"):
            if time.monotonic() >= deadline:
                raise ReviewError(
                    f"no turn was seen: {(sent.stderr or sent.stdout).strip()}. "
                    f"Read the pane with `herdr agent read {name} --source recent-unwrapped`.", 2)
            time.sleep(1)

    deadline = time.monotonic() + timeout
    while True:
        remaining_ms = int((deadline - time.monotonic()) * 1000)
        if remaining_ms <= 0:
            raise ReviewError(f"the reviewer gave no reply in {timeout} s; status {agent_status(name)}", 3)
        waited = herdr("agent", "wait", name, "--until", "idle", "--until", "done", "--until", "blocked",
                       "--timeout", str(min(remaining_ms, HERDR_WAIT_SLICE_MS)))
        status = agent_status(name)
        if status is None:
            raise ReviewError("the reviewer is gone; start a new reviewer", 2)
        if status == "blocked":
            raise ReviewError(f"the reviewer is blocked; inspect it with `herdr agent read {name}`", 3)
        if waited.returncode == 0 and status in ("idle", "done"):
            break

    # Keep only the text after the pointer line, so an earlier turn does not repeat.
    # The search starts at the pointer text, so a reply that quotes the path stays whole.
    screen = recent_screen(WATCH_READ_LINES)
    pointer_at = screen.rfind(POINTER_START)
    path_at = screen.find(prompt_path, pointer_at) if pointer_at != -1 else -1
    if path_at == -1:
        print("review_agent: the pointer line scrolled out of the read; the reply can be cut", file=sys.stderr)
        reply = screen
    else:
        reply = screen[screen.find("\n", path_at) + 1:]
    state.next_reply_path().write_text(reply)
    return reply


def check_prompt(prompt: Path, watch: bool) -> None:
    if not prompt.is_file():
        raise ReviewError(f"no prompt file: {prompt}")
    if watch:
        pointer_line(prompt)


def run_turn(state: RunState, prompt: Path, timeout: int) -> None:
    if state.data["watch"]:
        reply = run_watched_turn(state, prompt, timeout)
    else:
        reply = run_headless_turn(state, prompt, timeout)
    reply_path = state.next_reply_path()
    state.data["turns"] = state.data.get("turns", 0) + 1
    state.save()
    print(f"REPLY={reply_path}")
    print(reply)


def cmd_start(args: argparse.Namespace) -> None:
    check_prompt(Path(args.prompt), args.watch)
    run_dir = Path(args.run).resolve()
    run_dir.mkdir(parents=True, exist_ok=True)
    state = RunState(run_dir)
    if state.data.get("turns"):
        raise ReviewError(f"{run_dir} already has a reviewer; use resume")
    reads = [str(run_dir)] + [str(Path(path).expanduser().resolve()) for path in args.read]
    state.data.update(kind=args.kind, model=args.model, cwd=str(Path(args.cwd).resolve()),
                      reads=reads, watch=args.watch)
    state.save()
    if args.watch:
        start_watched_reviewer(state)
    run_turn(state, Path(args.prompt), args.timeout)


def cmd_resume(args: argparse.Namespace) -> None:
    state = RunState(Path(args.run).resolve())
    if not state.data.get("turns"):
        raise ReviewError(f"{args.run} has no reviewer; use start")
    if not state.data["watch"] and not state.data.get("session"):
        raise ReviewError(f"{args.run} has no session id; start a new reviewer", 2)
    check_prompt(Path(args.prompt), state.data["watch"])
    run_turn(state, Path(args.prompt), args.timeout)


def cmd_close(args: argparse.Namespace) -> None:
    state = RunState(Path(args.run).resolve())
    pane = state.data.get("pane")
    if not state.data.get("watch") or not pane:
        print("a headless reviewer has no pane to close")
        return
    # Close the pane only while it still holds this reviewer, never a reused pane id.
    agent = herdr("agent", "get", state.data["name"])
    if agent.returncode != 0 or json.loads(agent.stdout)["result"]["agent"]["pane_id"] != pane:
        print(f"pane {pane} no longer holds reviewer {state.data['name']}; close it yourself if it is yours")
        return
    herdr_json("pane", "close", pane)
    print(f"closed pane {pane}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser("budget").set_defaults(func=cmd_budget)

    capture = commands.add_parser("capture")
    capture.add_argument("--repo", required=True)
    capture.add_argument("--out", required=True)
    origin = capture.add_mutually_exclusive_group()
    origin.add_argument("--base", help="diff from the merge base of this ref and HEAD")
    origin.add_argument("--since", help="diff from this earlier TREE (a fix delta)")
    capture.set_defaults(func=cmd_capture)

    start = commands.add_parser("start")
    start.add_argument("--run", required=True)
    start.add_argument("--kind", required=True, choices=["codex", "claude"])
    start.add_argument("--model", required=True)
    start.add_argument("--cwd", required=True)
    start.add_argument("--prompt", required=True)
    start.add_argument("--read", action="append", default=[],
                       help="a directory outside --cwd that a claude reviewer must read")
    start.add_argument("--watch", action="store_true")
    start.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    start.set_defaults(func=cmd_start)

    resume = commands.add_parser("resume")
    resume.add_argument("--run", required=True)
    resume.add_argument("--prompt", required=True)
    resume.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    resume.set_defaults(func=cmd_resume)

    close = commands.add_parser("close")
    close.add_argument("--run", required=True)
    close.set_defaults(func=cmd_close)

    args = parser.parse_args()
    if getattr(args, "model", None) == "":
        parser.error("--model is empty; resolve the reviewer first")
    try:
        args.func(args)
    except ReviewError as error:
        print(f"review_agent: {error}", file=sys.stderr)
        sys.exit(error.exit_code)


if __name__ == "__main__":
    main()
