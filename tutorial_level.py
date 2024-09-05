import pygame
import math
import sys
import L1

def run_tutorial_level(screen, SCREEN_WIDTH, SCREEN_HEIGHT, run_first_level):
    clock = pygame.time.Clock()
    running = True

    #Fonts
    normal_font = pygame.font.SysFont(None, 30)
    button_font = pygame.font.SysFont(None, 40)
    wallet_font = pygame.font.SysFont(None, 28, bold=True)

    #Player Settings
    player_color = (0, 128, 255)
    player_size = 50
    player_x = SCREEN_WIDTH // 2
    player_y = SCREEN_HEIGHT - player_size
    player_velocity = 8

    #Gravity
    gravity = 1
    jump_strength = -15
    player_velocity_y = 0
    is_jumping = False

    #Item Settings
    item_color = (255, 0, 0)
    item_size = 30
    special_item = (SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT - item_size)
    items = [special_item]
    collected_items = 0
    show_interact_e = False

    # NEXT Button
    button_text = "NEXT"
    button_rect = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 50, 140, 40)
    button_color = (0, 0, 0)
    show_button_e = False

    #Instructions
    instructions = [
        "Use ARROW KEYS to move",
        "Press SPACE to jump",
        "Press 'E' to interact and collect",
        "(You have to interact with next buttons)"
    ]
    float_offset = 0

    #Fade
    fade_alpha = 255
    fade_speed = 3
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))


    fade_out = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        #Level Skip (Broken)
        if keys[pygame.K_9]:
            run_first_level(screen, SCREEN_WIDTH, SCREEN_HEIGHT, collected_items, run_tutorial_level)
            return

        #Movement
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

        if moving:
            pygame.draw.line(
                screen,
                (100, 100, 100),
                (player_x, player_y + player_size),
                (player_x + player_size, player_y + player_size + 10),
                3
            )

        float_offset = 10 * math.sin(pygame.time.get_ticks() / 500)

        screen.fill((255, 255, 255))
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        pygame.draw.rect(screen, player_color, player_rect)

        show_interact_e = False
        for item_x, item_y in items[:]:
            item_rect = pygame.Rect(item_x, item_y, item_size, item_size)
            pygame.draw.rect(screen, item_color, item_rect)
            if player_rect.colliderect(item_rect):
                show_interact_e = True
                if keys[pygame.K_e]:
                    items.remove((item_x, item_y))
                    collected_items += 1

        show_button_e = False
        pygame.draw.rect(screen, button_color, button_rect)
        draw_text(button_text, button_font, (255, 255, 255), screen, button_rect.centerx, button_rect.centery, center=True)

        if player_rect.colliderect(button_rect):
            show_button_e = True
            if keys[pygame.K_e]:
                fade_out = True

        for idx, line in enumerate(instructions):
            draw_text(line, normal_font, (0, 0, 0), screen, SCREEN_WIDTH // 2, 50 + idx * 30 + float_offset, center=True)

        for i in range(collected_items):
            pygame.draw.rect(screen, item_color, (10 + 25 * i, 40, 20, 20))

        draw_text("Wallet", wallet_font, (0, 0, 0), screen, 20, 10)

        #Floating E
        if show_interact_e:
            draw_text("E", button_font, (0, 0, 0), screen, player_x + player_size // 2, player_y - 20 + float_offset, center=True)
        if show_button_e:
            draw_text("E", button_font, (0, 0, 0), screen, button_rect.centerx, button_rect.centery - 40 + float_offset, center=True)

        if fade_out:
            fade_alpha += fade_speed
            if fade_alpha >= 255:
                fade_alpha = 255
                L1.run_first_level(screen, SCREEN_WIDTH, SCREEN_HEIGHT, collected_items, run_first_level)
                return
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))

        if fade_alpha > 0 and not fade_out:
            fade_alpha -= fade_speed
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))

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
