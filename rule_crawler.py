# Figured bass extractor rule crawlers:
# imports specialized rule classes
# depending on what rule set is called;
# Tests and applies the list of rules

import music21 as m21
# from rules import Rule
# from rules import Ruleset
import rules

import logging_setup as Logging
LOG = Logging.getLogger('rules')


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
    def __init__(self, extraction_work, **kwargs):
        self.score = extraction_work
        self.ruleset = []  # TODO  = kwargs.get('ruleset', [])
        #self.direction = kwargs.get('direction','backward')

        self.total_length = len(self.score._bassline.flat.getElementsByClass(m21.note.Note))
        self.rule_max = 0
        self.rule_min = 0
        self.possible_rules = [{} for i in range(self.total_length)]
        self.chosen_rules = [{} for i in range(self.total_length)]

        self._load_score()
        self._load_rules(extraction_work.ruleset)

    def full_check_rules(self):
        LOG.info("\n* * * Matching rules to score: %s * * *", self.score.title)

        #Initialize temporary variables
        L = self.rule_max
        c_start = 0

        #Loop through the entire score
        while c_start <= self.total_length - self.rule_min:
            # Make sure length of score isn't exceeded by length of rules
            while c_start + L > self.total_length:
                L = L - 1

            #Create chunk and it's possible rule array
            chunk = self._chunkify(c_start, c_start + L)
            poss_rules = self.possible_rules[c_start]

            #Test each rule in the ruleset on it
            for rule in self.ruleset:
                if rule.size <= L:
                    if not self.test_rule(chunk, rule):
                        continue

                    LOG.info('  Passes: Rule %s (length %s).',
                        rule.__class__.__name__, str(rule.size))

                    #Add figures to dictionary
                    poss_rules[rule] = rule.figures

            #If the chunk didn't get any rules, say so
            if len(poss_rules) == 0:
                LOG.info('  Passed no rules.')

            #Increase start index
            c_start = c_start + 1

        #Return possible rules to the original score
        self.score.possible_rules = self.possible_rules

    def full_apply_rules(self):
        LOG.info("\n* * * Rule Selection/Application * * *")
        c_start = 0  # TODO -- go through all chunks, not just first one! :)

        #For the entirety of the piece...
        while c_start < self.total_length:
            poss_rules = self.possible_rules[c_start]

            #Is there a choice of rules at this start?
            if len(poss_rules) > 0:

                #Determine which rule to actually apply to the chunk
                while len(poss_rules) > 1:
                    ruleA = poss_rules.keys()[0]
                    ruleB = poss_rules.keys()[1]
                    winner, loser = rules.compare_rules(ruleA, ruleB)
                    del poss_rules[loser]

                #Remaining rule is the chosen rule
                this_rule = poss_rules.keys()[0]
                these_figures = poss_rules.values()[0]
                self.chosen_rules[c_start] = poss_rules  # TODO-check_back
                LOG.info('@Note index %s: Applied %s.',
                            str(c_start), this_rule.__class__.__name__)

                #Apply it to the score
                for x in range(len(these_figures)):
                    if these_figures[x]:
                        try:
                            self.score._fb_figureString[c_start + x] = these_figures[x].notationColumn
                        except AttributeError as e:
                            print e
                            print 'split note? ' + str(these_figures[x])
                        #TODO - deal with split notes

                #Increase start index by length of applied rule
                c_start = c_start + this_rule.size
            else:
                #LOG.info("@Note index %s: No rule to apply.", str(c_start))
                #Increase start index by one
                c_start = c_start + 1

        LOG.info("\n* * * * * * * * * * * * * *.")
        self.score.chosen_rules = self.chosen_rules


    def _load_score(self):
        self.total_length = len(self.score._bassline.flat.getElementsByClass(m21.note.Note))
        self.rule_min = self.total_length

    def _load_rules(self, incomingrules):
        self.ruleset = rules.get_ruleset(incomingrules).rulelist
        self.score._allrules = self.ruleset  # Save to orig score, too.
        self.rule_max, self.rule_min = rules.rule_max_min(self.ruleset)



    def _chunkify(self, start_index, end_index):
        L = end_index - start_index
        bassfull = self.score._bassline.flat.getElementsByClass(m21.note.Note)
        chunk = bassfull[start_index:end_index]
        chunk.start_measure = chunk[0].measureNumber
        try:
            chunk.start_beat = chunk[0].beat
        except:
            chunk.start_beat = -1

        #Get intervals
        chunk.intervals = [False for x in range(L - 1)]
        for x in range(L - 1):
            chunk.intervals[x] = m21.interval.Interval(noteStart=chunk[x], noteEnd=chunk[x + 1])

        #Get beats
        chunk.beats = [-1 for x in chunk]
        for x in range(len(chunk)):
            try:
                chunk.beats[x] = chunk[x].beat
            except:
                print ("can't find a beat for the %s note of chunk starting in measure", x, chunk.start_measure)

        #Get harmonic content
        #TODO:Note - currently, only gets direct chord (not all notes until next chord)
        chunk.harmonic_content = [False for x in range(L)]
        for x in range(L):
            o = chunk[x].offset
            c = self.score._chordscore.flat.getElementsByClass(m21.chord.Chord).getElementAtOrBefore(o)
            chunk.harmonic_content[x] = c

        #Get additional info
        chunk.extras = []  # TODO-2ndTier
        chunk.figures = []  # TODO-2ndTier

        #Display output
        istring = ''
        for i in chunk.intervals:
            istring = istring + str(i.directedName)

        cstring = ''
        for i in chunk.harmonic_content:
            cstring = cstring + str(i.pitches)

        LOG.info('CHUNK@ measure %s, beat %s\n\t indecies: %s-%s \n\tintervals: %s;'
                    ' \n\t    beats: %s; \n\t   chords: %s',
                    str(chunk.start_measure), str(chunk.start_beat),
                    str(start_index), str(end_index), istring,
                    str(chunk.beats), cstring)
        return chunk

    def check_intervals(self, chunk, rule):
        #Note: currently only checks chromatic intervals
        for i in range(rule.size - 1):

            #If the rule doesn't care about this note's interval, next up!
            if not rule.intervals[i]:
                continue

            #If the chunk doesn't fit this rule's interval, return false
            if chunk.intervals[i].chromatic not in rule.intervals[i]:
                return False

        return True

    def check_qualities(self, chunk, rule):
        for i in range(rule.size):

            #If the rule doesn't care about this note's quality, next up!
            if not rule.harmonic_content[i]:
                continue

            #Easier names
            chord = chunk.harmonic_content[i]
            rules = rule.harmonic_content[i]

            chordstr = '  chord notes {'
            for x in reversed(chord.pitches):
                chordstr = chordstr + ' ' + str(x)
            chordstr = chordstr + ' }...'
            LOG.debug(chordstr)

            rbool = True
            for r in rules:
                #Based on: http://mit.edu/music21/doc/html/moduleChord.html
                #HANK! This is your bit to check.

                if r == 'isMajor':  # TODO: okay to rely on music21?
                    if not chord.quality == 'major':
                        rbool = False
                        LOG.debug('   ...don\'t pass music21\'s chord.quality==major')
                    else:
                        LOG.debug('   ...pass music21\'s chord.quality==major')

                elif r == 'isPerfect':  # TODO: okay to rely on music21?
                    if not chord.isConsonant():
                        rbool = False
                        LOG.debug('   ...don\'t pass music21\'s chord.isConsonant()')
                    else:
                        LOG.debug('   ...pass music21\'s chord.isConsonant()')

                elif r == 'hasSix':
                    #TODO: get rid of %12 semitones if direction matters!
                    invls = [m21.interval.Interval(noteStart=chunk[i], noteEnd=p).semitones % 12 for p in chord.pitches]
                    if 9 not in invls and 8 not in invls:
                        rbool = False
                        LOG.debug('   ...don\'t pass our hasSix()')
                    else:
                        LOG.debug('   ...pass our hasSix()')

                elif r == 'notHasSix':
                    #TODO: get rid of %12 semitones if direction matters!
                    invls = [m21.interval.Interval(noteStart=chunk[i], noteEnd=p).semitones % 12 for p in chord.pitches]
                    if 9 in invls or 8 in invls:
                        rbool = False
                        LOG.debug('   ...don\'t pass our notHasSix()')
                    else:
                        LOG.debug('   ...pass our notHasSix()')

                elif r == 'hasSharpSix':
                    #TODO: get rid of %12 semitones if direction matters!
                    invls = [m21.interval.Interval(noteStart=chunk[i], noteEnd=p).semitones % 12 for p in chord.pitches]
                    if not 9 in invls:
                        rbool = False
                        LOG.debug('   ...don\'t pass our hasSharpSix()')
                    else:
                        LOG.debug('   ...pass our hasSharpSix()')

                elif r == 'hasSeventh':
                    invls = [m21.interval.Interval(noteStart=chunk[i], noteEnd=p).semitones % 12 for p in chord.pitches]
                    if 10 not in invls and 11 not in invls:
                        rbool = False
                        LOG.debug('   ...don\'t pass our hasSeventh()')
                    else:
                        LOG.debug('   ...pass our hasSeventh()')

                elif r == 'hasDiminishedFifth':
                    invls = [m21.interval.Interval(noteStart=chunk[i], noteEnd=p).semitones % 12 for p in chord.pitches]
                    if 6 not in invls:
                        rbool = False
                        LOG.debug('   ...don\'t pass our hasDiminishedFifth()')
                    else:
                        LOG.debug('   ...pass our hasDiminishedFifth()')

                elif r == 'perfectMajorTriadOkSeven':  # TODO: okay to rely on music21?
                    #"chord is a Major Triad or a Dominant Seventh"
                    if not chord.canBeDominantV():
                        rbool = False
                        LOG.debug('   ...don\'t pass music21\'s chord.canBeDominantV()')
                    else:
                        LOG.debug('   ...pass music21\'s chord.canBeDominantV()')

                elif r == 'minorTriadNoSeven':  # TODO: okay to rely on music21?
                    #"chord is a minor triad, no 7"
                    if not chord.isMinorTriad():
                        rbool = False
                        LOG.debug('   ...don\'t pass music21\'s chord.isMinorTriad()')
                    else:
                        LOG.debug('   ...pass music21\'s chord.isMinorTriad()')

                elif r == 'perfectMajorTriadNoSeven':  # TODO: okay to rely on music21?
                    #"chord is a Major Triad, that is, if it contains only notes that are either in unison with the root, a major third above the root, or a perfect fifth above the root. Additionally, must contain at least one of each third and fifth above the root."
                    if not chord.isMajorTriad():
                        rbool = False
                        LOG.debug('   ...don\'t pass music21\'s chord.isMajorTriad()')
                    else:
                        LOG.debug('   ...pass music21\'s chord.isMajorTriad()')

                elif r == 'perfectTriadNoSeven':  # TODO: okay to rely on music21?
                    #"chord is a major or minor triad"
                    if not chord.canBeTonic():
                        rbool = False
                        LOG.debug('   ...don\'t pass music21\'s chord.canBeTonic()')
                    else:
                        LOG.debug('   ...pass music21\'s chord.canBeTonic()')

                else:
                    LOG.warning('Cannot yet check for rule property %s', r)

            #If the chunk doesn't fit this rule's quality, return false
            if rbool == False:
                return False

        return True

    def check_beats(self, chunk, rule):
        for i in range(rule.size):

            #If the rule doesn't care about this note's beat, next up!
            if not rule.beats[i]:
                continue

            #If the chunk doesn't fit this rule's beat needs, return false
            if chunk.beats[i] not in rule.beats[i]:
                return False

        return True

    def check_extras(self, chunk, rule):  # TODO-2ndTier-currently all false
        for i in range(rule.size):

            #If the rule doesn't care about this note's extras, next up!
            if not rule.extras[i]:
                continue

            rbool = False  # True
            for e in rule.extras[i]:

                if e == 'accidental:flat':  # TODO
                    pass
                    #if not chord.quality == 'major': rbool = False

                elif e == 'accidental:sharp':  # TODO
                    pass
                    #if not chord.quality == 'major': rbool = False

                elif e == 'scale:on5th':  # TODO
                    pass
                    #if not chord.quality == 'major': rbool = False

                elif e == 'duration:two':  # TODO  ("working hypothesis": half a measure in length or bigger or worth two of the denominator of the time signature)
                    pass
                    #if not chord.isConsonant(): rbool = False

                elif e == 'duration:lessThanPreceding':  # TODO
                    pass
                    #if not chord.isConsonant(): rbool = False

                elif e == 'duration:twicePreviousTwo':  # TODO
                    pass
                    #if not chord.isConsonant(): rbool = False

                elif e == 'duration:shortAgainstSignature':  # TODO #either only one or half of the denominator
                    pass
                    #if not chord.isConsonant(): rbool = False

                elif e == 'meter:triple':  # TODO
                    pass
                    #if not chord.isConsonant(): rbool = False

                else:
                    LOG.warning('Cannot yet check for rule extra %s', e)

            #If the chunk doesn't fit this rule's extras, return false
            if rbool == False:
                return False

        return True

    def check_pre_figures(self, chunk, rule):  # TODO-2ndTier
        """Make sure there are no conflicts with pre-existing figures."""
        return True

    def test_rule(self, chunk, rule):
        if (
            self.check_intervals(chunk, rule) and
            self.check_qualities(chunk, rule) and
            self.check_beats(chunk, rule) and
            self.check_extras(chunk, rule) and
            self.check_pre_figures(chunk, rule)
            ):
            return rule.figures
        else:
            return False

