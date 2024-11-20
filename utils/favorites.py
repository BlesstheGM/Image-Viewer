import tkinter as tk
from tkinter import filedialog

class FavoritesManager:
    def __init__(self, favorites_file="favorites.txt"):
        self.favorites = []
        self.favorites_file = favorites_file
        self.load_favorites()

    def add_to_favorites(self, file_path=None):
        """
        Add a new image to the favorites. If no file path is provided, prompt the user to select one.
        """
        if not file_path:
            # Use a file dialog to select the image
            root = tk.Tk()
            root.withdraw()  # Hide the main Tkinter window
            file_path = filedialog.askopenfilename(
                title="Select Image to Add to Favorites",
                filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif")]
            )
        
        if file_path:
            self.favorites.append(file_path)
            print("Added to favorites:", file_path)
            self.save_favorites()  # Save the updated list of favorites to the file

    def remove_from_favorites(self, file_path):
        """
        Remove an image from the favorites.
        """
        if file_path in self.favorites:
            self.favorites.remove(file_path)
            print("Removed from favorites:", file_path)
            self.save_favorites()  # Save the updated list after removal

    def get_favorites(self):
        """
        Get the list of favorite images.
        """
        return self.favorites

    def save_favorites(self):
        """
        Save the list of favorites to a file.
        """
        with open(self.favorites_file, "w") as file:
            for favorite in self.favorites:
                file.write(favorite + "\n")
        print("Favorites saved to", self.favorites_file)

    def load_favorites(self):
        """
        Load the list of favorites from a file.
        """
        try:
            with open(self.favorites_file, "r") as file:
                self.favorites = [line.strip() for line in file.readlines()]
            print("Favorites loaded from", self.favorites_file)
        except FileNotFoundError:
            print("Favorites file not found. Starting with an empty list.")
