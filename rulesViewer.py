"""Get and print rule information
"""

import sys
import os
import argparse
import logging

import rules


import logging_setup as Logging
LOG=Logging.getLogger('rulesViewer')

class FileNotFoundError(Exception):
    pass

class InputError(Exception):
    pass

LOG.info("\n")
#Get, parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-todo', action='store_true',
                    dest='viewOutput', default=False,
                    help='Just todo')
parser.add_argument('-r', nargs='*', dest='rules_type', default=['SL'], help='Set of rules to list')

#Set flags
args = parser.parse_args()
ruleSet = args.rules_type
viewOutput = args.viewOutput

try:
    # Get the extraction rules
    extraction_rules = rules.get_rules(ruleSet)

    rules_umbrella = ""

    for rule in extraction_rules:
        if rules_umbrella != rule.umbrella:
            rules_umbrella = rule.umbrella
            LOG.info("* * RULE SET: %s * *", rules_umbrella)

        if viewOutput == True and rule.todo != "-":
            LOG.info("Rule: %s \t ...%s", rule.__class__.__name__, rule.todo)

        elif viewOutput == False:
            LOG.info("Rule: %s", rule.__class__.__name__)
            LOG.info(" .....range: %s", rule.range)
            LOG.info(" ...details: %s", rule.details)
            LOG.debug(" .....to do: %s", rule.todo)
    LOG.info("Done reviewing rules.")

except rules.RuleImplementationError:
    LOG.critical("cannot find extraction rules in rules.py or rules are not all valid")
    exit(1)
