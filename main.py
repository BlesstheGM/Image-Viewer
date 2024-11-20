import pygame
from utils.directory_picker import pick_directory
from utils.favorites import FavoritesManager
from utils.image_handler import load_images, load_image, scale_image
from utils.image_selector import select_images

# Initialize Pygame
pygame.init()

# Constants
BG_COLOR = (30, 30, 30)
BUTTON_COLOR = (50, 50, 200)
BUTTON_HOVER_COLOR = (80, 80, 255)
TEXT_COLOR = (255, 255, 255)
PANEL_COLOR = (20, 20, 20)
PADDING = 20
PANEL_WIDTH = 250
BUTTON_HEIGHT = 50
ICON_PATH = "icon.jpg"

# Initialize app variables
current_directory = "images"
images = load_images(current_directory)
current_image_index = 0
favorites = FavoritesManager()
favorite_images = []
favorite_index = 0

# Set up the display
screen = pygame.display.set_mode((1000, 600), pygame.RESIZABLE)
pygame.display.set_caption("Image Viewer")
if ICON_PATH:
    icon = pygame.image.load(ICON_PATH)
    pygame.display.set_icon(icon)
font = pygame.font.Font(None, 28)

# Draw button
def draw_button(screen, rect, text, is_hovered):
    color = BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR
    pygame.draw.rect(screen, color, rect)
    text_surface = font.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

# Helper functions
def reload_folder():
    global current_directory, images, current_image_index
    directory = pick_directory()
    if directory:
        current_directory = directory
        images = load_images(current_directory)
        current_image_index = 0

def add_images():
    global images, current_image_index
    selected_images = select_images()
    if selected_images:
        images = selected_images
        current_image_index = 0

def add_to_favorites():
    if images and current_image_index < len(images):
        favorites.add_to_favorites(images[current_image_index])
        print("Added to favorites:", images[current_image_index])

def remove_from_favorites():
    if favorite_images and favorite_index < len(favorite_images):
        favorites.remove_from_favorites(favorite_images[favorite_index])
        print("Removed from favorites:", favorite_images[favorite_index])

def open_favorites():
    global favorite_images, favorite_index
    favorite_images = favorites.get_favorites()
    favorite_index = 0

# Favorites window loop
def favorites_window():
    global favorite_images, favorite_index
    running = True
    selected_images = []  # To store selected image paths

    while running:
        screen_width, screen_height = screen.get_size()
        panel_width = PANEL_WIDTH
        grid_start_x = panel_width + PADDING
        grid_start_y = PADDING
        grid_spacing = 10
        thumbnail_size = (150, 150)  # Size of each thumbnail
        images_per_row = (screen_width - panel_width - PADDING) // (thumbnail_size[0] + grid_spacing)

        # Define Home button
        home_button_rect = pygame.Rect(
            PADDING,
            screen_height - BUTTON_HEIGHT - PADDING,
            panel_width - 2 * PADDING,
            BUTTON_HEIGHT,
        )

        panel_buttons = [
            {"label": "Add", "action": lambda: favorites.add_to_favorites()},
            {"label": "Remove", "action": lambda: [
                favorites.remove_from_favorites(img) for img in selected_images
            ]},
        ]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check Home button
                if home_button_rect.collidepoint(event.pos):
                    return  # Close favorites window and return to main screen

                # Check panel buttons
                for i, button in enumerate(panel_buttons):
                    button_rect = pygame.Rect(
                        PADDING,
                        PADDING + i * (BUTTON_HEIGHT + PADDING),
                        panel_width - 2 * PADDING,
                        BUTTON_HEIGHT,
                    )
                    if button_rect.collidepoint(event.pos):
                        button["action"]()

                # Check grid images
                if favorite_images:
                    for idx, image_path in enumerate(favorite_images):
                        row = idx // images_per_row
                        col = idx % images_per_row
                        x = grid_start_x + col * (thumbnail_size[0] + grid_spacing)
                        y = grid_start_y + row * (thumbnail_size[1] + grid_spacing)
                        image_rect = pygame.Rect(x, y, *thumbnail_size)

                        if image_rect.collidepoint(event.pos):
                            if image_path in selected_images:
                                selected_images.remove(image_path)  # Deselect if already selected
                            else:
                                selected_images.append(image_path)  # Select if not already selected

        # Drawing
        screen.fill(BG_COLOR)
        panel_rect = pygame.Rect(0, 0, panel_width, screen_height)
        pygame.draw.rect(screen, PANEL_COLOR, panel_rect)

        # Draw panel buttons
        for i, button in enumerate(panel_buttons):
            button_rect = pygame.Rect(
                PADDING,
                PADDING + i * (BUTTON_HEIGHT + PADDING),
                panel_width - 2 * PADDING,
                BUTTON_HEIGHT,
            )
            draw_button(screen, button_rect, button["label"], button_rect.collidepoint(pygame.mouse.get_pos()))

        # Draw Home button
        draw_button(screen, home_button_rect, "Home", home_button_rect.collidepoint(pygame.mouse.get_pos()))

        # Draw grid of images
        if favorite_images:
            for idx, image_path in enumerate(favorite_images):
                row = idx // images_per_row
                col = idx % images_per_row
                x = grid_start_x + col * (thumbnail_size[0] + grid_spacing)
                y = grid_start_y + row * (thumbnail_size[1] + grid_spacing)
                image_rect = pygame.Rect(x, y, *thumbnail_size)

                try:
                    thumbnail = scale_image(load_image(image_path), thumbnail_size)
                    screen.blit(thumbnail, (x, y))
                except Exception as e:
                    print(f"Error loading image {image_path}: {e}")

                # Highlight selected images
                if image_path in selected_images:
                    pygame.draw.rect(screen, (255, 0, 0), image_rect, 3)  # Red border for selected images

        pygame.display.flip()

# Main loop
running = True
favorites_window_open = False  # Flag to track if the favorites window is open

while running:
    screen_width, screen_height = screen.get_size()

    # Define buttons
    next_button_rect = pygame.Rect(screen_width - 140, screen_height - BUTTON_HEIGHT - PADDING, 120, BUTTON_HEIGHT)
    prev_button_rect = pygame.Rect(280, screen_height - BUTTON_HEIGHT - PADDING, 120, BUTTON_HEIGHT)

    panel_buttons = [
        {"label": "Select Folder", "action": reload_folder},
        {"label": "Select Image", "action": add_images},
        {"label": "Favorites", "action": open_favorites},  # Open favorites window
    ]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if next_button_rect.collidepoint(event.pos):
                current_image_index = (current_image_index + 1) % len(images)
            elif prev_button_rect.collidepoint(event.pos):
                current_image_index = (current_image_index - 1) % len(images)
            
            for i, button in enumerate(panel_buttons):
                button_rect = pygame.Rect(PADDING, PADDING + i * (BUTTON_HEIGHT + PADDING), PANEL_WIDTH - 2 * PADDING, BUTTON_HEIGHT)
                if button_rect.collidepoint(event.pos):
                    # Open favorites window when clicked
                    if button["label"] == "Favorites":
                        favorites_window_open = True  # Set flag to open favorites window
                        open_favorites()  # Call the function to populate the favorites list
                    else:
                        button["action"]()

    # If the favorites window is open, we stop drawing the main screen and show the favorites window instead
    if favorites_window_open:
        favorites_window()  # Open the favorites window loop
        favorites_window_open = False  # Reset flag after closing favorites window
        continue  # Skip the rest of the main loop to prevent drawing the main screen

    # Main screen logic (if favorites window is not open)
    screen.fill(BG_COLOR)
    panel_rect = pygame.Rect(0, 0, PANEL_WIDTH, screen_height)
    pygame.draw.rect(screen, PANEL_COLOR, panel_rect)

    for i, button in enumerate(panel_buttons):
        button_rect = pygame.Rect(PADDING, PADDING + i * (BUTTON_HEIGHT + PADDING), PANEL_WIDTH - 2 * PADDING, BUTTON_HEIGHT)
        draw_button(screen, button_rect, button["label"], button_rect.collidepoint(pygame.mouse.get_pos()))

    if images:
        scaled_image = scale_image(load_image(images[current_image_index]), (screen_width, screen_height - BUTTON_HEIGHT - 2 * PADDING))
        image_rect = scaled_image.get_rect(center=((screen_width + PANEL_WIDTH) // 2, (screen_height - BUTTON_HEIGHT) // 2))
        screen.blit(scaled_image, image_rect)

    draw_button(screen, next_button_rect, "Next", next_button_rect.collidepoint(pygame.mouse.get_pos()))
    draw_button(screen, prev_button_rect, "Previous", prev_button_rect.collidepoint(pygame.mouse.get_pos()))

    pygame.display.flip()

# Quit Pygame
pygame.quit()
