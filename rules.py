MIN_APPLICABILITY=0.0
MAX_APPLICABILITY=1.0

from music21 import interval




class RuleImplementationError(Exception):
    pass


class Context(object):
    def __init__(self,work_browser,note,figured_bass):
        self.work_browser = work_browser
        self.note = note
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
            if not figured_bass.has_interval(self.note,interval) and not figured_bass.is_full(self.note):
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


class DummyRule(Rule):
    def __init__(self):
        Rule.__init__(self)

    def apply(self,context):
        self.applicability = 0.1*MAX_APPLICABILITY
        self.addition = IntervalAddition(context.note,6)


class DummyHarmonicRule(Rule):
    def __init__(self):
        Rule.__init__(self)

        # To be redefined in sub-classes
        self.applicability_multiplier = 0.0 

    def get_harmonic_notes(self,context):
        """To be re-defined in sub-classess"""

    def apply(self,context):
        # Get 'harmonic' notes (either simultaneous or overlapping notes depeding on the re-definition of get_harmonic_notes)
        harmonic_notes = self.get_harmonic_notes(context)

        harmonic_intervals = context.work_browser.get_harmonic_intervals(context.note,harmonic_notes)

        # Remove unisons (1)
        harmonic_intervals = [inter for inter in harmonic_intervals if inter != 1]

        # Remove intervals that are already present in the figured_bass
        harmonic_intervals = [inter for inter in harmonic_intervals if not context.figured_bass.has_interval(context.note,inter)]

        # Dummy rule: add any harmonic intervals
        if harmonic_intervals:
            self.applicability = self.applicability_multiplier * MAX_APPLICABILITY
            self.addition = MultipleIntervalAddition(context.note,harmonic_intervals)
        else:
            self.applicability = MIN_APPLICABILITY
            self.addition = NullAddition()


    
class DummyOverlappingRule(DummyHarmonicRule):
    """Specialize the HarmonicRule to overlapping notes"""

    def __init__(self):
        DummyHarmonicRule.__init__(self)

        self.applicability_multiplier = 0.5

    def get_harmonic_notes(self,context):
        return context.work_browser.get_overlapping_notes(context.note)        



class DummySimultaneousRule(DummyHarmonicRule):
    """Specialize the HarmonicRule to simultaneous notes"""

    def __init__(self):
        DummyHarmonicRule.__init__(self)

        # Simultaneous is weighted more than overlapping
        self.applicability_multiplier = 0.8

    def get_harmonic_notes(self,context):
        return context.work_browser.get_simultaneous_notes(context.note)        



class DummyMelodicRule(Rule):
    def __init__(self):
        Rule.__init__(self)

        self.applicability_multiplier = 1.0 

    def interval_to_add(self,context):
        # Select any harmonic interval
        harmonic_notes = context.work_browser.get_overlapping_notes(context.note)        
        harmonic_intervals = context.work_browser.get_harmonic_intervals(context.note,harmonic_notes)
        harmonic_intervals = [inter for inter in harmonic_intervals if inter != 1]
        harmonic_intervals = [inter for inter in harmonic_intervals if not context.figured_bass.has_interval(context.note,inter)]
        return harmonic_intervals[0]

    def apply(self,context):    
        # Dummy rule: if the melodic interval with previous note is <=4, add some harmonic interval
        previous_notes = context.work_browser.get_previous_notes(context.note,1)

        try:
            # This will raise an exception for the first note as it does not have a previous note
            melodic_interval = interval.notesToChromatic(context.note,previous_notes[0])
            if not melodic_interval<=4:
                raise
            self.applicability = self.applicability_multiplier * MAX_APPLICABILITY
            self.addition = IntervalAddition(context.note,self.interval_to_add())
        except:
            self.applicability = MIN_APPLICABILITY
            self.addition = NullAddition()


class SLRules(Rule):
    # Monsieur de Saint-Lambert
    # Rules for figuring unfigured bass parts (Konstantin Bozhinov - Version 1)

    def __init__(self):
        Rule.__init__(self)

        # To be redefined in sub-classes
        self.applicability_multiplier = 0.0 

    def get_harmonic_notes(self,context):
        """To be re-defined in sub-classess"""

    def apply(self,context):
        print "to implement: SL rules"
        # 1. When the bass note goes up by a semitone
        # * First note gets a 6, second nothing.
        # * Or, first gets nothing, second gets 6.

        # 2. When bass note goes down by a semitone, second note is a perfect chord and is on beat 1
        # * First note gets a 6

        # 3. When bass note goes up by a semitone and the first note has a #6
        # * Second note gets a 6

        # 4. When bass note goes down by a minor 3rd
        # * If first chord is perfect, second gets false fifth (no figure)

        # 5. When bass note goes down by a major 3rd
        # * If first note is perfect and major, second gets a 6

        # 6. When bass note goes down by a false 5th
        # * No figure ( include the b5 in second chord)

        # 7. When bass note goes up by a 3rd or 6th (of any kind)
        # * Second note gets a 6

        # 8. When bass note goes up 3 consecutive tones
        # * 1st note gets a 6
        # * 2nd note gets a 65
        # * 3rd note gets a major chord (no figure)

        # 9. When bass note goes down 3 consecutive tones and if first chord is major
        # * 2nd gets '-'
        # * 3rd gets a 6

        # 10. When bass note goes down 3 consecutive tones and the third note has a 7
        # * 1st gets no figure
        # * Second gets '-'

        # 11. When bass note goes down by a major/minor 3rd, then goes up a tone and third chord is major and is on first beat
        # * 2nd gets a 6

        # 12. When bass note goes down a minor 3rd, then goes up a semitone
        # * 1st gets perfect major chord (no figure)
        # * 2nd gets a 6
        # * 3rd gets perfect major chord (no figure)

        # 13. When bass note goes up a semitone, then goes up a 5th or down a 4th and is on 1st beat
        # * 1st gets 6 b5
        # * 2nd no figure
        # * 3rd no figure

        # 14. When bass note goes down a major 3rd, then goes up a 4th
        # * 2nd note gets a 7
        # * 3rd note gets perfect chord (no figure)

        # 15. When bass remains same for two notes and then goes up a 5th and the 3rd note is on 1st beat
        # * 1st note gets no figure
        # * 2nd note gets a 6
        # * 3rd note gets no figure

        # 16. When bass note remains same for two notes and then the 3rd goes down a 4th and is on the 1st beat
        # * 1st gets no figure
        # * 2nd gets a 6 #4
        # * 3rd gets no figure

        # 17. When bass note goes up a tone, then up a tone, then up a semitone (sol la si ut) and last note is on 1st beat
        # * 1st note gets no figure
        # * 2nd note gets a 6
        # * 3rd note gets no figure (diminished chord)
        # * 4th note gets no figure

        # 18. When bass note goes down a semitone, then down a tone, then down a tone and the last note is on 1st beat
        # * 1st note gets no figure
        # * 2nd note gets a 6
        # * 3rd note gets #6
        # * 4th note gets no figure

        # 19. When bass note goes down a tone, then down a semitone, then down a tone
        # * 1st note gets no figure
        # * 2nd note get a '-'
        # * 3rd note gets a #6
        # * 4th note gets no figure

        # 20. When bass note goes down a tone, then down a tone, then down a semitone
        # * 1st note gets no figure
        # * 2nd note gets no figure
        # * 3rd note gets a 6
        # * 4th note gets no figure

        # 21. When bass note goes down a tone, then down a semitone, then down a tone, then down a tone
        # * 1st note gets no figure
        # * 2nd note gets a 6#42 or just '-'
        # * 3rd gets a 6
        # * 4th gets a 6
        # * 5th gets no figure

        # 22. When bass note goes down a tone, then down a tone, then down a semitone, then down a tone
        # * 1st note gets no figure
        # * 2nd note gets a '-'
        # * 3rd note gets a 6
        # * 4th note gets a 6
        # * 5th note gets no figure

        # 23. When bass note goes up a tone, then up a tone, then up a semitone, then up a tone
        # * 1st note gets no figure
        # * 2nd note gets a 6
        # * 3rd note gets a 6
        # * 4th note gets a 65
        # * 5th note gets no figure

        # 24. When bass note goes up a tone, then up a semitone, then up a tone, then up a tone
        # * 1st note gets no figure
        # * 2nd note gets a #6
        # * 3rd note gets a 6
        # * 4th note gets a 65
        # * 5th note gets no figure

        # 25. When at a cadence -
        # -sol sol ut gets 4 7 no figure, respectively

        # 26. cadence - short sol ut
        # Short sol gets 7 (no 4) and ut gets no figure

        # 27. When at a cadence - long sol ut
        # * Long sol gets 4 and 7 and ut gets no figure

        # 28. When at a cadence and sol is 3 beats in 3/4 time
        # * Sol gets 4, no figure, then a 7 (respectively on each beat)


def get_rules(ruleset):

    if ruleset == "SL":
        extraction_rules = [SLRules(),
                            DummySimultaneousRule(),  # Put most important rules first (important = most likely to be applied)
                            DummyOverlappingRule(),
                            #DummyMelodicRule(),
                            DummyRule(),
                            ]
    else:
        extraction_rules = [DummySimultaneousRule(),  # Put most important rules first (important = most likely to be applied)
                            DummyOverlappingRule(),
                            #DummyMelodicRule(),
                            DummyRule(),
                            ]

    # Test the list of rules
    try:
        if not len(extraction_rules)>0:
            raise
        if not all([isinstance(x,Rule) for x in extraction_rules]):
            raise
    except:
        raise RuleImplementationError()

    return extraction_rules
