---
type: rule
tags: [workflow, tooling]
repo: none
created: 2026-08-06
---
# Writing Style

How the user wants prose written. The standard applies to chat responses, brain notes, spine notes, and docs for a repo. Writing is not coding: the code-style rules in [code-style](code-style.md) do not govern prose.

## The Rules

- **Fewer line-breaking punctuation.** A single, concise sentence trumps everything else. Use em-dashes, colons, and semicolons sparingly. These punctuation marks are useful to flesh out complex ideas, but at the cost of simplicity.
- **Plain, unsensational tone.** State facts without hype, drama, or sensational metaphors (no "this bites every new Mac"). Warnings are stated, not dramatized.
- **Do not hard-wrap prose.** Write each paragraph as one flowing line and let the editor soft-wrap.
- **A table of contents on every substantial document** (discovery, plan, runbook, PRD) so readers can jump around. Running lists are exempt: `open-questions.md` never carries one. See [the running-docs convention](../../spine/README.md#work-tracking-and-open-questions).
- **Title Case all titles and headings.** Capitalize the first and last words, and all major words (nouns, pronouns, verbs, adjectives, and adverbs). Do not capitalize articles (a, an, the), coordinating conjunctions (and, but, or, nor, for, so, yet), or short prepositions (in, to, for, with, of, on, at, by). Leave code identifiers, file names, and acronyms as written.
- **Let a diagram carry the explanation.** Where a figure shows the mechanism, the prose beside it states only what the figure cannot: why a choice was made, or a fact with no visual form. Do not narrate in text what the reader can see in the picture.
- **Obsidian-flavored section links.** This is an [Obsidian vault](https://obsidian.md/help/obsidian-flavored-markdown): link to a heading with `[[#Heading]]` (same note) or `[[note#Heading]]` (across notes), never standard-Markdown `[text](#anchor)`. Use `[[#Heading|display text]]` when the visible text should differ from the heading. Native links resolve reliably and survive heading edits; `[](#slug)` anchors silently break.

## How to Apply

Apply before the first draft, not after a rejection. These hold even for docs destined for another repo: the user's prose style governs everywhere, while the target repo's own conventions govern structure (source tags, layout).

## Why

The user wanted this rule because agent prose had too many em-dashes, a sensational tone, and hard wraps on 2026-06-10 and 2026-06-22.

## Related

[comments-and-docstrings](comments-and-docstrings.md) · [keep-it-simple-stupid](keep-it-simple-stupid.md) · [simplified-technical-english](simplified-technical-english.md)
