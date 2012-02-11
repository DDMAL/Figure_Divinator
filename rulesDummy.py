# Rules for figuring unfigured bass parts 
# Dummy rules - coded by Mathieu (2011)

from rules import *
from music21 import interval

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
            # [0] will raise an exception for the first note as it does not have a previous note
            melodic_interval = interval.notesToChromatic(context.note,previous_notes[0])
            if not melodic_interval<=4:
                raise
            self.applicability = self.applicability_multiplier * MAX_APPLICABILITY
            self.addition = IntervalAddition(context.note,self.interval_to_add())
        except:
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
