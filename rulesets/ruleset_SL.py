# Rules for figuring unfigured bass parts
# Monsieur de Saint-Lambert

import rules
import sys
import inspect
import music21 as m21
from music21.figuredBass import notation

import logging_setup as Logging
LOG = Logging.getLogger('rules')

key_name = "SL"
long_name = "Saint Lambert (Full)"


class SLRule(rules.Rule):
    def __init__(self, size):  # size=1
        rules.Rule.__init__(self)
        self.umbrella = "Saint Lambert"
        self.size = size

        self.intervals = [False for x in range(size - 1)]
        self.beats = [False for x in range(size)]
        self.harmonic_content = [False for x in range(size)]
        self.figures = [False for x in range(size)]
        self.extras = [False for x in range(size)]


def full_ruleset():
    """
    All rules available in this ruleset
    """
    allrules = []
    for name, rule in inspect.getmembers(sys.modules[__name__]):
        try:
            if issubclass(rule, SLRule):
                allrules.append(rule())

                #Add rule to global rule dictionary
                rules.full_rule_dictionary[name] = rule
        except TypeError:
            pass

    fullruleset = rules.Ruleset(allrules, from_module=True, name=long_name)
    return fullruleset


#* * * RULES * * *
class SLRule_3(SLRule):
    """
    K's rule:   1
    Page:       45
    Conditions:
        * When the bass note goes up by a diatonic semitone
        * Second chord should be a triad (maj or min)(no 7)TODO
    Figures:
        * First note gets a 6 (6,3)
            -> Realization: l'accord double or accord simple
        * Second gets 5,3.
    Notes:
        * A generalization of SL1
        * Confirms that we don't want augmented unison
    """
    def __init__(self):
        SLRule.__init__(self, 2)
        self.todo = 'interval to diatonic!'

        #Conditions:
        self.intervals[0] = [m21.interval.ChromaticInterval(1)]  # TODO:diatonic semitone
        self.harmonic_content[1] = ['perfectTriadNoSeven']  # TODO:diatonic semitone

        #Figures:
        self.figures[0] = notation.Notation('6,3')
        self.figures[1] = notation.Notation('5,3')


class SLRule_4(SLRule):
    """
    K's rule:   NA
    Page:       46
    Conditions:
        * When the bass note goes up by a diatonic semitone
        * First note has a major triad (7 doesn't matter)
    Figures:
        * First note gets a 5,3+
        * Second gets 6 (l'accord double)
    """
    def __init__(self):
        SLRule.__init__(self, 2)
        self.todo = 'interval to diatonic!'

        #Conditions:
        self.intervals[0] = [m21.interval.ChromaticInterval(1)]  # TODO:diatonic semitone
        self.harmonic_content[0] = ['perfectMajorTriadOkSeven']

        #Figures:
        self.figures[0] = notation.Notation('5,3+')
        self.figures[1] = notation.Notation('6')


class SLRule_5(SLRule):
    """
    K's rule:   2
    Page:       46
    Conditions:
        * When bass note goes down by a diatonic semitone
        * second note is a perfect chord (major triad) "accord majeur" (no 7)
        * second note is on beat 1
    Figures:
        * First note gets a 6 "accord double"
        * Second note gets a 5,3+
    """
    def __init__(self):
        SLRule.__init__(self, 2)
        self.todo = 'interval to diatonic'

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(-1)]  # TODOdiatonic
        self.beats[1] = [1]
        self.harmonic_content[1] = ['perfectMajorTriadNoSeven']

        #Figures"
        self.figures[0] = notation.Notation('6')
        self.figures[1] = notation.Notation('5,3+')


    #     class SLRule_5(SLRule):
    # def __init__(self):
    #     SLRule.__init__(self,2)

    #     #Conditions
    #     self.intervals[0] = [m21.interval.DiatonicInterval('major', -2)]
    #     self.beats[1] = [1]
    #     self.harmonic_content[1] = ['perfectMajorTriadNoSeven']

    #     #Figures"
    #     self.figures[0] = notation.Notation('6')
    #     self.figures[1] = notation.Notation('5,3+')


class SLRule_6(SLRule):
    """
    K's rule:   3
    Page:       46
    Conditions:
        * bass note goes up by a diatonic semitone
        * the first note has a #6
    Figures:
        * First note gets a "6+(4)(3)"
        * Second note gets a 6
    """

    def __init__(self):
        SLRule.__init__(self, 2)
        self.todo = 'diatonic'

        #Conditions:
        self.intervals[0] = [m21.interval.ChromaticInterval(1)]  # TODOdiatonic
        self.harmonic_content[0] = ['hasSharpSix']

        #Figures:
        self.figures[0] = notation.Notation('6+')  # TODO'6+,(4),(3)')
        self.figures[1] = notation.Notation('6')


class SLRule_7(SLRule):
    """
    K's rule:   4
    Page:       47
    Conditions:
        * Bass note goes down by a minor 3rd (ch)
        * First chord is minor triad (no 7)
    Figures:
        * First gets 3-
        * Second gets false fifth (5,3-) "fausse quinte"
    Notes:
        * {explicitly says down minor third;
            should check (w/switch!) to see if modulated (up 6) is also okay}
    """

    def __init__(self):
        SLRule.__init__(self, 2)

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(-3)]
        self.harmonic_content[0] = ['isPerfect']

        #Figures
        self.figures[0] = notation.Notation('3-')
        self.figures[1] = notation.Notation('5,3-')


class SLRule_8a(SLRule):
    """
    K's rule:   NA
    Page:       47
    Conditions:
        * first note has a flat (outside of the key signature)
        * second note does not have a 6 above it
        * bass descends minor third (ch)
    Figures:
        * first chord gets a 5,3
        * second chord gets a 5,3-
    Notes:
        * Hank might yank!
    """
    def __init__(self):
        SLRule.__init__(self, 2)

        #Conditions
        self.extras[0] = ['accidental:flat']
        self.harmonic_content[1] = ['notHasSix']
        self.intervals[0] = [m21.interval.ChromaticInterval(-3)]

        #Figures
        self.figures[0] = notation.Notation('5,3')
        self.figures[1] = notation.Notation('5,3-')


class SLRule_8b(SLRule):
    """
    K's rule:   NA
    Page:       47
    Conditions:
        * first note has a flat (outside of the key signature)
        * second note has a 6 (maj,min)
        * bass descends minor third (ch)
    Figures:
        * first chord gets a 5,3
        * second chord gets a 6,3-
    Notes:
        * Hank might yank!
    """
    def __init__(self):
        SLRule.__init__(self, 2)

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(-3)]
        self.harmonic_content[1] = ['hasSix']
        self.extras[0] = ['accidental:flat']

        #Figures
        self.figures[0] = notation.Notation('5,3')
        self.figures[1] = notation.Notation('6,3-')


class SLRule_10a(SLRule):
    """
    K's rule:   NA
    Page:       47
    Conditions:
        * bass descends major third (ch)
        * first note has sharp outside of key signature
    Figures:
        * first note gets a 6
        * the second chord gets 5,3+
    Notes:
        * Same as 8, but with major thirds instead of minor thirds
        * Hank might yank!
    """

    def __init__(self):
        SLRule.__init__(self, 2)

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(-4)]
        self.extras[0] = ['accidental:sharp']

        #Figures
        self.figures[0] = notation.Notation('6')
        self.figures[1] = notation.Notation('5,3+')


class SLRule_10b(SLRule):
    """
    K's rule:   NA
    Page:       47
    Conditions:
        * bass note rises by a major third (ch)
        * second note has sharp outside of key signature
    Figures:
        * first chord gets 5,3+
        * second chord gets 6
    Notes:
        * Same as 9, but with major thirds instead of minor thirds
        * Hank might yank!
    """

    def __init__(self):
        SLRule.__init__(self, 2)

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(4)]
        self.extras[1] = ['accidental:sharp']

        #Figures
        self.figures[0] = notation.Notation('5,3+')
        self.figures[1] = notation.Notation('6')


class SLRule_11(SLRule):
    """
    K's rule:   5
    Page:       47
    Conditions:
        * bass note goes down by a 3rd, (either major or minor) (ch)
        * first chord is a perfect major triad {this case: could have a seven}
    Figures:
        * first gets 5,3+
        * second gets a 6 (l'accord simple)
    """

    def __init__(self):
        SLRule.__init__(self, 2)

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(-3),
                            m21.interval.ChromaticInterval(-4)]
        self.harmonic_content[0] = ['perfectMajorTriadOkSeven']

        #Figures
        self.figures[0] = notation.Notation('5,3+')
        self.figures[1] = notation.Notation('6')


class SLRule_12(SLRule):
    """
    K's rule:   6
    Page:       48
    Conditions:
        * bass note descends by a false 5th (aka tritone aka diminished fifth) (ch)
    Figures:
        * 1st gets 5,3
        * 2nd gets 5-
    """

    def __init__(self):
        SLRule.__init__(self, 2)

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(-6)]

        #Figures
        self.figures[0] = notation.Notation('5,3')
        self.figures[1] = notation.Notation('5-')


class SLRule_13(SLRule):
    """
    K's rule:   7
    Page:       48
    Conditions:
        * bass note goes up by a 3rd or DOWN by 6th (of any kind) (ch)
        * first chord is perfect triad (no 7)
    Figures:
        * First gets 5,3
        * Second note gets a 6 (l'accord simple)
    """

    def __init__(self):
        SLRule.__init__(self, 2)

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(3),
                            m21.interval.ChromaticInterval(4),
                            m21.interval.ChromaticInterval(-8),
                            m21.interval.ChromaticInterval(-9)]
        self.harmonic_content[0] = ['perfectTriadNoSeven']

        #Figures
        self.figures[0] = notation.Notation('5,3')
        self.figures[1] = notation.Notation('6')


class SLRule_14(SLRule):
    """
    K's rule:   8
    Page:       48
    Conditions:
        * When bass note goes up 3 consecutive tones (MUST BE SEMITONE OR TONE)
        * 3rd chord is perfect major triad, no 7
    Figures:
        * 1st note gets a 6
        * 2nd note gets a 6,5,3
        * 3rd note gets a major chord (5,3+)
    """

    def __init__(self):
        SLRule.__init__(self, 3)

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(1), m21.interval.ChromaticInterval(2)]
        self.intervals[1] = [m21.interval.ChromaticInterval(1), m21.interval.ChromaticInterval(2)]
        self.harmonic_content[2] = ['perfectMajorTriadNoSeven']

        #Figures
        self.figures[0] = notation.Notation('6')
        self.figures[1] = notation.Notation('6,5,3')
        self.figures[2] = notation.Notation('5,3+')


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
        SLRule.__init__(self, 3)

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(-2)]
        self.intervals[1] = [m21.interval.ChromaticInterval(-2)]
        self.harmonic_content[0] = ['perfectMajorTriadOkSeven']

        #Figures
        self.figures[1] = notation.Notation('6,4+,2')
        self.figures[2] = notation.Notation('6')


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
        SLRule.__init__(self, 3)
        self.todo = "Notation: '-' represents '-' not figures!"

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(-2)]
        self.intervals[1] = [m21.interval.ChromaticInterval(-2)]
        self.harmonic_content[0] = ['perfectTriadNoSeven']
        self.harmonic_content[2] = ['hasSeventh']

        #Figures
        self.figures[0] = notation.Notation('5,3')
        self.figures[1] = notation.Notation('----')
        self.figures[2] = notation.Notation('7')


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
        SLRule.__init__(self, 3)

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(-3),
                             m21.interval.ChromaticInterval(-4)]
        self.intervals[1] = [m21.interval.ChromaticInterval(2)]
        self.harmonic_content[2] = ['isMajor']
        self.beats[2] = [1]

        #Figures
        self.figures[1] = notation.Notation('6')


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
        SLRule.__init__(self, 3)

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(-3)]
        self.intervals[1] = [m21.interval.ChromaticInterval(1)]
        self.beats[2] = [1]

        #Figures
        self.figures[0] = notation.Notation('5,3')
        self.figures[1] = notation.Notation('6')
        self.figures[2] = notation.Notation('5,3')


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
        SLRule.__init__(self, 3)

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(-4)]
        self.intervals[1] = [m21.interval.ChromaticInterval(5)]
        self.harmonic_content[0] = ['hasDiminishedFifth']

        #Figures
        self.figures[1] = notation.Notation('7')
        self.figures[2] = notation.Notation('5,3')


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
        SLRule.__init__(self, 3)
        self.todo = "Ambiguous figure application"

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(1)]
        self.intervals[1] = [m21.interval.ChromaticInterval(7),
                            m21.interval.ChromaticInterval(-5)]
        self.beats[2] = [1]

        #Figures
        self.figures[0] = notation.Notation('6,5b')
        self.figures[1] = notation.Notation('5,3')
        self.figures[2] = notation.Notation('5,3')


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
        SLRule.__init__(self, 3)

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(0)]
        self.intervals[1] = [m21.interval.ChromaticInterval(7)]
        self.beats[2] = [1]

        #Figures
        self.figures[0] = notation.Notation('5,3')
        self.figures[1] = notation.Notation('6')
        self.figures[2] = notation.Notation('5,3')


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
        SLRule.__init__(self, 3)

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(0)]
        self.intervals[1] = [m21.interval.ChromaticInterval(-5)]
        self.harmonic_content[0] = ['perfectMajorTriadNoSeven']
        self.beats[2] = [1]

        #Figures
        self.figures[0] = notation.Notation('5,3')
        self.figures[1] = notation.Notation('6,4+')
        self.figures[2] = notation.Notation('5,3')


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
        SLRule.__init__(self, 4)

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(2)]
        self.intervals[1] = [m21.interval.ChromaticInterval(2)]
        self.intervals[2] = [m21.interval.ChromaticInterval(1)]
        self.beats[3] = [1]

        #Figures
        self.figures[0] = notation.Notation('5,3')
        self.figures[1] = notation.Notation('6')
        self.figures[2] = notation.Notation('6,5b')
        self.figures[3] = notation.Notation('5,3')


class SLRule_24a(SLRule):
    """
    K's rule:   18
    Page:       52
    Conditions:
        * bass note goes down a semitone
        * [second interval] then down a tone
        * [third interval] then down a tone
        * last note is on 1st beat
    Figures:
        * 1st note gets root position triad (5,3)
        * 2nd note gets a 6
        * 3rd note gets #6 (5b)
        * 4th note gets a major triad (5,3+)
    Note:
        * SL calls all of 24 "Cadences imparfaites": half-cadences,
            or first half of the descending 'Rule of the Octave'
    """

    def __init__(self):
        SLRule.__init__(self, 4)

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(-1)]
        self.intervals[1] = [m21.interval.ChromaticInterval(-2)]
        self.intervals[2] = [m21.interval.ChromaticInterval(-2)]
        self.beats[3] = [1]

        #Figures
        self.figures[0] = notation.Notation('5,3')
        self.figures[1] = notation.Notation('6')
        self.figures[2] = notation.Notation('6+')  # TODO'6+(5-)')
        self.figures[3] = notation.Notation('5,3+')


class SLRule_24a1(SLRule):
    """
    K's rule:   18
    Page:       52
    Conditions:
        * bass note goes down a semitone
        * [second interval] then down a tone
        * [third interval] then down a tone
        * last note is on 1st beat
        * second note is smaller note value than first
    Figures:
        * 1st note gets root position triad (5,3)
        * 2nd note gets nothing (same as chord before --> dash!)(6,4,2)
        * 3rd note gets #6 (5b)
        * 4th note gets a major triad (5,3+)
    """

    def __init__(self):
        SLRule.__init__(self, 4)

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(-1)]
        self.intervals[1] = [m21.interval.ChromaticInterval(-2)]
        self.intervals[2] = [m21.interval.ChromaticInterval(-2)]
        self.beats[3] = [1]
        self.extras[1] = ['duration:lessThanPreceding']

        #Figures
        self.figures[0] = notation.Notation('5,3')
        self.figures[1] = notation.Notation('6,4,2')
        self.figures[2] = notation.Notation('6+')  # TODO'6+(5-)')
        self.figures[3] = notation.Notation('5,3+')


class SLRule_24b1(SLRule):
    """
    K's rule:   19
    Page:       52-3
    Conditions:
        * When bass note goes down a tone,
        * [second interval] then down a semitone
        * [third interval] then down a tone
        * first chord has perfect (major) triad
        * last note is on 1st beat
    Figures:
        * 1st note gets root position major triad (5,3+)
        * 2nd note get a (6,4+,2)
        * 3rd note gets a #6
        * 4th note gets minor triad (5,3-)
    Note:
        * SL calls all of 24 "Cadences imparfaites": half-cadences,
            or first half of the descending 'Rule of the Octave'
    """

    def __init__(self):
        SLRule.__init__(self, 4)
        self.todo = "triad with or without 7?"

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(-2)]
        self.intervals[1] = [m21.interval.ChromaticInterval(-1)]
        self.intervals[2] = [m21.interval.ChromaticInterval(-2)]
        self.beats[3] = [1]
        self.harmonic_content[0] = ['perfectMajorTriadNoSeven']  # TODO-maybewrong

        #Figures
        self.figures[0] = notation.Notation('5,3+')
        self.figures[1] = notation.Notation('6,4+,2')
        self.figures[2] = notation.Notation('6+')
        self.figures[3] = notation.Notation('5,3-')


class SLRule_24b2(SLRule):
    """
    K's rule:   19
    Page:       52-3
    Conditions:
        * When bass note goes down a tone,
        * [second interval] then down a semitone
        * [third interval] then down a tone
        * first chord has minor triad
        * last note is on 1st beat
    Figures:
        * 1st note gets root position major triad (5,3+)
        * 2nd note get a (6,4,2)
        * 3rd note gets a #6,4,3 (petit accord)
        * 4th note gets minor triad (5,3-)
    Note:
        * SL calls all of 24 "Cadences imparfaites": half-cadences,
            or first half of the descending 'Rule of the Octave'
    """

    def __init__(self):
        SLRule.__init__(self, 4)
        self.todo = "minor triad has seven?"

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(-2)]
        self.intervals[1] = [m21.interval.ChromaticInterval(-1)]
        self.intervals[2] = [m21.interval.ChromaticInterval(-2)]
        self.beats[3] = [1]
        self.harmonic_content[0] = ['minorTriadNoSeven']  # TODO-maybewrong

        #Figures
        self.figures[0] = notation.Notation('5,3+')
        self.figures[1] = notation.Notation('6,4,2')
        self.figures[2] = notation.Notation('6+,4,3')
        self.figures[3] = notation.Notation('5,3-')


class SLRule_24c(SLRule):
    """
    K's rule:   20
    Page:       53
    Conditions:
        * bass note goes down a tone
        * [second interval] then down a tone
        * [third interval] then down a semitone
        * last note is on 1st beat
    Figures:
        * 1st note gets minor triad (5,3-)
        * 2nd note gets perfect major triad (5,3+)  or (in paren (6,4,2))
        * 3rd note gets a 6 or (in paren (6,4+,3) "le petit accord")
        * 4th note gets major triad (5,3+) ("l'accord parfait majeur")
    Note:
        * SL calls all of 24 "Cadences imparfaites": half-cadences,
            or first half of the descending 'Rule of the Octave'
    """

    def __init__(self):
        SLRule.__init__(self, 4)

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(-2)]
        self.intervals[1] = [m21.interval.ChromaticInterval(-2)]
        self.intervals[2] = [m21.interval.ChromaticInterval(-1)]
        self.beats[3] = [1]

        #Figures
        self.figures[0] = notation.Notation('5,3-')
        self.figures[1] = notation.Notation('5,3+')
        self.figures[2] = notation.Notation('6,4+,3')
        self.figures[3] = notation.Notation('5,3+')


class SLRule_24c1(SLRule):
    """
    K's rule:   20
    Page:       53
    Conditions:
        * bass note goes down a tone
        * [second interval] then down a tone
        * [third interval] then down a semitone
        * third note is at least twice as long as first two individually
        * last note is on 1st beat
    Figures:
        * 1st note gets minor triad (5,3-)
        * 2nd note gets nothing or (6,4,2)
        * 3rd note gets two figures:(in two halves)
        * (7,5)
        * 2nd chord (6,4,3) ("le petit accord")(in paren (6)) "l'accord double")
        * 4th note gets major triad (5,3+) ("l'accord parfait majeur")
    Note:
        * SL calls all of 24 "Cadences imparfaites": half-cadences,
            or first half of the descending 'Rule of the Octave'
    """

    def __init__(self):
        SLRule.__init__(self, 4)

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(-2)]
        self.intervals[1] = [m21.interval.ChromaticInterval(-2)]
        self.intervals[2] = [m21.interval.ChromaticInterval(-1)]
        self.beats[3] = [1]
        self.extras[2] = ['duration:twiceAsPreviousTwo']

        #Figures
        self.figures[0] = notation.Notation('5,3-')
        self.figures[1] = notation.Notation('6,4,2')
        self.figures[2] = ['split', notation.Notation('7,5'),
                            notation.Notation('6,4,3')]
        self.figures[3] = notation.Notation('5,3+')


class SLRule_25a(SLRule):
    """
    K's rule:   21
    Page:       54
    Conditions:
        * When bass note goes down a tone
        * [second interval] then down a semitone
        * [third interval] then down a tone
        * [fourth interval] then down a tone
        * last note is on a down beat
        * first note has major triad (without 7)(Dominant chord)
        * Starts on the fifth degree of the scale
    Figures:
        * 1st note gets no figure (5,3+)
        * 2nd note gets a 64+2
        * 3rd gets a 6,3 ("l'accord double"" or "l'accord simple")
        * 4th gets a 6+ or (6+,4,3)("l'accord simple de la sixieme majeur or le petit accord")
        * 5th gets no figure (5,3) ("l'accord parfait")(major or minor)
    Note:
        * Typo in last of the first SL examples! (off by a tone)
        * This rule is last five notes of the descending 'rule of the octave': Sol fa mi re ut
        * Major version
        * Starts on the fifth degree of the scale
    """

    def __init__(self):
        SLRule.__init__(self, 5)

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(-2)]
        self.intervals[1] = [m21.interval.ChromaticInterval(-1)]
        self.intervals[2] = [m21.interval.ChromaticInterval(-2)]
        self.intervals[3] = [m21.interval.ChromaticInterval(-2)]
        self.beats[4] = [1]
        self.harmonic_content[0] = ['perfectMajorTriadNoSeven']
        self.extras[0] = ['scale:on5th']

        #Figures
        self.figures[0] = notation.Notation('5,3+')
        self.figures[1] = notation.Notation('6,4+,2')
        self.figures[2] = notation.Notation('6,3')
        self.figures[3] = notation.Notation('6+')
        self.figures[4] = notation.Notation('5,3')


class SLRule_25b(SLRule):
    """
    K's rule:   21
    Page:       54
    Conditions:
        * When bass note goes down a tone
        * [second interval] then down a tone
        * [third interval] then down a semitone
        * [fourth interval] then down a tone
        * last note is on a down beat
        * first note has major triad (without 7)(Dominant chord)
        * Starts on the fifth degree of the scale
    Figures:
        * 1st note gets no figure (5,3+)
        * 2nd note gets a 64+2
        * 3rd gets a 6,3 ("l'accord double"" or "l'accord simple")
        * 4th gets a 6+ or (6+,4,3)("l'accord simple de la sixieme majeur or le petit accord")
        * 5th gets no figure (5,3) ("l'accord parfait")(major or minor)
    Note:
        * Typo in last of the first SL examples! (off by a tone)
        * This rule is last five notes of the descending 'rule of the octave': Sol fa mi re ut
        * Major version
        * Starts on the fifth degree of the scale
    """

    def __init__(self):
        SLRule.__init__(self, 5)

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(-2)]
        self.intervals[1] = [m21.interval.ChromaticInterval(-1)]
        self.intervals[2] = [m21.interval.ChromaticInterval(-2)]
        self.intervals[3] = [m21.interval.ChromaticInterval(-2)]
        self.beats[4] = [1]
        self.harmonic_content[0] = ['perfectMajorTriadNoSeven']
        self.extras[0] = ['scale:on5th']

        #Figures
        self.figures[0] = notation.Notation('5,3+')
        self.figures[1] = notation.Notation('6,4+,2')
        self.figures[2] = notation.Notation('6,3')
        self.figures[3] = notation.Notation('6+')
        self.figures[4] = notation.Notation('5,3')


class SLRule_26a1(SLRule):
    """
    K's rule:   22
    Page:       54
    Conditions:
        * When bass note goes down a tone
        * [second interval] then down a semitone
        * [third interval] then down a tone
        * [fourth interval] then down a tone
        * [fifth interval] down semitone
        * 6 note is on strong beat

    Figures:
        * 1st note gets no figure (5,3+)
        * 2nd note gets a 64+2
        * 3rd gets a 6,3 ("l'accord double"" or "l'accord simple")
        * 4th gets a 6+ or (6+,4,3)("l'accord simple de la sixieme majeur or le petit accord")
        * 5th gets no figure (5,3) ("l'accord parfait")(major or minor)
        * 6th gets a 6
    """

    def __init__(self):
        SLRule.__init__(self, 6)

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(-2)]
        self.intervals[1] = [m21.interval.ChromaticInterval(-1)]
        self.intervals[2] = [m21.interval.ChromaticInterval(-2)]
        self.intervals[3] = [m21.interval.ChromaticInterval(-2)]
        self.intervals[4] = [m21.interval.ChromaticInterval(-1)]
        self.beats[5] = [1]

        #Figures
        self.figures[0] = notation.Notation('5,3+')
        self.figures[1] = notation.Notation('6,4+,2')
        self.figures[2] = notation.Notation('6,3')
        self.figures[3] = notation.Notation('6+')
        self.figures[4] = notation.Notation('5,3')
        self.figures[5] = notation.Notation('6')


class SLRule_26a2(SLRule):
    """
    K's rule:   22
    Page:       54
    Conditions:
        * When bass note goes down a tone
        * [second interval] then down a semitone
        * [third interval] then down a tone
        * [fourth interval] then down a tone
        * [fifth interval] up 5th or down 4th
        * 6 note is on strong beat

    Figures:
        * 1st note gets no figure (5,3+)
        * 2nd note gets a 64+2
        * 3rd gets a 6,3 ("l'accord double"" or "l'accord simple")
        * 4th gets a 6+ or (6+,4,3)("l'accord simple de la sixieme majeur or le petit accord")
        * 5th gets no figure (5,3) ("l'accord parfait")(major or minor)
        * 6th gets a major triad (5,3+)
    """

    def __init__(self):
        SLRule.__init__(self, 6)

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(-2)]
        self.intervals[1] = [m21.interval.ChromaticInterval(-1)]
        self.intervals[2] = [m21.interval.ChromaticInterval(-2)]
        self.intervals[3] = [m21.interval.ChromaticInterval(-2)]
        self.intervals[4] = [m21.interval.ChromaticInterval(7),
                            m21.interval.ChromaticInterval(-5)]
        self.beats[5] = [1]

        #Figures
        self.figures[0] = notation.Notation('5,3+')
        self.figures[1] = notation.Notation('6,4+,2')
        self.figures[2] = notation.Notation('6,3')
        self.figures[3] = notation.Notation('6+')
        self.figures[4] = notation.Notation('5,3')
        self.figures[5] = notation.Notation('5,3+')


class SLRule_26b1(SLRule):
    """
    K's rule:   22
    Page:       54
    Conditions:
        * When bass note goes down a tone
        * [second interval] then down a tone
        * [third interval] then down a semitone
        * [fourth interval] then down a tone
        * [fifth interval] down semitone
        * 6 note is on strong beat

    Figures:
        * 1st note gets no figure (5,3+)
        * 2nd note gets a 64+2
        * 3rd gets a 6,3 ("l'accord double"" or "l'accord simple")
        * 4th gets a 6+ or (6+,4,3)("l'accord simple de la sixieme majeur or le petit accord")
        * 5th gets no figure (5,3) ("l'accord parfait")(major or minor)
        * 6th gets a 6
    """

    def __init__(self):
        SLRule.__init__(self, 6)

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(-2)]
        self.intervals[1] = [m21.interval.ChromaticInterval(-2)]
        self.intervals[2] = [m21.interval.ChromaticInterval(-1)]
        self.intervals[3] = [m21.interval.ChromaticInterval(-2)]
        self.intervals[4] = [m21.interval.ChromaticInterval(-1)]
        self.beats[5] = [1]

        #Figures
        self.figures[0] = notation.Notation('5,3+')
        self.figures[1] = notation.Notation('6,4+,2')
        self.figures[2] = notation.Notation('6,3')
        self.figures[3] = notation.Notation('6+')
        self.figures[4] = notation.Notation('5,3')
        self.figures[5] = notation.Notation('6')


class SLRule_26b2(SLRule):
    """
    K's rule:   22
    Page:       54
    Conditions:
        * When bass note goes down a tone
        * [second interval] then down a tone
        * [third interval] then down a semitone
        * [fourth interval] then down a tone
        * [fifth interval] up 5th or down 4th
        * 6 note is on strong beat

    Figures:
        * 1st note gets no figure (5,3+)
        * 2nd note gets a 64+2
        * 3rd gets a 6,3 ("l'accord double"" or "l'accord simple")
        * 4th gets a 6+ or (6+,4,3)("l'accord simple de la sixieme majeur or le petit accord")
        * 5th gets no figure (5,3) ("l'accord parfait")(major or minor)
        * 6th gets a major triad (5,3+)
    """

    def __init__(self):
        SLRule.__init__(self, 6)

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(-2)]
        self.intervals[1] = [m21.interval.ChromaticInterval(-2)]
        self.intervals[2] = [m21.interval.ChromaticInterval(-1)]
        self.intervals[3] = [m21.interval.ChromaticInterval(-2)]
        self.intervals[4] = [m21.interval.ChromaticInterval(7),
                            m21.interval.ChromaticInterval(-5)]
        self.beats[5] = [1]

        #Figures
        self.figures[0] = notation.Notation('5,3+')
        self.figures[1] = notation.Notation('6,4+,2')
        self.figures[2] = notation.Notation('6,3')
        self.figures[3] = notation.Notation('6+')
        self.figures[4] = notation.Notation('5,3')
        self.figures[5] = notation.Notation('5,3+')


class SLRule_27a(SLRule):
    """
    K's rule:   23
    Page:       55
    Conditions:
        * When bass note goes up a tone
        * [second interval] then up a tone
        * [third interval] then up a semitone
        * [fourth interval] then up a tone
    Figures:
        * 1st note gets no figure (5,3) "l'accord parfait"
        * 2nd note gets a 6+ "l'accord simple" or (6+,4,3) "l'petit accord"
        * 3rd note gets a 6 "l'accord double" or (6,3) "l'accord simple" #Hnote: don't put in l'accord simple this time
        * 4th note gets a 5,3 (l'accord parfait) or (6,5,3)
        * 5th note gets l'accord parfait majeur (perfect major triad) 5,3+
    Note:
        * major version: ut re me fa sol
        * SL prefers the variants to the simple version
        * Note: pay attention to variants when doing the realization! :)
    """

    def __init__(self):
        SLRule.__init__(self, 5)

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(2)]
        self.intervals[1] = [m21.interval.ChromaticInterval(2)]
        self.intervals[2] = [m21.interval.ChromaticInterval(1)]
        self.intervals[3] = [m21.interval.ChromaticInterval(2)]

        #Figures
        self.figures[0] = notation.Notation('5,3')
        self.figures[1] = notation.Notation('6+')
        self.figures[2] = notation.Notation('6')
        self.figures[3] = notation.Notation('5,3')
        self.figures[4] = notation.Notation('5,3+')


class SLRule_27b(SLRule):
    """
    K's rule:   24
    Page:       55
    Conditions:
        * When bass note goes up a tone,
        * [second interval] then up a semitone,
        * [third interval] then up a tone,
        * [fourth interval] then up a tone
    Figures:
        * 1st note gets no figure (5,3) "l'accord parfait"
        * 2nd note gets a 6+ "l'accord simple" or (6+,4,3) "l'petit accord"
        * 3rd note gets a 6 "l'accord double" or (6,3) "l'accord simple" #Hnote: don't put in l'accord simple this time
        * 4th note gets a 5,3 (l'accord parfait) or (6,5,3)
        * 5th note gets l'accord parfait majeur (perfect major triad) 5,3+
    Note:
        * minor version: re me fa sol la
    """

    def __init__(self):
        SLRule.__init__(self, 5)

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(2)]
        self.intervals[1] = [m21.interval.ChromaticInterval(1)]
        self.intervals[2] = [m21.interval.ChromaticInterval(2)]
        self.intervals[3] = [m21.interval.ChromaticInterval(2)]

        #Figures
        self.figures[0] = notation.Notation('5,3')
        self.figures[1] = notation.Notation('6+')
        self.figures[2] = notation.Notation('6')
        self.figures[3] = notation.Notation('5,3')
        self.figures[4] = notation.Notation('5,3+')


class SLRule_28(SLRule):
    """
    K's rule:   25
    Page:       55
    Conditions:
        * first interval is an octave (up or down)
        * second interval either rising fourth or descending fifth
        * last note is a perfect triad (no 7)(major or minor)
        * Last note on first note
    Figures:
        * 1st note gets 5,4
        * 2nd note gets 7,3+
        * 3rd note gets 5,3
    Questions?
        * When at a cadence - -sol sol ut
    """

    def __init__(self):
        SLRule.__init__(self, 3)

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(12),
                             m21.interval.ChromaticInterval(-12)]
        self.intervals[1] = [m21.interval.ChromaticInterval(-7),
                            m21.interval.ChromaticInterval(5)]
        self.beats[2] = [1]
        self.harmonic_content[2] = ['perfectTriadNoSeven']

        #Figures
        self.figures[0] = notation.Notation('5,4')
        self.figures[1] = notation.Notation('7,3+')
        self.figures[2] = notation.Notation('5,3')


class SLRule_29(SLRule):
    """
    K's rule:   26
    Page:       55
    Conditions:
        * only interval is either descending fifth or rising fourth
        * first note must be long enough to support two chords ("working hypothesis": half a measure in length or bigger or worth two of the denominator of the time signature)
        * last note falls on first note
    Figures:
        * 1st half of first note gets 5,4
        * 2nd half of first note gets 7,3+
        * 2nd note gets 5,3
    Questions?
        * cadence - long sol ut
        * variant of 28
    """

    def __init__(self):
        SLRule.__init__(self, 2)

        #Conditions
        self.intervals[0] = [m21.interval.ChromaticInterval(-7),
                            m21.interval.ChromaticInterval(5)]
        self.beats[1] = [1]
        self.extras[0] = ['duration:two']

        #Figures
        self.figures[0] = ['split', notation.Notation('5,4'),
                            notation.Notation('7,3+')]
        self.figures[1] = notation.Notation('5,3')


class SLRule_30(SLRule):
    """
    K's rule:   27
    Page:       56
    Conditions:
        * first note is short relative to time signature: either only one or half of the denominator
        * second note is perfect triad (major or minor, no 7)
        * last note falls on first beat
    Figures:
        * 1st note gets 5,3+(7)
        * 2nd note gets 5,3
    Note:
        * When at a cadence - short sol ut
    """

    def __init__(self):
        SLRule.__init__(self, 2)

        #Conditions
        self.extras[0] = ['duration:shortAgainstSignature']
        self.harmonic_content[1] = ['perfectTriadNoSeven']
        self.beats[1] = [1]

        #Figures
        self.figures[0] = notation.Notation('5,3+')  # '5,3+(7)')
        self.figures[1] = notation.Notation('5,3')


class SLRule_31(SLRule):
    """
    K's rule:   28
    Page:       56
    Conditions:
        * first note long enough to support two chords
        * second note on strong beat
    Figures:
        * First note gets 5,4
        * Second placement of first note: 7,5,3+
        * Second note gets 5,3
    Note:
        * has to do with 29!
        * for placement of chords on long note, see additional chicken scratch
        * choice between location on triple -- left for another day!
    """

    def __init__(self):
        SLRule.__init__(self, 3)

        #Conditions
        self.extras[0] = ['duration:two']
        self.beats[1] = [1]

        #Figures
        self.figures[0] = notation.Notation('5,4')
        self.figures[1] = notation.Notation('7,5,3+')
        self.figures[2] = notation.Notation('5,3')


class SLRule_32(SLRule):
    """
    K's rule:   NA
    Page:       56
    Conditions:
        * first note long enough to support two chords
        * second note on strong beat
        * triple meter
    Figures:
        * First note gets 5,4
        * Second placement of first note: 8,5,3+
        * Third placement of first note gets 7,5,3+
        * Second note: 5,3
    Note:
        * has to do with 29!
        * has to do with triple meter
        * for placement of chords on long note, see additional chicken scratch
        * choice between location on triple -- left for another day!
    """

    def __init__(self):
        SLRule.__init__(self, 3)

        #Conditions
        self.extras[0] = ['duration:two', 'meter:triple']
        self.beats[1] = [1]

        #Figures
        self.figures[0] = ['split',
                            notation.Notation('5,4'),
                            notation.Notation('8,5,3+'),
                            notation.Notation('7,5,3+')]
        self.figures[2] = notation.Notation('5,3')

#*************************

#Create Ruleset from all these rules, add to dictionary
rules.packagedRulesets[key_name] = full_ruleset()
