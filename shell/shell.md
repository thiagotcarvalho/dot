# Shell Configs and Tools

This file lists my shell tools, with their config files.

This folder holds only the files that I wrote or changed. A link points to each tool that I installed without a change. A config file name below links to its copy in this folder. The path after it is where the file lives locally.

## bat

[repo](https://github.com/sharkdp/bat)

bat shows the contents of a file with syntax highlighting.

- `.zshrc` makes `cat` an alias for bat.

## eza

[repo](https://github.com/eza-community/eza)

eza lists files and folders in place of `ls`.

- `.zshrc` makes `ls` an alias for `eza -lao --header --icons`.

## fastfetch

[repo](https://github.com/fastfetch-cli/fastfetch)

fastfetch shows the system information in the terminal.

## fzf

[website](https://junegunn.github.io/fzf/)

fzf is a fuzzy finder for the command line.

## Ghostty

[website](https://ghostty.org/)

Ghostty is the terminal app that runs the shell.

[config.ghostty](ghostty/config.ghostty): `~/Library/Application Support/com.mitchellh.ghostty/config.ghostty`

- It sets the Japanesque theme.

## Homebrew

[website](https://brew.sh/)

Homebrew is the package manager that installs most of the tools in this file.

- `.zprofile` adds Homebrew to the `PATH` with `brew shellenv`. `.zshrc` loads powerlevel10k, zsh-autosuggestions, and zsh-syntax-highlighting from the Homebrew folder.
- The [Brewfile](../macos/Brewfile) lists the tools that Homebrew installs. The Homebrew section of [macos.md](../macos/macos.md) explains how to run the Brewfile.

## lazyvim

[website](https://www.lazyvim.org/)

LazyVim is a neovim setup with a set of plugins. I installed it from the [LazyVim starter](https://github.com/LazyVim/starter) by folke. I added or changed only the two files below. lazy.nvim also writes `lazy-lock.json`, a lock file that this folder leaves out.

[lazyvim.json](lazyvim/lazyvim.json): `~/.config/nvim/lazyvim.json`

- It lists the LazyVim extras that I turned on.

[disable-markdown-lint.lua](lazyvim/lua/plugins/disable-markdown-lint.lua): `~/.config/nvim/lua/plugins/disable-markdown-lint.lua`

- It turns off the Markdown linter and keeps the rest of the Markdown extra.

## neovim

[website](https://neovim.io/)

neovim is the text editor in the terminal. My setup is LazyVim.

## oh-my-zsh

[website](https://ohmyz.sh/)

oh-my-zsh is a framework for the zsh configuration.

- `.zshrc` loads it with the `git` plugin.

## powerlevel10k

[repo](https://github.com/romkatv/powerlevel10k)

powerlevel10k is the zsh prompt theme. Homebrew installs it, and `.zshrc` loads it.

[.p10k.zsh](powerlevel10k/.p10k.zsh): `~/.p10k.zsh`

- The `p10k configure` wizard wrote this file from the [`pure` style template](https://github.com/romkatv/powerlevel10k/blob/master/config/p10k-pure.zsh). The template is by Roman Perepelitsa and contributors, under the [MIT license](licenses/powerlevel10k-LICENSE.txt).

## tmux

[repo](https://github.com/tmux/tmux/wiki)

tmux is a terminal multiplexer.

[.tmux.conf](tmux/.tmux.conf): `~/.tmux.conf`

- The prefix key is `ctrl+a`. The [herdr](https://herdr.dev/) prefix key is also `ctrl+a`. The mouse is on.
- The file needs tmux 3.6 or later.

## zoxide

[repo](https://github.com/ajeetdsouza/zoxide)

zoxide replaces `cd`. It remembers the folders that I use most.

- `.zshrc` starts zoxide as the `cd` command.

## zsh

[website](https://www.zsh.org/)

zsh is the default shell on macOS.

[.zshrc](zsh/.zshrc): `~/.zshrc`

- It loads oh-my-zsh, powerlevel10k, and the two zsh plugins below. It also sets the aliases, [pyenv](https://github.com/pyenv/pyenv), and zoxide.
- It is a changed copy of the [oh-my-zsh template](https://github.com/ohmyzsh/ohmyzsh/blob/master/templates/zshrc.zsh-template) by Robby Russell and contributors, under the [MIT license](licenses/ohmyzsh-LICENSE.txt). The powerlevel10k wizard wrote its instant prompt block, under the [MIT license](licenses/powerlevel10k-LICENSE.txt).

[.zprofile](zsh/.zprofile): `~/.zprofile`

- It adds Homebrew, Docker Desktop, `~/.local/bin`, and pyenv to the `PATH`. This copy uses `$HOME` in place of my home path.

## zsh-autosuggestions

[repo](https://github.com/zsh-users/zsh-autosuggestions)

zsh-autosuggestions suggests a command from the history while I type. Homebrew installs it, and `.zshrc` loads it.

## zsh-syntax-highlighting

[repo](https://github.com/zsh-users/zsh-syntax-highlighting)

zsh-syntax-highlighting colors a command while I type it. Homebrew installs it, and `.zshrc` loads it.

## References

[oh-my-ghostty](https://github.com/sudo-conner/oh-my-ghostty)
