#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
View module to display the data
"""

__author__ = 'Mohamed Ouertani'

# Standard library imports
import tkinter as tk
from tkinter import DISABLED, END, RIGHT, Y, ttk, filedialog, messagebox
from tkinter.font import NORMAL
from pathlib import Path




class View(tk.Tk):
    
    def __init__(self,controller) -> None:
        self.controller = controller
        super().__init__()
        self.title("Huffman/BWT")
        self.geometry("700x600")
        self.buttons = ["Open","Save","Compress","Decompress",
                        "Sequence to BWT","BWT to sequence",
                        "Next","End"]
        self.labels = []
        self.text_display = None

    def create_interface(self):
        #Create main frame
        main_frame = ttk.Frame(self)
        main_frame.pack()

        # Set the initial theme
        self.tk.call("source", "./Sun-Valley-ttk-theme-master/sun-valley.tcl")
        self.tk.call("set_theme", "dark")

        #Create an instance of Style Object
        style = ttk.Style()

        #Configure the properties of the Buttons
        style.configure('style.TButton', font=("Palatino Linotype", 12, "bold"), foreground="#3a86ff")
        
        #Create all the buttons
        column,row = 0,0
        for button_number,button_text in enumerate(self.buttons):
            button = ttk.Button(main_frame,text=button_text,style='style.TButton',
                                command=lambda button = button_text :self.controller.function_handler(button))
            button.grid(column=column,row=row, padx=10,pady=10,sticky="news")
            if button_number == 5:
                row +=1
            if column > 0 and column %2 == 1:
                column = 0
                row += 1 
            else:
                column += 1

        #Create frame inside search result window
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(column=0,row=3,columnspan=2,
                        padx=5,pady=5,sticky="news")

        #Add scrollbar
        y_scroll_bar = ttk.Scrollbar(text_frame)
        y_scroll_bar.pack(side=RIGHT,fill=Y)

        #Create text widget
        self.text_display = tk.Text(text_frame,height=22,yscrollcommand=y_scroll_bar.set,
                                    width=80,state=DISABLED)
        self.text_display.pack()

        #Configure scrollbar
        y_scroll_bar.config(command=self.text_display.yview)

        #Set initial text
        self.update_text("No sequence is loaded, please choose a file to start.")


    def center_window(self):
        """Center the GUI window inside the screen"""
        self.update() #update object states (used to return new value of h / w)
        width = self.winfo_width()
        height = self.winfo_height()
        x_offset = ((self.winfo_screenwidth() - width) // 2 )
        # // is to return int of devision not float
        y_offset = ((self.winfo_screenheight() - height) // 2 )
        self.geometry(f"{width}x{height}+{x_offset}+{y_offset}")

    def open_file(self):
        self.filename = filedialog.askopenfilename(initialdir="./",
                                                   title="Select a file",
                                                   filetypes=(("text files","*.txt"),
                                                              ("fasta file",".fasta"),
                                                              ("all files","*.*")))
        print(self.filename)
        if (len(self.filename)) == 0 :
            name_file = ""
            messagebox.showwarning("File selection","No selected file")
        else :
            name_file = Path(self.filename).stem #extracts file name without extension from selected local file
            messagebox.showwarning("File selection",f"Selected file : {name_file}")
        return self.filename , name_file


    def show_warning(self,message="No sequence is loaded :\nPlease select a file first"):
        messagebox.showwarning("File selection",message)


    def update_text(self,text):
        self.text_display.configure(state=NORMAL)
        self.text_display.delete(1.0, "end")   #Clear the text window so we can write.
        self.text_display.insert(END,text)
        self.text_display.configure(state=DISABLED)


    def main(self):
        """Launch the GUI"""
        self.create_interface()
        self.center_window()
        self.mainloop()
