# The following lines were added by Docker Desktop to add commands to your PATH.
export PATH="$PATH:$HOME/.docker/bin"
# End of Docker Desktop section.

eval "$(/opt/homebrew/bin/brew shellenv zsh)"

# >>> Codex installer >>>
export PATH="$HOME/.local/bin:$PATH"
# <<< Codex installer <<<
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - --no-rehash zsh)"
