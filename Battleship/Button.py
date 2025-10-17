import pygame as pg
from pathlib import Path
import string
import os
pg.init()

# Create the game window
screen = pg.display.set_mode((500, 600))
pg.display.set_caption("Button Change Example")

# Get the directory of the current project
parent = Path(__file__).parent

# BACKGROUNDS
def GameBg():
    # Make sure 'background.jpg' exists in the same directory as your script
    background_image = pg.image.load(Path(parent, 'img/background.png')).convert() 
    # Scale the image to fit the screen (optional, but often necessary)
    background_image = pg.transform.scale(background_image, (1200, 600))
    screen.blit(background_image, (0, 0))

def tempobg():
    # Make sure 'TempBG.jpg' exists in the same directory as your script
    TempBG = pg.image.load(Path(parent, 'img/TempBG.jpg')).convert() 
    # Scale the image to fit the screen (optional, but often necessary)
    TempBG = pg.transform.scale(TempBG, (500, 600))
    screen.blit(TempBG, (0, 0))
tempobg()

# BUTTON CLASS
class p1_btn:
    def __init__(self, x, y, size, callback, name, font=pg.font.Font(None, 36)):
        self.name = name
        self.image = font.render(None, 1, (pg.Color('white')))
        self.rect = pg.Rect(x, y, size, size)
        self.bg_color = (127, 127, 127)
        self.hover_color = (200, 200, 200)
        self.mouse_hovering = False
        self.callback = callback

    def draw(self, screen):
        if self.mouse_hovering:
            screen.fill(self.hover_color, self.rect)
        else:
            screen.fill(self.bg_color, self.rect)
        screen.blit(self.image, self.rect)
    
    def on_mousemotion(self, event):
        self.mouse_hovering = self.rect.collidepoint(event.pos)

    def on_click(self, event):
        if self.mouse_hovering:
            self.callback(self)

def button_callback(btn):
    print(btn.name)

p1_btns = []
# Board buttons
i = 0
while i < 5:
    count = 0
    for enum, letter in enumerate(string.ascii_lowercase):
        x = enum % 1 * 70 + 90
        y = i * 70 + 20
        name = letter + str(i)
        p1_btns.append(p1_btn(x, y, 60, button_callback, name))
        count += 1
        if count == 6:
            break
    i += 1


# Define the first button (red)
button = pg.Rect(140, 250, 200, 60)  # x, y, width, height

# Back button ewan
back_button = pg.Rect(500, 300, 50, 50)

# Back button click state
back_click = False

# Font for button text (uses default pg font)
font = pg.font.Font(None, 40)

# Track if the first button was clicked
button_clicked = False

running = True
while running:
    # --- EVENT LOOP ---
    for event in pg.event.get():
        
        if event.type == pg.QUIT:
            running = False  # Exit if window is closed
        elif event.type == pg.MOUSEMOTION:
                for p1_button in p1_btns:
                    p1_button.on_mousemotion(event)
 
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                for p1_button in p1_btns:
                    p1_button.on_click(event)
 
        
        if event.type == pg.MOUSEBUTTONDOWN:
            # Click on first button → hide it and show new box
            
            if not button_clicked and button.collidepoint(event.pos):
                button_clicked = True
                back_click = True
                pg.display.quit()
                screen = pg.display.set_mode((1200, 600))
                GameBg()
                
            # Click on back button → go back to first button
            elif back_click and back_button.collidepoint(event.pos):
                button_clicked = False
                back_click = False
                pg.display.quit()
                screen = pg.display.set_mode((500, 600))
                tempobg()

    
    # Change mouse cursor when hovering over back button
    if back_click and back_button.collidepoint(pg.mouse.get_pos()):
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
    

    # Draw and label the active button/box
    if not button_clicked:
        # Draw first (red) button
        pg.draw.rect(screen, (200, 0, 0), button)
        text = font.render("Click Me", True, (255, 255, 255))
        text_rect = text.get_rect(center=button.center)
        screen.blit(text, text_rect)
    else:
        # Draw all the buttons
        for p1_button in p1_btns:
                p1_button.draw(screen)
        
        # Draw back button
        pg.draw.rect(screen, (0, 0, 200), back_button)
        back_text = font.render("<", True, (255, 255, 255))
        back_text_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, back_text_rect)

    # Update display
    pg.display.flip()

pg.quit()
