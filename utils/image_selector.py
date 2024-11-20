import tkinter as tk
from tkinter import filedialog

def select_images():
    root = tk.Tk()
    root.withdraw()
    files = filedialog.askopenfilenames(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    return list(files)
