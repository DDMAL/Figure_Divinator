####################
Notes for developers
####################

FigDiv was developed in Python 2.7.1 on OS X 10.7.4 (Lion), using music21
version 1.0.0.

Building documentation
======================
Documentation is created with `Sphinx <http://sphinx.pocoo.org/>`_.
To install Sphinx, in Terminal run ::

    easy_install sphinx

To rebuild documentation, from the FigDiv program directory type ::

    make <target>

where <target> is the type of documentation desired: html, latex, latexpdf,
or text. (For a full list of documentation types, type make help from the
FigDiv directory.)

Output will be saved to FigDiv/documentation/_build/<target>. Rebuilt html documentation should be uploaded to the project documentation page, Documentation_Website_Location (TODO).

Note:
    * All class and method documentation is built automatically from docstrings, once the class is listed in FigDiv/documentation/moduleRules.rst or FigDiv/documentation/moduleRulesets.rst. Any new files must be listed there in order to be included in the documentation.

    * All non-auto-generated pages are saved as `.rst files <http://matplotlib.sourceforge.net/sampledoc/cheatsheet.html>`_ and saved in FigDiv/documentation. Any new .rst files must be added to the documentation index (FigDiv/index.rst).


Testing
=======
Testing is done with
`nosetests <http://nose.readthedocs.org/en/latest/usage.html>`_.
To install, use ::

    easy_install nose

To run tests, from the main FigDiv program directory type ::

    nosetests

or, to see which tests were run, ::

    nosetests -v


Note that nosetests will run any file that contains 'test' or 'Test'
within the figdiv directory. To specify only a certain test, use::

    nosetests only_test_this_test.py

or to change the directory tested from, use ::

    nosetests -w /path/to/tests


Additional notes
================
* All testing has been done on .xml files. All files accepted by music21 should work, but it is possible that there are unexpected incompatibilities (imprecise midi recordings, for example, might be difficult for extracting the bass line). It might be worth testing these file types explicitly or making it clear that users should be wary.

Task list
===================
Documentation
-------------
* Write tutorial for building new rule sets
* Write tutorial for investigating rule sets
* Write tutorial for figuring a score

--> http://ivory.idyll.org/articles/nose-intro.html
--> http://nose.readthedocs.org/en/latest/writing_tests.html
--> http://docs.python.org/dev/library/unittest.html#unittest.TestCase

Code
----
* Complete rule-related functions needed for SL rule set

* Modules:

    * Remove passing tones from bass lines

    * Build in rule-trumping (no more 'chosen at random')

    * Make sure rules.compare_rules isn't bogus

    * Several TO-DO functions; search modules

* Testing:

    * Functions that compare rules

    * Test rule set for self-sufficiency

Hank
----
* rules.extraCheck_dictionary

