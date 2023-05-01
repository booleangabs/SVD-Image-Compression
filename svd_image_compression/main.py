"""MIT License

Copyright (c) 2023 Yano R. Vasconcelos, Eduardo G. de M. Albuquerque and José Gabriel P. Tavares

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import numpy as np
from tkinter import (
    Tk, 
    Label, 
    Frame, 
    Button, 
    Scale, 
    BOTTOM, 
    HORIZONTAL
)
import tkinter as tk
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
from metrics import get_metrics

class App(Tk):
    def __init__(self):
        self.root = Tk()
        self.root.title("SVD Image Compression")
        width = self.root.winfo_screenwidth()               
        height = self.root.winfo_screenheight()               
        self.root.geometry(f"{width}x{height}")

        self.image_field = Label(self.root, pady=25)
        self.image_field.pack(pady=50)
        
        text_psnr = "PSNR (dB): ranges from 0 to infinity, higher is better!"
        self.psnr_report = Label(self.root, text=text_psnr, font=("Arial", 14))
        self.psnr_report.pack()

        text_ssim = "SSIM: ranges from -1 to 1, higher is better!"
        self.ssim_report = Label(self.root, text=text_ssim, font=("Arial", 14))
        self.ssim_report.pack()
        
        self.ratio_report = Label(self.root, text="Compression ratio: X", font=("Arial", 14))
        self.ratio_report.pack()

        self.control_panel = Frame(self.root)
        self.control_panel.pack(side = BOTTOM, padx= 25, pady= 25)

        self.button_select = Button(self.control_panel, text = "Select Image", 
                                    command = self.show_image, font = ("Arial", 14))
        self.button_select.pack()

        # IMPORTANT: Use the following lines if automatically computing metrics gets slow
        # self.button_metrics = Button(self.control_panel, text = "Calculate metrics",
        #                              command = self.show_metrics, font = ("Arial", 14))
        # self.button_metrics.pack()

        self.slider_label = tk.Label(self.control_panel, text = "Target rank (k)", 
                          font = ("Arial", 14))
        self.slider_label.pack()

        self.slider = Scale(self.control_panel, from_= 0, to = 255, orient = HORIZONTAL, 
                       tickinterval=50, length=500, command=self.update_image)
        self.slider.set(10)
        self.slider.pack()
        
        self.image = None
        self.uncompressed_image = None
        self.compressed_image = None
        
    def show_image(self):
        global path 
        working_dir = os.getcwd()
        path = askopenfilename(initialdir = working_dir, title = "Select Image", 
                               filetypes = (("PNG files", "*.png*"), ("all files", "*.*")))
        self.image = Image.open(path)
        self.image = self.image.convert("L")
        self.uncompressed_image = np.asarray(self.image)
        self.image.thumbnail((400, 400))
        image = ImageTk.PhotoImage(self.image)
        self.image_field.configure(image = image)
        self.image_field.image = image
        
    def update_image(self, slider_value):
        if self.image == None:
            return

        # Do stuff here
        if len(self.uncompressed_image.shape) > 2:
            image = self.uncompressed_image.mean(2).astype("uint8")
        else:
            image = self.uncompressed_image.copy()
        image = image * (image >= int(slider_value))
        # Stop doing stuff
        
        self.compressed_image = image.copy()
        
        # Update label image
        image = Image.fromarray(image.astype("uint8"))
        image.thumbnail((400, 400))
        image = ImageTk.PhotoImage(image)
        self.image_field.configure(image = image)
        self.image_field.image = image
        self.show_metrics() # IMPORTANT: comment this if it gets too slow
        
    def show_metrics(self):
        if self.uncompressed_image is None or self.compressed_image is None:
            return
        metrics = get_metrics(self.uncompressed_image, self.compressed_image)
        self.psnr_report.config(text=f"PSNR (dB): {metrics['psnr']}")
        self.ssim_report.config(text=f"SSIM: {metrics['ssim']}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()

    

