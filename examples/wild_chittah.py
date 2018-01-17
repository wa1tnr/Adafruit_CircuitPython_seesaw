
# The wild chitta

# CircuitPython version - tested on Metro M0 Express
# Wed Jan 17 17:39:27 UTC 2018
# Pin 6 - Servo motor

from board import *
import busio
import adafruit_seesaw
import time


print("do: import main;main.looping() CR  << HOWTO run this program in REPL")

myI2C = busio.I2C(SCL, SDA)

ss = adafruit_seesaw.Seesaw(myI2C)


global calmer
global servoPinA
global hiDutyCy
global loDutyCy
global dutyCy

# calmer = 0.001   # not calm at all.  Increase for more calm-ness
calmer = 0.2

servoPinA = 6
hiDutyCy = -1
loDutyCy = -1
dutyCy = -1

def scale16():
    global hiDutyCy
    global loDutyCy
    hiDutyCy = dutyCy >> 8
    loDutyCy = dutyCy & 0xFF

def tryiv():
        global dutyCy
        dutyCy   = 1800 # 16-bit value is easier to specify what you want as a scalar
        freq = 45   # 50 Hz would be ideal but Seesaw produces 45 Hz instead

        scale16()       # whenever you change dutyCy, convert it with scale16()

        ss.setPWMFreq(servoPinA, freq);
        time.sleep(0.1)
        
        ss.analog_write(servoPinA, hiDutyCy, loDutyCy, 16)
        time.sleep(.1)
        time.sleep(calmer)

def iterate():
    global dutyCy
    while True:

        # WIND
        for dCycle in range(1800, 7000, 200):
            dutyCy = dCycle
            scale16()

            ss.analog_write(servoPinA, hiDutyCy, loDutyCy, 16)
            time.sleep(.09)
            time.sleep(calmer)

        # REWIND
        for dCycle in range(7000, 1800, -1200): # much faster rewind
            dutyCy = dCycle
            scale16()

            ss.analog_write(servoPinA, hiDutyCy, loDutyCy, 16)
            time.sleep(.09)
            time.sleep(calmer)

def cleanup():
    time.sleep(1.1) 
    time.sleep(.004) # be nice to others

ss.sw_reset()
time.sleep(.6)
tryiv() # do a single iteration
iterate() # do many ierations
# cleanup() # never seen as the while True captures
# end
