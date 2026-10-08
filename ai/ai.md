# AI Agent Setup

This file lists my AI coding agents, with their config files, skills, rules, and notes vault.

This folder holds only the files that I wrote or changed. A link points to each tool, skill, and plugin that I installed without a change. A config file name below links to its copy in this folder. The path after it is where the file lives locally.

## herdr

[website](https://herdr.dev/)

herdr is a terminal workspace. Each agent runs in its own herdr pane.

[config.toml](herdr/config.toml): `~/.config/herdr/config.toml`

- The prefix key is `ctrl+a`. The plugin keys are below.

`herdr integration install claude`, `herdr integration install codex`, and `herdr integration install omp` add the herdr hooks. The Claude Code and Codex hooks report the session of each agent to its pane. The omp extension also reports the working, blocked, and idle state. herdr manages these files, so this folder does not copy them:

- `~/.claude/hooks/herdr-agent-state.sh`
- `~/.codex/hooks.json` and `~/.codex/herdr-agent-state.sh`
- `~/.omp/agent/extensions/herdr-omp-agent-state.ts`

### herdr Plugins

[herdr-file-viewer](https://github.com/smarzban/herdr-file-viewer)

- `prefix+f` opens it in a split. `prefix+shift+f` opens it in a tab.

[herdr-reviewr](https://github.com/persiyanov/herdr-reviewr)

- `prefix+r` toggles it.

[herdr-plugin-manager](https://github.com/speardragon/herdr-plugin-manager)

- `prefix+m` opens it.

## omp

[website](https://omp.sh/)

omp is the main coding agent. It uses Claude models and Codex models in different roles.

[config.yml](omp/config.yml): `~/.omp/agent/config.yml`

- Opus 5.5 is the `default` and `plan` model. Sonnet 5.5 is the `vision` and `designer` model. GPT-6 models from Codex do the `task`, `advisor`, `smol`, and `slow` roles.
- The `scout` and `sonic` subagents and the `judge` role use Claude Haiku 5.5.
- The config tells omp to continue the work on the other provider when one provider reaches its usage limit.
- The config tells omp to spend a saved Claude or Codex reset automatically.

>Roles are subject to change.

### omp Plugins

[superpowers](https://github.com/obra/superpowers)

## Claude Code

[repo](https://github.com/anthropics/claude-code)

[settings.json](claude/settings.json): `~/.claude/settings.json`

- It sets the model, the status line, the plugins, the ASD-STE100 output style, and the herdr session hook. It also turns off some installed skills for Claude Code.

[CLAUDE.md](claude/CLAUDE.md): `~/Developer/CLAUDE.md`

- This file holds the global instructions: the repo boundary, the pointer to the vault, and the ASD-STE100 language standard. `~/.claude/CLAUDE.md` is a link to it.

[ASD-STE100.md](claude/output-styles/ASD-STE100.md): `~/.claude/output-styles/ASD-STE100.md`

- This output style applies the language standard.

### Claude Code Plugins

[claude-hud](https://github.com/jarrodwatts/claude-hud)

- It draws the status line.

[superpowers](https://github.com/obra/superpowers)

## Codex

[repo](https://github.com/openai/codex)

[config.toml](codex/config.toml): `~/.codex/config.toml`

- It sets the model and the plugins. The local file also holds app paths, project trust entries, and a hook trust hash. This copy leaves them out.

[AGENTS.md](codex/AGENTS.md): `~/.codex/AGENTS.md`

- This file holds the global instructions: the pointer to the vault and the ASD-STE100 language standard.

[default.rules](codex/rules/default.rules): `~/.codex/rules/default.rules`

- This file lists the commands that Codex runs without a prompt.

## Obsidian Vault

[vault_name](vault_name/AGENTS.md): `~/Developer/vault_name`

- The vault holds the instructions that all agents follow. Replace `vault_name` with the name of your vault.

The vault has three parts. The [frankenstein](skills/frankenstein/SKILL.md) skill loads all three at the start of a session.

[brain](vault_name/brain/README.md)

- The brain holds the rules and the memory index. Its README lists each rule.

[spine](vault_name/spine/README.md)

- The spine holds the work-product: plans, discovery notes, and runbooks. Its README gives the layout.

[arms](vault_name/arms/task-queue/README.md)

- The arms hold one task file for each unit of work, in `Now`, `Next`, `Waiting`, and `Done`.

These copies are generic. My notes, my memory files, and my tasks stay private. The copies use relative Markdown links, so GitHub can show them. Obsidian opens the linked notes too.

[AGENTS.md](agents/AGENTS.md): `~/.agents/AGENTS.md`

- This file points any other agent tool at the vault.

## Skills

All agents read the skills in `~/.agents/skills/`. Claude Code reads them through links in `~/.claude/skills/`.

### My Skills

[adversarial-code-review](skills/adversarial-code-review/SKILL.md)

- A second agent reviews local changes, read-only, in a herdr pane.

[frankenstein](skills/frankenstein/SKILL.md)

- It loads the vault: the brain, the spine, and the arms.

### Altered Skills

[ponytail](skills/ponytail/SKILL.md), [ponytail-audit](skills/ponytail-audit/SKILL.md), [ponytail-debt](skills/ponytail-debt/SKILL.md), [ponytail-review](skills/ponytail-review/SKILL.md)

- These are trimmed copies of [ponytail](https://github.com/DietrichGebert/ponytail) by DietrichGebert, under the [MIT license](skills/licenses/ponytail-LICENSE.txt).

[improve-codebase-architecture](skills/improve-codebase-architecture/SKILL.md)

- This is a copy of the skill from [mattpocock/skills](https://github.com/mattpocock/skills) by Matt Pocock, under the [MIT license](skills/licenses/mattpocock-skills-LICENSE.txt).

[review-python-code](skills/review-python-code/SKILL.md)

- It adapts `python-code-review` and `review-verification-protocol` from [beagle](https://github.com/existential-birds/beagle) by Existential Birds, LLC, under the [Apache-2.0 license](skills/licenses/beagle-LICENSE.txt). I changed it to follow my house rules.

### Installed Skills

I installed these skills without a change, before the [skills-are-tools](vault_name/brain/rules/skills-are-tools.md) rule. A new install follows that rule.

[mattpocock/skills](https://github.com/mattpocock/skills)

- diagnose, grill-me, handoff, prototype, tdd, teach, write-a-skill, zoom-out

[vercel-labs/skills](https://github.com/vercel-labs/skills)

- find-skills

[herdrdev/herdr](https://github.com/herdrdev/herdr)

- herdr

[fireworks-tech-graph](https://github.com/yizhiyanhua-ai/fireworks-tech-graph)

- It is a git clone in `~/.local/share/agent-skills/`, with a link in `~/.agents/skills/`.
