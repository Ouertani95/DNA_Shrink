#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Huffman module to ...
"""

__author__ = 'Mohamed Ouertani'

from collections import Counter
from dnashrink.binary_tree import BinaryTree

class Huffman():
    """Huffman class for sequence compression / decompression"""
    def __init__(self,input_sequence,decoding_dict=None):
        self.input_sequence = input_sequence
        if self.sequence_checker():
            self.original_sequence = input_sequence
            self.frequency_list = self.car_frequency()
            self.binary_tree = BinaryTree().tree_builder(self.frequency_list)
            self.coding_dict, self.decoding_dict = self.binary_tree.get_tree_leaves()
            self.huffman_sequence = None
        else:
            self.original_sequence = None
            self.frequency_list = None
            self.binary_tree = None
            self.coding_dict,self.decoding_dict = None, decoding_dict
            self.huffman_sequence = input_sequence
        self.binary_sequence = None

    def sequence_checker(self):
        """Checks if sequence is uncompressed or not"""
        uncompressed = True
        for char in self.input_sequence:
            if char not in ["A","T","G","C","N","$"]:
                uncompressed = False
                break
        return uncompressed

    def car_frequency(self):
        """Calculates character frequencies in the sequence"""
        counts = Counter(self.original_sequence)
        counts_list = sorted(counts.items(), key=lambda x:x[1])
        print("frequency list : ",counts_list)
        return counts_list

    def sequence_to_binary(self):
        """Compresses the sequence into binary code"""
        self.binary_sequence = ""
        for nuc in self.original_sequence:
            self.binary_sequence += self.coding_dict[nuc]
        print("initial sequence : ",self.original_sequence)
        print("coding dictionnary : ",self.coding_dict)
        print("binary sequence  =  ",self.binary_sequence)
        return self.binary_sequence

    def binary_to_char(self):
        """Transforms compressed binary sequence to 8 bit characters"""
        self.huffman_sequence = ""
        len_binary = len(self.binary_sequence)
        i=0
        while i < len_binary:
            if i+8 <= len_binary:
                partial_sequence = self.binary_sequence[i:i+8]
                self.huffman_sequence += chr(int(partial_sequence,2))
                i = i+8
            else:
                partial_sequence = self.binary_sequence[i:len_binary]
                self.huffman_sequence += chr(int(partial_sequence,2))
                break

        print("Compressed sequence : ",self.huffman_sequence)
        # print(type(self.huffman_sequence))

        len_compressed = len(self.huffman_sequence)
        last_char = self.huffman_sequence[len_compressed-1]
        last_bits = len_binary%8

        if last_bits == 0:
            self.decoding_dict[last_char] = 8
        else:
            self.decoding_dict[last_char] = last_bits

        print("new decoding dictionnary : ",self.decoding_dict)

        return self.huffman_sequence,self.decoding_dict

    def char_to_binary(self):
        """Transforms a compressed sequence to binary"""
        self.binary_sequence = ""
        for index,char in enumerate(self.huffman_sequence):
            if index != len(self.huffman_sequence)-1:
                binary_char = str(format(ord(char),'b')).zfill(8)
            else:
                decoding_keys = list(self.decoding_dict.values())
                binary_char = str(format(ord(char),'b')).zfill(int(decoding_keys[-1]))
            self.binary_sequence += binary_char
        print("char to binary seq: ",self.binary_sequence)
        return self.binary_sequence

    def binary_to_sequence(self):
        """Decompresses the sequence"""
        print("decoding dictionnary : ",self.decoding_dict)
        self.original_sequence = ""
        seq_len = len(self.binary_sequence)
        i = 0
        len_sub = 1
        while i + len_sub <= seq_len:
            subbinary_sequence = self.binary_sequence[i:i+len_sub]
            if subbinary_sequence in self.decoding_dict.keys():
                self.original_sequence += self.decoding_dict[subbinary_sequence]
                i = i + len_sub
                len_sub = 1
            else:
                len_sub += 1
        self.frequency_list = self.car_frequency()
        self.binary_tree = BinaryTree().tree_builder(self.frequency_list)
        self.coding_dict, self.decoding_dict = self.binary_tree.get_tree_leaves()
        print("decompressed sequence : ",self.original_sequence)
        return self.original_sequence
