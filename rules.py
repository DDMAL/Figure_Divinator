# Figured bass extractor rules:
# basic rule class; tests the list of rules
import os

packagedRulesets = {}
full_rule_dictionary = {}


class Rule(object):
    def __init__(self):
        self.umbrella = "undefined"
        self.todo = "undefined"
        self.size = 0
        self.intervals = []
        self.beats = []
        self.harmonic_content = []
        self.figures = []
        self.extras = []

    def show_it_off(self):
        from pprint import pprint
        pprint(vars(self))


class Ruleset(object):
    def __init__(self, rules, **kwargs):
        self.rulelist = []
        self.name = kwargs.get('name', 'Unique Rule Set')
        self.metadata = kwargs.get('metadata', {})
        load = kwargs.get('from_module', False)

        # Load is true if this ruleset is being built from a module script
        if load:
            self.rulelist = rules

        # Otherwise, ruleset is being built from individual rules
        else:
            for r in rules:
                try:
                    rule = full_rule_dictionary[r]
                    new_rule = rule()
                    self.rulelist.append(new_rule)
                except Exception:
                    print "Sorry, '" + r + "'' doesn't register as a rule..."

    def check_validity(self):
        pass  # TODO: make sure all rules are valid


def get_ruleset(input_item):
    """
    Given the key to a packaged rule set or a list of rules,
    return (or create and then return) a rule set.
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
    '''
    For each rule in set, compare with each other rule in set.
    '''
    #Create filler return array
    #returnArray = {}
    for ruleA in rule_list:
        LOG.info("Rule %s...", ruleA.__class__.__name__)

        #Compare with every other rule
        otherRules = [i for i in rule_list if i != ruleA]
        for ruleB in otherRules:
            LOG.info("...compared with rule %s:", ruleB.__class__.__name__)

            #Figure out if they can coexist
            if not check_rules_coexist(ruleA, ruleB):
                print ("\t\tMutually exclusive")  # TODO - save this thing
                continue
            print ("\t\tCoexist!")  # TODO - save this thing

            #Figure out which rule wins
            #winner, loser = compare_rules(ruleA, ruleB)
            #print ("Rule %s wins")  # TODO - save this thing


def check_rules_coexist(ruleA, ruleB, indexA=0, indexB=0):
    #Figure out the length to be compared
    overlap_length = min(ruleA.size - indexA, ruleB.size - indexB)

    #For each step compared, check the interval:
    for i in range(overlap_length - 1):
        if (ruleA.intervals[indexA + i] and ruleB.intervals[indexB + i] and not
            lists_overlap(ruleA.intervals[indexA + i], ruleB.intervals[indexB + i])):
            return False

    # ...check beat and harmonies: -- harmonies need more looking into
    for i in range(overlap_length):
        if (ruleA.beats[indexA + i] and ruleB.beats[indexB + i] and not
            lists_overlap(ruleA.beats[indexA + i], ruleB.beats[indexB + i])):
            return False
        if (ruleA.harmonic_content[indexA + i] and ruleB.harmonic_content[indexB + i] and not
            lists_overlap(ruleA.harmonic_content[indexA + i], ruleB.harmonic_content[indexB + i])):
            return False

    # ...check extras:
        if ruleA.extras[indexA + i] and ruleB.extras[indexB + i]:
            #for each extra in A...
            for a in ruleA.extras[indexA + i]:
                #If it is mutually exclusive with any in b, return false
                if lists_overlap(extraCheck_dictionary[a], ruleB.extras[indexB + i]):
                    return False

    return True



def lists_overlap(listA, listB):
    '''
    If the lists overlap, returns true; else returns false.
    '''
    print set(listA)
    print set(listB)
    return bool(set(listA) & set(listB))


def compare_rules(ruleA, ruleB):
        #NOTE: right now, gives winner and loser
        #TODO: needs to take into account figure equivalences
        #TODO: assumes rules are same length

        loser = False
        winner = False
        reason = ''
        decision = False

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


# For each possible "extra" that a rule could contain, a list of the other extras that it can't coexist with
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

# For each possible "extra" that a rule could contain, a list of the other extras that it can't coexist with
harmonyCheck_dictionary = {
    'accidental:flat': ['accidental:sharp'],
    'accidental:sharp': ['accidental:flat'],
    'duration:lessThanPreceding': ['duration:twiceAsPreviousTwo'],
    'duration:twiceAsPreviousTwo': ['duration:lessThanPreceding'],
    'scale:on5th': [],
    'duration:two': [],
    'duration:shortAgainstSignature': [],
    'meter:triple': []
    }

#Import all the rulesets in the 'rulesets' directory:
for filename in os.listdir('rulesets'):
    if (filename == 'ruleset_template.py' or
        filename[-3:] != '.py' or filename == '__init__.py'):
        continue
    filename = 'rulesets.' + filename
    module = __import__(filename[:-3], locals(), globals())
