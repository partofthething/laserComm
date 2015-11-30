'''
Transmit and receive in full duplex. 

This sets up threads and runs transmission and receiving at the same time. 
In this mode, a station can communicate with itself (for testing) or with another station. 

'''

import threading

import morsecodelib.sound

from laserComm import receiver
from laserComm import signal_processor
from laserComm import laserControl

DUPLEX = 0
RECEIVE_ONLY = 1
TRANSMIT_ONLY = 2

class Transceiver(object):
    def __init__(self, mode=DUPLEX):
        if mode in [DUPLEX, RECEIVE_ONLY]:
            print 'Receive mode'
            self.receive = ReceiveThread()
            self.receive.start()

        if mode in [DUPLEX, TRANSMIT_ONLY]:
            print 'Transmit mode'
            self.transmit = TransmitThread()
            self.transmit.start()

class ReceiveThread(threading.Thread):

    def run(self):
        receive = receiver.Receiver()
        adc = receiver.ADC()
        with adc:
            receive.receive(adc)
        processor = signal_processor.Processor(receive)
        processor.get_off_range()
        processor.get_change_indices()
        processor.get_on_bounds()
        print ''.join(processor.get_letters())
        receive.plot('rap.pdf')
        receive.save('rap.txt')

class TransmitThread(threading.Thread):

    def get_message(self):
        return """have you ever went over a friends house to eat
and the food just ain't no good"""
# I mean the macaroni's soggy the peas are mushed
# and the chicken tastes like wood
# so you try to play it off like you think you can
# by sayin that you're full
# and then your friend says momma he's just being polite
# he ain't finished uh uh that's bull"""

    def run(self):
        morsecodelib.sound.config.config.WORDS_PER_MINUTE = 20
        laser = laserControl.LaserController()
        with laser:
            morse = laserControl.MorseRenderLaser(laser)
            morse.text_to_sound(self.get_message())

if __name__ == '__main__':
    trans = Transceiver()
