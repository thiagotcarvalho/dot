# Python Review Checklist

> Existential Birds, LLC wrote the original of this file as part of `python-code-review` in [beagle](https://github.com/existential-birds/beagle), under the [Apache-2.0 license](../../licenses/beagle-LICENSE.txt). The user changed this file.

You are the reviewer. Apply this file to the scope in your prompt. Only read
files. Report as text.

Formatting is out of scope. The repository formatter owns indentation, line
length, blank lines, and import order. Never report a finding that the
formatter rewrites on the next run.

Names, comments, docstrings, and test names are out of scope. Another review
covers them.

## Quick Reference

Load a reference when the column on the left describes the code in front of you.

| Issue type | Reference |
|---|---|
| Missing or wrong type hints, `Any`, generics | [type-safety.md](type-safety.md) |
| Blocking calls in async, missing `await` | [async-patterns.md](async-patterns.md) |
| Bare `except`, swallowed errors, lost context | [error-handling.md](error-handling.md) |
| Mutable defaults, magic numbers, deep nesting | [common-mistakes.md](common-mistakes.md) |
| Duplicated knowledge, logging safety | [house-rules.md](house-rules.md) |
| False-positive screen, severity, verdict | [verification.md](verification.md) |

## Review Checklist

### Type safety
- [ ] Every parameter and every return value carries a type.
- [ ] `Any` appears only where an untyped boundary forces it.
- [ ] A collection type is generic: `list[T]`, `dict[K, V]`.
- [ ] The code writes `T | None`, and never `Optional[T]`.

### Async
- [ ] No blocking call runs inside an `async def`.
- [ ] Every coroutine call has an `await`.
- [ ] An async context manager uses `async with`.

### Error handling
- [ ] No bare `except:` clause exists.
- [ ] A re-raise preserves the chain with `raise ... from`.
- [ ] An error message carries enough context to diagnose the failure.

### Common mistakes
- [ ] No mutable default argument exists.
- [ ] A magic number has a named constant.
- [ ] An early return replaces a deep `if` pyramid.
- [ ] No name shadows a builtin, such as `id`, `type`, or `list`.

### House rules
- [ ] No log statement carries a sensitive field.

## Valid Patterns — Never Flag These

- `dict.get(key, default)`. This returns a default. It does not suppress an error.
- `typing.cast()` after a runtime check. The check narrows the type, so the cast is correct.
- A type annotation on a variable. An annotation is not a cast, and it is not validation.
- `Any` at an untyped library boundary. The external package supplies no stubs.
- An empty `__init__.py`. The file declares a package, and it needs no code.
- A `noqa` comment. The suppressed rule does not apply to that line.

## Observations, Not Defects

Report each item below as an observation. Never count it as a defect, and never block on it. The house rules on simplicity and on speculative work decide whether the change earns its cost, and that decision belongs to the author.

- **Sequential awaits that `asyncio.gather` could run together.** Concurrency earns its place only when the latency is a stated requirement.
- **A plain `dict` that a `TypedDict` could describe.** A new class for one caller is speculative structure.
- **A bare `raise` with no log line.** Logging the same failure at every layer duplicates the record.

## Context-Sensitive Rules

| Finding | Report it only if |
|---|---|
| Broad exception handling | A specific exception type exists and carries meaning, and the handler is not teardown or a top-level boundary |
| Unused name | The name has no `_` prefix, and a workspace-wide search finds no dynamic registration |
| Missing validation | No caller, route, middleware, or framework already validates the value |
| Missing type hint | The function is public, and the type is not obvious from the assignment |

## Gates

Complete these in order. Never advance until the pass condition holds.

1. **Scope.** You list every `.py` path you inspected on this run.
2. **False-positive screen.** You checked each planned finding against **Valid Patterns**, **Observations**, and **Context-Sensitive Rules**, then dropped or narrowed it.
3. **Evidence.** Each finding carries `[FILE:LINE]`, or a bounded line range. `LINE` is the line in the current file, not the line in the diff. Read the file to get it. A symbol name supplements that anchor. It never replaces it.
4. **Verification.** You load [verification.md](verification.md) and complete its steps for every finding you still plan to report.
5. **Ship.** Your output follows the structure in that reference, and every finding carries a severity.
