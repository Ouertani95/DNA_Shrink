#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Controller module to coordinate between view and model
"""

__author__ = 'Mohamed Ouertani'

from model import Model
from view import View

class Controller():

    def __init__(self) -> None:
        self.model = Model(self)
        self.view = View(self)
        # self.button_functions = self.set_button_functions()
      
    def function_handler(self,function):
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
        if self.model.huffman_handler:
            if self.model.is_uncompressed():
                compressed_seq = self.model.compress_sequence()
                self.view.change_status(compressed_seq)#,"Compressed"
            else:
                self.view.show_warning("Sequence is already compressed")
        else:
            self.view.show_warning()

    def decompression(self):
        if self.model.huffman_handler:
            if not self.model.is_uncompressed():
                decompressed_seq = self.model.decompress_sequence()
                self.view.change_status(decompressed_seq)#,"Uncompressed"
            else:
                self.view.show_warning("Sequence is already decompressed")
        else:
            self.view.show_warning()

    def transform_bwt(self):
        if self.model.bwt_handler:
            if self.model.is_uncompressed():
                if not self.model.bwt_handler.is_bwt():
                    bwt_generator = self.model.sequence_to_bwt()
                    self.model.update_current_function(bwt_generator)
                    self.view.update_text("""Transform bwt function, Press Next or End to continue""")
                else:
                    self.view.show_warning("Sequence is already BWT")
            else:
                self.view.show_warning("Sequence is compressed\nTry decompressing first")
        else:
            self.view.show_warning()
        

    def transform_sequence(self):
        if self.model.bwt_handler:
            if self.model.is_uncompressed():
                if self.model.bwt_handler.is_bwt():
                    bwt_decoder = self.model.bwt_to_sequence()
                    self.model.update_current_function(bwt_decoder)
                    self.view.update_text("""Transform sequence function, Press Next or End to continue""")
                else:
                    self.view.show_warning("Sequence is already normal")
            else:
                self.view.show_warning("Sequence is compressed\nTry decompressing first")
        else:
            self.view.show_warning()

    def step_by_step(self):
        if self.model.current_function:
            try:
                next_value = next(self.model.current_function)
                self.view.update_text(f" Next step :\n{next_value} ")
            except StopIteration:
                self.view.update_text("The protocole is finished, please refer to the main menu.")
                current_sequence = self.model.get_current_sequence()
                self.view.change_status(current_sequence)
        else:
            self.view.show_warning("No function is chosen yet")

    def jump_to_end(self):
        if self.model.current_function:
            try:
                last_value = list(self.model.current_function)[-1]
                self.view.update_text(f" Last step :\n{last_value} ")
            except IndexError:
                self.view.update_text("The protocole is finished, please refer to the main menu.")
                current_sequence = self.model.get_current_sequence()
                self.view.change_status(current_sequence)
        else:
            self.view.show_warning("No function is chosen yet")

    def save(self):
        if self.model.current_sequence:
            self.model.save_file()
        else:
            self.view.show_warning()

    def open(self):
        file_path,file_name = self.view.open_file()
        if file_path:
            loaded_sequence = self.model.file_loader(file_path,file_name)
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
