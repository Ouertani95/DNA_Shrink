#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BWT module to encode and decode a sequence
"""

__author__ = 'Mohamed Ouertani'


class Bwt():

    """BWT transformer class to help with compression"""

    def __init__(self,input_sequence):
        self.input_sequence = input_sequence
        self.normal_sequence = None
        self.bwt_sequence = None

    def bwt_generator(self):

        """Generates the bwt encoded sequence"""
        if "$" in self.input_sequence:
            self.bwt_sequence = self.input_sequence
            print("the sequence is already bwt")
        else:
            actual_sequence = self.input_sequence + "$"
            sequence_len = len(actual_sequence)
            bwt_matrix = []
            for line_index in range(sequence_len):
                bwt_matrix.append(actual_sequence)
                yield "\n".join(bwt_matrix)
                actual_sequence = actual_sequence[-1] + actual_sequence[:-1]
            bwt_matrix.sort()
            yield "\n".join(bwt_matrix)
            self.bwt_sequence = "".join(list(iteration[sequence_len-1] for iteration in bwt_matrix))
            yield self.bwt_sequence


    def bwt_decoder(self):

        """Decodes a BWT sequence to recover original sequence"""
        if "$" not in self.input_sequence:
            self.normal_sequence = self.input_sequence
            print("sequence is already not bwt")
        else:
            self.bwt_sequence = self.input_sequence
            bwt_len = len(self.bwt_sequence)
            decoding_matrix = [""]*bwt_len
            split_bwt = list(self.bwt_sequence)
            for i in range(bwt_len):
                decoding_matrix = [i + j for i, j in zip(split_bwt, decoding_matrix)]
                yield "\n".join(decoding_matrix) 
                decoding_matrix.sort()
                yield "\n".join(decoding_matrix) 
            for dollar_sequence in decoding_matrix:
                if dollar_sequence[bwt_len-1] == "$":
                    self.normal_sequence = dollar_sequence[:-1]
                    break
            yield self.normal_sequence

    def is_bwt(self):
        return "$" in self.input_sequence

    