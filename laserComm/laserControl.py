'''
Blinks the laser with Morse code. 
'''

import time

import RPi.GPIO as GPIO

import morsecodelib.sound

LED_PIN = 11

class LaserController(object):

    def __init__(self):
        pass

    def __enter__(self):
        GPIO.setmode(GPIO.BOARD)  # Number GPIOs by physical location
        GPIO.setup(LED_PIN, GPIO.OUT)
        GPIO.output(LED_PIN, GPIO.HIGH)  # Set high(+3.3V) to turn off led

    def __exit__(self, exc_type, exc_value, traceback):
        self.turnOff()
        GPIO.cleanup()

    def turnOn(self):
        GPIO.output(LED_PIN, GPIO.LOW)

    def turnOff(self):
        GPIO.output(LED_PIN, GPIO.HIGH)

class MorseRenderLaser(morsecodelib.sound.MorsePlayer):

    def __init__(self, laserController):
        self.laserController = laserController

    def _play_tone(self, durationInSeconds):
        self.laserController.turnOn()
        time.sleep(durationInSeconds)
        self.laserController.turnOff()

def testBlink():
    laser = LaserController()
    with laser:
        for _i in range(10):
            laser.turnOn()
            time.sleep(0.5)
            laser.turnOff()
            time.sleep(0.5)

def testMorse():
    laser = LaserController()
    morsecodelib.sound.config.config.WORDS_PER_MINUTE = 20
    with laser:
        morse = MorseRenderLaser(laser)
        morse.text_to_sound('What up everyone?')

if __name__ == '__main__':
    testMorse()
