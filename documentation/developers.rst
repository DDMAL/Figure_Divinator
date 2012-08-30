####################
Notes for developers
####################

Building documentation
----------------------
Documentation has been created with Sphinx. To install, use TODO

To rebuild documentation, from the FigDiv program directory, type

make <type>

where <type> is the type of documentation: html, TODO.

Once the html has been rebuilt, it will be found in the FigDiv/documentation/_build/<html/doctrees/etc> folder, and can be uploaded  to Documentation_Website_Location (TODO).

Note:
-- All doc-string documentation for classes is built automatically, assuming the class is listed in FigDiv/documentation/moduleRules.rst or FigDiv/documentation/moduleRulesets.rst. Any new files will need to be listed in one of these files in order to be included in the documentation.

-- All non-auto-generated documentation is written as .rst files and stored in FigDiv/documentation. In order to include any new .rst files in the documentation, be sure to add its file name to FigDiv/index.rst.


Running unit tests
------------------
Testing is done with nosetests. To install, use easy_install nose. Documentation is found here: http://nose.readthedocs.org/en/latest/usage.html.

To run tests, while in the main FigDiv program directory, type

nosetests

or

nosetests -v to see which tests were run.


Note that nosetests will run any file that contains 'test' or 'Test' within the figdiv directory. To specify only a certain test, use

nosetests only_test_this_test.py

or to change the directory tested from, use

nosetests -w /path/to/tests


