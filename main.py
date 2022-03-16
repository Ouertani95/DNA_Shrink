#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main script to launch the program"""

__author__ = 'Mohamed Ouertani'

# Local package imports
from dnashrink.controller import Controller


def main() -> None:
    """
    main function used to launch the program

    Returns:
    ----------
    None
    """
    #Initiate Controller Object
    coordinator = Controller()
    #Launch the GUI
    coordinator.launch_view()


#Execute main function
if __name__ == "__main__":
    main()
