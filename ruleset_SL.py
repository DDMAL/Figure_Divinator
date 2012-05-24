# Rules for figuring unfigured bass parts
# Monsieur de Saint-Lambert

from figure_rules import *
#from music21 import interval
#import random

import logging_setup as Logging
LOG=Logging.getLogger('rules')

class SLRule(Rule):
    def __init__(self,size): #size=1
        Rule.__init__(self)
        self.umbrella = "Saint Lambert"
        self.size = size

        self.intervals = [False for x in range(size-1)]
        self.beats = [False for x in range(size)]
        self.harmonic_content = [False for x in range(size)]
        self.figures = ['NA' for x in range(size)]

    def show_it_off(self):
        from pprint import pprint
        pprint (vars(self))

    def check_intervals(self,chunk):
        for i in range(self.size - 2):
            #If the rule doesn't care about this note's interval, next up!
            if not self.interval[i]: continue
            #If the chunk doesn't fit this rule's interval, return false
            if chunk.interval[i] not in self.interval[i]: return False
        return True
    def check_qualities(self,chunk):
        for i in range(self.size - 1):

            #If the rule doesn't care about this note's quality, next up!
            if not self.quality[i]: continue

            
            quality = chunk.quality[i]
            rule = self.quality[i]

            #If the chunk doesn't fit this rule's quality, return false
            if chunk.quality[i] not in self.quality[i]: return False

        return True
    def check_beats(self,chunk):
        for i in range(self.size - 1):
            #If the rule doesn't care about this note's beat, next up!
            if not self.beats[i]: continue
            #If the chunk doesn't fit this rule's beat needs, return false
            if chunk.beats[i] not in self.beats[i]: return False
        return True
    def test_rule(self,chunk):
        return (check_intervals(chunk) and 
                check_qualities(chunk) and
                check_beats(chunk))
    def apply_rule(self,chunk,write='notes'):
        for i in range(self.size - 1):
            chunk.notes[i].addLyrics()
        pass

#* * * RULES * * *
class SLRule_3(SLRule):
    """When the bass note goes up by a semitone
    * First note gets a 6, second nothing."""

    #Was Konstantin's rule 1
    def __init__(self):
        SLRule.__init__(self,2)

        #"When the bass note goes up by a semitone"
        self.intervals[0] = ['up by a semitone']

        #"First note gets a 6, second nothing.""
        self.figures[0] = '6'
        self.figures[1] = 'nothing'

class SLRule_5(SLRule):
    """RULE QUOTE FOO"""

    #Was Konstantin's rule 2
    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ''

        #"FOO-quote"
        self.intervals[foo] = ['FOO']
        self.beats[foo] = ['FOO']
        self.harmonic_content[foo] = ['FOO']

        #"FOO-figures""
        self.figures[FOO] = 'FOO'

class SLRule_FOO(SLRule):
    """RULE QUOTE FOO"""

    #Was Konstantin's rule 2
    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ''

        #"FOO-quote"
        self.intervals[foo] = ['FOO']
        self.beats[foo] = ['FOO']
        self.harmonic_content[foo] = ['FOO']

        #"FOO-figures""
        self.figures[FOO] = 'FOO'

********
class SLRule_1(SLRule):

    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ""

        #"FOO-quote"
        self.intervals[foo] = ["FOO"]
        self.beats[foo] = ["FOO"]
        self.harmonic_content[foo] = ["FOO"]

        #"FOO-figures"
        self.figures[FOO] = "FOO"
class SLRule_2(SLRule):

    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ""

        #"FOO-quote"
        self.intervals[foo] = ["FOO"]
        self.beats[foo] = ["FOO"]
        self.harmonic_content[foo] = ["FOO"]

        #"FOO-figures"
        self.figures[FOO] = "FOO"
class SLRule_3(SLRule):

    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ""

        #"FOO-quote"
        self.intervals[foo] = ["FOO"]
        self.beats[foo] = ["FOO"]
        self.harmonic_content[foo] = ["FOO"]

        #"FOO-figures"
        self.figures[FOO] = "FOO"
class SLRule_4(SLRule):

    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ""

        #"FOO-quote"
        self.intervals[foo] = ["FOO"]
        self.beats[foo] = ["FOO"]
        self.harmonic_content[foo] = ["FOO"]

        #"FOO-figures"
        self.figures[FOO] = "FOO"
class SLRule_5(SLRule):

    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ""

        #"FOO-quote"
        self.intervals[foo] = ["FOO"]
        self.beats[foo] = ["FOO"]
        self.harmonic_content[foo] = ["FOO"]

        #"FOO-figures"
        self.figures[FOO] = "FOO"
class SLRule_6(SLRule):

    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ""

        #"FOO-quote"
        self.intervals[foo] = ["FOO"]
        self.beats[foo] = ["FOO"]
        self.harmonic_content[foo] = ["FOO"]

        #"FOO-figures"
        self.figures[FOO] = "FOO"
class SLRule_7(SLRule):

    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ""

        #"FOO-quote"
        self.intervals[foo] = ["FOO"]
        self.beats[foo] = ["FOO"]
        self.harmonic_content[foo] = ["FOO"]

        #"FOO-figures"
        self.figures[FOO] = "FOO"
class SLRule_8(SLRule):

    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ""

        #"FOO-quote"
        self.intervals[foo] = ["FOO"]
        self.beats[foo] = ["FOO"]
        self.harmonic_content[foo] = ["FOO"]

        #"FOO-figures"
        self.figures[FOO] = "FOO"
class SLRule_9(SLRule):

    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ""

        #"FOO-quote"
        self.intervals[foo] = ["FOO"]
        self.beats[foo] = ["FOO"]
        self.harmonic_content[foo] = ["FOO"]

        #"FOO-figures"
        self.figures[FOO] = "FOO"
class SLRule_10(SLRule):

    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ""

        #"FOO-quote"
        self.intervals[foo] = ["FOO"]
        self.beats[foo] = ["FOO"]
        self.harmonic_content[foo] = ["FOO"]

        #"FOO-figures"
        self.figures[FOO] = "FOO"
class SLRule_11(SLRule):

    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ""

        #"FOO-quote"
        self.intervals[foo] = ["FOO"]
        self.beats[foo] = ["FOO"]
        self.harmonic_content[foo] = ["FOO"]

        #"FOO-figures"
        self.figures[FOO] = "FOO"
class SLRule_12(SLRule):

    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ""

        #"FOO-quote"
        self.intervals[foo] = ["FOO"]
        self.beats[foo] = ["FOO"]
        self.harmonic_content[foo] = ["FOO"]

        #"FOO-figures"
        self.figures[FOO] = "FOO"
class SLRule_13(SLRule):

    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ""

        #"FOO-quote"
        self.intervals[foo] = ["FOO"]
        self.beats[foo] = ["FOO"]
        self.harmonic_content[foo] = ["FOO"]

        #"FOO-figures"
        self.figures[FOO] = "FOO"
class SLRule_14(SLRule):

    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ""

        #"FOO-quote"
        self.intervals[foo] = ["FOO"]
        self.beats[foo] = ["FOO"]
        self.harmonic_content[foo] = ["FOO"]

        #"FOO-figures"
        self.figures[FOO] = "FOO"
class SLRule_15(SLRule):

    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ""

        #"FOO-quote"
        self.intervals[foo] = ["FOO"]
        self.beats[foo] = ["FOO"]
        self.harmonic_content[foo] = ["FOO"]

        #"FOO-figures"
        self.figures[FOO] = "FOO"
class SLRule_16(SLRule):

    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ""

        #"FOO-quote"
        self.intervals[foo] = ["FOO"]
        self.beats[foo] = ["FOO"]
        self.harmonic_content[foo] = ["FOO"]

        #"FOO-figures"
        self.figures[FOO] = "FOO"
class SLRule_17(SLRule):

    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ""

        #"FOO-quote"
        self.intervals[foo] = ["FOO"]
        self.beats[foo] = ["FOO"]
        self.harmonic_content[foo] = ["FOO"]

        #"FOO-figures"
        self.figures[FOO] = "FOO"
class SLRule_18(SLRule):

    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ""

        #"FOO-quote"
        self.intervals[foo] = ["FOO"]
        self.beats[foo] = ["FOO"]
        self.harmonic_content[foo] = ["FOO"]

        #"FOO-figures"
        self.figures[FOO] = "FOO"
class SLRule_19(SLRule):

    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ""

        #"FOO-quote"
        self.intervals[foo] = ["FOO"]
        self.beats[foo] = ["FOO"]
        self.harmonic_content[foo] = ["FOO"]

        #"FOO-figures"
        self.figures[FOO] = "FOO"
class SLRule_20(SLRule):

    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ""

        #"FOO-quote"
        self.intervals[foo] = ["FOO"]
        self.beats[foo] = ["FOO"]
        self.harmonic_content[foo] = ["FOO"]

        #"FOO-figures"
        self.figures[FOO] = "FOO"
class SLRule_21(SLRule):

    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ""

        #"FOO-quote"
        self.intervals[foo] = ["FOO"]
        self.beats[foo] = ["FOO"]
        self.harmonic_content[foo] = ["FOO"]

        #"FOO-figures"
        self.figures[FOO] = "FOO"
class SLRule_22(SLRule):

    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ""

        #"FOO-quote"
        self.intervals[foo] = ["FOO"]
        self.beats[foo] = ["FOO"]
        self.harmonic_content[foo] = ["FOO"]

        #"FOO-figures"
        self.figures[FOO] = "FOO"
class SLRule_23(SLRule):

    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ""

        #"FOO-quote"
        self.intervals[foo] = ["FOO"]
        self.beats[foo] = ["FOO"]
        self.harmonic_content[foo] = ["FOO"]

        #"FOO-figures"
        self.figures[FOO] = "FOO"
class SLRule_24(SLRule):

    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ""

        #"FOO-quote"
        self.intervals[foo] = ["FOO"]
        self.beats[foo] = ["FOO"]
        self.harmonic_content[foo] = ["FOO"]

        #"FOO-figures"
        self.figures[FOO] = "FOO"
class SLRule_25(SLRule):

    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ""

        #"FOO-quote"
        self.intervals[foo] = ["FOO"]
        self.beats[foo] = ["FOO"]
        self.harmonic_content[foo] = ["FOO"]

        #"FOO-figures"
        self.figures[FOO] = "FOO"
class SLRule_26(SLRule):

    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ""

        #"FOO-quote"
        self.intervals[foo] = ["FOO"]
        self.beats[foo] = ["FOO"]
        self.harmonic_content[foo] = ["FOO"]

        #"FOO-figures"
        self.figures[FOO] = "FOO"
class SLRule_27(SLRule):

    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ""

        #"FOO-quote"
        self.intervals[foo] = ["FOO"]
        self.beats[foo] = ["FOO"]
        self.harmonic_content[foo] = ["FOO"]

        #"FOO-figures"
        self.figures[FOO] = "FOO"
class SLRule_28(SLRule):

    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ""

        #"FOO-quote"
        self.intervals[foo] = ["FOO"]
        self.beats[foo] = ["FOO"]
        self.harmonic_content[foo] = ["FOO"]

        #"FOO-figures"
        self.figures[FOO] = "FOO"
class SLRule_29(SLRule):

    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ""

        #"FOO-quote"
        self.intervals[foo] = ["FOO"]
        self.beats[foo] = ["FOO"]
        self.harmonic_content[foo] = ["FOO"]

        #"FOO-figures"
        self.figures[FOO] = "FOO"
class SLRule_30(SLRule):

    def __init__(self):
        SLRule.__init__(self,FOO)
        self.todo = ""

        #"FOO-quote"
        self.intervals[foo] = ["FOO"]
        self.beats[foo] = ["FOO"]
        self.harmonic_content[foo] = ["FOO"]

        #"FOO-figures"
        self.figures[FOO] = "FOO"
