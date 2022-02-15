#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Huffman module to ...
"""

__author__ = 'Mohamed Ouertani'

from bz2 import compress
from collections import Counter

def car_frequency(sequence):
    counts = Counter(sequence)
    counts_list = sorted(counts.items(), key=lambda x:x[1])
    print(counts_list)
    return counts_list

def sequence_compression(sequence,binary_tree,freq_list):
    coding_dict,decoding_dict = binary_tree.head_node.get_leaves(binary_tree)
    coded_sequence = ""
    for nuc in sequence:
        coded_sequence += coding_dict[nuc]
    print(coding_dict)
    print(decoding_dict)
    print(sequence)
    print(coded_sequence)
    return coded_sequence

def sequence_decompression(compressed_sequence,binary_tree,freq_list=""):
    coding_dict,decoding_dict = binary_tree.head_node.get_leaves(binary_tree)
    decoded_sequence = ""
    seq_len = len(compressed_sequence)
    i = 0
    len_sub = 1
    while i + len_sub <= seq_len:
        subbinary_sequence = compressed_sequence[i:i+len_sub]
        if subbinary_sequence in decoding_dict.keys():
            decoded_sequence += decoding_dict[subbinary_sequence]
            i = i + len_sub
            len_sub = 1
        else:
            len_sub += 1
    print(decoded_sequence)
    return decoded_sequence

    pass