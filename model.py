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
        if self.sequence_checker():
            self.bwt_handler = Bwt(self.input_sequence)
        else:
            self.bwt_handler = None
        self.huffman_handler = Huffman(self.input_sequence)

    def sequence_extractor(self,input_file):
        """Reads a sequence file and returns the sequence ready to be encoded"""

        with open(input_file,"r") as file_input:
            raw_sequence = file_input.read()
        print("input sequence : \n",raw_sequence)
        return raw_sequence

    def sequence_checker(self):
        uncompressed = True
        for char in self.input_sequence:
            if char not in ["A","T","G","C","N","$"]:
                uncompressed = False
                break
        return uncompressed

    def handle_uncompressed(self,modif_type):
        if modif_type == 0:
            self.bwt_handler.bwt_generator()

        if modif_type == 1:
            self.huffman_handler.sequence_to_binary()
            self.huffman_handler.binary_to_char()

        if modif_type == 2:
            bwt_sequence = self.bwt_handler.bwt_generator()
            self.huffman_handler = Huffman(bwt_sequence)
            self.huffman_handler.sequence_to_binary()
            self.huffman_handler.binary_to_char()

    def handle_compressed(self):
        pass

    def save_file(self):
        pass

if __name__ == "__main__":
    test_model = Model("NC_009513.1_copy.fasta")
    test_model.handle_uncompressed(0)
    print("-------------------------------------------------------------------")
    test_model.handle_uncompressed(1)
    print("-------------------------------------------------------------------")
    test_model.handle_uncompressed(2)