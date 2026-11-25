#!/usr/bin/env python3
"""Wait for new feedback from other people on one pull request, then print it as JSON."""

import argparse
import json
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path

LISTS = {
    "reviews": "pulls/{number}/reviews",
    "review_comments": "pulls/{number}/comments",
    "issue_comments": "issues/{number}/comments",
}
MAX_FAILURES = 5


class GhError(Exception):
    pass


def gh_api(*args):
    result = subprocess.run(["gh", "api", *args], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise GhError(result.stderr.strip() or result.stdout.strip())
    return json.loads(result.stdout)


def with_retries(read, interval):
    """Return read(), after up to MAX_FAILURES tries in sequence."""
    last_error = None
    for _ in range(MAX_FAILURES):
        try:
            return read()
        except GhError as error:
            last_error = error
        time.sleep(interval)
    raise last_error


def read_pull_request(repo, number):
    # ponytail: Each poll makes 4 calls, so one watch uses about 240 of the 5,000 calls an hour.
    # Use conditional requests on the newest page of each list if the number of watches grows.
    lists = {}
    for kind, path in LISTS.items():
        pages = gh_api("--paginate", "--slurp", f"repos/{repo}/{path.format(number=number)}")
        lists[kind] = [item for page in pages for item in page]
    return gh_api(f"repos/{repo}/pulls/{number}"), lists


def state_path(repo, number, suffix):
    state_home = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local" / "state"))
    return state_home / "watchtower" / f"{repo.replace('/', '_')}_{number}{suffix}"


def read_json(path, default):
    return json.loads(path.read_text()) if path.exists() else default


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(path.name + ".tmp")
    temp_path.write_text(json.dumps(value))
    temp_path.replace(path)


def author(item):
    return (item.get("user") or {}).get("login")


def is_feedback(kind, item, login):
    """Return True for an item that another person wrote and that carries a request.

    A review in state COMMENTED with an empty body only wraps inline comments,
    and the inline comments list returns those comments.
    """
    if author(item) == login:
        return False
    return kind != "reviews" or item["state"] == "CHANGES_REQUESTED" or bool(item.get("body"))


def summarize(kind, item):
    return {
        "kind": kind,
        "id": item["id"],
        "author": author(item),
        "time": item.get("submitted_at") or item.get("created_at"),
        "url": item.get("html_url"),
        "path": item.get("path"),
        "line": item.get("line"),
        "in_reply_to_id": item.get("in_reply_to_id"),
        "state": item.get("state"),
        "body": item.get("body"),
    }


def wait(repo, number, interval):
    """Poll until feedback arrives or the pull request closes.

    The marker holds every ID that the user saw, not the highest ID. A pending
    review gets its ID when the reviewer starts it. The reviewer can submit it
    after a newer review, so its ID can be lower than an ID that the user saw.
    """
    marker = state_path(repo, number, ".json")
    login = with_retries(lambda: gh_api("user"), interval)["login"]
    seen = read_json(marker, None)
    while True:
        pull, lists = with_retries(lambda: read_pull_request(repo, number), interval)
        if pull["state"] != "open":
            return {"event": "closed", "merged": pull["merged"]}
        visible = {kind: sorted(item["id"] for item in items) for kind, items in lists.items()}
        if seen is None:
            seen = visible
            write_json(marker, seen)
        items = [
            summarize(kind, item)
            for kind, kind_items in lists.items()
            for item in kind_items
            if item["id"] not in seen[kind] and is_feedback(kind, item, login)
        ]
        if items:
            token = uuid.uuid4().hex[:12]
            write_json(state_path(repo, number, f".{token}.shown.json"), visible)
            return {"event": "feedback", "items": items, "ack": token}
        time.sleep(interval)


def ack(repo, number, token):
    """Add the IDs that one wake showed to the marker. The token names that wake."""
    marker = state_path(repo, number, ".json")
    shown_path = state_path(repo, number, f".{token}.shown.json")
    seen = read_json(marker, {})
    shown = read_json(shown_path, {})
    write_json(marker, {kind: sorted(set(seen.get(kind, [])) | set(shown.get(kind, []))) for kind in LISTS})
    shown_path.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    wait_command = commands.add_parser("wait", help="Poll until new feedback arrives, then print it.")
    wait_command.add_argument("repo")
    wait_command.add_argument("number")
    wait_command.add_argument("--interval", type=float, default=60)
    ack_command = commands.add_parser("ack", help="Record that the user saw the items of one wake.")
    ack_command.add_argument("repo")
    ack_command.add_argument("number")
    ack_command.add_argument("token", help="The `ack` value from the output of that wake.")
    args = parser.parse_args()
    if args.command == "ack":
        ack(args.repo, args.number, args.token)
        return
    try:
        print(json.dumps(wait(args.repo, args.number, args.interval)))
    except (GhError, OSError, ValueError) as error:
        print(json.dumps({"event": "error", "detail": str(error)}))


if __name__ == "__main__":
    sys.exit(main())
