"""Entry point script."""

from git_pp.git_pp import main as main_async
import asyncio


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
