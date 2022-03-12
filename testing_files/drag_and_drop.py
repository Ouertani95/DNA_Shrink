    #from tkdnd import DND_FILES
    
    #tkdnd.TkinterDnD.Tk
    
    # self.text_display.drop_target_register(DND_FILES)
    # self.text_display.dnd_bind('<<Drop>>', self.show_text)

    # self.text_display.configure(state=NORMAL)
    # self.text_display.insert("end","Drag and drop a .txt file")
    # self.text_display.configure(state=DISABLED)


    # def show_text(self,event):
    #     self.text_display.configure(state=NORMAL)
    #     self.text_display.delete("1.0","end")
    #     if event.data.endswith(".txt"):
    #         with open(event.data, "r") as file:
    #             for line in file:
    #                 line=line.strip()
    #                 self.text_display.insert("end",f"{line}\n")
    #     self.text_display.configure(state=DISABLED)