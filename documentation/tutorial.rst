##################
Command-line usage
##################

To apply a set of rules to an unfigured score, do

    ``python figure_extrator ~\path\to\yourscore [-r RULE_SET]``

To visualise a set of rules, do

    ``python rulesViewer -compare [-r RULE_SET]``

To see a print-out of a set of rules, do

    ``python rulesViewer [-r RULE_SET]``

In all use cases, if a special rule set is not indicated the program will default to the full Saint Lambert rule set.


Choosing a set of rules
-----------------------
For both use cases (figure divination and rule set investigation), the rule set flag allows for a specific set or subset of rules to be chosen.

To choose a set of rules, type its name. Currently, the only full rule set include is the Saint Lambert set, named 'SL'.

    ``python figure_extractor \path\to\score -r SL``

To choose several individual rules, list them after the -r flag. If any additional option flags are chosen, make sure -r is the last in the list.

    ``python rulesViewer -r SLRule_03 SLRule_28 SLRule_10a``

To see what rules are available, use

    ``python rulesViewer -list``



Choosing a score
----------------
Input scores can be in any format accepted by music21: musicxml,

Either a filepath or a URL can be given. For example, for example file bwv307.xml in the main figured_bass_extractor directory, use

    ``python figure_extractor bwv307.xml``

To get the same score from a URL, such as from the `Kern Scores library <http://kern.ccarh.org/>`_, use

    ``python figure_extractor 'http://kern.ccarh.org/cgi-bin/ksdata?l=osu/classical/bach/chorale/chorales.all&file=bwv0307.krn&f=kern'``

To get a file a filepath outside of the figured_bass_extractor directory, such as in foo directory on the Desktop, use

    ``python figure_exctractor ~/Desktop/foo/bwv307.xml``



*******************
Working with scores
*******************


**********************
Working with rule sets
**********************
To see details about a rule set:

    python rulesViewer.py [-r [rule] [rule] ...]

For full usage description:

    python rulesViewer.py -h

Example useage:

    python rulesViewer.py
    (All SL rules)

    python rulesViewer.py -size -R SLRule_6 SLRule_8
    (Just the size of SL rules 6 and 8)


***********************************
Creation of new rules and rule sets
***********************************