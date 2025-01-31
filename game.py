import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Platformer")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Load assets
player_image = pygame.image.load("player.png")  # Replace with your player image
enemy_image = pygame.image.load("enemy.png")  # Replace with your enemy image
coin_image = pygame.image.load("coin.png")  # Replace with your coin image
powerup_image = pygame.image.load("powerup.png")  # Replace with your power-up image
background_image = pygame.image.load("background.jpg")  # Replace with your background image

# Resize images to match the size variables
player_size = 50
enemy_size = 40
coin_size = 30
powerup_size = 30

player_image = pygame.transform.scale(player_image, (player_size, player_size))
enemy_image = pygame.transform.scale(enemy_image, (enemy_size, enemy_size))
coin_image = pygame.transform.scale(coin_image, (coin_size, coin_size))
powerup_image = pygame.transform.scale(powerup_image, (powerup_size, powerup_size))

# Resize background image to fit the screen
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Sound effects
pygame.mixer.init()
jump_sound = pygame.mixer.Sound("jump.wav")  # Replace with your jump sound
coin_sound = pygame.mixer.Sound("coin.wav")  # Replace with your coin sound
hit_sound = pygame.mixer.Sound("hit.wav")  # Replace with your hit sound

# Player settings
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 10
player_speed = 5
player_jump = False
player_jump_height = 15
player_jump_count = player_jump_height
player_health = 100

# Enemy settings
enemy_x = random.randint(0, WIDTH - enemy_size)
enemy_y = 0
enemy_speed = 3

# Coin settings
coin_x = random.randint(0, WIDTH - coin_size)
coin_y = 0
coin_speed = 4
coin_collected = False

# Power-up settings
powerup_x = random.randint(0, WIDTH - powerup_size)
powerup_y = 0
powerup_speed = 4
powerup_active = False
powerup_timer = 0

# Score and level
score = 0
level = 1
font = pygame.font.SysFont("Arial", 30)

# Clock
clock = pygame.time.Clock()

# Game states
START = 0
PLAYING = 1
GAME_OVER = 2
game_state = START

# Functions
def draw_text(text, x, y, color=WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def reset_game():
    global player_x, player_y, player_health, score, level, enemy_speed, coin_speed, powerup_active, powerup_timer
    player_x = WIDTH // 2 - player_size // 2
    player_y = HEIGHT - player_size - 10
    player_health = 100
    score = 0
    level = 1
    enemy_speed = 3
    coin_speed = 4
    powerup_active = False
    powerup_timer = 0

# Main game loop
running = True
while running:
    screen.fill(BLACK)
    screen.blit(background_image, (0, 0))  # Draw the resized background

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_state == START:
                if event.key == pygame.K_RETURN:
                    game_state = PLAYING
            elif game_state == GAME_OVER:
                if event.key == pygame.K_RETURN:
                    reset_game()
                    game_state = PLAYING

    if game_state == START:
        draw_text("Press ENTER to Start", WIDTH // 2 - 100, HEIGHT // 2)
    elif game_state == PLAYING:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
            player_x += player_speed
        if keys[pygame.K_SPACE] and not player_jump:
            player_jump = True
            jump_sound.play()

        # Player jump
        if player_jump:
            if player_jump_count >= -player_jump_height:
                player_y -= (player_jump_count * abs(player_jump_count)) * 0.3
                player_jump_count -= 1
            else:
                player_jump = False
                player_jump_count = player_jump_height

        # Enemy movement
        enemy_y += enemy_speed
        if enemy_y > HEIGHT:
            enemy_x = random.randint(0, WIDTH - enemy_size)
            enemy_y = 0

        # Coin movement
        if not coin_collected:
            coin_y += coin_speed
            if coin_y > HEIGHT:
                coin_x = random.randint(0, WIDTH - coin_size)
                coin_y = 0

        # Power-up movement
        if not powerup_active:
            powerup_y += powerup_speed
            if powerup_y > HEIGHT:
                powerup_x = random.randint(0, WIDTH - powerup_size)
                powerup_y = 0

        # Collision detection
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size)
        coin_rect = pygame.Rect(coin_x, coin_y, coin_size, coin_size)
        powerup_rect = pygame.Rect(powerup_x, powerup_y, powerup_size, powerup_size)

        if player_rect.colliderect(enemy_rect):
            player_health -= 20
            hit_sound.play()
            enemy_x = random.randint(0, WIDTH - enemy_size)
            enemy_y = 0
            if player_health <= 0:
                game_state = GAME_OVER

        if player_rect.colliderect(coin_rect):
            coin_collected = True
            score += 10
            coin_sound.play()
            coin_x = random.randint(0, WIDTH - coin_size)
            coin_y = 0
            coin_collected = False

        if player_rect.colliderect(powerup_rect):
            powerup_active = True
            powerup_timer = pygame.time.get_ticks()
            player_health += 20
            if player_health > 100:
                player_health = 100
            powerup_x = random.randint(0, WIDTH - powerup_size)
            powerup_y = 0

        # Power-up timer
        if powerup_active:
            if pygame.time.get_ticks() - powerup_timer > 5000:  # 5 seconds
                powerup_active = False

        # Draw player
        screen.blit(player_image, (player_x, player_y))

        # Draw enemy
        screen.blit(enemy_image, (enemy_x, enemy_y))

        # Draw coin
        screen.blit(coin_image, (coin_x, coin_y))

        # Draw power-up
        if not powerup_active:
            screen.blit(powerup_image, (powerup_x, powerup_y))

        # Draw score and health
        draw_text(f"Score: {score}", 10, 10)
        draw_text(f"Health: {player_health}", 10, 50)
        draw_text(f"Level: {level}", 10, 90)

        # Level progression
        if score >= level * 50:
            level += 1
            enemy_speed += 1
            coin_speed += 1

    elif game_state == GAME_OVER:
        draw_text("Game Over! Press ENTER to Restart", WIDTH // 2 - 150, HEIGHT // 2)
        draw_text(f"Final Score: {score}", WIDTH // 2 - 80, HEIGHT // 2 + 40)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()