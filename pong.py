import pygame
import random
import time

pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
SPRITE_WIDTH = 100  
SPRITE_HEIGHT = 180  
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
    def __init__(self, from_right=None):
        self.rect = pygame.Rect(0, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
        
        if from_right is None:
            # Initial center position and random direction
            self.rect.centerx = WIDTH//2
            self.dx = BALL_SPEED * random.choice((1, -1))
        else:
            # Position based on scoring player
            self.rect.x = WIDTH - 50 - BALL_SIZE if from_right else 50
            self.dx = -BALL_SPEED if from_right else BALL_SPEED
            
        self.dy = BALL_SPEED * random.choice((1, -1))
        self.color = WHITE  

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
    # Wait briefly to show the end screen before exiting
    pygame.time.wait(2000)
    pygame.quit()
    exit()

def handle_game_state(event, game_started, game_over, start_time, frog_score, princess_score):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
        if not game_started:
            return True, False, time.time()
        elif game_started and not game_over:
            play_time = time.time() - start_time
            end_screen(frog_score, princess_score, play_time)
    return game_started, game_over, start_time

def handle_player_movement(frog, princess):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]: frog.move(-PLAYER_SPEED)
    if keys[pygame.K_DOWN]: frog.move(PLAYER_SPEED)
    if keys[pygame.K_w]: princess.move(-PLAYER_SPEED)
    if keys[pygame.K_s]: princess.move(PLAYER_SPEED)

def update_ball_position(ball, frog, princess):
    ball.move()
    if ball.rect.top <= 0 or ball.rect.bottom >= HEIGHT:
        ball.dy = -ball.dy

    for player in (frog, princess):
        if ball.rect.colliderect(player.rect):
            ball.dx = abs(ball.dx) if player == frog else -abs(ball.dx)

def check_scoring(ball, frog_score, princess_score):
    if ball.rect.left <= 0:
        show_score_message()
        return frog_score, princess_score + 1, Ball(from_right=False)  # Ball starts from princess side
    if ball.rect.right >= WIDTH:
        show_score_message()
        return frog_score + 1, princess_score, Ball(from_right=True)   # Ball starts from frog side
    return frog_score, princess_score, ball

def draw_game_state(screen, frog, princess, ball, frog_score, princess_score):
    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT), 2)
    pygame.draw.line(screen, WHITE, (0, HEIGHT - 10), (WIDTH, HEIGHT - 10), 2)

    font = pygame.font.Font(None, 36)
    for score, pos in [(frog_score, WIDTH//4), (princess_score, 3*WIDTH//4)]:
        score_text = font.render(str(score), True, WHITE)
        screen.blit(score_text, (pos, 20))

    frog.draw()
    princess.draw()
    ball.draw()
    pygame.display.flip()

def show_score_message():
    font = pygame.font.Font(None, 74)
    score_text = font.render("SCORE!", True, WHITE)
    text_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(score_text, text_rect)
    pygame.display.flip()
    pygame.time.wait(500)  

def main():
    game_started = False
    game_over = False
    start_screen()

    frog = Player(50, HEIGHT//2 - SPRITE_HEIGHT//2, "frog.png")
    princess = Player(WIDTH - 50 - SPRITE_WIDTH, HEIGHT//2 - SPRITE_HEIGHT//2, "princess.png")
    ball = Ball()
    frog_score = princess_score = 0
    start_time = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game_started, game_over, start_time = handle_game_state(
                event, game_started, game_over, start_time, frog_score, princess_score)

        if game_started and not game_over:
            handle_player_movement(frog, princess)
            update_ball_position(ball, frog, princess)
            frog_score, princess_score, ball = check_scoring(ball, frog_score, princess_score)
            draw_game_state(screen, frog, princess, ball, frog_score, princess_score)

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
