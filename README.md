# Laser Communication with Morse Code

This program sends and receives text encoded with Morse code
over line-of-sight with a laser. It can be controlled by a 
Raspberry Pi or similar microcontroller. 

## Requirements
* morsecodelib (my little morse code library)
* RPi.GPIO for controlling Raspberry Pi pins
* numpy for doing some simple signal processing
* py-spidev for controlling the ADC over SPI (optional iff you update the code)
* matplotlib if you want plots

## Use
Just run clone the repo and run `transceiver.py` and it will send
and receive the pre-programmed message. This is a very early work in progress and
more usability features will be added in the future. 

There will be a blog post at http://partofthething.com/thoughts soon showing this off. 