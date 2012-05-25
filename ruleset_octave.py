# Rules of Octaves -- currently a dummy ruleset!

from rules import *
from music21 import interval
#import random

import logging_setup as Logging
LOG=Logging.getLogger('rules')

class octaveRule(Rule):
    def __init__(self,size): #size=1
        Rule.__init__(self)
        self.umbrella = "Rule of Octaves"
        self.size = size

        self.intervals = [False for x in range(size-1)]
        self.beats = [False for x in range(size)]
        self.harmonic_content = [False for x in range(size)]
        self.figures = ['NA' for x in range(size)]
        self.extras = [False for x in range(size)]

#* * * * Interval key:
# unison:            interval.ChromaticInterval(0)
# semitone up:       interval.ChromaticInterval(1)
# semitone down:     interval.ChromaticInterval(-1)
# tone up:           interval.ChromaticInterval(2)
# tone down:         interval.ChromaticInterval(-2)
# minor third up:    interval.ChromaticInterval(3)
# minor third down:  interval.ChromaticInterval(-3)
# major third up:    interval.ChromaticInterval(4)
# major third down:  interval.ChromaticInterval(-4)
# perfect fourth:    interval.ChromaticInterval(5)
# diminished fifth:  interval.ChromaticInterval(6)
# perfect fifth:     interval.ChromaticInterval(7)
# minor sixth:       interval.ChromaticInterval(8)
# major sixth:       interval.ChromaticInterval(9)


#* * * RULES * * *
class octave_1(octaveRule):
    """ 
    Currently a dummy rule!
    """
    def __init__(self):
        octaveRule.__init__(self,2)

        #Conditions: 
        # * When the bass note goes up
        self.intervals[0] = [interval.ChromaticInterval(1), 
                             interval.ChromaticInterval(2),
                             interval.ChromaticInterval(3),
                             interval.ChromaticInterval(4),
                             interval.ChromaticInterval(5),
                             interval.ChromaticInterval(6),
                             interval.ChromaticInterval(7),
                             interval.ChromaticInterval(8),
                             interval.ChromaticInterval(9),
                             interval.ChromaticInterval(10),
                             interval.ChromaticInterval(11)
                             ]

        #Figures:
        self.figures[0] = 'up1'
        self.figures[1] = 'up2'

class octave_2(octaveRule):
    """ 
    Currently a dummy rule!
    """
    def __init__(self):
        octaveRule.__init__(self,2)

        #Conditions: 
        # * When the bass note goes down
        self.intervals[0] = [interval.ChromaticInterval(-1), 
                             interval.ChromaticInterval(-2),
                             interval.ChromaticInterval(-3),
                             interval.ChromaticInterval(-4),
                             interval.ChromaticInterval(-5),
                             interval.ChromaticInterval(-6),
                             interval.ChromaticInterval(-7),
                             interval.ChromaticInterval(-8),
                             interval.ChromaticInterval(-9),
                             interval.ChromaticInterval(-10),
                             interval.ChromaticInterval(-11)
                             ]

        #Figures:
        self.figures[0] = 'down1'
        self.figures[1] = 'down2'