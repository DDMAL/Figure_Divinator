# Rules for figuring unfigured bass parts
# Monsieur de Saint-Lambert

from figure_rules import *
from music21 import interval
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
        self.extras = [False for x in range(size)]

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

#* * * * Interval key:
# unison:            interval.ChromaticInterval(0)
# semitone up:       interval.ChromaticInterval(1)
# semitone down:     interval.ChromaticInterval(-1)
# tone up:           interval.ChromaticInterval(2)
# tone down:         interval.ChromaticInterval(-2)
# minor third up:    interval.ChromaticInterval(3)
# minor third down:  interval.ChromaticInterval(-3)


#* * * RULES * * *
class SLRule_3(SLRule):
    """ 
    K's rule:   1
    Page:       45
    Conditions: 
        * When the bass note goes up by a semitone
    Figures:
        * First note gets a 6
        * Second gets nothing.
    """
    def __init__(self):
        SLRule.__init__(self,2)

        #Conditions: 
        # * When the bass note goes up by a semitone
        self.intervals[0] = [interval.ChromaticInterval(1)]

        #Figures:
        self.figures[0] = '6'
        self.figures[1] = 'nothing'


class SLRule_5(SLRule):
    """
    K's rule:   2
    Page:       46
    Conditions: 
        * When bass note goes down by a semitone
        * second note is a perfect chord (major triad) 
        * second note is on beat 1
    Figures:
        * First note gets a 6
    """
    def __init__(self):
        SLRule.__init__(self,2)
        self.todo = ''

        #Conditions
        self.intervals[0] = [interval.ChromaticInterval(-1)]
        self.beats[1] = [1]
        self.harmonic_content[1] = ['perfect chord (major triad)']

        #Figures"
        self.figures[0] = '6'


class SLRule_6(SLRule):
    """
    K's rule:   3
    Page:       46
    Conditions: 
        * bass note goes up by a semitone
        * the first note has a #6
    Figures:
        * Second note gets a 6
    """

    def __init__(self):
        SLRule.__init__(self,2)
        self.todo = ""

        #Conditions:
        self.intervals[0] = [interval.ChromaticInterval(1)]
        self.harmonic_content[0] = ["has #6"]

        #Figures:
        self.figures[1] = "6"


class SLRule_7(SLRule):
    """
    K's rule:   4
    Page:       47
    Conditions: 
        * Bass note goes down by a minor 3rd
        * First chord is perfect
    Figures:
        * Second gets false fifth (no figure)
    """

    def __init__(self):
        SLRule.__init__(self,2)
        self.todo = ""

        #Conditions
        self.intervals[0] = ["down by minor 3rd"]
        self.harmonic_content[0] = ["perfect"]

        #Figures
        self.figures[1] = "false fifth (no figure)"


class SLRule_8(SLRule):
    """
        K's rule:   NA
        Page:       47
        Conditions: 
            * bass descends minor third, either directly or with intervening step, 
        Figures:
            * the second chord maintains the minor third
    """
    def __init__(self):
        SLRule.__init__(self,2)
        self.todo = ""

        #Conditions
        self.intervals[0] = ["minor third"]

        #Figures
        self.figures[1] = "maintains the minor third"


class SLRule_9(SLRule):
    """
    K's rule:   NA
    Page:       47
    Conditions: 
        * bass note rises by a minor third, either directly or with an intervening passing tone,
    Figures:
        * first chord should have a minor third
    """

    def __init__(self):
        SLRule.__init__(self,2)
        self.todo = ""

        #Conditions
        self.intervals[0] = ["rises minor third"]

        #Figures
        self.figures[0] = "minor third"


class SLRule_10a(SLRule):
    """
    K's rule:   NA
    Page:       ?
    Conditions: 
        * bass descends major third, either directly or with intervening step, 
    Figures:
        * the second chord maintains the major third
    """

    def __init__(self):
        SLRule.__init__(self,2)
        self.todo = ""

        #Conditions
        self.intervals[0] = ["down major third"]

        #Figures
        self.figures[1] = "maintains the major third"


class SLRule_10b(SLRule):
    """
    K's rule:   NA
    Page:       ?
    Conditions: 
        * bass note rises by a major third, either directly or with an intervening passing tone,
    Figures:
        * first chord should have a major third
    """

    def __init__(self):
        SLRule.__init__(self,2)
        self.todo = ""

        #Conditions
        self.intervals[0] = ["rises major third"]

        #Figures
        self.figures[0] = "major 3"


class SLRule_11(SLRule):
    """
    K's rule:   5
    Page:       47
    Conditions: 
        * bass note goes down by a 3rd, (either major or minor)
        * first chord is a perfect major triad {this case: could have a seven}
    Figures:
        * second gets a 6
    """

    def __init__(self):
        SLRule.__init__(self,2)
        self.todo = ""

        #Conditions
        self.intervals[0] = ["down maj or min 3rd"]
        self.harmonic_content[0] = ["perfect major triad, 7 okay"]

        #Figures
        self.figures[1] = "6"


class SLRule_12(SLRule):
    """
    K's rule:   6
    Page:       48
    Conditions: 
        * bass note descends by a false 5th (aka tritone aka diminished fifth)
    Figures:
        * 2nd note has a flat fifth
    """

    def __init__(self):
        SLRule.__init__(self,2)
        self.todo = ""

        #Conditions
        self.intervals[0] = ["down diminished fifth"]

        #Figures
        self.figures[1] = "flat fifth"


class SLRule_13(SLRule):
    """
    K's rule:   7
    Page:       48
    Conditions: 
        * bass note goes up by a 3rd or DOWN by 6th (of any kind)
    Figures:
        * Second note gets a 6
    """

    def __init__(self):
        SLRule.__init__(self,2)
        self.todo = ""

        #Conditions
        self.intervals[0] = ["up by 3rd or down by 6th of any kind"]

        #Figures
        self.figures[1] = "6"


class SLRule_14(SLRule):
    """
    K's rule:   8
    Page:       48
    Conditions: 
        * When bass note goes up 3 consecutive tones (MUST BE SEMITONE OR TONE)
        * 3rd chord is perfect major triad, no("unlikely") 7
    Figures:
        * 1st note gets a 6
        * 2nd note gets a 65(minor3)
        * 3rd note gets a major chord (no figure)(5,#)
    """

    def __init__(self):
        SLRule.__init__(self,3)
        self.todo = ""

        #Conditions
        self.intervals[0] = [interval.ChromaticInterval(1),interval.ChromaticInterval(2)]
        self.intervals[1] = [interval.ChromaticInterval(1),interval.ChromaticInterval(2)]
        self.harmonic_content[2] = ["perfect major triad, no 7"]

        #Figures
        self.figures[0] = "6"
        self.figures[1] = "65(minor3)"
        self.figures[2] = "major chord (no figure)(5,#)"


class SLRule_15(SLRule):
    """
    K's rule:   9
    Page:       49
    Conditions: 
        * When bass note goes down 2 consecutive whole tone steps (3 notes!) 
        * first chord is perfect major triad (7 is fine)
    Figures:
        * 2nd gets '-' or 6/4+/2
        * 3rd gets a 6
    """
    def __init__(self):
        SLRule.__init__(self,3)
        self.todo = ""

        #Conditions
        self.intervals[0] = [interval.ChromaticInterval(-2)]
        self.intervals[1] = [interval.ChromaticInterval(-2)]
        self.harmonic_content[0] = ["perfect major triad 7 okay"]

        #Figures
        self.figures[1] = "- or 6/4+/2"
        self.figures[2] = "6"


class SLRule_16(SLRule):
    """
    K's rule:   10
    Page:       49
    Conditions: 
        * bass note goes down 2 consecutive whole tone steps 
        * first chord is perfect major OR minor triad (no 7)
        * third note has a 7 
    Figures:
        * 1st gets no figure
        * Second gets '-'
        * Third gets a 7
    """

    def __init__(self):
        SLRule.__init__(self,3)
        self.todo = ""

        #Conditions
        self.intervals[0] = [interval.ChromaticInterval(-2)]
        self.intervals[1] = [interval.ChromaticInterval(-2)]
        self.harmonic_content[0] = ["perfect major or minor triad no 7"]
        self.harmonic_content[2] = ["has 7"]

        #Figures
        self.figures[0] = "no figure"
        self.figures[1] = "-"
        self.figures[2] = "7"


class SLRule_17(SLRule):
    """
    K's rule:   11
    Page:       ?
    Conditions: 
        * When bass note goes down by a major/minor 3rd
        * [second interval] up a whole tone 
        * third chord is major 
        * third chord is on first beat
    Figures:
        * 2nd gets a 6
    """

    def __init__(self):
        SLRule.__init__(self,3)
        self.todo = ""

        #Conditions
        self.intervals[0] = ["down major/min 3"]
        self.intervals[1] = [interval.ChromaticInterval(2)]
        self.harmonic_content[2] = ["major"]
        self.beats[2] = ["on first beat"]

        #Figures
        self.figures[1] = "6"


class SLRule_18(SLRule):
    """
    K's rule:   12
    Page:       50
    Conditions: 
        * When bass note goes down a minor 3rd
        * [second interval] then goes up a semitone 
        * third note is on a downbeat
    Figures:
        * 1st gets perfect major triad (#)
        * 2nd gets a 6
        * 3rd gets perfect major triad (#)
    """

    def __init__(self):
        SLRule.__init__(self,3)
        self.todo = ""

        #Conditions
        self.intervals[0] = ["down a minor 3rd"]
        self.intervals[1] = [interval.ChromaticInterval(1)]
        self.beats[2] = ["downbeat"]

        #Figures
        self.figures[0] = "perfect major triad (#)"
        self.figures[1] = "6"
        self.figures[2] = "perfect major triad (#)"


class SLRule_19(SLRule):
    """
    K's rule:   14
    Page:       50
    Conditions: 
        * When bass note goes down a major 3rd
        * [second interval] up a 4th
        * first chord has a diminished 5
    Figures:
        * 2nd note gets a 7
        * 3rd note gets perfect triad (no figure)
    """

    def __init__(self):
        SLRule.__init__(self,3)
        self.todo = ""

        #Conditions
        self.intervals[0] = ["down major third"]
        self.intervals[1] = ["up a 4th"]
        self.harmonic_content[0] = ["has a diminished 5"]

        #Figures
        self.figures[1] = "7"
        self.figures[2] = "perfect triad (no figure)"


class SLRule_20(SLRule):
    """
    K's rule:   13
    Page:       50
    Conditions: 
        * When bass note goes up a semitone
        * [second interval] then goes up a 5th or down a 4th 
        * third note on 1st beat
    Figures:
        * 1st gets 6 b5
        * 2nd perfect triad (major or minor) OR a six chord (SOOOOOOO 5(6)/3)
        * 3rd perfect major chord (5,#)
    """

    def __init__(self):
        SLRule.__init__(self,3)
        self.todo = ""

        #Conditions
        self.intervals[0] = [interval.ChromaticInterval(1)]
        self.intervals[1] = ["up 5th or down 4th"]
        self.beats[2] = ["first beat"]

        #Figures
        self.figures[0] = "6 b5"
        self.figures[1] = "perfect triad (maj or minor) OR a six chord (5(6)/3)"
        self.figures[2] = "perfect major chord (5,#)"


class SLRule_21(SLRule):
    """
    K's rule:   15
    Page:       51
    Conditions: 
        * [first interval] bass remains same for two notes
        * [second interval] then up a 5th 
        * 3rd note is on 1st beat
    Figures:
        * 1st note gets perfect triad
        * 2nd note gets a 6
        * 3rd note gets perfect triad
    """
    def __init__(self):
        SLRule.__init__(self,3)
        self.todo = ""

        #Conditions
        self.intervals[0] = [interval.ChromaticInterval(0)]
        self.intervals[1] = ["up 5th"]
        self.beats[2] = ["1st beat"]

        #Figures
        self.figures[0] = "perfect triad"
        self.figures[1] = "6"
        self.figures[2] = "perfect triad"


class SLRule_22(SLRule):
    """
    K's rule:   16
    Page:       51
    Conditions: 
        * When bass note remains same for two notes
        * [second interval] then goes down a 4th
        * first chord is a perfect major triad (no 7)
        * third note is on the 1st beat
    Figures:
        * 1st gets 53
        * 2nd gets a 64+ (6#4) 
        * 3rd gets 53
    """
    def __init__(self):
        SLRule.__init__(self,3)
        self.todo = ""

        #Conditions
        self.intervals[0] = [interval.ChromaticInterval(0)]
        self.intervals[1] = ["down a 4th"]
        self.harmonic_content[0] = ["perfect major triad (no 7)"]
        self.beats[2] = ["1st beat"]

        #Figures
        self.figures[0] = "53"
        self.figures[1] = "64+ (6#4)"
        self.figures[2] = "53"


class SLRule_23(SLRule):
    """
    K's rule:   17
    Page:       51
    Conditions: 
        * When bass note goes up a tone
        * [second interval] then up a tone
        * [third interval] then up a semitone (sol la si ut) 
        * last note is on 1st beat
    Figures:
        * 1st note gets (53)
        * 2nd note gets a 6
        * 3rd note gets (6 5/)(six flat five)
        * 4th note gets (53)
    """
    def __init__(self):
        SLRule.__init__(self,4)
        self.todo = ""

        #Conditions
        self.intervals[0] = [interval.ChromaticInterval(2)]
        self.intervals[1] = [interval.ChromaticInterval(2)]
        self.intervals[2] = [interval.ChromaticInterval(1)]
        self.beats[3] = ["1st beat"]

        #Figures
        self.figures[0] = "53"
        self.figures[1] = "6"
        self.figures[2] = "6 flat5"
        self.figures[3] = "53"


class SLRule_24maybe(SLRule):
    """
    K's rule:   18
    Page:       xx
    Conditions: 
        * bass note goes down a semitone
        * [second interval] then down a tone
        * [third interval] then down a tone 
        * last note is on 1st beat
    Figures:
        * 1st note gets no figure
        * 2nd note gets a 6
        * 3rd note gets #6
        * 4th note gets no figure
    """

    def __init__(self):
        SLRule.__init__(self,4)
        self.todo = "TBD"

        #Conditions
        self.intervals[0] = [interval.ChromaticInterval(-1)]
        self.intervals[1] = [interval.ChromaticInterval(-2)]
        self.intervals[2] = [interval.ChromaticInterval(-2)]
        self.beats[3] = ["1st beat"]

        #Figures
        self.figures[0] = "no figure"
        self.figures[1] = "6"
        self.figures[2] = "#6"
        self.figures[3] = "no figure"


class SLRule_25maybe(SLRule):
    """
    K's rule:   19
    Page:       xx
    Conditions: 
        * When bass note goes down a tone, 
        * [second interval] then down a semitone
        * [third interval] then down a tone
    Figures:
        * 1st note gets no figure
        * 2nd note get a '-'
        * 3rd note gets a #6
        * 4th note gets no figure
    """

    def __init__(self):
        SLRule.__init__(self,4)
        self.todo = ""

        #Conditions
        self.intervals[0] = [interval.ChromaticInterval(-2)]
        self.intervals[1] = [interval.ChromaticInterval(-1)]
        self.intervals[2] = [interval.ChromaticInterval(-2)]

        #Figures
        self.figures[0] = "no figure"
        self.figures[1] = "-"
        self.figures[2] = "#6"
        self.figures[3] = "no figure"


class SLRule_26maybe(SLRule):
    """
    K's rule:   20
    Page:       xx
    Conditions: 
        * bass note goes down a tone
        * [second interval] then down a tone
        * [third interval] then down a semitone
    Figures:
        * 1st note gets no figure
        * 2nd note gets no figure
        * 3rd note gets a 6
        * 4th note gets no figure
    """

    def __init__(self):
        SLRule.__init__(self,4)
        self.todo = ""

        #Conditions
        self.intervals[0] = [interval.ChromaticInterval(-2)]
        self.intervals[1] = [interval.ChromaticInterval(-2)]
        self.intervals[2] = [interval.ChromaticInterval(-1)]

        #Figures
        self.figures[0] = "no figure"
        self.figures[1] = "no figure"
        self.figures[2] = "6"
        self.figures[3] = "no figure"


class SLRule_27maybe(SLRule):
    """
    K's rule:   21
    Page:       xx
    Conditions: 
        * When bass note goes down a tone
        * [second interval] then down a semitone
        * [third interval] then down a tone
        * [fourth interval] then down a tone
    Figures:
        * 1st note gets no figure
        * 2nd note gets a 6#42 or just '-'
        * 3rd gets a 6
        * 4th gets a 6
        * 5th gets no figure
    """

    def __init__(self):
        SLRule.__init__(self,5)
        self.todo = ""

        #Conditions
        self.intervals[0] = [interval.ChromaticInterval(-2)]
        self.intervals[1] = [interval.ChromaticInterval(-1)]
        self.intervals[2] = [interval.ChromaticInterval(-2)]
        self.intervals[3] = [interval.ChromaticInterval(-2)]

        #Figures
        self.figures[0] = "no figure"
        self.figures[1] = "6#42 or just -"
        self.figures[2] = "6"
        self.figures[3] = "6"
        self.figures[4] = "no figure"


class SLRule_28maybe(SLRule):
    """
    K's rule:   22
    Page:       xx
    Conditions: 
        * When bass note goes down a tone
        * [second interval] then down a tone
        * [third interval] then down a semitone
        * [fourth interval] then down a tone
    Figures:
        * 1st note gets no figure
        * 2nd note gets a '-'
        * 3rd note gets a 6
        * 4th note gets a 6
        * 5th note gets no figure
    """

    def __init__(self):
        SLRule.__init__(self,5)
        self.todo = "TBD"

        #Conditions
        self.intervals[0] = [interval.ChromaticInterval(-2)]
        self.intervals[1] = [interval.ChromaticInterval(-2)]
        self.intervals[2] = [interval.ChromaticInterval(-1)]
        self.intervals[3] = [interval.ChromaticInterval(-2)]

        #Figures
        self.figures[0] = "no figure"
        self.figures[1] = "-"
        self.figures[2] = "6"
        self.figures[3] = "6"
        self.figures[4] = "no figure"


class SLRule_29maybe(SLRule):
    """
    K's rule:   23
    Page:       xx
    Conditions: 
        * When bass note goes up a tone
        * [second interval] then up a tone
        * [third interval] then up a semitone
        * [fourth interval] then up a tone
    Figures:
        * 1st note gets no figure
        * 2nd note gets a 6
        * 3rd note gets a 6
        * 4th note gets a 65
        * 5th note gets no figure
    """

    def __init__(self):
        SLRule.__init__(self,5)
        self.todo = "TBD"

        #Conditions
        self.intervals[0] = [interval.ChromaticInterval(2)]
        self.intervals[1] = [interval.ChromaticInterval(2)]
        self.intervals[2] = [interval.ChromaticInterval(1)]
        self.intervals[3] = [interval.ChromaticInterval(2)]

        #Figures
        self.figures[0] = "no figure"
        self.figures[1] = "6"
        self.figures[2] = "6"
        self.figures[3] = "65"
        self.figures[4] = "no figure"


class SLRule_30maybe(SLRule):
    """
    K's rule:   24
    Page:       xx
    Conditions:
        * When bass note goes up a tone,
        * [second interval] then up a semitone,
        * [third interval] then up a tone,
        * [fourth interval] then up a tone
    Figures:
        * 1st note gets no figure
        * 2nd note gets a #6
        * 3rd note gets a 6
        * 4th note gets a 65
        * 5th note gets no figure
    """

    def __init__(self):
        SLRule.__init__(self,5)
        self.todo = "TBD"

        #Conditions
        self.intervals[0] = [interval.ChromaticInterval(2)]
        self.intervals[1] = [interval.ChromaticInterval(1)]
        self.intervals[2] = [interval.ChromaticInterval(2)]
        self.intervals[3] = [interval.ChromaticInterval(2)]

        #Figures
        self.figures[0] = "no figure"
        self.figures[1] = "#6"
        self.figures[2] = "6"
        self.figures[3] = "65"
        self.figures[4] = "no figure"


class SLRule_31maybe(SLRule):
    """
    K's rule:   25
    Page:       xx
    Conditions:
        * When at a cadence - -sol sol ut
    Figures:
        * 1st note gets a 4
        * 2nd note gets 7
        * 3rd note gets no figure
    """

    def __init__(self):
        SLRule.__init__(self,3)
        self.todo = "TBD; also cadence; also sol->ut up or down?."

        #Conditions
        self.intervals[0] = [interval.ChromaticInterval(0)]
        self.intervals[1] = [interval.ChromaticInterval(5)]

        #Figures
        self.figures[0] = "4"
        self.figures[1] = "7"
        self.figures[2] = "no figure"


class SLRule_32maybe(SLRule):
    """
    K's rule:   26
    Page:       xx
    Conditions: 
        * cadence - short sol ut
    Figures:
        * Short sol gets 7 (no 4) 
        * ut gets no figure
    """

    def __init__(self):
        SLRule.__init__(self,2)
        self.todo = "TBD; also cadence; also sol->ut up or down?."

        #Conditions
        self.intervals[0] = [interval.ChromaticInterval(5)]

        #Figures
        self.figures[0] = "7 (no 4)"
        self.figures[1] = "no figure"


class SLRule_33maybe(SLRule):
    """
    K's rule:   27
    Page:       xx
    Conditions: 
        * When at a cadence - long sol ut
    Figures:
        * Long sol gets 4 and 7
        * ut gets no figure
    """

    def __init__(self):
        SLRule.__init__(self,2)
        self.todo = "TBD; also cadence; also sol->ut up or down?."

        #Conditions
        self.intervals[0] = [interval.ChromaticInterval(5)]

        #Figures
        self.figures[0] = "4 and 7"
        self.figures[1] = "no figure"


class SLRule_34maybe(SLRule):
    """
    K's rule:   28
    Page:       xx
    Conditions:
        * When at a cadence and sol is 3 beats in 3/4 time
    Figures:
        * Sol gets 4,
        * no figure,
        * then a 7 (respectively on each beat)
    """

    def __init__(self):
        SLRule.__init__(self,3)
        self.todo = "TBD; also cadence."

        #Conditions
        self.extras[0] = ["3 beats", "time signature is 3/4"]

        #Figures
        self.figures[0] = "4"
        self.figures[1] = "no figure"
        self.figures[2] = "7"