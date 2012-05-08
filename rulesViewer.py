"""Get and print rule information
"""

import sys
import os
import argparse
import logging

import rules


import logging_setup as Logging
LOG=Logging.getLogger('rulesViewer') #TODO

class FileNotFoundError(Exception):
    pass

class InputError(Exception):
    pass

LOG.info("\n")
#Get, parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-r', nargs='*', dest='rules_type', default=['SL'], help='Set of rules to list')

#Set flags
args = parser.parse_args()
ruleSet = args.rules_type

try:
    # Get the extraction rules
    extraction_rules = rules.get_rules(ruleSet)

    rules_umbrella = ""

    for rule in extraction_rules:
        if rules_umbrella != rule.umbrella:
            rules_umbrella = rule.umbrella
            LOG.info("* * RULE SET: %s * *", rules_umbrella)

        LOG.info("Rule: %s", rule.__class__.__name__)
        LOG.info("\t...range: %s", rule.range)
        LOG.info("\t...details: %s", rule.details)
        
    print "done"

except rules.RuleImplementationError:
    LOG.critical("cannot find extraction rules in rules.py or rules are not all valid")
    exit(1)
