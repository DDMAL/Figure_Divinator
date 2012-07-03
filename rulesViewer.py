"""Get and print rule information
"""

import argparse
import rules
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
parser.add_argument('-compare', action='store_true',
                    dest='compare', default=False,
                    help='Show rule comparisons?')
parser.add_argument('-r', nargs='*', dest='rules_type', default='SL', help='Set of rules to list')

#Set flags
args = parser.parse_args()
ruleSet = args.rules_type

toView = False
toCompare = args.compare

if (args.viewTodo == True or args.viewSize == True or
    args.viewIntervals == True or args.viewBeats == True or
    args.viewFigures == True or args.viewContent == True or
    args.viewExtra == True):
    toView = True


if (args.viewTodo == False and args.viewSize == False and
    args.viewIntervals == False and args.viewBeats == False and
    args.viewFigures == False and args.viewContent == False and
    args.viewExtra == False and args.compare == False):
        toView = True
        args.viewTodo = True
        args.viewSize = True
        args.viewIntervals = True
        args.viewBeats = True
        args.viewFigures = True
        args.viewContent = True
        args.viewExtra = True


# Get the extraction rules
extraction_rules = rules.get_ruleset(ruleSet).rulelist

#Are we viewing the rules?
if toView:
    #Run through and list the various qualities of the rules
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

#Are we comparing the rules?
if toCompare:
    rules.compare_rules_in_list(extraction_rules)
    LOG.info("* * DONE COMPARING RULES. * *")
