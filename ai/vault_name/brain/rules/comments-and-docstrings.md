---
type: rule
tags: [python, workflow]
repo: none
created: 2026-08-05
---
# Comments and Docstrings

Follow the [Google Python style guide §3.8](https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings), biased hard toward minimal: comments and docstrings only when absolutely necessary. The nine rules below come from [Stack Overflow's best practices for writing code comments](https://stackoverflow.blog/2021/12/23/best-practices-for-writing-code-comments/) and are the working checklist; the default above is what decides whether a comment gets written at all.

## The Default: Write Fewer Comments

- Default to **no** docstring or comment. Add one only when a reader could not infer it from the name and signature, or the logic is genuinely subtle.
- Docstrings only for public API, nontrivial, or non-obvious logic. Omit them for short, obvious, or private functions where the name and signature already say it.
- Comments explain **why**. They never narrate what the code does.
- Keep domain-rule docstrings. Cut boilerplate and obvious ones.

## The Nine Rules

1. **Comments should not duplicate the code.** A comment that restates the line it sits above is the failure mode to watch for; it is pure noise and it rots the moment the line changes.
2. **Good comments do not excuse unclear code.** If a comment exists to make a confusing name or a tangled branch survivable, rename or restructure instead. A comment is not a patch for bad code.
3. **If you cannot write a clear comment, there may be a problem with the code.** Difficulty explaining a piece of logic is a design signal, not a writing problem. Treat it as a prompt to simplify.
4. **Comments should dispel confusion, not cause it.** A comment that needs its own explanation, or that hedges instead of stating, is worse than silence. If it does not make the code clearer to someone reading it cold, delete it.
5. **Explain unidiomatic code in comments.** This is the case where a comment is close to mandatory: when correct code looks wrong, say why it is written that way, so the next reader does not "fix" it. Ordering that matters, a deliberate non-obvious comparison, a guard that exists for one specific input.
6. **Provide links to the original source of copied code.** Copied or closely adapted code carries a link to where it came from.
7. **Include links to external references where they will be most helpful.** A specification, an RFC, a vendor quirk, an algorithm write-up: link it at the line that depends on it. See [Two Places These Meet a Standing Constraint](#two-places-these-meet-a-standing-constraint) for what counts as external.
8. **Add comments when fixing bugs.** A non-obvious fix leaves behind why the guard or the ordering exists, stated as a property of the code. Not the ticket, not the incident, not who found it.
9. **Use comments to mark incomplete implementations.** Narrowed: mark a **decided** limitation, never an **open question**. See [Two Places These Meet a Standing Constraint](#two-places-these-meet-a-standing-constraint).

## Two Places These Meet a Standing Constraint

Two hard constraints (stated 2026-07-27) govern where rules 6, 7, 8, and 9 land. Where they conflict, the constraints win; they are narrower and they were set with a reason.

**Internal references are barred, external technical references are not.** No open-question IDs (`OQ-xx`), catalog refs, plan phases (`B6`, `Phase D`), PR or ticket numbers, people's names, or "per the docs/review/decision". Those make the code depend on a document to be legible, and the document moves. Rules 6 and 7 survive intact for things that are stable, public, and explain the code on their own terms: a spec section, a vendor bug report, the upstream source of copied code, an algorithm reference. The test is whether a reader outside this project could follow the link and learn why the code is that way. Rationale and history belong in the spine plan or the PR description.

**A marker records a decided limitation, not an unresolved one.** No "scoping undecided", "not yet what to replace", "until then", "TBD", "for now (Qxx)". If there is no clarity, do not implement it until there is, or implement something basic; uncertainty is handled by the implementation choice, not annotated in a comment.

Rule 9 therefore applies only to a limitation already decided, where the ceiling is known and stated: a global lock instead of per-key locks, an O(n²) scan that is fine at current sizes, a naive heuristic. Name the ceiling and the upgrade path, in the shape ponytail already uses (`# ponytail: This code uses one global lock. Use per-account locks if throughput matters.`). A comment saying "this is unresolved" is noise; a comment saying "this is bounded, here is the bound" is information.

## Three Shapes the Nine Rules Do Not Name

The nine rules cover the comments that restate code and the comments that explain it. They do not name three shapes that antirez identifies in [Writing system software: code comments](https://antirez.com/news/124). Each shape is permitted. Each one inherits a constraint that this file already states.

- **Design comment.** A note at the top of a file that states the chosen approach and the alternatives that lost. It inherits the internal-reference ban. Restate the reasoning inline. Do not cite a plan, a ticket, or a review. [vault-is-not-a-repo](vault-is-not-a-repo.md) gives the same instruction in its outbound form.
- **Teacher comment.** A note that explains the domain the code operates in, for a reader without that background. It inherits rule 7. It earns its place when it teaches something stable and public, such as the trigonometry behind a rotation.
- **Checklist comment.** A note that names the other site which must change together with this one. It inherits the [dont-repeat-yourself](dont-repeat-yourself.md) clause on layer boundaries. That clause already requires the code to name where the authoritative version lives.

The same article defends a fourth shape, the guide comment, which rule 1 bars. That defense rests on C and on long functions, so it does not carry here.

## Style

When a docstring summary is warranted, write it as a single plain sentence. Do not use the "Name: clause, clause" colon style. Avoid "CLI entry point: `scan` triggers a workflow, `worker` runs the host"; prefer "Command-line entry point for running a scan or the worker that hosts it."

## Why

The user wanted this rule because earlier code had wordy docstrings and comments that restated the code on 2026-07-09. The two hard constraints followed comments that carried open-question IDs and "undecided" notes on 2026-07-27.

## Related

[writing-style](writing-style.md) · [keep-it-simple-stupid](keep-it-simple-stupid.md) · [dont-repeat-yourself](dont-repeat-yourself.md)
