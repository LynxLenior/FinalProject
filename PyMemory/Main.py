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

# Main Color variables used by the game
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (55, 111, 159)
YELLOW = (255, 209, 65)
AZURE = (0, 38, 69)

# Card size and margins
CARD_SIZE = 100
MARGIN = 20

# change window size if 5x5 grid is selected later
# Initial button positions for pause and win screens
def ChangeWindowSize(size):
    global WIDTH, HEIGHT, screen
    if size == "small":
        WIDTH, HEIGHT = 500, 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
    elif size == "large":
        WIDTH, HEIGHT = 615, 700
        screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Button settings
button_width, button_height = 200, 60

# Center positions
btn1_x = (WIDTH - button_width) // 2
btn1_y = HEIGHT // 2 - 40
btn2_x = (WIDTH - button_width) // 2
btn2_y = btn1_y + button_height + 20

# Game variables used for scoring and game state
first_card = None
second_card = None
matches = 0
attempts = 0
running = True
clock = pygame.time.Clock()

# declare Sound effects Folder Path
Sound_Folder = Path(__file__).parent / "SoundEfx"
# Sound files used by the game
Click = pygame.mixer.Sound(Sound_Folder / "ButtonClicked.wav")
Match = pygame.mixer.Sound(Sound_Folder / "Match.wav")
Exit = pygame.mixer.Sound(Sound_Folder / "Exit.wav")
Play = pygame.mixer.Sound(Sound_Folder / "Play.wav")
Win = pygame.mixer.Sound(Sound_Folder / "Win.wav")
# declare Background Folder path
BackGround = Path(__file__).parent / 'Bg'

# declare image folder path using pathlib
image_folder = Path(__file__).parent / 'img'

# Load all programming logo images using a function
def load_images():
    
    images = []

    # store images in a list that can be accessed later
    for image_file in os.listdir(image_folder):
        # only accept png and jpg image files
        if image_file.endswith(('.png', '.jpg', '.jpeg')):
            # combine image folder path and image file name to get full path
            # then load the image using pygame image load method
            image_path = image_folder / image_file
            img = pygame.image.load(str(image_path))
            # scale the image to fit on the card while maintaining aspect ratio
            img = pygame.transform.scale(img, (CARD_SIZE - 20, CARD_SIZE - 20))  # Scale image to fit card
            # append image to images list
            images.append(img)
    return images  # return the list of images

# function to create card positions dynamically based on grid size
def create_card_positions(size):
    # store the positions of the cards in a list
    positions = []
    for column in range(size):
        for row in range(size):
            if size == 5 and column == 2 and row == 2:
                continue  # skip the middle position for 5x5 grid
            
            x = MARGIN + row * (CARD_SIZE + MARGIN)
            y = MARGIN + column * (CARD_SIZE + MARGIN)
            positions.append((x, y))
    # the positions would return a list of tuples with x and y coordinates
    # the formula is MARGIN = 20 + column/row index * (CARD_SIZE = 100 + MARGIN = 20)
    # e.g., [(20, 20), (140, 20), (260, 20), ...] for the 4x4 grid it's 16 positions
    # while the 5x5 grid would return 24 positions (one skipped in the middle)
    return positions # return the list of card positions

# defines a card class that can easily be used to create card objects and modified easily
class Card:
    # Load the card back image once
    card_back = pygame.image.load(Path(BackGround / 'Card.png')).convert()
    card_back = pygame.transform.scale(card_back, (CARD_SIZE, CARD_SIZE))
    # initializes the card object with image, position, rect, revealed and matched attributes
    def __init__(self, image, position):
        self.image = image # image variable used to store the image of the card
        self.position = position # position variable used to store the x and y coordinates of the card
        self.rect = pygame.Rect(position[0], position[1], CARD_SIZE, CARD_SIZE) # rect variable used for collision detection
        self.revealed = False # revealed variable used to check if the card is face up or down
        self.matched = False # matched variable used to check if the card has been matched already

    # draw method used to draw the card on the screen, and also check if it's revealed or matched
    # if it is revealed or matched, it draws the image, otherwise it draws the back of the card
    def draw(self, screen):
        if self.revealed or self.matched:
            pygame.draw.rect(screen, WHITE, self.rect)
            screen.blit(self.image, (self.position[0] + 10, self.position[1] + 10))
        else:
            screen.blit(Card.card_back, self.position)

# Main menu function used to display the main menu and handle button clicks
def main_menu():
    # Menu loop variable
    inMenu = True
    
    # Define button
    #Centering the buttons using amazing math equations(Just incase the size of the window changes again)
    play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 60)
    quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 60)

    while inMenu:
        # Background image load
        bg_img = pygame.image.load(Path(BackGround / 'Menu.png')).convert()
        bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
        screen.blit(bg_img, (0, 0))

        # Event handling
        for event in pygame.event.get():
            # if player exits, pygame closes
            if event.type == pygame.QUIT:
                pygame.quit()
            # on mouse button press
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # check if play button is clicked then continue with choose_grid_size menu
                if play_button.collidepoint(event.pos):
                    Click.play()
                    inMenu = False  # Start the game
                # if quit, then exit pygame
                elif quit_button.collidepoint(event.pos):
                    Exit.play()
                    Exit.set_volume(0.2)
                    pygame.time.wait(560)
                    pygame.quit()  # Quit if quit clicked
        pygame.display.update()

# Choosing grid size either 4x4 or 5x5
def choose_grid_size():
    choosing = True
    four_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 70, 200, 60)
    five_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 30, 200, 60)

    while choosing:
        bg_img = pygame.image.load(Path(BackGround / 'ChooseGrid.png')).convert()
        bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
        screen.blit(bg_img, (0, 0))

        for event in pygame.event.get():
            # if player exits, the program closes
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if four_button.collidepoint(event.pos):
                    Play.play()
                    Play.set_volume(0.1)
                    # if 4x4 selected, the function returns 4
                    return 4
                elif five_button.collidepoint(event.pos):
                    Play.play()
                    Play.set_volume(0.1)
                    # if 5x5 selected, the function returns 5
                    return 5

        pygame.display.update()

# call main menu function first
main_menu()
# then run choose grid size after main menu function, and also store value inside grid_size
grid_size = choose_grid_size()
# Create cards and positions dynamically using grid_size
positions = create_card_positions(grid_size)
# stores the number of cards inside the positions list into total_cards
total_cards = len(positions)

# Adjust window size if 5x5 is selected
if grid_size == 5:
    WIDTH, HEIGHT = 615, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

# gets the returned list of images that was loaded in the load_images function
images = load_images()

# Limit number of images based on grid size
# if grid size selected is exactly 4 then only pick 8 images inside the images list
# if not then pick exactly 12 images
if grid_size == 4:
    selected_images = images[:8]
else:
    selected_images = images[:12]

# Duplicate images to have pairs and shuffle the pairs
pairs = selected_images * 2
random.shuffle(pairs)

# Create Card objects inside a list, while using images inside pairs, 
# and insert positions list then loop
# for i in range of total_cards which is either 16 or 24
cards = [Card(pairs[i], positions[i]) for i in range(total_cards)]


# Function only used for restarting game variables
def restart_game():
    # global accesses all the variables outside the function and changes them within the function
    global first_card, second_card, matches, attempts, cards, positions, pairs, grid_size, WIDTH, HEIGHT, screen

    grid_size = choose_grid_size() # Gets and store new grid size

    # Change the screen size depending on grid size
    if grid_size == 5:
        WIDTH, HEIGHT = 615, 700
    else:
        WIDTH, HEIGHT = 500, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # resets the board and scores
    first_card = None
    second_card = None
    matches = 0
    attempts = 0

    # reloads the images again
    images = load_images()
    selected_images = images[:8] if grid_size == 4 else images[:12]
    pairs = selected_images * 2
    random.shuffle(pairs)

    # sets positions again
    positions = create_card_positions(grid_size)
    cards = [Card(pairs[i], positions[i]) for i in range(len(positions))]


# Pause Screen
def pause_screen(pause=False):
    # Button settings
    button_width, button_height = 200, 60
    

    while pause:
        
        # Background image load
        bg_img = pygame.image.load(Path(BackGround / 'Win.png')).convert()
        bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
        screen.blit(bg_img, (0, 0))
        # Draw buttons
        restart = pygame.Rect(btn1_x, btn1_y, button_width, button_height)
        menu = pygame.Rect(btn2_x, btn2_y, button_width, button_height)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if grid_size == 5:
                        ChangeWindowSize("large")
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
    global WIDTH, HEIGHT, screen
    Win.play()
    Win.set_volume(0.1)
    if grid_size == 5:
        ChangeWindowSize("small")

    while win:
        # Background image load
        bg_img = pygame.image.load(Path(BackGround / 'Win.png')).convert()
        bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
        screen.blit(bg_img, (0, 0))
        restart = pygame.Rect(btn1_x, btn1_y, button_width, button_height)
        menu = pygame.Rect(btn2_x, btn2_y, button_width, button_height)

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
    if grid_size == 5:
        bg_img = pygame.image.load(Path(BackGround / 'Free.png')).convert()
        bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
        screen.blit(bg_img, (0, 0))
    else:
        screen.fill(AZURE)
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
                if grid_size == 5:
                    ChangeWindowSize("small")
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