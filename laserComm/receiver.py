'''
receiver runs the ADC and photoresistor to receive an input signal.

USes MCP3008 ADC via the hardware SPI interface.

Connections are:

    MCP3008 VDD -> 3.3V (red)
    MCP3008 VREF -> 3.3V (red)
    MCP3008 AGND -> GND (orange)
    MCP3008 CLK -> SCLK (yellow)
    MCP3008 DOUT -> MISO (green)
    MCP3008 DIN -> MOSI (yellow)
    MCP3008 CS -> CE0 (red)
    MCP3008 DGND -> GND (orange)
    
The photoresistor goes from 4 kOhms (dark) to like 90 Ohms. (flashlight).
Output is 1024*Vin/Vref.  

Build a voltage divider with like a 200 Ohm resistor in series w/ the photoR and measure
Vout between them. I put photoresistor between vout and ground. 

The signal is intended to be processed using signal_processor

'''
import time

import numpy
import matplotlib
matplotlib.use('Agg')  # works headless (e.g. on Raspberry Pi)
import matplotlib.pyplot as plt
try:
    import spidev
except ImportError:
    print('no spidev')

GAP = 0.001

class ADC(object):
    """
    The Analog-to-digital converter
    """
    def __init__(self):
        self.adc = None

    def __enter__(self):
        self.adc = spidev.SpiDev()
        self.adc.open(0, 0)

    def __exit__(self, exc_type, exc_value, traceback):
        self.adc.close()

    def read(self, input_number):
        """
        read SPI data from MCP3008 chip
        
        There are 8 possible channels (0 through 7)
        
        Will return value between 0 and 1023
        """
        if ((input_number > 7) or (input_number < 0)):
            return -1

        r = self.adc.xfer2([1, (8 + input_number) << 4, 0])
        adcValue = ((r[1] & 3) << 8) + r[2]

        return adcValue

class Receiver(object):
    """
    Stream processor that uses adc
    """
    @property
    def times(self):
        return numpy.linspace(0, 10, len(self.vals))

    def receive(self, adc):
        self.vals = []
        # receive for 10 seconds
        print('Receiving')
        start = time.time()
        while time.time() - start < 30.0:
            self.vals.append(adc.read(0))
            time.sleep(GAP / 10)

    def plot(self, fname='adc.pdf'):
        print('Plotting')
        t = self.times
        plt.figure(figsize=(12, 10))
        plt.plot(t, self.vals, '-')
        plt.xlabel('Time (s)')
        plt.ylabel('ADC signal')
        plt.title('ADC Signal Trace')
        plt.grid(color='0.7')
        if fname:
            plt.savefig(fname)

    def save(self, fname='adc.txt'):
        """
        Save results to file
        """
        print('Saving')
        with open(fname, 'w') as f:
            f.writelines(['{0:04d}\n'.format(vi) for vi in self.vals])

    def load(self, fname='adc.txt'):
        print('Loading')
        with open(fname) as f:
            vals = f.readlines()
        self.vals = [float(vi) for vi in vals]


if __name__ == '__main__':
    adc = ADC()
    receiver = Receiver()
    with adc:
        vals = receiver.receive(adc)
    receiver.plot()
    receiver.save()

