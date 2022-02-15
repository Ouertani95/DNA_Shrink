#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Huffman module to ...
"""

__author__ = 'Mohamed Ouertani'

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

def binary_to_char(compressed_sequence):
    char_sequence = ""
    len_compressed = len(compressed_sequence)
    i=0
    while i < len_compressed:
        if i+8 <= len_compressed:
            print(compressed_sequence[i:i+8])
            print(chr(int(compressed_sequence[i:i+8],2)))
            char_sequence += chr(int(compressed_sequence[i:i+8],2))
            i = i+8
        else:
            print(compressed_sequence[i:len_compressed])
            print(chr(int(compressed_sequence[i:len_compressed],2)))
            char_sequence += chr(int(compressed_sequence[i:len_compressed],2))
            break
    print(char_sequence)
    return char_sequence
