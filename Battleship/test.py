import pygame
import string
 
class SimpleButton:
    def __init__(self, caption, position, callback, font, color, bg_color, hover_color):
        self.image = font.render(caption, 1, color)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.mouse_hovering = False
        self.callback = callback
        self.caption = caption
 
    def draw(self, surface):
        if self.mouse_hovering:
            surface.fill(self.hover_color, self.rect)
        else:
            surface.fill(self.bg_color, self.rect)
 
        surface.blit(self.image, self.rect)
 
    def on_mousemotion(self, event):
        self.mouse_hovering = self.rect.collidepoint(event.pos)
 
    def on_click(self, event):
        if self.mouse_hovering:
            self.callback(self)
 
def button_callback(button):
    print(button.caption)
 
def main():
    pygame.init()
    pygame.display.set_caption('Simple Button Example')
    surface = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
 
    buttons = []
    button_layout = (pygame.font.Font(None, 24),
                     pygame.Color('white'),
                     pygame.Color('navy'),
                     pygame.Color('dodgerblue'))
 
    for enum, letter in enumerate(string.ascii_lowercase):
        x = enum % 13
        pos = x * 20 + 100, enum // 13 * 30 + 40
        buttons.append(SimpleButton(letter, pos, button_callback, *button_layout))
 
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
 
            elif event.type == pygame.MOUSEMOTION:
                for button in buttons:
                    button.on_mousemotion(event)
 
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    for button in buttons:
                        button.on_click(event)
 
        surface.fill(pygame.Color('black'))
        for button in buttons:
            button.draw(surface)
 
        pygame.display.flip()
        clock.tick(20)
 
    pygame.quit()
 
main()