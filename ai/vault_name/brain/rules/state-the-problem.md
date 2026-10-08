---
type: rule
tags: [workflow, decision]
repo: none
created: 2026-06-10
---
# State the Problem Before Describing the Solution

> Specify the precise conditions a solution must satisfy **before** designing the solution, and independently of it.
> (Leslie Lamport, [*State the Problem Before Describing the Solution*](https://lamport.azurewebsites.net/pubs/state-the-problem.pdf), SRI International)

## The Rule

Lamport's observation: most work is organized as *(1) informal problem statement → (2) solution → (3) proof of properties the solution happens to have*. The correct order is:

1. A brief informal statement of the problem;
2. **The precise correctness conditions required of a solution;**
3. The solution;
4. A demonstration that the solution satisfies those conditions.

The difference is profound. In the first ordering, correctness gets stated **in terms of the solution itself**: you prove things about what you built, but it's never clear what problem was actually solved, and comparing two alternative solutions becomes nearly impossible. In the second, you're forced to specify the problem independently of any solution method.

Lamport: this is "a surprisingly difficult and enlightening task. It has on several occasions led me to discover that a 'correct' algorithm did not really accomplish what I wanted it to."

(And the floor below the rule: don't be one of the "disturbingly large number of papers that never even attempt a precise statement of what problem they are solving.")

## How to Apply

- Every plan, discovery note, or PRD in this vault has a `## Problem` section **and** acceptance criteria written *before* any `## Approach`. The criteria must not mention the mechanism: if a technology, library, or design choice appears in the success conditions, rewrite them.
- Litmus test: could someone use your problem statement + criteria to judge a *completely different* solution? If not, the criteria are describing your solution, not the problem.
- For bugs: state expected vs. actual behavior and what "fixed" observably means before touching code.
- After drafting a solution, re-check it against the original conditions. This is where you discover the "correct" implementation doesn't accomplish what you actually wanted.
- When comparing options (libraries, designs, vendors), write the evaluation criteria first; otherwise the front-runner's features silently become the criteria.
- A condition that nobody has confirmed is an open question, not a criterion. Record it in the scope `open-questions.md`. Build only to the confirmed criteria. [comments-and-docstrings](comments-and-docstrings.md) states the same standard for code.

## When NOT to Apply

- Trivial mechanical chores (rename, version bump): the problem is self-evident; don't let the rule become ceremony.
- Exploratory prototyping where the goal *is* to discover the requirements. But write the conditions down as soon as they crystallize, before committing to the design.

## Red Flags

- The "problem" sentence contains "we need to add/use/migrate to…" (a solution wearing a problem's clothes).
- Acceptance criteria that read like a feature list of the chosen design.
- You can prove properties of what you built but stumble on "what breaks if we do nothing?"
- Two people debating solutions endlessly, usually solving two different unstated problems.

## Related

[you-arent-gonna-need-it](you-arent-gonna-need-it.md) · [keep-it-simple-stupid](keep-it-simple-stupid.md) · [dont-repeat-yourself](dont-repeat-yourself.md)
