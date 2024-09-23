#Assets section.
import pygame

class FloatingText: # ChatGPT. Somewhat used as a base
    """Displays floating text with a fade-out effect over a specified duration."""

    def __init__(self, text, font, color, screen, x, y, duration):
        self.text = text
        self.font = font
        self.color = color
        self.screen = screen
        self.x = x
        self.y = y
        self.alpha = 255
        self.duration = duration * 60
        self.frame_count = 0

    def update(self):
        """Updates the text's alpha value to create a fading effect."""
        self.frame_count += 1
        if self.frame_count >= self.duration:
            self.alpha = max(0, self.alpha - 5)

#unused sword code
# def draw_sword(screen, x, y, hilt_width, hilt_height, blade_length, blade_color, hilt_color):
#     """ Draws a simple pixelated sword using rectangles and lines. """
#     # Draw the blade (gray)
#     pygame.draw.rect(screen, blade_color, (x + hilt_width // 2 - 2, y, 4, blade_length))  # Thin blade
#
#      Draw the hilt (brown)
#     pygame.draw.rect(screen, hilt_color, (x, y + blade_length, hilt_width, hilt_height))  # Handle