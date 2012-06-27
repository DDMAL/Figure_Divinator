# Figured bass extractor rules:
# basic rule class; tests the list of rules
import os


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

        if load:
            self.rulelist = rules

        else:
            for rule in rules:
                #Try adding it from string
                try:
                    new_rule = rule()
                    self.rulelist.append(new_rule)
                except Exception:
                    raise
                    print rule + " doesn't register as a rule..."

    def check_validity(self):
        pass  # TODO: make sure all rules are valid


#Import all the rulesets in the 'rulesets' directory:
packagedRulesets = {}
for filename in os.listdir('rulesets'):
    if (filename == 'ruleset_template.py' or
        filename[-3:] != '.py' or filename == '__init__.py'):
        continue
    filename = 'rulesets.' + filename
    module = __import__(filename[:-3], locals(), globals())
