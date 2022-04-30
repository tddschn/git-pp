#!/usr/bin/env python3

from pathlib import Path
import typer, asyncio
from .git_push_to_all_remotes import PathLike
# from subprocess import CompletedProcess
from asyncio.subprocess import Process

# cSpell:disable
# https://github.com/faif/python-patterns
# https://github.com/faif/python-patterns.git
# git@github.com:faif/python-patterns.git
# gh repo clone faif/python-patterns
# cSpell:enable

app = typer.Typer(name='clone')


@app.command()
async def clone(git_repo_url: str,
                timeout: float | None = None,
                dest: PathLike = '.',
                name: str | None = None) -> tuple[int, tuple[str, str]]:
    """Clone a git repo to a local directory."""
    if name is None:
        name = git_repo_url.split('/')[-1].split('.')[0]
    dest = Path(dest)
    if not dest.exists():
        dest.mkdir()
    dest = dest / name
    program = ['git', 'clone', git_repo_url, str(dest)]
    process: Process = await asyncio.create_subprocess_exec(*program)
    print(f'Pushing {git_repo_url} to {str(dest)}.')
    try:
        status_code = await asyncio.wait_for(process.wait(), timeout=timeout)
        # print(status_code)
    except asyncio.TimeoutError:
        print('Timed out waiting to finish, terminating...')
        process.terminate()
        status_code = await process.wait()
        # print(status_code)
    return (status_code, (git_repo_url, str(dest)))


if __name__ == '__main__':
    app()