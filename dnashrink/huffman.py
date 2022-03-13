#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Huffman module part of the dnashrink package to compress or 
decompress DNA sequences using the Huffman algorithm
"""

__author__ = 'Mohamed Ouertani'

# Standard library imports
from collections import Counter
# Local application imports
from dnashrink.binary_tree import BinaryTree

class Huffman():

    """
    Huffman class for sequence compression / decompression

    Attributes
    ----------
    input_sequence : str
        Initial sequence passed by the Model to be compressed/decompressed
    original_sequence : str
        Non-binary decompressed DNA sequence
    binary_tree : BinaryTree
        Binary tree created using the sequence
    coding_dict : Dict
        Dictionnary used for transforming DNA sequence to binary
    decoding_dict : Dict
        Dictionnary used for transforming binary sequence back to original DNA sequence
    huffman_sequence : str
        Final compressed sequence obtained after the Huffman compression algorithm 
    binary_sequence : str
        Intermediate binary sequence for compression and decompression steps
    """

    def __init__(self,input_sequence,decoding_dict=None) -> None:
        """
        Class constructor method for initializing all the attributes

        Parameters
        -----------
        input_sequence : str
            Sequence passed by the Model to be compressed/decompressed
        decoding_dict : dict (default = None)
            Dictionnary used for decompression if input sequence is already compressed

        Returns:
        ----------
        None
        """
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

    def sequence_checker(self) -> bool:
        """
        Class method for checking if input_sequence attribute is uncompressed or not

        Returns:
        ----------
        uncompressed : bool
            Boolean variable result for compression verification 
        """
        uncompressed = True
        for char in self.input_sequence:
            if char not in ["A","T","G","C","N","$"]:
                uncompressed = False
                break
        return uncompressed

    def car_frequency(self) -> list:
        """
        Class method to calculate character frequencies in the original_sequence attribute

        Returns:
        ----------
        counts_list : list[tuples]
            A list of all the characters in the original_sequence and their corresponding
            frequencies ordered in a descending order by frequencies 
        """
        #Count all character occurences in the sequence using Counter object
        counts = Counter(self.original_sequence)
        #Sort all the counted characters using their frequencies in a descending order
        counts_list = sorted(counts.items(), key=lambda x:x[1])
        return counts_list

    def sequence_to_binary(self) -> str:
        """
        Class method to transform the original_sequence nucleotides into binary code 
        using the coding_dict

        Returns:
        ----------
        binary_sequence : str
            Final binary sequence after transformation
        """
        self.binary_sequence = ""
        #Fill binary_sequence with binary code corresponding to each nucleotide from coding_dict
        for nuc in self.original_sequence:
            self.binary_sequence += self.coding_dict[nuc]
        return self.binary_sequence

    def binary_to_char(self) -> str:
        """
        Class method to transform binary_sequence by taking 8 bits at a time 
        and converting them to their corresponding Char using UTF-8 encoding

        Returns:
        ----------
        huffman_sequence : str
            The final compressed sequence of the Huffman compression algorithm
        decoding_dict : Dict
            The new decoding dictionnary with the last Char number of bits needed
            for decompressing the sequence
        """
        self.huffman_sequence = ""
        len_binary = len(self.binary_sequence)
        i=0
        #Transforming the binary sequence to Char sequence
        while i < len_binary:
            if i+8 <= len_binary: 
                partial_sequence = self.binary_sequence[i:i+8]
                self.huffman_sequence += chr(int(partial_sequence,2))
                i = i+8
            else: #Condition for the last Char transformation
                partial_sequence = self.binary_sequence[i:len_binary]
                self.huffman_sequence += chr(int(partial_sequence,2))
                break

        #Calculating the number of bits of the last Char
        len_compressed = len(self.huffman_sequence)
        last_char = self.huffman_sequence[len_compressed-1]
        last_bits = len_binary%8

        #Adding the last character and it's number of bits to decoding_dict
        if last_bits == 0:
            self.decoding_dict[last_char] = 8
        else:
            self.decoding_dict[last_char] = last_bits

        return self.huffman_sequence,self.decoding_dict

    def char_to_binary(self) -> str:
        """
        Class method to transform a compressed sequence to binary
        
        Returns:
        ----------
        binary_sequence : str
            Intermediate binary sequence obtained from decompressing the Huffman_sequence
        """
        #Transforming the Char sequence to binary sequence
        self.binary_sequence = ""
        for index,char in enumerate(self.huffman_sequence):
            if index != len(self.huffman_sequence)-1:
                #Transform Char to binary int and fill first characters with 0 to obtain 8 bit code
                binary_char = str(format(ord(char),'b')).zfill(8)
            else: 
                #Replace the last Char by binary equivalent with number of bits from decoding_dict
                decoding_keys = list(self.decoding_dict.values())
                binary_char = str(format(ord(char),'b')).zfill(int(decoding_keys[-1]))
            #Add partial binary seq to binary_sequence
            self.binary_sequence += binary_char
        return self.binary_sequence

    def binary_to_sequence(self) -> str:
        """
        Class method for the final step of decompressing the sequence

        Returns:
        ----------
        original sequence : str
            The final decompressed sequence obtained using the Huffman algorithm
        """
        self.original_sequence = ""
        sequence_length = len(self.binary_sequence)
        i = 0
        length_subsequence = 1
        #Transforming the binary sequence to original DNA sequence
        while i + length_subsequence <= sequence_length:
            subbinary_sequence = self.binary_sequence[i:i+length_subsequence]
            if subbinary_sequence in self.decoding_dict.keys():
                #If subsequence is in dictionnary add the corresponding value to original_sequence
                self.original_sequence += self.decoding_dict[subbinary_sequence]
                i = i + length_subsequence
                length_subsequence = 1
            else: #If subsequence is not in the dictionnary increase it's length
                length_subsequence += 1
        #Calculate frequency of new original_sequence
        self.frequency_list = self.car_frequency()
        #Build BinaryTree corresonding to new original_sequence
        self.binary_tree = BinaryTree().tree_builder(self.frequency_list)
        #Create new coding and decoding dictionnaries
        self.coding_dict, self.decoding_dict = self.binary_tree.get_tree_leaves()
        return self.original_sequence
