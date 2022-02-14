#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Node and BinaryTree Classes
"""

__author__ = 'Mohamed Ouertani'


from pickle import FALSE


class Node:
    def __init__(self, freq,car=None):
        self.freq = freq 
        self.car = car 
        self.zero = None
        self.one = None

    def get_freq(self):
        return self.freq

    def get_car(self):
        return self.car

    def get_zero(self):
        return self.zero

    def set_zero(self,node):
        self.zero = node

    def get_one(self):
        return self.one

    def set_one(self,node):
        self.one = node

    def print_node(self):
        print(self)
        if self.zero:
            self.zero.print_node()
        if self.one:
            self.one.print_node()

    def is_leaf(self):
        if self.zero is None and self.one is None:
            return True
        return False
    
    def get_leaf(self,car,car_code=""):
        code = car_code
        if self.car == car:
            print("WE MADE IT !!!")
            print(code)
            final_code = code
            return final_code
        if self.zero:
            code += "0"
            self.zero.get_leaf(car,code)
            code = code[:-1]
        if self.one:
            code += "1"
            self.one.get_leaf(car,code)
            code = code[:-1]


    def __str__(self):
        return f"{self.get_car()} , {self.get_freq()}"

class BinaryTree():
    def __init__(self):
        self.head_node = None
    
    def tree_builder(self,list_frequencies):
        i = 0
        while i < len(list_frequencies):
            if self.head_node is None :
                head_freq = list_frequencies[i][1] + list_frequencies[i+1][1]
                self.head_node = Node(head_freq)
                self.head_node.set_zero(Node(list_frequencies[i][1],list_frequencies[i][0]))
                self.head_node.set_one(Node(list_frequencies[i+1][1],list_frequencies[i+1][0]))
                i += 2
            elif i == len(list_frequencies)-2:
                first_sibling = self.head_node
                last_two_freq = list_frequencies[i][1] + list_frequencies[i+1][1]
                second_sibling = Node(last_two_freq)
                second_sibling.set_zero(Node(list_frequencies[i][1],list_frequencies[i][0]))
                second_sibling.set_one(Node(list_frequencies[i+1][1],list_frequencies[i+1][0]))
                self.head_node = Node(first_sibling.get_freq() + second_sibling.get_freq())
                if second_sibling.get_freq() <= first_sibling.get_freq():
                    self.head_node.set_zero(second_sibling)
                    self.head_node.set_one(first_sibling)
                else:
                    self.head_node.set_zero(first_sibling)
                    self.head_node.set_one(second_sibling)
                break
            else:
                first_sibling = self.head_node
                second_sibling = Node(list_frequencies[i][1],list_frequencies[i][0])
                head_freq = first_sibling.get_freq() + second_sibling.get_freq()
                self.head_node = Node(head_freq)
                if second_sibling.get_freq() <= first_sibling.get_freq():
                    self.head_node.set_zero(second_sibling)
                    self.head_node.set_one(first_sibling)
                else:
                    self.head_node.set_zero(first_sibling)
                    self.head_node.set_one(second_sibling)
                i += 1


        
    def __str__(self):
        return str(self.head_node.print_node())

        