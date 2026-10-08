# dot

This repo holds my config files and lists the apps that I use every day.

## Categories

| Category | What it Holds |
| --- | --- |
| [ai](ai/ai.md) | The doc lists my AI coding agents (omp, Claude Code, and Codex) and the herdr terminal workspace. The folder holds their config files, my skills and rules, and a template of an Obsidian vault. |
| [cursor](cursor/cursor.md) | The folder holds the settings of Cursor, my code editor. The doc links to my extensions. |
| [macos](macos/macos.md) | The doc lists the macOS apps that I use every day, and some alternatives to them. |
| [shell](shell/shell.md) | The folder holds the config files of zsh, powerlevel10k, tmux, Ghostty, and LazyVim. The doc also lists oh-my-zsh and command-line tools such as bat, eza, fzf, and zoxide. |

## How the Categories Work

Each category has one doc, `<category>/<category>.md`. The doc lists the tools of the category.

- A category holds only the files that I wrote or changed. It also holds the other files of a changed skill and the license texts of copied work. A tool that I installed without a change gets a link only.
- The doc links to each config file that I copied. The path after the link is the local path of the file.
- The category doc credits the creator of each copy of someone else's work. The license texts are in `shell/licenses/` and `ai/skills/licenses/`.
- The repo is public. The copies hold no secret, no home path, and no name of a company that I work for or with.

Follow these steps to set up a new machine:

1. Install the tools that the category docs link.
2. Copy each file to the local path that its category doc gives.
3. In the `ai` files, replace `vault_name` with the name of your vault.
