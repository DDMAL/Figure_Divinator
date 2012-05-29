# Figured bass extractor rules:
# Implements basic rule class; imports specialized rule classes
# depending on what rule set was called; tests the list of rules

from music21 import interval
from music21 import note

import logging_setup as Logging
LOG=Logging.getLogger('rules')

class RuleImplementationError(Exception):
    pass

class Rule(object):
    def __init__(self):
        self.umbrella = "undefined"
        self.todo = "undefined"
        self.size = 0
        self.intervals = []
        self.beats = []
        self.harmonic_content = []
        self.figures = []
        self.extras = []

    def show_it_off(self):
        from pprint import pprint
        pprint (vars(self))

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

class rule_crawler(object):
    def __init__(self, extraction_work,**kwargs):
        self.score = extraction_work
        self.ruleset = []
        #self.direction = kwargs.get('direction','backward')

        self.total_length = len(self.score._bassline.flat.getElementsByClass(note.Note))
        self.rule_max = 0
        self.rule_min = 0

        self._load_score()
        self._load_rules(extraction_work.ruleset)


    def full_apply_rules(self):
        L = self.total_length 
        for rule in self.ruleset:
            if rule.size == L:
                chunk = self._chunkify(0,0+L)
                LOG.debug('Rule %s fits!', rule.__class__.__name__)
                if (self.check_intervals(chunk,rule) and 
                    self.check_beats(chunk,rule)):
                    for x in range(rule.size):
                        if rule.figures[x]:
                            self.score._fb_figureString[x] = rule.figures[x].notationColumn #TODO-wont work for larger than 2!
            else:
                pass
                #LOG.debug('Rule %s doesn\'t fit here.', rule.__class__.__name__)

    def _load_score(self):
        self.total_length = len(self.score._bassline.flat.getElementsByClass(note.Note))
        self.rule_min = self.total_length

    def _load_rules(self,incomingrules):
        self.ruleset = get_rules(incomingrules)
        for rule in self.ruleset:
            if rule.size > self.rule_max: self.rule_max = rule.size
            if rule.size < self.rule_min: self.rule_min = rule.size

    def _chunkify(self,start_index,end_index): #TODO
        L = end_index - start_index
        bassfull = self.score._bassline.flat.getElementsByClass(note.Note)
        chunk = bassfull[start_index:end_index]

        #Get intervals
        chunk.intervals = [False for x in range(L-1)]
        for x in range(L-1):
            chunk.intervals[x] = interval.Interval(noteStart=chunk[x],noteEnd=chunk[x+1])

        #Get beats
        chunk.beats = [x.beat for x in chunk]
        
        #Get harmonic content 
        #TODO:Note - currently, only gets direct chord (not all notes until next chord)
        chunk.harmonic_content = [False for x in range(L)]
        for x in range(L-1):
            chunk.harmonic_content[x] = self.score._chordscore.getElementAtOrBefore(chunk[x].offset)

        #Get additional info
        chunk.extras = [] #TODO-2ndTier
        chunk.figures = [] #TODO-2ndTier
        return chunk

    def check_intervals(self,chunk,rule):
        #Note: currently only checks chromatic intervals
        for i in range(rule.size - 1):

            #If the rule doesn't care about this note's interval, next up!
            if not rule.intervals[i]: continue

            #If the chunk doesn't fit this rule's interval, return false
            if chunk.intervals[i].chromatic not in rule.intervals[i]: return False

        return True

    def check_qualities(self,chunk,rule): #TODO
        for i in range(rule.size):

            #If the rule doesn't care about this note's quality, next up!
            if not rule.quality[i]: continue

            quality = chunk.quality[i]
            rule = rule.quality[i]

            #If the chunk doesn't fit this rule's quality, return false
            if chunk.quality[i] not in rule.quality[i]: return False
        return True
        
    def check_beats(self,chunk,rule):
        for i in range(rule.size):

            #If the rule doesn't care about this note's beat, next up!
            if not rule.beats[i]: continue

            #If the chunk doesn't fit this rule's beat needs, return false
            if chunk.beats[i] not in rule.beats[i]: return False

        return True

    def check_extra(self,chunk,rule): #TODO-2ndTier
        return True

    def check_pre_figures(self,chunk,rule): #TODO-2ndTier
        """Make sure there are no conflicts with pre-existing figures."""
        return True

    def test_rule(self,chunk,rule):
        if (
            check_intervals(chunk,rule) and
            check_qualities(chunk,rule) and
            check_beats(chunk,rule) and
            check_extras(chunk,rule) and
            check_pre_figures(chunk,rule)
            ):
            return self.figures
        else:
            return False

    def apply_figures(self,chunk,figures): #TODO - fix?
        for i in range(len(figures)):
            n = chunk._bassline.flat.getElementsByClass(note.Note)[i]
            self.score.fb.addElement(n,figures[i])
        pass

    # def apply_rules(self,where='notes'):
    #     applying = True

    #     while applying == True:

    #         #get chunk
    #         START = 1 #TODO
    #         END = 5 #TODO
    #         chunk = self.score._chunkify(START,END)
    #         if True: applying = False #todo update

    #         #for each rule in rules, try rule
    #         for rule in self.ruleset:
    #             figures = rule.test_rule(chunk)
    #             LOG.info("%s is %s at chunk for range %s - %s", rule.__class__.__name__, str(figures), str(START), str(END))
    #             if figures:
    #                 #write to notes? #write to log?
    #                 #For now, notes (make optional)
    #                 for i in range(len(figures)):
    #                     score_note_[i].addlyricssomehow(figures[i])


#* * *IMPORT ALL POSSIBLE RULESETS* * *
from ruleset_octave import *
from ruleset_SL import *

def get_rules(ruleset):
    if ruleset[0] == "SL":
        extraction_rules = [
                            SLRule_3(),
                            SLRule_5(),
                            SLRule_6(),
                            SLRule_7(),
                            SLRule_8(),
                            SLRule_9(),
                            SLRule_10a(),
                            SLRule_10b(),
                            SLRule_11(),
                            SLRule_12(),
                            SLRule_13(),
                            SLRule_14(),
                            SLRule_15(),
                            SLRule_16(),
                            SLRule_17(),
                            SLRule_18(),
                            SLRule_19(),
                            SLRule_20(),
                            SLRule_21(),
                            SLRule_22(),
                            SLRule_23(),
                            SLRule_24maybe(),
                            SLRule_25maybe(),
                            SLRule_26maybe(),
                            SLRule_27maybe(),
                            SLRule_28maybe(),
                            SLRule_29maybe(),
                            SLRule_29maybe(),
                            SLRule_30maybe(),
                            SLRule_31maybe(),
                            SLRule_32maybe(),
                            SLRule_33maybe(),
                            SLRule_34maybe()
                            ]

    elif ruleset[0] == "octave":
        extraction_rules = [octave_1(),octave_2()]

    else:
        LOG.info("note: trying unique ruleset input")
        extraction_rules = []
        for rule in ruleset:
            try:
                new_rule = globals()[rule]()
                extraction_rules.append(new_rule)
            except:
                raise RuleImplementationError()

    # Test the list of rules
    try:
        if not len(extraction_rules)>0:
            raise
        if not all([isinstance(x,Rule) for x in extraction_rules]):
            raise
    except:
        raise RuleImplementationError()

    return extraction_rules
