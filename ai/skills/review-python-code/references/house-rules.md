# House Rules

`~/Developer/vault_name/brain/rules/` holds the authoritative version of everything below. This file restates the substance, so a reviewer needs no second file. When the two disagree, the rules win, and this file needs an update. The [review-names-and-comments](../../review-names-and-comments/SKILL.md) skill covers names, comments, docstrings, and tests.

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
