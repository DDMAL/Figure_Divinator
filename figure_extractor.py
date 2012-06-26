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
from music21 import note
from music21.figuredBass import realizer

from rule_crawler import *
from rule_plotter import *

#Set up logging
import logging_setup as Logging
LOG = Logging.getLogger('f_extractor')


class FileNotFoundError(Exception):
    pass


class InputError(Exception):
    pass


class ExtractionWork(object):
    """A class that holds both the original score and newly extracted portion"""
    def __init__(self, score_file_input, *args, **kwargs):
        #Possible kwargs: ruleset, solution, type_of_bass,

        #Input score details
        self.score_input = score_file_input
        self.input_filename = ''
        self.original_score = stream.Score()
        self.title = ''
        self.composer = ''

        #Input options
        self.ruleset = kwargs.get('ruleset', ['SL'])
        self.solution = kwargs.get('solution', False)
        self.bass_options = kwargs.get('type_of_bass', 'all')
        self.display_option = kwargs.get('display', True)

        #Output
        self.output_filename = ''
        self._fb_figureString = []
        self.fb = realizer.FiguredBassLine()
        self.output_score = stream.Score()
        self.output_fb_score = stream.Score()
        self.possible_rules = []
        self.chosen_rules = []

        #Inner workings
        self._bassline = stream.Stream()
        self._chordscore = stream.Score()
        self._allrules = []

        #Load the file, get the original bassline!
        self._load_score_from_file()      # ...TODO-Hh{future:accept straight score?}
        self.extract_bassline_from_score()

    def _load_score_from_file(self):
        """Reads score into music21, harvests metadata"""
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

        (input_base, ext_sep, input_ext) = self.score_input.rpartition(os.extsep)

        self.input_filename = input_base + ext_sep + input_ext
        self.output_filename = (input_base + '_figured_bass' + ext_rule +
                            ext_sep + input_ext)

        # Open score with Music21
        try:
            self.original_score = converter.parse(self.input_filename)
        except:  # TODO - figure out type of exception
            raise InputError('Score is not compatible with Music21 input formats')

        # Collect metadata
        try:
            self.title = self.original_score.metadata.title
        except:  # TODO - figure out type of exception
            self.title = str(score_input)

        try:
            self.composer = self.original_score.metadata.composer
        except:  # TODO - figure out type of exception
            self.composer = ' - '

        #Chordify
        self._chordscore = self.original_score.chordify()

    def extract_bassline_from_score(self):
        """Extract the full bassline from the score"""  # TODO-Hh{f:additional methods?}

        try:
            self._bassline = copy.deepcopy(self.original_score['bass'])
            LOG.debug('Bassline is pre-labeled bass line')

        except:  # TODO - figure out type of exception
            try:
                #Get all of lowest staff
                i = len(self.original_score.getElementsByClass(stream.Part)) - 1
                self._bassline = copy.deepcopy(self.original_score.getElementsByClass(stream.Part)[i])
                LOG.debug('Bassline is lowest part')
            except:  # TODO - figure out type of exception
                raise InputError('Cannot extract bass line from score')

    def process_bassline(self):
        #Post-processing:
        #TODO - keep all notes? eliminate passing tones?
        #TODO - check to make sure aren't multiple bass notes/voicing
        pass

    def extract(self):
        """When given a score, this method extracts and returns the figured bass"""
        #Process the bassline?
        self.process_bassline()

        #Set up the figure strings:
        basslength = len(self._bassline.flat.getElementsByClass(note.Note))
        self._fb_figureString = ['n' for x in range(basslength)]

        #Run through rules
        ruler = rule_crawler(self)
        ruler.full_check_rules()
        ruler.full_apply_rules()

        #Plot the results
        makePlot(self)

        #Add figures into score:
        for i in range(basslength):
            n = self._bassline.flat.getElementsByClass(note.Note)[i]
            f = self._fb_figureString[i]
            try:
                self.fb.addElement(n, f)
            except KeyError as e:
                print e

        self.fb = realizer.figuredBassFromStream(self._bassline)
        return object

    def _setup_output(self):  # TODO-Hh{non-critical: metadata fail!}
        """Attempts to add metadata to new score. Doesn't work."""
        #Create output metadata
        my_metadata = metadata.Metadata()
        my_metadata.title = 'Figured bass reduction of \n' + str(self.title)
        my_metadata.composer = str(self.composer) + '\nFigure extraction: Auto'

        #Add metadata to output score
        self.output_score.metadata = my_metadata
        self.output_fb_score.metadata = my_metadata

    def append_to_extraction(self):

        #append the original to the extraction?
        LOG.debug('appending original!')
        for partline in (self.original_score.getElementsByClass(stream.Part)):
            self.output_score.insert(partline)

        for n in self.output_score.flat:
            n.color = 'blue'

        #append the solution to the extraction?
        if self.solution != False and self.solution != 'x':
            LOG.debug('appending solution!')
            #Insert the solution below the reduction
            solutionline = stream.Part()
            solutionline.append(tinyNotation.TinyNotationStream(self.solution))
            for n in solutionline.flat:
                n.color = 'red'
            self.output_score.insert(solutionline)

    def create_output(self):
        #Set up output
        self._setup_output()

        #Showing solution and/or original with old?
        #append original score and/or solution to test file
        self.append_to_extraction()

        #Make score from bassline
        self.output_score.insert(0, self.fb.generateBassLine())
        self.output_fb_score.insert(0, self.fb.generateBassLine())
        #self.output_score.show()

        #save the file
        LOG.debug('\tSaving the file!')
        self.output_score.write(fmt='musicxml', fp=str(self.output_filename))

        #display the new file?
        if self.display_option == True:
            try:
                new_score = converter.parse(self.output_filename)
                #new_score.show()
                self.output_score.show()
                LOG.info('Displaying output if xml viewer has been installed.')
            except:  # TODO - figure out type of exception
                LOG.info('Unable to show .xml output through MusicXML,')
                LOG.info('try opening the file directly.')
        else:
            LOG.info('Not displaying file.')
        #TODO - selfcomparison = score


def full_extraction(scorefile, *args, **kwargs):
#optional kwargs: ruleset, teststring, display

    #Get, load score
    my_work = ExtractionWork(scorefile, *args, **kwargs)

    #Prepare output
    my_work._setup_output()

    #make extract
    my_work.extract()

    #do output
    my_work.create_output()

    #done!
    LOG.info('Done with full extraction.')

    return my_work


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
