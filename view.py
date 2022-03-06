#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
View module to display the data
"""

__author__ = 'Mohamed Ouertani'

# Standard library imports
from distutils.log import warn
from tkinter import DISABLED, END, RIGHT, Y, ttk, filedialog, messagebox
from pathlib import Path
import tkinter as tk
from tkinter import font
from tkinter.font import NORMAL
from turtle import update
# Third party imports
import ttkthemes as themes


class View(themes.ThemedTk):
    
    def __init__(self,controller) -> None:
        self.controller = controller
        super().__init__()
        self.title("Huffman/BWT")
        self.geometry("700x650")
        # self.set_theme("black")
        self.buttons = ["Open","Save","Compress","Decompress","Sequence to BWT","BWT to sequence"]
        self.labels = []
        self.text_display = None

    def create_interface(self):
        main_frame = ttk.Frame(self)
        main_frame.pack()
        
        sequence_label = ttk.Label(main_frame,
                                   text="Current sequence : No sequence is loaded yet")
        sequence_label.grid(column=0,row=0, padx=5,pady=5,columnspan=2,sticky="w")
        self.labels.append(sequence_label)
        status_label = ttk.Label(main_frame,
                                 text="Sequence status : Not available")
        status_label.grid(column=0,row=1, padx=5,pady=5,columnspan=2,sticky="w")
        self.labels.append(status_label)

        column,row = 0,2
        for button_text in self.buttons:
            button = ttk.Button(main_frame,text=button_text,
                                command=lambda button = button_text :self.controller.function_handler(button))
            button.grid(column=column,row=row, padx=10,pady=10,sticky="news")
            if column > 0 and column %2 == 1:
                column = 0
                row += 1 
            else:
                column += 1
        #Create frame inside search result window
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(column=0,row=5,columnspan=2,
                        padx=5,pady=5,sticky="news")#
        #Add scrolbar
        y_scroll_bar = ttk.Scrollbar(text_frame)
        y_scroll_bar.pack(side=RIGHT,fill=Y)
        self.text_display = tk.Text(text_frame,height=22,yscrollcommand=y_scroll_bar.set,
                                    width=80)
        self.text_display.pack()
        y_scroll_bar.config(command=self.text_display.yview)
        next_button = ttk.Button(main_frame,text="Next",
                                 command=lambda button = "Next" :self.controller.function_handler(button))
        next_button.grid(column=0,row=9,padx=10,pady=10,sticky="news")
        final_button = ttk.Button(main_frame,text="End",
                                  command=lambda button = "End" :self.controller.function_handler(button))
        final_button.grid(column=1,row=9,padx=10,pady=10,sticky="news")
        
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
        self.filename = filedialog.askopenfilename(initialdir="~/Desktop/projetProgrammation2021",
                                                   title="Select a file")
        print(self.filename)
        if (len(self.filename)) == 0 :
            name_file = ""
            messagebox.showwarning("File selection","No selected file")
        else :
            name_file = Path(self.filename).stem #extracts file name without extension from selected local file
            messagebox.showwarning("File selection",f"Selected file : {name_file}")
        return self.filename , name_file

    def change_status(self,sequence):#,status
        self.labels[0].pack_forget()
        self.labels[0].config(text=f"Current sequence : {sequence}")
        # self.labels[1].pack_forget()
        # self.labels[1].config(text=f"Sequence status : {status}")

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
