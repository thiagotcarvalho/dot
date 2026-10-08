---
type: rule
tags: [python, workflow]
repo: none
created: 2026-07-17
---
# Code Style

How agents write code, following the [Google Python style guide](https://google.github.io/styleguide/pyguide.html) for Python. Writing is separate and lives in [writing-style](writing-style.md): these rules govern code, not prose.

## The Rules

[keep-it-simple-stupid](keep-it-simple-stupid.md), [dont-repeat-yourself](dont-repeat-yourself.md), and [you-arent-gonna-need-it](you-arent-gonna-need-it.md) are the cornerstone; apply them first, then:

- Code should be self-documenting. Keep comments minimal and terse; a comment exists only to state what the code cannot. See [comments-and-docstrings](comments-and-docstrings.md).
- No shortened variable names unless absolutely necessary. Names explain the **what**; abbreviations confuse future devs.
- **Short names, not sentences.** A name identifies; it does not explain. `test_duplicate_order_note`, not `test_duplicate_order_note_is_the_discount_rule_alone_while_discount_never_stacks`. This is the counterweight to the rule above: no abbreviations, and no paragraphs either. Where a name cannot carry the reasoning, put one brief sentence in the docstring, which is also the only place that reasoning survives a rename.
- **Names take no articles.** Do not put `a`, `an`, or `the` in a variable, function, method, or test name. An article adds no information. It makes the name longer. Write `parse_order`, not `parse_the_order`. Write `test_duplicate_order`, not `test_the_duplicate_order`.
- Tests are specific and tackle a single case each. One test must not handle multiple scenarios.
- No comments referencing a specific ticket (e.g. `PROJ-1203`). `git blame` carries that attribution.
- Keep functions flat: a maximum of 1 to 2 levels of nesting. See [flat-is-better-than-nested](flat-is-better-than-nested.md).
- **Compare data text in a normalized form.** Casefold both sides when you compare data: report values, database codes and IDs, and human-entered text. For human-entered text, also collapse each run of whitespace and line breaks to one space. Never compare raw data text directly. Compare code identifiers, hashes, file paths, and secrets exactly. Write and display the raw value. A field can need more tolerance, for example for punctuation, and that is a decision for the field.
- When a repo enforces its own line length via an auto-formatter (e.g. ruff `line-length` run by `task qa`/CI), defer to that config: the formatter is authoritative on disk.

## Why

The user wanted the text-comparison bullet because a case-sensitive compare silently missed rows on 2026-07-28.

## Related

[keep-it-simple-stupid](keep-it-simple-stupid.md) · [dont-repeat-yourself](dont-repeat-yourself.md) · [you-arent-gonna-need-it](you-arent-gonna-need-it.md) · [flat-is-better-than-nested](flat-is-better-than-nested.md) · [comments-and-docstrings](comments-and-docstrings.md) · [writing-style](writing-style.md)
