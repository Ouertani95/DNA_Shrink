#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
View module part of the MVC architechture that represents
the UI logic of the application
"""

__author__ = 'Mohamed Ouertani'

# Standard library imports
import os
import tkinter as tk
from tkinter import DISABLED, END, RIGHT, Y, ttk, filedialog, messagebox
from tkinter.font import NORMAL
from pathlib import Path
# Third party imports
from ttkthemes import ThemedTk


class View(ThemedTk):

    """View class representing the GUI interface.
    The View class inherits all the methods and attributes of the ttkthemes Class.

    Attributes
    ----------
    controller : Controller
        Controller logic that interacts with the view
    text_display : Text widget
        Text widget to display all the results
    file_list : Combobox widget
        Combobox widget to enable file loading from GUI
    """

    def __init__(self,controller) -> None:
        """
        Class constructor method for initializing all the attributes

        Returns:
        ----------
        None
        """
        #Initialize the tk.Tk superclass
        super().__init__()
        #Initialize the attributes
        self.controller = controller
        self.title("DNAshrink Tool")
        self.geometry("700x640")
        self.set_theme("scidmint")
        self.text_display = None
        self.file_list = None
        self.style = None
        

    def create_interface(self) -> None:
        """
        Class method for Creation of interface and all the widgets inside

        Returns:
        ----------
        None
        """
        #Create main frame
        main_frame = ttk.Labelframe(self,text="DNAshrink Tool")
        main_frame.pack(anchor="center")
        #Create new style for buttons
        self.style=ttk.Style(main_frame)
        self.style.configure('TButton',font=("Palatino Linotype", 11, "bold"))

        #Create label for file loading combobox
        load_label = ttk.Label(main_frame,text="Load previous sequence : ",
                               font=("Palatino Linotype", 12, "bold"))
        load_label.grid(column=0,row=0,sticky="w",padx=10)
        #Create combobox widget
        selected_file = tk.StringVar()
        self.file_list = ttk.Combobox(main_frame,state="readonly",
                                      textvariable=selected_file,width=50)
        self.file_list.grid(column=1,row=0,pady=2,padx=5,sticky="news")
        #Bind file selection event from combobox to file_loader method
        self.file_list.bind("<<ComboboxSelected>>", self.file_loader)
        #Load all the files in data directory to combobox
        self.update_file_list(os.listdir("./data"))

        #Create a list of all the frame names
        Frame_list = ["File control",
                      "Huffman compression/decompression",
                      "Burrows-Wheeler Transformation",
                      "Steps"]
        #Create the Lableframe and buttons for file controlling
        file_buttons = ["Open","Save"]
        self.function_framer(main_frame,Frame_list[0],file_buttons,0,1)
        #Create the Labelframe and buttons for Huffman compression/decompression 
        huffman_buttons = ["Compress","Decompress"]
        self.function_framer(main_frame,Frame_list[1],huffman_buttons,0,2)
        #Create the Labelframe and buttons for BWT transformation
        bwt_buttons = ["Sequence to BWT","BWT to sequence"]
        self.function_framer(main_frame,Frame_list[2],bwt_buttons,0,3)
        #Create the Labelframe and buttons for the steps
        step_buttons = ["Next","End"]
        self.function_framer(main_frame,Frame_list[3],step_buttons,0,5)

        #Create frame for text widget
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(column=0,row=4,columnspan=2,padx=5,pady=5,sticky="ew")
        #Add scrollbar
        y_scroll_bar = ttk.Scrollbar(text_frame)
        y_scroll_bar.pack(side=RIGHT,fill=Y)
        #Create text widget
        self.text_display = tk.Text(text_frame,height=18,yscrollcommand=y_scroll_bar.set,
                                    width=92,state=DISABLED,font=("Palatino Linotype", 11, "bold"))
        self.text_display.pack()
        #Configure scrollbar
        y_scroll_bar.config(command=self.text_display.yview)
        #Set initial text
        self.update_text("No sequence is loaded, please choose a file to start.")


    def center_window(self) -> None:
        """
        Class method used to center the GUI window inside the screen

        Returns:
        ----------
        None
        """
        #update window height and width according to the widgets
        self.update()

        #Get the width and height of the window
        width = self.winfo_width()
        height = self.winfo_height()

        #Get the coordinates representing the middle of the screen
        x_offset = ((self.winfo_screenwidth() - width) // 2 )
        y_offset = ((self.winfo_screenheight() - height) // 2 )
        # // is to return int of devision not float

        #Set the new geometry/positioning of the window
        self.geometry(f"{width}x{height}+{x_offset}+{y_offset}")

    @staticmethod
    def open_file() -> tuple:
        """
        Static class method for opening new window to choose file from local directories

        Returns:
        ----------
        file_path : str
            path of the chosen file
        name_file : str
            name of the chosen file extracted from the file path with no extension
        """
        #Open filedialog window for file selection
        file_path = filedialog.askopenfilename(initialdir="./data",
                                                   title="Select a file",
                                                   filetypes=(("text files","*.txt"),
                                                              ("fasta file",".fasta"),
                                                              ("all files","*.*")))
        #Check if a file is selected or not and show message
        if (len(file_path)) == 0 :
            name_file = ""
            messagebox.showwarning("File selection","No selected file")
        else :
            #Extract file name without extension from the file path
            name_file = Path(file_path).stem
            messagebox.showwarning("File selection",f"Selected file : {name_file}")
        return file_path , name_file

    @staticmethod
    def show_warning(message="No sequence is loaded :\nPlease select a file first") -> None:
        """
        Static class method to show input message given by the Controller

        Parameters
        -----------
        message : str
            Input message given by the Controller

        Returns:
        ----------
        None
        """
        #Show messagebox with the specified message
        messagebox.showwarning("File selection",message)


    def update_text(self,text:str) -> None:
        """
        Class method to update the text widget content with request results

        Parameters
        -----------
        text : str
            Results from the model class passed by the Controller to be displayed

        Returns
        -----------
        None
        """
        #Remove readonly status of the text widget
        self.text_display.configure(state=NORMAL)
        #Clear the text widget content
        self.text_display.delete(1.0, "end")
        #Insert the input text
        self.text_display.insert(END,text)
        #Reestablish readonly status of the text widget
        self.text_display.configure(state=DISABLED)

    def file_loader(self,event) -> None:
        """
        Class method to initiaite file loading from combobox.
        This method actually calls the controller method function_handler.

        Parameters
        -----------
        event :
            Represents the selection of a file from Combobox widget inside the interface

        Returns
        -----------
        None
        """
        #Call controller's method function_handler
        self.controller.function_handler("Load")

    def get_selected_file(self) -> str:
        """
        Class method to recover selected file's path and name
        This method is mainly used by the controller

        Returns
        -----------
        file_path : str
            path of the chosen file
        file_name: str
            name of the chosen file extracted from the file path with no extension
        """
        #Get chosen file path from combobox widget
        file_path = self.file_list.get()
        #Extract file name from path
        file_name = Path(file_path).stem
        return file_path,file_name
    
    def update_file_list(self,file_list) -> None:
        """
        Class method to update the files in the combobox widget

        Returns
        -----------
        None
        """
        #Update the values attribute of the combobox widget
        self.file_list["values"] = file_list
    
    def function_framer(self,main_frame,frame_name,buttons_list,column,row)-> None:
        """
        Class method to create Labelframes and buttons for organised layout

        Parameters
        -----------
        main_frame : Frame
            The initial frame where the Labelframe will be created
        frame_name : str
            Name of the Labelframe to be created
        buttons_list : List
            Contains the names of the Buttons to be created
        column : int
            Number of the initial column for creating the Frame and Buttons
        row : 
            Number of the initial row for creating the Frame and Buttons

        Returns
        -----------
        None
        """
        #Create Labelframe widget to delimit each part of the tool
        label_frame = ttk.Labelframe(main_frame,text=frame_name,labelanchor="ns")
        label_frame.grid(column=column,row=row,columnspan=2,sticky="news",padx=5,pady=2)
        #Create the buttons in the specified layout
        for i in buttons_list:
            button = ttk.Button(label_frame,text=i,width=20,style='TButton',
                                command=lambda button = i :
                                self.controller.function_handler(button))
            button.pack(side='left',expand=True,fill="both",padx=10,pady=5)


    def main(self) -> None:
        """
        Main class method to launch the GUI by calling window specific methods

        Returns
        -----------
        None
        """
        self.create_interface()
        self.center_window()
        self.mainloop()
