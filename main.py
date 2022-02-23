#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
main file to ...
"""

__author__ = 'Mohamed Ouertani'

from bwt import Bwt
from huffman import Huffman

if __name__ == "__main__":

    BWT_transformer = Bwt(input_file="NC_009513.1_copy.fasta")
    bwt_sequence = BWT_transformer.bwt_generator()
    DECODED_SEQUENCE = BWT_transformer.bwt_decoder()
    print()
    print("#----------------------------------------------------------")
    print()
    Huffman_transformer = Huffman(input_file="NC_009513.1_copy.fasta")
    binary_sequence = Huffman_transformer.sequence_to_binary()
    characters = Huffman_transformer.binary_to_char()
    original_sequence = Huffman_transformer.binary_to_sequence()
