#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Model module part of the MVC architechture that represents the component
interacting and manipulating the data directly under the commands of the Controller
"""

__author__ = 'Mohamed Ouertani'

import os
from typing import Generator
from dnashrink.bwt import Bwt
from dnashrink.huffman import Huffman


class Model():

    """
    Model class to manipulate all the data in the program

    Attributes
    ----------
    controller : Controller
        Controller object that calls the model
    bwt_handler : Bwt
        Bwt object to be called for Burrows-Wheeler transform
        and reverse transform on DNA sequences
    huffman_handler : Huffman
        Huffman object to be called for Huffman compression and
        decompression of DNA sequences
    decoding_dict : dict
        Dictionnary necessary for Decompression of DNA sequences
    current_file : str
        Currently used file name without extension used for saving files
    current_sequence : str
        Sequence being treated inside the program
    current_function : method
        Function being used to transform the current_sequence
    bwt_status : bool
        Current state of the sequence : BWT or Normal
    """

    def __init__(self,controller) -> None:
        """
        Class method for Creation of interface and all the widgets inside

        Parameters
        -----------
        controller : Controller
            Controller Object coordinating between the model and view

        Returns:
        ----------
        None
        """
        self.controller = controller
        self.bwt_handler = None
        self.huffman_handler = None
        self.decoding_dict = None
        self.current_file = None
        self.current_sequence = None
        self.current_function = None
        self.bwt_status = None
        self.create_save_directory()

    def file_loader(self,input_file,file_name) -> str:
        """
        Class method to load file into model object and update attributes

        Returns:
        ----------
        current_sequence : str
            Sequence being transformed inside the program
        """
        #Load new file name
        self.current_file = file_name
        #Extract sequence from file using sequence_extractor method
        self.current_sequence = self.sequence_extractor(input_file)
        #Conditional update of attributes
        if self.is_uncompressed():
            self.bwt_handler = Bwt(self.current_sequence)
            if self.bwt_handler.input_is_bwt():
                self.bwt_status = True
            else:
                self.bwt_status = False
        else:
            self.bwt_handler = None
        self.huffman_handler = Huffman(self.current_sequence,self.decoding_dict)
        return self.current_sequence


    def sequence_extractor(self,input_file) -> str:
        """
        Class method to read a sequence file and extract the sequence inside

        Parameters
        -----------
        input_file : str
            path of file from which the sequence will be extracted

        Returns:
        ----------
        raw_sequence : str
            Sequence extracted from the input file
        """
        #Open input_file in read mode
        with open(input_file,"r") as file_input:
            #Create a list of strings representing all the lines inside the file
            all_lines = file_input.readlines()
        #Verify is file contains string_dictionnary or not
        if ":" in all_lines[-1] and "," in all_lines[-1]:
            #Recover the full DNA sequence
            raw_sequence = "".join(all_lines[0:len(all_lines)-1])
            #Recover the last line representing the decoding_dict in string format
            string_dict = all_lines[-1]
            #Convert dictionnary from string format to original format
            self.string_to_dict(string_dict)
        else:
            #Recover the full DNA sequence
            raw_sequence = "".join(all_lines)
        #Clean the sequence by removing spaces and backlines
        raw_sequence = raw_sequence.replace(" ","")
        raw_sequence = raw_sequence.replace("\n","")

        return raw_sequence

    def is_uncompressed(self) -> bool:
        """
        Class method that verifies if a sequence is uncompressed

        Returns:
        ----------
        bool :
            Verification result of compression status of self.current_sequence
        """
        for char in self.current_sequence:
            if char not in ["A","T","G","C","N","$"]:
                return False
        return True


    def compress_sequence(self) -> str:
        """
        Class method that compresses the current sequence

        Returns:
        ----------
        current_sequence : str
            Final Char sequence after compression
        binary_sequence : str
            Intermediate binary sequence used for compression
        """
        #Transform current_sequence to binary_sequence
        binary_sequence = self.huffman_handler.sequence_to_binary()
        #Transfotm binary_sequence to Char sequence
        huffman_sequence, decoding_dict = self.huffman_handler.binary_to_char()
        #Update model attributes
        self.current_sequence = huffman_sequence
        self.decoding_dict = decoding_dict
        return self.current_sequence , binary_sequence

    def decompress_sequence(self) -> str:
        """
        Class method that decompresses the current sequence

        Returns:
        ----------
        current_sequence : str
            Final Char sequence after decompression
        binary_sequence : str
            Intermediate binary sequence used for decompression
        """
        #Transform current_sequence to binary_sequence
        binary_sequence = self.huffman_handler.char_to_binary()
        #Transform binary_sequence to original_sequence
        decompressed_sequence = self.huffman_handler.binary_to_sequence()
        #Update bwt_handler with new sequence
        self.bwt_handler = Bwt(decompressed_sequence)
        #Update current_sequence
        self.current_sequence = decompressed_sequence
        return self.current_sequence,binary_sequence

    def sequence_to_bwt(self) -> Generator:
        """
        Class method that transforms normal_sequence to bwt_sequence

        Returns:
        ----------
        Generator :
            When called returns the results of bwt transformation step by steps
        """
        #Return bwt generation steps one by one
        yield from self.bwt_handler.bwt_generator()
        #Recover final result of transformation directly
        bwt_sequence = list(self.bwt_handler.bwt_generator())[-1]
        #Update model attribuutes using new bwt_sequence
        self.current_sequence = bwt_sequence
        self.huffman_handler = Huffman(bwt_sequence)
        self.bwt_handler = Bwt(bwt_sequence)
        self.bwt_status = True

    def bwt_to_sequence(self) -> Generator:
        """
        Class method that transforms bwt_sequence to normal_sequence

        Returns:
        ----------
        Generator :
            When called returns the results of bwt reverse transformation step by steps
        """
        #Return reverse bwt transformation steps one by one
        yield from self.bwt_handler.bwt_decoder()
        #Recover last result of bwt transformation directly
        original_sequence = list(self.bwt_handler.bwt_decoder())[-1]
        #Update model attribuutes using new normal_sequence
        self.current_sequence = original_sequence
        self.huffman_handler = Huffman(original_sequence)
        self.bwt_handler = Bwt(original_sequence)
        self.bwt_status = False


    def save_file(self) -> str:
        """
        Class method that saves the current sequence into .txt file

        Returns:
        ----------
        file_name : str
            Name of the file that was saved in data directory
        """
        #Verify if sequence is compressed and save file accordingly
        if self.is_uncompressed():
            #Verify is sequence is bwt or not
            if "$" in self.current_sequence:
                file_name = f"{self.current_file}_bwt.txt"
                with open (f"./data/{file_name}","w") as bwt_output:
                    bwt_output.write(self.current_sequence)
            else:
                file_name = f"{self.current_file}_original.txt"
                with open (f"./data/{file_name}","w") as original_output:
                    original_output.write(self.current_sequence)
        else:
            #Verify is sequence was bwt or not before compression
            if self.bwt_status:
                file_name = f"{self.current_file}_bwt_huffman.txt"
            else:
                file_name = f"{self.current_file}_huffman.txt"
            string_dict = self.dict_to_string()
            with open (f"./data/{file_name}","w") as huffman_output:
                huffman_output.writelines([self.current_sequence,"\n",string_dict])
        return file_name


    def update_current_function(self,function) -> None:
        """
        Class method to update the current_function arrtibute
        This attribute is useful for the step_by_step method in Controller

        Parameters
        -----------
        function : method
            Current function being used in view to display results

        Returns:
        ----------
        None
        """
        self.current_function = function


    def get_current_sequence(self) -> str:
        """
        Class method used to get the current sequence

        Returns:
        ----------
        current_sequence : str
            Actual sequence being transformed in the program
        """
        return self.current_sequence


    def dict_to_string(self) -> str:
        """
        Class method that transforms a decoding_dict into a string for the saving process

        Input
        ----------
        decoding_dict : dict
            Dictionnary used for the decompression process

        Returns:
        ----------
        string_dict : str
            Decoding_dict transformed into string format for lighter save
        """
        string_dict = ""
        for i,j in self.decoding_dict.items():
            string_dict += f"{i}:{j},"
        return string_dict


    def string_to_dict(self,string_dict) -> None:
        """
        Class method that converts a decoding_dict from string
        format to a dictionnary for the decompression of the sequence

        Parameters
        -----------
        string_dict : str
            Decoding_dict in string format to be converted into a dictionnary

        Returns:
        ----------
        None
        """
        #Split the string using , separator
        dict_elements = string_dict.split(",")
        #Remove the last , :
        dict_elements = dict_elements[:-1]
        self.decoding_dict = {}
        #Fill the dictionnary with the original values
        for i in dict_elements:
            #Split key and value using : separator
            temp_items = i.split(":")
            #Fill the dictionnary
            self.decoding_dict[temp_items[0]]=temp_items[1]
    
    @staticmethod
    def create_save_directory() -> None:
        """
        Class method used for creating the save directory on startup

        Returns:
        ----------
        None
        """
        #verify if data directory exits / if not create it
        if not os.path.exists("./data"):
            #Using bash mkdir equivalent to create data folder
            os.mkdir("./data")

