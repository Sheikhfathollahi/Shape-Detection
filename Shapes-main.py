import tkinter as tk
import imutils
import cv2
import numpy as np
from PIL import ImageGrab
import os
from keras.models import load_model
model=load_model('Shapes/Shapes_Model.h5')

def fix_dimension(img):
    new_img = np.zeros((56, 56, 3))
    for i in range(1):
        new_img[:, :, i] = img
        return new_img


def true_resize (img):
    img = imutils.resize(img, height=56)
    if img.shape[1]<56:
        new_w= round((56 - img.shape[1]) /2)
        center_image = np.zeros((56,56) , np.uint8)
        center_image[:,new_w:new_w+img.shape[1]] = img
    else:
        center_image = cv2.resize(img, (56, 56), interpolation=cv2.INTER_CUBIC)

    return  center_image



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

        self.output_frame = tk.Frame(root, width =500 , height = 300 , bd = 5 , relief = tk.FLAT)
        self.output_frame.pack(side=tk.RIGHT)
        # Set up the clear button widget
        clear_button = tk.Button(root, text='Clear', command=self.clear_canvas , font=("Helvetica", 12, "bold"))
        clear_button.place(x=60 , y =425)

        # Set up the save button widget
        Predict_button = tk.Button(root, text='Predict', command=self.save_image  , font=("Helvetica", 12, "bold"))
        Predict_button.place(x=20 , y =350 , width=150, height=75)

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

        for widget in self.output_frame.winfo_children():
            widget.destroy()


        # Generate file path in the current working directory
        file_path = os.path.join(os.getcwd(), 'drawing.png')

        # Take a screenshot and save it to file_path
        ImageGrab.grab().crop((x, y, x1, y1)).save(file_path)
        print(f"image saved as {file_path}")

        image = ImageGrab.grab().crop((x, y, x1, y1))
        image = image.convert('L')
        image = np.array(image)
        img_blur = cv2.GaussianBlur(image, (3, 3), 1)
        thresh = cv2.threshold(img_blur, 1, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        contours, hier = cv2.findContours(thresh, cv2.RETR_EXTERNAL,
                                          cv2.CHAIN_APPROX_NONE)
        contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0])
        Output = []
        for ctr in contours:
            x, y, w, h = cv2.boundingRect(ctr)
            #cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            Pelak = thresh[y:y + h, x:x + w]

            CLASSES = ["مثلث", "مستطیل", "دایره", "پنج ضلعی"]



            dic = {}
            characters = '0123456789'
            for i, c in enumerate(characters):
                dic[i] = c

            savedir = "Shapes"
            img_ = true_resize(Pelak)
            # cv2.imwrite("Shapes/triangle.jpg" , img_)
            # cv2.imwrite(os.path.join(savedir, str(x) + 'img.jpg'), img_)
            img = fix_dimension(img_)
            # cv2.imshow("img",img)
            # cv2.waitKey(0)
            img = img.reshape(1, 56, 56, 3)
            y_ = model.predict(img)[0]
            classes_x = np.argmax(y_, axis=0)
            character = CLASSES[classes_x]
            Output.append(character)
        Output = ' '.join(Output)
        print(Output)

        output_label = tk.Label(self.output_frame , text = Output , font=("Helvetica" , 100))
        output_label.pack()
        self.root.update_idletasks()

# Create the main application window
root = tk.Tk()
root.geometry('700x500')
app = DrawingApplication(root)
root.mainloop()


