"""Python figured bass extractor using Music21 for score processing
"""

import sys
import os
import argparse
import logging
import copy

from music21 import converter
from music21 import corpus
from music21 import metadata
from music21 import stream
from music21 import tinyNotation

#"rules" contains both the basic rules class and the additional rules sets
import rules

#Set up logging
import logging_setup as Logging
LOG=Logging.getLogger('f_extractor')

class FileNotFoundError(Exception):
    pass

class InputError(Exception):
    pass


#When given a score, extract and return the figured bass
def extract(original_score, extraction_score, ruleset=["SL"]):

    extract = copy.deepcopy(original_score)

    #Get the bassline from the original
    bassline = get_bassline(original_score)

    #Process the bassline
    proc_bassline(bassline)

    for n in bassline.flat:
        n.color = "red"

    #Get the chords from the original
    chords = original_score.chordify()
    for c in chords.flat.getElementsByClass('Chord'):
        c.closedPosition(forceOctave=4, inPlace=True)
        c.removeRedundantPitches(inPlace=True)
        c.annotateIntervals()
        c.color = "yellow"

    #TODO -- run rules

    #Put bassline in extraction score
    extraction_score.insert(0,bassline)

    return extraction_score


def get_bassline(score, proc_type="all"):
    
    try:
        return copy.deepcopy(score['bass'])
        LOG.debug("Bassline is pre-labeled bass line")

    except:
        try:
            #Get all of lowest staff
            bassnum = len(score.getElementsByClass(stream.Part)) - 1
            return copy.deepcopy(score.getElementsByClass(stream.Part)[ bassnum ])
            LOG.debug("Bassline is lowest part")
        except:
            raise InputError("cannot extract bass line from score")


def proc_bassline(line, proc_type="all"):
    #Post-processing:
    #TODO - keep all notes?
    #TODO - check to make sure aren't multiple bass notes
    pass


def create_comparison(extraction, original=False, solution="x" ):
    
    for n in extraction.flat.notes:
            n.color = "blue"

    #append the original to the extraction?
    if original != False:
        LOG.debug("appending original!")
        for partline in original.getElementsByClass(stream.Part):
            extraction.insert(-1,partline)

    #append the solution to the extraction?
    if solution != "x":
        LOG.debug("appending solution!")
        #Insert the solution below the reduction
        solutionline = tinyNotation.TinyNotationStream(solution) #'E2_#6 F2_6')
        for n in solutionline.flat:
            n.color="red"
        extraction.insert(0,solutionline)

    return extraction


def open_score_in_music21(scoreFile, ruleset=[""]):
    #...TODO -- accept straight score?

    #set output file additional suffix
    if ruleset[0] == "SL":
        ext_rule = "_SL"
    elif ruleset[0] == "dummyrules":
        ext_rule = "_dummy"
    else:
        ext_rule = "_unique"

    #read in score file 
    if not os.path.isfile(scoreFile):
        raise FileNotFoundError(scoreFile)

    (input_base,ext_sep,input_ext) = scoreFile.rpartition(os.extsep)

    input_file_name = input_base + ext_sep + input_ext
    output_file_name = (input_base + "_figured_bass" + ext_rule +
                        ext_sep + input_ext)

    # Open score with Music21
    try:
        score = converter.parse(input_file_name)
    except:
        raise InputError("score is not compatible with Music21 input formats")

    return score,output_file_name


def full_extraction(scorefile, ruleset='dummyrules', teststring = "x", display=True):

    #Read in score
    original_score,output_file_name = open_score_in_music21(scorefile, ruleset)

    #Create new score to hold extraction
    reduction = stream.Score()

    #Add metadata
    oldtitle = ""
    oldcomposer = ""

    try:
        oldtitle = score.metadata.title
    except:
        oldtitle = str(scorefile)

    try:
        oldcomposer= score.metadata.composer
    except:
        pass

    reduction.insert(metadata.Metadata())
    reduction.metadata.title = 'Figured bass reduction of \n' + oldtitle
    reduction.metadata.composer = oldcomposer + '\nFigure extraction: Auto'

    #extract figured bass
    reduction = extract(original_score, reduction, ruleset)

    #append original score and/or solution to test file
    if teststring != False:
        create_comparison(reduction, original_score, teststring)

    #save the file
    LOG.debug('\tSaving the file!')
    reduction.write(fmt='musicxml', fp=output_file_name)

    #display the new file?
    if teststring != False or display == True:
        try:
            new_score = converter.parse(output_file_name)
            new_score.show()
            LOG.info("Displaying output if xml viewer has been installed.")
        except:
            LOG.info("Unable to show .xml output through MusicXML,")
            LOG.info("try opening the file directly.")

    #done!
    LOG.info('Done with full extraction.')


# Run from command line
if __name__ == "__main__":
    LOG.info("cl start")

    #Get, parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('-o', action='store_true',
                    dest='viewOutput', default=False,
                    help='View output in MusicXML interface?')
    parser.add_argument('-t', nargs='?', const='x', default=False, dest='test_string')
    parser.add_argument('-r', nargs='*', dest='rules_type', default=['dummyrules'], help='Set of rules to apply')

    LOG.debug("Arguments: %s\n", parser.parse_args())

    #Set flags
    args = parser.parse_args()
    scoreFile = args.input_file
    ruleSet = args.rules_type
    testString = args.test_string
    viewOutput = args.viewOutput

    full_extraction(scoreFile, ruleSet, testString, True)
    LOG.info("cl done")