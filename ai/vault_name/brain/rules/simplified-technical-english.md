---
type: rule
tags: [workflow]
repo: none
created: 2026-08-14
---
# Simplified Technical English (ASD-STE100)

Every AI agent writes in Simplified Technical English (ASD-STE100). This applies to chat responses, to [spine](../../spine/README.md) documents, to code comments, to commit subjects, and to any prose an agent produces. This rule is the authoritative version of the standard for all tools.

## The Rules

- **Short sentences.** A maximum of 20 words for an instruction. A maximum of 25 words for descriptive text.
- **One instruction in one sentence.** Do not join two actions with "and".
- **Active voice.** Passive voice is permitted in descriptive text only when the actor is unknown or is not relevant.
- **Simple tenses only:** simple present, simple past, simple future.
- **One meaning for one word.** Use the same word for the same thing every time. Do not use a synonym for variety.
- **Complete sentences.** Keep the verb, the subject, and the article. Do not remove words to make a sentence shorter. A fragment is not permitted, because it creates ambiguity.
- **One topic in one paragraph.** A maximum of 6 sentences.
- **Vertical lists for sequences.** Do not put a sequence of actions in one long sentence.
- **No slang, no idiom, no metaphor, no jargon.**
- **A maximum of 3 words in a noun cluster.** Long noun strings hide the relationship between the words.
- **A warning comes before the step that it applies to.**

Technical names and technical verbs are always permitted. Identifiers, file paths, commands, API names, and error text keep their exact form. Quoted material stays verbatim: do not rewrite a log line, an error message, or the user's own words to make them conform. Code, diffs, and command output are not prose, so the rules do not apply inside them.

## How to Apply

Apply the standard to the first draft. Do not write normal English and then convert it.

This standard controls language. It does not control engineering behavior, and it does not reduce technical depth. The facts, the evidence, and the verification stay complete. Only the sentences change.

[writing-style](writing-style.md) stays in force and controls a different layer: tone, em-dashes, hard wrapping, Title Case headings, and the table of contents. The two layers seldom meet. If they disagree on sentence structure, ASD-STE100 wins. If a tool or a default permits a sentence fragment, ASD-STE100 still forbids it. [code-style](code-style.md) and [comments-and-docstrings](comments-and-docstrings.md) control code, and this rule controls the English inside a comment.

The vocabulary limit is honest and stated: the standard has 53 writing rules and a dictionary of approximately 900 approved words ([edition of January 2025](https://en.wikipedia.org/wiki/Simplified_Technical_English)). The brain carries the structural rules, not the dictionary. Apply "one meaning per word, the simplest available word". Do not claim verified dictionary conformance.

## Per-Tool Adapters

The rule text is the single source. Each tool gets a pointer, not a copy. See [How tools load the brain](../README.md#how-tools-load-the-brain) for the current adapter list.

## Why

The user wanted this rule on 2026-08-13 because the ASD-STE100 output style reached only Claude Code, and the user wanted it in every AI agent.

## Related

[writing-style](writing-style.md) · [comments-and-docstrings](comments-and-docstrings.md) · [vault-is-not-a-repo](vault-is-not-a-repo.md)
