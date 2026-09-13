import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 200, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 30))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.velocity = 0
        self.gravity = 0.5
        self.jump_strength = -12

    def update(self):
        # Apply gravity
        self.velocity += self.gravity
        self.rect.y += self.velocity

        # Keep bird on screen (top and bottom)
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def jump(self):
        self.velocity = self.jump_strength

# Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, is_top):
        super().__init__()
        self.is_top = is_top
        self.width = 60
        self.gap = 150
        
        if is_top:
            self.height = random.randint(50, 200)
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(GREEN)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = 0
        else:
            self.height = SCREEN_HEIGHT - self.gap - (random.randint(50, 200))
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill(GREEN)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = SCREEN_HEIGHT - self.height

        self.speed = 5

    def update(self):
        self.rect.x -= self.speed

# Sprite groups
all_sprites = pygame.sprite.Group()
pipes = pygame.sprite.Group()

# Create bird
bird = Bird()
all_sprites.add(bird)

# Game variables
score = 0
game_over = False
pipe_spawn_timer = 0
pipe_spawn_interval = 90  # Spawn a pipe every 90 frames

# Font for displaying score
font = pygame.font.Font(None, 36)

# Main game loop
running = True
while running:
    clock.tick(FPS)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()
            if event.key == pygame.K_r and game_over:
                # Reset game
                game_over = False
                score = 0
                bird.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                bird.velocity = 0
                pipes.empty()
                pipe_spawn_timer = 0

    if not game_over:
        # Spawn pipes
        pipe_spawn_timer += 1
        if pipe_spawn_timer >= pipe_spawn_interval:
            top_pipe = Pipe(SCREEN_WIDTH, True)
            bottom_pipe = Pipe(SCREEN_WIDTH, False)
            all_sprites.add(top_pipe, bottom_pipe)
            pipes.add(top_pipe, bottom_pipe)
            pipe_spawn_timer = 0

        # Update sprites
        all_sprites.update()

        # Check for collisions with pipes
        if pygame.sprite.spritecollideany(bird, pipes):
            game_over = True

        # Check if bird passed a pipe (scoring)
        for pipe in pipes:
            if pipe.rect.right == bird.rect.centerx and not pipe.is_top:
                score += 1

        # Remove pipes that are off screen
        for pipe in pipes:
            if pipe.rect.right < 0:
                all_sprites.remove(pipe)
                pipes.remove(pipe)

    # Draw everything
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Draw game over message
    if game_over:
        game_over_font = pygame.font.Font(None, 72)
        game_over_text = game_over_font.render("GAME OVER", True, BLACK)
        restart_font = pygame.font.Font(None, 36)
        restart_text = restart_font.render("Press R to Restart", True, BLACK)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100))
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2))

    pygame.display.flip()

pygame.quit()
sys.exit()
