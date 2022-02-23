#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Model module to manipulate the data
"""

__author__ = 'Mohamed Ouertani'

from bwt import Bwt
from huffman import Huffman

class Model():

    """Model class"""

    def __init__(self,input_file):
        self.input_sequence = self.sequence_extractor(input_file)
        self.BWT = Bwt()
        self.HUFFMAN = Huffman()

    def sequence_extractor(self,input_file):
        """Reads a sequence file and returns the sequence ready to be encoded"""

        caracters = ["A","T","G","C","N"]
        with open(input_file,"r") as file_input:
            raw_sequence = file_input.read()
        for car in raw_sequence:
            if car not in caracters:
                raw_sequence = raw_sequence.replace(car,"")
        print("input sequence : \n",raw_sequence)
        return raw_sequence
