# #Modules to test:
# figure_extractor
# rule_crawler
# rule_plotter
# rules
# rulesViewer
# test_rulesSL?


""" Tests the most prickly functions in rules.py """
import unittest
import music21 as m21
import rules

class rulesTest(unittest.TestCase):
    """ Test that ..."""
    def setUp(self):
        self.ruleA =
        self.ruleB =

    def tearDown(self):
        pass

    def test_check_figures_coexist(self):
        assert rules.intervals_overlap(self.rulelistA, self.rulelistB)

    def test_case_2(self):
        print 'bb'
        assert self.b == 'b'


