# Rules of Octaves -- currently a dummy ruleset!

from rules import Rule
from music21 import interval
from music21.figuredBass import notation

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


def all_rules():
    """
    All rules available in the octave ruleset
    """
    allrules=[
        octave_1(),
        octave_2()
        ]
    return allrules


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
        self.figures[0] = notation.Notation('+')
        self.figures[1] = notation.Notation('++')

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
        self.figures[0] = notation.Notation('-')
        self.figures[1] = notation.Notation('--')