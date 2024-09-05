import pygame
import sys
import math

def run_second_level(screen, SCREEN_WIDTH, SCREEN_HEIGHT, collected_items):
    clock = pygame.time.Clock()
    running = True

    # Fonts
    normal_font = pygame.font.SysFont(None, 30)
    button_font = pygame.font.SysFont(None, 40)
    wallet_font = pygame.font.SysFont(None, 28, bold=True)

    # Player Settings
    player_color = (0, 128, 255)
    player_size = 50
    player_x = 50  # Player Start
    player_y = SCREEN_HEIGHT - player_size
    player_velocity = 8

    # Gravity
    gravity = 1
    jump_strength = -15
    player_velocity_y = 0
    is_jumping = False

    # Enemy Settings
    green_cube_color = (0, 255, 0)
    green_cube_size = 40
    green_cube_x = SCREEN_WIDTH // 2
    green_cube_y = SCREEN_HEIGHT - green_cube_size - 100
    green_cube_velocity = 2

    # Platform for green cube
    platform_color = (100, 100, 100)
    platform_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 20)

    # Fading
    fade_alpha = 255  # Start fully black
    fade_speed = 3
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))
    fading_out = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        # Player movement
        moving = False
        if keys[pygame.K_LEFT]:
            player_x -= player_velocity
            moving = True
        if keys[pygame.K_RIGHT]:
            player_x += player_velocity
            moving = True

        if keys[pygame.K_SPACE] and not is_jumping:
            player_velocity_y = jump_strength
            is_jumping = True

        player_velocity_y += gravity
        player_y += player_velocity_y

        if player_y >= SCREEN_HEIGHT - player_size:
            player_y = SCREEN_HEIGHT - player_size
            player_velocity_y = 0
            is_jumping = False

        # Green cube movement (enemy)
        green_cube_x += green_cube_velocity
        if green_cube_x <= platform_rect.left or green_cube_x + green_cube_size >= platform_rect.right:
            green_cube_velocity = -green_cube_velocity

        # Drawing objects
        screen.fill((255, 255, 255))

        # Player
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        pygame.draw.rect(screen, player_color, player_rect)

        # Green cube enemy
        green_cube_rect = pygame.Rect(green_cube_x, green_cube_y, green_cube_size, green_cube_size)
        pygame.draw.rect(screen, green_cube_color, green_cube_rect)

        # Platform
        pygame.draw.rect(screen, platform_color, platform_rect)

        # Check for collision with green cube
        if player_rect.colliderect(green_cube_rect):
            # Handle player death or restart
            fading_out = True

        # Fade-in effect
        if fade_alpha > 0:
            fade_alpha -= fade_speed
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))

        # Display updates
        pygame.display.update()
        clock.tick(30)

def draw_text(text, font, color, surface, x, y, center=False):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    if center:
        textrect.center = (x, y)
    else:
        textrect.topleft = (x, y)
    surface.blit(textobj, textrect)