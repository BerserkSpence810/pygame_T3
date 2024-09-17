import pygame
import sys
import time
import math
from tutorial_level import run_tutorial_level
from L1 import run_first_level  # Corrected function import

def draw_text(text, font, color, surface, x, y, center=False):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    if center:
        textrect.center = (x, y)
    else:
        textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main_menu(screen, SCREEN_WIDTH, SCREEN_HEIGHT):
    clock = pygame.time.Clock()
    menu_running = True
    fade_to_black = False
    fade_alpha = 0

    pygame.mixer.music.load('main.mp3')
    pygame.mixer.music.play(-1)  # Loop indefinitely

    title_font = pygame.font.SysFont(None, 80)
    button_font = pygame.font.SysFont(None, 50)

    float_offset = 0

    button_width = 200
    button_height = 50
    play_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2, button_width, button_height)
    assets_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + 60, button_width, button_height)
    exit_button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 + 120, button_width, button_height)

    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    fade_to_black = True
                elif assets_button.collidepoint(event.pos):
                    print("All assets used are at utils.py couldn't finish the button")
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        float_offset = 10 * math.sin(pygame.time.get_ticks() / 500)

        if fade_to_black:
            fade_alpha += 5
            if fade_alpha >= 255:
                menu_running = False
                cutscene(screen, SCREEN_WIDTH, SCREEN_HEIGHT)

        screen.fill((255, 255, 255))

        draw_text("Cube Quest", title_font, (0, 0, 0), screen, SCREEN_WIDTH // 2,
                  SCREEN_HEIGHT // 2 - 150 + float_offset, center=True)

        play_button.y = SCREEN_HEIGHT // 2 + float_offset
        pygame.draw.rect(screen, (0, 0, 0), play_button)
        draw_text("PLAY", button_font, (255, 255, 255), screen, play_button.centerx, play_button.centery, center=True)

        assets_button.y = SCREEN_HEIGHT // 2 + 60 + float_offset
        pygame.draw.rect(screen, (0, 0, 0), assets_button)
        draw_text("ASSETS", button_font, (255, 255, 255), screen, assets_button.centerx, assets_button.centery, center=True)

        exit_button.y = SCREEN_HEIGHT // 2 + 120 + float_offset
        pygame.draw.rect(screen, (0, 0, 0), exit_button)
        draw_text("EXIT GAME", button_font, (255, 255, 255), screen, exit_button.centerx, exit_button.centery, center=True)

        if fade_alpha > 0:
            fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surface.set_alpha(fade_alpha)
            fade_surface.fill((0, 0, 0))
            screen.blit(fade_surface, (0, 0))

        pygame.display.update()
        clock.tick(30)

def cutscene(screen, SCREEN_WIDTH, SCREEN_HEIGHT):
    clock = pygame.time.Clock()
    cutscene_running = True

    storyline = [
        "Long ago, the Blue squares discovered",
        "the rare and sought for Red squares.",
        "These Red squares have immense value.",
        "Your mission is to collect them and",
        "raise money to pay off your crippling debt",
        "from buying a house."
    ]

    font = pygame.font.SysFont(None, 40)
    text_speed = 0.05
    text_y_start = SCREEN_HEIGHT // 2 - 100
    line_height = 50

    fade_out = False
    fade_alpha = 0

    text_index = 0
    char_index = 0
    text_completed = False
    text_start_time = time.time()

    continue_button = pygame.Rect(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 200, 150, 50)

    while cutscene_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and text_completed:
                if continue_button.collidepoint(event.pos):
                    fade_out = True
        if not text_completed:
            current_time = time.time()
            if current_time - text_start_time > text_speed:
                char_index += 1
                text_start_time = current_time
                if char_index > len(storyline[text_index]):
                    char_index = 0
                    text_index += 1
                    if text_index >= len(storyline):
                        text_completed = True

        if fade_out:
            fade_alpha += 5
            if fade_alpha >= 255:
                cutscene_running = False
                run_tutorial_level(screen, SCREEN_WIDTH, SCREEN_HEIGHT, run_first_level)

        screen.fill((0, 0, 0))

        for i in range(text_index):
            draw_text(storyline[i], font, (255, 255, 255), screen, SCREEN_WIDTH // 2, text_y_start + i * line_height,
                      center=True)

        if text_index < len(storyline):
            draw_text(storyline[text_index][:char_index], font, (255, 255, 255), screen, SCREEN_WIDTH // 2,
                      text_y_start + text_index * line_height, center=True)

        if text_completed:
            pygame.draw.rect(screen, (0, 0, 0), continue_button)
            draw_text("CONTINUE", font, (255, 255, 255), screen, continue_button.centerx, continue_button.centery, center=True)

        if fade_alpha > 0:
            fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surface.set_alpha(fade_alpha)
            fade_surface.fill((0, 0, 0))
            screen.blit(fade_surface, (0, 0))

        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Cube Quest')
    main_menu(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    pygame.quit()