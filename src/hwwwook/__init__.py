#!/usr/bin/env python3
"""A simple webhook API server"""


from subprocess import CalledProcessError

from fastapi import FastAPI, HTTPException

from .utils import build, clone, pull
from .website import Website

__all__ = ["api"]

api = FastAPI()


@api.post("/gitolite")
async def deploy_website(website: Website) -> dict[str, dict[str, str | int]]:
    """gitolite webhook for hugo to build static site"""

    try:
        try:
            git = clone(website.repository, website.sourcepath)
        except CalledProcessError:
            git = pull(website.sourcepath, website.reset, website.ref)

        hugo = build(website.sourcepath, website.target)

        return {
            "git": {
                "args": git.args,
                "returncode": git.returncode,
                "stderr": git.stderr,
                "stdout": git.stdout,
            },
            "hugo": {
                "args": hugo.args,
                "returncode": hugo.returncode,
                "stderr": hugo.stderr,
                "stdout": hugo.stdout,
            },
        }

    except CalledProcessError as err:
        raise HTTPException(status_code=500, detail=f"{err}") from err
