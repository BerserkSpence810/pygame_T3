import pygame
#Chat GPT code Some stuff is based off of.

def draw_text(text, font, color, surface, x, y, center=False):
    """Draws text on the given surface at the specified position, with optional centering."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y) if center else (0, 0))
    if not center:
        text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


class FloatingText:
    """Displays floating text with a fade-out effect over a specified duration."""

    def __init__(self, text, font, color, screen, x, y, duration):
        self.text = text
        self.font = font
        self.color = color
        self.screen = screen
        self.x = x
        self.y = y
        self.alpha = 255
        self.duration = duration * 60  # Duration in frames (assuming 60 FPS)
        self.frame_count = 0

    def update(self):
        """Updates the text's alpha value to create a fading effect."""
        self.frame_count += 1
        if self.frame_count >= self.duration:
            self.alpha = max(0, self.alpha - 5)

    def draw(self):
        """Renders the text on the screen with the current alpha value."""
        text_surface = self.font.render(self.text, True, self.color)
        text_surface.set_alpha(self.alpha)
        self.screen.blit(text_surface, (self.x - text_surface.get_width() // 2, self.y))