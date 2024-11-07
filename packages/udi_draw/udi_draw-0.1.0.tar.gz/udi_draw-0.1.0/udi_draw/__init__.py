"""An amazing paint app for the command line."""

__version__ = "0.1.0"

import sys

from .simple.shapes import square
from .buildings import house


def main():
    print("Welcome to udi_draw!", __version__)
    print("Running on python:", sys.executable, sys.version_info)
    square(8, "!")
