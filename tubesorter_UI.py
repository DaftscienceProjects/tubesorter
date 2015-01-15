import pygame, os
import sys
from constants import *
from label import Label
from pygame.locals import *

sys.dont_write_bytecode = True


os.putenv("SDL_FBDEV", "/dev/fb1")
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

display_width = 320
display_height = 240
screen = pygame.display.set_mode((display_width, display_height))
background = pygame.Surface(screen.get_size())
clock = pygame.time.Clock()




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
    self.accn_input = text_prompt(maxlength=20, color=ASPHALT, prompt='Accn #: ', x=2, y=2)
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
        # self.accn_input.draw()
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

class ConfigError(KeyError): pass

class Config:
    """ A utility for configuration """
    def __init__(self, options, *look_for):
        assertions = []
        for key in look_for:
            if key[0] in options.keys(): exec('self.'+key[0]+' = options[\''+key[0]+'\']')
            else: exec('self.'+key[0]+' = '+key[1])
            assertions.append(key[0])
        for key in options.keys():
            if key not in assertions: raise ConfigError(key+' not expected as option')

class text_prompt:
    """ A text input for pygame apps """
    def __init__(self, **options):
        """ Options: x, y, font, color, restricted, maxlength, prompt """
        self.options = Config(options, ['x', '0'], ['y', '0'], ['font', 'pygame.font.Font(None, 32)'],
                              ['color', '(0,0,0)'], ['restricted', '\'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&\\\'()*+,-./:;<=>?@[\]^_`{|}~\''],
                              ['maxlength', '-1'], ['prompt', '\'\''])
        self.x = self.options.x; self.y = self.options.y
        self.font = self.options.font
        self.color = self.options.color
        self.restricted = self.options.restricted
        self.maxlength = self.options.maxlength
        self.prompt = self.options.prompt; self.value = ''
        self.shifted = False
        
        self.text = Label(
                  screen,
                  bg_color=CLOUD, 
                  font_color=ASPHALT, 
                  font_size = 30,
                  background_size=(314, 25),
                  center=(background.get_width()/2, 15), 
                  align="left")
        self.text.text = self.prompt + ' '
        self.text_sprite = pygame.sprite.Group(self.text)
        self.text.update()

    def draw(self):
        mouse = pygame.mouse.get_pos()
        # self.accn_input.draw()
        self.text.text = self.text.text = self.prompt + ' '+self.value
        self.text.update()
        self.text_sprite.clear(screen, background)
        self.text_sprite.update()
        self.text_sprite.draw(screen)
        # self.osk_btn.draw(screen, mouse)
        # self.exit.draw(screen, mouse)


    def update(self, events):
        """ Update the input based on passed events """
        for event in events:
            if event.type == KEYUP:
                if event.key == K_LSHIFT or event.key == K_RSHIFT: self.shifted = False
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE: self.value = self.value[:-1]
                elif event.key == K_LSHIFT or event.key == K_RSHIFT: self.shifted = True
                elif event.key == K_SPACE: self.value += ' '
                elif event.key == K_RETURN: 
                    submit = self.value
                    self.value = ''
                    return submit
                if not self.shifted:
                    if event.key == K_a and 'a' in self.restricted: self.value += 'a'
                    elif event.key == K_b and 'b' in self.restricted: self.value += 'b'
                    elif event.key == K_c and 'c' in self.restricted: self.value += 'c'
                    elif event.key == K_d and 'd' in self.restricted: self.value += 'd'
                    elif event.key == K_e and 'e' in self.restricted: self.value += 'e'
                    elif event.key == K_f and 'f' in self.restricted: self.value += 'f'
                    elif event.key == K_g and 'g' in self.restricted: self.value += 'g'
                    elif event.key == K_h and 'h' in self.restricted: self.value += 'h'
                    elif event.key == K_i and 'i' in self.restricted: self.value += 'i'
                    elif event.key == K_j and 'j' in self.restricted: self.value += 'j'
                    elif event.key == K_k and 'k' in self.restricted: self.value += 'k'
                    elif event.key == K_l and 'l' in self.restricted: self.value += 'l'
                    elif event.key == K_m and 'm' in self.restricted: self.value += 'm'
                    elif event.key == K_n and 'n' in self.restricted: self.value += 'n'
                    elif event.key == K_o and 'o' in self.restricted: self.value += 'o'
                    elif event.key == K_p and 'p' in self.restricted: self.value += 'p'
                    elif event.key == K_q and 'q' in self.restricted: self.value += 'q'
                    elif event.key == K_r and 'r' in self.restricted: self.value += 'r'
                    elif event.key == K_s and 's' in self.restricted: self.value += 's'
                    elif event.key == K_t and 't' in self.restricted: self.value += 't'
                    elif event.key == K_u and 'u' in self.restricted: self.value += 'u'
                    elif event.key == K_v and 'v' in self.restricted: self.value += 'v'
                    elif event.key == K_w and 'w' in self.restricted: self.value += 'w'
                    elif event.key == K_x and 'x' in self.restricted: self.value += 'x'
                    elif event.key == K_y and 'y' in self.restricted: self.value += 'y'
                    elif event.key == K_z and 'z' in self.restricted: self.value += 'z'
                    elif event.key == K_0 and '0' in self.restricted: self.value += '0'
                    elif event.key == K_1 and '1' in self.restricted: self.value += '1'
                    elif event.key == K_2 and '2' in self.restricted: self.value += '2'
                    elif event.key == K_3 and '3' in self.restricted: self.value += '3'
                    elif event.key == K_4 and '4' in self.restricted: self.value += '4'
                    elif event.key == K_5 and '5' in self.restricted: self.value += '5'
                    elif event.key == K_6 and '6' in self.restricted: self.value += '6'
                    elif event.key == K_7 and '7' in self.restricted: self.value += '7'
                    elif event.key == K_8 and '8' in self.restricted: self.value += '8'
                    elif event.key == K_9 and '9' in self.restricted: self.value += '9'
                    elif event.key == K_BACKQUOTE and '`' in self.restricted: self.value += '`'
                    elif event.key == K_MINUS and '-' in self.restricted: self.value += '-'
                    elif event.key == K_EQUALS and '=' in self.restricted: self.value += '='
                    elif event.key == K_LEFTBRACKET and '[' in self.restricted: self.value += '['
                    elif event.key == K_RIGHTBRACKET and ']' in self.restricted: self.value += ']'
                    elif event.key == K_BACKSLASH and '\\' in self.restricted: self.value += '\\'
                    elif event.key == K_SEMICOLON and ';' in self.restricted: self.value += ';'
                    elif event.key == K_QUOTE and '\'' in self.restricted: self.value += '\''
                    elif event.key == K_COMMA and ',' in self.restricted: self.value += ','
                    elif event.key == K_PERIOD and '.' in self.restricted: self.value += '.'
                    elif event.key == K_SLASH and '/' in self.restricted: self.value += '/'
                elif self.shifted:
                    if event.key == K_a and 'A' in self.restricted: self.value += 'A'
                    elif event.key == K_b and 'B' in self.restricted: self.value += 'B'
                    elif event.key == K_c and 'C' in self.restricted: self.value += 'C'
                    elif event.key == K_d and 'D' in self.restricted: self.value += 'D'
                    elif event.key == K_e and 'E' in self.restricted: self.value += 'E'
                    elif event.key == K_f and 'F' in self.restricted: self.value += 'F'
                    elif event.key == K_g and 'G' in self.restricted: self.value += 'G'
                    elif event.key == K_h and 'H' in self.restricted: self.value += 'H'
                    elif event.key == K_i and 'I' in self.restricted: self.value += 'I'
                    elif event.key == K_j and 'J' in self.restricted: self.value += 'J'
                    elif event.key == K_k and 'K' in self.restricted: self.value += 'K'
                    elif event.key == K_l and 'L' in self.restricted: self.value += 'L'
                    elif event.key == K_m and 'M' in self.restricted: self.value += 'M'
                    elif event.key == K_n and 'N' in self.restricted: self.value += 'N'
                    elif event.key == K_o and 'O' in self.restricted: self.value += 'O'
                    elif event.key == K_p and 'P' in self.restricted: self.value += 'P'
                    elif event.key == K_q and 'Q' in self.restricted: self.value += 'Q'
                    elif event.key == K_r and 'R' in self.restricted: self.value += 'R'
                    elif event.key == K_s and 'S' in self.restricted: self.value += 'S'
                    elif event.key == K_t and 'T' in self.restricted: self.value += 'T'
                    elif event.key == K_u and 'U' in self.restricted: self.value += 'U'
                    elif event.key == K_v and 'V' in self.restricted: self.value += 'V'
                    elif event.key == K_w and 'W' in self.restricted: self.value += 'W'
                    elif event.key == K_x and 'X' in self.restricted: self.value += 'X'
                    elif event.key == K_y and 'Y' in self.restricted: self.value += 'Y'
                    elif event.key == K_z and 'Z' in self.restricted: self.value += 'Z'
                    elif event.key == K_0 and ')' in self.restricted: self.value += ')'
                    elif event.key == K_1 and '!' in self.restricted: self.value += '!'
                    elif event.key == K_2 and '@' in self.restricted: self.value += '@'
                    elif event.key == K_3 and '#' in self.restricted: self.value += '#'
                    elif event.key == K_4 and '$' in self.restricted: self.value += '$'
                    elif event.key == K_5 and '%' in self.restricted: self.value += '%'
                    elif event.key == K_6 and '^' in self.restricted: self.value += '^'
                    elif event.key == K_7 and '&' in self.restricted: self.value += '&'
                    elif event.key == K_8 and '*' in self.restricted: self.value += '*'
                    elif event.key == K_9 and '(' in self.restricted: self.value += '('
                    elif event.key == K_BACKQUOTE and '~' in self.restricted: self.value += '~'
                    elif event.key == K_MINUS and '_' in self.restricted: self.value += '_'
                    elif event.key == K_EQUALS and '+' in self.restricted: self.value += '+'
                    elif event.key == K_LEFTBRACKET and '{' in self.restricted: self.value += '{'
                    elif event.key == K_RIGHTBRACKET and '}' in self.restricted: self.value += '}'
                    elif event.key == K_BACKSLASH and '|' in self.restricted: self.value += '|'
                    elif event.key == K_SEMICOLON and ':' in self.restricted: self.value += ':'
                    elif event.key == K_QUOTE and '"' in self.restricted: self.value += '"'
                    elif event.key == K_COMMA and '<' in self.restricted: self.value += '<'
                    elif event.key == K_PERIOD and '>' in self.restricted: self.value += '>'
                    elif event.key == K_SLASH and '?' in self.restricted: self.value += '?'

        if len(self.value) > self.maxlength and self.maxlength >= 0: self.value = self.value[:-1]
        self.draw()
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
