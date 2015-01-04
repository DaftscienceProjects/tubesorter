""" labelDemo.py
    creating a basic label sprite"""
    
import pygame
# pygame.init()

# screen = pygame.display.set_mode((640, 480))    
red = (231, 76, 60)
blue = (52, 152, 219)
teal = (26, 188, 156)
purple = (155, 89, 182)
green = (46, 204, 113)
orange = (230, 126, 34)
yellow = (241, 196, 15)
cloud = (236, 240, 241)
asphalt = (52, 73, 94)
concrete = (149, 165, 166)

class Label(pygame.sprite.Sprite):
    """ a basic label 
        properties: 
            text: text to display
            fgColor: foreground color
            bgColor: background color
            center: position of label's center
    """
    
    def __init__(self, text=None, bg_color=cloud, font_color=purple, font=None, size=24):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont(font, size)
        self.text = text
        self.fgColor = font_color
        self.bgColor = bg_color
        self.center = (100, 100)
        self.size = (150, 30)

    def update(self):
        self.image = pygame.Surface(self.size)
        self.image.fill(self.bgColor)
        fontSurface = self.font.render(self.text, True, self.fgColor, self.bgColor)
        #center the text
        xPos = (self.image.get_width() - fontSurface.get_width())/2
        
        self.image.blit(fontSurface, (xPos, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.center