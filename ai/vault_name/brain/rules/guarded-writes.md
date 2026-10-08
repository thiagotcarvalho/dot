---
type: rule
tags: [sql-server, architecture]
repo: none
created: 2026-10-01
---
# Guarded Writes to a System of Record

A system of record is the database that the business runs on. This rule covers code that changes existing records in a system of record. Code that creates new records follows the rules of its own repo.

## The Rules

1. **Dry run is the default.** A live write happens only when the caller gives an explicit opt-in. It never happens implicitly.
2. **Write only a change that the code can prove exactly.** Any other change is a proposal for a person.
3. **One review finding stops every automatic write to its target.** When one finding on a record needs review, the other findings on that record also go to review. Their proposals stay visible.
4. **Resolve the target from authoritative data.** Exactly one row is the only acceptable result. Zero rows or two rows stop the write. Never infer the target from a name, a prefix, or a location.
5. **Read the concurrency token from the database that you write.** A `rowversion` from a replica does not protect a write to the source server, because `rowversion` is per database.
6. **Protected text stays.** When people mark a phrase as protected, no rule clears it or writes over it.
7. **Leave an audit record for each write.** The record names the service account and identifies the write, so that a person can trace the write.
8. **A report-only mode writes nothing to the system of record.** It observes and proposes. A person approves, and only the write path applies the change.

## When NOT to Apply

- **Do not guard against the authoritative source.** The upstream selection decides what enters the write path. A downstream guard that contradicts it needs evidence first.
- **Do not put a check in the schema that only our own bug can trip.** That check belongs in a unit test.

## How to Apply

Read these guards before you change a write path. In the plan, name each guard that the change touches. A change that removes or weakens a guard needs the user's decision first. Prove each write with a read-back, per [prove-it-where-it-runs](prove-it-where-it-runs.md).

## Related

[explicit-go-for-outward-actions](explicit-go-for-outward-actions.md) · [prove-it-where-it-runs](prove-it-where-it-runs.md) · [keep-it-simple-stupid](keep-it-simple-stupid.md)
