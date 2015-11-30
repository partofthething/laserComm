"""
Processes signal received from receiver and turns it into text

To read, it's best to just look at the high voltage timing. Shake in the "on" signal
means it's best to just figure out when the signal is off (high voltage) and do timing from that. 

"""
import numpy

from morsecodelib import text

class Processor(object):
    """
    process the input signal 
    
    Converts pulse timing into morse code and then text.  
    """
    def __init__(self, receiver=None):
        self.receiver = receiver
        self.change_indices = None

    def get_off_range(self):
        """
        Use a histogram to determine when the signal should be considered on and when off
        
        Requires constant ambient lighting conditions. 
        
        sets Min and max bounds of the values where the signal should be considered off. 
        All other signals are "on". 
        """
        _hist, bin_edges = numpy.histogram(self.receiver.vals, bins=6)
        self.off_min = bin_edges[-2]
        self.off_max = bin_edges[-1]

    @property
    def first_is_on(self):
        return self.is_on(self.receiver.vals[0])

    def is_on(self, sample):
        """
        On when value is not in the (high voltage) off-range. 
        """
        return not self.off_min <= sample <= self.off_max

    def get_change_indices(self):
        """
        Figure out for how long the signal was on.
        
        Really we need to know the on and off durations to separate words and letters. 
        Long off = new word. We should just figure out the average dit length and go from 
        there with error bounds around it. Though when the computer sends, timing should
        be pretty precise. 
        """
        previous_was_on = self.first_is_on
        self.change_indices = []
        prevRecorded = 0
        for i, val in enumerate(self.receiver.vals):
            on = self.is_on(val)
            if (on and not previous_was_on) or (not on and previous_was_on):
                if i - prevRecorded < 10:
                    # spurious signal. skip it.
                    continue
                # it just changed state. Record.
                self.change_indices.append(i)
                prevRecorded = i
            previous_was_on = on

    def get_on_bounds(self):
        """
        Gets lists of tuples of indices where the light was on
        """
        self.on_bounds = []
        first_on = self.first_is_on
        previous_index = 0
        for i, change_index in enumerate(self.change_indices):
            if (first_on and not i % 2) or (not first_on and i % 2):
                self.on_bounds.append((previous_index, change_index))
            previous_index = change_index
        # print self.change_indices

    def get_letters(self):
        on_durations = numpy.array([off - on for on, off in self.on_bounds])

        # print on_durations
        # anything in first bound interval is considered short. Otherwise, it's long.
        # Use 3 bins and call the smallest one dits. This is because humans vary the longs more.
        _hist, bounds_edges = numpy.histogram(on_durations, bins=9)
        dit_cutoff = bounds_edges[4]
        dit_durations = [od for od in on_durations if od < dit_cutoff]
        dit = numpy.average(dit_durations)

        # split bounds into letters_morse based on a gap of like 3+ dits.
        letters_morse = []
        thisLetter = []
        lastOff = 0.0
        for (on, off), duration in zip(self.on_bounds, on_durations):
            if on - lastOff >= dit * 3:
                letters_morse.append(''.join(thisLetter))
                thisLetter = []

            if duration < dit_cutoff:
                thisLetter.append('.')
            else:
                thisLetter.append('-')
            lastOff = off

        # don't forget leftover
        if thisLetter:
            letters_morse.append(''.join(thisLetter))

        letters_alpha = [text.code_to_text(ltr) for ltr in letters_morse]
        return letters_alpha


if __name__ == '__main__':
    pass
