"""Python figured bass extractor using Music21 for score processing
"""

# See http://mit.edu/music21/doc/html/contents.html
# for Music21 docs

# See http://docs.python.org/modindex.html
# for Python docs
# (tip: googling the query usually works better)

import sys
import os
import argparse
import logging

from music21 import corpus
from music21 import converter
from music21 import stream
from music21 import * #todo-Hh{very bad!}

import rules

import engine # Searching an 'optimal' application of the rules found in
              # rules.py (or other rule file)

# Import Psyco if available...for a little speed.
try:
    import psyco
    psyco.full()
except ImportError:
    pass

import logging_setup as Logging
LOG=Logging.getLogger('extractor')

class FileNotFoundError(Exception):
    pass

class InputError(Exception):
    pass

LOG.info("\n")
#Get, parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('input_file')
parser.add_argument('-o', action='store_true',
                    dest='viewOutput', default=False,
                    help='View output in MusicXML interface?')
parser.add_argument('-r', nargs='*', dest='rules_type', default=['dummyrules'], help='Set of rules to apply')
parser.add_argument('-t', nargs='?', const='x', default=False, dest='test_string')

LOG.debug("Arguments: %s\n", parser.parse_args())

#Set flags
args = parser.parse_args()
scoreFile = args.input_file
ruleSet = args.rules_type
testState = args.test_string
viewOutput = args.viewOutput

#set output file additional string
if ruleSet[0] == "SL":
    ext_rule = "_SL"
elif ruleSet[0] == "dummyrules":
    ext_rule = ""
else:
    ext_rule = "_unique"

try:
    if not os.path.isfile(scoreFile):
        raise FileNotFoundError(scoreFile)

    (input_base,ext_sep,input_ext) = scoreFile.rpartition(os.extsep)

    input_file_name = input_base + ext_sep + input_ext

    output_file_name = (input_base + "_figured_bass" + ext_rule +
                        ext_sep + input_ext)

    # Open work with Music21
    try:
        work = converter.parse(input_file_name)
    except:
        raise InputError("score is not compatible with Music21 input formats")

    # Get the extraction rules
    extraction_rules = rules.get_rules(ruleSet)

    # Create the engine
    #extraction_engine = engine.GreedyEngine(work,extraction_rules)
    extraction_engine = engine.WindowedGreedyEngine(work,extraction_rules)

    # Set the engine.explorer parameters
    # (this is specific to the kind of engine)
    # TODO-Hh{Make specific to ruleset flag (e.g. SL probably only needs windowsize 1, increment 1 OR windowsize )}

    # Use bigger WINDOW_SIZE if rules have long-term dependencies (i.e. refer to
    # notes 'far' from the current note); Smaller WINDOW_SIZE = faster, but less
    # exploration of how rules can combine.
    extraction_engine.explorer.WINDOW_SIZE=4

    # INCREMENT must be <= WINDOW_SIZE
    # Bigger increment = faster, but less exploration of how rules can combine.
    extraction_engine.explorer.INCREMENT=2

    # Fastest setting:
    # Computes one figure at a time, without any backtracking
    #extraction_engine.explorer.WINDOW_SIZE=1
    #extraction_engine.explorer.INCREMENT=1


    # Extract figures only for a subset of the work
    # (this is useful to quickly test new rules)
    #extraction_engine.explorer.FIRST_NOTE=3
    #extraction_engine.explorer.LAST_NOTE=10
    #
    # Comment-out the lines above to extract figures for the whole work

    # If the piece size is smaller than the window, resize window
    length_piece = extraction_engine.work_browser.note_count

    if extraction_engine.explorer.WINDOW_SIZE > length_piece:
        LOG.debug("Window size too large for piece, switching to size %d", length_piece)
        extraction_engine.explorer.WINDOW_SIZE = length_piece
    if extraction_engine.explorer.INCREMENT < extraction_engine.explorer.WINDOW_SIZE:
        extraction_engine.explorer.INCREMENT = extraction_engine.explorer.WINDOW_SIZE

    # Call the engine
    extraction_engine.compute_figured_bass()

    if testState:
        LOG.info("-Testing-")

        # original unfigured
        original_work = stream.Score(work)

        fb_stream = stream.Stream(extraction_engine.apply_figured_bass())

        #for note in original_work.flat.getElementsByClass(note.Note):
        #    if note.hasLyrics():
        #        note.lyrics = ''

        #fb_stream.show('text')

        notes1 = fb_stream.flat.notes
        for thing in notes1:
            thing.color = "red"

        #original_work.insert(0,fb_stream)

        # solution
        if testState == 'x':
            pass
            original_work.show()
        else:
            solution_stream = tinyNotation.TinyNotationStream(testState)
            for n in solution_stream.flat.notes:
                n.color = "blue"
            original_work.insert(0,solution_stream)
            original_work.show()


    # Write the figured bass if it isn't in test mode
    else:
        extraction_engine.write_figured_bass(output_file_name)
        LOG.info("Great! It should have saved as '%s'",output_file_name)

        if viewOutput:
            try:
                s = converter.parse(output_file_name)
                s.show()
                LOG.info("Displaying output if xml viewer has been installed.")
            except:
                LOG.info("Unable to show .xml output through MusicXML,")
                LOG.info("try opening the file directly.")
    LOG.info("\n\n")


except FileNotFoundError as file:
    LOG.critical("file '%s' does not exists", file)
    exit(1)

except InputError as msg:
    LOG.critical("score %s is invalid: %s",sys.argv[1],msg)
    exit(1)

except engine.EngineParameterError as msg:
    LOG.critical("Engine parameter error: ",str(msg))
    exit(1)

except rules.RuleImplementationError:
    LOG.critical("cannot find extraction rules in rules.py or rules are not all valid")
    exit(1)
