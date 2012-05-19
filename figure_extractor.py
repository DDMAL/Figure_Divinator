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


class ExtractionWork(object):
    """A class that holds both the original score and newly extracted portion"""
    def __init__(self, score_file_input, **kwargs):
        self.score_input = score_file_input
        self.ruleset = kwargs.get('ruleset','SL')
        self.input_filename = ''
        self.output_filename = ''
        self.original_score = ''
        self.solution = kwargs.get('solution',False)
        self.extracted_bassline
        self.extracted_fbassline
        
        _load_score_from_file()        #...TODO -- accept straight score?


    def _load_score_from_file(self):
        #set output file additional suffix
        ext_rule = ''
        if self.ruleset[0] == 'SL':
            ext_rule = '_SL'
        elif self.ruleset[0] == 'dummyrules':
            ext_rule = '_dummy'
        else:
            ext_rule = '_unique'

        #read in score file 
        if not os.path.isfile(self.score_input):
            raise FileNotFoundError(self.score_input)

        (input_base,ext_sep,input_ext) = self.score_input.rpartition(os.extsep)

        self.input_filename = input_base + ext_sep + input_ext
        self.output_filename = (input_base + '_figured_bass' + ext_rule +
                            ext_sep + input_ext)

        # Open score with Music21
        try:
            self.original_score = converter.parse(self.input_filename)
        except:
            raise InputError('Score is not compatible with Music21 input formats')


    def extract_bassline_from_score(self):
        """Extract the full bassline from the score"""
        try:
            self.extracted_bassline = copy.deepcopy(self.original_score['bass'])
            LOG.debug('Bassline is pre-labeled bass line')

        except:
            try:
                #Get all of lowest staff
                bassnum = len(self.original_score.getElementsByClass(stream.Part)) - 1
                self.extracted_bassline = copy.deepcopy(self.original_score.getElementsByClass(stream.Part)[ bassnum ])
                LOG.debug('Bassline is lowest part')
            except:
                raise InputError('Cannot extract bass line from score')


    def process_bassline(self, process_type = 'all'):
        #Post-processing:
        #TODO - keep all notes? eliminate passing tones?
        #TODO - check to make sure aren't multiple bass notes/voicing
        pass

    def extract(self):
        """When given a score, this method extracts and returns the figured bass"""
        #(original_score, extraction_score, ruleset=["SL"]):

        extract = copy.deepcopy(self.original_score)

        #Get the bassline from the original
        bassline = extract_bassline_from_score(self.original_score) #TODO - get_bassline method???

        #Process the bassline
        proc_bassline(bassline) #TODO - get_bassline method???

        for n in bassline.flat:
            n.color = 'red'

        #Get the chords from the original
        chords = self.original_score.chordify()
        for c in chords.flat.getElementsByClass('Chord'):
            c.closedPosition(forceOctave=4, inPlace=True)
            c.removeRedundantPitches(inPlace=True)
            c.annotateIntervals()
            c.color = 'yellow'

        #TODO -- run rules

        #Put bassline in extraction score
        extraction_score.insert(0,bassline)

        self.extracted_fbassline = extraction_score #TODO: MAKE fb not score


    def create_extract_comparison(self): #TODO
        #extraction, original=False, solution='x' ):
        
        for n in extraction.flat.notes:
                n.color = 'blue'

        #append the original to the extraction?
        if original != False:
            LOG.debug('appending original!')
            for partline in original.getElementsByClass(stream.Part):
                extraction.insert(-1,partline)

        #append the solution to the extraction?
        if solution != 'x':
            LOG.debug('appending solution!')
            #Insert the solution below the reduction
            solutionline = tinyNotation.TinyNotationStream(solution) #'E2_#6 F2_6')
            for n in solutionline.flat:
                n.color='red'
            extraction.insert(0,solutionline)

        #TODO - selfcomparison = score



def full_extraction(scorefile, **kwargs):
#optional kwargs: ruleset, teststring, display

    teststring = kwargs.get('teststring','x')
    teststring = kwargs.get('display',True)

    #Get, load score
    my_score = ExtractionWork(scorefile, kwargs)

    #Create new score to hold extraction #TODO wrong???
    reduction = stream.Score()

    #Add metadata
    oldtitle = ''
    oldcomposer = ''

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
    reduction = my_score.extract() #original_score, reduction, ruleset)

    #append original score and/or solution to test file #TODO<--
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
            LOG.info('Displaying output if xml viewer has been installed.')
        except:
            LOG.info('Unable to show .xml output through MusicXML,')
            LOG.info('try opening the file directly.')

    #done!
    LOG.info('Done with full extraction.')


# Run from command line
if __name__ == '__main__':
    LOG.info('cl start')

    #Get, parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('-o', action='store_true',
                    dest='viewOutput', default=False,
                    help='View output in MusicXML interface?')
    parser.add_argument('-t', nargs='?', const='x', default=False, dest='test_string')
    parser.add_argument('-r', nargs='*', dest='rules_type', default=['dummyrules'], help='Set of rules to apply')

    LOG.debug('Arguments: %s\n', parser.parse_args())

    #Set flags
    args = parser.parse_args()
    scoreFile = args.input_file
    ruleSet = args.rules_type
    testString = args.test_string
    viewOutput = args.viewOutput

    full_extraction(scoreFile, ruleSet, testString, True)
    LOG.info('cl done')