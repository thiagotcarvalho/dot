---
name: ponytail-review
description: >
  Code review focused exclusively on over-engineering. Finds what to delete:
  reinvented standard library, unneeded dependencies, speculative abstractions,
  dead flexibility. One line per finding: location, what to cut, what replaces
  it. Use when the user says "review for over-engineering", "what can we
  delete", "is this over-engineered", "simplify review", or invokes
  /ponytail-review. Complements correctness-focused review, this one only
  hunts complexity.
---

Review diffs for unnecessary complexity. One line per finding: location, what
to cut, what replaces it. The diff's best outcome is getting shorter.

## Format

`L<line>: <tag> <what>. <replacement>.`, or `<file>:L<line>: ...` for
multi-file diffs. Write `<what>` and `<replacement>` as complete sentences.

Tags:

- `delete:` dead code, unused flexibility, speculative feature. Replacement: nothing.
- `stdlib:` hand-rolled thing the standard library ships. Name the function.
- `native:` dependency or code doing what the platform already does. Name the feature.
- `yagni:` abstraction with one implementation, config nobody sets, layer with one caller.
- `shrink:` same logic, fewer lines. Show the shorter form.

## Examples

❌ "This EmailValidator class might be more complex than necessary, have you
considered whether all these validation rules are needed at this stage?"

✅ `L12-38: stdlib: The 27-line validator class repeats a one-line check. Use "@" in email. Let the confirmation mail do the real validation.`

✅ `L4: native: The code imports moment.js for one format call. Use Intl.DateTimeFormat, which needs no dependency.`

✅ `repo.py:L88: yagni: AbstractRepository has one implementation. Inline it until a second one exists.`

✅ `L52-71: delete: The retry wrapper wraps an idempotent local call. Delete it, because nothing needs to replace it.`

✅ `L30-44: shrink: A manual loop builds the dict. Use dict(zip(keys, values)), which is one line.`

## Scoring

End with the only metric that matters, as one sentence: `The fixes can remove <N> lines.`

If there is nothing to cut, say `This review found no code to cut.` and stop.

## Boundaries

Scope: over-engineering and complexity only. Correctness bugs, security holes,
and performance are explicitly out of scope. Route them to a normal review
pass, not this one. A single smoke test or `assert`-based
self-check is the ponytail minimum, not bloat, never flag it for deletion.
Does not apply the fixes, only lists them.
"stop ponytail-review" or "normal mode": revert to verbose review style.
