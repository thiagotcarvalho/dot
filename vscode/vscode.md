# VS Code Setup

This file lists my code editor, with its settings and extensions.

This folder holds only the files that I wrote or changed. A link points to each extension that I installed without a change. A config file name below links to its copy in this folder. The path after it is where the file lives locally.

## Visual Studio Code

[website](https://code.visualstudio.com/)

VS Code is the code editor that I use every day.

[settings.json](settings.json): `~/Library/Application Support/Code/User/settings.json`

- It makes the color scheme follow the system, and it puts the activity bar at the top.
- It turns off the built-in AI features.
- It also sets git, the file explorer prompts, and Python. Python gets a ruler at 100 characters, auto-import suggestions, and suggestions in strings.
- This copy leaves out the remote SSH hosts and my color themes, because the themes are not public.

### VS Code Extensions

From the repo root, `brew bundle --file=macos/Brewfile` installs these extensions and the other Brewfile items.

[Container Tools](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-containers)

[Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

[Docker](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)

[GitLens](https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens)

[markdownlint](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint)

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance)

[Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)

[Python Debugger](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy)

[Rainbow CSV](https://marketplace.visualstudio.com/items?itemName=mechatroner.rainbow-csv)

[Remote - SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh)

[Vim](https://marketplace.visualstudio.com/items?itemName=vscodevim.vim)
