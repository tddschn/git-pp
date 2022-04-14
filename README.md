# git pp: Git utility for auto-committing and concurrent pushing

Powered by `asyncio`, with no dependency besides `python>=3.10`.

## Features
- Auto-stages and commits with custom or generated commit messages
- Pushes to multiple or all remotes of a git repository concurrently with `asyncio`
- Operates on any number of git repositories at the same time

## Demo

[![asciicast](https://asciinema.org/a/487579.png)](https://asciinema.org/a/487579)

## Installation

### pipx

This is the recommended installation method.

```
$ pipx install git-pp
```

### [pip](https://pypi.org/project/git-pp/)
```
$ pip install git-pp
```

### [AUR](https://aur.archlinux.org/packages/python-git-pp)
For Archlinux.
```
$ yay -S python-git-pp
```


## Usage
```
$ git pp -h
usage: git pp [-h] [-m COMMIT_MESSAGE] [-v] [-so] [-p] [-po] [-r REMOTE [REMOTE ...]] [-b BRANCH] [-f] [-t TIMEOUT] [DIRS ...]

Git utility for auto-committing and concurrent pushing

positional arguments:
  DIRS                  Dirs to operate on (default: ['.'])

options:
  -h, --help            show this help message and exit
  -m COMMIT_MESSAGE, --commit-message COMMIT_MESSAGE
                        commit message (default: None)
  -v, --version         show program's version number and exit
  -so, --status-only    Prints status only (default: False)
  -p, --push            Push to all remotes (default: False)
  -po, --push-only      Push to all remotes, without pre_pull (default: False)
  -r REMOTE [REMOTE ...], --remote REMOTE [REMOTE ...]
                        Remote name (default: None)
  -b BRANCH, --branch BRANCH
                        Branch name (default: None)
  -f, --force           Force push (default: False)
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout for a single push (default: None)
```