#!/usr/bin/env python3

import asyncio, sys
from asyncio.subprocess import Process
from pathlib import Path
from typing import AnyStr

PathLike = AnyStr | Path

from git_pp import logger


# logger.add(sys.stdout,
#            colorize=True,
#            format="{level} <green>{time}</green> <level>{message}</level>")
async def git_get_all_remotes(cwd: PathLike | None = None) -> list[str]:
    program = ['git', 'remote']
    proc: Process = await asyncio.create_subprocess_exec(
        *program, stdout=asyncio.subprocess.PIPE, cwd=cwd)
    logger.info(f'Getting all remotes of {cwd} .')
    logger.info(f'Running: {program}')
    # logger.info(f'Args: {proc.__dict__}')  # type: ignore
    stdout, _ = await proc.communicate()
    return stdout.decode().strip().splitlines()


async def git_get_current_branch(cwd: PathLike | None = None) -> str:
    program = ['git', 'branch', '--show-current']
    proc: Process = await asyncio.create_subprocess_exec(
        *program, stdout=asyncio.subprocess.PIPE, cwd=cwd)
    stdout, _ = await proc.communicate()
    return stdout.decode().strip()


# async def git_push_to_remote(branch: str,
#                              remote: str,
#                              force=False,
#                              timeout=None,
#                              cwd: PathLike | None = None) -> tuple[int, str]:
#     """pushes branch to remote named remote, and returns the return code

#     Args:
#         remote (str): name of the remote

#     Returns:
#         int: return code
#     """
#     program = ['git', 'push', remote, branch]
#     if force:
#         program.append('--force')
#     process: Process = await asyncio.create_subprocess_exec(*program, cwd=cwd)
#     print(f'Pushing {branch} to {remote}.')
#     try:
#         status_code = await asyncio.wait_for(process.wait(), timeout=timeout)
#         # print(status_code)
#     except asyncio.TimeoutError:
#         print('Timed out waiting to finish, terminating...')
#         process.terminate()
#         status_code = await process.wait()
#         # print(status_code)
#     return (status_code, remote)


async def git_push_to_remote(remote: str,
                             branch: str | None = None,
                             force=False,
                             timeout=None,
                             cwd: PathLike | None = None) -> tuple[int, str]:
    """pushes branch to remote named remote, and returns the return code

    Args:
        remote (str): name of the remote
        branch (str | None): name of the branch to push

    Returns:
        int: return code
    """
    if branch is None:
        branch = await git_get_current_branch(cwd=cwd)
    program = ['git', 'push', remote, branch]
    logger.info(f'Pushing {branch} to {remote} .')
    logger.info(f'Running: {program}')
    if force:
        program.append('--force')
    process: Process = await asyncio.create_subprocess_exec(*program, cwd=cwd)
    # logger.info(f'Args: {process.__dict__}')  # type: ignore
    print(f'Pushing {branch} to {remote}.')
    try:
        status_code = await asyncio.wait_for(process.wait(), timeout=timeout)
        # print(status_code)
    except asyncio.TimeoutError:
        print('Timed out waiting to finish, terminating...')
        process.terminate()
        status_code = await process.wait()
        # print(status_code)
    return (status_code, remote)


async def git_push_to_all_remote(
        remotes: list[str] | None = None,
        branch: str | None = None,
        force=False,
        timeout=None,
        cwd: PathLike | None = None) -> tuple[int, str, PathLike | None]:

    if remotes is None:
        remotes = await git_get_all_remotes(cwd=cwd)
        PUSH_TO_ALL = True
    else:
        PUSH_TO_ALL = False

    if branch is None:
        branch = await git_get_current_branch(cwd=cwd)

    coros = [
        git_push_to_remote(remote=remote,
                           branch=branch,
                           force=force,
                           timeout=timeout,
                           cwd=cwd) for remote in remotes
    ]
    # status_codes = asyncio.gather(*ts)
    status_codes = []
    for td in asyncio.as_completed(coros):
        # from icecream import ic
        # ic(td.cr_frame.f_locals)
        # ic(await td.get_coro())
        status_code, remote = await td
        if status_code == 0:
            print(f'✓ Pushed {branch} to {remote}.')
        else:
            print(f'𐄂 Failed to push {branch} to {remote}.')
        status_codes.append(status_code)
    if not any(status_codes):
        # all 0
        print(
            f'✅ Pushed {branch} to {"all remotes" if PUSH_TO_ALL else remotes} successfully.'
            + ('(FORCE)' if force else ''))
        return (0, branch, cwd)
    else:
        print(
            f'❌ Failed to push {branch} to some of the remotes in {remotes}.' +
            ('(FORCE)' if force else ''))
        return (1, branch, cwd)


async def git_push_to_all_remote_C(dirs: list[PathLike],
                                   remotes: list[str] | None = None,
                                   branch: str | None = None,
                                   force: bool = False,
                                   timeout: float | None = None) -> int:
    coros = [
        git_push_to_all_remote(remotes=remotes,
                               branch=branch,
                               force=force,
                               timeout=timeout,
                               cwd=cwd) for cwd in dirs
    ]
    # status_codes = asyncio.gather(*ts)
    status_codes = []
    for td in asyncio.as_completed(coros):
        # from icecream import ic
        # ic(td.cr_frame.f_locals)
        # ic(await td.get_coro())
        status_code, curr_branch, cwd = await td
        if status_code == 0:
            print(f'✓ Pushed {curr_branch} to all remotes of {cwd}.')
        else:
            print(f'𐄂 Failed to push {curr_branch} to all_remotes of {cwd}.')
        status_codes.append(status_code)
    if not any(status_codes):
        # all 0
        print(
            f'✅ Pushed {"current branch" if branch is not None else branch} of {dirs} to all of their remotes successfully.'
            + ('(FORCE)' if force else ''))
        return 0
    else:
        print(
            f'❌ Failed to push {"current branch" if branch is not None else branch} of {dirs} to all of their remotes.'
            + ('(FORCE)' if force else ''))
        return 1


async def main() -> None:
    if len(sys.argv) > 1:
        dirs: list[PathLike] = sys.argv[1:]  # type: ignore
        await git_push_to_all_remote_C(dirs, force=False, timeout=None)
    else:
        await git_push_to_all_remote(force=False, timeout=None)


if __name__ == '__main__':
    asyncio.run(main())