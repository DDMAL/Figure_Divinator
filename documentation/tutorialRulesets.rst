**********************
Creating new rule sets
**********************

Set-up
------
A template for creating new rule sets can be found at ``figured_bass_extractor\rulesets\ruleset_template.py``.

In order to be automatically imported into the Figure Divination program, the rule set must be named using the convention 'ruleset_[yourRulesetName].py'.


Rule Naming
-----------
Rules should follow the naming convention [yourRulesetNamePrefix]_[rule_number], where single digit numbers start with 0:

    myruleset_01

    myruleset_02

    ...

    myruleset_10

    etc.

Rules can be further split into abc or 123:

    myruleset_01a

    myruleset_01b1

    myruleset_01b2


Creating individual rules
-------------------------


Testing rule set
----------------
See :mod:`test_rulesSL.py` for an example script created for the Saint Lambert rule set. It should be easy to modify the script work with any other score, by merely altering the block of variables commented in the script.

Each test .xml file should be named after the single rule it tests; if a single rule has multiple test files, append _repetition to the rule name. For example, test files for rule myruleset_01a should be named myruleset_01a_1.xml and myruleset_01a_2.xml, or a single test file for rule myruleset_11 should be named myruleset_11.xml.