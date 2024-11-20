import pygame

def resize_image(image, new_size):
    """Resize the image to the new size."""
    try:
        resized_image = pygame.transform.scale(image, new_size)
        return resized_image
    except Exception as e:
        print(f"Error resizing image: {e}")
        return image

def adjust_brightness(image, factor):
    """Adjust the brightness of the image."""
    try:
        image_copy = image.copy()
        width, height = image_copy.get_size()
        for x in range(width):
            for y in range(height):
                color = image_copy.get_at((x, y))
                r, g, b, a = color
                r = min(max(int(r * factor), 0), 255)
                g = min(max(int(g * factor), 0), 255)
                b = min(max(int(b * factor), 0), 255)
                image_copy.set_at((x, y), (r, g, b, a))
        return image_copy
    except Exception as e:
        print(f"Error adjusting brightness: {e}")
        return image

def rotate_image(image, angle):
    """Rotate the image by the given angle."""
    try:
        rotated_image = pygame.transform.rotate(image, angle)
        return rotated_image
    except Exception as e:
        print(f"Error rotating image: {e}")
        return image

def save_image(image, filename):
    """Save the image to a file."""
    try:
        pygame.image.save(image, filename)
        print(f"Image saved as {filename}")
    except Exception as e:
        print(f"Error saving image: {e}")
