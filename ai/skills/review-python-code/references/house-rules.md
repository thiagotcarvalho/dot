# House Rules

`~/Developer/vault_name/brain/rules/` holds the authoritative version of everything below. This file restates the substance, so a reviewer needs no second file. When the two disagree, the rules win, and this file needs an update.

## Names

- **No abbreviation.** A name states the thing. `user_id`, not `uid`. `quantity`, not `qty`.
- **A name is not a sentence.** A name identifies. It does not explain. `test_duplicate_order_rejection_note` is right. A name that carries the whole reason is wrong. Where a name cannot hold the reasoning, put one brief sentence in the docstring.
- Report a name that shadows a builtin, such as `id`, `type`, or `list`.

## Comments

- **The default is no comment.** Add one only when a reader cannot infer the point from the name and the signature, or when the logic is genuinely subtle.
- **A comment states why.** It never narrates what the code does. A comment that restates the line below it is the failure mode to look for. Report it.
- **A comment never repairs unclear code.** When a comment exists to make a confusing name survivable, the fix is the rename.
- **Unidiomatic code earns a comment.** When correct code looks wrong, the reason belongs beside it, so the next reader does not "fix" it. An ordering that matters, a deliberate non-obvious comparison, a guard for one specific input.
- **A copied block carries a link to its source.** A specification, an RFC, or a vendor bug report belongs at the line that depends on it.

## Comments That Must Not Ship

- **No internal reference.** No ticket number, no PR number, no plan phase such as `B6` or `Phase D`, no catalog identifier, no person's name, and no phrase such as "per the review" or "per the decision". Each one makes the code depend on a document to be legible, and the document moves. `git blame` carries attribution. Report every occurrence.
- **A marker records a decided limitation, never an open question.** No "TBD", no "scoping undecided", no "for now". A marker names a known ceiling and its upgrade path, in this shape:

```python
# ponytail: global lock, per-account locks if throughput matters
```

  A comment that says the design is unresolved is noise. Report it.

## Docstrings

- **Public, nontrivial, or non-obvious only.** Omit the docstring on a short, obvious, or private function where the name and the signature already say it.
- **A summary is one plain sentence.** Never the "Name: clause, clause" colon style. Write "Command-line entry point for running a scan or the worker that hosts it." Never "CLI entry point: `scan` triggers a workflow, `worker` runs the host".
- A full `Args:` / `Returns:` / `Raises:` block is correct on a public API with non-obvious behaviour. On a two-line helper it is noise. Report the noise, not the absence.

## Tests

- **One test covers one case.** A test that exercises several scenarios hides which one failed. Report it.
- Repetition inside tests is acceptable. A shared helper that hides the assertion is worse than the repetition.

## Duplicated Knowledge

- A business rule, a constant, a schema, or an algorithm belongs in one place. Report a second copy that must change together with the first.
- **Incidental similarity is not duplication.** Two blocks that look alike but serve different decisions will diverge. Never ask for a shared helper there.
- **Tolerate the second occurrence.** Ask for the extraction on the third, when the real shape is visible. A wrong abstraction costs more than the duplication.

## Logging Safety

Report a violation as Critical. A sensitive field is a credential, a token, a personal identifier, or any field that the project marks as sensitive.

- **Never log a sensitive field.** A log line may carry an internal identifier, a count, a status code, or a duration.
- **Report a whole-object log.** `logger.info("payload=%s", payload)` sends every field, including the sensitive fields. Ask for the named fields instead.
- A message built for an exception follows the same rule. See [error-handling.md](error-handling.md).

## Message Construction

- Use an f-string to build a plain string.
- Use the logger's own placeholders for a log call when the module uses the standard library `logging`. `logger.info("processing %s", order_id)` defers the formatting until a handler needs it.
- When the module uses a logger that formats eagerly, an f-string in the call is idiomatic. Match the module. Never report the style the module already uses consistently.

## Out of Scope

Indentation, line length, blank lines, bracket whitespace, operator spacing, and import order all belong to the formatter. The formatter is authoritative on disk. Never report any of them.
