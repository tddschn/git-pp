#!/usr/bin/env python3
"""
Author : Xinyuan Chen <45612704+tddschn@users.noreply.github.com>
Date   : 2022-04-12
"""

import argparse
from pathlib import Path
from . import __version__, __app_name__, logger


def import_asyncio():
    import asyncio

    try:
        import uvloop

        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except ImportError:
        pass
    return asyncio


# --------------------------------------------------
# git_pp.py
def get_args():
    """Get command-line arguments"""

    epilog_text = """
Examples:
  You can run this program with either `git-pp` or `git pp`.

  # Check status, stage changes, and commit with a timestamp message in the current directory
  git pp

  # Do the same as above, but also push to all remotes
  git pp -p

  # Just push the current branch to all remotes without creating a new commit
  git pp -po

  # Check status, stage changes, and commit with a custom message
  git pp -m "feat: add new feature"

  # Perform the pre-pull and push operation on multiple directories
  git pp -p path/to/repo1 path/to/repo2

  # Push only specific remotes (works with -p or -po)
  git pp -p -r origin upstream
  git pp -po -r origin

  # Push a specific branch (works with -p or -po)
  git pp -po -b main

  # Force push (works with -p or -po)
  git pp -po -f

  # Set a timeout for push operations (e.g., 60 seconds, works with -p or -po)
  git pp -p -t 60

For more details, visit: https://github.com/tddschn/git-pp

This is an old project, created for self-use only (I still use it daily), to replace some bash scripts and learn asyncio.
"""

    parser = argparse.ArgumentParser(
        prog=__app_name__,
        description="Git utility for auto-committing and concurrent pushing",
        formatter_class=argparse.RawDescriptionHelpFormatter,  # Use RawDescriptionHelpFormatter to preserve epilog formatting
        epilog=epilog_text,  # Add the epilog
    )

    parser.add_argument(
        "dirs",
        metavar="DIRS",
        nargs="*",
        help="Dirs to operate on (default: current directory)",
        type=Path,
        default=["."],
    )

    parser.add_argument(
        "-m",
        "--commit-message",
        help="Commit message (default: ISO8601 timestamp)",
        metavar="COMMIT_MESSAGE",
        type=str,
        default=None,
    )

    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )

    parser.add_argument(
        "-so",
        "--status-only",
        help="Prints status only, stages changes, but does not commit",
        action="store_true",
    )

    parser.add_argument(
        "-p",
        "--push",
        help="Stage, commit (if needed), and push to specified/all remotes",
        action="store_true",
    )

    parser.add_argument(
        "-po",
        "--no-create-commit",
        "--push-only",
        dest="push_only",
        help="Push current state to specified/all remotes, without staging or committing first",
        action="store_true",
    )

    parser.add_argument(
        "-r",
        "--remote",
        help="Specify remote name(s) to push to (default: all remotes)",
        metavar="REMOTE",
        type=str,
        default=None,
        nargs="+",
    )

    parser.add_argument(
        "-b",
        "--branch",
        help="Specify branch name to push (default: current branch)",
        metavar="BRANCH",
        type=str,
        default=None,
    )

    parser.add_argument(
        "-f", "--force", help="Force push (`git push --force`)", action="store_true"
    )

    parser.add_argument(
        "-t",
        "--timeout",
        help="Timeout in seconds for each push operation",
        metavar="TIMEOUT",
        type=float,
        default=None,
    )

    return parser.parse_args()


async def main(args):
    # args = get_args()
    dirs = args.dirs
    commit_message = args.commit_message
    status_only = args.status_only
    push_only = args.push_only
    push = args.push
    remotes = args.remote
    branch = args.branch
    force = args.force
    timeout = args.timeout

    import sys
    from .git_pre_pull import git_pre_pull, git_pre_pull_and_push_to_all_remote_C
    from .git_push_to_all_remotes import git_push_to_all_remote_C

    if push and push_only:
        sys.exit("Error: -po and -p are mutually exclusive")
    elif push:
        await git_pre_pull_and_push_to_all_remote_C(
            dirs=dirs,
            commit_message=commit_message,
            status_only=status_only,
            remotes=remotes,
            branch=branch,
            force=force,
            timeout=timeout,
        )
    elif push_only:
        await git_push_to_all_remote_C(
            dirs=dirs, remotes=remotes, branch=branch, force=force, timeout=timeout
        )
    else:
        await git_pre_pull(
            dirs[0] if dirs else ".",
            commit_message=commit_message,
            status_only=status_only,
        )


def main_sync():
    logger.info("getting args")
    args = get_args()
    logger.info("importing asyncio")
    asyncio = import_asyncio()
    asyncio.run(main(args))


if __name__ == "__main__":
    main_sync()
