"""These tests check the behavior of pr_wait.py with a fake gh on PATH."""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "pr_wait.py"
REPO = "acme/widgets"
NUMBER = "7"
PULL = f"repos/{REPO}/pulls/{NUMBER}"
REVIEWS = f"{PULL}/reviews"
REVIEW_COMMENTS = f"{PULL}/comments"
ISSUE_COMMENTS = f"repos/{REPO}/issues/{NUMBER}/comments"

FAKE_GH = """#!/usr/bin/env python3
import json, os, sys
from pathlib import Path

fixtures = Path(os.environ["FAKE_GH_DIR"])
endpoint = next(arg for arg in sys.argv[2:] if not arg.startswith("-"))
login_failures = fixtures / "login_failures_left"
poll_failures = fixtures / "poll_failures_left"
failures_left = login_failures if endpoint == "user" else poll_failures
if failures_left.exists() and int(failures_left.read_text()) > 0:
    failures_left.write_text(str(int(failures_left.read_text()) - 1))
    sys.exit("gh: HTTP 502")
body = json.loads((fixtures / (endpoint.replace("/", "_") + ".json")).read_text())
print(json.dumps([body] if "--slurp" in sys.argv else body))
"""


def comment(item_id, login, **fields):
    return {
        "id": item_id,
        "user": {"login": login} if login else None,
        "body": "Please rename this.",
        "created_at": "2026-11-25T16:00:00Z",
        "html_url": f"https://github.com/{REPO}/pull/{NUMBER}#c{item_id}",
        **fields,
    }


class PrWaitTest(unittest.TestCase):
    def setUp(self):
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        root = Path(temp_dir.name)
        bin_dir = root / "bin"
        bin_dir.mkdir()
        fake_gh = bin_dir / "gh"
        fake_gh.write_text(FAKE_GH)
        fake_gh.chmod(0o755)
        self.fixtures = root / "fixtures"
        self.fixtures.mkdir()
        self.marker = root / "state" / "watchtower" / "acme_widgets_7.json"
        self.env = {
            **os.environ,
            "PATH": f"{bin_dir}:{os.environ['PATH']}",
            "FAKE_GH_DIR": str(self.fixtures),
            "XDG_STATE_HOME": str(root / "state"),
        }
        self.serve("user", {"login": "me"})
        self.serve(PULL, {"state": "open", "merged": False})
        for endpoint in (REVIEWS, REVIEW_COMMENTS, ISSUE_COMMENTS):
            self.serve(endpoint, [])

    def serve(self, endpoint, body):
        (self.fixtures / (endpoint.replace("/", "_") + ".json")).write_text(json.dumps(body))

    def start_watch(self):
        """Record a watch that started before any item existed."""
        self.marker.parent.mkdir(parents=True, exist_ok=True)
        self.marker.write_text(json.dumps({"reviews": [], "review_comments": [], "issue_comments": []}))

    def run_script(self, *args, timeout=10):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            env=self.env,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )

    def wait_output(self):
        result = self.run_script("wait", REPO, NUMBER, "--interval", "0")
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def ack(self, output):
        result = self.run_script("ack", REPO, NUMBER, output["ack"])
        self.assertEqual(result.returncode, 0, result.stderr)

    def item_ids(self, output):
        return [(item["kind"], item["id"]) for item in output["items"]]

    def test_new_comment_wakes(self):
        self.start_watch()
        self.serve(ISSUE_COMMENTS, [comment(5, "reviewer")])

        output = self.wait_output()

        self.assertEqual(output["event"], "feedback")
        self.assertEqual(self.item_ids(output), [("issue_comments", 5)])

    def test_own_comment_ignored(self):
        self.start_watch()
        self.serve(ISSUE_COMMENTS, [comment(6, "me"), comment(7, "reviewer")])

        output = self.wait_output()

        self.assertEqual(self.item_ids(output), [("issue_comments", 7)])

    def test_approval_without_text_ignored(self):
        self.start_watch()
        self.serve(REVIEWS, [comment(3, "reviewer", state="APPROVED", body="")])
        self.serve(ISSUE_COMMENTS, [comment(8, "reviewer")])

        output = self.wait_output()

        self.assertEqual(self.item_ids(output), [("issue_comments", 8)])

    def test_empty_commented_review_yields_its_inline_comment(self):
        self.start_watch()
        self.serve(REVIEWS, [comment(4, "reviewer", state="COMMENTED", body="")])
        self.serve(REVIEW_COMMENTS, [comment(9, "reviewer", path="app.py", line=12)])

        output = self.wait_output()

        self.assertEqual(self.item_ids(output), [("review_comments", 9)])

    def test_changes_requested_without_text_wakes(self):
        self.start_watch()
        self.serve(REVIEWS, [comment(2, "reviewer", state="CHANGES_REQUESTED", body=None)])

        output = self.wait_output()

        self.assertEqual(self.item_ids(output), [("reviews", 2)])

    def test_deleted_account_comment_wakes(self):
        self.start_watch()
        self.serve(ISSUE_COMMENTS, [comment(11, None)])

        output = self.wait_output()

        self.assertEqual(self.item_ids(output), [("issue_comments", 11)])

    def test_acked_item_stays_quiet(self):
        self.start_watch()
        self.serve(ISSUE_COMMENTS, [comment(5, "reviewer")])
        self.ack(self.wait_output())
        self.serve(ISSUE_COMMENTS, [comment(5, "reviewer"), comment(6, "reviewer")])

        output = self.wait_output()

        self.assertEqual(self.item_ids(output), [("issue_comments", 6)])

    def test_unacked_item_returns(self):
        self.start_watch()
        self.serve(ISSUE_COMMENTS, [comment(5, "reviewer")])
        self.wait_output()

        output = self.wait_output()

        self.assertEqual(self.item_ids(output), [("issue_comments", 5)])

    def test_late_published_review_wakes(self):
        self.start_watch()
        self.serve(REVIEWS, [comment(20, "second", state="COMMENTED")])
        self.ack(self.wait_output())
        self.serve(REVIEWS, [comment(10, "first", state="COMMENTED"), comment(20, "second", state="COMMENTED")])

        output = self.wait_output()

        self.assertEqual(self.item_ids(output), [("reviews", 10)])

    def test_late_published_inline_comment_wakes(self):
        self.start_watch()
        self.serve(REVIEW_COMMENTS, [comment(20, "second")])
        self.ack(self.wait_output())
        self.serve(REVIEW_COMMENTS, [comment(10, "first"), comment(20, "second")])

        output = self.wait_output()

        self.assertEqual(self.item_ids(output), [("review_comments", 10)])

    def test_ack_covers_only_its_own_wake(self):
        self.start_watch()
        self.serve(ISSUE_COMMENTS, [comment(5, "reviewer")])
        first_wake = self.wait_output()
        self.serve(ISSUE_COMMENTS, [comment(5, "reviewer"), comment(6, "reviewer")])
        self.wait_output()
        self.ack(first_wake)

        output = self.wait_output()

        self.assertEqual(self.item_ids(output), [("issue_comments", 6)])

    def test_missing_marker_starts_from_now(self):
        self.serve(ISSUE_COMMENTS, [comment(5, "reviewer")])
        with self.assertRaises(subprocess.TimeoutExpired):
            self.run_script("wait", REPO, NUMBER, "--interval", "0.1", timeout=2)
        self.serve(ISSUE_COMMENTS, [comment(5, "reviewer"), comment(6, "reviewer")])

        output = self.wait_output()

        self.assertEqual(self.item_ids(output), [("issue_comments", 6)])

    def test_unreadable_marker_reports_error(self):
        self.start_watch()
        self.marker.write_text("")

        output = self.wait_output()

        self.assertEqual(output["event"], "error")

    def test_merged_pull_request_ends_watch(self):
        self.start_watch()
        self.serve(PULL, {"state": "closed", "merged": True})

        output = self.wait_output()

        self.assertEqual(output, {"event": "closed", "merged": True})

    def test_repeated_login_failures_end_watch(self):
        self.start_watch()
        (self.fixtures / "login_failures_left").write_text("99")

        output = self.wait_output()

        self.assertEqual(output["event"], "error")

    def test_single_login_failure_recovers(self):
        self.start_watch()
        self.serve(ISSUE_COMMENTS, [comment(5, "reviewer")])
        (self.fixtures / "login_failures_left").write_text("1")

        output = self.wait_output()

        self.assertEqual(self.item_ids(output), [("issue_comments", 5)])

    def test_repeated_poll_failures_end_watch(self):
        self.start_watch()
        (self.fixtures / "poll_failures_left").write_text("99")

        output = self.wait_output()

        self.assertEqual(output["event"], "error")

    def test_single_poll_failure_recovers(self):
        self.start_watch()
        self.serve(ISSUE_COMMENTS, [comment(5, "reviewer")])
        (self.fixtures / "poll_failures_left").write_text("1")

        output = self.wait_output()

        self.assertEqual(self.item_ids(output), [("issue_comments", 5)])

    def test_unwritable_state_reports_error(self):
        self.start_watch()
        self.serve(ISSUE_COMMENTS, [comment(5, "reviewer")])
        self.marker.parent.chmod(0o500)
        self.addCleanup(self.marker.parent.chmod, 0o700)

        output = self.wait_output()

        self.assertEqual(output["event"], "error")

    def test_inline_comment_carries_thread_location(self):
        self.start_watch()
        self.serve(REVIEW_COMMENTS, [comment(9, "reviewer", path="app.py", line=12, in_reply_to_id=4)])

        item = self.wait_output()["items"][0]

        self.assertEqual(
            {key: item[key] for key in ("author", "url", "path", "line", "in_reply_to_id")},
            {
                "author": "reviewer",
                "url": f"https://github.com/{REPO}/pull/{NUMBER}#c9",
                "path": "app.py",
                "line": 12,
                "in_reply_to_id": 4,
            },
        )


if __name__ == "__main__":
    unittest.main()
