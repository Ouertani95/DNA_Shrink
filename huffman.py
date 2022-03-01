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
    def __init__(self,input_sequence):
        self.input_sequence = input_sequence
        if self.sequence_checker():
            self.original_sequence = input_sequence
            self.frequency_list = self.car_frequency()
            self.binary_tree = BinaryTree().tree_builder(self.frequency_list)
            self.coding_dict, self.decoding_dict = self.binary_tree.get_tree_leaves()
            self.huffman_sequence = None
        else:
            self.frequency_list = None
            self.binary_tree = None
            self.coding_dict,self.decoding_dict = None, None
            self.original_sequence = None
            self.huffman_sequence = input_sequence
        self.binary_sequence = None

    # @staticmethod
    # def file_reading(input_file):

    #     """Reads a sequence file and returns the sequence ready to be encoded"""

    #     caracters = ["A","T","G","C","N"]
    #     with open(input_file,"r") as file_input:
    #         raw_sequence = file_input.read()
    #     for car in raw_sequence:
    #         if car not in caracters:
    #             raw_sequence = raw_sequence.replace(car,"")
    #     print("input sequence : \n",raw_sequence)
    #     return raw_sequence7

    def sequence_checker(self):
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
        # coding_dict,_ = self.binary_tree.get_tree_leaves()
        print("initial sequence : ",self.original_sequence)
        print("coding dictionnary : ",self.coding_dict)
        print("decoding dictionnary : ",self.decoding_dict)
        self.binary_sequence = ""
        for nuc in self.original_sequence:
            self.binary_sequence += self.coding_dict[nuc]
        # print("coding dictionnary : ",coding_dict)
        # print("decoding dictionnary : ",decoding_dict)
        # print("initial sequence : ",sequence)
        # print("compressed sequence : ",coded_sequence)
        print("binary sequence  =  ",self.binary_sequence)
        return self.binary_sequence

    def binary_to_sequence(self):
        """Decompresses the sequence"""
        # _,decoding_dict = self.binary_tree.get_tree_leaves()
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

    def binary_to_char(self):
        """Transforms compressed binary sequence to 8 bit characters"""
        self.huffman_sequence = ""
        len_compressed = len(self.binary_sequence)
        i=0
        while i < len_compressed:
            if i+8 <= len_compressed:
                partial_sequence = self.binary_sequence[i:i+8]
                self.huffman_sequence += chr(int(partial_sequence,2))
                i = i+8
            else:
                partial_sequence = self.binary_sequence[i:len_compressed]
                self.huffman_sequence += chr(int(partial_sequence,2))
                break
        print("Compressed sequence : ",self.huffman_sequence)
        last_bits = len_compressed%8
        if last_bits == 0:
            print("last char number of bits : 8",)
        else:
            print("last char number of bits : ",last_bits)
        return self.huffman_sequence,last_bits,self.decoding_dict

    def char_to_binary(self,last_bits,decoding_dict):
        self.decoding_dict = decoding_dict
        self.binary_sequence = ""
        for index,char in enumerate(self.huffman_sequence):
            if index != len(self.huffman_sequence)-1:
                binary_char = str(format(ord(char),'b')).zfill(8)
            else:
                binary_char = str(format(ord(char),'b')).zfill(last_bits)
            self.binary_sequence += binary_char
        print("char to binary seq: ",self.binary_sequence)
        return self.binary_sequence

if __name__ == "__main__":
    
    #decoding,coding:
    huff = Huffman('·D\x06')
    decoding = {'00': 'A', '01': 'T', '10': 'C', '110': '$', '111': 'G'}
    rebinary_seq = huff.char_to_binary(4,decoding)
    original_seq = huff.binary_to_sequence()
    binary_seq = huff.sequence_to_binary()
    char_seq,last_bits,decode = huff.binary_to_char()
    print()
    print("--------------------------------------------------------")
    print()
    # #coding,decoding:
    # huff = Huffman("ACTTGATC")
    # binary_seq = huff.sequence_to_binary()
    # char_seq,last_bits = huff.binary_to_char()
    # rebinary_seq = huff.char_to_binary(last_bits,huff.decoding_dict)
    # original_seq = huff.binary_to_sequence()
    pass