==================
Command-line usage
==================

Basic usage
+++++++++++

To apply a set of rules to an unfigured score, do ::

    python figure_extractor ~\PATH\TO\SCORE.XML [-r RULESET]

For additional :mod:`figure_extractor` flag options, see :ref:`detailed-usage` or type ``python figure_extractor -h``.



To visualise a set of rules, do ::

    python rulesViewer -compare [-r RULESET]


or to see a print-out of a set of rules, do ::

    python rulesViewer [-r RULESET]

For additional :mod:`rulesViewer` flag options, see :ref:`detailed-viewer` or type ``python rulesViewer -h``..



In all use cases, if a special rule set ``[-r RULESET]`` is not indicated the program will default to the full Saint Lambert rule set.

.. _rules:

Choosing a set of rules
-----------------------
For both use cases (figure divination and rule set investigation), the flag
``[-r RULE_SET]`` allows for a specific set name or subset of rules to be
chosen.

To choose a named set of rules, type that name. Currently, the only full rule set include is the Saint Lambert set, named 'SL'. ::

    python figure_extractor \path\to\score -r SL

To choose several individual rules, list them after the -r flag. If any additional option flags are chosen, make sure -r is the last in the list. ::

    python rulesViewer -r SLRule_03 SLRule_28 SLRule_10a

To see what rules are available, use ::

    python rulesViewer -list

.. _score:

Choosing a score
----------------
Input scores can be in `any format accepted by music21 <http://mit.edu/music21/doc/html/overviewFormats.html>`_: MusicXML, Humdrum, ABC, Musedata, and MIDI, although only .xml has been extensively tested.

Either a filepath or a URL can be given. For example, to use example file ``bwv307.xml`` in the main Figure_Divinator directory, use ::

    python figure_extractor bwv307.xml

To use ``foo.xml`` from the desktop, use ::

    python figure_extractor ~/Desktop/foo.xml

To get the same score from a URL, such as from the `Kern Scores library <http://kern.ccarh.org/>`_, use ::

    python figure_extractor 'http://kern.ccarh.org/cgi-bin/ksdata?l=osu/classical/bach/chorale/chorales.all&file=bwv0307.krn&f=kern'

To get a file a filepath outside of the Figure_Divinator directory, such as in foo directory on the Desktop, use ::

    python figure_exctractor ~/Desktop/foo/bwv307.xml


.. _detailed-usage:

Figure divination options
+++++++++++++++++++++++++
The full set of options for divining/applying figures to an unfigured score is as follows::

    python figure_extractor.py [-o] [-s] [-c] [-p] [-b backward] [-r RULESET] input_file


There are several additional flag options:

    -o                      Prevents score, visualisation output from displaying.

    -s                      Does not save output score and visualisation.

    -c                      Shows all figures in output score, even musically redundant ones (e.g. '3,5').

    -p                      Attempts to remove passing tones from bassline by using built-in :mod:`music21` analysis modules.

    -b backward             If two rules overlap, default preference is given to the one that starts first ('forward'). This flag changes the default preference to the rule with the later ending note past the overlap.

    -r [RULESET]              See :ref:`rules`.



.. _detailed-viewer:

Rule set visualisation options
++++++++++++++++++++++++++++++
TODO - HHHHHHHH

