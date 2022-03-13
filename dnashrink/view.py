#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
View module part of the MVC architechture that represents
the UI logic of the application
"""

__author__ = 'Mohamed Ouertani'

# Standard library imports
import tkinter as tk
from tkinter import DISABLED, END, RIGHT, Y, ttk, filedialog, messagebox
from tkinter.font import NORMAL
from pathlib import Path


class View(tk.Tk):

    """View class representing the GUI interface.
    The View class inherits all the methods and attributes of the tkinter Class.

    Attributes
    ----------
    controller : Controller
        Controller logic that interacts with the view
    buttons : List[str]
        All the button titles present in the interface
    labels : List[Label Widgets]
        All the labels present in the Interface
    text_display : Text widget
        Text widget to display all the results
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
        self.title("Huffman/BWT")
        self.geometry("700x620")
        self.buttons = ["Open","Save","Compress","Decompress",
                        "Sequence to BWT","BWT to sequence",
                        "Next","End"]
        self.labels = []
        self.text_display = None

    def create_interface(self) -> None:
        """
        Class method for Creation of interface and all the widgets inside

        Returns:
        ----------
        None
        """
        #Create main frame
        main_frame = ttk.Frame(self)
        main_frame.pack()

        # Set the initial theme
        self.tk.call("source", "./Sun-Valley-ttk-theme-master/sun-valley.tcl")
        self.tk.call("set_theme", "dark")

        #Create an instance of Style Object and Configure the styles of the Buttons
        style = ttk.Style()
        style.configure('style.TButton',
                        font=("Palatino Linotype", 12, "bold"), foreground="#3a86ff")

        #Create all the buttons
        column,row = 0,0
        for button_number,button_text in enumerate(self.buttons):
            button = ttk.Button(main_frame,text=button_text,style='style.TButton',
                                command=lambda button = button_text :
                                self.controller.function_handler(button))
            button.grid(column=column,row=row, padx=10,pady=10,sticky="news")
            if button_number == 5:
                row +=1
            if column > 0 and column %2 == 1:
                column = 0
                row += 1
            else:
                column += 1

        #Create new frame inside the main frame
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(column=0,row=3,columnspan=2,
                        padx=5,pady=5,sticky="news")

        #Add scrollbar
        y_scroll_bar = ttk.Scrollbar(text_frame)
        y_scroll_bar.pack(side=RIGHT,fill=Y)

        #Create text widget
        self.text_display = tk.Text(text_frame,height=20,yscrollcommand=y_scroll_bar.set,
                                    width=65,state=DISABLED,font=(10))
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
        file_path = filedialog.askopenfilename(initialdir="./",
                                                   title="Select a file",
                                                   filetypes=(("text files","*.txt"),
                                                              ("fasta file",".fasta"),
                                                              ("all files","*.*")))
        print(file_path)
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
