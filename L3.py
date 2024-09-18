import pygame
import sys

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
    green_cube_velocity = 2
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

    # Fading
    fade_alpha = 255  # Start fully black
    fade_speed = 3
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))
    fading_out = False

    # Next Button
    button_text = "NEXT"
    button_rect = pygame.Rect(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 50, 140, 40)
    button_color = (0, 0, 0)
    show_button_e = False

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
