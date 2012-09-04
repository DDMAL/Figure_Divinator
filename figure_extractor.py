# Copyright (C) 2012 by Hannah Robertson
"""
Sets up and runs score processing for figure divination.

When run from command line, does :func:`full_extraction`. For command line
option flags, in terminal run ``python figure_extractor.py -h``.

"""

import os
import argparse
import copy
import music21 as m21

import rules
import rule_crawler
import rule_plotter

#Set up logging
import logging_setup as Logging
LOG = Logging.getLogger('f_extractor')


class FileNotFoundError(Exception):
    pass


class InputError(Exception):
    pass


class ExtractionWork(object):
    """
    Holds the original score and manages the intermediate extraction steps.

    **Args**
        **score_file_input**: Local path or URL to input file.
        File can be of any type supported by :mod:`music21`: musicXML,
        Humdrum (kern), ABC, Musedata, and MIDI
        (`full list of music21's accepted file types
        <http://mit.edu/music21/doc/html/overviewFormats.html>`_).

    **kwargs**
        **ruleset**: (Optional) The name of a rule set or list of rules to be
        applied to score. Can be given as either a rule set id string,
        e.g. 'SL', or an array of rule names, e.g.
        ``['SLRule_03', 'SLRule_08a']``, as in :func:`rules.get_ruleset`.
        Default is the full Saint Lambert rule set.

        **display**: (Optional) Boolean. If true, displays score and
        graphical visualisation of output. Default False.

        **save**: (Optional) Boolean. If true, saves the output score as an .xml
        file. Default True.

        **remove_passing**: (Optional) Boolean. If true, removes passing tones
        from bassline using :mod:`music21` analysis methods. Default False.

        **rule_direction**: (Optional) Direction rules are applied to score,
        either 'forward' (starting at the beginning and working towards the end)
        or 'backward' (starting on the last note and working towards the first).
        Default 'forward'.

        **clean**: (Optional) Boolean. If true, makes output score visually
        cleaner by hiding implied figures such as '3,5'. Default True.

        **solution**: (Optional) A `music21.tinyNotation
        <http://mit.edu/music21/doc/html/moduleTinyNotation.html>`_ string. If
        present, solution will be appended to final output score for easy
        comparison between given solution and figure divination output. Default
        False.

        **make_fb_object**: (Optional) Boolean. In future, useful for piping
        output from this figure divination module to a module for figure
        realization. Default False.

    """

    def __init__(self, score_file_input, **kwargs):
        #Input score details
        self.score_input = score_file_input
        self.input_filename = ''
        self.original_score = m21.stream.Score()
        self.title = ''
        self.composer = ''

        #Input options
        self.ruleset = kwargs.get('ruleset', ['SL'])
        self.solution = kwargs.get('solution', False)
        self.display_option = kwargs.get('display', False)
        self.save_option = kwargs.get('save', True)
        self.create_fb_object = kwargs.get('make_fb_object', False)
        self.clean_option = kwargs.get('clean', True)
        self.remove_passing_option = kwargs.get('remove_passing', False)
        self.rule_application_direction = kwargs.get('rule_direction', 'forward')

        if self.rule_application_direction != 'backward':
            self.rule_application_direction = 'forward'

        #Output
        self.output_filename = '' ##TODO - make user option
        self._fb_figureString = []
        self.fb = False
        self.output_score = m21.stream.Score()
        self.output_fb_score = m21.stream.Score()
        self.possible_rules = []
        self.chosen_rules = []

        #Inner workings
        self._bassline = m21.stream.Stream()
        self._chordscore = m21.stream.Score()
        self._allrules = []

        #Load the file, get the original bassline!
        self._load_score_from_file()
        self.extract_bassline_from_score()

        #Load the rule set
        self.ruleset = rules.get_ruleset(self.ruleset)
        self._allrules = self.ruleset.rulelist

    def _load_score_from_file(self):
        """Reads score into music21, harvests metadata."""
        #set output file additional suffix
        ext_rule = ''
        if self.ruleset[0] == 'SL':
            ext_rule = '_SL'
        elif self.ruleset[0] == 'dummyrules':
            ext_rule = '_dummy'
        else:
            ext_rule = '_unique'

        #read in score file
        # if not os.path.isfile(self.score_input):
        #     raise FileNotFoundError(self.score_input)

        (base, filename) = os.path.split(self.score_input)
        if len(base) > 0:
            base = base + '/'
        (input_base, ext_sep, input_ext) = filename.rpartition(os.extsep)

        self.input_filename = base + input_base + ext_sep + input_ext
        self.output_filename = ('results/' + input_base + '_figured_bass' + ext_rule)

        # Open score with Music21
        try:
            self.original_score = m21.converter.parse(self.input_filename)
        except:  # TODO - figure out type of exception
            raise InputError('Score is not compatible with Music21 input formats')

        # Collect metadata
        try:
            self.title = self.original_score.metadata.title
        except:  # TODO - figure out type of exception
            self.title = str(self.score_input)

        try:
            self.composer = self.original_score.metadata.composer
        except:  # TODO - figure out type of exception
            self.composer = ' - '

        #Chordify
        self._chordscore = self.original_score.chordify()

    def extract_bassline_from_score(self):
        """
        Extracts bassline from ``self.original_score``, saves to ``self._bassline``.

        The bassline is simply the part in the original_score labeled 'bass',
        if present, or the bottom-most part in the score if none is specifically
        labeled.

        TO-DO in :func:`_clean_bassline_single_voice`: If the part is polyphonic,
        only returns the lowest notes.

        """
        try:
            self._bassline = copy.deepcopy(self.original_score['bass'])
            LOG.debug('Bassline is pre-labeled bass line')

        except:  # TODO - figure out type of exception
            try:
                #Get all of lowest staff
                i = len(self.original_score.getElementsByClass(m21.stream.Part)) - 1
                self._bassline = copy.deepcopy(self.original_score.getElementsByClass(m21.stream.Part)[i])
                LOG.debug('Bassline is lowest part')
            except:  # TODO - figure out type of exception
                raise InputError('Cannot extract bass line from score')

        self._clean_bassline_single_voice()

    def _clean_bassline_single_voice(self):
        """
        Rewrites bassline as lowest line of multi-voice bassline.

        TO-DO: currently throws error; need to actually FIX this!

        """
        newline = self._bassline.chordify()
        chords = newline.flat.getElementsByClass(m21.chord.Chord)
        for c in chords:
            if len(c) > 1:
                raise InputError('Bass line is not monophonic!')

    def makeFiguredBassObject(self):
        """
        Converts ``self._bassline`` stream to :mod:`music21.figuredBass` object ``self.fb``.


        In future, useful for piping output from this figure divination module
        to a module for figure realization.

        """
        LOG.debug('doing \'makeFiguredBassObject.\'')
        try:
            self.fb = m21.figuredBass.realizer.figuredBassFromStream(self._bassline)
        except:
            LOG.debug('Could not convert to figured bass object!')
        # Programmer note: to get the actual score from figuredbass object,
        # do self.fb.generateBassLine()

    def extract(self):
        """
        Main ExtractionWork method; extracts the figured bass from score.

        """
        #Remove passing tones?
        if self.remove_passing_option:
            self._clean_bassline_remove_passing_tones()

        #Set up the figure strings:
        basslength = len(self._bassline.flat.getElementsByClass(m21.note.Note))
        self._fb_figureString = ['n' for x in range(basslength)]

        #Run through rules
        ruler = rule_crawler.rule_crawler(self)
        ruler.full_check_rules()
        ruler.full_apply_rules(direction=self.rule_application_direction)

        #Plot the results
        if self.save_option == True or self.display_option == True:
            rule_plotter.makePlotFromScore(self, filepath=self.output_filename, viewResults=self.display_option, direction=self.rule_application_direction)

        #Clean up figures
        if self.clean_option == True:
            self._clean_figures()

        #Add figures into score:
        for i in range(basslength):
            n = self._bassline.flat.getElementsByClass(m21.note.Note)[i]
            f = self._fb_figureString[i]
            try:
                m21.figuredBass.realizer.addLyricsToBassNote(n, f)
            except KeyError as e:
                print e

        #Going to realize the figures soon? Make it a figuredBass object!
        if self.create_fb_object:
            print 'makin fb'
            self.makeFiguredBassObject()

    def _clean_bassline_remove_passing_tones(self):
        """
        Removes identified passing tones from bassline using music21 methods.

        TO-DO!
        """
        pass

    def _clean_figures(self):
        """
        Makes figured output cleaner by hiding implied figures (e.g. '5,3').

        """
        for i in range(len(self._fb_figureString)):
            fig = self._fb_figureString[i]

            #TODO - in all cases? dependent on the key quality??
            if fig in ['5,3', '5,3+', '5,3-', '3-']:
                self._fb_figureString[i] = ''

            if fig == '6,5,3':  # TODO - 27b; etc.
                self._fb_figureString[i] = '6,5'

            if fig == '6,3':
                self._fb_figureString[i] = '6'

            if fig == '7,3+':
                self._fb_figureString[i] = '7'

    def _setup_output(self):  # TODO-Hh{non-critical: metadata fail!}
        """
        Attempts to add metadata to new score. Doesn't work.

        TO-DO! Fix this. :)

        """
        #Create output metadata
        my_metadata = m21.metadata.Metadata()
        my_metadata.title = 'Figured bass reduction of \n' + str(self.title)
        my_metadata.composer = str(self.composer) + '\nFigure extraction: Auto'

        #Add metadata to output score
        self.output_score.metadata = my_metadata
        self.output_fb_score.metadata = my_metadata

    def _append_to_extraction(self):
        """
        Appends original score and user-input solution to figured output.

        """
        #append the original to the extraction
        LOG.debug('appending original!')
        for partline in (self.original_score.getElementsByClass(m21.stream.Part)):
            self.output_score.insert(partline)

        for n in self.output_score.flat:
            n.color = 'blue'

        #append the solution to the extraction?
        if self.solution != False and self.solution != 'x':
            LOG.debug('appending solution!')
            #Insert the solution below the reduction
            solutionline = m21.stream.Part()
            solutionline.append(m21.tinyNotation.TinyNotationStream(self.solution))
            for n in solutionline.flat:
                n.color = 'red'
            self.output_score.insert(solutionline)

    def create_output(self):
        """
        Creates, formats, and saves/displays figured output score.

        """
        #Set up output
        self._setup_output()

        #Showing solution and/or original with old?
        #append original score and/or solution to test file
        self._append_to_extraction()

        #Make score from bassline
        self.output_score.insert(0, self._bassline)
        self.output_fb_score.insert(0, self._bassline)

        #save the file?
        if self.save_option == True:
            LOG.debug('\tSaving the file!')
            xmlfilename = self.output_filename + '.xml'
            self.output_score.write(fmt='musicxml', fp=xmlfilename)
            LOG.info('File saved to %s in the figured_bass_extractor/ directory' % xmlfilename)

        #display the new file?
        if self.display_option == True:
            if self.save_option == True:
                try:
                    new_score = m21.converter.parse(xmlfilename)
                    new_score.show()
                    #self.output_score.show()
                    LOG.info('Displaying output if xml viewer has been installed.')
                except:  # TODO - figure out type of exception
                    LOG.info('Unable to show .xml output through MusicXML,')
                    LOG.info('try opening the file directly.')
            #If file hasn't been saved, can't show it by opening old file; must open current object
            else:
                self.output_score.show()

        else:
            LOG.info('Not displaying file.')


def full_extraction(scorefile, **kwargs):
    #TODO - make full_extraction_with_solution
    """
    Creates an ExtractionWork object and runs the full figure divination process.

    Same kwargs as :mod:`ExtractionWork`: ruleset, display, save,
    remove_passing, rule_direction, clean, solution, and make_fb_object.

    """
    #Get, load score
    my_work = ExtractionWork(scorefile, **kwargs)

    #Prepare output
    my_work._setup_output()

    #make extract
    my_work.extract()

    #do output
    my_work.create_output()

    #done!
    LOG.info('Done with full extraction.')

    return my_work


# Run from command line:
if __name__ == '__main__':
    #Run full_extraction function.

    #Get, parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('-o', action='store_false',
                    dest='display_outputs', default=True,
                    help='View outputs in MusicXML interface?')
    parser.add_argument('-s', action='store_false',
                    dest='save_outputs', default=True,
                    help='Save output in MusicXML interface?')
    parser.add_argument('-c', action='store_false',
                    dest='clean_figure_string', default=True,
                    help='Visually remove redundant figures from output?')
    parser.add_argument('-p', action='store_true',
                    dest='remove_passing', default=False,
                    help='Remove passing tones from bassline?')
    parser.add_argument('-t', nargs='?', const='x',
                    dest='solution_notation_string', default=False,
                    help='TODO')
    parser.add_argument('-r', nargs='*',
                    dest='rule_set_or_list', default='SL',
                    help='Set of rules to apply')
    parser.add_argument('-b', nargs='?', const='backward',
                    dest='rule_direction', default='forward',
                    help='Direction rules are applied: forward or backward')

    #Set flags
    args = parser.parse_args()
    input_file_name = args.input_file  # The un-figured xml file to be parsed
    ruleset = args.rule_set_or_list  # The name of a rule set or list of rules to apply
    solution = args.solution_notation_string  # A solution string (in music21 tiny notation)
    clean = args.clean_figure_string  # If true, makes result visually cleaner by removing '3,5' etc.
    remove_passing = args.remove_passing  # If true, removes passing tones from bassline
    display = args.display_outputs  # If true, displays score and visualisation
    save = args.save_outputs  # If true, saves .xml file
    rule_direction = args.rule_direction  # Direction rules are applied (default forward)

    full_extraction(input_file_name, \
                    ruleset=ruleset, \
                    solution=solution, \
                    clean=clean, \
                    remove_passing=remove_passing, \
                    save=save, \
                    display=display, \
                    rule_direction=rule_direction
                    )
