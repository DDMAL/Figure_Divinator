"""This modules searches for a good application of the figured bass extraction rules.
For now, the best implementation is a windowed greedy search.
To improve search, consider implementing other strategies.
"""

import sys
import copy

import figured_bass

# Extraction rules
import rules

from rules import MAX_APPLICABILITY
from rules import MIN_APPLICABILITY
from rules import Context


import figured_bass
from figured_bass import FiguredBass

import work_browser
from work_browser import WorkBrowser


DEFAULT_WINDOW_SIZE = 4
DEFAULT_INCREMENT = 2


class EngineParameterError(Exception):
    pass
    

class Region(object):
    """A region is simply
    a set of bass notes for which
    figures shall be extracted
    """

    def __init__(self,work_browser):
        self.work_browser = work_browser

class FigureSpaceExplorer(object):
    """This decides how
    to split-up the space of figures into
    regions, and how to proceed from
    one region to the next.
    """

    def __init__(self,work_browser):
        self.work_browser = work_browser
        self.figured_bass = None

    def initialize(self):
        self.figured_bass = FiguredBass()

    def next_region(self):
        return


class FigureExtractor(object):
    """Given a region, this
    searches for the best
    rule application for that
    region
    """

    def __init__(self,work_browser,rules):
        self.work_browser = work_browser
        self.rules = rules

    def initialize(self):
        pass


class Engine(object):
    """An engine combines a
    specific FigureSpaceExplorer
    with a specific FigureExtractor,
    resulting in a specific flavor
    of search
    """

    def __init__(self,work,rules):
        self.work_browser = WorkBrowser(work)
        self.rules = rules

        self.explorer = None
        self.extractor = None


    def compute_figured_bass(self):
        self.explorer.initialize()
        self.extractor.initialize()

        # Iterate all the regions
        for region in self.explorer.next_region():

            # For every region, extract figures and add to current figures
            self.extractor.extract(region,self.explorer.figured_bass)

        # The iteration above only stops
        # when all figures are extracted
        # (according to self.explorer criteria)

    def write_figured_bass(self,output_file_name):
        self.explorer.figured_bass.add_lyrics()
        self.work_browser.get_bass_line().write(fmt='musicxml',fp=output_file_name)


class RangeRegion(Region):
    """A range is simply a list with indices
    """

    def __init__(self,work_browser,range):
        Region.__init__(self,work_browser)
        self.range = range

    def next_note(self):
        for index in self.range:
            yield self.work_browser.note_of_index(index)

class DummyFigureSpaceExplorer(FigureSpaceExplorer):
    """The dummy figure space explorer
    simply defines the whole work as the only region
    in the space
    """

    def __init__(self,work):
        FigureSpaceExplorer.__init__(self,work)

    def initialize(self):
        FigureSpaceExplorer.initialize(self)

        self.current_region = None

    def next_region(self):
        if self.current_region is None:
            yield RangeRegion(self.work_browser,range(len(self.work_browser.bass_notes)))
        else:
            raise StopIteration


class WindowedFigureSpaceExplorer(FigureSpaceExplorer):
    """The windowed figure space explorer
    splits the bass line in overlapping windows of WINDOW_SIZE 
    notes, i.e. the extraction is done WINDOW_SIZE
    notes at a time, which speeds things up and is
    not harmful to the exploration of the search space
    is the WINDOW_SIZE is relevant to the temporal 
    dependency of rules (i.e. how 'far' a rule refers
    to past notes or future notes).
    """

    def __init__(self,work_browser):
        FigureSpaceExplorer.__init__(self,work_browser)

        self.WINDOW_SIZE = DEFAULT_WINDOW_SIZE
        self.INCREMENT = DEFAULT_INCREMENT

        self.FIRST_NOTE = 0 
        self.LAST_NOTE = len(self.work_browser.bass_notes)
 
 
    def initialize(self):
        FigureSpaceExplorer.initialize(self)

        self.previous_window_start = self.FIRST_NOTE - self.WINDOW_SIZE
        self.current_window_start = self.FIRST_NOTE - self.INCREMENT

        self.max_window_start = self.LAST_NOTE - self.WINDOW_SIZE

    def next_region(self):
        while(True):
            # Next region
            self.current_window_start = self.current_window_start + self.INCREMENT

            if self.current_window_start > self.max_window_start:
                raise StopIteration
            else:
                # Clear the figures overlap two sucessive windows
                # (these will be recomputed by for next window)
                for index in range(self.current_window_start,self.previous_window_start+self.WINDOW_SIZE):
                    self.figured_bass.clear_figure(self.work_browser.note_of_index(index))

            self.previous_window_start = self.current_window_start

            yield RangeRegion(self.work_browser,range(self.current_window_start,self.current_window_start+self.WINDOW_SIZE))


        


class GreedyFigureExtractor(FigureExtractor):
    """A greedy figure extractor:
    - Find the best rule for the given region
    - Apply the rule
    - Repeat until the region is saturated with figures
    """

    def __init__(self,work_browser,rules):
        FigureExtractor.__init__(self,work_browser,rules)

    def next_addition(self,region,figured_bass):
        """This returns
        with the best addition available
        for the current region

        Iteration stops
        when no additions are available
        """

        while(True):
            best_applicability = MIN_APPLICABILITY
            best_addition = None

            for note in region.next_note():
                if best_applicability>=MAX_APPLICABILITY:
                    break

                for rule in self.rules:
                    rule.apply(Context(self.work_browser,note,figured_bass))
                    if rule.applicability > best_applicability and rule.addition.is_applicable(figured_bass):
                        best_applicability = rule.applicability
                        best_addition = rule.addition

            if best_addition is not None:
                yield best_addition
            else:
                raise StopIteration

            
    def extract(self,region,figured_bass):
        # This returns when no additions are possible
        for addition in self.next_addition(region,figured_bass):
            addition.apply(figured_bass)


class GreedyEngine(Engine):
    """A simple greedy engine.
    This combines the dummy figure space explorer
    with the greedy figure extractor
    """
    
    def __init__(self,work,rules):
        Engine.__init__(self,work,rules)

        self.explorer = DummyFigureSpaceExplorer(self.work_browser)
        self.extractor = GreedyFigureExtractor(self.work_browser,rules)




class WindowedGreedyEngine(Engine):
    """A simple windowed greedy engine.
    This combines the windowed figure space explorer
    with the greedy figure extractor
    """

    def __init__(self,work,rules):
        Engine.__init__(self,work,rules)

        self.explorer = WindowedFigureSpaceExplorer(self.work_browser)
        self.extractor = GreedyFigureExtractor(self.work_browser,rules)



        
