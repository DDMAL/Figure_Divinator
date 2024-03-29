# Copyright (C) 2012 by Hannah Robertson
"""
This module sets up rules and sets of rules, as well rule comparison functions.

In addition, upon import it loads all pre-made rule sets stored in the
``rulesets`` directory.

"""

import os
import logging_setup as Logging
import logging
import music21 as m21

LOG = Logging.getLogger('rules')

packagedRulesets = {}
full_rule_dictionary = {}
extraCheck_dictionary = {}
harmonyCheck_dictionary = {}


class Rule(object):
    """
    The parent class for all Figure Divination Rule objects.

    """
    def __init__(self):
        self.umbrella = "undefined"
        self.todo = "undefined"
        self.size = 0
        self.intervals = []
        self.beats = []
        self.harmonic_content = []
        self.figures = []
        self.extras = []

    def _show_it_off(self):
        from pprint import pprint
        #a rule's name is stored in self.__class__.__name__
        pprint(str(self.__class__.__name__))
        pprint(vars(self))


class Ruleset(object):
    """
    A class for managing a list of figure divination Rule objects.

    In addition, a Ruleset manages interactions between all of the rules it
    contains.

    kwargs:
        **name**: (Optional) The name of the rule set (default 'Unique Rule Set').

        **metadata**: (Optional) A dictionary that holds additional information about the set.

        **from_module**: (Optional) Only set as true if Ruleset is created from a script in the ``ruleset`` directory (default False).

    """
    def __init__(self, rules, **kwargs):
        self.rulelist = []
        self.name = kwargs.get('name', 'Unique Rule Set')
        self.metadata = kwargs.get('metadata', {})
        self.coexistence_array = False
        self.dominance_array = False
        load = kwargs.get('from_module', False)

        # Load is true if this ruleset is being built from a module script
        if load:
            self.rulelist = rules

        # Otherwise, ruleset is being built from a list of individual rules
        else:
            for r in rules:
                try:
                    rule = full_rule_dictionary[r]
                    new_rule = rule()
                    self.rulelist.append(new_rule)
                except Exception:
                    LOG.info("Sorry, '" + r + "'' doesn't register as a rule...")

        #Compare all rules (while suppressing output)
        oldLog = LOG.level
        LOG.setLevel(logging.CRITICAL)
        self.coexistence_array, self.dominance_array = compare_rules_in_list(self.rulelist)
        LOG.setLevel(oldLog)


def get_ruleset(input_item):
    """
    Returns a Ruleset object when given Ruleset id key or list of rules.

    input_item can be an id string, e.g. ``get_ruleset('SL')``, or an array of rule
    names, e.g. ``get_ruleset(['SLRule_03', 'SLRule_08a'])``.

    """
    try:
        return packagedRulesets[input_item]

    except:
        #Perhaps key has been stored in an array rather than as just a string...
        try:
            return packagedRulesets[input_item[0]]

        #If input is list of rules, rather than a key, make a new ruleset
        except:
            return Ruleset(input_item)


def compare_rules_in_list(rule_list):
    """
    Returns coexistence and dominance interaction arrays from a list of rules.

    """
    #Create filler return array
    coexistence_array = {}
    dominance_array = {}
    for ruleA in rule_list:
        LOG.info("* * * * *\n\t\tRule %s...", ruleA.__class__.__name__)
        coexistence_array[ruleA] = []
        dominance_array[ruleA] = []

        #Compare with every other rule
        otherRules = [i for i in rule_list if i != ruleA]
        for ruleB in otherRules:
            LOG.info("...compared with rule %s:", ruleB.__class__.__name__)

            #...at every offset:
            min_overlap_index = -1 * (ruleB.size - 1)
            max_overlap_index = ruleA.size
            for offset in range(min_overlap_index, max_overlap_index):
                if offset < 0:
                    indA = 0
                    indB = offset * -1
                elif offset == 0:
                    indA = 0
                    indB = 0
                else:
                    indA = offset
                    indB = 0

                #Figure out if they can coexist
                if not check_rules_coexist(ruleA, ruleB, indexA=indA, indexB=indB):
                    LOG.info("\t\tMutually exclusive (offset " + str(offset) + ").")
                    continue

                #Figure out if they conflict or coexist
                coexist_type = 'coexist'
                if not check_figures_coexist(ruleA, ruleB, indexA=indA, indexB=indB):
                    coexist_type = 'conflict'
                    LOG.info("\t\tConflicts (offset " + str(offset) + ")!")
                else:
                    LOG.info("\t\tCoexists (offset " + str(offset) + ").")
                coexistence_array[ruleA].append((ruleB, offset, coexist_type))

            #Figure out which rule wins
            #winner, loser = compare_rules(ruleA, ruleB)
            #print ("Rule %s wins")  # TODO - save this thing

    return coexistence_array, dominance_array


def check_figures_coexist(ruleA, ruleB, indexA=0, indexB=0):
    """
    Returns true if rules' figures are identical over length of their overlap.

    Args:
        **ruleA**: First rule to compare.

        **ruleB**: Second rule to compare.

        **indexA**: (Optional) Starting index of ruleA (default 0).

        **indexB**: (Optional) Starting index of ruleB (default 0).

    """
    #Figure out the length to be compared
    overlap_length = min(ruleA.size - indexA, ruleB.size - indexB)

    #For each step compared, check the figure:
    for i in range(overlap_length):
        if ruleA.figures[indexA + i] and ruleB.figures[indexB + i]:

            try:
                figA = ruleA.figures[indexA + i][1].notationColumn
            except:
                figA = ruleA.figures[indexA + i].notationColumn
            try:
                figB = ruleB.figures[indexB + i][1].notationColumn
            except:
                figB = ruleB.figures[indexB + i].notationColumn

            if figA != figB:
                return False
    return True


def check_rules_coexist(ruleA, ruleB, indexA=0, indexB=0):
    """
    Returns true if both rules are applicable over length of their overlap.

    Args:
        **ruleA**: First rule to compare.

        **ruleB**: Second rule to compare.

        **indexA**: (Optional) Starting index of ruleA (default 0).

        **indexB**: (Optional) Starting index of ruleB (default 0).

    """

    #Figure out the length to be compared
    overlap_length = min(ruleA.size - indexA, ruleB.size - indexB)

    #For each step compared, check the interval:
    for i in range(overlap_length - 1):
        if (ruleA.intervals[indexA + i] and ruleB.intervals[indexB + i] and not
            intervals_overlap(ruleA.intervals[indexA + i], ruleB.intervals[indexB + i])):
            return False

    # For each rule note compared, check...
    for i in range(overlap_length):

        # ...beats:
        if (ruleA.beats[indexA + i] and ruleB.beats[indexB + i] and not
            lists_overlap(ruleA.beats[indexA + i], ruleB.beats[indexB + i])):
            return False

        # ...harmonic content:
        if (ruleA.harmonic_content[indexA + i] and ruleB.harmonic_content[indexB + i]):
            for a in ruleA.harmonic_content[indexA + i]:
                #If it is mutually exclusive with any in b, return false
                if not lists_overlap(harmonyCheck_dictionary[a], ruleB.harmonic_content[indexB + i]):
                    return False

        # ...extras:
        if ruleA.extras[indexA + i] and ruleB.extras[indexB + i]:
            #for each extra in A...
            for a in ruleA.extras[indexA + i]:
                #If it is mutually exclusive with any in b, return false
                if lists_overlap(extraCheck_dictionary[a], ruleB.extras[indexB + i]):
                    return False

    return True


def lists_overlap(listA, listB):
    """
    Returns true if the two lists intersect.

    """
    return bool(set(listA) & set(listB))


def intervals_overlap(intlistA, intlistB):
    """
    Returns true if the two lists of :mod:`music21` intervals intersect.

    This function checks for equivalence among any combination of the three
    :mod:`music21` interval classes: :class:`music21.interval.Interval`,
    :class:`music21.interval.diatonicInterval`, and
    :class:`music21.interval.chromaticInterval`.

    """
    for a in intlistA:
        for b in intlistB:

            #If they're the same...
            if a.__class__ == b.__class__:
                A = a
                B = b

            #Else, if one is interval and the other is diatonic...
            elif ((a.__class__ == m21.interval.Interval or
                    b.__class__ == m21.interval.Interval) and
                    (a.__class__ == m21.interval.diatonicInterval or
                    b.__class__ == m21.interval.diatonicInterval)):
                A = a.generic
                B = b.generic

            #Else, if one is interval and the other is chromatic
            elif ((a.__class__ == m21.interval.Interval or
                    b.__class__ == m21.interval.Interval) and
                    (a.__class__ == m21.interval.chromaticInterval or
                    b.__class__ == m21.interval.chromaticInterval)):
                A = a.semitones
                B = b.semitones

            #Else, one is chromatic and the other is diatonic
            else:
                try:
                    A = a.getDiatonic()
                    B = b
                except:
                    A = a
                    B = b.getDiatonic()

            #check them
            if A == B:
                #LOG.debug("Interval overlap check: Between %s and %s an intersection was found at %s and %s.",
                          #intlistA, intlistB, a, b)
                return True

    #If no overlaps have been found, return false
    #LOG.debug("Interval overlap check: Between %s and %s no intersection was found.", intlistA, intlistB)
    return False


def compare_rules(ruleA, ruleB):
    """
    Returns (winner, loser) of two rules, based on numbers of restrictions.

    Note: an extremely coarse comparison.

    """
    #NOTE: right now, gives winner and loser
    #TODO: needs to take into account figure equivalences
    #TODO: assumes rules are same length

    loser = False
    winner = False
    reason = ''
    decision = False

    #Check to see if one is longer than another (assumed more specific)
    if ruleA.size > ruleB.size:
        winner = ruleA
        loser = ruleB
    elif ruleA.size < ruleB.size:
        winner = ruleB
        loser = ruleA

    #Check to see if one is more specific than another!
    #Count things:
    dictA = {}
    dictB = {}
    dictA['intervals'] = sum(x > 0 for x in ruleA.intervals)
    dictB['intervals'] = sum(x > 0 for x in ruleB.intervals)
    dictA['beats'] = sum(x > 0 for x in ruleA.beats)
    dictB['beats'] = sum(x > 0 for x in ruleB.beats)
    dictA['content'] = sum(x > 0 for x in ruleA.harmonic_content)
    dictB['content'] = sum(x > 0 for x in ruleB.harmonic_content)
    dictA['extras'] = sum(x > 0 for x in ruleA.extras)
    dictB['extras'] = sum(x > 0 for x in ruleB.extras)

    #If they don't have the same number, preference the winner
    if dictA['intervals'] > dictB['intervals']:
        winner = ruleA
        loser = ruleB
        reason += "more interval restrictions"
        decision = True
    elif dictA['intervals'] < dictB['intervals']:
        winner = ruleB
        loser = ruleA
        reason += "more interval restrictions"
        decision = True

    if dictA['beats'] > dictB['beats']:
        if decision == False:
            winner = ruleA
            loser = ruleB
            reason += "more beat restrictions"
            decision = True
        else:
            reason += " (not included: beat restrictions)"
    elif dictA['beats'] < dictB['beats']:
        if decision == False:
            winner = ruleB
            loser = ruleA
            reason += "more beat restrictions"
            decision = True
        else:
            reason += " (not included: beat restrictions)"

    if dictA['content'] > dictB['content']:
        if decision == False:
            winner = ruleA
            loser = ruleB
            reason += "more harmonic content restrictions"
            decision = True
        else:
            reason += " (not included: content restrictions)"
    elif dictA['content'] < dictB['content']:
        if decision == False:
            winner = ruleB
            loser = ruleA
            reason += "more harmonic content restrictions"
            decision = True
        else:
            reason += " (not included: content restrictions)"

    if dictA['extras'] > dictB['extras']:
        if decision == False:
            winner = ruleA
            loser = ruleB
            reason += "more extras restrictions"
            decision = True
        else:
            reason += " (not included: extras restrictions)"
    elif dictA['extras'] < dictB['extras']:
        if decision == False:
            winner = ruleB
            loser = ruleA
            reason += "more extras restrictions"
            decision = True
        else:
            reason += " (not included: extras restrictions)"

    if decision == False:
        loser = ruleB
        winner = ruleA
        reason = 'arbitrary assignment'

    LOG.info('  Compared %s and %s:',
                ruleA.__class__.__name__, ruleB.__class__.__name__,)
    LOG.info('    %s trumps because of %s.',
                winner.__class__.__name__, reason)

    return winner, loser


def rule_max_min(rule_list):
    """
    Returns max, min rule lengths of a list of rules.

    """
    maxsize = rule_list[0].size
    minsize = rule_list[0].size
    for rule in rule_list:
        if rule.size > maxsize:
            maxsize = rule.size
        if rule.size < minsize:
            minsize = rule.size
    return maxsize, minsize


# For each possible "extra" that a rule could contain,
# a list of the other extras that it CANNOT coexist with
extraCheck_dictionary = {
    'accidental:flat': ['accidental:sharp'],
    'accidental:sharp': ['accidental:flat'],
    'duration:lessThanPreceding': ['duration:twiceAsPreviousTwo'],
    'duration:twiceAsPreviousTwo': ['duration:lessThanPreceding'],
    'scale:on5th': [],
    'duration:two': [],
    'duration:shortAgainstSignature': [],
    'meter:triple': []
    }

# For each possible "extra" that a rule could contain,
# a list of the other extras that it CAN coexist with
# TODO - Hank, these need checking!
harmonyCheck_dictionary = {
    'isMajor': [],
    'isPerfect': [],
    'hasSix': [],
    'notHasSix': [],
    'hasSharpSix': [],
    'hasSeventh': ['perfectMajorTriadOkSeven'],
    'hasDiminishedFifth': [],
    'perfectMajorTriadOkSeven': ['hasSeventh'],
    'minorTriadNoSeven': ['perfectTriadNoSeven'],
    'perfectMajorTriadNoSeven': ['perfectTriadNoSeven'],
    'perfectTriadNoSeven': ['minorTriadNoSeven', 'perfectMajorTriadNoSeven']
    }

# Upon loading, auto-import all the rule sets in the 'rulesets' directory:
for filename in os.listdir('rulesets'):
    if (filename == 'ruleset_template.py' or
        filename[-3:] != '.py' or filename == '__init__.py'):
        continue
    filename = 'rulesets.' + filename
    module = __import__(filename[:-3], locals(), globals())
