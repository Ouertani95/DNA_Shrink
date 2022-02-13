#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BWT module to encode and decode a sequence
"""

__author__ = 'Mohamed Ouertani'

import numpy as np


def file_reading(input_file):

    """Reads a sequence file and returns the sequence ready to be encoded"""
    caracters = ["A","T","G","C","N"]
    with open(input_file,"r") as file_input:
        dollar_sequence = file_input.read()
        for car in dollar_sequence:
            if car not in caracters:
                dollar_sequence = dollar_sequence.replace(car,"")
        dollar_sequence += "$"
        print(dollar_sequence)
    return dollar_sequence


def bwt_generator(raw_sequence):

    """Generates the bwt encoded sequence"""

    actual_sequence = raw_sequence
    sequence_len = len(actual_sequence)
    bwt_matrix = np.empty((sequence_len,sequence_len),dtype=str)
    for line_index in range(sequence_len):
        bwt_matrix[line_index,:] = list(actual_sequence)
        actual_sequence = actual_sequence[-1] + actual_sequence[:-1]
    print(bwt_matrix)
    bwt_matrix =  bwt_matrix[bwt_matrix[:,0].argsort()]
    print(bwt_matrix)
    bwt_sequence = "".join(bwt_matrix[:,sequence_len-1  ])
    print(bwt_sequence)
    return bwt_sequence


def bwt_decoder(bwt_sequence):

    """Decodes a BWT sequence to recover original sequence"""

    bwt_len = len(bwt_sequence)
    print(bwt_len)
    decoding_matrix = np.empty((bwt_len,bwt_len),dtype=str)
    print(decoding_matrix.shape)
    for _ in range(bwt_len):
        decoding_matrix = np.roll(decoding_matrix,1)
        decoding_matrix[:,0] = list(bwt_sequence)
        # decoding_matrix = decoding_matrix[decoding_matrix[:,0].argsort()]
        decoding_matrix = decoding_matrix[np.lexsort(decoding_matrix[:,::-1].T)]
    print(decoding_matrix)
    for dollar_index in range(bwt_len):
        if decoding_matrix[dollar_index,bwt_len-1] == "$":
            original_sequence = "".join(decoding_matrix[dollar_index,:bwt_len])
            print(original_sequence)
            break
    return original_sequence


if __name__ == "__main__":

    sequence_to_transform = file_reading("NC_009513.1_copy.fasta")
    encoded_sequence = bwt_generator(sequence_to_transform)
    DECODED_SEQUENCE = bwt_decoder(encoded_sequence)
