import tkinter as tk
from PIL import ImageGrab
import os
import numpy as np

class DrawingApplication:
    def __init__(self, root):
        self.root = root
        self.root.title('Tkinter Drawing App')
        # Set up the canvas widget for drawing
        self.canvas = tk.Canvas(root, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Bind mouse events to methods
        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)



        # Set up the save button widget
        Save_button = tk.Button(root, text='Save', command=self.save_image  , font=("Helvetica", 12, "bold"))
        #Save_button.place(x=20 , y =350 , width=150, height=75)
        Save_button.pack()

        # Set up the clear button widget
        clear_button = tk.Button(root, text='Clear', command=self.clear_canvas, font=("Helvetica", 12, "bold"))
        # clear_button.place(x=60 , y =425)
        clear_button.pack()

        # Initialize the line start coordinates
        self.x1 = None
        self.y1 = None

    def paint(self, event):
        # Draw a line from the last point to the current point
        if self.x1 and self.y1:
            self.canvas.create_line(self.x1, self.y1, event.x, event.y, smooth=tk.TRUE,
                                    capstyle=tk.ROUND, width=2)
        # Update the last point coordinates
        self.x1 = event.x
        self.y1 = event.y

    def reset(self, event):
        # Reset the last point coordinates to None
        self.x1 = None
        self.y1 = None

    def clear_canvas(self):
        # Clear the canvas
        self.canvas.delete('all')

    def save_image(self):
        # Get the canvas coordinates relative to the root window
        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()



        # Generate file path in the current working directory
        file_path = os.path.join(os.getcwd(), 'drawing.png')

        # Take a screenshot and save it to file_path
        ImageGrab.grab().crop((x, y, x1, y1)).save(file_path)
        print(f"image saved as {file_path}")
        img =ImageGrab.grab().crop((x, y, x1, y1))
        img = np.array(img)
        print(img.shape)

        self.root.update_idletasks()

# Create the main application window
root = tk.Tk()
root.geometry('700x500')
app = DrawingApplication(root)
root.mainloop()


