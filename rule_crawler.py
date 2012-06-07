# Figured bass extractor rule crawlers:
# imports specialized rule classes
# depending on what rule set is called;
# Tests and applies the list of rules

from music21 import interval
from music21 import note
from music21 import chord
from rules import Rule

import logging_setup as Logging
LOG=Logging.getLogger('rules')


#* * *IMPORT ALL POSSIBLE RULESETS* * *
import ruleset_SL as SL
import ruleset_octave as octave

class RuleImplementationError(Exception):
    pass

#Get specific rules
def get_rules(ruleset):

    if ruleset[0] == "SL":
        extraction_rules = SL.all_rules()

    elif ruleset[0] == "octave":
        extraction_rules = octave.all_rules()

    else:
        LOG.info("note: trying unique ruleset input")
        extraction_rules = []
        for rule in ruleset:
            try:
                new_rule = globals()[rule]()
                extraction_rules.append(new_rule)
            except:
                raise RuleImplementationError()

    # Test the list of rules (make sure they're all rules!)
    try:
        if not len(extraction_rules)>0:
            raise
        if not all([isinstance(x,Rule) for x in extraction_rules]):
            raise
    except:
        raise RuleImplementationError()

    return extraction_rules


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
        poss_rules = {}

        #Test each rule in the ruleset on it
        for rule in self.ruleset:
            if rule.size == L:
                if not self.test_rule(chunk,rule): continue

                LOG.info('  Passes: Rule %s.',
                    rule.__class__.__name__)

                #Add figures to dictionary
                poss_rules[rule] = rule.figures

        #If the chunk didn't get any rules, our work is done here
        if len(poss_rules)==0:
            LOG.info('  Passed no rules, applying no figures.')
            return

        #Determine which rule to actually apply to the chunk
        while len(poss_rules) > 1:
            ruleA = poss_rules.keys()[0]
            ruleB = poss_rules.keys()[1]
            winner,loser = self.compare_rules(ruleA,ruleB)
            del poss_rules[loser]
        this_rule = poss_rules.keys()[0]
        these_figures = poss_rules.values()[0]
        LOG.info('  Applied %s.',
                    this_rule.__class__.__name__)

        #Apply it
        for x in range(len(these_figures)):
            if these_figures[x]:
                try:
                    self.score._fb_figureString[c_start+x] = these_figures[x].notationColumn
                except:
                    print 'split note? ' + str(these_figures[x])
                #TODO - deal with split notes


    def compare_rules(self,ruleA,ruleB):
        #NOTE: right now, gives winner and loser
        #TODO: needs to take into account figure equivalences
        #TODO: assumes rules are same length

        loser = False
        winner = False
        reason = ''
        decision = False

        #Make sure they aren't mutually exclusive
        #TODO

        #Check to see if one is more specific than another!
        #Count things:
        dictA = {}
        dictB = {}
        dictA['intervals'] = sum(x > 0 for x in ruleA.intervals)
        dictB['intervals'] = sum(x > 0 for x in ruleB.intervals)
        dictA['beats'] = sum(x > 0 for x in ruleA.beats)
        dictB['beats'] = sum(x > 0 for x in ruleB.beats)
        dictA['content'] = sum(x > 0 for x in ruleA.harmonic_content)
        dictB['content'] = sum(x > 0 for x in ruleB.harmonic_content)
        dictA['extras'] = sum(x > 0 for x in ruleA.extras)
        dictB['extras'] = sum(x > 0 for x in ruleB.extras)

        #If they don't have the same number, preference the winner
        if dictA['intervals'] > dictB['intervals']:
            winner = ruleA
            loser = ruleB
            reason += "more interval restrictions"
            decision = True
        elif dictA['intervals'] < dictB['intervals']:
            winner = ruleB
            loser = ruleA
            reason += "more interval restrictions"
            decision = True

        if dictA['beats'] > dictB['beats']:
            if decision == False:
                winner = ruleA
                loser = ruleB
                reason += "more beat restrictions"
                decision = True
            else:
                reason += " (not included: beat restrictions)"
        elif dictA['beats'] < dictB['beats']:
            if decision == False:
                winner = ruleB
                loser = ruleA
                reason += "more beat restrictions"
                decision = True
            else:
                reason += " (not included: beat restrictions)"

        if dictA['content'] > dictB['content']:
            if decision == False:
                winner = ruleA
                loser = ruleB
                reason += "more harmonic content restrictions"
                decision = True
            else:
                reason += " (not included: content restrictions)"
        elif dictA['content'] < dictB['content']:
            if decision == False:
                winner = ruleB
                loser = ruleA
                reason += "more harmonic content restrictions"
                decision = True
            else:
                reason += " (not included: content restrictions)"

        if dictA['extras'] > dictB['extras']:
            if decision == False:
                winner = ruleA
                loser = ruleB
                reason += "more extras restrictions"
                decision = True
            else:
                reason += " (not included: extras restrictions)"
        elif dictA['extras'] < dictB['extras']:
            if decision == False:
                winner = ruleB
                loser = ruleA
                reason += "more extras restrictions"
                decision = True
            else:
                reason += " (not included: extras restrictions)"

        if decision == False:
            loser = ruleB
            winner = ruleA
            reason = 'random assignment'

        LOG.info(' Compared %s and %s:',
                    ruleA.__class__.__name__, ruleB.__class__.__name__,)
        LOG.info('   %s trumps because of %s.',
                    winner.__class__.__name__, reason)

        return winner, loser

    def _load_score(self):
        self.total_length = len(self.score._bassline.flat.getElementsByClass(note.Note))
        self.rule_min = self.total_length

    def _load_rules(self,incomingrules):
        self.ruleset = get_rules(incomingrules)
        for rule in self.ruleset:
            if rule.size > self.rule_max: self.rule_max = rule.size
            if rule.size < self.rule_min: self.rule_min = rule.size

    def _chunkify(self,start_index,end_index):
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

        LOG.info('CHUNK@ %s-%s (%s): \n\tintervals: %s; \n\t    beats: %s; \n\t   chords: %s', str(start_index), str(end_index), str(L), istring,
                    str(chunk.beats),
                    cstring)
        return chunk

    def check_intervals(self,chunk,rule):
        #Note: currently only checks chromatic intervals
        for i in range(rule.size - 1):

            #If the rule doesn't care about this note's interval, next up!
            if not rule.intervals[i]: continue

            #If the chunk doesn't fit this rule's interval, return false
            if chunk.intervals[i].chromatic not in rule.intervals[i]: return False

        return True

    def check_qualities(self,chunk,rule):
        for i in range(rule.size):

            #If the rule doesn't care about this note's quality, next up!
            if not rule.harmonic_content[i]: continue

            #Easier names
            chord = chunk.harmonic_content[i]
            rules = rule.harmonic_content[i]

            rbool = True
            for r in rules:
                #Based on: http://mit.edu/music21/doc/html/moduleChord.html
                #HANK! This is your bit to check.

                if r == 'isMajor': #TODO: okay to rely on music21?
                    if not chord.quality == 'major': rbool = False

                elif r== 'isPerfect': #TODO: okay to rely on music21?
                    if not chord.isConsonant(): rbool = False

                elif r == 'hasSix':
                    #TODO: get rid of %12 semitones if direction matters!
                    invls = [interval.Interval(noteStart=chunk[i],noteEnd=p).semitones%12 for p in chord.pitches]
                    if 9 not in invls and 8 not in invls: rbool = False

                elif r == 'notHasSix':
                    #TODO: get rid of %12 semitones if direction matters!
                    invls = [interval.Interval(noteStart=chunk[i],noteEnd=p).semitones%12 for p in chord.pitches]
                    if 9 in invls or 8 in invls: rbool = False

                elif r == 'hasSharpSix':
                    #TODO: get rid of %12 semitones if direction matters!
                    invls = [interval.Interval(noteStart=chunk[i],noteEnd=p).semitones%12 for p in chord.pitches]
                    if not 9 in invls: rbool = False

                elif r == 'hasSeventh':
                    invls = [interval.Interval(noteStart=chunk[i],noteEnd=p).semitones%12 for p in chord.pitches]
                    if 10 not in invls and 11 not in invls: rbool = False

                elif r == 'hasDiminishedFifth':
                    invls = [interval.Interval(noteStart=chunk[i],noteEnd=p).semitones%12 for p in chord.pitches]
                    if 6 not in invls: rbool = False

                elif r == 'perfectMajorTriadOkSeven': #TODO: okay to rely on music21?
                    #"chord is a Major Triad or a Dominant Seventh"
                    if not chord.canBeDominantV(): rbool = False

                elif r == 'minorTriadNoSeven': #TODO: okay to rely on music21?
                    #"chord is a minor triad, no 7"
                    if not chord.isMinorTriad(): rbool = False

                elif r == 'perfectMajorTriadNoSeven': #TODO: okay to rely on music21?
                    #"chord is a Major Triad, that is, if it contains only notes that are either in unison with the root, a major third above the root, or a perfect fifth above the root. Additionally, must contain at least one of each third and fifth above the root."
                    if not chord.isMajorTriad(): rbool = False

                elif r == 'perfectTriadNoSeven': #TODO: okay to rely on music21?
                    #"chord is a major or minor triad"
                    if not chord.canBeTonic(): rbool = False

                else:
                    LOG.warning('Cannot yet check for rule property %s', r)

            #If the chunk doesn't fit this rule's quality, return false
            if rbool == False: return False

        return True

    def check_beats(self,chunk,rule):
        for i in range(rule.size):

            #If the rule doesn't care about this note's beat, next up!
            if not rule.beats[i]: continue

            #If the chunk doesn't fit this rule's beat needs, return false
            if chunk.beats[i] not in rule.beats[i]: return False

        return True

    def check_extras(self,chunk,rule): #TODO-2ndTier-currently all false
        for i in range(rule.size):

            #If the rule doesn't care about this note's extras, next up!
            if not rule.extras[i]: continue

            rbool = False #True
            for e in rule.extras[i]:

                if e == 'accidental:flat': #TODO
                    pass
                    #if not chord.quality == 'major': rbool = False

                elif e == 'accidental:sharp': #TODO
                    pass
                    #if not chord.quality == 'major': rbool = False

                elif e == 'scale:on5th': #TODO
                    pass
                    #if not chord.quality == 'major': rbool = False

                elif e == 'duration:two': #TODO  ("working hypothesis": half a measure in length or bigger or worth two of the denominator of the time signature)
                    pass
                    #if not chord.isConsonant(): rbool = False

                elif e == 'duration:lessThanPreceding': #TODO
                    pass
                    #if not chord.isConsonant(): rbool = False

                elif e == 'duration:twicePreviousTwo': #TODO
                    pass
                    #if not chord.isConsonant(): rbool = False

                elif e == 'duration:shortAgainstSignature': #TODO #either only one or half of the denominator
                    pass
                    #if not chord.isConsonant(): rbool = False

                elif e == 'meter:triple': #TODO
                    pass
                    #if not chord.isConsonant(): rbool = False

                else:
                    LOG.warning('Cannot yet check for rule extra %s', e)

            #If the chunk doesn't fit this rule's extras, return false
            if rbool == False: return False

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
