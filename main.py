#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main script to launch the program"""

from __future__ import absolute_import
from dnashrink.controller  import Controller

def main() -> None:
    """Launches the program."""
    brains = Controller()
    brains.launch_view()

if __name__ == "__main__":
    main()
