import tkinter as tk
from tkinter import filedialog

def pick_directory():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    directory = filedialog.askdirectory()
    return directory
