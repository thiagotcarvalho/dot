---
type: rule
tags: [architecture, python]
repo: none
created: 2026-10-01
---
# SOLID: Five Principles of Object-Oriented Design

> SOLID names five object-oriented design principles by Robert C. Martin. They keep software easy to maintain and extend as a project grows. ([DigitalOcean: SOLID, the first five principles of object-oriented design](https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design))

## The Rule

| Principle | Statement |
| --- | --- |
| **S**: Single responsibility | A class has one reason to change, so it has one job. |
| **O**: Open-closed | An entity is open for extension and closed for modification. |
| **L**: Liskov substitution | Each subtype can replace its base type without breaking the program. |
| **I**: Interface segregation | No client depends on methods that it does not use. |
| **D**: Dependency inversion | High-level and low-level modules both depend on abstractions. |

The principles apply to modules and functions too, not only to classes.

SOLID and [you-arent-gonna-need-it](you-arent-gonna-need-it.md) work together. YAGNI decides what to build. SOLID decides how to build it well, so that nobody has to build it twice.

## How to Apply

- **Single responsibility.** Ask what would make this module change. If two independent answers exist, split the module. A function that computes a result and also writes it has two reasons to change. Keep the computation pure. Do the write in the caller.
- **Open-closed.** Put the parts that change often in data, not in code. An `if` chain that grows with each new case is a warning. Ask whether a table, a registry, or a published rule can hold the cases.
- **Liskov substitution.** Write one contract test for each port. Run it against each adapter, including the fakes. A substitute that passes in memory but fails on the real dependency breaks the contract. Prefer composition to inheritance, because a subclass inherits obligations that it can silently break.
- **Interface segregation.** Keep each port small, and name it for its client. A read port and a write port are two ports, so that a reader cannot write.
- **Dependency inversion.** At an I/O boundary that a test fake or a second adapter replaces, the domain calls a port. In Python, a port is a `typing.Protocol` or an abstract base class. Choose the concrete adapter in one place, the composition root.

## When NOT to Apply

- **One implementation needs no interface.** An interface with a single implementation adds a layer and no choice. Add the port when a second adapter or a test fake needs it.
- **Two similar cases are not yet an abstraction.** Wait for the third case, per [dont-repeat-yourself](dont-repeat-yourself.md).
- **Prefer the replaceable option to the general one.** A small module that is easy to delete is better than a framework that is easy to extend.
- **Do not split one responsibility.** Classes that always change together hold one responsibility. Keep them together.

## Red Flags

- An `if`/`elif` chain on a type or a code grows with each new case.
- A subclass overrides a method only to raise `NotImplementedError`, or it returns a different shape.
- A port has methods that some of its clients never call.
- A test must patch a database driver to reach the business logic.
- A generic class name hides two jobs. [keep-it-simple-stupid](keep-it-simple-stupid.md) lists the usual names.

## Why

The user wanted this rule on 2026-10-01 because work that is done right once is not a waste of time.

## Related

[keep-it-simple-stupid](keep-it-simple-stupid.md) · [you-arent-gonna-need-it](you-arent-gonna-need-it.md) · [dont-repeat-yourself](dont-repeat-yourself.md) · [flat-is-better-than-nested](flat-is-better-than-nested.md) · [code-style](code-style.md) · [guarded-writes](guarded-writes.md)
