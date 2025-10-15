import pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((1200, 600))
pygame.display.set_caption("Button Change Example")

# Board
a1 = pygame.Rect(200, 200, 30, 30)
a2 = pygame.Rect(200, 230, 30, 30)
a3 = pygame.Rect(200, 260, 30, 30)
a4 = pygame.Rect(200, 290, 30, 30)
a5 = pygame.Rect(200, 320, 30, 30)

b1 = pygame.Rect(230, 200, 30, 30)
b2 = pygame.Rect(230, 230, 30, 30)
b3 = pygame.Rect(230, 260, 30, 30)
b4 = pygame.Rect(230, 290, 30, 30)
b5 = pygame.Rect(230, 320, 30, 30)

c1 = pygame.Rect(260, 200, 30, 30)
c2 = pygame.Rect(260, 230, 30, 30)
c3 = pygame.Rect(260, 260, 30, 30)
c4 = pygame.Rect(260, 290, 30, 30)
c5 = pygame.Rect(260, 320, 30, 30)

d1 = pygame.Rect(290, 200, 30, 30)
d2 = pygame.Rect(290, 230, 30, 30)
d3 = pygame.Rect(290, 260, 30, 30)
d4 = pygame.Rect(290, 290, 30, 30)
d5 = pygame.Rect(290, 320, 30, 30)

e1 = pygame.Rect(320, 200, 30, 30)
e2 = pygame.Rect(320, 230, 30, 30)
e3 = pygame.Rect(320, 260, 30, 30)
e4 = pygame.Rect(320, 290, 30, 30)
e5 = pygame.Rect(320, 320, 30, 30)

# Define the first button (red)
button = pygame.Rect(500, 250, 200, 60)  # x, y, width, height

# Back button ewan
back_button = pygame.Rect(500, 300, 50, 50)

# Back button click state
back_click = False

# Font for button text (uses default pygame font)
font = pygame.font.Font(None, 40)

# Track if the first button was clicked
button_clicked = False

running = True
while running:
    # --- EVENT LOOP ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Exit if window is closed

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Click on first button → hide it and show new box
            if not button_clicked and button.collidepoint(event.pos):
                button_clicked = True
                back_click = True

            # Click on new box → do something (example print)
            elif button_clicked and a1.collidepoint(event.pos):
                print("A1!")
            elif button_clicked and a2.collidepoint(event.pos):
                print("A2!")
            elif button_clicked and a3.collidepoint(event.pos):
                print("A3!")
            elif button_clicked and a4.collidepoint(event.pos):
                print("A4!")
            elif button_clicked and a5.collidepoint(event.pos):
                print("A5!")
            elif button_clicked and b1.collidepoint(event.pos):
                print("B1!")
            elif button_clicked and b2.collidepoint(event.pos):
                print("B2!")
            elif button_clicked and b3.collidepoint(event.pos):
                print("B3!")
            elif button_clicked and b4.collidepoint(event.pos):
                print("B4!")
            elif button_clicked and b5.collidepoint(event.pos):
                print("B5!")
            elif button_clicked and c1.collidepoint(event.pos):
                print("C1!")
            elif button_clicked and c2.collidepoint(event.pos):
                print("C2!")
            elif button_clicked and c3.collidepoint(event.pos):
                print("C3!")
            elif button_clicked and c4.collidepoint(event.pos):
                print("C4!")
            elif button_clicked and c5.collidepoint(event.pos):
                print("C5!")
            elif button_clicked and d1.collidepoint(event.pos):
                print("D1!")
            elif button_clicked and d2.collidepoint(event.pos):
                print("D2!")
            elif button_clicked and d3.collidepoint(event.pos):
                print("D3!")
            elif button_clicked and d4.collidepoint(event.pos):
                print("D4!")
            elif button_clicked and d5.collidepoint(event.pos):
                print("D5!")
            elif button_clicked and e1.collidepoint(event.pos):
                print("E1!")
            elif button_clicked and e2.collidepoint(event.pos):
                print("E2!")
            elif button_clicked and e3.collidepoint(event.pos):
                print("E3!")
            elif button_clicked and e4.collidepoint(event.pos):
                print("E4!")
            elif button_clicked and e5.collidepoint(event.pos):
                print("E5!")
            # Click on back button → go back to first button
            elif back_click and back_button.collidepoint(event.pos):
                button_clicked = False
                back_click = False
                

    # --- DRAWING SECTION ---
    screen.fill((30, 30, 30))  # Background color

    # Change mouse cursor when hovering over clickable areas
    if not button_clicked and button.collidepoint(pygame.mouse.get_pos()):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    elif button_clicked and a1.collidepoint(pygame.mouse.get_pos()):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    elif button_clicked and a2.collidepoint(pygame.mouse.get_pos()):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    elif button_clicked and a3.collidepoint(pygame.mouse.get_pos()):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    
    # Change mouse cursor when hovering over back button
    if back_click and back_button.collidepoint(pygame.mouse.get_pos()):
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    

    # Draw and label the active button/box
    if not button_clicked:
        # Draw first (red) button
        pygame.draw.rect(screen, (200, 0, 0), button)
        text = font.render("Click Me", True, (255, 255, 255))
        text_rect = text.get_rect(center=button.center)
        screen.blit(text, text_rect)
    else:
        # Loop to draw all boxes
        for box in [a1, a2, a3, a4, a5]:
            pygame.draw.rect(screen, (0, 100, 0), box)
            text = font.render("x", True, (0, 0, 0))
            text_rect = text.get_rect(center=box.center)
            screen.blit(text, text_rect)
        for box in [b1, b2, b3, b4, b5]:
            pygame.draw.rect(screen, (0, 100, 0), box)
            text = font.render("x", True, (0, 0, 0))
            text_rect = text.get_rect(center=box.center)
            screen.blit(text, text_rect)
        for box in [c1, c2, c3, c4, c5]:
            pygame.draw.rect(screen, (0, 100, 0), box)
            text = font.render("x", True, (0, 0, 0))
            text_rect = text.get_rect(center=box.center)
            screen.blit(text, text_rect)
        for box in [d1, d2, d3, d4, d5]:
            pygame.draw.rect(screen, (0, 100, 0), box)
            text = font.render("x", True, (0, 0, 0))
            text_rect = text.get_rect(center=box.center)
            screen.blit(text, text_rect)
        for box in [e1, e2, e3, e4, e5]:
            pygame.draw.rect(screen, (0, 100, 0), box)
            text = font.render("x", True, (0, 0, 0))
            text_rect = text.get_rect(center=box.center)
            screen.blit(text, text_rect)


        # Draw back button
        pygame.draw.rect(screen, (0, 0, 200), back_button)
        back_text = font.render("<", True, (255, 255, 255))
        back_text_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, back_text_rect)

        

    # Update display
    pygame.display.flip()

pygame.quit()
