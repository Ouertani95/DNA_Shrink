#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BWT module part of the dnashrink package to restructure DNA sequences
and make them more compressible
"""

__author__ = 'Mohamed Ouertani'

from typing import Generator

class Bwt():

    """A class to represent the Burrows-Wheeler tranform algorithm
    which help with the compression of the DNA sequences

    Attributes
    ----------
    input_sequence : str
        Input sequence passed by the Model to be transformed
    normal_sequence : str
        Original sequence obtained after reverse Burrows-Wheeler Transform
    bwt_sequence : str
        Bwt sequence obtained after Burrows-Wheeler Transform
    """

    def __init__(self,input_sequence:str) -> None:
        """
        Class method for Creation of interface and all the widgets inside
        
        Parameters
        -----------
        input_sequence : str
            input sequence to be transformed or reverse transformed 
            using Burrows-Wheeler algorithm
        
        Returns:
        ----------
        None
        """
        self.input_sequence = input_sequence
        self.normal_sequence = None
        self.bwt_sequence = None

    def bwt_generator(self) -> Generator:

        """
        Class method that returns all the steps of the Burrows-Wheeler Transform 
        from a created Burrows-Wheeler matrix using the input sequence.
        The Burrows-Wheeler Transform corresponds to the last column of the matrix.

        Input
        ----------
        self.input_sequence : str

        Returns
        -------
        Generator :
            The Burrows-Wheeler Transform steps
        """
        #Adding $ to the end of the input_sequence
        dollar_sequence = self.input_sequence + "$"
        sequence_length = len(dollar_sequence)
        bwt_list = []
        #Transforming the dollar_sequence into bwt_sequence
        for _ in range(sequence_length):
            #Adding the sequence to the bwt_list
            bwt_list.append(dollar_sequence)
            #Returning the current bwt_list
            yield "\n".join(bwt_list)
            #Rotating the dollar_sequence by one character
            dollar_sequence = dollar_sequence[-1] + dollar_sequence[:-1]
        bwt_list.sort()
        #Returning the final sorted bwt_list
        yield "\n".join(bwt_list)
        #Getting the last character of each line to form the bwt_sequence
        self.bwt_sequence = "".join(list(rotation[sequence_length-1] for rotation in bwt_list))
        #Returning the obtained bwt_sequence
        yield self.bwt_sequence


    def bwt_decoder(self) -> Generator:

        """
        Class method for decoding a BWT sequence to recover original sequence

        Returns
        -------
        Generator :
            The Burrows-Wheeler reverse transformation steps
        """
        
        self.bwt_sequence = self.input_sequence
        bwt_length = len(self.bwt_sequence)
        #Filling decoding list with empty string
        decoding_list = [""]*bwt_length
        #Split the bwt_sequence to a list of single characters
        split_bwt = list(self.bwt_sequence)
        #Generate the bwt reverse transformation matrix
        for _ in range(bwt_length):
            #Adding the bwt_list characters at the start of each line
            decoding_list = [i + j for i, j in zip(split_bwt, decoding_list)]
            #returning the current list before sort
            yield "\n".join(decoding_list)
            decoding_list.sort()
            #returning the current matrix after sort
            yield "\n".join(decoding_list)
        #Getting the line wih $ at the end
        for dollar_sequence in decoding_list:
            if dollar_sequence[bwt_length-1] == "$":
                #Removing the dollar at the end of the sequence
                self.normal_sequence = dollar_sequence[:-1]
                break
        #Returning the original sequence obtained from the reverse transformation
        yield self.normal_sequence

    def input_is_bwt(self) -> bool:
        """
        Class method for checking if input_sequence is bwt or not

        Returns
        -------
        bool : 
            Result of bwt verification
        """
        return "$" in self.input_sequence
