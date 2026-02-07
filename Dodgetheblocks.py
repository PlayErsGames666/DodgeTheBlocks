import pygame
import random
import sys

# Settings
WIDTH, HEIGHT = 600, 800
PLAYER_SIZE = 50
BLOCK_SIZE = 50
PLAYER_SPEED = 7
BLOCK_SPEED = 5
SPAWN_TIME = 900  # мс

# Inicialisation
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Blocks")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 32)

# User
player = pygame.Rect(WIDTH // 2 - PLAYER_SIZE // 2,
                     HEIGHT - PLAYER_SIZE - 20,
                     PLAYER_SIZE,
                     PLAYER_SIZE)

# Enemy
blocks = []
SPAWN_BLOCK = pygame.USEREVENT
pygame.time.set_timer(SPAWN_BLOCK, SPAWN_TIME)

score = 0
running = True

# Main Cycle
while running:
    clock.tick(60)
    screen.fill((20, 20, 30))

    # Event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SPAWN_BLOCK:
            x = random.randint(0, WIDTH - BLOCK_SIZE)
            block = pygame.Rect(x, -BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            blocks.append(block)

    # Control
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player.x -= PLAYER_SPEED
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player.x += PLAYER_SPEED

    player.x = max(0, min(WIDTH - PLAYER_SIZE, player.x))

    # Block Movement
    for block in blocks[:]:
        block.y += BLOCK_SPEED

        if block.y > HEIGHT:
            blocks.remove(block)
            score += 1
            if score % 5 == 0:
                BLOCK_SPEED += 0.5

        if block.colliderect(player):
            running = False

    # Rendering
    pygame.draw.rect(screen, (0, 200, 255), player)

    for block in blocks:
        pygame.draw.rect(screen, (255, 60, 60), block)

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))

    pygame.display.flip()

# GAME OVER
screen.fill((0, 0, 0))
game_over = font.render("GAME OVER", True, (255, 80, 80))
final_score = font.render(f"Final Score: {score}", True, (255, 255, 255))

screen.blit(game_over, (WIDTH // 2 - game_over.get_width() // 2, HEIGHT // 2 - 40))
screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, HEIGHT // 2 + 10))
pygame.display.flip()

pygame.time.wait(3000)
pygame.quit()
