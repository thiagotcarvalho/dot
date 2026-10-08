---
type: rule
tags: [workflow, architecture]
repo: none
created: 2026-06-10
---
# YAGNI: You Aren't Gonna Need It

> Build what the current requirement demands. Nothing speculative.

## The Rule

Don't implement functionality, abstraction, or configurability because you *might* need it later. Most predicted needs never materialize, and the ones that do rarely arrive in the shape you guessed. Speculative code is pure cost today (more to read, test, maintain) for a benefit that usually never comes. When the need does arrive, you'll design it better with real requirements in hand.

## How to Apply

- Implement the ticket, not the ticket you imagine coming next quarter.
- One caller? No interface, no plugin system, no strategy pattern. Add the abstraction when the **second** concrete need exists.
- No config options, feature flags, or parameters that nothing currently sets.
- Delete dead code instead of keeping it "in case"; git remembers.
- In plans and PRDs: cut every requirement that starts with "eventually" or "in the future we could" into a separate, deferred note.
- Reuse a pattern from another repo one mechanism at a time. Name the problem that each mechanism solves. Copy a mechanism only when the new system has that problem. State the trigger that would justify each mechanism that you leave out.

## When NOT to Apply

- **Hard-to-reverse decisions.** Data schemas, public APIs, wire formats, and security boundaries are expensive to change later, so spending design effort there is diligence, not speculation.
- YAGNI applies to *building* things, not to *thinking* about them. It's fine to leave a seam ("this function is where pagination would go") as long as the seam costs nothing now.

## Red Flags

- "While I'm in here, I'll also make it support…"
- Generic parameters/`**kwargs` threaded through layers that only one value ever flows through.
- An abstraction layer wrapping a library "so we can swap it out later." (You won't.)
- Test scaffolding for behavior that doesn't exist yet.

## Related

[keep-it-simple-stupid](keep-it-simple-stupid.md) · [dont-repeat-yourself](dont-repeat-yourself.md) · [state-the-problem](state-the-problem.md) · [solid-principles](solid-principles.md)
