#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Node and BinaryTree Classes used for the Huffman compression/decompression steps
"""

__author__ = 'Mohamed Ouertani'


class Node:

    """
    Node class used for Tree construction

    Attributes
    ----------
    freq : int
        Represents the frequency of each character in a given sequence or a cumulative
        frequency Node while assembling the tree
    car : str (default : None)
        Represents the character present in the sequence or could be None for a cumulative Node
    zero : Node
        Represents the zero branch for the path construction of tree leaves; Could be associated
        to a Node or could be empty/None
    one : Node
        Represents the one branch for the path construction of tree leaves; Could be associated
        to a Node or could be empty/None
    """

    def __init__(self, freq,car=None) -> None:
        """
        Class constructor method for initializing all the attributes

        Parameters
        -----------
        freq : int
            Frequency input for the creation of the Node which is mandatory
        car : car
            Character to be assigned to the Node which could be None if not precised

        Returns:
        ----------
        None
        """
        self.freq = freq
        self.car = car
        self.zero = None
        self.one = None

    def get_freq(self) -> int:
        """
        Class method that gets node frequency value

        Returns:
        ----------
        freq : int
            Frequency attribute of the Node
        """
        return self.freq

    def get_car(self) -> str:
        """
        Class method that gets character assigned to the Node

        Returns:
        ----------
        car : int
            character attribute of the Node
        """
        return self.car

    def get_zero(self):
        """
        Class method to get node assigned to zero branch

        Returns:
        ----------
        zero : Node
            Node Object assigned to zero branch
        """
        return self.zero

    def set_zero(self,node) -> None:
        """
        Class method that assigns a Node to zero branch

        Parameters
        -----------
        node : Node
            Represents the Node object to be assigned to the zero branch

        Returns:
        ----------
        None
        """
        self.zero = node

    def get_one(self):
        """
        Class method to get node assigned to one branch

        Returns:
        ----------
        one : Node
            Node Object assigned to one branch
        """
        return self.one

    def set_one(self,node):
        """
        Class method that assigns a Node to one branch

        Parameters
        -----------
        node : Node
            Represents the Node object to be assigned to the one branch

        Returns:
        ----------
        None
        """
        self.one = node

    def print_node(self) -> None:
        """
        Class recursive method that prints the node and all it's subnodes

        Returns:
        ----------
        None
        """
        print(self)
        if self.zero:
            self.zero.print_node()
        if self.one:
            self.one.print_node()

    def is_leaf(self) -> bool:
        """
        Class method that verifies if a node is a leaf

        Returns:
        ----------
        bool
        """
        if self.zero is None and self.one is None:
            return True
        return False

    def get_leaves(self,binary_tree,car_code="") -> dict:
        """
        Class recursive method that gets all leaves of the Node
        This method also fills the coding and decoding leaves while searching
        for the leaves of the binary tree

        Parameters
        -----------
        binary_tree :
            BinaryTree Object from which to extract the leaves; could be the head node of
            that tree
        car_code :
            Represents the path to a certain leaf inside the tree. It is initialized to an empty
            string at the start of the method

        Returns:
        ----------
        coding_dict : dict
            Dictionnary that will be used for the compression steps of the Huffman algorithm
        decoding_dict : dict
            Dictionnary that will be used for the decompression steps of the Huffman algorithm
        """
        #Initialize code for path
        code = car_code
        #Verify if Node is a leaf
        if (not self.zero and
            not self.one):
            #If Node is a leaf fill the dictionnaries with it's values
            binary_tree.coding_dic[self.car] = code
            binary_tree.decoding_dic[code] = self.car
            return binary_tree.coding_dic , binary_tree.decoding_dic
        #Verify if leaf has a Node assigned to zero branch
        if self.zero:
            #Add 0 to leaf path
            code += "0"
            #Call recursive method on zero Node
            self.zero.get_leaves(binary_tree,code)
        #Verify if leaf has a Node assigned to one branch
        if self.one:
            #Remove last digit and add 1 to leaf path
            code = code[:-1]
            code += "1"
            #Call recursive method on one Node
            self.one.get_leaves(binary_tree,code)
        return binary_tree.coding_dic , binary_tree.decoding_dic

    def __str__(self) -> str:
        """
        Class method used to format displayed content when print is called on Node object

        Returns:
        ----------
        str :
            Represents the character and frequency of the Node
        """
        return f"{self.get_car()} , {self.get_freq()}"

class BinaryTree():

    """
    BinaryTree class for the huffman compression/decompression

    Attributes
    ----------
    head_node : Node
        Represents the top Node of the tree
    coding_dic : dict
        Compression dictionnary extracted from the creation of the tree
    decoding_dic : dict
        Decompression dictionnary extracted from the creation of the tree
    """

    def __init__(self):
        """
        Class constructor method for initializing all the attributes

        Returns:
        ----------
        None
        """
        self.head_node = None
        self.coding_dic = {}
        self.decoding_dic = {}

    def tree_builder(self,list_frequencies):
        """
        Class method that builds the tree nodes according to frequency list

        Parameters
        -----------
        list_frequencies : list[int]
            An list of all the characters and their corresponding frequencies which is in
            a descending order by the frequencies

        Returns:
        ----------
        BinaryTree :
            Represents the final built BinaryTree Object
        """
        i = 0
        while i < len(list_frequencies):
            #Check if the tree is empty
            if self.head_node is None :
                #Calculate the frequency of the cumulative Node using the 2 lowest frequencies
                head_freq = list_frequencies[i][1] + list_frequencies[i+1][1]
                #Create the cumulative Node
                self.head_node = Node(head_freq)
                #Assign the 2 Nodes with lowest frequencies to zero and one branches
                self.head_node.set_zero(Node(list_frequencies[i][1],list_frequencies[i][0]))
                self.head_node.set_one(Node(list_frequencies[i+1][1],list_frequencies[i+1][0]))
                #Skip the 2 used Nodes
                i += 2
            #Check if only 2 Nodes are left to add
            elif i == len(list_frequencies)-2:
                #Assign previous head Node to first sister Node
                first_sibling = self.head_node
                #Caluclate the sum of the last 2 frequencies
                last_two_freq = list_frequencies[i][1] + list_frequencies[i+1][1]
                #Create the second sister Node
                second_sibling = Node(last_two_freq)
                #Assign the 2 last Nodes to zero and one branches
                second_sibling.set_zero(Node(list_frequencies[i][1],list_frequencies[i][0]))
                second_sibling.set_one(Node(list_frequencies[i+1][1],list_frequencies[i+1][0]))
                #Create the last head Node
                self.head_node = Node(first_sibling.get_freq() + second_sibling.get_freq())
                #Assign the 2 sister Nodes to zero and one branches
                self.head_node.set_zero(second_sibling)
                self.head_node.set_one(first_sibling)
                break
            else:
                #Assign previous head Node to first sister Node
                first_sibling = self.head_node
                #Create the second sister Node
                second_sibling = Node(list_frequencies[i][1],list_frequencies[i][0])
                #Caluclate the sum of the last 2 frequencies
                head_freq = first_sibling.get_freq() + second_sibling.get_freq()
                #Create the new head Node
                self.head_node = Node(head_freq)
                #Assign the 2 sister Nodes to zero and one branches of head Node
                self.head_node.set_zero(second_sibling)
                self.head_node.set_one(first_sibling)
                i += 1
        print("Frequency tree :\n",self)
        return self

    def get_tree_leaves(self) -> dict:
        """
        Class method that gets all tree leaves and creates coding/decoding dictionnaries
        This method calls the get_leaves method of the head_node attribute

        Returns:
        ----------
        coding_dic : dict
            Compression dictionnary extracted from the creation of the tree
        decoding_dic : dict
            Decompression dictionnary extracted from the creation of the tree
        """
        self.coding_dic , self.decoding_dic = self.head_node.get_leaves(self)
        return self.coding_dic , self.decoding_dic


    def __str__(self) -> str:
        """
        Class method used to format displayed content when print
        is called on BinarTree object

        Returns:
        ----------
        str :
            Represents the print_node method of the head Node which prints the entire
            Nodes and sub Nodes of the BinaryTree Object
        """
        return str(self.head_node.print_node())
