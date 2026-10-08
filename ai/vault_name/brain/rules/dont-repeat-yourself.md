---
type: rule
tags: [workflow, architecture]
repo: none
created: 2026-06-10
---
# DRY: Don't Repeat Yourself

> Every piece of **knowledge** must have a single, unambiguous, authoritative representation within a system. (Andrew Hunt and David Thomas, *The Pragmatic Programmer*)

## The Rule

When the same business rule, constant, schema, or algorithm exists in two places, a change to one will eventually miss the other. Extract it to one place and reference it.

DRY is about **knowledge**, not text. Two functions that happen to contain similar lines are not duplication if they represent different decisions that can change independently.

## How to Apply

- Before copy-pasting a block, ask: *if this logic changes, must both copies change together?* If yes, extract first.
- Single source of truth for: magic numbers, validation rules, config values, type/schema definitions, error messages users see.
- Duplication across layer boundaries (e.g. a rule enforced in both UI and backend) is sometimes necessary. When it is, document where the authoritative version lives.

## When NOT to Apply

- **Incidental similarity.** Code that looks alike today but serves different domains will diverge. Deduplicating it couples things that should evolve separately.
- **Rule of three.** Tolerate the second occurrence; extract on the third, when the real shape of the abstraction is visible. A wrong abstraction is more expensive than duplication.
- **Tests.** Some repetition in tests is fine: readability of a single test in isolation beats DRY test helpers that hide what's being asserted.

## Red Flags

- "I'll just copy this and tweak one line."
- A helper with boolean flags growing to serve callers that were "deduplicated" too early.
- The same constant defined in two files with different values (the bug DRY exists to prevent).

## Related

[keep-it-simple-stupid](keep-it-simple-stupid.md) · [you-arent-gonna-need-it](you-arent-gonna-need-it.md) · [state-the-problem](state-the-problem.md) · [solid-principles](solid-principles.md)
