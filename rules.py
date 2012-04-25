# Figured bass extractor rules:
# Implements basic rule class; imports specialized rule classes
# depending on what rule set was called; tests the list of rules

MIN_APPLICABILITY=0.0
MAX_APPLICABILITY=1.0

from music21 import interval

import logging_setup as Logging
LOG=Logging.getLogger('rules')

class RuleImplementationError(Exception):
    pass


class Context(object):
    def __init__(self,work_browser,note,figured_bass):
        self.work_browser = work_browser
        self.note = note
        self.note_index = self.work_browser.index_of_note(note)
        self.figured_bass = figured_bass


class Addition(object):
    def is_applicable(self,figured_bass):
        return False

    def apply(self,figured_bass):
        pass

    def cancel(self,figured_bass):
        pass


class NullAddition(Addition):
    pass


class IntervalAddition(Addition):
    def __init__(self,note,interval):
        self.note = note
        self.interval = interval

    def is_applicable(self,figured_bass):
        if figured_bass.has_interval(self.note,self.interval):
            return False
        elif figured_bass.is_full(self.note):
            return False
        else:
            return True

    def apply(self,figured_bass):
        figured_bass.add_interval(self.note,self.interval)

    def cancel(self,figured_bass):
        figured_bass.remove_interval(self.note,self.interval)


class MultipleIntervalAddition(Addition):
    def __init__(self,note,intervals):
        self.note = note
        self.intervals = intervals

    def is_applicable(self,figured_bass):
        if figured_bass.is_full(self.note):
            return False

        # True if at least one interval can be added
        for interval in self.intervals:
            if not figured_bass.has_interval(self.note,interval):
                return True
        return False

    def apply(self,figured_bass):
        for interval in self.intervals:
            if (not figured_bass.has_interval(self.note,interval) and
                    not figured_bass.is_full(self.note)):
                figured_bass.add_interval(self.note,interval)

    def cancel(self,figured_bass):
        for interval in self.intervals:
            figured_bass.remove_interval(self.note,interval)


class Rule(object):
    def __init__(self):
        self.applicability = MIN_APPLICABILITY
        self.addition = NullAddition()

    def apply(self,context):
        pass

from rulesSL import *
from rulesDummy import *

def get_rules(ruleset):
    # Put most important rules first (important = most likely to be applied)

    if ruleset[0] == "dummyrules":
        extraction_rules = [#DummySimultaneousRule(),
                            #DummyOverlappingRule(),
                            #DummyMelodicRule(),
                            DummyRule(),
                            ]

    elif ruleset[0] == "SL":
        extraction_rules = [# SLRule_test(),
                            SLRule1a(),  #needs clarification
                            SLRule1b(),  #needs clarification
                            SLRule2(),
                            SLRule3(),
                            SLRule4(),
                            SLRule5(),
                            SLRule6(),  #waiting on clarification
                            SLRule7(),
                            SLRule8(),
                            SLRule9(),
                            SLRule10(),
                            SLRule11(),
                            SLRule12(),
                            SLRule13(),
                            SLRule14(),
                            SLRule15(),
                            SLRule16(),
                            SLRule17(),
                            SLRule18(),
                            SLRule19(),
                            SLRule20(),
                            SLRule21(),  #needs clarification
                            SLRule22(),
                            SLRule23(),
                            SLRule24(),
                            SLRule25(),  #waiting on clarification
                            SLRule26(),  #waiting on clarification
                            SLRule27(),  #waiting on clarification
                            SLRule28(),  #waiting on clarification
                            #SLRuleOthers(), #empty
                            ]
    else:
        LOG.info("note: trying unique ruleset input")
        extraction_rules = []
        for rule in ruleset:
            new_rule = globals()[rule]()
            extraction_rules.append(new_rule)


    # Test the list of rules
    try:
        if not len(extraction_rules)>0:
            raise
        if not all([isinstance(x,Rule) for x in extraction_rules]):
            raise
    except:
        raise RuleImplementationError()

    return extraction_rules
