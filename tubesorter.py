import pygame, os, time, random, sys, eztext, databaseFunctions
from tubesorter_UI import *
from font import *
import RPi.GPIO as GPIO
from piTFT import PiTFT_GPIO



pitft = PiTFT_GPIO()

def backlight_Off(argument):
    pitft.Backlight(False)
def backlight_On(argument):
  pitft.Backlight(True)

pitft.Button4Interrupt(backlight_On)
pitft.Button3Interrupt(backlight_Off)

sys.dont_write_bytecode = True




os.putenv("SDL_FBDEV", "/dev/fb1")
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
pygame.init()

display_width = 320
display_height = 240

pygame.mouse.set_visible(False)

debug = False
if debug:
   pygame.mouse.set_visible(True)
   debug_rect = pygame.Rect(270, 0, 50, 35)

fontMgr = cFontManager(((None, 24), (None, 48), ('DejaVu Sans', 24), ('Droid Sans Mono', 12), ('Droid Sans', 16), ('DejaVu Sans Mono', 12), ('DejaVu Sans', 16)))
screen = pygame.display.set_mode((display_width, display_height))
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
   txtbx = eztext.Input(maxlength=20, color=asphalt, prompt='Accn#: ', x=0, y=0)
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
         elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            for btn in keyboard:
               if btn.obj.collidepoint(mouse):
                  inp = inp + btn.value
                  txtbx.value = inp
            if enter.obj.collidepoint(mouse):
               pygame.mouse.set_pos(0,0)
               screen.fill(cloud)
               return txtbx.value
            if exit.obj.collidepoint(mouse):
               pygame.mouse.set_pos(0,0)
               screen.fill(cloud)
               return
      accn = txtbx.update(events)
      txtbx.draw(screen)

      pygame.display.flip()
      pygame.event.wait

def file_tube():
    pygame.mouse.set_pos(0,0)
    screen.fill(cloud)
    mouse = pygame.mouse.get_pos()


    title_rect = pygame.Rect(0, 25, 320, 50)
    accn = ''
    txtbx = eztext.Input(maxlength=20, color=asphalt, prompt='Accn#: ', x=0, y=95)
    exit= my_button('Exit', (170, 185,  130, 40,), (125,103))
    OSk_BTN = my_button('Keyboard', (20,  185,  130, 40,), (125,163))

    subtitle_rect = pygame.Rect(0, 75, 320, 20)
    lastFiled_rect = pygame.Rect(0, 0, 320, 20)
    accn_rect = (0, 95, 320, 30)

    update_Rects = [subtitle_rect, lastFiled_rect, title_rect, accn_rect]


    OSk_BTN.draw(screen, mouse)
    exit.draw(screen, mouse)
    pygame.display.update()

    run = True
    while run:
        events = pygame.event.get()
        lastFiled = databaseFunctions.lastFiled()
        accn = txtbx.update(events)
        
        
        loc = databaseFunctions.locateNext()
        pygame.draw.rect(screen, purple, subtitle_rect)
        location = loc[3] + loc[0] + ": " + ROWS[loc[2]]  + "-" + loc[1]


        pygame.draw.rect(screen, cloud, lastFiled_rect)
        fontMgr.Draw(screen, 'Droid Sans', 16, "Last Filed: " + str(lastFiled[3]) , lastFiled_rect, purple, "left", "center")
        # fontMgr.Draw(screen, 'Droid Sans', 16, "Last Filed: ", lastFiled_rect, purple, "left", "center")
        
        fontMgr.Draw(screen, 'Droid Sans', 16, "Location:", subtitle_rect, cloud, 'left', 'center')
        pygame.draw.rect(screen, cloud, accn_rect)
        
        

        pygame.draw.rect(screen, cloud, accn_rect)
        txtbx.draw(screen)
        pygame.draw.rect(screen, purple, title_rect)
        fontMgr.Draw(screen, 'DejaVu Sans', 24, 'File Tube', title_rect, cloud, 'center', 'center')
        pygame.draw.rect(screen, purple, subtitle_rect)
        fontMgr.Draw(screen, 'Droid Sans Mono', 12, location, subtitle_rect, cloud, 'center', 'center')
        


        pygame.display.update(update_Rects)
        pygame.event.wait
        for event in events:
             if event.type == pygame.QUIT:
                run = False
             elif event.type == pygame.KEYDOWN:
                if event.key == K_RETURN: 
                  databaseFunctions.fileAccn(accn)
                  txtbx.value = ''
             elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if exit.obj.collidepoint(mouse):
                   pygame.mouse.set_pos(0,0)
                   screen.fill(cloud)
                   return
                elif OSk_BTN.obj.collidepoint(mouse):
                    accn = osk()
                    databaseFunctions.fileAccn(accn)
                    txtbx.value = ''
                    OSk_BTN.draw(screen, mouse)
                    exit.draw(screen, mouse)
                    pygame.display.update()
def locate_tube():
 pass


def main_menu():
   fileTube    = my_button('File',     (20,  125,  130, 40,), (125,103))
   locateTube  = my_button('Locate',   (170, 125,  130, 40,), (125,133))
   settings    = my_button('Settings', (20,  185,  130, 40,), (125,163))
   exit        = my_button('Exit',     (170, 185,  130, 40,), (125,103))
   # screen_surface = pygame.display.get_surface()

   screen.fill(cloud)

   title_rect = pygame.Rect(0, 25, 320, 50)
   subtitle_rect = pygame.Rect(0, 75, 320, 20)


   while True:
      mouse = pygame.mouse.get_pos()
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            return
         elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if fileTube.obj.collidepoint(mouse):
               print('file pressed')
               file_tube()
            elif locateTube.obj.collidepoint(mouse):
               print('locate pressed')
               locate_tube()
            elif settings.obj.collidepoint(mouse):
               print('settings pressed')
               osk()
            elif exit.obj.collidepoint(mouse):
               print('exit pressed')
               return

      pygame.draw.rect(screen, purple, title_rect)
      fontMgr.Draw(screen, 'DejaVu Sans', 24, 'Tube Sorter', title_rect, cloud, 'center', 'center')

      pygame.draw.rect(screen, purple, subtitle_rect)
      fontMgr.Draw(screen, 'DejaVu Sans', 16, 'Version 1.0b', subtitle_rect, cloud, 'right', 'top')

      if debug: draw_FPS(screen, debug_rect, fontMgr, clock)

      fileTube.draw(    screen, mouse)
      locateTube.draw(  screen, mouse)
      settings.draw(    screen, mouse)
      exit.draw(        screen, mouse)
      
      pygame.display.flip()
      # pygame.display.update()
      pygame.event.wait

if __name__ == '__main__':
   main_menu()
   quitgame()
