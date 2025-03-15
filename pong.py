import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
BALL_SIZE = 15
BALL_SPEED = 4
PADDLE_SPEED = 6  # Speed for both players
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Clock for controlling game framerate
clock = pygame.time.Clock()

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.color = WHITE  # Initial color

    def move(self, dy):
        self.rect.y += dy
        # Keep paddle within screen bounds
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > HEIGHT - PADDLE_HEIGHT:
            self.rect.y = HEIGHT - PADDLE_HEIGHT

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

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
    controls = font.render("Player 1: UP/DOWN | Player 2: W/S", True, WHITE)

    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
    screen.blit(instruction, (WIDTH//2 - instruction.get_width()//2, HEIGHT//2))
    screen.blit(controls, (WIDTH//2 - controls.get_width()//2, HEIGHT//2 + 40))
    pygame.display.flip()

def end_screen(player1_score, player2_score, play_time):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 50)
    player1_text = font.render(f"Player 1 Score: {player1_score}", True, WHITE)
    player2_text = font.render(f"Player 2 Score: {player2_score}", True, WHITE)
    time_text = font.render(f"Time Played: {play_time:.1f} seconds", True, WHITE)

    screen.blit(player1_text, (WIDTH//2 - player1_text.get_width()//2, HEIGHT//3))
    screen.blit(player2_text, (WIDTH//2 - player2_text.get_width()//2, HEIGHT//2))
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
    player1 = Paddle(50, HEIGHT//2 - PADDLE_HEIGHT//2)  # Player 1 (left)
    player2 = Paddle(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2)  # Player 2 (right)
    ball = Ball()

    # Scores
    player1_score = 0
    player2_score = 0

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
                    end_screen(player1_score, player2_score, play_time)

        if game_started and not game_over:
            # Player 1 movement (left paddle)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                player1.move(-PADDLE_SPEED)
            if keys[pygame.K_DOWN]:
                player1.move(PADDLE_SPEED)

            # Player 2 movement (right paddle)
            if keys[pygame.K_w]:
                player2.move(-PADDLE_SPEED)
            if keys[pygame.K_s]:
                player2.move(PADDLE_SPEED)

            # Ball movement
            ball.move()

            # Ball collision with top and bottom
            if ball.rect.top <= 0 or ball.rect.bottom >= HEIGHT:
                ball.dy = -ball.dy

            # Ball collision with paddles and color change
            if ball.rect.colliderect(player1.rect):
                ball.dx = abs(ball.dx)  # Reverse direction
                ball.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Random color for ball
                player1.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Random color for paddle
            if ball.rect.colliderect(player2.rect):
                ball.dx = -abs(ball.dx)  # Reverse direction
                ball.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Random color for ball
                player2.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Random color for paddle

            # Scoring
            if ball.rect.left <= 0:
                player2_score += 1
                ball = Ball()  # Reset ball with default color
            if ball.rect.right >= WIDTH:
                player1_score += 1
                ball = Ball()  # Reset ball with default color

            # Draw everything
            screen.fill(BLACK)
            # Draw center line
            pygame.draw.line(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 2)
            # Draw bottom limit line
            pygame.draw.line(screen, WHITE, (0, HEIGHT - 10), (WIDTH, HEIGHT - 10), 2)

            # Draw scores
            font = pygame.font.Font(None, 36)
            player1_text = font.render(str(player1_score), True, WHITE)
            player2_text = font.render(str(player2_score), True, WHITE)
            screen.blit(player1_text, (WIDTH//4, 20))
            screen.blit(player2_text, (3*WIDTH//4, 20))

            # Draw game objects
            player1.draw()
            player2.draw()
            ball.draw()

            pygame.display.flip()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()