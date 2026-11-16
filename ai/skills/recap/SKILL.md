---
name: recap
description: Summarizes the most recent work in the current session in one paragraph. Use when the user calls /recap.
disable-model-invocation: true
---

# Recap

Write one paragraph for the user about the most recent work in this session.

## Find the Most Recent Work

The most recent work is the latest user goal for which the agent used tools. It starts at the user message that set the goal. It includes each follow-up turn on the same goal. It stops before this `/recap` call.

- An earlier goal is not part of the recap, also when it is in the same repo or area.
- An answer without tool calls after the work, for example an explanation, is not part of the recap.
- If no goal in the session used tools, write one sentence that says so.

Use only facts that the session shows: tool output and the reports of the agent. Do not run a tool.

## Write the Paragraph

The reply is one paragraph of 4 to 6 sentences, in the first person. Each sentence has at most 25 words. The paragraph has these parts, in this order:

1. The goal, in one sentence.
2. The main result and its strongest evidence, for example a test count or a read-back check. Give the result, not each step.
3. What the work did not do or did not change, for example "not pushed" or "no change made". Include each failure that the work found but did not cause.
4. What waits for the user: each open question and each action that needs a go. If nothing waits, the last sentence is "Nothing waits for you."

Keep the exact names: file paths, branches, PR numbers, and task IDs. The reply contains only the paragraph.
