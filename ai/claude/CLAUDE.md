# CLAUDE.md

`~/Developer` is the parent folder for all of the user's repos. It is **not** a git repository;
each repo under it is an independent git project with its own conventions.

**Do not modify any repo under `~/Developer/` unless the user explicitly tells you to.**

My workspace is the Obsidian vault at `~/Developer/vault_name`, which holds two things:

- The **brain** (`vault_name/brain/`): how agents behave. Authored standards in `brain/rules/` and learned facts in `brain/memory/`. **Apply the rules in `brain/rules/`** to the relevant work (they are indexed in `brain/README.md`).
- The **spine**: where all my own output lives (plans, architecture, discovery, runbooks), organized by repo and ticket.

`vault_name/AGENTS.md` is the canonical entry point for both, plus code style and workspace conventions. **Read `vault_name/AGENTS.md` first.**

## Language Standard: ASD-STE100

Write every response and every document in Simplified Technical English (ASD-STE100). The authoritative rule is `vault_name/brain/rules/simplified-technical-english.md`. The operative constraints are repeated here on purpose, because a language standard must arrive with the prompt and not one read-hop later:

- Short sentences: a maximum of 20 words for an instruction, 25 for descriptive text.
- One instruction in one sentence. Active voice. Simple tenses.
- One meaning for one word. Use the same word for the same thing every time.
- Complete sentences. Keep the verb, the subject, and the article. No fragments.
- One topic in one paragraph, a maximum of 6 sentences. Use vertical lists for sequences.
- No slang, no idiom, no metaphor. A maximum of 3 words in a noun cluster.

Technical names, file paths, commands, error text, and quoted material keep their exact form. Code, diffs, and command output are not prose, so the rules do not apply inside them. The standard controls language only. It does not change engineering behavior, and it does not reduce technical depth.
