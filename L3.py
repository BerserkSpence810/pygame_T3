import pygame
import sys
import math
import L2

def run_third_level(screen, SCREEN_WIDTH, SCREEN_HEIGHT, collected_items):
    clock = pygame.time.Clock()
    running = True

    # Fonts
    normal_font = pygame.font.SysFont(None, 30)
    button_font = pygame.font.SysFont(None, 40)
    wallet_font = pygame.font.SysFont(None, 28, bold=True)

    # Player Settings
    player_color = (0, 128, 255)
    player_size = 50
    player_x = 50
    player_y = SCREEN_HEIGHT - player_size
    player_velocity = 8

    # Gravity
    gravity = 1
    jump_strength = -15
    player_velocity_y = 0
    is_jumping = False

    # Enemy Settings (Yellow Cube)
    yellow_enemy_color = (255, 255, 0)
    yellow_enemy_size = 50
    yellow_enemy_x = SCREEN_WIDTH - 200
    yellow_enemy_y = SCREEN_HEIGHT - yellow_enemy_size
    yellow_enemy_velocity = 2
    yellow_enemy_jump_strength = -1
    yellow_enemy_velocity_y = 0
    yellow_enemy_is_jumping = False

    # Enemy Settings (Green Cube)
    green_cube_color = (0, 255, 0)
    green_cube_size = 70
    green_cube_x = SCREEN_WIDTH - 200
    green_cube_y = SCREEN_HEIGHT - green_cube_size
    green_cube_velocity = 1
    green_cube_alive = True

    # Red Cube
    item_color = (255, 0, 0)
    item_size = 30
    special_item = (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - item_size)
    items = [special_item]
    show_interact_e = False

    # Red Cube 2
    item_color_2 = (255, 0, 0)
    item_size_2 = 30
    special_item_2 = (SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT - 220)
    items_2 = [special_item_2]
    show_interact_e_2 = False

    # Next Button
    button_text = "NEXT"
    button_rect = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 50, 140, 40)
    button_color = (0, 0, 0)
    show_button_e = False

    # Fading
    fade_alpha = 255  # Start fully opaque (for fade-in)
    fade_speed = 3
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))
    fading_in = True
    fading_out = False

    # Death Cutscene
    death_cutscene_running = False

    # Instructions
    instructions = [
        "Be Careful!",
        "You can only jump on",
        "Platforms once"
    ]
    float_offset = 0

    # Platform
    platform_color = (100, 100, 100)
    platform_rect = pygame.Rect(SCREEN_WIDTH // 2 - 0, SCREEN_HEIGHT - 200, 200, 20)

    # Platform 2
    platform_color_2 = (100, 100, 100)
    platform_rect_2 = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 100, 200, 20)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if death_cutscene_running:
            screen.fill((0, 0, 0))
            draw_text("YOU GOT ROBBED", button_font, (255, 0, 0), screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
            pygame.display.update()
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit()

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

        if moving:
            pygame.draw.line(
                screen,
                (100, 100, 100),  # The line color
                (player_x, player_y + player_size),
                (player_x + player_size, player_y + player_size + 10),
                3
            )

        # Green cube movement (enemy)
        if green_cube_x < player_x:
            green_cube_x += green_cube_velocity
        elif green_cube_x > player_x:
            green_cube_x -= green_cube_velocity

        screen.fill((255, 255, 255))

        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        pygame.draw.rect(screen, player_color, player_rect)

        # Platform Collision 1
        if player_rect.colliderect(platform_rect):
            if player_velocity_y > 0:
                if player_y + player_size <= platform_rect.top + 10:
                    player_y = platform_rect.top - player_size
                    player_velocity_y = 0
                    is_jumping = False

        # Platform Collision 2
        if player_rect.colliderect(platform_rect_2):
            if player_velocity_y > 0:
                if player_y + player_size <= platform_rect_2.top + 10:
                    player_y = platform_rect_2.top - player_size
                    player_velocity_y = 0
                    is_jumping = False

        # Yellow Enemy
        enemy_rect = pygame.Rect(yellow_enemy_x, yellow_enemy_y, yellow_enemy_size, yellow_enemy_size)
        pygame.draw.rect(screen, yellow_enemy_color, enemy_rect)

        # Enemy Tracking
        if yellow_enemy_x < player_x:
            yellow_enemy_x += yellow_enemy_velocity
        elif yellow_enemy_x > player_x:
            yellow_enemy_x -= yellow_enemy_velocity

        # Nil jump for yellow enemy
        if player_y < yellow_enemy_y and not yellow_enemy_is_jumping:
            yellow_enemy_velocity_y = yellow_enemy_jump_strength
            yellow_enemy_is_jumping = True

        yellow_enemy_velocity_y += gravity
        yellow_enemy_y += yellow_enemy_velocity_y

        if yellow_enemy_y >= SCREEN_HEIGHT - yellow_enemy_size:
            yellow_enemy_y = SCREEN_HEIGHT - yellow_enemy_size
            yellow_enemy_velocity_y = 0
            yellow_enemy_is_jumping = False

        # Enemy Detection
        if player_rect.colliderect(enemy_rect):
            death_cutscene_running = True

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

        if player_rect.colliderect(enemy_rect):
            screen.fill((0, 0, 0))
            draw_text("YOU GOT ROBBED", button_font, (255, 0, 0), screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
            pygame.display.update()
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit()

        # Interaction with Red Cube
        show_interact_e = False
        for item_x, item_y in items[:]:
            item_rect = pygame.Rect(item_x, item_y, item_size, item_size)
            pygame.draw.rect(screen, item_color, item_rect)
            if player_rect.colliderect(item_rect):
                show_interact_e = True
                if keys[pygame.K_e]:
                    items.remove((item_x, item_y))
                    collected_items += 1

        # Interaction with Red Cube 2
        show_interact_e_2 = False
        for item_x_2, item_y_2 in items_2[:]:
            item_rect_2 = pygame.Rect(item_x_2, item_y_2, item_size_2, item_size_2)
            pygame.draw.rect(screen, item_color_2, item_rect_2)
            if player_rect.colliderect(item_rect_2):
                show_interact_e_2 = True
                if keys[pygame.K_e]:
                    items_2.remove((item_x_2, item_y_2))
                    collected_items += 1

        # Next Button
        show_button_e = False
        pygame.draw.rect(screen, button_color, button_rect)
        draw_text(button_text, button_font, (255, 255, 255), screen, button_rect.centerx, button_rect.centery, center=True)

        if player_rect.colliderect(button_rect):
            show_button_e = True
            if keys[pygame.K_e] and not fading_out and not fading_in:
                fading_out = True  # Start fade out

        # Fading logic
        if fading_in:
            fade_alpha -= fade_speed
            if fade_alpha <= 0:
                fade_alpha = 0
                fading_in = False

        if fading_out:
            fade_alpha += fade_speed
            if fade_alpha >= 255:
                running = False
                L2.run_second_level(screen, SCREEN_WIDTH, SCREEN_HEIGHT, collected_items)  # Transition to next level

        # Platform rendering
        pygame.draw.rect(screen, platform_color, platform_rect)
        pygame.draw.rect(screen, platform_color_2, platform_rect_2)

        # Display collected items
        for i in range(collected_items):
            pygame.draw.rect(screen, item_color, (10 + 25 * i, 40, 20, 20))

        draw_text("Wallet", wallet_font, (0, 0, 0), screen, 20, 10)

        # Floating "E" for interactables
        if show_interact_e:
            draw_text("E", button_font, (0, 0, 0), screen, player_x + player_size // 2, player_y - 20, center=True)
        if show_interact_e_2:
            draw_text("E", button_font, (0, 0, 0), screen, player_x + player_size // 2, player_y - 20, center=True)
        if show_button_e:
            draw_text("E", button_font, (0, 0, 0), screen, button_rect.centerx, button_rect.centery - 40, center=True)

        # Instructions display
        float_offset = 10 * math.sin(pygame.time.get_ticks() / 500)
        for idx, line in enumerate(instructions):
            draw_text(line, normal_font, (0, 0, 0), screen, SCREEN_WIDTH // 2, 50 + idx * 30 + float_offset, center=True)

        # Render fade effect
        if fading_in or fading_out:
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))

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
