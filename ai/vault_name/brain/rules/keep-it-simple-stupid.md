---
type: rule
tags: [workflow, architecture]
repo: none
created: 2026-06-10
---
# KISS: Keep It Simple, Stupid

> The simplest design that solves the actual problem wins. Complexity must earn its place.

## The Rule

Given two solutions that both work, choose the one that is easier to read, debug, and delete. Cleverness is a cost: every layer of indirection, every pattern, every configuration option is something the next reader (often future you, often an AI agent) must load into their head before they can touch the code.

## How to Apply

- Prefer a plain function over a class, a class over a hierarchy, a hierarchy over a framework.
- Prefer boring, idiomatic constructs over clever one-liners. Code is read far more than written.
- Reach for the standard library before adding a dependency; add a dependency before writing your own version of a hard thing (dates, crypto, parsing).
- [flat-is-better-than-nested](flat-is-better-than-nested.md): early returns over deep `if` pyramids, data pipelines over tangled state.
- If you can't explain the design in two sentences, it's probably too complicated.

## When NOT to Apply

- Simple ≠ simplistic. Don't ignore real requirements (error handling, edge cases, security) to keep code short; that just moves complexity onto the user or operator.
- Essential complexity belongs in the code. KISS targets **accidental** complexity: the parts the problem didn't ask for.

## Red Flags

- "This abstraction will make it flexible." (See [you-arent-gonna-need-it](you-arent-gonna-need-it.md).)
- A design that needs a diagram to explain a CRUD operation.
- Generic names like `Manager`, `Processor`, `Handler`, `AbstractFactory` are usually a sign the thing has no single clear job.
- You're proud of how clever it is.

## Related

[you-arent-gonna-need-it](you-arent-gonna-need-it.md) · [dont-repeat-yourself](dont-repeat-yourself.md) · [state-the-problem](state-the-problem.md) · [flat-is-better-than-nested](flat-is-better-than-nested.md) · [solid-principles](solid-principles.md)
