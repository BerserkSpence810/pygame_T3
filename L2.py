import pygame
import sys
import math
import L3

def run_second_level(screen, SCREEN_WIDTH, SCREEN_HEIGHT, collected_items):
    clock = pygame.time.Clock()
    running = True

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

    # Green Enemy Settings
    green_cube_color = (0, 255, 0)
    green_cube_size = 70
    green_cube_x = SCREEN_WIDTH - 200
    green_cube_y = SCREEN_HEIGHT - green_cube_size
    green_cube_velocity = 1
    green_cube_alive = True

    # Red Cube
    item_colour = (255, 0, 0)
    item_size = 30
    special_item = (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - item_size)
    items = [special_item]
    show_interact_e = False
    red_cube_dropped = False
    red_cube_rect = None

    # Platform
    platform_color = (100, 100, 100)
    platform_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 20)

    # Next Button
    button_text = "NEXT"
    button_rect = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 50, 140, 40)
    button_color = (0, 0, 0)
    show_button_e = False

    # Fading
    fade_alpha = 255
    fade_speed = 3
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))
    fading_in = True
    fading_out = False

    # Instructions
    instructions = [
        "The green cubes are",
        "larger than yellow cubes",
        "but move slower"
    ]
    float_offset = 0

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

        # Enemy movement
        if green_cube_x < player_x:
            green_cube_x += green_cube_velocity
        elif green_cube_x > player_x:
            green_cube_x -= green_cube_velocity

        screen.fill((255, 255, 255))

        # Player
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        pygame.draw.rect(screen, player_color, player_rect)

        # Platform Collision
        if player_rect.colliderect(platform_rect):
            if player_velocity_y > 0 and player_y + player_size <= platform_rect.top + 10:
                player_y = platform_rect.top - player_size
                player_velocity_y = 0
                is_jumping = False
            elif player_y + player_size > platform_rect.bottom:
                player_velocity_y = gravity

        # Interaction
        show_interact_e = False
        for item_x, item_y in items[:]:
            item_rect = pygame.Rect(item_x, item_y, item_size, item_size)
            pygame.draw.rect(screen, item_colour, item_rect)
            if player_rect.colliderect(item_rect):
                show_interact_e = True
                if keys[pygame.K_e]:
                    items.remove((item_x, item_y))
                    collected_items += 1

        # Next Button
        show_button_e = False
        pygame.draw.rect(screen, button_color, button_rect)
        draw_text(button_text, button_font, (255, 255, 255), screen, button_rect.centerx, button_rect.centery, center=True)

        if player_rect.colliderect(button_rect):
            show_button_e = True
            if keys[pygame.K_e] and not fading_out:
                fading_out = True

        if fading_in:
            fade_alpha -= fade_speed
            if fade_alpha <= 0:
                fade_alpha = 0
                fading_in = False

        if fading_out:
            fade_alpha += fade_speed
            if fade_alpha >= 255:
                fade_alpha = 255
                L3.run_third_level(screen, SCREEN_WIDTH, SCREEN_HEIGHT, collected_items)
                return

        if fade_alpha > 0:
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))

        # Green cube
        green_cube_rect = pygame.Rect(green_cube_x, green_cube_y, green_cube_size, green_cube_size)
        pygame.draw.rect(screen, green_cube_color, green_cube_rect)

        if player_rect.colliderect(green_cube_rect):
            screen.fill((0, 0, 0))
            draw_text("YOU GOT ROBBED", button_font, (255, 0, 0), screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
            pygame.display.update()
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit()

        # Platform
        pygame.draw.rect(screen, platform_color, platform_rect)

        # Wallet
        for i in range(collected_items):
            pygame.draw.rect(screen, item_colour, (10 + 25 * i, 40, 20, 20))
        draw_text("Wallet", wallet_font, (0, 0, 0), screen, 20, 10)

        if show_interact_e:
            draw_text("E", button_font, (0, 0, 0), screen, player_x + player_size // 2, player_y - 20, center=True)
        if show_button_e:
            draw_text("E", button_font, (0, 0, 0), screen, button_rect.centerx, button_rect.centery - 40, center=True)

        # Instructions display
        float_offset = 10 * math.sin(pygame.time.get_ticks() / 500)
        for idx, line in enumerate(instructions):
            draw_text(line, normal_font, (0, 0, 0), screen, SCREEN_WIDTH // 2, 50 + idx * 30 + float_offset, center=True)

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
