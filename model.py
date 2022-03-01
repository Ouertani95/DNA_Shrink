#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Model module to manipulate the data
"""

__author__ = 'Mohamed Ouertani'

from bwt import Bwt
from huffman import Huffman

class Model():

    """Model class"""

    def __init__(self,controller):
        self.controller = controller
        self.bwt_handler = None
        self.huffman_handler = None
        self.input_sequence = None
        self.current_sequence = None
        
        #TODO : add self.actual_sequence , self.decompression_dict
        #decompression dict could contain also the last char number of bits

    def file_loader(self,input_file):
        self.input_sequence = self.sequence_extractor(input_file)
        self.current_sequence = self.input_sequence
        if self.is_uncompressed():
            self.bwt_handler = Bwt(self.input_sequence)
        else:
            self.bwt_handler = None
        self.huffman_handler = Huffman(self.input_sequence)
        return self.current_sequence
    

    def sequence_extractor(self,input_file):
        """Reads a sequence file and returns the sequence ready to be encoded"""

        with open(input_file,"r") as file_input:
            raw_sequence = file_input.read()
        raw_sequence = raw_sequence.replace(" ","")
        print("input sequence : \n",raw_sequence)
        return raw_sequence

    def is_uncompressed(self):
        uncompressed = True
        for char in self.current_sequence:
            if char not in ["A","T","G","C","N","$"]:
                uncompressed = False
                break
        return uncompressed

    def compress_sequence(self):
        self.huffman_handler.sequence_to_binary()
        huffman_sequence, _ = self.huffman_handler.binary_to_char()
        #deactivate all bwt buttons and compression button
        #only decompress and save will be available
        self.current_sequence = huffman_sequence
        return self.current_sequence

    def decompress_sequence(self):
        self.huffman_handler.char_to_binary()
        decompressed_sequence = self.huffman_handler.binary_to_sequence()
        self.bwt_handler = Bwt(decompressed_sequence)
        #deactivate decompress button
        #activate compress and save
        #if sequence is bwt activate bwt_to_sequence button
        #if sequence is normal activate sequence_to_bwt
        self.current_sequence = decompressed_sequence
        return self.current_sequence

    def sequence_to_bwt(self):
        bwt_sequence = self.bwt_handler.bwt_generator()
        self.huffman_handler = Huffman(bwt_sequence)
        #deactivate sequence_to_bwt button
        self.current_sequence = bwt_sequence
        return self.current_sequence

    def bwt_to_sequence(self):
        original_sequence = self.bwt_handler.bwt_decoder()
        self.huffman_handler = Huffman(original_sequence)
        self.current_sequence = original_sequence
        return self.current_sequence

    def save_file(self,status):
        if "Uncompressed" in status:
            if "$" in self.current_sequence:
                with open ("test_bwt.txt","w") as bwt_output:
                    bwt_output.write(self.current_sequence)
            else:
                with open ("test_original.txt","w") as original_output:
                    original_output.write(self.current_sequence)
        else:
            pass

if __name__ == "__main__":
    test_model = Model("NC_009513.1_copy.fasta")
    test_model.handle_uncompressed(0)
    print("-------------------------------------------------------------------")
    test_model.handle_uncompressed(1)
    print("-------------------------------------------------------------------")
    test_model.handle_uncompressed(2)