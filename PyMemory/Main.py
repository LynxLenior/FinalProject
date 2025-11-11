import pygame
import random
import time
import os
from pathlib import Path

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# initialize clock
clock = pygame.time.Clock()

# Set up display
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyMemory - Do you KNOW what it takes?")
font = pygame.font.Font(None, 74)
font_gamevar = pygame.font.Font(None, 36)
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# Main Color variables used by the game
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (55, 111, 159)
YELLOW = (255, 209, 65)
AZURE = (0, 38, 69)
GREEN = (12, 255, 60)

# Card size and margins
CARD_SIZE = 100
MARGIN = 20

# change window size if 5x5 grid is selected later
# Initial button positions for pause and win screens
def ChangeWindowSize(size):
    global WIDTH, HEIGHT, screen
    # if window size is small it is used for menus, and 4x4 grid
    if size == "small":
        WIDTH, HEIGHT = 500, 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
    # window size used for 5x5 grid only
    elif size == "large":
        WIDTH, HEIGHT = 615, 700
        screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Button default sizes for win and pause menu
button_width, button_height = 200, 60

# Center positions for win and pause menu buttons
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
seconds = 0
start_time = time.time()

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
    # choose loop variable
    choosing = True
    # buttons for choosing grid size
    four_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 70, 200, 60)
    five_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 30, 200, 60)

    while choosing:
        # set background image for choosing grid size
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
# and insert positions list then do a loop to create cards based on total no. of cards
# for i in range of total_cards which is either 16 or 24
cards = [Card(pairs[i], positions[i]) for i in range(total_cards)]


# Function only used for restarting game variables
def restart_game():
    # global accesses all the variables outside the function and changes them within the function
    global first_card, second_card, matches, attempts, cards, positions, pairs, grid_size, WIDTH, HEIGHT, screen, start_time, seconds
    # reset timer
    start_time = time.time()
    seconds = time.time() - start_time

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
    global start_time, seconds
    # run while the screen is paused
    while pause:
        # Background image load
        bg_img = pygame.image.load(Path(BackGround / 'Pause.png')).convert()
        bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
        screen.blit(bg_img, (0, 0))
        # Draw buttons
        restart = pygame.Rect(btn1_x, btn1_y, button_width, button_height)
        menu = pygame.Rect(btn2_x, btn2_y, button_width, button_height)
        
        # Event handling
        for event in pygame.event.get():
            # if player quits, then close the program
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    start_time = time.time() - seconds
                    # if the grid size selected is 5x5 make sure to change the window size back to large
                    if grid_size == 5:
                        ChangeWindowSize("large")
                    pause = False
                    continue
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # --- Handle Pause Buttons on mouse click ---
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
    # play win screen sound
    Win.play()
    Win.set_volume(0.1)
    # change window size to small on win screen
    if grid_size == 5:
        ChangeWindowSize("small")
    
    while win:
        # Background image load
        bg_img = pygame.image.load(Path(BackGround / 'Win.png')).convert()
        bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
        screen.blit(bg_img, (0, 0))
        restart = pygame.Rect(btn1_x, btn1_y, button_width, button_height)
        menu = pygame.Rect(btn2_x, btn2_y, button_width, button_height)

        # winning comment for the player, position of the text, then display it
        gamevar = font_gamevar.render(f"You matched {matches} cards in {attempts} attempts!", True, YELLOW)
        elapsed = font_gamevar.render(f"Your time is {seconds:.1f}s", True, YELLOW)
        text_y = MARGIN + 10
        screen.blit(gamevar, (10, text_y))
        screen.blit(elapsed, (10, text_y + 30))

        for event in pygame.event.get():
            # if user closes the game, the program exits
            if event.type == pygame.QUIT:
                Click.play()
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # win screen buttons
                if restart and restart.collidepoint(event.pos):
                    # Go back to restart game and choose grid size
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
    pause = pause_screen()    

    # set different background for 5x5 grid
    if grid_size == 5:
        bg_img = pygame.image.load(Path(BackGround / 'Free.png')).convert()
        bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
        screen.blit(bg_img, (0, 0))
    else:
        # blank background on 4x4 grid
        screen.fill(AZURE)
    # loop to get events for the game
    for event in pygame.event.get():
        # end main game loop if the game is exited
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
        # get event on mouse click
            # --- Handle Card Clicks ---
            # first_card and second_card is used to store revealed cards
            # if either of both cards have none stored, then the user can open a card
            if first_card is None or second_card is None:
                # when a card is clicked, loop for all the card objects stored in cards list
                for card in cards:
                    # if the card clicked is found inside the list, and it has not been revealed
                    # nor has it been matched, then set the card's revealed variable to "True"
                    if card.rect.collidepoint(event.pos) and not card.revealed and not card.matched:
                        card.revealed = True
                        Click.play()
                        # if the first card variable has none, then store the card inside
                        if first_card is None:
                            first_card = card
                        # if not, then store it in the second card variable, then add 1 to attempts
                        elif second_card is None:
                            second_card = card
                            attempts += 1

        # if the event is a keydown and it is the escape button, then change the grid size to small
        # and set the pause screen to true
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if grid_size == 5:
                    ChangeWindowSize("small")
                pause_screen(pause=True)

    # each frame, it subtracts start_time from the current time count
    seconds = time.time() - start_time
    
    # Check for match if there's a card inside first and second card variables
    if first_card and second_card:
        # Redraw cards before delay so both are visible
        for card in cards:
            card.draw(screen)
        # update the contents for the whole display
        pygame.display.flip()

        # wait 500 milliseconds before the game checks if the cards are matching
        pygame.time.wait(500)
        # if the first card image variable matches the second card image variable
        # then set both card matched variable into true, add 1 to matches point
        # unreveal the cards if it does not match
        # then clear the first and second variables
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

    # Display all game variables such as matches, attempts and time
    gamevar = font_gamevar.render(f"Matches: {matches}  Attempts: {attempts}", True, YELLOW)
    elapsed = font_gamevar.render(f"Time: {seconds:.1f}s", True, YELLOW)
    # position of the text in the game screen
    if grid_size == 4:
        text_y = (MARGIN + 4 * (CARD_SIZE + MARGIN)) + 10  # just below 4x4 grid
    else:
        text_y = (MARGIN + 5 * (CARD_SIZE + MARGIN)) + 10 # just below 5x5 grid
    screen.blit(gamevar, (10, text_y))
    screen.blit(elapsed, (10, text_y + 30))

    # Check for win, 4x4 needs 8 card matches and 5x5 needs 12 card matches
    if grid_size == 4 and matches == 8:
        win_screen(win=True)
    elif grid_size == 5 and matches == 12:
        win_screen(win=True)

    pygame.display.update()
    # game will tick every 60 milliseconds
    clock.tick(60)

pygame.quit()