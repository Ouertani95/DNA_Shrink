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

def text_compression(sequence=None,binary_tree=None,freq_list=[]):
    len_list = len(freq_list)
    binary_car_dict = {freq_list[i][0]:0 for i in range(len_list)}
    print(binary_car_dict)
    for car in binary_car_dict.keys():
        binary_car_dict[car] = binary_tree.head_node.get_leaf(car)
    print(binary_car_dict)
    return binary_car_dict
