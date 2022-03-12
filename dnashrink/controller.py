#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Controller module to coordinate between view and model
"""

__author__ = 'Mohamed Ouertani'

from binaryornot.check import is_binary
from model import Model
from view import View

class Controller():

    def __init__(self) -> None:
        self.model = Model(self)
        self.view = View(self)
        # self.button_functions = self.set_button_functions()
      
    def function_handler(self,function):
        if function != "Open" and not self.model.huffman_handler:
            self.view.show_warning()
        else:
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
            if function == "Next":
                self.step_by_step()
            if function == "End":
                self.jump_to_end()

    def compression(self):
        if self.model.is_uncompressed():
            compressed_seq,binary_sequence = self.model.compress_sequence()
            self.view.update_text(f"Binary sequence : {binary_sequence}\n\n"
                                 +f"Compressed sequence : {compressed_seq}")
        else:
            self.view.show_warning("Sequence is already compressed")
        

    def decompression(self):
        if not self.model.is_uncompressed():
            decompressed_seq,binary_sequence = self.model.decompress_sequence()
            self.view.update_text(f"Binary sequence : {binary_sequence}\n\n"
                                 +f"Decompressed sequence : {decompressed_seq}")
        else:
            self.view.show_warning("Sequence is already decompressed")

    def transform_bwt(self):
        if self.model.is_uncompressed():
            if not self.model.bwt_handler.input_is_bwt():
                bwt_generator = self.model.sequence_to_bwt()
                self.model.update_current_function(bwt_generator)
                self.view.update_text("""Transform bwt function, Press Next or End to continue""")
            else:
                self.view.show_warning("Sequence is already BWT")
        else:
            self.view.show_warning("Sequence is compressed\nTry decompressing first")
        

    def transform_sequence(self):
        if self.model.is_uncompressed():
            if self.model.bwt_handler.input_is_bwt():
                bwt_decoder = self.model.bwt_to_sequence()
                self.model.update_current_function(bwt_decoder)
                self.view.update_text("""Transform sequence function, Press Next or End to continue""")
            else:
                self.view.show_warning("Sequence is already normal")
        else:
            self.view.show_warning("Sequence is compressed\nTry decompressing first")

    def step_by_step(self):
        if self.model.current_function:
            try:
                next_value = next(self.model.current_function)
                self.view.update_text(f" Next step :\n{next_value} ")
            except StopIteration:
                current_sequence = self.model.get_current_sequence()
                self.view.update_text(f"Current sequence : {current_sequence}")
        else:
            self.view.show_warning("No function is chosen yet")

    def jump_to_end(self):
        if self.model.current_function:
            try:
                last_value = list(self.model.current_function)[-1]
                self.view.update_text(f" Last step :\n{last_value} ")
            except IndexError:
                current_sequence = self.model.get_current_sequence()
                self.view.update_text(f"Current sequence : {current_sequence}")
        else:
            self.view.show_warning("No function is chosen yet")

    def save(self):
        if self.model.current_sequence:
            saved_files = self.model.save_file()
            self.view.show_warning(f"The Following files were save :\n{saved_files}")
        else:
            self.view.show_warning()

    def open(self):
        file_path,file_name = self.view.open_file()
        if file_path:
            # if self.is_plain_text(file_path):
            loaded_sequence = self.model.file_loader(file_path,file_name)
            self.view.update_text(f"Current sequence : {loaded_sequence}")
            # else:
            #     self.view.show_warning("wrong file format")
            #     #"Sequence longer than 50 :\nTry another file"

    def is_plain_text(self,file_path):
        with open (file_path,"r") as file_check:
            try:
                content = file_check.read()
            except UnicodeDecodeError:
                return False
        if len(content)> 100 or is_binary(file_path):
            return False
        return True


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
