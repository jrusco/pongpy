import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
SPRITE_WIDTH = 50  # Width of the sprite images
SPRITE_HEIGHT = 90  # Height of the sprite images
BALL_SIZE = 15
BALL_SPEED = 4
PLAYER_SPEED = 6  # Speed for both players
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Clock for controlling game framerate
clock = pygame.time.Clock()

class Player:
    def __init__(self, x, y, image_path):
        # Load and convert the image with alpha channel
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (SPRITE_WIDTH, SPRITE_HEIGHT))
        # Set the colorkey to the background color (assuming white for now)
        self.image.set_colorkey((255, 255, 255))  # White background
        self.rect = self.image.get_rect(topleft=(x, y))
        self.color = WHITE  # Used for ball color change logic

    def move(self, dy):
        self.rect.y += dy
        # Keep player within screen bounds
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > HEIGHT - SPRITE_HEIGHT:
            self.rect.y = HEIGHT - SPRITE_HEIGHT

    def draw(self):
        screen.blit(self.image, self.rect)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2 - BALL_SIZE//2, 
                              HEIGHT//2 - BALL_SIZE//2, 
                              BALL_SIZE, BALL_SIZE)
        self.dx = BALL_SPEED * random.choice((1, -1))
        self.dy = BALL_SPEED * random.choice((1, -1))
        self.color = WHITE  # Initial color

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

def start_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    title = font.render("Pong", True, WHITE)
    font = pygame.font.Font(None, 36)
    instruction = font.render("Press F to start/stop playing", True, WHITE)
    controls = font.render("Frog: UP/DOWN | Princess: W/S", True, WHITE)

    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
    screen.blit(instruction, (WIDTH//2 - instruction.get_width()//2, HEIGHT//2))
    screen.blit(controls, (WIDTH//2 - controls.get_width()//2, HEIGHT//2 + 40))
    pygame.display.flip()

def end_screen(frog_score, princess_score, play_time):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 50)
    frog_text = font.render(f"Frog Score: {frog_score}", True, WHITE)
    princess_text = font.render(f"Princess Score: {princess_score}", True, WHITE)
    time_text = font.render(f"Time Played: {play_time:.1f} seconds", True, WHITE)

    screen.blit(frog_text, (WIDTH//2 - frog_text.get_width()//2, HEIGHT//3))
    screen.blit(princess_text, (WIDTH//2 - princess_text.get_width()//2, HEIGHT//2))
    screen.blit(time_text, (WIDTH//2 - time_text.get_width()//2, 2*HEIGHT//3))
    pygame.display.flip()
    # Wait briefly to show the end screen (e.g., 2 seconds) before exiting
    pygame.time.wait(2000)
    # Exit the application
    pygame.quit()
    exit()

def main():
    # Initial state
    game_started = False
    game_over = False

    # Show start screen
    start_screen()

    # Game objects
    frog = Player(50, HEIGHT//2 - SPRITE_HEIGHT//2, "frog.png")  # Player 1 (left, frog)
    princess = Player(WIDTH - 50 - SPRITE_WIDTH, HEIGHT//2 - SPRITE_HEIGHT//2, "princess.png")  # Player 2 (right, princess)
    ball = Ball()

    # Scores
    frog_score = 0
    princess_score = 0

    # Time tracking
    start_time = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                if not game_started:
                    game_started = True
                    start_time = time.time()
                elif game_started and not game_over:
                    game_over = True
                    play_time = time.time() - start_time
                    end_screen(frog_score, princess_score, play_time)

        if game_started and not game_over:
            # Frog movement (left player)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                frog.move(-PLAYER_SPEED)
            if keys[pygame.K_DOWN]:
                frog.move(PLAYER_SPEED)

            # Princess movement (right player)
            if keys[pygame.K_w]:
                princess.move(-PLAYER_SPEED)
            if keys[pygame.K_s]:
                princess.move(PLAYER_SPEED)

            # Ball movement
            ball.move()

            # Ball collision with top and bottom
            if ball.rect.top <= 0 or ball.rect.bottom >= HEIGHT:
                ball.dy = -ball.dy

            # Ball collision with players and color change
            if ball.rect.colliderect(frog.rect):
                ball.dx = abs(ball.dx)  # Reverse direction
                ball.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Random color for ball
            if ball.rect.colliderect(princess.rect):
                ball.dx = -abs(ball.dx)  # Reverse direction
                ball.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Random color for ball

            # Scoring
            if ball.rect.left <= 0:
                princess_score += 1
                ball = Ball()  # Reset ball with default color
            if ball.rect.right >= WIDTH:
                frog_score += 1
                ball = Ball()  # Reset ball with default color

            # Draw everything
            screen.fill(BLACK)
            # Draw center line
            pygame.draw.line(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 2)
            # Draw bottom limit line
            pygame.draw.line(screen, WHITE, (0, HEIGHT - 10), (WIDTH, HEIGHT - 10), 2)

            # Draw scores
            font = pygame.font.Font(None, 36)
            frog_text = font.render(str(frog_score), True, WHITE)
            princess_text = font.render(str(princess_score), True, WHITE)
            screen.blit(frog_text, (WIDTH//4, 20))
            screen.blit(princess_text, (3*WIDTH//4, 20))

            # Draw game objects
            frog.draw()
            princess.draw()
            ball.draw()

            pygame.display.flip()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()