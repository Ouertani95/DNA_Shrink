#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
View module to display the data
"""

__author__ = 'Mohamed Ouertani'

# Standard library imports
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
# Third party imports
import ttkthemes as themes

class View(themes.ThemedTk):
    
    def __init__(self,controller) -> None:
        self.controller = controller
        super().__init__()
        self.title("Huffman/BWT")
        # self.set_theme("black")
        self.buttons = ["Open","Save","Compress","Decompress","Sequence to BWT","BWT to sequence"]
        self.labels = []

    def create_interface(self):
        main_frame = ttk.Frame(self)
        main_frame.pack()
        
        sequence_label = ttk.Label(main_frame,
                                        text="Current sequence : No sequence is loaded yet")
        sequence_label.grid(column=0,row=0, padx=10,pady=10,columnspan=2)
        self.labels.append(sequence_label)

        column,row = 0,1
        for button_text in self.buttons:
            button = ttk.Button(main_frame,text=button_text,
                                command=lambda button = button_text :self.controller.function_handler(button))
            button.grid(column=column,row=row, padx=10,pady=10)
            if column > 0 and column %2 == 1:
                column = 0
                row += 1 
            else:
                column += 1
        
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
                                                   title="Selectionner un fichier")
        print(self.filename)
        if (len(self.filename)) == 0 :
            messagebox.showwarning("Sélection fichier","Aucun fichier sélectionné")
        else : 
            global nameFile
            nameFile = Path(self.filename).stem #extracts file name without extension from selected local file
            messagebox.showwarning("Sélection fichier",f"Fichier sélectionné : {nameFile}")
        return self.filename

    def change_status(self,sequence):
        self.labels[0].pack_forget()
        self.labels[0].config(text=f"Current sequence : {sequence}")

    def main(self):
        """Launch the GUI"""
        self.create_interface()
        self.center_window()
        self.mainloop()

if __name__ == "__main__":
    window = View()
    window.main()