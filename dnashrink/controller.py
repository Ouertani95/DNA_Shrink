#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Controller module part of the MVC architechture  that acts as a middle-man 
between Model and View components to process all  the business logic and incoming requests,
manipulate data  using the Model component  and interact with the Views to render the final output
"""

__author__ = 'Mohamed Ouertani'

from binaryornot.check import is_binary
from dnashrink.model import Model
from dnashrink.view import View

class Controller():

    """
    Controller class to coordinate between model and view

    Attributes
    ----------
    model : Model
        Model object that manipulates all sequences and data in the program
    view : View
        View object that interacts with the user and displays request results
    """

    def __init__(self) -> None:
        """
        Class constructor method for initializing all the attributes

        Returns:
        ----------
        None
        """
        self.model = Model(self)
        self.view = View(self)

    def function_handler(self,function) -> None:
        """
        Class method for handling all the view button functions

        Parameters
        -----------
        function : str
            Corresponds to the text attribute of the clicked button from view

        Returns:
        ----------
        None
        """
        #Verify if no file is already loaded
        if function != "Open" and not self.model.huffman_handler:
            self.view.show_warning()
        else:
            #Assign function according to text attribute passed from view
            if function == "Open":
                self.open()
            elif function == "Save":
                self.save()
            elif function == "Compress":
                self.compression()
            elif function == "Decompress":
                self.decompression()
            elif function == "Sequence to BWT":
                self.transform_bwt()
            elif function == "BWT to sequence":
                self.transform_sequence()
            elif function == "Next":
                self.step_by_step()
            elif function == "End":
                self.jump_to_end()
        

    def compression(self) -> None:
        """
        Class method that calls model for compression method then displays
        compression results
        
        Returns:
        ----------
        None
        """
        #Verify if sequence is uncompressed
        if self.model.is_uncompressed():
            #Call model compression method
            compressed_seq,binary_sequence = self.model.compress_sequence()
            #Call view update_text method to display results
            self.view.update_text(f"Binary sequence : {binary_sequence}\n\n"
                                 +f"Compressed sequence : {compressed_seq}")
        else:
            #Show warning message if sequence is already compressed
            self.view.show_warning("Sequence is already compressed")


    def decompression(self) -> None:
        """
        Class method that calls model for decompression method then displays
        decompression results

        Returns:
        ----------
        None
        """
        #Verify if sequence is compressed
        if not self.model.is_uncompressed():
            #Call model decompression method
            decompressed_seq,binary_sequence = self.model.decompress_sequence()
            #Call view update_text method to display results
            self.view.update_text(f"Binary sequence : {binary_sequence}\n\n"
                                 +f"Decompressed sequence : {decompressed_seq}")
        else:
            #Show warning message if sequence is already decompressed
            self.view.show_warning("Sequence is already decompressed")

    def transform_bwt(self) -> None:
        """
        Class method that calls model for bwt transformation method then displays
        transformation results

        Returns:
        ----------
        None
        """
        #Verify if sequence is uncompressed
        if self.model.is_uncompressed():
            #Verify if sequence is not bwt
            if not self.model.bwt_handler.input_is_bwt(): #TODO: add the method to model instead
                #Call model sequence_to_bwt method 
                bwt_generator = self.model.sequence_to_bwt()
                #Update model's current_function attribute with bwt transformation method
                self.model.update_current_function(bwt_generator)
                #Call view update_text method to display results
                self.view.update_text("""Transform to bwt, Press Next or End to continue""")
            else:
                #Show warning message if sequence is already BWT
                self.view.show_warning("Sequence is already BWT")
        else:
            #Show warning message if sequence is compressed
            self.view.show_warning("Sequence is compressed\nTry decompressing first")


    def transform_sequence(self) -> None:
        """
        Class method that calls model for reverse bwt transformation method then displays
        tranformation results

        Returns:
        ----------
        None
        """
        #Verify if sequence is uncompressed
        if self.model.is_uncompressed():
            #Verify if sequence is bwt
            if self.model.bwt_handler.input_is_bwt(): #TODO: add the method to model instead
                #Call model bwt_to_sequence method
                bwt_decoder = self.model.bwt_to_sequence()
                #Update model's current_function attribute with reverse bwt transformation method
                self.model.update_current_function(bwt_decoder)
                #Call view update_text method to display results
                self.view.update_text("""Transform to sequence , press Next or End to continue""")
            else:
                #Show warning message if sequence is already normal
                self.view.show_warning("Sequence is already normal")
        else:
            #Show warning message if sequence is compressed
            self.view.show_warning("Sequence is compressed\nTry decompressing first")

    def step_by_step(self) -> None:
        """
        Class method linked to Next button in view
        This method shows the results of the model's current_function attribute
        one by one

        Returns:
        ----------
        None
        """
        #Verify if a function is already selected
        if self.model.current_function:
            try:
                #Get yield result from the current_function attribute
                next_value = next(self.model.current_function)
                #Call view update_text method to display results
                self.view.update_text(f" Next step :\n{next_value} ")
            #Intercept no more results
            except StopIteration:
                #Update model's current_sequence
                current_sequence = self.model.get_current_sequence()
                #Call view update_text method to display results
                self.view.update_text(f"Current sequence : {current_sequence}")
        else:
            #Display warning if no function is selected
            self.view.show_warning("No function is chosen yet")

    def jump_to_end(self) -> None:
        """
        Class method linked to end button from view that displays 
        the last result directly from the model'l current_function 
        attribute
        
        Returns:
        ----------
        None
        """
        #Verify if a function is already selected
        if self.model.current_function:
            try:
                #Recover last yield value directly from current_function generator
                last_value = list(self.model.current_function)[-1]
                #Call view update_text method to display results
                self.view.update_text(f" Last step :\n{last_value} ")
            #Intercept no more results
            except IndexError:
                #Update model's current_sequence
                current_sequence = self.model.get_current_sequence()
                #Call view update_text method to display results
                self.view.update_text(f"Current sequence : {current_sequence}")
        else:
            #Display warning if no function is selected
            self.view.show_warning("No function is chosen yet")

    def save(self) -> None:
        """
        Class method linked to save button in view which is used 
        to Save the current sequence

        Returns:
        ----------
        None
        """
        #Verify if a sequence is loaded to the program
        if self.model.current_sequence:
            #Save file using model's save_file method and recover file name
            saved_files = self.model.save_file()
            #Display name of the saved file using the view's show_warning method
            self.view.show_warning(f"The Following files were saved :\n{saved_files}")
        else:
            #Show warning if no sequence is loaded
            self.view.show_warning()

    def open(self) -> None:
        """
        Class method to open a new sequence file using the view's open_file method 
        then load the sequence to the program using the model's file_loader method

        Returns:
        ----------
        None
        """
        #Recover file_path and file_name after opening new file
        file_path,file_name = self.view.open_file()
        #Verify if a file is actually chosen 
        if file_path:
            #Load file sequence to program using model's file_loader method
            loaded_sequence = self.model.file_loader(file_path,file_name)
            #Display new loaded sequence using view's update_text method
            self.view.update_text(f"Current sequence : {loaded_sequence}")

    def launch_view(self) -> None:
        """
        Class method to launch the GUI interface using the view's main method
        
        Returns:
        ----------
        None
        """
        self.view.main()
