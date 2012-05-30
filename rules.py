# Figured bass extractor rules:
# Implements basic rule class; imports specialized rule classes
# depending on what rule set was called; tests the list of rules

from music21 import interval
from music21 import note
from music21 import chord

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
        LOG.info("\n* * * Applying rules to score: %s * * *", self.score.title)

        #Get a chunk!
        L = self.total_length #TODO - cheater method! :)
        c_start = 0
        c_end = 0+L
        chunk = self._chunkify(c_start,c_end)

        #Test each rule in the ruleset on it
        for rule in self.ruleset:
            if rule.size == L:
                if not self.test_rule(chunk,rule): continue

                LOG.info("  Passes: Rule %s, length %s.",
                    rule.__class__.__name__, str(rule.size))

                #Add figures
                for x in range(rule.size):
                    if rule.figures[x]:
                        self.score._fb_figureString[c_start+x] = rule.figures[x].notationColumn


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
        for x in range(L):
            o = chunk[x].offset
            c = self.score._chordscore.flat.getElementsByClass(chord.Chord).getElementAtOrBefore(o)
            chunk.harmonic_content[x] = c

        #Get additional info
        chunk.extras = [] #TODO-2ndTier
        chunk.figures = [] #TODO-2ndTier

        #Display output
        istring = ''
        for i in chunk.intervals: istring = istring + str(i.directedName)

        cstring = ''
        for i in chunk.harmonic_content: cstring = cstring + str(i.pitches)

        LOG.info('CHUNK@ %s: \n\t\t\t%s(intervals); \n\t\t\t%s(beats); \n\t\t\t%s(content)', str(start_index), istring,
                    str(chunk.beats),
                    cstring)
        LOG.debug('test')
        LOG.debug('eaefawefawefawe')
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
            if not rule.harmonic_content[i]: continue

            #Easier names
            notes = chunk.harmonic_content[i]
            rules = rule.harmonic_content[i]

        #     'perfect chord (major triad)'
        #     'has#6'
        #     'perfect'
        #     'perfect major triad, 7 okay'
        #     'perfect major triad, no 7'
        #     'perfect major or minor triad no 7'
        #     'has 7'
        #     'major'
        #     'has a diminished 5'


            #If the chunk doesn't fit this rule's quality, return false
            rbool = True

            for r in rules:
                # if r == 'containsSeventh':
                #     if not notes.containsSeventh(): rbool = False
                # elif r == 'isSeventh':
                #         if not notes.isSeventh(): rbool = False
                if r == 'hasSharpSix':
                    #Note: substitute "intervalClass" for "semitones" if direction invariant
                    #Store the semitones in the interval for comparison
                    invls = [interval.Interval(noteStart=chunk[i],noteEnd=p).semitones%12 for p in notes.pitches]
                    if not 9 in invls: rbool = False
                # elif r == 'canBeDominantV':
                #     #Returns true if the chord is a major triad or a dominant seventh
                #     if not quality.canBeDominantV(): rbool = False
                # elif r == 'isMajorTriad':
                #     if not quality.canBeDominantV(): rbool = False

            if rbool == False: return False

        return True

    def check_beats(self,chunk,rule):
        for i in range(rule.size):

            #If the rule doesn't care about this note's beat, next up!
            if not rule.beats[i]: continue

            #If the chunk doesn't fit this rule's beat needs, return false
            if chunk.beats[i] not in rule.beats[i]: return False

        return True

    def check_extras(self,chunk,rule): #TODO-2ndTier
        return True

    def check_pre_figures(self,chunk,rule): #TODO-2ndTier
        """Make sure there are no conflicts with pre-existing figures."""
        return True

    def test_rule(self,chunk,rule):
        if (
            self.check_intervals(chunk,rule) and
            self.check_qualities(chunk,rule) and
            self.check_beats(chunk,rule) and
            self.check_extras(chunk,rule) and
            self.check_pre_figures(chunk,rule)
            ):
            return rule.figures
        else:
            return False


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
