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
    print("frequency list : ",counts_list)
    return counts_list

def sequence_compression(sequence,binary_tree,freq_list):
    coding_dict,decoding_dict = binary_tree.head_node.get_leaves(binary_tree)
    coded_sequence = ""
    for nuc in sequence:
        coded_sequence += coding_dict[nuc]
    print("coding dictionnary : ",coding_dict)
    print("decoding dictionnary : ",decoding_dict)
    print("initial sequence : ",sequence)
    print("compressed sequence : ",coded_sequence)
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
    print("decompressed sequence : ",decoded_sequence)
    return decoded_sequence

def binary_to_char(compressed_sequence):
    # print(compressed_sequence)
    # char_sequence = ""
    char_list = []
    len_compressed = len(compressed_sequence)
    i=0
    while i < len_compressed:
        if i+8 <= len_compressed:
            partial_sequence = compressed_sequence[i:i+8]
            # print(type(partial_sequence))
            # print(str(partial_sequence))
            # print(chr(int(partial_sequence,2)))
            char_list.append(chr(int(partial_sequence,2)))
            # char_sequence += chr(int(partial_sequence,2))
            i = i+8
        else:
            partial_sequence = compressed_sequence[i:len_compressed]
            # print(partial_sequence)
            # print(chr(int(partial_sequence,2)))
            char_list.append(chr(int(partial_sequence,2)))
            # char_sequence += chr(int(compressed_sequence[i:len_compressed],2))
            break
    # print(char_sequence)
    print("list of chars from compressed sequence : ",char_list)
    print("last char number of bits :",len_compressed%8)
    # return char_sequence
    return char_list
