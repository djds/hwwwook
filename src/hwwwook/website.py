#!/bin/false
"""A simple website class"""

# https://github.com/pydantic/pydantic/issues/1961
# https://github.com/nokia-wroclaw/innovativeproject-sudoku/issues/39
# pylint: disable-next=no-name-in-module
from pydantic import BaseModel


# pylint: disable-next=too-few-public-methods
class Website(BaseModel):
    """Basic class for website source code"""

    repository: str
    sourcepath: str
    target: str
    reset: bool = False
