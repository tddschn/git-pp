#!/usr/bin/env python3

import asyncio, sys
from distutils.util import strtobool
import datetime
from asyncio.subprocess import Process
from pathlib import Path

from git_pp.git_push_to_all_remotes import PathLike, git_push_to_all_remote


async def run_command(*args,
                      cwd: PathLike | None = None,
                      silent: bool = False) -> int:
    """Run a command in a subprocess and return the output.

    Args:
        *args: command and arguments

    Returns:
        str: output of the command
    """
    process: Process = await asyncio.create_subprocess_exec(
        *args,
        cwd=cwd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, _ = await process.communicate()
    if not silent:
        print(stdout.decode())

    rc = await process.wait()
    return rc


def get_iso8601_timestamp():
    """get current time in this format "%Y-%m-%dT%H-%M-%SZ"
    """
    # return datetime.datetime.utcnow().isoformat() + 'Z'
    # return datetime.datetime.now().isoformat()
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%dT%H-%M-%SZ')


async def git_pre_pull(cwd: PathLike | None = None,
                       commit_message: str | None = None,
                       status_only: bool = False) -> None:
    """
    Args:
        cwd (PathLike | None): working directory
    """
    print(f'📦 Pre-pulling {cwd or "."} ...')
    # https://unix.stackexchange.com/questions/46814/watch-command-not-showing-colors-for-git-status
    await run_command('git', '-c', 'color.status=always', 'status', cwd=cwd)
    await run_command('git', 'add', '--all', cwd=cwd, silent=status_only)
    await run_command(
        'git',
        'commit',
        '-m',
        f'{get_iso8601_timestamp() if not commit_message else commit_message}',
        cwd=cwd,
        silent=status_only)


async def git_pre_pull_and_push_to_all_remote(
        commit_message: str
    | None = None,
        status_only: bool = False,
        remotes: list[str]
    | None = None,
        branch: str | None = None,
        force=False,
        timeout=None,
        cwd: PathLike | None = None) -> tuple[int, PathLike | None]:
    """
    Args:
        force (bool): force push
        timeout (int): timeout in seconds
        cwd (PathLike | None): working directory
    """
    await git_pre_pull(commit_message=commit_message,
                       status_only=status_only,
                       cwd=cwd)
    rc, _, _ = await git_push_to_all_remote(remotes=remotes,
                                            branch=branch,
                                            force=force,
                                            timeout=timeout,
                                            cwd=cwd)
    return rc, cwd


async def git_pre_pull_and_push_to_all_remote_C(dirs: list[PathLike],
                                                commit_message: str
                                                | None = None,
                                                status_only: bool = False,
                                                remotes: list[str]
                                                | None = None,
                                                branch: str | None = None,
                                                force=False,
                                                timeout=None) -> int:
    """
    Args:
        force (bool): force push
        timeout (int): timeout in seconds
        cwd (PathLike | None): working directory
    """
    coros = [
        git_pre_pull_and_push_to_all_remote(commit_message=commit_message,
                                            status_only=status_only,
                                            force=force,
                                            remotes=remotes,
                                            branch=branch,
                                            timeout=timeout,
                                            cwd=cwd) for cwd in dirs
    ]
    # status_codes = asyncio.gather(*ts)
    status_codes = []
    for td in asyncio.as_completed(coros):
        # from icecream import ic
        # ic(td.cr_frame.f_locals)
        # ic(await td.get_coro())
        status_code, cwd = await td
        if status_code == 0:
            print(f'✓ Pre-pulled and pushed to all remotes of {cwd}.')
        else:
            print(f'𐄂 Failed to pre-pull and push to all_remotes of {cwd}.')
        status_codes.append(status_code)
    dirs_s = list(map(str, dirs))
    if not any(status_codes):
        print(
            f'✅ Pushed {"current branch" if branch is not None else branch} of {dirs} to all of their remotes successfully.'
            + ('(FORCE)' if force else ''))
        return 0
    else:
        print(
            f'❌ Failed to push {"current branch" if branch is not None else branch} of {dirs} to all of their remotes.'
            + ('(FORCE)' if force else ''))
        return 1
    #     # all 0
    #     print(
    #         f'✅ Pre-pulled and pushed {dirs_s} to all of their remotes successfully.'
    #         + ('(FORCE)' if force else ''))
    #     return 0
    # else:
    #     print(
    #         f'❌ Failed to pre-pull and push {dirs_s} to all of their remotes.'
    #         + ('(FORCE)' if force else ''))
    #     return 1


async def main() -> None:
    if len(sys.argv) > 1:
        await git_pre_pull(
            cwd=sys.argv[1],  # type: ignore
            commit_message=sys.argv[2] if len(sys.argv) > 2 else None,
            status_only=bool(strtobool(sys.argv[3]))
            if len(sys.argv) > 3 else False)
    else:
        await git_pre_pull()


if __name__ == '__main__':
    asyncio.run(main())