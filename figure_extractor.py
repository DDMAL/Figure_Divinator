"""Python figured bass extractor using Music21 for score processing
"""

import sys
import os
import argparse
import logging
import copy

from music21 import corpus
from music21 import converter
from music21 import tinyNotation
from music21 import stream

#"rules" contains both the basic rules class and the additional rules sets
import rules

#Set up logging
import logging_setup as Logging
LOG=Logging.getLogger('f_extractor')

class FileNotFoundError(Exception):
    pass

# class InputError(Exception):
#     pass


#When given a score, extract and return the figured bass
def extract(score, ruleset=["SL"]):
    extract = copy.deepcopy(score)
    extract = extract.chordify()

    #TODO -- pull bassline

    #TODO -- pull chords
    #TODO -- run rules

    return extract


def create_comparison(extraction, original=False, solution="x" ):
    
    for n in extraction.flat.notes:
            n.color = "blue"

    #append the original to the extraction?
    if original != False:
        LOG.debug("appending original!")
        for i  in range(0,len(original.parts)):
            extraction.insert(-1, original.parts[i])

    #append the solution to the extraction?
    if solution != "x":
        LOG.debug("appending solution!")
        solution_stream = tinyNotation.TinyNotationStream(solution)
        for n in solution_stream.flat.notes:
            n.color = "red"
        extraction.insert(0, solution_stream)

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
    print output_file_name

    # Open score with Music21
    try:
        score = converter.parse(input_file_name)
    except:
        raise InputError("score is not compatible with Music21 input formats")

    return score,output_file_name


def full_extraction(scorefile, ruleset='dummyrules', teststring = "x", display=True):

    #Read in score
    original_score,output_file_name = open_score_in_music21(scorefile)

    #extract figured bass
    extraction = extract(original_score, ruleset)

    #append original score and/or solution to test file
    if teststring != False:
        create_comparison(extraction, original_score, teststring)

    #save the file
    LOG.debug('\tSaving the file!')
    extraction.write(fmt='musicxml', fp=output_file_name)

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

    full_extraction(scoreFile, ruleSet, testString, viewOutput, True)
    LOG.info("cl done")