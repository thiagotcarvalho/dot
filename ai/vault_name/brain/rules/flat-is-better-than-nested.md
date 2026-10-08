---
type: rule
tags: [python, workflow, architecture]
repo: none
created: 2026-09-10
---
# Flat Is Better Than Nested

> Use a maximum of 1 to 2 levels of nesting in one function. If the code goes deeper, refactor it.

## The Rule

Each level of nesting adds a condition the reader must hold in their head. At three or more levels, the real logic hides inside a pyramid of `if` and `for` blocks. Keep the body of a function flat. Read [Elements of Python Style: Flat is better than nested](https://github.com/amontalenti/elements-of-python-style#flat-is-better-than-nested) for the source.

Bad (deeply nested):

```python
def process_data(response):
    if response:
        if response.get("status") == "success":
            if response.get("data"):
                return len(response["data"])
```

Good (flat):

```python
def process_data(response):
    if not response or response.get("status") != "success":
        return None

    data = response.get("data")
    return len(data) if data else None
```

## How to Apply

- Return early. Test each failure condition first and return, so the main path stays at the top level.
- Use guard clauses to reject bad input at the start of the function.
- Combine related conditions with `and` or `or` instead of one `if` block inside another.
- Invert a condition to remove one level: `if not x: return` replaces `if x:` around the whole body.
- Extract a nested block into a named helper function. The helper starts a fresh nesting budget.
- For a nested loop, extract the inner loop into a helper, or use a comprehension or `itertools`.

## When NOT to Apply

- Essential structure counts. A `try`/`except` inside an `if`, or a `with` block, is one honest level; do not hide it to win a count.
- A comprehension carries its own nesting. Two `for` clauses in one comprehension read worse than a plain loop; prefer the loop.
- Do not trade depth for a long, unreadable boolean. If a guard needs five clauses, name it as a helper that returns a bool.

## Red Flags

- The main logic sits three or more indents deep.
- A function ends with a tall stack of closing blocks and no early return.
- An `if` block wraps the whole function body, and the `else` is empty or missing.
- You scroll right to read the real work.

## Related

[keep-it-simple-stupid](keep-it-simple-stupid.md) · [code-style](code-style.md) · [state-the-problem](state-the-problem.md)
