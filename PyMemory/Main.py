import pygame
import random
import time
import os
from pathlib import Path

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Set up display
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyMemory - Do you KNOW what it takes?")
font = pygame.font.Font(None, 74)
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)
BLUE = (55, 111, 159)
YELLOW = (255, 209, 65)

# Card settings
CARD_SIZE = 100
MARGIN = 20

# Game variables
first_card = None
second_card = None
matches = 0
attempts = 0
running = True
clock = pygame.time.Clock()

# After pygame.init(), add:

#Sound Folder Path
Sound_Folder = Path(__file__).parent / "SoundEfx"
#Sounds
Click = pygame.mixer.Sound(Sound_Folder / "ButtonClicked.wav")
Match = pygame.mixer.Sound(Sound_Folder / "Match.wav")
Exit = pygame.mixer.Sound(Sound_Folder / "Exit.wav")
Play = pygame.mixer.Sound(Sound_Folder / "Play.wav")
Win = pygame.mixer.Sound(Sound_Folder / "Win.wav")

BackGround = Path(__file__).parent / 'Bg'

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
def create_card_positions(size):
    positions = []
    for i in range(size):
        for j in range(size):
            if size == 5 and i == 2 and j == 2:
                continue  #Skipping middle boy
            x = MARGIN + j * (CARD_SIZE + MARGIN)
            y = MARGIN + i * (CARD_SIZE + MARGIN)
            positions.append((x, y))
    return positions

# Generate pairs
def generate_pairs(grid_size):
    if grid_size == 4:
        symbols = list(range(8)) * 2  # 16 cards total
    else:  # grid_size == 5
        symbols = list(range(12)) * 2  # 24 cards (one space will be skipped)
    random.shuffle(symbols)
    return symbols

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
            pygame.draw.rect(screen, GRAY, self.rect)

# Main menu
def main_menu():
    inMenu = True
    
    # Define button
    #Centering the buttons using amazing math equations(Just incase the size of the window changes again)
    play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 60)
    quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 60)

    font = pygame.font.Font(None, 50)

    while inMenu:
        #If set to True it will be more smoother, if False it will be more blocky according to what I read
        play_text = font.render("", True, WHITE)
        quit_text = font.render("", True, WHITE)

        # Background
        Tempbg = pygame.image.load(Path(BackGround / 'Menu.png')).convert()
        Tempbg = pygame.transform.scale(Tempbg, (WIDTH, HEIGHT))
        screen.blit(Tempbg, (0, 0))

        #Center the text on buttons thing
        screen.blit(play_text, (play_button.x + 60, play_button.y + 10))
        screen.blit(quit_text, (quit_button.x + 60, quit_button.y + 10))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    Click.play()
                    inMenu = False  # Start the game
                elif quit_button.collidepoint(event.pos):
                    Exit.play()
                    Exit.set_volume(0.2)
                    pygame.time.wait(3000)
                    pygame.quit()  # Quit if quit clicked
        pygame.display.update()

# Choosing grid size
def choose_grid_size():
    choosing = True
    font = pygame.font.Font(None, 50)
    four_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 70, 200, 60)
    five_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 30, 200, 60)

    while choosing:
        Tempbg = pygame.image.load(Path(BackGround / 'ChooseGrid.png')).convert()
        Tempbg = pygame.transform.scale(Tempbg, (WIDTH, HEIGHT))
        screen.blit(Tempbg, (0, 0))
        four_text = font.render("", True, WHITE)
        five_text = font.render("", True, WHITE)
        screen.blit(four_text, (four_button.x + 60, four_button.y + 10))
        screen.blit(five_text, (five_button.x + 60, five_button.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if four_button.collidepoint(event.pos):
                    Play.play()
                    Play.set_volume(0.1)
                    return 4
                elif five_button.collidepoint(event.pos):
                    Play.play()
                    Play.set_volume(0.1)
                    return 5

        pygame.display.update()
main_menu()

grid_size = choose_grid_size()
# Create cards and positions dynamically
positions = create_card_positions(grid_size)
# If 5x5, there are 25 spots but one skipped (center)
total_cards = len(positions)

# Adjust window size if 5x5 is selected
if grid_size == 5:
    WIDTH, HEIGHT = 615, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Generate correct number of pairs
# Load and prepare image cards
images = load_images()

# Limit number of images based on grid size
if grid_size == 4:
    selected_images = images[:8]
else:
    selected_images = images[:12]

# Duplicate and shuffle for pairs
pairs = selected_images * 2
random.shuffle(pairs)

# Create Card objects using images, not ints
cards = [Card(pairs[i], positions[i]) for i in range(total_cards)]


# Restart game variables
def restart_game():
    global first_card, second_card, matches, attempts, cards, positions, pairs, grid_size, WIDTH, HEIGHT, screen

    grid_size = choose_grid_size() # Gets and store new grid size

    # Change the screen size depending on grid size
    if grid_size == 5:
        WIDTH, HEIGHT = 615, 700
    else:
        WIDTH, HEIGHT = 500, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    #resets the board
    first_card = None
    second_card = None
    matches = 0
    attempts = 0

    images = load_images()
    selected_images = images[:8] if grid_size == 4 else images[:12]
    pairs = selected_images * 2
    random.shuffle(pairs)

    positions = create_card_positions(grid_size)
    cards = [Card(pairs[i], positions[i]) for i in range(len(positions))]


# Pause Screen
def pause_screen(pause=False):
    font_title = pygame.font.Font(None, 80)
    font_button = pygame.font.Font(None, 50)

    # Button settings
    button_width, button_height = 200, 60
    button_color = 'white'
    text_color = BLACK
    win_color = GREEN

    # Center positions
    restart_x = (WIDTH - button_width) // 2
    restart_y = HEIGHT // 2 - 40
    menu_x = (WIDTH - button_width) // 2
    menu_y = restart_y + button_height + 20

    while pause:
        screen.fill((0, 0, 0, 0))  # Clear transparent surface
        pygame.draw.rect(screen, (128, 128, 128, 150), [0, 0, WIDTH, HEIGHT])  # semi-transparent overlay

        # Draw buttons
        restart = pygame.draw.rect(screen, button_color, (restart_x, restart_y, button_width, button_height))
        menu = pygame.draw.rect(screen, button_color, (menu_x, menu_y, button_width, button_height))

        # Draw text
        paused_text = font_title.render("PAUSED", True, win_color)
        screen.blit(paused_text, ((WIDTH - paused_text.get_width()) // 2, 150))
    

        restart_text = font_button.render("Restart", True, text_color)
        screen.blit(restart_text, ((WIDTH - restart_text.get_width()) // 2, restart_y + 10))
        

        menu_text = font_button.render("Main Menu", True, text_color)
        screen.blit(menu_text, ((WIDTH - menu_text.get_width()) // 2, menu_y + 10))
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = False
                    continue
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # --- Handle Pause Buttons ---
                if restart and restart.collidepoint(event.pos):
                    # Go back to choose grid size
                    Click.play()
                    restart_game()
                    pause = False
                    continue
                elif menu and menu.collidepoint(event.pos):
                    # Go back to main menu
                    Click.play()
                    main_menu()
                    restart_game()
                    pause = False
                    continue
        pygame.display.update()
    return pause


def win_screen(win=False):
    global first_card, second_card, matches, attempts, cards, positions, pairs, grid_size, WIDTH, HEIGHT, screen
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
    Win.play()
    Win.set_volume(0.1)

    while win:
        screen.fill((0, 0, 0, 0))  # Clear transparent surface
        pygame.draw.rect(screen, (128, 128, 128, 150), [0, 0, WIDTH, HEIGHT])  # semi-transparent overlay
        
        # Draw buttons
        restart = pygame.draw.rect(screen, button_color, (restart_x, restart_y, button_width, button_height))
        menu = pygame.draw.rect(screen, button_color, (menu_x, menu_y, button_width, button_height))

        # Draw text
        paused_text = font_title.render("YOU WIN!", True, text_color)
        screen.blit(paused_text, ((WIDTH - paused_text.get_width()) // 2, 150))
        restart_text = font_button.render("Restart", True, text_color)
        screen.blit(restart_text, ((WIDTH - restart_text.get_width()) // 2, restart_y + 10))
        menu_text = font_button.render("Main Menu", True, text_color)
        screen.blit(menu_text, ((WIDTH - menu_text.get_width()) // 2, menu_y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Click.play()
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # win screen buttons
                if restart and restart.collidepoint(event.pos):
                    # Go back to choose grid size
                    Click.play()
                    restart_game()
                    win = False
                    continue
                elif menu and menu.collidepoint(event.pos):
                    # Go back to main menu
                    Click.play()
                    main_menu()
                    restart_game()
                    win = False
                    continue
        pygame.display.update()

# Main game loop
while running:
    # BackGround
    if grid_size == 4:
        Tempbg = pygame.image.load(Path(BackGround / 'Game.png')).convert()
        Tempbg = pygame.transform.scale(Tempbg, (WIDTH, HEIGHT))
        screen.blit(Tempbg, (0, 0))
    else:
        Tempbg = pygame.image.load(Path(BackGround / 'FiveBG.png')).convert()
        Tempbg = pygame.transform.scale(Tempbg, (WIDTH, HEIGHT))
        screen.blit(Tempbg, (0, 0))
    pause = pause_screen()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not pause:
                # --- Handle Card Clicks ---
                if first_card is None or second_card is None:
                    for card in cards:
                        if card.rect.collidepoint(event.pos) and not card.revealed and not card.matched:
                            card.revealed = True
                            Click.play()
                            if first_card is None:
                                first_card = card
                            elif second_card is None:
                                second_card = card
                                attempts += 1
            else:
                pause = pause_screen(pause)
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause_screen(pause=True)

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
            Match.play()
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
    text = font.render(f"Matches: {matches}  Attempts: {attempts}", True, YELLOW)
    if grid_size == 4:
        text_y = (MARGIN + 4 * (CARD_SIZE + MARGIN)) + 10  # just below 4x4 grid
    else:
        text_y = (MARGIN + 5 * (CARD_SIZE + MARGIN)) + 10 # just below 5x5 grid
    screen.blit(text, (10, text_y))

    # Check for win
    if grid_size == 4 and matches == 1:
        win_screen(win=True)
    elif grid_size == 5 and matches == 1:
        win_screen(win=True)

    pygame.display.update()
    clock.tick(30)

pygame.quit()