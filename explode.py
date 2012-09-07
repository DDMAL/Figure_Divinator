# Copyright (C) 2012 by Hannah Robertson
"""
Basic script showing how to realize score from Figure Divinator output.

More info on the :class:`music21.figuredBass` can be found at
http://mit.edu/music21/doc/html/moduleFiguredBassExamples.html.

To run from command line, do ``python explode.py [PATH/TO/SCORE]``.
If no score is given, defaults to ``bwv307.xml``.

"""

import sys
import figure_extractor


def divine_and_realize(url='bwv'):
    if url == 'bwv':
        this_file = 'bwv307.xml'
    else:
        this_file = url

    #Get the extraction
    print 'Getting divination:'
    score = figure_extractor.full_extraction(this_file,
                                            display=True, logging=False)

    #Make a music21.figuredBass object from the divination output
    score.makeFiguredBassObject()

    #Show figured bass line
    print 'Displaying bass line'
    score.fb.generateBassLine().show()

    #Make the realizations with the default rule set
    print 'Creating realizations'
    bassline = score.fb.realize()
    print '-->There are %s possible solutions using default rule set' % \
            str(bassline.getNumSolutions())

    #Show one of these realizations
    print 'Showing a random realization'
    bassline.generateRandomRealization().show()


# Run from command line
if __name__ == '__main__':
    if len(sys.argv) > 1:
        divine_and_realize(sys.argv[1])
    else:
        divine_and_realize()
