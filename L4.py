import pygame
import sys


def run_cutscene(screen, SCREEN_WIDTH, SCREEN_HEIGHT, collected_items, target_items):
    clock = pygame.time.Clock()
    running = True

    # Fonts
    normal_font = pygame.font.SysFont(None, 20)  # Smaller font
    button_font = pygame.font.SysFont(None, 40)

    # Colors
    BLACK = (0, 0, 0)
    POP_COLOR = (255, 215, 0)  # Gold color to pop out

    # Fading variables
    fade_alpha = 255  # Start fully opaque (for fade-in)
    fade_speed = 3
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill(BLACK)
    fading_in = True

    # Messages
    success_message = "You repaid your debt"
    failure_message = "You couldn't pay off your debt. The Cube Mafia wasn't happy."

    # Determine which message and image to display
    if collected_items >= target_items:
        storyline_message = success_message
        message_color = POP_COLOR
        image = pygame.image.load("Good.png")
    else:
        storyline_message = failure_message
        message_color = POP_COLOR
        image = pygame.image.load("Bad.png")

    # Scale the image to fit nicely on the screen (you can adjust scaling as needed)
    image = pygame.transform.scale(image, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    image_rect = image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Background
        screen.fill(BLACK)

        # Display storyline message at the top of the screen, centered
        draw_text(storyline_message, normal_font, message_color, screen, SCREEN_WIDTH // 2, 50, center=True)

        # Display the Good.png or Bad.png image
        screen.blit(image, image_rect)

        # Fading logic
        if fading_in:
            fade_alpha -= fade_speed
            if fade_alpha <= 0:
                fade_alpha = 0
                fading_in = False

        # Render fade effect
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))

        # Update the screen
        pygame.display.update()
        clock.tick(30)


def draw_text(text, font, color, surface, x, y, center=False):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


# Example to run the cutscene
if __name__ == "__main__":
    pygame.init()
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Debt Repayment Cutscene")

    collected_items = 4  # Change this to test different outcomes
    target_items = 5  # Required items to win

    run_cutscene(screen, SCREEN_WIDTH, SCREEN_HEIGHT, collected_items, target_items)

    pygame.quit()
    sys.exit()
