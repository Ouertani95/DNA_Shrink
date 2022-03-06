#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Model module to manipulate the data
"""

__author__ = 'Mohamed Ouertani'

from bwt import Bwt
from huffman import Huffman
import pickle

class Model():

    """Model class"""

    def __init__(self,controller):
        self.controller = controller
        self.bwt_handler = None
        self.huffman_handler = None
        self.current_file = None
        self.input_sequence = None
        self.current_sequence = None
        self.decoding_dict = None
        self.current_function = None
        
        #TODO : add self.actual_sequence , self.decompression_dict
        #decompression dict could contain also the last char number of bits

    def file_loader(self,input_file,file_name):
        self.input_sequence = self.sequence_extractor(input_file)
        self.current_file = file_name
        print(self.current_file)
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
        huffman_sequence, decoding_dict = self.huffman_handler.binary_to_char()
        #deactivate all bwt buttons and compression button
        #only decompress and save will be available
        self.current_sequence = huffman_sequence
        self.decoding_dict = decoding_dict
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
        yield from self.bwt_handler.bwt_generator()
        bwt_sequence = list(self.bwt_handler.bwt_generator())[-1]
        self.current_sequence = bwt_sequence
        self.huffman_handler = Huffman(bwt_sequence)
        self.bwt_handler = Bwt(bwt_sequence)

    def bwt_to_sequence(self):
        yield from self.bwt_handler.bwt_decoder()
        original_sequence = list(self.bwt_handler.bwt_decoder())[-1]
        self.current_sequence = original_sequence
        self.huffman_handler = Huffman(original_sequence)
        self.bwt_handler = Bwt(original_sequence)
        

    def save_file(self):
        if self.is_uncompressed():
            if "$" in self.current_sequence:
                with open (f"{self.current_file}_bwt.txt","w") as bwt_output:
                    bwt_output.write(self.current_sequence)
            else:
                with open (f"{self.current_file}_original.txt","w") as original_output:
                    original_output.write(self.current_sequence)
        else:
            with open (f"{self.current_file}_huffman.txt","w") as huffman_output:
                huffman_output.write(self.current_sequence)
            with open(f"{self.current_file}_decoding_dict.pickle", "wb") as decoding_output:
                pickle.dump(self.decoding_dict,decoding_output)

    def update_current_function(self,function):
        self.current_function = function

    def get_current_sequence(self):
        return self.current_sequence