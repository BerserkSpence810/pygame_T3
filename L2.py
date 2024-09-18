import pygame
import sys
import math
import L3
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
    player_has_sword = False
    player_attack_cooldown = 0  # Cooldown timer for sword attack

    # Sword (drawn with Pygame)
    # sword_color = (169, 169, 169)
    # sword_hilt_color = (139, 69, 19)
    # sword_blade_length = 30
    # sword_hilt_width = 15
    # sword_hilt_height = 10
    # sword_x = SCREEN_WIDTH // 4
    # sword_y = SCREEN_HEIGHT - player_size - 60
    # sword_picked_up = False
    # sword_rect = pygame.Rect(sword_x, sword_y, sword_hilt_width, sword_blade_length + sword_hilt_height)

    # Gravity
    gravity = 1
    jump_strength = -15
    player_velocity_y = 0
    is_jumping = False

    # Enemy Settings (Green Cube)
    green_cube_color = (0, 255, 0)
    green_cube_size = 80
    green_cube_x = SCREEN_WIDTH -200
    green_cube_y = SCREEN_HEIGHT - green_cube_size
    green_cube_velocity = 1
    green_cube_alive = True

    #red cube
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
    fade_alpha = 255  # Start fully black
    fade_speed = 3
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))
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

        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

        # # Sword Pickup
        # if not sword_picked_up and player_rect.colliderect(sword_rect):
        #     if keys[pygame.K_e]:
        #         sword_picked_up = True
        #         player_has_sword = True
        #
        # # Sword Swing (Attack keybind)
        # if player_has_sword and keys[pygame.K_RETURN] and player_attack_cooldown == 0:
        #     # Perform attack animation (short duration of swing)
        #     player_attack_cooldown = 15  # Cooldown for attack
        #     sword_swing_rect = pygame.Rect(player_x + player_size, player_y, 80, 20)  # Sword swing hitbox
        #
        #     # Check if the sword hit the green cube
        #     green_cube_rect = pygame.Rect(green_cube_x, green_cube_y, green_cube_size, green_cube_size)
        #     if green_cube_alive and sword_swing_rect.colliderect(green_cube_rect):
        #         # Kill the green cube and drop a red cube
        #         green_cube_alive = False
        #         red_cube_rect = pygame.Rect(green_cube_x, green_cube_y, item_size, item_size)
        #         red_cube_dropped = True

        # Platform Collision
        if player_rect.colliderect(platform_rect):
            if player_velocity_y > 0 and player_y + player_size <= platform_rect.top + 10:
                player_y = platform_rect.top - player_size
                player_velocity_y = 0
                is_jumping = False
            elif player_y + player_size > platform_rect.bottom:
                player_velocity_y = gravity

        # Green cube movement (enemy)
        if green_cube_x < player_x:
            green_cube_x += green_cube_velocity
        elif green_cube_x > player_x:
            green_cube_x -= green_cube_velocity
            #if green_cube_x <= platform_rect.left or green_cube_x + green_cube_size >= platform_rect.right:
                #green_cube_velocity = -green_cube_velocity

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
                fading_out = True  # Start fade out

        if fading_out:
            fade_alpha += fade_speed
            if fade_alpha >= 255:
                fade_alpha = 255
                L3.run_third_level(screen, SCREEN_WIDTH, SCREEN_HEIGHT, collected_items)
                return
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))


        # Drawing objects
        screen.fill((255, 255, 255))

        # Player
        pygame.draw.rect(screen, player_color, player_rect)

        # Sword (drawn with Pygame shapes)
        #if not sword_picked_up:
            #draw_sword(screen, sword_x, sword_y, sword_hilt_width, sword_hilt_height, sword_blade_length, sword_color, sword_hilt_color)

        # Display sword on the player after it's picked up
        #if player_has_sword:
            #draw_sword(screen, player_x + player_size // 2 - sword_hilt_width // 2, player_y - sword_blade_length, sword_hilt_width, sword_hilt_height, sword_blade_length, sword_color, sword_hilt_color)

        # Green cube (only if it's still alive)
        if green_cube_alive:
            green_cube_rect = pygame.Rect(green_cube_x, green_cube_y, green_cube_size, green_cube_size)
            pygame.draw.rect(screen, green_cube_color, green_cube_rect)

        # # Red cube (if green cube was killed)
        # if red_cube_dropped:
        #     pygame.draw.rect(screen, item_colour, red_cube_rect)



        # Check if player picks up the red cube
        show_interact_e = False
        for item_x, item_y in items[:]:
            item_rect = pygame.Rect(item_x, item_y, item_size, item_size)
            pygame.draw.rect(screen, item_colour, item_rect)
            if player_rect.colliderect(item_rect):
                show_interact_e = True
                if keys[pygame.K_e]:
                    items.remove((item_x, item_y))
                    collected_items += 1
            red_cube_dropped = False

        # Display wallet (collected items)
        for i in range(collected_items):
            pygame.draw.rect(screen, item_colour, (10 + 25 * i, 40, 20, 20))

        draw_text("Wallet", wallet_font, (0, 0, 0), screen, 20, 10)

        if show_interact_e:
            draw_text("E", button_font, (0, 0, 0), screen, player_x + player_size // 2, player_y - 20, center=True)
        if show_button_e:
            draw_text("E", button_font, (0, 0, 0), screen, button_rect.centerx, button_rect.centery - 40, center=True)

        # Display Instructions
        float_offset = 10 * math.sin(pygame.time.get_ticks() / 500)
        for idx, line in enumerate(instructions):
            draw_text(line, normal_font, (0, 0, 0), screen, SCREEN_WIDTH // 2, 50 + idx * 30 + float_offset, center=True)

        # Death sequence if killed by cube
        if not green_cube_alive and player_rect.colliderect(green_cube_rect):
            # "You got robbed" scene
            draw_text("You got robbed!", normal_font, (255, 0, 0), screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
            pygame.display.update()
            pygame.time.wait(2000)  # Display message for 2 seconds
            running = False

        # Platform
        pygame.draw.rect(screen, platform_color, platform_rect)

        # Fade-in effect
        if fade_alpha > 0:
            fade_alpha -= fade_speed
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))

        # Handle attack cooldown
        if player_attack_cooldown > 0:
            player_attack_cooldown -= 1

        pygame.display.update()
        clock.tick(30)

#def draw_sword(screen, x, y, hilt_width, hilt_height, blade_length, blade_color, hilt_color):
    #""" Draws a simple pixelated sword using rectangles and lines. """
    # Draw the blade (gray)
    #pygame.draw.rect(screen, blade_color, (x + hilt_width // 2 - 2, y, 4, blade_length))  # Thin blade

    # Draw the hilt (brown)
    #pygame.draw.rect(screen, hilt_color, (x, y + blade_length, hilt_width, hilt_height))  # Handle

def draw_text(text, font, color, surface, x, y, center=False):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    if center:
        textrect.center = (x, y)
    else:
        textrect.topleft = (x, y)
    surface.blit(textobj, textrect)