import pygame, eztext
import sys
from constants import *
from label import Label

sys.dont_write_bytecode = True

def quitgame():
    pygame.quit()
    quit()

class my_button:
    # label_coord may not be needed anymore
    def __init__(self, text, rect_coord, label_coord, font_color=ASPHALT, color=ORANGE, value=None):
      self.text = text
      self.is_hover = False
      self.rect_coord = rect_coord
      self.label_coord = label_coord
      self.is_clicked = False
      self.value = value
      self.default_color = color
      self.hover_color = BLUE
      self.clicked_color = BLUE
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


class app_screen:
  def __init__(self, screen, background, title, info=True):
    self.screen = screen
    self.background = background
    self.exit= my_button('Exit', (162, 185,  155, 40,), (125,103))
    self.osk_btn = my_button('Keyboard', (3,  185,  155, 40,), (125,163))
    self.accn_input = eztext.Input(maxlength=20, color=ASPHALT, prompt='Accn #: ', x=2, y=2)
    self.title_text = Label(
                  screen, 
                  text=title,
                  bg_color=PURPLE, 
                  font_color=CLOUD, 
                  font_size = 40,
                  # background_size=(background.get_width()-50, 60),
                  background_size=(314, 60),
                  center=(background.get_width()/2, 60))
    self.subtitle_text = Label(
                  screen,
                  bg_color=PURPLE, 
                  font_color=CLOUD, 
                  font_size = 20,
                  background_size=(314, 25),
                  center=(background.get_width()/2, 90), 
                  align="center")
    self.info_sprites = pygame.sprite.OrderedUpdates(self.title_text, self.subtitle_text)
    if info:
      self.info_text = Label(
                  screen,
                  bg_color=CLOUD,
                  transparent=True, 
                  font_color=ASPHALT, 
                  font_size = 22,
                  background_size=(300, 25),
                  center=(background.get_width()/2, 120), 
                  align="left")
      self.info_sprites.add(self.info_text)
    else:
      self.info_text = None
    


  def check_scanner(self, events):
      return self.accn_input.update(events)
  def draw(self):
        mouse = pygame.mouse.get_pos()
        self.accn_input.draw(self.screen)
        self.info_sprites.clear(self.screen, self.background)
        self.info_sprites.update()
        self.info_sprites.draw(self.screen)
        self.osk_btn.draw(self.screen, mouse)
        self.exit.draw(self.screen, mouse)



class TextRectException:
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

def render_textrect(string, font, rect, text_color, background_color, justification=0):
    final_lines = []

    requested_lines = string.splitlines()

    # Create a series of lines that will fit on the provided
    # rectangle.

    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            # if any of our words are too long to fit, return.
            for word in words:
                if font.size(word)[0] >= rect.width:
                    raise TextRectException, "The word " + word + " is too long to fit in the rect passed."
            # Start a new line
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "
                # Build the line while the words fit.    
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line
                else:
                    final_lines.append(accumulated_line)
                    accumulated_line = word + " "
            final_lines.append(accumulated_line)
        else:
            final_lines.append(requested_line)

    # Let's try to write the text out on the surface.

    surface = pygame.Surface(rect.size)
    surface.fill(background_color)

    accumulated_height = 0
    for line in final_lines:
        if accumulated_height + font.size(line)[1] >= rect.height:
            raise TextRectException, "Once word-wrapped, the text string was too tall to fit in the rect."
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
            else:
                raise TextRectException, "Invalid justification argument: " + str(justification)
        accumulated_height += font.size(line)[1]

    return surface







class multi_line_textbox:
  def __init__(
            self,
            screen, 
            rect, 
            font=None, 
            font_size=16, 
            font_color=PURPLE, 
            bg_color=CLOUD, 
            string=''):
    self.screen = screen
    self.rect = pygame.Rect(rect)
    self.font = pygame.font.Font(font, font_size)
    self.font_color = font_color
    self.bg_color = bg_color
    self.string = string
    self.update()
  def update(self):
    self.rendered_text = render_textrect(self.string, self.font, self.rect, self.font_color, self.bg_color, 0)
    self.screen.blit(self.rendered_text, self.rect.topleft)
