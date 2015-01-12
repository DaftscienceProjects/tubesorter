import pygame
import sys

sys.dont_write_bytecode = True

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
transparent = (0,0,0,0)

ROWS = {'1':'A',
        '2':'B',
        '3':'C',
        '4':'D',
        '5':'E',
        '6':'F',
        '7':'G',
        '8':'H',
        '9':'I',
        '10':'J',
        '11':'K',
        '12':'L'}

def quitgame():
    pygame.quit()
    quit()











class my_button:
    # label_coord may not be needed anymore
    def __init__(self, text, rect_coord, label_coord, font_color=asphalt, color=orange, value=None):
      self.text = text
      self.is_hover = False
      self.rect_coord = rect_coord
      self.label_coord = label_coord
      self.is_clicked = False
      self.value = value
      self.default_color = color
      self.hover_color = blue
      self.clicked_color = blue
      self.font_color = font_color
      self.obj = None
      
    def label(self):
      font = pygame.font.Font(None, 22)
      return font.render(self.text, 1, self.font_color)

    def label_rect(self):
        textRect = self.label().get_rect()
        textRect.center = ((self.rect_coord[0]+(self.rect_coord[2]/2)), (self.rect_coord[1]+(self.rect_coord[3]/2)))
        return textRect

    def color(self):
      if self.is_clicked:
         return self.clicked_color
      else:
         return self.default_color
         
    def draw(self, screen, mouse):
      # print "drawn"
      self.obj  = pygame.draw.rect(screen, self.color(), self.rect_coord)
      screen.blit(self.label(), self.label_rect())
      self.check_hover(mouse)
      
    def check_hover(self, mouse):
      if self.obj.collidepoint(mouse):
         self.is_hover = True 
      else:
         self.is_hover = False
    def clicked():
      self.clicked = True
      self.draw()



class keyboard:
  def __init__(self, value):
    self.one =    my_button('1', (20,  75, 50, 50), (125,103))
    self.two =    my_button('2', (71,  75, 50, 50), (125,103))
    self.three =  my_button('3', (122, 75, 50, 50), (125,103))
    self.four =   my_button('4', (20,  126, 50, 50), (125,103))
    self.five =   my_button('5', (71,  126, 50, 50), (125,103))
    self.six =    my_button('6', (122, 126, 50, 50), (125,103))
    self.seven =  my_button('7', (20,  178, 50, 50), (125,103))
    self.eight =  my_button('8', (71,  178, 50, 50), (125,103))
    self.nine =   my_button('9', (122, 178, 50, 50), (125,103))
    self.zero =   my_button('0', (71,  229, 50, 50), (125,103))