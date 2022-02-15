#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
main file to ...
"""

__author__ = 'Mohamed Ouertani'

import bwt
import huffman
from binary_tree import BinaryTree

if __name__ == "__main__":
    sequence_to_transform = bwt.file_reading("NC_009513.1_copy.fasta")
    ENCODED_SEQUENCE = bwt.bwt_generator(sequence_to_transform)
    DECODED_SEQUENCE = bwt.bwt_decoder(ENCODED_SEQUENCE)
    frequency_count = huffman.car_frequency(DECODED_SEQUENCE)
    frequency_tree  = BinaryTree()
    frequency_tree.tree_builder(frequency_count)
    print(frequency_tree)
    compressed_sequence = huffman.sequence_compression (DECODED_SEQUENCE,frequency_tree ,frequency_count)
    decompressed_sequence = huffman.sequence_decompression(compressed_sequence,frequency_tree)