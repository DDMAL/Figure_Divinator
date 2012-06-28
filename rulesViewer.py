"""Get and print rule information
"""

import argparse
import rule_crawler
import logging_setup as Logging

LOG = Logging.getLogger('rulesViewer')


class FileNotFoundError(Exception):
    pass


class InputError(Exception):
    pass

LOG.info("\n")
#Get, parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-todo', action='store_true',
                    dest='viewTodo', default=False,
                    help='Just todo')
parser.add_argument('-size', action='store_true',
                    dest='viewSize', default=False,
                    help='Just size')
parser.add_argument('-intervals', action='store_true',
                    dest='viewIntervals', default=False,
                    help='Just intervals')
parser.add_argument('-beats', action='store_true',
                    dest='viewBeats', default=False,
                    help='Just intervals')
parser.add_argument('-figures', action='store_true',
                    dest='viewFigures', default=False,
                    help='Just intervals')
parser.add_argument('-content', action='store_true',
                    dest='viewContent', default=False,
                    help='Just harmonic content')
parser.add_argument('-extras', action='store_true',
                    dest='viewExtra', default=False,
                    help='Just extras')
parser.add_argument('-r', nargs='*', dest='rules_type', default=['SL'], help='Set of rules to list')

#Set flags
args = parser.parse_args()
ruleSet = args.rules_type

if (args.viewTodo == False and args.viewSize == False and
    args.viewIntervals == False and args.viewBeats == False and
    args.viewFigures == False and args.viewContent == False and
    args.viewExtra == False):
        args.viewTodo = True
        args.viewSize = True
        args.viewIntervals = True
        args.viewBeats = True
        args.viewFigures = True
        args.viewContent = True
        args.viewExtra = True

try:
    # Get the extraction rules
    extraction_rules = rule_crawler.get_rules(ruleSet)

    rules_umbrella = ""

    for rule in extraction_rules:
        if rules_umbrella != rule.umbrella:
            rules_umbrella = rule.umbrella
            LOG.info("* * RULE SET: %s * *", rules_umbrella)

        named = False

        def not_all_false(items):
            return not all(x == False for x in items)

        if args.viewSize == True:
            if named == False:
                LOG.info("\n" + rule.__class__.__name__ + ":")
                named = True
            LOG.info("          size: " + str(rule.size))

        if args.viewIntervals == True and not_all_false(rule.intervals):
            if named == False:
                LOG.info("\n" + rule.__class__.__name__ + ":")
                named = True
            intstr = ''
            for i in range(len(rule.intervals)):
                intstr = intstr + '{'
                for j in range(len(rule.intervals[i])):
                    if j > 0:
                        intstr = intstr + ' or '
                    intstr = intstr + str(rule.intervals[i][j].simpleDirected)
                intstr = intstr + '} '
            LOG.info("     intervals: " + intstr)

        if args.viewBeats == True and not_all_false(rule.beats):
            if named == False:
                LOG.info("\n" + rule.__class__.__name__ + ":")
                named = True
            LOG.info("         beats: " + str(rule.beats))

        if args.viewContent == True and not_all_false(rule.harmonic_content):
            if named == False:
                LOG.info("\n" + rule.__class__.__name__ + ":")
                named = True
            LOG.info("      hcontent: " + str(rule.harmonic_content))

        if args.viewExtra == True and not_all_false(rule.extras):
            if named == False:
                LOG.info("\n" + rule.__class__.__name__ + ":")
                named = True
            LOG.info("         extra: " + str(rule.extras))

        if args.viewFigures == True and not_all_false(rule.figures):
            if named == False:
                LOG.info("\n" + rule.__class__.__name__ + ":")
                named = True
            try:
                figstr = '[' + rule.figures[0].notationColumn + ']'
            except:  # TODO - figure out type of exception
                figstr = '[NA]'
                for i in range(1, len(rule.figures)):
                    try:
                        figstr = figstr + '; [' + rule.figures[i].notationColumn + ']'
                    except:  # TODO - figure out type of exception
                        figstr = figstr + '; [NA]'

            LOG.info("       figures: " + figstr)

        if args.viewTodo == True and rule.todo != "undefined":
            if named == False:
                LOG.info("\n" + rule.__class__.__name__ + ":")
                named = True
            LOG.info("         to do: %s", rule.todo)

    LOG.info("* * DONE REVIEWING RULES. * *")

except rule_crawler.RuleImplementationError:
    LOG.critical("cannot find extraction rule or rules are not all valid")
    exit(1)
