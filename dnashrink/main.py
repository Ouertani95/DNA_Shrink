#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main script to launch the GUI."""

from __future__ import absolute_import
from controller import Controller

def main() -> None:
    """Launches the program."""
    Brains = Controller()
    Brains.launch_view()

if __name__ == "__main__":
    main()
    
