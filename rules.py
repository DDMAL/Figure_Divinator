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


#Import all the rulesets in the 'rulesets' directory:
for filename in os.listdir('rulesets'):
    if (filename == 'ruleset_template.py' or
        filename[-3:] != '.py' or filename == '__init__.py'):
        continue
    filename = 'rulesets.' + filename
    module = __import__(filename[:-3], locals(), globals())
