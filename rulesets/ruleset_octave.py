# Rules of Octaves -- currently a dummy ruleset!

import rules
import sys
import inspect
import music21 as m21

import logging_setup as Logging
LOG = Logging.getLogger('rules')

key_name = "ROO"
long_name = "Rule of Octave (Currently a dummy set)"


class octaveRule(rules.Rule):
    def __init__(self, size):  # size=1
        rules.Rule.__init__(self)
        self.umbrella = "Rule of Octaves"
        self.size = size

        self.intervals = [False for x in range(size - 1)]
        self.beats = [False for x in range(size)]
        self.harmonic_content = [False for x in range(size)]
        self.figures = ['NA' for x in range(size)]
        self.extras = [False for x in range(size)]


def full_ruleset():
    """
    All rules available in this ruleset
    """
    allrules = []
    for name, rule in inspect.getmembers(sys.modules[__name__]):
        try:
            if issubclass(rule, octaveRule):
                allrules.append(rule())

                #Add rule to global rule dictionary
                rules.full_rule_dictionary[name] = rule
        except TypeError:
            pass

    fullruleset = rules.Ruleset(allrules, from_module=True, name=long_name)
    return fullruleset


#* * * RULES * * *
class octave_1(octaveRule):
    """
    Currently a dummy rule!
    """
    def __init__(self):
        octaveRule.__init__(self, 2)

        #Conditions:
        # * When the bass note goes up
        self.intervals[0] = [m21.interval.ChromaticInterval(1),
                             m21.interval.ChromaticInterval(2),
                             m21.interval.ChromaticInterval(3),
                             m21.interval.ChromaticInterval(4),
                             m21.interval.ChromaticInterval(5),
                             m21.interval.ChromaticInterval(6),
                             m21.interval.ChromaticInterval(7),
                             m21.interval.ChromaticInterval(8),
                             m21.interval.ChromaticInterval(9),
                             m21.interval.ChromaticInterval(10),
                             m21.interval.ChromaticInterval(11)
                             ]

        #Figures:
        self.figures[0] = m21.figuredBass.notation.Notation('+')
        self.figures[1] = m21.figuredBass.notation.Notation('++')


class octave_2(octaveRule):
    """
    Currently a dummy rule!
    """
    def __init__(self):
        octaveRule.__init__(self, 2)

        #Conditions:
        # * When the bass note goes down
        self.intervals[0] = [m21.interval.ChromaticInterval(-1),
                             m21.interval.ChromaticInterval(-2),
                             m21.interval.ChromaticInterval(-3),
                             m21.interval.ChromaticInterval(-4),
                             m21.interval.ChromaticInterval(-5),
                             m21.interval.ChromaticInterval(-6),
                             m21.interval.ChromaticInterval(-7),
                             m21.interval.ChromaticInterval(-8),
                             m21.interval.ChromaticInterval(-9),
                             m21.interval.ChromaticInterval(-10),
                             m21.interval.ChromaticInterval(-11)
                             ]

        #Figures:
        self.figures[0] = m21.figuredBass.notation.Notation('-')
        self.figures[1] = m21.figuredBass.notation.Notation('--')

#*************************

#Create Ruleset from all these rules, add to dictionary
rules.packagedRulesets[key_name] = full_ruleset()
