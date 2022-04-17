#!/usr/bin/env python3
"""
Author : Xinyuan Chen <45612704+tddschn@users.noreply.github.com>
Date   : 2022-04-12
"""

import argparse, asyncio
from pathlib import Path
import sys
from git_pp import __version__, __app_name__
from git_pp.git_pre_pull import git_pre_pull, git_pre_pull_and_push_to_all_remote_C
from git_pp.git_push_to_all_remotes import git_push_to_all_remote_C


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        prog=__app_name__,
        description='Git utility for auto-committing and concurrent pushing',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('dirs',
                        metavar='DIRS',
                        nargs='*',
                        help='Dirs to operate on',
                        type=Path,
                        default=['.'])

    parser.add_argument('-m',
                        '--commit-message',
                        help='commit message',
                        metavar='COMMIT_MESSAGE',
                        type=str,
                        default=None)

    # parser.add_argument('-i',
    #                     '--int',
    #                     help='A named integer argument',
    #                     metavar='int',
    #                     type=int,
    #                     default=0)

    parser.add_argument('-v',
                        '--version',
                        action='version',
                        version=f'%(prog)s {__version__}')

    parser.add_argument('-so',
                        '--status-only',
                        help='Prints status only',
                        action='store_true')

    parser.add_argument('-p',
                        '--push',
                        help='Push to all remotes',
                        action='store_true')

    parser.add_argument('-po',
                        '--push-only',
                        help='Push to all remotes, without pre_pull',
                        action='store_true')

    parser.add_argument('-r',
                        '--remote',
                        help='Remote name',
                        metavar='REMOTE',
                        type=str,
                        default=None,
                        nargs='+')

    parser.add_argument('-b',
                        '--branch',
                        help='Branch name',
                        metavar='BRANCH',
                        type=str,
                        default=None)

    parser.add_argument('-f',
                        '--force',
                        help='Force push',
                        action='store_true')

    parser.add_argument('-t',
                        '--timeout',
                        help='Timeout for a single push',
                        metavar='TIMEOUT',
                        type=float,
                        default=None)

    return parser.parse_args()


async def main():
    args = get_args()
    dirs = args.dirs
    commit_message = args.commit_message
    status_only = args.status_only
    push_only = args.push_only
    push = args.push
    remotes = args.remote
    branch = args.branch
    force = args.force
    timeout = args.timeout

    if push and push_only:
        sys.exit('Error: -po and -p are mutually exclusive')
    elif push:
        await git_pre_pull_and_push_to_all_remote_C(
            dirs=dirs,
            commit_message=commit_message,
            status_only=status_only,
            remotes=remotes,
            branch=branch,
            force=force,
            timeout=timeout)
    elif push_only:
        await git_push_to_all_remote_C(dirs=dirs,
                                       remotes=remotes,
                                       branch=branch,
                                       force=force,
                                       timeout=timeout)
    else:
        await git_pre_pull(dirs[0] if dirs else '.',
                           commit_message=commit_message,
                           status_only=status_only)


def main_sync():
    asyncio.run(main())

if __name__ == '__main__':
    main_sync()