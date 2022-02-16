#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BWT module to encode and decode a sequence
"""

__author__ = 'Mohamed Ouertani'

from time import time
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
        print("input sequence with dollar : \n",dollar_sequence)
    return dollar_sequence

def matrix_sorter(matrix,length):

    """Sorts a matrix in lexicographical order"""

    sorting_vector = np.full((1,length),"",dtype="U1000")
    for line_index in range(length):
        sorting_vector[0,line_index] = "".join(matrix[line_index,:])
    sorting_vector.sort()
    for line_index in range(length):
        matrix[line_index,:] = list(sorting_vector[0,line_index])
    print(matrix)
    return matrix

def bwt_generator(raw_sequence):

    """Generates the bwt encoded sequence"""

    actual_sequence = raw_sequence
    sequence_len = len(actual_sequence)
    bwt_matrix = np.full((sequence_len,sequence_len),"",dtype=str)
    for line_index in range(sequence_len):
        bwt_matrix[line_index,:] = list(actual_sequence)
        actual_sequence = actual_sequence[-1] + actual_sequence[:-1]
    print("matrix with all offsets : \n",bwt_matrix)
    bwt_matrix = matrix_sorter(bwt_matrix,sequence_len)
    print("sorted matrix with all offsets : \n",bwt_matrix)
    bwt_sequence = "".join(bwt_matrix[:,sequence_len-1])
    print("bwt sequence : \n",bwt_sequence)
    return bwt_sequence


def bwt_decoder(bwt_sequence):

    """Decodes a BWT sequence to recover original sequence"""

    bwt_len = len(bwt_sequence)
    decoding_matrix = np.full((bwt_len,bwt_len),"",dtype=str)
    for _ in range(bwt_len):
        decoding_matrix = np.roll(decoding_matrix,1)
        print(decoding_matrix)
        decoding_matrix[:,0] = list(bwt_sequence)
        print(decoding_matrix)
        decoding_matrix = matrix_sorter(decoding_matrix,bwt_len)
    print("bwt decoding matrix : \n",decoding_matrix)
    for dollar_index in range(bwt_len):
        if decoding_matrix[dollar_index,bwt_len-1] == "$":
            original_sequence = "".join(decoding_matrix[dollar_index,:bwt_len-1])
            print("original sequence : \n",original_sequence)
            print("length of original sequence : ",len(original_sequence))
            break
    return original_sequence


if __name__ == "__main__":
    start = time()
    sequence_to_transform = file_reading("NC_009513.1_copy.fasta")
    ENCODED_SEQUENCE = bwt_generator(sequence_to_transform)
    DECODED_SEQUENCE = bwt_decoder(ENCODED_SEQUENCE)
    print(time()-start)
    