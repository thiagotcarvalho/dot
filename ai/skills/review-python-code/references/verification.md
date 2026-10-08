# Verification

> Existential Birds, LLC wrote the original of this file as `review-verification-protocol` in [beagle](https://github.com/existential-birds/beagle), under the [Apache-2.0 license](../../licenses/beagle-LICENSE.txt). The user changed this file.

Complete this file for every finding before you write the report. A finding that skips it does not ship.

## Gate 0 — Echo the Artifact

Before any verdict, quote the exact code you judge, read in this same turn:

- A code finding carries the `file:line` and the cited lines, read now. Never recall them from earlier in the session.
- A diff review carries the actual diff hunk.

The source is the only authority. Never infer the content from a branch name, a directory name, a neighbouring file, or memory. When your model of the code differs from the file you just read, the file wins. A verdict with no same-turn echo is invalid.

This gate exists because a reviewer under contextual pressure states a defect in code that the file does not contain.

## Hard Gates

Complete these in order for each finding. A gate passes on objective evidence. Confidence is not evidence.

1. **Read scope.** You cite the full enclosing unit you judged: the file path plus the start and end lines, or the symbol name. Diff context alone fails this gate.
2. **Reference check.** Required for "unused", "dead code", or "never called". You ran a workspace-wide search and recorded whether a non-definition match exists. When the use may be dynamic, through a decorator, `getattr`, an entry point, or a registry, you name the registration path that could justify the name.
3. **Upstream and downstream.** Required for "missing validation", "no error handling", or "leak". You checked at least one caller, route, middleware, parent task, framework hook, or teardown path, and recorded whether the responsibility already sits there.
4. **Evidence line.** The finding carries `[FILE:LINE]` pointing at the line that shows the problem.

When a gate fails, gather the evidence or drop the finding. Never report it anyway.

## Severity

One ladder. It matches the ladder that `requesting-code-review` uses, so the two compose.

**Critical.** A sensitive field reaches a log or an external destination. A security defect. Data corruption. A crash on the happy path. A breaking change to a public API.

**Important.** A logic defect that changes behaviour. A missing validation with no upstream cover. A lost exception chain. A mutable default argument. A blocking call inside `async def`.

**Minor.** A missing type hint. A magic number. A comment that repeats the code. A name that shadows a builtin. A test that covers several cases.

**Observation.** Everything in the "Observations, Not Defects" section of `SKILL.md`, plus any suggestion that asks for a new module, a new dependency, or an abstraction that does not exist yet. An observation never enters the actionable count, and it never affects the verdict.

## Never Report

- A style preference where both forms are correct.
- Anything the formatter rewrites: indentation, line length, blank lines, whitespace, import order.
- A missing docstring on a short or private function.
- Test code held to production standards. A test is deliberately plainer.
- Generated code, vendored code, or a dependency's internals.
- A hypothetical defect that needs an unlikely precondition.
- A request for code that never existed. That is an observation.

## Output

### Strengths
What the code does well. Be specific, and cite lines.

### Findings

#### Critical
#### Important
#### Minor

Each finding carries four things:

1. `[FILE:LINE]` and a short title.
2. What is wrong.
3. Why it matters.
4. How to fix it, when the fix is not obvious.

### Observations
Items that need no action. Name each one in a single line.

### Verdict

**Ready to hand off?** Yes, No, or With fixes.

**Reasoning.** One or two sentences.

A clean verdict is not permission to commit. Only the user authorises a commit, for this change, in the moment.

## Before You Submit

1. Re-read every finding, and ask whether you verified it or assumed it.
2. Confirm that each finding points at a line that proves the problem.
3. Ask whether a domain expert would call it a defect, or a preference.
4. Ask whether the fix delivers real value, or busywork.
5. On a re-review, verify the previous fixes only. Never introduce new findings.

When a finding still feels uncertain, drop it, or state it as a question instead of a defect.
