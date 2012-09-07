#script!

#Get figures from score


import sys
import figure_extractor


def divine_and_realize(url='bwv'):
    if url == 'bwv':
        this_file = 'bwv307.xml'
    else:
        this_file = url

    #Get the extraction
    print 'making extraction'
    score = figure_extractor.full_extraction(this_file, display=True)
    score.makeFiguredBassObject()

    #create realization
    print 'showing bassline'
    score.fb.generateBassLine().show()

    print 'making realization with default rule set'
    bassline = score.fb.realize()


    print 'there are %s possible solutions using default rule set' % str(bassline.getNumSolutions())
    print 'showing a random realization'
    bassline.generateRandomRealization().show()
























# Run from command line
if __name__ == '__main__':
    if len(sys.argv) > 1:
        Hh_test(sys.argv[1])
    else:
        divine_and_realize()
