#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import subprocess

GPIO.setmode(GPIO.BCM)

# set button 2 as input, with pull-up resistor
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

oldButtonState = True
while True:
    buttonState = GPIO.input(22)

    if buttonState != oldButtonState and buttonState == False :
        # print "Button 1 pressed"
        subprocess.call("/home/pi/toggle-backlight.sh", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    oldButtonState = buttonState
    time.sleep(.1)