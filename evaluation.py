"""This evaluates the quality
of a figured bass for a region.

The search engine will call this to determine:

 - When to stop searching (self.accept = True)
 - When to disregard a figured bass (self.reject = True)
 - How good a partial figured bass is (self.quality), i.e. should we continue
 searching in that direction
"""

import logging_setup as Logging
LOG=Logging.getLogger('evaluation')

MIN_QUALITY=0.0
MAX_QUALITY=1.0


class Evaluator(object):

    def __init__(self,work_browser):
        self.work_browser = work_browser

        self.region = None
        self.figured_bass = None

        # Estimation of the quality of a partial or complete figured bass
        self.quality = MIN_QUALITY

        # Should the figured bass be accepted as such?
        # This will prompt the engine to stop searching
        # and use the evaluated figured bass as the result
        self.accept = False

        # Should be figured to be rejected?
        # This will prompt the engine to disregard
        # the evaluated figured bass in its search
        self.reject = False


    def evaluate(self,region,figured_bass):
        pass
