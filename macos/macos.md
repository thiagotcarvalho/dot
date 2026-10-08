# macOS Applications

This file lists the apps that I use every day, and the Brewfile that installs most of them.

## Homebrew

[website](https://brew.sh/)

Homebrew installs my Cursor extensions and most of my command-line tools and apps on a new Mac.

[Brewfile](Brewfile)

- `brew bundle dump` wrote this file. I added a cask for each installed app that has a current Homebrew cask.
- Install Homebrew first. Then run `brew bundle --file=macos/Brewfile` from the repo root.
- It installs the command-line tools, the apps, the Cursor extensions, and the tools that `uv` and `npm` install.
- It does not install the Codex app, SaveHollyWood, Cold Turkey Blocker, Hidden, Notion, Notion Calendar, Notion Mail, or the alternatives. Use their links below. Homebrew marks the Codex app cask as discontinued. The `npm` entry installs the Codex command-line tool.
- It does not install oh-my-zsh, which `.zshrc` needs. Install oh-my-zsh from its [website](https://ohmyz.sh/) before you copy `.zshrc`.
- Homebrew installs the Cursor extensions with the first of `code`, `codium`, `cursor`, and `code-insiders` that it finds. The `cursor` cask adds `cursor`. If the extensions do not install, open a new shell. Then run the `brew bundle` command again.

## Daily Drivers

[Arc Browser](https://arc.net/)

[Claude](https://claude.ai/onboarding)

[Codex](https://openai.com/codex/)

[Cold Turkey Blocker](https://getcoldturkey.com/)

[Cursor](https://cursor.com/)

[Ghostty](https://ghostty.org/)

[Hidden](https://github.com/dwarvesf/hidden?tab=readme-ov-file)

[KeepingYouAwake](https://keepingyouawake.app/)

[Notion](https://www.notion.com/)

[Notion Calendar](https://www.notion.com/product/calendar)

[Notion Mail](https://www.notion.com/product/mail)

[Obsidian](https://obsidian.md/)

[Raycast](https://www.raycast.com/)

[Rectangle](https://rectangleapp.com/)

[SaveHollyWood](http://s.sudre.free.fr/Software/SaveHollywood/about.html)

[Shottr](https://shottr.cc/)

[Spotify](https://open.spotify.com/)

[TextMate](https://macromates.com/)

## Alternatives

[Firefox Browser](https://www.firefox.com/en-US/)

[Ice App](https://icemenubar.app/)

[Spark Mail](https://sparkmailapp.com/)

- If Notion Mail cannot be used.

[Visual Studio Code](https://code.visualstudio.com/)

- If Cursor or Neovim cannot be used.
