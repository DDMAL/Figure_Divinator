# Rules for figuring unfigured bass parts
# Monsieur de Saint-Lambert

import rules
import sys
import inspect
from music21 import interval
from music21.figuredBass import notation

import logging_setup as Logging
LOG = Logging.getLogger('rules')

key_name = "TEMP"                                       # ADJUST: "YOURRule"
long_name = "FULL NAME"                                 # ADJUST: "YOURRule"


class YOURRule(rules.Rule):                             # ADJUST: "YOURRule"
    def __init__(self, size):  # size=1
        rules.Rule.__init__(self)
        self.umbrella = long_name
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
            if issubclass(rule, YOURRule):              # ADJUST: "YOURRule"
                allrules.append(rule())

                #Add rule to global rule dictionary
                rules.full_rule_dictionary[name] = rule
        except TypeError:
            pass

    fullruleset = rules.Ruleset(allrules, from_module=True, name=long_name)
    return fullruleset


#* * * * * * * * *
#* * * RULES * * *
class Yourrulename(YOURRule):            # ADJUST: "YOURRule", "Yourrulename"
    """
    ADJUST: Rule description here!.
    """
    def __init__(self):
        YOURRule.__init__(self, 2)                       # ADJUST: "YOURRule"
        self.todo = 'interval to diatonic!'

        #Conditions:
        self.intervals[0] = [m21.interval.ChromaticInterval(1)]
        self.harmonic_content[1] = ['perfectTriadNoSeven']

        #Figures:
        self.figures[0] = notation.Notation('6,3')
        self.figures[1] = notation.Notation('5,3')

#*************************

#Create Ruleset from all these rules, add to dictionary
rules.packagedRulesets[key_name] = full_ruleset()
