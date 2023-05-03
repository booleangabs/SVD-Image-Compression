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
    CENTER, 
    HORIZONTAL
)
import tkinter as tk
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
from metrics import get_metrics
import sys


class App(Tk):
    def __init__(self, full_report):
        self.full = full_report
        
        self.root = Tk()
        self.root.title("SVD Image Compression")
        width = self.root.winfo_screenwidth()               
        height = self.root.winfo_screenheight()               
        self.root.geometry(f"{width}x{height}")
        
        ws = Label(self.root)
        ws.pack(pady=5)
        
        self.info = Label(self.root, text="----", font=("Arial", 14))
        self.info.pack()

        self.image_field = Label(self.root, pady=25)
        self.image_field.pack(pady=50, )
        self.image_field.bind("<Enter>", func=self.__show_original)
        self.image_field.bind("<Leave>", func=self.__show_compressed)
        
        text_psnr = "PSNR (dB): ranges from 0 to infinity, higher is better!"
        self.psnr_report = Label(self.root, text=text_psnr, font=("Arial", 14))
        self.psnr_report.pack()

        text_ssim = "SSIM: ranges from -1 to 1, higher is better!"
        self.ssim_report = Label(self.root, text=text_ssim, font=("Arial", 14))
        self.ssim_report.pack()
        
        self.ratio_report = Label(self.root, text="Compression ratio: X", font=("Arial", 14))
        self.ratio_report.pack()

        ws = Label(self.root)
        ws.pack(pady=15)

        self.button_select = Button(self.root, text = "Select Image", 
                                    command = self.get_image, font = ("Arial", 14))
        self.button_select.pack()

        self.slider_label = Label(self.root, text = "Target rank (k)", 
                          font = ("Arial", 14))
        self.slider_label.pack()

        self.slider = Scale(self.root, from_= 0, to = 255, orient = HORIZONTAL, 
                       tickinterval=50, length=500, command=self.update_image)
        self.slider.set(0)
        self.slider.pack()
        
        self.image = None
        self.uncompressed_image = None
        self.compressed_image = None
        
    def __show_original(self, *args, **kwargs):
        if not(self.image is None):
            self.__update_image_field()
        
    def __show_compressed(self, *args, **kwargs):
        if not(self.compressed_image is None) and (self.slider.get() > 0):
            image = Image.fromarray(self.compressed_image)
            self.__update_image_field(image)
            
    def __update_image_field(self, image=None):
        if image == None:
            image = self.image.copy()
        h = 350
        wp = h / image.size[1]
        nw = int(image.size[0] * wp)
        image = image.resize((nw, h))
        pimage = ImageTk.PhotoImage(image)
        self.image_field.configure(image = pimage)
        self.image_field.image = pimage
        
    def get_image(self):
        global path 
        working_dir = os.getcwd()
        path = askopenfilename(initialdir = working_dir, title = "Select Image", 
                               filetypes = (("PNG files", "*.png*"), ("all files", "*.*")))
        self.image = Image.open(path).convert("RGB")
        self.uncompressed_image = np.asarray(self.image)
        k = min(self.uncompressed_image.shape[:2])
        self.slider.config(to=k, length=min(500, k))
        self.slider.set(0)
        self.__update_image_field()
        
    def update_image(self, slider_value):
        if self.image == None:
            return
        
        self.info.config(text="Hover to see original image")
        
        value = int(slider_value)
        
        image = self.uncompressed_image
        if value > 0:
            # Do stuff here
            image = image * (value / self.slider.cget("to"))
            image = image.astype("uint8")
            # Stop doing stuff
            
            self.compressed_image = image.copy()
            
            # Update label image
            image = Image.fromarray(image)
            self.__update_image_field(image)
            
        else:
            self.__show_original()
            self.compressed_image = image.copy()
        self.show_metrics() # IMPORTANT: comment this if it gets too slow
        
    def show_metrics(self):
        if self.uncompressed_image is None or self.compressed_image is None:
            return
        metrics = get_metrics(self.uncompressed_image, self.compressed_image, self.full)
        self.psnr_report.config(text="PSNR (dB):" + f"{metrics['psnr']}".rjust(22))
        self.ssim_report.config(text="SSIM:" + f"{metrics['ssim']}".rjust(30))
        k = self.slider.get()
        
        if k > 0:
            m, n = self.uncompressed_image.shape[:2]
            cr = (m * n) / (k * (m + n + 1))
            
            cr = np.round(cr, 5)
        else:
            cr = np.inf
        self.ratio_report.config(text=f"Compression ratio:" + f"{cr}".rjust(10))

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    full_report = True
    if len(sys.argv) > 1:
        full_report = bool(int(sys.argv[1]))
    app = App(full_report)
    app.run()

    

