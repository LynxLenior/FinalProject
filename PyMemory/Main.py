import pygame
import random
import time
import os
from pathlib import Path

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Matching Game")
font = pygame.font.Font(None, 74)
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)
BLUE = (0, 0, 255)

# Card settings
CARD_SIZE = 100
MARGIN = 20

pause = False

# Pause Screen
def pause_screen():
    surface.fill((0, 0, 0, 0))  # Clear transparent surface
    pygame.draw.rect(surface, (128, 128, 128, 150), [0, 0, WIDTH, HEIGHT])  # semi-transparent overlay

    font_title = pygame.font.Font(None, 80)
    font_button = pygame.font.Font(None, 50)

    # Button settings
    button_width, button_height = 200, 60
    button_color = 'white'
    text_color = BLACK

    # Center positions
    restart_x = (WIDTH - button_width) // 2
    restart_y = HEIGHT // 2 - 40
    menu_x = (WIDTH - button_width) // 2
    menu_y = restart_y + button_height + 20

    # Draw buttons
    restart = pygame.draw.rect(surface, button_color, (restart_x, restart_y, button_width, button_height))
    menu = pygame.draw.rect(surface, button_color, (menu_x, menu_y, button_width, button_height))

    # Draw text
    paused_text = font_title.render("PAUSED", True, text_color)
    surface.blit(paused_text, ((WIDTH - paused_text.get_width()) // 2, 150))

    restart_text = font_button.render("Restart", True, text_color)
    surface.blit(restart_text, ((WIDTH - restart_text.get_width()) // 2, restart_y + 10))

    menu_text = font_button.render("Main Menu", True, text_color)
    surface.blit(menu_text, ((WIDTH - menu_text.get_width()) // 2, menu_y + 10))

    # Draw to main screen
    screen.blit(surface, (0, 0))

    return restart, menu

# After pygame.init(), add:
# Load images
def load_images():
    image_folder = Path(__file__).parent / 'img'
    images = []
    for image_file in os.listdir(image_folder):
        if image_file.endswith(('.png', '.jpg', '.jpeg')):
            image_path = image_folder / image_file
            img = pygame.image.load(str(image_path))
            img = pygame.transform.scale(img, (CARD_SIZE - 20, CARD_SIZE - 20))  # Scale image to fit card
            images.append(img)
    return images  # Create pairs

# Create card positions
def create_card_positions():
    positions = []
    for i in range(4):
        for j in range(4):
            x = MARGIN + j * (CARD_SIZE + MARGIN)
            y = MARGIN + i * (CARD_SIZE + MARGIN)
            positions.append((x, y))
    return positions

positions = create_card_positions()

# Generate pairs
def generate_pairs():
    images = load_images()
    random.shuffle(images)
    return images[:8] * 2# Select only 4 pairs

pairs = generate_pairs()

# Card class
class Card:
    def __init__(self, image, position):
        self.image = image
        self.position = position
        self.rect = pygame.Rect(position[0], position[1], CARD_SIZE, CARD_SIZE)
        self.revealed = False
        self.matched = False

    def draw(self, screen):
        if self.revealed or self.matched:
            pygame.draw.rect(screen, WHITE, self.rect)
            screen.blit(self.image, (self.position[0] + 10, self.position[1] + 10))
        else:
            pygame.draw.rect(screen, GREEN, self.rect)

# Create card objects
cards = [Card(pairs[i], positions[i]) for i in range(16)]

# Game variables
first_card = None
second_card = None
matches = 0
attempts = 0
running = True
clock = pygame.time.Clock()

# Main menu
def main_menu():
    inMenu = True

    # Define button
    #Centering the buttons using amazing math equations(Just incase the size of the window changes again)
    play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 60)
    quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 60)

    font = pygame.font.Font(None, 50)

    while inMenu:
        screen.fill(GRAY) # Background color

        #If set to True it will be more smoother, if False it will be more blocky according to what I read
        title = font.render("Memory Game", True, WHITE)
        play_text = font.render("Play", True, WHITE)
        quit_text = font.render("Quit", True, WHITE)

        # Draw title
        screen.blit(title, (140, 150))

        # Draw buttons
        pygame.draw.rect(screen, BLUE, play_button)
        pygame.draw.rect(screen, RED, quit_button)

        #Center the text on buttons thing
        screen.blit(play_text, (play_button.x + 60, play_button.y + 10))
        screen.blit(quit_text, (quit_button.x + 60, quit_button.y + 10))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    inMenu = False  # Start the game
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()  # Quit if quit clicked

        pygame.display.update()
main_menu()

# Main game loop
while running:
    screen.fill(BLACK)
    restart_rect, menu_rect = None, None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not pause:
            if not pause:
                if first_card is None or (first_card and second_card is None):
                    for card in cards:
                        if card.rect.collidepoint(event.pos) and not card.revealed and not card.matched:
                            card.revealed = True
                            if first_card is None:
                                first_card = card
                            elif second_card is None:
                                second_card = card
                                attempts += 1
            else:
                if restart_rect and restart_rect.collidepoint(event.pos):
                    # Restart game
                    pairs = generate_pairs()
                    cards = [Card(pairs[i], positions[i]) for i in range(16)]
                    matches = 0
                    attempts = 0
                    pause = False

                if menu_rect and menu_rect.collidepoint(event.pos):
                    # Go back to main menu
                    main_menu()
                    pause = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause = not pause

    # Check for match
    if first_card and second_card:
        # Redraw cards before delay so both are visible
        for card in cards:
            card.draw(screen)
        pygame.display.flip()

        pygame.time.wait(500)
        if first_card.image == second_card.image:
            first_card.matched = True
            second_card.matched = True
            matches += 1
        else:
            first_card.revealed = False
            second_card.revealed = False
        first_card = None
        second_card = None

    # Draw cards
    for card in cards:
        card.draw(screen)

    # Display match count
    font = pygame.font.Font(None, 36)
    text = font.render(f"Matches: {matches}  Attempts: {attempts}", True, WHITE)
    screen.blit(text, (10, 500))

    # Check for win
    if matches == 8:
        font = pygame.font.Font(None, 74)
        win_text = font.render("You Win!", True, RED)
        screen.blit(win_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))

    if pause:
        pause_screen()

    pygame.display.update()
    clock.tick(30)

pygame.quit()