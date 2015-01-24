import pygame, os, time, random, sys, eztext
from tubesorter_UI import *
from database_functions import *
# from font import *
import RPi.GPIO as GPIO
from piTFT import *
from label import Label


# Initialize touchscreen
pitft = PiTFT_Screen()

# define touchscreen buttons
pitft.Button1Interrupt(pitft.backlight_off)
pitft.Button2Interrupt(pitft.backlight_low)
pitft.Button3Interrupt(pitft.backlight_med)
pitft.Button4Interrupt(pitft.backlight_high)



# sys.dont_write_bytecode = True

# set video and input to pitft
os.putenv("SDL_FBDEV", "/dev/fb1")
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')



# initialize pygame and global variables
pygame.init()
display_width = 320
display_height = 240
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((display_width, display_height))
background = pygame.Surface(screen.get_size())
clock = pygame.time.Clock()


def osk():

   screen.fill(cloud)
   exit  = my_button('exit', (187,  188, 60, 50), (125,103))
   enter = my_button('enter', (65,  188, 60, 50), (125,103))
   mouse = pygame.mouse.get_pos()
   keyboard = [ 
            my_button('1', (65,   35,  60, 50), (125,103), value='1'),
            my_button('2', (126,  35,  60, 50), (125,103), value='2'),
            my_button('3', (187,  35,  60, 50), (125,103), value='3'),
            my_button('4', (65,   86,  60, 50), (125,103), value='4'),
            my_button('5', (126,  86,  60, 50), (125,103), value='5'),
            my_button('6', (187,  86,  60, 50), (125,103), value='6'),
            my_button('7', (65,   137, 60, 50), (125,103), value='7'),
            my_button('8', (126,  137, 60, 50), (125,103), value='8'),
            my_button('9', (187,  137, 60, 50), (125,103), value='9'),
            my_button('0', (126,  188, 60, 50), (125,103), value='0'), 
   ]

   for btn in keyboard:
        btn.draw(screen, pygame.mouse.get_pos())
   accn_input = eztext.Input(maxlength=20, color=asphalt, prompt='Accn#: ', x=2, y=2)
   inp = ''
   exit.draw(screen, mouse)
   enter.draw(screen, mouse)

   while True:
      # screen.fill(cloud)
      mouse = pygame.mouse.get_pos()
      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:
            run = False
         elif event.type == pygame.MOUSEBUTTONUP:
            mouse = pygame.mouse.get_pos()
            for btn in keyboard:
               if btn.obj.collidepoint(mouse):
                  inp = inp + btn.value
                  accn_input.value = inp
            if enter.obj.collidepoint(mouse):
               pygame.mouse.set_pos(0,0)
               screen.fill(cloud)
               if accn_input.value == '':
                  return None
               else:
                 return accn_input.value
            if exit.obj.collidepoint(mouse):
               pygame.mouse.set_pos(0,0)
               screen.fill(cloud)
               return None
      accn = accn_input.update(events)
      accn_input.draw(screen)

      pygame.display.flip()
      pygame.event.wait

def file_tube(db):
    accn = ''
    pygame.mouse.set_pos(0,0)
    screen.fill(cloud)
    mouse = pygame.mouse.get_pos()
    
    exit= my_button('Exit', (170, 185,  130, 40,), (125,103))
    OSk_BTN = my_button('Keyboard', (20,  185,  130, 40,), (125,163))
    
    accn_input = eztext.Input(maxlength=20, color=asphalt, prompt='Accn#: ', x=2, y=2)
    
    title_text = Label(screen, 
                  text="File Tube",
                  bg_color=purple, 
                  font_color=cloud, 
                  font_size = 40,
                  background_size=(background.get_width(), 60),
                  center=(background.get_width()/2, 60))
    location_text = Label(screen,
                  bg_color=purple, 
                  font_color=cloud, 
                  font_size = 20,
                  background_size=(background.get_width(), 25),
                  center=(background.get_width()/2, 90), 
                  align="center")


    allSprites = pygame.sprite.OrderedUpdates(title_text, location_text)

    run = True

    while run:
        events = pygame.event.get()
        accn = accn_input.update(events)

        row = ROWS[str(db.next_row)]
        rack = str(db.next_rack)
        column = str(db.next_column)

        print(row+column+rack)
        location_text.text = "Scan tube, then place here: Rack"+rack+": "+row+"-"+column

        accn_input.draw(screen)

        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)

        OSk_BTN.draw(screen, mouse)
        exit.draw(screen, mouse)
        pygame.display.flip()

        pygame.event.wait
        for event in events:
             if event.type == pygame.QUIT:
                run = False
             elif event.type == pygame.KEYDOWN:
                if event.key == K_RETURN: 
                  db.file_accn(accn)
                  accn_input.value = ''
             elif event.type == pygame.MOUSEBUTTONUP:
                mouse = pygame.mouse.get_pos()
                if exit.obj.collidepoint(mouse):
                   pygame.mouse.set_pos(0,0)
                   screen.fill(cloud)
                   return
                elif OSk_BTN.obj.collidepoint(mouse):
                    accn = osk()
                    if accn:
                      db.file_accn(accn)
                    else:
                      accn_input.value = ''
def locate_tube(db):
 pass


def main_menu(db):
    
    
    fileTube    = my_button('File',     (20,  125,  130, 40,), (125,103))
    locateTube  = my_button('Locate',   (170, 125,  130, 40,), (125,133))
    settings    = my_button('Settings', (20,  185,  130, 40,), (125,163))
    exit        = my_button('Exit',     (170, 185,  130, 40,), (125,103))
    
    screen.fill(cloud)

    title = Label(screen, 
                  text="Pi-Tube Ledger",
                  bg_color=purple, 
                  font_color=cloud, 
                  font_size = 40,
                  background_size=(background.get_width(), 60),
                  center=(background.get_width()/2, 60))
    sub_title = Label(screen, 
                  text="beta  ",
                  bg_color=purple, 
                  font_color=cloud, 
                  font_size = 20,
                  background_size=(background.get_width(), 25),
                  center=(background.get_width()/2, 90), 
                  align="right")


    allSprites = pygame.sprite.OrderedUpdates(title, sub_title)

    while True:
      mouse = pygame.mouse.get_pos()
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            return
         elif event.type == pygame.MOUSEBUTTONUP:
            mouse = pygame.mouse.get_pos()
            if fileTube.obj.collidepoint(mouse):
               print('file pressed')
               file_tube(db)
            elif locateTube.obj.collidepoint(mouse):
               print('locate pressed')
               locate_tube(db)
            elif settings.obj.collidepoint(mouse):
               print('settings pressed')
               osk()
            elif exit.obj.collidepoint(mouse):
               print('exit pressed')
               return

      fileTube.draw(    screen, mouse)
      locateTube.draw(  screen, mouse)
      settings.draw(    screen, mouse)
      exit.draw(        screen, mouse)



      allSprites.clear(screen, background)
      allSprites.update()
      allSprites.draw(screen)



      pygame.display.flip()

if __name__ == '__main__':
  rack_dimensions = {'columns': 6, 'rows': 12}
  db = sqlite_database('racks.db', rack_dimensions)
  main_menu(db)
  quitgame()
