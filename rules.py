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


    

def get_rules():
    extraction_rules = [DummySimultaneousRule(),  # Put most important rules first (important = most likely to be applied)
                        DummyOverlappingRule(),
                        DummyMelodicRule(),
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
