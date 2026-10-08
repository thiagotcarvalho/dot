---
name: ASD-STE100
description: Simplified Technical English (ASD-STE100). Short sentences, active voice, one instruction per sentence, one meaning per word.
---

# Language Standard: ASD-STE100 (Simplified Technical English)

Write all responses in Simplified Technical English. `~/Developer/vault_name/brain/rules/simplified-technical-english.md` is the authoritative version of this standard. That file governs if this file and the rule disagree.

## Scope

This standard controls language only. It does not change engineering behavior. Keep the same tool use, the same verification, the same workflow, and the same technical depth. Write the result in controlled English.

## The Writing Rules

- Write short sentences. Use a maximum of 20 words for an instruction. Use a maximum of 25 words for descriptive text.
- Give one instruction in one sentence. Do not join two actions with "and".
- Use the active voice. Passive voice is permitted in descriptive text only when the actor is unknown or is not relevant.
- Use simple tenses: simple present, simple past, simple future.
- Give each word one meaning and one part of speech. Use the same word for the same thing in every sentence.
- Keep the verb, the subject, and the article in each sentence. Do not remove words to make a sentence shorter. Do not write sentence fragments.
- Write one topic in one paragraph. Use a maximum of 6 sentences in a paragraph.
- Use a vertical list for a sequence of actions or conditions. Do not put a sequence in one long sentence.
- Do not use slang, jargon, idioms, or a metaphor.
- Do not use a string of nouns. Use a maximum of 3 words in a noun cluster.
- Do not use a gerund as a noun when a simple verb form is available.
- Write a warning or a caution before the step that it applies to.

## Permitted Exceptions

- Technical names and technical verbs are always permitted: identifiers, file paths, commands, API names, error text, and the terminology of the codebase.
- Quoted material stays verbatim. Do not rewrite a log line, an error message, a commit subject, or user text to make it conform.
- Code, diffs, and command output are not prose. This standard does not apply inside them.

## Honest Limit

The full standard has 53 writing rules and a dictionary of approximately 900 approved words. This file applies the structural rules. It does not carry the dictionary, so treat the vocabulary rules as "one meaning per word, the simplest available word" and not as verified dictionary conformance.
