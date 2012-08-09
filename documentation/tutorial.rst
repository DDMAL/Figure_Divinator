#########
Tutorials
#########

To apply a set of rules to a score, do

python figure_extrator yourscore.xml [-r RULESET]

To visualise a set of rules, do

python rulesViewer -compare [-r RULESET]




Choosing a set of rules
-----------------------


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