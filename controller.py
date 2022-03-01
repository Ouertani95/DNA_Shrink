#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Controller module to coordinate between view and model
"""

from model import Model
from view import View
__author__ = 'Mohamed Ouertani'

class Controller():

    def __init__(self) -> None:
        self.model = Model(self)
        self.view = View(self)
        # self.button_functions = self.set_button_functions()
            


    def function_handler(self,function):
        #["Open","Save","Compress","Decompress","Sequence to BWT","BWT to sequence"]
        if function == "Open":
            self.open()
        if function == "Save":
            self.save()
        if function == "Compress":
            self.compression()
        if function == "Decompress":
            self.decompression()
        if function == "Sequence to BWT":
            self.transform_bwt()
        if function == "BWT to sequence":
            self.transform_sequence()

    def compression(self):
        compressed_seq = self.model.compress_sequence()
        self.view.change_status(compressed_seq)

    def decompression(self):
        decompressed_seq = self.model.decompress_sequence()
        self.view.change_status(decompressed_seq)

    def transform_bwt(self):
        bwt_sequence = self.model.sequence_to_bwt()
        self.view.change_status(bwt_sequence)

    def transform_sequence(self):
        original_sequence = self.model.bwt_to_sequence()
        self.view.change_status(original_sequence)


    def save(self):
        pass

    def open(self):
        file_path = self.view.open_file()
        print(type(file_path))
        print(f"the path is : {file_path}")
        if file_path:
            loaded_sequence = self.model.file_loader(file_path)
            self.view.change_status(loaded_sequence)
        
        

    def launch_view(self):
        self.view.main()

if __name__ == "__main__":
    test = Controller()
    test.launch_view()

# def set_button_functions(self):
    #     function_dict = {}
    #     functions = [lambda : self.open(),
    #                  lambda : self.save(),
    #                  lambda : self.compression(),
    #                  lambda : self.decompression(),
    #                  lambda : self.transform_bwt(),
    #                  lambda : self.transform_sequence()]
    #     for button_id,button in enumerate(self.view.buttons):
    #         function_dict[button] = functions[button_id]
    #     print(function_dict)
    #     return function_dict
