===========================================================================
Figure Divinator: Rule-based generation of figured bass from musical scores
===========================================================================

Figure Divinator is a tool for automated, rule-based divination of figured bass from unfigured musical scores. It can be used both for performance and study; musicians can use it to avoid the tedius task of figuring un-figured scores, and musicologists can use it to study the interaction and application of rules used to do the figuring.

Figure Divinator was created as part of the `Centre de Recherche sur l'Interprétation au Clavecin (CRIC) <http://cric.music.mcgill.ca/>`_, which is associated with McGill's `Schulich School of Music <http://www.mcgill.ca/music/>`_. CRIC is funded in part by the `Social Sciences and Humanities Research Council of Canada (SSHRC) <http://www.sshrc-crsh.gc.ca/Default.aspx>`_.


Installation and basic usage
----------------------------

After installing `Music21 <http://mit.edu/music21/doc/html/install.html#install>`_ and `MATPLOTLIB <http://matplotlib.sourceforge.net/>`_, download the `Figure Divinator source code <https://github.com/DDMAL/figured-bass-extractor>`_.

From the Figure_Divinator folder, to apply a set of rules to an unfigured
score, do ::

    python figure_extrator ~\path\to\yourscore [-flags]

To visualise a set of rules, do ::

    python rulesViewer -compare [-flags]

To see a print-out of a set of rules, do ::

    python rulesViewer [-flags]

In all use cases, if a special rule set is not indicated the program will default to the full Saint Lambert rule set. To choose a special subset of rules or use other ``[-flags]`` options, see :doc:`documentation/tutorial`.

Tutorials
---------

.. toctree::
   :maxdepth: 2

   documentation/tutorial
   documentation/tutorialRulesets
   documentation/examples

Included Rule Sets:

.. toctree::
   :maxdepth: 2

   documentation/moduleRulesets

Developers
----------

.. toctree::
   :maxdepth: 2

   Development notes <documentation/developers>
   documentation/moduleRules


Indices and Search
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

