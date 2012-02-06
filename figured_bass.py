"""Module to store and save a figured bass line
"""


from rules import NullAddition

MAX_NUMBER_OF_INTERVALS = 3


class Figure(object):
    """A figure is a list of intervals"""
    def __init__(self):
        self.intervals=[]


    def sort_intervals(self):
        """Re-order the intervals
        in the way they should be printed
        """
        self.intervals.sort()
        self.intervals.reverse()

    def add_interval(self,interval):
        self.intervals.append(interval)

    def remove_interval(self,interval):
        self.intervals.remove(interval)

    def has_interval(self,interval):
        return interval in self.intervals

    def is_full(self):
        return len(self.intervals)>=MAX_NUMBER_OF_INTERVALS


class FiguredBass(object):
    """
    A figured bass line is simply a mapping of notes to figures
    """
    def __init__(self):
        self.figures = {}

    def add_interval(self,note,interval):
        if self.figures.has_key(note):
            self.figures[note].add_interval(interval)
        else:
            figure = Figure()
            figure.add_interval(interval)
            self.figures[note] = figure

    def remove_interval(self,note,interval):
        if self.figures.has_key(note):
            self.figures[note].remove_interval(interval)

    def clear_figure(self,note):
        del self.figures[note]

    def is_full(self,note):
        try:
            return self.figures[note].is_full()
        except:
            return False

    def has_interval(self,note,interval):
        try:
            return self.figures[note].has_interval(interval)
        except:
            return False

    def add_lyrics(self):
        for (note,figure) in self.figures.items():
            figure.sort_intervals()
            for interval in figure.intervals:
                note.addLyric(interval)