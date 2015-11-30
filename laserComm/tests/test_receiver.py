'''

'''
import unittest

from morsecodelib import text
import matplotlib.pyplot as plt

from laserComm import receiver
from laserComm import signal_processor


class TestProcessor(unittest.TestCase):
    def setUp(self):
        p = signal_processor.Processor()
        r = receiver.Receiver()
        r.load()
        p.receiver = r
        p.get_off_range()
        p.get_change_indices()
        p.get_on_bounds()
        self.p = p

    def test_get_change_indices(self):
        p = self.p
        letters_alpha = p.get_letters()
        self.assertEqual(''.join(letters_alpha), 'TRRLL')  # known answer from test data

    @unittest.skip('too plotty')
    def test_plot_spans(self):

        p = self.p
        p.receiver.plot(None)
        t = p.receiver.times
        for minI, maxI in p.on_bounds:
            span_min = t[minI]
            span_max = t[maxI]
            plt.axvspan(span_min, span_max, facecolor='g', alpha=0.5)
        plt.show()

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
