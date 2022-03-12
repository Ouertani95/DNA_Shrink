#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Model module to manipulate the data
"""

__author__ = 'Mohamed Ouertani'

import os
from dnashrink.bwt import Bwt
from dnashrink.huffman import Huffman


class Model():

    """Model class"""

    def __init__(self,controller):
        self.controller = controller

        self.bwt_handler = None
        self.huffman_handler = None

        self.input_sequence = None
        self.decoding_dict = None

        self.current_file = None
        self.current_sequence = None
        self.current_function = None

        self.bwt_status = None
        
        
        


    def file_loader(self,input_file,file_name):
        self.input_sequence = self.sequence_extractor(input_file)
        self.current_file = file_name
        print(self.current_file)
        self.current_sequence = self.input_sequence
        if self.is_uncompressed():
            self.bwt_handler = Bwt(self.input_sequence)
            if self.bwt_handler.input_is_bwt():
                self.bwt_status = True
            else:
                self.bwt_status = False
        else:
            self.bwt_handler = None
        self.huffman_handler = Huffman(self.input_sequence,self.decoding_dict)
        return self.current_sequence
    

    def sequence_extractor(self,input_file):
        """Reads a sequence file and returns the sequence ready to be encoded"""

        with open(input_file,"r") as file_input:
            all_lines = file_input.readlines()
            raw_sequence = all_lines[0]
        raw_sequence = raw_sequence.replace(" ","")
        raw_sequence = raw_sequence.replace("\n","")
        if len(all_lines)>1:
            string_dict = all_lines[1]
            self.string_to_dict(string_dict)
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
        binary_sequence = self.huffman_handler.sequence_to_binary()
        huffman_sequence, decoding_dict = self.huffman_handler.binary_to_char()
        self.current_sequence = huffman_sequence
        self.decoding_dict = decoding_dict
        return self.current_sequence , binary_sequence

    def decompress_sequence(self):
        binary_sequence = self.huffman_handler.char_to_binary()
        decompressed_sequence = self.huffman_handler.binary_to_sequence()
        self.bwt_handler = Bwt(decompressed_sequence)
        self.current_sequence = decompressed_sequence
        return self.current_sequence,binary_sequence

    def sequence_to_bwt(self):
        yield from self.bwt_handler.bwt_generator()
        bwt_sequence = list(self.bwt_handler.bwt_generator())[-1]
        self.current_sequence = bwt_sequence
        self.huffman_handler = Huffman(bwt_sequence)
        self.bwt_handler = Bwt(bwt_sequence)
        self.bwt_status = True

    def bwt_to_sequence(self):
        yield from self.bwt_handler.bwt_decoder()
        original_sequence = list(self.bwt_handler.bwt_decoder())[-1]
        self.current_sequence = original_sequence
        self.huffman_handler = Huffman(original_sequence)
        self.bwt_handler = Bwt(original_sequence)
        self.bwt_status = False
        

    def save_file(self):
        if not os.path.exists("./data"):
            os.mkdir("./data")
        if self.is_uncompressed():
            if "$" in self.current_sequence:
                file_name = f"{self.current_file}_bwt.txt"
                with open (f"./data/{file_name}","w") as bwt_output:
                    bwt_output.write(self.current_sequence)
            else:
                file_name = f"{self.current_file}_original.txt"
                with open (f"./data/{file_name}","w") as original_output:
                    original_output.write(self.current_sequence)
        else:
            if self.bwt_status:
                file_name = f"{self.current_file}_bwt_huffman.txt"
            else:
                file_name = f"{self.current_file}_huffman.txt"
            string_dict = self.dict_to_string()
            with open (f"./data/{file_name}","w") as huffman_output:
                huffman_output.writelines([self.current_sequence,"\n",string_dict])
        return file_name


    def update_current_function(self,function):
        self.current_function = function


    def get_current_sequence(self):
        return self.current_sequence


    def dict_to_string(self):
        string_dict = ""
        for i,j in self.decoding_dict.items():
            string_dict += f"{i}:{j},"
        return string_dict


    def string_to_dict(self,string_dict):
        dict_elements = string_dict.split(",")
        dict_elements = dict_elements[:-1]
        print(dict_elements)
        self.decoding_dict = {}
        for i in dict_elements:
            temp_items = i.split(":")
            self.decoding_dict[temp_items[0]]=temp_items[1]
