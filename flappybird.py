import pygame
import random

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Set up clock
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Load bird image
bird_image = pygame.image.load("bird.png")
bird_image = pygame.transform.scale(bird_image, (40, 30))

# Bird settings
BIRD_X = 50
BIRD_Y = 300
GRAVITY = 0.5
FLAP = -8

# Pipe settings
PIPE_WIDTH = 70
PIPE_GAP = 150
pipe_speed = -4
pipe_list = []

# Fonts
font = pygame.font.SysFont("Arial", 32)

# Function to generate pipes
def create_pipe():
    pipe_height = random.randint(150, 400)
    pipe_top = pygame.Rect(WIDTH, 0, PIPE_WIDTH, pipe_height)
    pipe_bottom = pygame.Rect(WIDTH, pipe_height + PIPE_GAP, PIPE_WIDTH, HEIGHT - pipe_height - PIPE_GAP)
    return pipe_top, pipe_bottom

# Function to move pipes
def move_pipes(pipes):
    for pipe in pipes:
        pipe.x += pipe_speed
    return pipes

# Function to check for collisions
def check_collision(bird_rect, pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True
    if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT:
        return True
    return False

# Function to display the score
def display_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Game Over screen
def game_over_screen(score):
    screen.fill(BLUE)
    game_over_text = font.render("Game Over!", True, RED)
    replay_text = font.render("Press R to Replay", True, WHITE)
    exit_text = font.render("Press Q to Quit", True, WHITE)
    score_text = font.render(f"Your Score: {score}", True, WHITE)

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    screen.blit(replay_text, (WIDTH // 2 - replay_text.get_width() // 2, HEIGHT // 2 + 50))
    screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 100))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False  # Replay the game
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()  # Quit the game

# Main game loop
def main():
    global pipe_list

    # Reset bird settings
    bird_rect = pygame.Rect(BIRD_X, BIRD_Y, 40, 30)
    bird_speed = 0  # Reset bird's speed when the game starts or restarts

    pipe_list = []
    score = 0
    passed_pipe = False  # Tracks whether the bird has passed a pipe

    # Add initial pipes
    pipe_timer = 0
    pipe_interval = 1500  # milliseconds

    # Game loop
    running = True
    game_over = False
    while running:
        if not game_over:
            screen.fill(BLUE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird_speed = FLAP

            # Bird movement
            bird_speed += GRAVITY
            bird_rect.y += bird_speed

            # Pipes movement
            if pygame.time.get_ticks() - pipe_timer > pipe_interval:
                pipe_timer = pygame.time.get_ticks()
                pipe_list.extend(create_pipe())

            pipe_list = move_pipes(pipe_list)
            pipe_list = [pipe for pipe in pipe_list if pipe.x > -PIPE_WIDTH]

            # Score logic: increase score only when the bird passes the gap between pipes
            if pipe_list and pipe_list[0].x + PIPE_WIDTH < bird_rect.x and not passed_pipe:
                score += 1
                passed_pipe = True  # Prevent multiple score increments for the same pipe set

            # Reset passed_pipe when the bird moves past the next set of pipes
            if pipe_list and pipe_list[0].x + PIPE_WIDTH >= bird_rect.x:
                passed_pipe = False

            # Check collision
            if check_collision(bird_rect, pipe_list):
                game_over = True

            # Draw pipes
            for pipe in pipe_list:
                pygame.draw.rect(screen, GREEN, pipe)

            # Draw bird
            screen.blit(bird_image, bird_rect)

            # Display score
            display_score(score)

            # Update display
            pygame.display.flip()

            # Cap the frame rate
            clock.tick(FPS)
        else:
            game_over_screen(score)  # Show the Game Over screen
            main()  # Restart the game

    pygame.quit()

if __name__ == "__main__":
    main()
