#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BWT module to encode and decode a sequence
"""

__author__ = 'Mohamed Ouertani'

import sys
from time import time
import numpy as np

class Bwt():

    """BWT transformer class to help with compression"""

    def __init__(self,input_sequence):
        self.input_sequence = input_sequence
        self.normal_sequence = None
        self.bwt_sequence = None

    @staticmethod
    def _matrix_sorter(matrix,length):

        """Sorts a matrix in lexicographical order"""

        all_sequences = ["".join(matrix[i,:]) for i in range(length)]
        all_sequences.sort()
        length_sub = len(all_sequences[0])
        for line_index in range(length):
            matrix[line_index,:length_sub] = list(all_sequences[line_index])
        print(matrix)
        return matrix

    def bwt_generator(self):

        """Generates the bwt encoded sequence"""
        if "$" in self.input_sequence:
            self.bwt_sequence = self.input_sequence
            print("the sequence is already bwt")
        else:
            actual_sequence = self.input_sequence + "$"
            sequence_len = len(actual_sequence)
            bwt_matrix = np.full((sequence_len,sequence_len),"",dtype=str)
            for line_index in range(sequence_len):
                bwt_matrix[line_index,:] = list(actual_sequence)
                print(bwt_matrix)
                actual_sequence = actual_sequence[-1] + actual_sequence[:-1]
            print("matrix with all offsets : \n",bwt_matrix)
            bwt_matrix = self._matrix_sorter(bwt_matrix,sequence_len)
            print("sorted matrix with all offsets : \n",bwt_matrix)
            self.bwt_sequence = "".join(bwt_matrix[:,sequence_len-1])
            print("bwt sequence : \n",self.bwt_sequence)
        return self.bwt_sequence


    def bwt_decoder(self):

        """Decodes a BWT sequence to recover original sequence"""
        if "$" not in self.input_sequence:
            self.normal_sequence = self.input_sequence
            print("sequence is already not bwt")
        else:
            self.bwt_sequence = self.input_sequence
            bwt_len = len(self.bwt_sequence)
            decoding_matrix = np.full((bwt_len,bwt_len),"",dtype=str)
            for _ in range(bwt_len):
                decoding_matrix = np.roll(decoding_matrix,1)
                print(decoding_matrix)
                decoding_matrix[:,0] = list(self.bwt_sequence)
                print(decoding_matrix)
                decoding_matrix = self._matrix_sorter(decoding_matrix,bwt_len)
            print("bwt decoding matrix : \n",decoding_matrix)
            print(f"size of matrix  : {sys.getsizeof(decoding_matrix)}","bytes")
            for dollar_index in range(bwt_len):
                if decoding_matrix[dollar_index,bwt_len-1] == "$":
                    self.normal_sequence = "".join(decoding_matrix[dollar_index,:bwt_len-1])
                    break
            print("original sequence : \n",self.normal_sequence)
            print("length of original sequence : ",len(self.normal_sequence))
                    
        return self.normal_sequence


if __name__ == "__main__":
    start = time()
    test = Bwt("ACTTGATC")
    test.bwt_generator()
    test.bwt_decoder()
    print(time()-start)
