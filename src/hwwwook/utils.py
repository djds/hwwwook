#!/bin/false
"""A very simple webhook api - helper functions"""

from os import getcwd
from subprocess import CompletedProcess, run
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


def pull(path: str, reset: bool = False) -> CompletedProcess[Any]:
    """git pull or reset"""
    if reset:
        args = ["git", "-C", path, "reset", "--hard", "HEAD"]
    else:
        args = ["git", "-C", path, "pull"]

    return run(args, check=True, capture_output=True)


def build(
    source: str | None = None, destination: str | None = None
) -> CompletedProcess[Any]:
    """Build static site with hugo"""

    cwd = getcwd()

    if source is None:
        source = cwd
    if destination is None:
        destination = cwd

    return run(
        ["hugo", "--source", source, "--destination", destination],
        check=True,
        capture_output=True,
    )
