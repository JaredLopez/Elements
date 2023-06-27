import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Elements")

# Load images
background_img = pygame.image.load("forest.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

player_img = pygame.image.load("fire_emblem.png").convert_alpha()
player_width = 50
player_height = 50
player_img = pygame.transform.scale(player_img, (player_width, player_height))
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height
player_vel = 1

enemy_img = pygame.image.load("raindrop.png").convert_alpha()
enemy_width = 50
enemy_height = 50
enemy_img = pygame.transform.scale(enemy_img, (enemy_width, enemy_height))

# Time counter
start_time = time.time()
elapsed_time = 0
timer_stopped = False

# Enemy spawning
spawn_interval = 2.0  # Interval in seconds between enemy spawns
last_spawn_time = start_time

# Font
font = pygame.font.Font(None, 36)

# Game state
game_over = False

# Function to reset the game
def reset_game():
    global player_x, player_y, enemies, start_time, elapsed_time, game_over, timer_stopped, last_spawn_time
    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - player_height
    enemies = []
    start_time = time.time()
    elapsed_time = 0
    game_over = False
    timer_stopped = False
    last_spawn_time = start_time

# Function to create new enemies
def create_enemies(num_enemies):
    for _ in range(num_enemies):
        enemy_x = random.randint(0, WIDTH - enemy_width)
        enemy_y = 0
        enemy_vel = random.uniform(0.25, 1)  # Randomize enemy falling velocity
        enemies.append((enemy_x, enemy_y, enemy_vel))

# Main game loop
enemies = []
create_enemies(6)  # Create initial enemies
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_SPACE:
                reset_game()

    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_vel
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_vel

    # Spawn new enemies
    current_time = time.time()
    if not game_over and current_time - last_spawn_time >= spawn_interval:
        create_enemies(6)  # Create 6 new enemies
        last_spawn_time = current_time

    # Move the enemies
    if not game_over:
        for i, enemy in enumerate(enemies):
            enemy_x, enemy_y, enemy_vel = enemy
            enemy_y += enemy_vel
            if enemy_y > HEIGHT:
                enemies.pop(i)
            else:
                enemies[i] = (enemy_x, enemy_y, enemy_vel)

    # Check for collision
    for enemy in enemies:
        enemy_x, enemy_y, _ = enemy
        if player_x < enemy_x + enemy_width and \
                player_x + player_width > enemy_x and \
                player_y < enemy_y + enemy_height and \
                player_y + player_height > enemy_y:
            game_over = True
            timer_stopped = True

    # Calculate alive time
    if not timer_stopped:
        elapsed_time = int(time.time() - start_time)

    # Draw the game objects
    win.blit(background_img, (0, 0))  # Draw the background
    win.blit(player_img, (player_x, player_y))
    for enemy in enemies:
        enemy_x, enemy_y, _ = enemy
        win.blit(enemy_img, (enemy_x, enemy_y))

    # Display the alive time
    time_text = font.render("Time: " + str(elapsed_time) + " seconds", True, (255, 0, 0))
    win.blit(time_text, (10, 10))

    # Display game over message and retry prompt
    if game_over:
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        retry_text = font.render("Press SPACE to Retry", True, (255, 0, 0))
        win.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
        win.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + retry_text.get_height() // 2))

    pygame.display.update()