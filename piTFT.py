import RPi.GPIO as GPIO
from RPIO import PWM
from os.path import exists
from time import sleep
import subprocess
import sys

sys.dont_write_bytecode = True


class PiTFT_Screen(object):

    def __init__(self, v2 = True, buttons = [True, True, True, True]):
        '''Initialise class.

        v2 = True - if using older (v1) revision of board this should be
        set to False to ensure button 3 works correctly.

        buttons = [button1, button2, button3, button4] if you don't want to initialise
        any of the buttons then set the appropriate flag to False. Defaults to all
        buttons being initialised.

        NB. this class does not handle debouncing of buttons.
        '''
        self.init_backlight

        self.__b1 = False
        self.__b2 = False
        self.__b3 = False
        self.__b4 = False
        self.__pin1 = 23
        self.__pin2 = 22
        self.__pin3 = 27
        self.__pin4 = 17
        # # set GPIO mode
        GPIO.setmode(GPIO.BCM)
        
        # Initialise buttons
        if buttons[0]:
            GPIO.setup(self.__pin1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.__b1 = True

        if buttons[1]:
            GPIO.setup(self.__pin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.__b2 = True

        if buttons[2]:
            if not v2:
                self.__pin3 = 21

            GPIO.setup(self.__pin3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.__b3 = True

        if buttons[3]:
            GPIO.setup(self.__pin4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.__b4 = True

    def init_backlight():
        set_pwm = 'echo pwm > /sys/class/rpi-pwm/pwm0/mode'
        set_frequency = 'echo 1000 > /sys/class/rpi-pwm/pwm0/frequency'
        set_duty = 'echo 50 > /sys/class/rpi-pwm/pwm0/duty'

        subprocess.call(set_pwm, shell=True)
        subprocess.call(set_frequency, shell=True)
        subprocess.call(set_duty, shell=True)

    def set_backlight_brightness(self, duty):
        print "brightness Changed"
        set_duty = 'echo '+str(duty)+' > /sys/class/rpi-pwm/pwm0/duty'
        subprocess.call(set_duty, shell=True)

    def backlight_off(self, *arg):
      self.set_backlight_brightness('1')

    def backlight_low(self, *arg):
      self.set_backlight_brightness('10')

    def backlight_med(self, *arg):
      self.set_backlight_brightness('25')

    def backlight_high(self, *arg):
      self.set_backlight_brightness('99')


    # Add interrupt handling...
    def Button1Interrupt(self,callback=None, bouncetime=200):
        if self.__b1: 
            GPIO.add_event_detect(self.__pin1, 
                                  GPIO.FALLING, 
                                  callback=callback, 
                                  bouncetime=bouncetime)

    def Button2Interrupt(self,callback=None, bouncetime=200):
        if self.__b2: 
            GPIO.add_event_detect(self.__pin2, 
                                  GPIO.FALLING, 
                                  callback=callback, 
                                  bouncetime=bouncetime)

    def Button3Interrupt(self,callback=None, bouncetime=200):
        if self.__b3: 
            GPIO.add_event_detect(self.__pin3, 
                                  GPIO.FALLING, 
                                  callback=callback, 
                                  bouncetime=bouncetime)

    def Button4Interrupt(self,callback=None, bouncetime=200):
        if self.__b4: 
            GPIO.add_event_detect(self.__pin4, 
                                  GPIO.FALLING, 
                                  callback=callback, 
                                  bouncetime=bouncetime)

    # Include the GPIO cleanup method
    def Cleanup(self):
        GPIO.cleanup()


    # Some properties to retrieve value state of pin and return more logical
    # True when pressed.
    @property
    def Button1(self):
        '''Returns value of Button 1. Equals True when pressed.'''
        print "Button 1"
        if self.__b1:
            return not GPIO.input(self.__pin1)

    @property
    def Button2(self):
        '''Returns value of Button 2. Equals True when pressed.'''
        print "Button 2"
        if self.__b2:
            return not GPIO.input(self.__pin2)

    @property
    def Button3(self):
        '''Returns value of Button 3. Equals True when pressed.'''
        print "Button 3"
        if self.__b3:
            return not GPIO.input(self.__pin3)

    @property
    def Button4(self):
        '''Returns value of Button 4. Equals True when pressed.'''
        print "Button 4"
        if self.__b4:
            return not GPIO.input(self.__pin4)                      


    