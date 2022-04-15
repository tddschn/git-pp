# git pp

A (tiny) Git utility for auto-committing and concurrent pushing.

Powered by `asyncio`, with no dependency besides `python>=3.10` and `git`.

## Features
- Auto-stages and commits with custom or generated commit messages
- Pushes to multiple or all remotes of a git repository concurrently with `asyncio`
- Operates on any number of git repositories at the same time

## Demo

<!-- [![asciicast](https://asciinema.org/a/487579.png)](https://asciinema.org/a/487579) -->
<a href="https://asciinema.org/a/487579"><img src="https://asciinema.org/a/487579.png" alt="asciicast" style="width:500px;height:300px;"></a>


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