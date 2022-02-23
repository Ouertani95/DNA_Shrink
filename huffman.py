#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Huffman module to ...
"""

__author__ = 'Mohamed Ouertani'

from collections import Counter
from binary_tree import BinaryTree

class Huffman():
    """Huffman class for sequence compression / decompression"""
    def __init__(self,input_file):
        self.input_sequence = self.file_reading(input_file)
        self.frequency_list = self.car_frequency()
        self.binary_tree = BinaryTree().tree_builder(self.frequency_list)
        self.huffman_sequence = None

    @staticmethod
    def file_reading(input_file):

        """Reads a sequence file and returns the sequence ready to be encoded"""

        caracters = ["A","T","G","C","N"]
        with open(input_file,"r") as file_input:
            raw_sequence = file_input.read()
        for car in raw_sequence:
            if car not in caracters:
                raw_sequence = raw_sequence.replace(car,"")
        print("input sequence : \n",raw_sequence)
        return raw_sequence

    def car_frequency(self):
        """Calculates character frequencies in the sequence"""
        counts = Counter(self.input_sequence)
        counts_list = sorted(counts.items(), key=lambda x:x[1])
        print("frequency list : ",counts_list)
        return counts_list

    def sequence_to_binary(self):
        """Compresses the sequence into binary code"""
        coding_dict,_ = self.binary_tree.get_tree_leaves()
        print("coding dictionnary : ",coding_dict)
        binary_sequence = ""
        for nuc in self.input_sequence:
            binary_sequence += coding_dict[nuc]
        # print("coding dictionnary : ",coding_dict)
        # print("decoding dictionnary : ",decoding_dict)
        # print("initial sequence : ",sequence)
        # print("compressed sequence : ",coded_sequence)
        self.huffman_sequence = binary_sequence
        print("binary sequence  =  ",binary_sequence)
        return binary_sequence

    def binary_to_sequence(self):
        """Decompresses the sequence"""
        _,decoding_dict = self.binary_tree.get_tree_leaves()
        print("decoding dictionnary : ",decoding_dict)
        decoded_sequence = ""
        seq_len = len(self.huffman_sequence)
        i = 0
        len_sub = 1
        while i + len_sub <= seq_len:
            subbinary_sequence = self.huffman_sequence[i:i+len_sub]
            if subbinary_sequence in decoding_dict.keys():
                decoded_sequence += decoding_dict[subbinary_sequence]
                i = i + len_sub
                len_sub = 1
            else:
                len_sub += 1
        print("decompressed sequence : ",decoded_sequence)
        return decoded_sequence

    def binary_to_char(self):
        """Transforms compressed binary sequence to 8 bit characters"""
        char_list = []
        len_compressed = len(self.huffman_sequence)
        i=0
        while i < len_compressed:
            if i+8 <= len_compressed:
                partial_sequence = self.huffman_sequence[i:i+8]
                char_list.append(chr(int(partial_sequence,2)))
                i = i+8
            else:
                partial_sequence = self.huffman_sequence[i:len_compressed]
                char_list.append(chr(int(partial_sequence,2)))
                break
        print("list of chars from compressed sequence : ",char_list)
        last_bits = len_compressed%8
        if last_bits == 0:
            print("last char number of bits : 8",)
        else:
            print("last char number of bits : ",last_bits)
        return char_list
