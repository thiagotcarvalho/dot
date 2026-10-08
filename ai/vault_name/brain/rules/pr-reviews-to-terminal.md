---
type: rule
tags: [workflow, tooling]
repo: none
created: 2026-07-17
---
# PR Reviews Go to the Terminal

Output PR and code reviews directly in the chat response. Do not create a Markdown file for them, not in the [spine](../../spine/README.md), not anywhere.

## The Rule

A review is a one-time read; persisting it as a `.md` is unwanted clutter. Write the findings straight into the chat response.

This is a deliberate exception to the [spine convention](../../spine/README.md) that all agent output lives in the spine. That convention still holds for plans, discovery notes, and runbooks.

A queue task may record the findings and their disposition as evidence, as [review-before-commit](review-before-commit.md) requires. That record is the result of the review. It is not a copy of the review.

## Related

[writing-style](writing-style.md) · [review-before-commit](review-before-commit.md) · [work-tracking](work-tracking.md)
