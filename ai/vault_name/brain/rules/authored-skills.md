---
type: rule
tags: [tooling, workflow]
repo: none
created: 2026-11-18
---
# Write Skills That Stand Alone

This rule covers each skill that the user authors in `~/.agents/skills/`. [skills-bring-methods](skills-bring-methods.md) covers the skills of other authors.

## The Rules

- **One skill does one job.** A skill that is not an umbrella skill does not load or run another skill. When a job needs several skills, an umbrella skill runs them. An umbrella skill can also run an installed skill. For example, `complete-code-review` runs `adversarial-code-review`, `review-python-code`, `review-names-and-comments`, and the installed `ponytail-review`. Each part stays usable alone.
- **An umbrella skill passes its inputs.** It names the inputs that it gives each part, for example one work directory and one diff. Each part says that it accepts these inputs.
- **Shared parts live in a shared folder.** Code or text that several skills use goes in a folder in `~/.agents/skills/` that is not a skill and has no `SKILL.md`, for example `review-common/`. Apply these rules:
  - In a command, refer to the folder by its full path, for example `$HOME/.agents/skills/review-common/`.
  - In a Markdown link, use a relative path, for example `../review-common/reviewers.md`.
  - Link the folder into `~/.claude/skills/` with a relative link, so that a relative path from a linked skill finds it.
  - Copy the folder together with each skill that uses it.
  - Remove the folder and its link only when no skill uses it.
- **A skill starts its agents headless.** An agent that a skill starts runs headless by default. A `--watch` option runs it in a `herdr` pane, so that the user can watch it. Both modes give the same result.
- **Each skill gives core examples.** It shows the default call, each main option, and the shape of the output. An agent that reads only the examples can run the skill.

## How to Apply

Before you write a new skill, read the `write-a-skill` skill for its structure. Then apply these rules. Check an existing skill against them at its next change. Write the skill text in ASD-STE100, as [simplified-technical-english](simplified-technical-english.md) requires.

## Why

The user wanted this rule because `adversarial-code-review` had become both an umbrella skill and a standalone skill, so the user split it into standalone skills, an umbrella skill, headless agents, and core examples, on 2026-11-18.

## Related

[skills-bring-methods](skills-bring-methods.md) · dot-mirror · [keep-it-simple-stupid](keep-it-simple-stupid.md) · [review-before-commit](review-before-commit.md)
