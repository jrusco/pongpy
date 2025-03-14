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
PADDLE_SPEED = 6  # Increased from 5 to 6, making player slightly faster than ball
AI_PADDLE_SPEED = 3
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

    def move(self, dy):
        self.rect.y += dy
        # Keep paddle within screen bounds
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > HEIGHT - PADDLE_HEIGHT:
            self.rect.y = HEIGHT - PADDLE_HEIGHT

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2 - BALL_SIZE//2, 
                              HEIGHT//2 - BALL_SIZE//2, 
                              BALL_SIZE, BALL_SIZE)
        self.dx = BALL_SPEED * random.choice((1, -1))
        self.dy = BALL_SPEED * random.choice((1, -1))

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

def ai_movement(ball, paddle):
    # Simple AI: move towards ball's y position with slower speed
    if ball.rect.centery < paddle.rect.centery and paddle.rect.y > 0:
        paddle.move(-AI_PADDLE_SPEED)
    if ball.rect.centery > paddle.rect.centery and paddle.rect.y < HEIGHT - PADDLE_HEIGHT:
        paddle.move(AI_PADDLE_SPEED)

def start_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    title = font.render("Pong", True, WHITE)
    font = pygame.font.Font(None, 36)
    instruction = font.render("Press F to start/stop playing", True, WHITE)

    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
    screen.blit(instruction, (WIDTH//2 - instruction.get_width()//2, HEIGHT//2))
    pygame.display.flip()

def end_screen(player_score, ai_score, play_time):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 50)
    player_text = font.render(f"Player Score: {player_score}", True, WHITE)
    ai_text = font.render(f"AI Score: {ai_score}", True, WHITE)
    time_text = font.render(f"Time Played: {play_time:.1f} seconds", True, WHITE)

    screen.blit(player_text, (WIDTH//2 - player_text.get_width()//2, HEIGHT//3))
    screen.blit(ai_text, (WIDTH//2 - ai_text.get_width()//2, HEIGHT//2))
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
    player = Paddle(50, HEIGHT//2 - PADDLE_HEIGHT//2)
    ai = Paddle(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2)
    ball = Ball()

    # Scores
    player_score = 0
    ai_score = 0

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
                    end_screen(player_score, ai_score, play_time)

        if game_started and not game_over:
            # Player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                player.move(-PADDLE_SPEED)
            if keys[pygame.K_DOWN]:
                player.move(PADDLE_SPEED)

            # AI movement
            ai_movement(ball, ai)

            # Ball movement
            ball.move()

            # Ball collision with top and bottom
            if ball.rect.top <= 0 or ball.rect.bottom >= HEIGHT:
                ball.dy = -ball.dy

            # Ball collision with paddles
            if ball.rect.colliderect(player.rect):
                ball.dx = abs(ball.dx)
            if ball.rect.colliderect(ai.rect):
                ball.dx = -abs(ball.dx)

            # Scoring
            if ball.rect.left <= 0:
                ai_score += 1
                ball = Ball()
            if ball.rect.right >= WIDTH:
                player_score += 1
                ball = Ball()

            # Draw everything
            screen.fill(BLACK)
            # Draw center line
            pygame.draw.line(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 2)
            # Draw bottom limit line
            pygame.draw.line(screen, WHITE, (0, HEIGHT - 10), (WIDTH, HEIGHT - 10), 2)

            # Draw scores
            font = pygame.font.Font(None, 36)
            player_text = font.render(str(player_score), True, WHITE)
            ai_text = font.render(str(ai_score), True, WHITE)
            screen.blit(player_text, (WIDTH//4, 20))
            screen.blit(ai_text, (3*WIDTH//4, 20))

            # Draw game objects
            player.draw()
            ai.draw()
            ball.draw()

            pygame.display.flip()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()