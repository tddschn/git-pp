# git pp

A (tiny) Git utility for auto-committing and concurrent pushing.

Powered by `asyncio`, with no dependency besides `python>=3.10` and `git`.

- [git pp](#git-pp)
  - [Features](#features)
  - [Use cases and example usage](#use-cases-and-example-usage)
  - [Demo](#demo)
  - [Installation](#installation)
    - [pipx](#pipx)
    - [pip](#pip)
    - [AUR](#aur)
  - [Usage](#usage)
  - [Develop](#develop)
## Features
- Auto-stages and commits with custom or generated commit messages
- Pushes to multiple or all remotes of a git repository **concurrently** with `asyncio`
- Operates on **any number of git repositories** at the same time

## Use cases and example usage
- You have multiple remotes registered on a local git repository (or more)
and want to push the changes to all or some of the remotes fast and efficiently.

```bash
# Use --push-only or -po

$ git pp --push-only # this pushes to all remotes of the current git repository, does not stages or commits
$ git pp --push-only --remote [one or more remotes] # only pushes to the specified remotes
$ git pp -po --timeout 10 # terminates pushing to one remotes if it takes more than 10 seconds
$ git pp -po -b dev ~/my-proj ~/my-proj2 # pushes the dev branch to all remotes in ~/my-proj and ~/my-proj2 repository
```

- You're tired of using `git add --all && git commit` every time you make a little change
and want to automate this across one or more repositories.

```bash
$ git pp # stages all files in the current git repository and commits with a timestamp as the commit message
$ git pp -m 'Initial commit' # custom commit message
$ git pp --no-status # don't show git status and git add outputs
```

And you can do both of the above (auto-commit and push) with `--push`:
```bash
# Use --push or -p

$ git pp --push # stages, commits and pushes to all remotes.
$ git pp --push --remote [one or more remotes]
$ git pp -p --timeout 10
$ git pp -p -b dev ~/my-proj ~/my-proj2
```

## Demo

<!-- [![asciicast](https://asciinema.org/a/487579.png)](https://asciinema.org/a/487579) -->
<!-- <a href="https://asciinema.org/a/487579"><img src="https://asciinema.org/a/487579.png" alt="asciicast" style="width:500px;height:300px;"></a> -->
<a href="https://asciinema.org/a/487579"><img src="https://asciinema.org/a/487579.svg" alt="Asciicast" width="650"/></a>

In this demo, git pp did the following in \~/config and \~/gui repos:

- (Concurrently) Auto staged all changes and commits with ISO-8601 timestamps as commit messages;
- (Concurrently) Pushed the changes in the checked out branch to all of their remotes, in this case, they’re origin and lab.

## Installation

First make sure the `git` executable is installed and in your `$PATH`.

Note that non-UNIX systems are not officially supported.

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

You can either invoke this tool with `git-pp` or `git pp`,
`--help` is unsupported when using the latter.

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

## Develop
```
$ git clone https://github.com/tddschn/git-pp.git
$ cd git-pp
$ poetry install
```