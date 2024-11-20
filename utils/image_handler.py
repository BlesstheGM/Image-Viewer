import os
import pygame

SUPPORTED_FORMATS = (".png", ".jpg", ".jpeg", ".bmp", ".gif")

def load_images(directory):
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(SUPPORTED_FORMATS)]

def load_image(image_path):
    return pygame.image.load(image_path)

def scale_image(image, frame_size):
    frame_width, frame_height = frame_size
    image_width, image_height = image.get_size()
    scale_factor = min(frame_width / image_width, frame_height / image_height)
    new_size = (int(image_width * scale_factor), int(image_height * scale_factor))
    return pygame.transform.scale(image, new_size)

def save_image(image, filename):
    """Saves the current image to the specified file."""
    try:
        pygame.image.save(image, filename)
        print(f"Image saved as {filename}")
    except Exception as e:
        print(f"Error saving image: {e}")

def adjust_brightness(image, factor):
    """Adjusts the brightness of the image. A factor > 1 makes the image brighter, 
    while a factor < 1 makes it darker."""
    try:
        # Create a copy of the image surface
        image_copy = image.copy()
        width, height = image_copy.get_size()
        
        # Loop through each pixel and adjust its brightness
        for x in range(width):
            for y in range(height):
                color = image_copy.get_at((x, y))
                r, g, b, a = color
                
                # Adjust brightness based on the factor
                r = min(max(int(r * factor), 0), 255)
                g = min(max(int(g * factor), 0), 255)
                b = min(max(int(b * factor), 0), 255)
                
                image_copy.set_at((x, y), (r, g, b, a))
        
        return image_copy
    except Exception as e:
        print(f"Error adjusting brightness: {e}")
        return image