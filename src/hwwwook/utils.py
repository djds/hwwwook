#!/bin/false
"""A very simple webhook api - helper functions"""

from os import getcwd
from subprocess import CalledProcessError, CompletedProcess, run
from typing import Any


def clone(
    repository: str, destination: str | None = None
) -> CompletedProcess[Any]:
    """Clone git repo"""
    if destination is None:
        args = ["git", "clone", repository]
    else:
        args = ["git", "clone", repository, destination]

    return run(args, check=True, capture_output=True)


def pull(path: str, reset: bool, ref: str) -> CompletedProcess[Any]:
    """git pull or reset"""
    try:
        return run(
            ["git", "-C", path, "pull"], check=True, capture_output=True
        )
    except CalledProcessError:
        if reset:
            return run(
                ["git", "-C", path, "reset", "--hard", ref],
                check=True,
                capture_output=True,
            )
        raise


def build(
    source: str | None = None, destination: str | None = None
) -> CompletedProcess[Any]:
    """Build static site with hugo"""

    cwd = getcwd()

    if source is None:
        source = cwd
    if destination is None:
        destination = f"{cwd}/public"

    return run(
        ["hugo", "--source", source, "--destination", destination],
        check=True,
        capture_output=True,
    )
