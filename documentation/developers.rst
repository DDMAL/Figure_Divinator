####################
Notes for developers
####################

Figure Divinator was developed in Python 2.7.1 on OS X 10.7.4 (Lion), using
music21 version 1.0.0.

Building documentation
======================
Documentation is created with `Sphinx <http://sphinx.pocoo.org/>`_.
To install Sphinx, in Terminal run ::

    easy_install sphinx

To rebuild documentation, from the Figure Divinator program directory type ::

    make <target>

where <target> is the type of documentation desired: html, latex, latexpdf,
or text. (For a full list of documentation types, type make help from the
Figure Divinator directory.)

Output will be saved to Figure_Divinator/documentation/_build/<target>. Rebuilt html documentation should be uploaded to the project documentation page, cric.music.mcgill.ca/docs/ (contact Andrew or other DDMAL member to get access).

Note:
    * All class and method documentation is built automatically from docstrings, once the class is listed in Figure_Divinator/documentation/moduleRules.rst or Figure_Divinator/documentation/moduleRulesets.rst. Any new files must be listed there in order to be included in the documentation.

    * All non-auto-generated pages are saved as `.rst files <http://matplotlib.sourceforge.net/sampledoc/cheatsheet.html>`_ and saved in Figure_Divinator/documentation. Any new .rst files must be added to the documentation index (Figure_Divinator/index.rst).


Testing
=======
Testing is done with
`nosetests <http://nose.readthedocs.org/en/latest/usage.html>`_.
To install, use ::

    easy_install nose

To run tests, from the main Figure_Divinator program directory type ::

    nosetests

or, to see which tests were run, ::

    nosetests -v


Note that nosetests will run any file that contains 'test' or 'Test'
within the Figure_Divinator directory. To specify only a certain test, use::

    nosetests only_test_this_test.py

or to change the directory tested from, use ::

    nosetests -w /path/to/tests


Additional notes
================
* All testing has been done on .xml files. All files accepted by music21 should work, but it is possible that there are unexpected incompatibilities (imprecise midi recordings, for example, might be difficult for extracting the bass line). It might be worth testing these file types explicitly or making it clear that users should be wary.

Task list
===================

H's remaining hours:
--------------------
* Discuss priorities with Hank.

* Bullets with (H) after them!


Documentation
-------------
* Write tutorial for building new rule sets (H-1)
* Write tutorial for investigating rule sets (H-1)
* Write tutorial for figuring a score (H-1)


Code
----
* Complete rule-related functions needed for SL rule set (H-2)

* Modules:

    * Remove passing tones from bass lines

    * Build in rule-trumping (no more 'chosen at random')

    * Make sure rules.compare_rules isn't bogus

    * Several TO-DO functions; search modules

    * Make sure co-app

* Testing:

    * Functions that compare rules

    * Test rule set for self-sufficiency

    * Make sure coexisting rules don't accidentally cancel one another out. (Possibly re-write rule application so that preferencing happens BEFORE selection....)

* Nit-picky:

    * There doesn't seem to be a "dash" option in music21. Currently, the hacked solution in our figured-bass-extractor is to use a quadruple flat instead (notation.Notation('----')), as a quadruple flat is acceptable to the figured bass class whereas 'dash' or 'NA' or any other non-number, non-modifier string is not. Once '-' is added to possible figures, add a clean-up option that determines which figures could be dashes and simplifies them down before output. [This is probably the best plan of action.]


* Wish list (non-critical but nice):

    * When displaying a solution string, currently only music21.tinyNote.Notation type is accepted; make it possible to input a score, maybe.

    * Allow pre-existing figures to be utilized (for full figuring of partially-figured scores).

Hank
----
* Look through rules.extraCheck_dictionary

* Provide test score (.xml) with figured solution

