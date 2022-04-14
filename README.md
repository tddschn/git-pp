## Usage:
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