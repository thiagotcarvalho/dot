---
type: rule
tags: [git, workflow]
repo: none
created: 2026-11-19
---
# Write on the User's Behalf

An agent sometimes writes text that other people read as the user's words. The user posts the text, or the agent posts it from the user's account after a go. Examples are a reply on a pull request, a review comment, and a Jira or Slack message. This rule sets how that text answers people, cites commits, and states times. Each post still needs its own go, per [explicit-go-for-outward-actions](explicit-go-for-outward-actions.md).

## The Rules

### Replies

- **Reply in the thread when GitHub allows it.** An inline review comment has a thread. Put the reply in that thread.
- **Use a quote reply with a tag when no thread exists.** A review summary and a top-level PR comment have no thread. Quote the part of the engineer's text that the reply answers. Then tag the engineer with `@<login>`. The tag notifies the engineer. The quote shows what the reply answers. Together, they show that the reply is on the user's behalf.
- **A reply can report status.** When an engineer asks about status, the answer is a reply, not a general comment.
- **Write as the user.** The text comes from the user's account, so use the first person. Do not refer to the user as "the user".
- **Cite a commit by its short SHA, linked to the commit URL.** The URL has the shape `https://github.com/<owner>/<repo>/commit/<full sha>`. After a rebase or a restack, the link points to a commit that is not on the branch. Tell the user which posted links are stale. Give the new SHAs.

### General Comments

A general comment is a top-level PR comment that answers nobody.

- **Post a general comment only to clarify the work in the PR.** Post it only when the text would make the PR description too long. Otherwise, put the text in the description.

[git-conventions](git-conventions.md) rule 7 also applies. A decision taken during the review clarifies the work in the PR. The test of the PR description length still applies to it.

### Review Comments

A review comment that an agent drafts for the user has this shape:

- The first sentence states the fact. Name the code identifier, the file, and the line. Do not start with a label or a headline sentence.
- The evidence follows in the first person, for example "I reproduced it on [`abc1234`](https://github.com/<owner>/<repo>/commit/<full sha>)" or "In a synthetic run, ...".
- After a blank line, one sentence gives the proposal: "My suggestion would be to ...". An alternative can follow: "... would also work."
- A nit starts with `nit: ` in lowercase, and then it has the same shape. A nit is never about something that breaks. A comment about a real break is a normal comment.
- Do not use "Suggestion:", "Fix:", or "Please". Write prose. Use a code block only when the code itself is the point.
- The review summary is short and direct: one or two sentences, for example "Just a few things" or "A few changes to make". The inline comments speak for themselves, so the summary does not repeat, list, or explain them. A point that cannot sit on a diff line goes in a file-level comment on a file in the diff. The user said this on 2026-11-20.
- **Choose the review state from the comments.** A review with any comment that is not a nit is Request Changes. A review that agrees with the blocking points of another reviewer is also Request Changes. A review with only nits is Approve.
- An approval with nits has this summary: "A few nits. Up to you if you'd like to address them now or later, but approved."
- An approval with no comment can have no message. Post it with an empty summary and no thread replies, unless the user asks for text. The user said this on 2026-11-20.

### Times

- **Write each time in Eastern Time.** Write `ET` after the time, for example `11:08 ET`. Convert a UTC time from a log or a tool before you write it.
- **Use another time zone only when the conversation needs it.** For example, an engineer asks about a UTC log line, or a schedule runs in UTC. Then write the time zone after each time.

## How to Apply

Check the draft before you ask for the go:

1. A reply is in its thread. When no thread exists, the reply quotes the engineer and tags the engineer.
2. A general comment clarifies the work, and the PR description cannot hold the text.
3. The text is in the first person.
4. Each commit is a linked short SHA.
5. Each time is in ET, unless another time zone is necessary.
6. The review state follows the comments: Request Changes for any comment that is not a nit, and Approve for nits only.

## Why

The user wanted this rule because a reply to a re-review had no quote and no tag, on 2026-11-19. The review comment shape and the SHA links date from 2026-10-30. The user wanted the review-state bullets because an agent posted Comment reviews that held requests for real changes, on 2026-11-25.

## Related

[explicit-go-for-outward-actions](explicit-go-for-outward-actions.md) · [git-conventions](git-conventions.md) · [pr-reviews-to-terminal](pr-reviews-to-terminal.md) · [vault-is-not-a-repo](vault-is-not-a-repo.md) · [simplified-technical-english](simplified-technical-english.md)
