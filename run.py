
# Things to fix-----------------------------------
# Imports need to be cleaned up:
#          the import * from whatevers in some includes are spilling into this file
# Timzone issues may be happening, I'm not sure
# In the database_functions.py Locate_next needs to check if it is a new day
#           it then needs to update the rack information
# fix the issue with new databases and filing the second tube. Something weird is happening
# Clean up database fileds, maybe
# when typing accns with keyboard they don't clear after hitting enter
# add a backspace button to the on screen keyboard
#
#


import pygame, os, time, random, sys, eztext, datetime
from tubesorter_UI import *
from constants import *
from database_functions import *
import RPi.GPIO as GPIO
from piTFT import *
from label import Label
from pygame.locals import K_RETURN



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
   screen.fill(CLOUD)
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
   accn_input = eztext.Input(maxlength=20, color=ASPHALT, prompt='Accn #: ', x=2, y=2)
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
               screen.fill(CLOUD)
               if accn_input.value == '':
                  return None
               else:
                 return accn_input.value
            if exit.obj.collidepoint(mouse):
               pygame.mouse.set_pos(0,0)
               screen.fill(CLOUD)
               return None
      accn = accn_input.update(events)
      accn_input.draw(screen)

      pygame.display.flip()
      pygame.event.wait

def file_tube(db):
    accn = ''
    pygame.mouse.set_pos(0,0)
    screen.fill(CLOUD)
    mouse = pygame.mouse.get_pos()
    
    file_screen = app_screen(screen,  background, "File Tube")

    run = True

    while run:
        events = pygame.event.get()
        accn = file_screen.check_scanner(events)

        row = ROWS[str(db.next_row)]
        rack = str(db.next_rack)
        column = str(db.next_column)
        day = strftime('%a', localtime(db.rack_date))


        file_screen.subtitle_text.text = "Scan tube, then place here: "+day+rack+": "+row+"-"+column
        file_screen.info_text.text = "Last accn filed: " + db.last_stored
        file_screen.draw()
        pygame.display.flip()

        pygame.event.wait
        for event in events:
             if event.type == pygame.QUIT:
                run = False
             elif event.type == pygame.KEYDOWN:
                if event.key == K_RETURN: 
                  db.file_accn(accn)
                  file_screen.accn_input.value = ''
             elif event.type == pygame.MOUSEBUTTONUP:
                mouse = pygame.mouse.get_pos()
                if file_screen.exit.obj.collidepoint(mouse):
                   pygame.mouse.set_pos(0,0)
                   screen.fill(CLOUD)
                   return
                elif file_screen.osk_btn.obj.collidepoint(mouse):
                    accn = osk()
                    if accn:
                      db.file_accn(accn)
                    else:
                      file_screen.accn_input.value = ''

def locate_tube(db):
    accn = ''
    pygame.mouse.set_pos(0,0)
    screen.fill(CLOUD)
    mouse = pygame.mouse.get_pos()
    found = None
    locate_screen = app_screen(screen,  background, "Locate Tube")
    locate_screen.subtitle_text.text = "Scan or Enter an accn # to locate"
    locate_screen.info_text.text = ""


    list_of_locations = multi_line_textbox(screen,rect=[210, 108, 100, 77], font=None, font_size=22, string='')


    run = True

    while run:
        events = pygame.event.get()
        accn = locate_screen.check_scanner(events)
        locate_screen.draw()
        list_of_locations.update()
        pygame.display.flip()
        

        pygame.event.wait


        for event in events:
             if event.type == pygame.QUIT:
                run = False
             elif event.type == pygame.KEYDOWN:
                if event.key == K_RETURN: 
                  found = db.find_accn(accn)
             elif event.type == pygame.MOUSEBUTTONUP:
                mouse = pygame.mouse.get_pos()
                if locate_screen.exit.obj.collidepoint(mouse):
                   pygame.mouse.set_pos(0,0)
                   screen.fill(CLOUD)
                   return
                elif locate_screen.osk_btn.obj.collidepoint(mouse):
                    accn = osk()
                    if accn:
                      found = db.find_accn(accn)
             if found:
                list_of_locations.string=''
                count = 0
                pprint(found)
                for row in found:
                  if count < 3:
                    list_of_locations.string += strftime('%a', localtime(row[5]))+":"+row[2]+'  '+ROWS[row[4]]+'-'+row[3]+'\n'
                    print strftime('%a', localtime(row[5]))
                    # print strftime("%a", row[5])
                    for item in row:
                      print item
                    print '---------'
                  count +=1
                locate_screen.info_text.text = "Last 3 locations for "+accn+":"
                locate_screen.accn_input.value = ''
                print list_of_locations.string
                found = False

                  

def main_menu(db):

    fileTube    = my_button('File',     (3,  125,  155, 40,), (125,103))
    locateTube  = my_button('Locate',   (162, 125,  155, 40,), (125,133))
    settings    = my_button('Settings', (3,  185,  155, 40,), (125,163))
    exit        = my_button('Exit',     (162, 185,  155, 40,), (125,103))
    
    screen.fill(CLOUD)

    title = Label(screen, 
                  text="Pi-Tube Ledger",
                  bg_color=PURPLE, 
                  font_color=CLOUD, 
                  font_size = 40,
                  background_size=(314, 60),
                  center=(background.get_width()/2, 60))
    sub_title = Label(screen, 
                  text="beta  ",
                  bg_color=PURPLE, 
                  font_color=CLOUD, 
                  font_size = 20,
                  background_size=(314, 25),
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
  # locate_tube(db)




  quitgame()
