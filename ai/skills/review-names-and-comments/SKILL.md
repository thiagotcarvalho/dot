---
name: review-names-and-comments
description: Use when the user asks to review, check, or align comments, docstrings, variable names, method names, function names, or test names with the user's rules, in any language. Also use when another review skill reaches its names and comments checks.
---

# Review Names and Comments

## Read the Rules

The rules in `~/Developer/vault_name/brain/rules/` are the only standard. This skill holds no copy of them. Read each file below in full before the review.

| Target | Rule files |
|---|---|
| Names of variables, functions, methods, classes, and tests | `code-style.md` |
| Test bodies: one case, behavior and not message text, no test for removed behavior | `code-style.md` |
| Comments and docstrings | `comments-and-docstrings.md`, `simplified-technical-english.md` (the English inside them), `writing-style.md` (the bullet about removed things), `vault-is-not-a-repo.md` |

## Set the Scope

- If the user names files or folders, review those files in full.
- If the user names nothing, review only the lines that the current branch adds or changes. Get them with `git diff "$(git merge-base HEAD main)"`. Use the repo's default branch if it is not `main`.
- A name or a comment on a line outside the scope is not a finding, also when it breaks a rule.
- Review every language in the scope. The Python-only parts of the rules, for example the Google pyguide docstring sections, apply only to Python.
- Review only the five targets. Logic, types, and formatting are not part of this review.

## Report First

Write the report in chat. Change no file before the user gives a go. The report has these parts, in this order:

1. The scope: the base commit or the paths, and the files that you read.
2. One table for each file, with the columns `Line`, `Current`, `Rule`, and `Proposed fix`. `Rule` is the rule file name. When a fix needs a decision from the user, for example a test to delete, `Proposed fix` states the choice.
3. One line for each comment or docstring that you checked and kept, with the reason that it follows the rules.
4. The last line: "Which findings do I fix?"

When another review skill loaded this skill, put the findings in that skill's report, and do not write a second report.

## Fix After the Go

1. Fix only the findings that the user approves.
2. Rename each symbol with the language server (`lsp` rename or references), so that each caller changes, in every file. If no language server is available, find the callers with `grep` across the repo, and say so.
3. A rename of a public name breaks callers outside the repo. Name that risk in the result.
4. Run the tests and the linters that cover the changed files.
5. Report each change and each check result.
