---
type: rule
tags: [git, workflow]
repo: none
created: 2026-10-09
---
# Pull Request Size and Stacks

A reviewer must understand the business context and the code of each pull request. A large pull request hides defects from the reviewer. AI agents write code quickly, so their pull requests grow large. This rule limits the size of a pull request, and it sets the standard for a stack of pull requests.

## The Rules

### Size

- **A pull request adds at most 750 lines of new code.** Count the added lines of source code and of tests. A pull request can be larger only when the user keeps a larger topic whole.
- **One topic goes in one pull request.** Keep a change in a single pull request, also when the work has several parts. Split a change into several pull requests only when its parts have different topics. A story of more than 5 topics is the one exception, as the Stacks section states.
- **Some lines do not count.** Deleted lines do not count. Docs, config files, generated files, lockfiles, vendored code, and bulk data files that a script produced do not count.
- **A mechanical pull request has no size limit.** A file move, a formatter run, or a rename by a tool can have any size. That pull request holds no other change.
- **Ask before you split a large change.** When one topic adds more than 750 lines, ask the user whether to split it. Split it only when the user says so. Otherwise it stays one pull request.
- **Plan the pull requests before you write code.** List each topic, its pull request, and its size estimate. Put the list in the plan of the scope.

### Each Pull Request

- **A refactor or a move is a different topic.** A pull request that changes behavior does not also refactor or move code. The refactor or the move goes in its own pull request.
- **New code merges with its first caller.** A new function or API is in the same pull request as the first code that uses it.
- **No pull request uses a temporary shim.** A shim is temporary code that keeps the checks green until a later pull request removes it. Each pull request passes the repo checks on its own, without a shim. When a pull request needs a shim, it is not ready. Change the order or the boundaries of the pull requests.

### Stacks

- **A stack holds different topics that depend on each other.** One topic is one pull request, not a stack. A stack tells one story. Each pull request in it is one topic. A story of more than 5 topics is the one exception. A reviewer reads the stack from the bottom to the top. Each pull request makes sense without the pull requests above it.
- **A stack holds at most 5 pull requests.** Prefer a smaller stack of larger pull requests to a larger stack of smaller pull requests. When a story has more than 5 topics, combine the closest topics into one pull request. Do not combine a refactor or a move with another topic. Keep each combined pull request at 750 lines or fewer. Split the story into several stacks only when that is not enough. Open each later stack after the stack before it merges.
- **A stack does not delete or rewrite its own code.** No pull request in a stack deletes or rewrites code that an earlier pull request in the same stack added. That code is wasted work for the author and for the reviewer. Write each line in its final form in the pull request that adds it.
- **A stack does not improve code that it deletes.** When a stack removes a line or a piece of logic, no earlier pull request in the stack optimizes that line or that logic first.

### Description

- **Each pull request states the what and the why.** The description says what the change does. It also says why the change is necessary. The code shows how.
- **A replacement states what the deleted code did.** When a pull request deletes code and adds code that does the same job, the description lists each job of the deleted code. For each job, it says where the job now lives, or it says that the pull request stops the job on purpose.
- **The description is short.** It says what changes in one sentence and why in one sentence. It gives each behavior change in one line, with at most 5 lines. It does not explain how the code works or list the commits, because the diff shows them. It holds at most one example, and only for output that people see.
- **The repo template sets the sections.** The description adds no section of its own. When the repo has no template, use these sections: Summary, Changes, and Validation. Add a Deploy section only when an operator must act.
- **The description gives no test counts.** The validation lists the commands that passed. Test counts change on every rebase, and CI shows its own results.

## How to Apply

### Measure Each Pull Request

```bash
git -C <repo> diff --numstat <base>...<head>
```

For a pull request in a stack, `<base>` is the branch directly below it. Each output line shows the insertions, the deletions, and the path of one file.

Decide the role of each file from its content and its place in the repo. The file extension does not decide the role, because a YAML or JSON file can hold test cases. A file of business rules is a config file.

Add the insertions of the source files and the test files. Git counts a changed line as one deletion and one insertion, so a changed line counts once. When the sum is more than 750, ask the user whether to split the change before you write the description. A mechanical pull request does not split.

### Check the Stack

Before you offer a stack, compare two numbers:

1. For each pull request, run `git -C <repo> diff --shortstat <base>...<head>`. Add the insertions and the deletions of all the pull requests.
2. Run `git -C <repo> diff --shortstat <trunk>...<top>`, where `<top>` is the branch of the last pull request. Add its insertions and its deletions.

When the first number is larger, the stack changes some lines more than once. Read the diff of each pull request to find those lines. When a later pull request deletes or rewrites a line from an earlier one, change the earlier pull request. Restack the branches above it. Then measure again.

### Write the Description

Write the description for a reviewer who does not know the context:

- **What.** State the change in behavior in one sentence.
- **Why.** State the problem or the business need that the change solves.
- **Replaced jobs.** For a replacement, list the jobs of the deleted code, as [Description](#description) states.

Put the reasoning in the description itself. Do not cite a vault note, per [vault-is-not-a-repo](vault-is-not-a-repo.md). Use the pull request template of the repo for the layout.

## Why

The user wanted this rule because AI-written pull requests became too large for a careful human review, on 2026-10-09. The user wanted the short description rules because the descriptions of a stack grew long, with sections that the template did not ask for, on 2026-10-27. The user raised the limit to 750 lines and asked for one pull request for each topic, with a question before any split, on 2026-11-24. The user lowered the stack limit to 5 pull requests because a longer stack is too much to review, on 2026-11-24.

## Related

[git-conventions](git-conventions.md) · [review-before-commit](review-before-commit.md) · [vault-is-not-a-repo](vault-is-not-a-repo.md) · [explicit-go-for-outward-actions](explicit-go-for-outward-actions.md) · [state-the-problem](state-the-problem.md)
