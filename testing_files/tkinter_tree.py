from tkinter import * # Import tkinter
import math

class Main:
    def __init__(self):
        window = Tk() # Create a window
        window.title("Recursive Tree") # Set a title

        self.width = 400
        self.height = 400
        self.canvas = Canvas(window, 
        width = self.width, height = self.height,bg="white")
        self.canvas.pack()

        # Add a label, an entry, and a button to frame1
        frame1 = Frame(window) # Create and add a frame to window
        frame1.pack()

        Label(frame1, 
            text = "Enter the depth: ").pack(side = LEFT)
        self.depth = StringVar()
        Entry(frame1, textvariable = self.depth, 
            justify = RIGHT).pack(side = LEFT)
        Button(frame1, text = "Display Recursive Tree", 
            command = self.display).pack(side = LEFT)

        self.angleFactor = math.pi/5
        self.sizeFactor = 0.58

        window.mainloop() # Create an event loop

    def drawLine(self, x1,y1, x2,y2):
        self.canvas.create_line(x1,y1, x2,y2, tags = "line")    

    def display(self):
        self.canvas.delete("line")
        depth = int(self.depth.get())
        return self.paintBranch(depth, self.width/2, self.height, self.height/3, math.pi/2)

    def paintBranch(self, depth, x1, y1, length, angle):
        if depth >= 0:
            depth -= 1
            x2 = x1 + int(math.cos(angle) * length)
            y2 = y1 - int(math.sin(angle) * length)

            # Draw the line
            self.drawLine(x1,y1, x2,y2)

            # Draw the left branch
            self.paintBranch(depth, x2, y2, length * self.sizeFactor, angle + self.angleFactor  )
            # Draw the right branch
            self.paintBranch(depth, x2, y2, length * self.sizeFactor, angle - self.angleFactor )        


drawer = Main()