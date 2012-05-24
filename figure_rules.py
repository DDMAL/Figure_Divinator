# Figured bass extractor rules:
# Implements basic rule class; imports specialized rule classes
# depending on what rule set was called; tests the list of rules

#from music21 import interval

import logging_setup as Logging
LOG=Logging.getLogger('rules')

# class RuleImplementationError(Exception):
#     pass

class Rule(object):
    def __init__(self):
        self.umbrella = "undefined"
        self.todo = "undefined"

    # def apply(self,context):
    #     pass

#from rulesSL import *
#from rulesDummy import *

# def get_rules(ruleset):
#     if ruleset[0] == "dummyrules":
#         extraction_rules = [
#                             DummyRule(),
#                             ]

#     elif ruleset[0] == "SL":
#         extraction_rules = [# SLRule_test(),
#                             SLRuleImplicit_1(),
#                             SLRule1a(),
#                             SLRule1b(),
#                             SLRule2(),
#                             SLRule3(),
#                             SLRule4(),
#                             SLRule5(),
#                             SLRule6(),
#                             SLRule7(),
#                             SLRule8(),
#                             SLRule9(),
#                             SLRule10(),
#                             SLRule11(),
#                             SLRule12(),
#                             SLRule13(),
#                             SLRule14(),
#                             SLRule15(),
#                             SLRule16(),
#                             SLRule17(),
#                             SLRule18(),
#                             SLRule19(),
#                             SLRule20(),
#                             SLRule21(),
#                             SLRule22(),
#                             SLRule23(),
#                             SLRule24(),
#                             SLRule25(),
#                             SLRule26(),
#                             SLRule27(),
#                             SLRule28(),
#                             ]
#     else:
#         LOG.info("note: trying unique ruleset input")
#         extraction_rules = []
#         for rule in ruleset:
#             new_rule = globals()[rule]()
#             extraction_rules.append(new_rule)


#     # Test the list of rules
#     try:
#         if not len(extraction_rules)>0:
#             raise
#         if not all([isinstance(x,Rule) for x in extraction_rules]):
#             raise
#     except:
#         raise RuleImplementationError()

#     return extraction_rules