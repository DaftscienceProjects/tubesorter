import pygame, os, time, random, sys, eztext, databaseFunctions
from tubesorter_UI import *
from pygame.locals import *
import RPi.GPIO as GPIO
from piTFT import *
from label import Label

debugging = True
if debugging: print 'debugging mode'
# Initialize touchscreen
pitft = PiTFT_Screen()
pitft.backlight_med

# define touchscreen buttons
pitft.Button1Interrupt(pitft.backlight_off)
pitft.Button2Interrupt(pitft.backlight_low)
pitft.Button3Interrupt(pitft.backlight_med)
pitft.Button4Interrupt(pitft.backlight_high)

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



# This needs to be changed to a class
def osk():
   screen.fill(cloud)
   exit  = my_button('exit', (187,  188, 60, 50), (125,103))
   enter = my_button('enter', (65,  188, 60, 50), (125,103))
   mouse = pygame.mouse.get_pos()
   for btn in OSK_Keyboard_Buttons:
        btn.draw(screen)
   accn_input = eztext.Input(maxlength=20, color=asphalt, prompt='Accn#: ', x=2, y=2)
   inp = ''
   exit.draw(screen)
   enter.draw(screen)

   while True:
      # screen.fill(cloud)
      mouse = pygame.mouse.get_pos()
      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:
            run = False
         elif event.type == pygame.MOUSEBUTTONUP:
            mouse = pygame.mouse.get_pos()
            for btn in OSK_Keyboard_Buttons:
               if btn.obj.collidepoint(mouse):
                  inp = inp + btn.value
                  accn_input.value = inp
            if enter.obj.collidepoint(mouse):
               pygame.mouse.set_pos(0,0)
               screen.fill(cloud)
               return accn_input.value
            if exit.obj.collidepoint(mouse):
               pygame.mouse.set_pos(0,0)
               screen.fill(cloud)
               return
      accn = accn_input.update(events)
      accn_input.draw(screen)
      pygame.display.flip()
      pygame.event.wait

class window_sprites():
  def __init__(self):
    self.open_osk_button = my_button('Keyboard', (20,  185,  130, 40,), (125,163))
    self.exit = my_button('Exit', (170, 185,  130, 40,), (125,103))
    self.accn_input = eztext.Input(maxlength=20, color=asphalt, prompt='Accn#: ', x=2, y=2)
    self.title_text = Label(screen, 
                      bg_color=purple, 
                      font_color=cloud, 
                      font_size = 40,
                      background_size=(background.get_width(), 60),
                      center=(background.get_width()/2, 60))
    self.sub_title_text = Label(screen,
                      bg_color=purple, 
                      font_color=cloud, 
                      font_size = 20,
                      background_size=(background.get_width(), 25),
                      center=(background.get_width()/2, 90), 
                      align="center")
    self.allSprites = pygame.sprite.OrderedUpdates(self.title_text, self.sub_title_text)
  def draw(self):
      self.accn_input.draw(screen)
      self.allSprites.clear(screen, background)
      self.allSprites.update()
      self.allSprites.draw(screen)
      self.open_osk_button.draw(screen)
      self.exit.draw(screen)
      pygame.display.flip()

window_objects = window_sprites()


def file_tube():
    if debugging: print "---File Tube Function"
    accn = ''

    screen.fill(cloud)
    window_objects.title_text.text = "File Tube"
    window_objects.sub_title_text.text = ''
    window_objects.sub_title_text.align = "center"

    run = True

    while run:
        if debugging: print 'looping'
        events = pygame.event.get()
        lastFiled = databaseFunctions.lastFiled()
        
        accn = window_objects.accn_input.update(events)

        loc = databaseFunctions.locateNext()
        window_objects.sub_title_text.text = "Scan tube, then place here: "+ loc[3] + loc[0] + ": " + ROWS[loc[2]]  + "-" + loc[1]

        window_objects.draw()
        pygame.event.wait
        for event in events:
             mouse = pygame.mouse.get_pos()
             if debugging: 
                print 'mouse position:  '
                print mouse
             if event.type == pygame.QUIT:
                run = False
             elif event.type == pygame.KEYDOWN:
                if event.key == K_RETURN:
                  databaseFunctions.fileAccn(accn)
                  window_objects.accn_input.value = ''
             elif event.type == pygame.MOUSEBUTTONUP:
                if window_objects.exit.obj.collidepoint(mouse):
                  if debugging: print ('exit pressed')
                  return
                elif window_objects.open_osk_button.obj.collidepoint(mouse):
                    accn = osk()
                    databaseFunctions.fileAccn(accn)
                    window_objects.accn_input.value = ''

def locate_tube():
    if debugging: print "---Locate Tube Function"
    accn = ''

    screen.fill(cloud)
    window_objects.title_text.text = "Locate Tube"
    window_objects.sub_title_text.text = 'Which tube are you looking for?'
    window_objects.sub_title_text.align = "center"

    run = True

    while run:
        events = pygame.event.get()
        accn = window_objects.accn_input.update(events)

        window_objects.draw()

        pygame.event.wait
        for event in events:
             if event.type == pygame.QUIT:
                run = False
             elif event.type == pygame.KEYDOWN:
                if event.key == K_RETURN: 
                    search_result = databaseFunctions.findAccn(accn)
                    if debugging: 
                        print("Find Accn result:")
                        print search_result
                    window_objects.accn_input.value = ''
             elif event.type == pygame.MOUSEBUTTONUP:
                mouse = pygame.mouse.get_pos()
                if window_objects.exit.obj.collidepoint(mouse):
                   return
                elif window_objects.open_osk_button.obj.collidepoint(mouse):
                    accn = osk()
                    if accn != '':
                      search_result = databaseFunctions.findAccn(accn)
                      if debugging: 
                        print("Find Accn result:")
                        print search_result
                      window_objects.accn_input.value = ''




def main_menu():
    if debugging:  print "---Main Menu"
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
               if debugging: print('file pressed')
               file_tube()
            elif locateTube.obj.collidepoint(mouse):
               if debugging: print('locate pressed')
               locate_tube()
            elif settings.obj.collidepoint(mouse):
               if debugging: print('settings pressed')
               osk()
            elif exit.obj.collidepoint(mouse):
               if debugging: print('exit pressed')
               return

      fileTube.draw(    screen)
      locateTube.draw(  screen)
      settings.draw(    screen)
      exit.draw(        screen)

      # allSprites.clear(screen, background)
      allSprites.update()
      allSprites.draw(screen)
      pygame.display.flip()

if __name__ == '__main__':
    if debugging: print "Started"
    main_menu()
    quitgame()
