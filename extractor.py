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
import logging #TODO-Hh{read about logging! implement this!}

from music21 import corpus
from music21 import converter

import rules

import engine # Searching an 'optimal' application of the rules found in 
              # rules.py (or other rule file)

# Import Psyco if available...for a little speed.
try:
    import psyco
    psyco.full()
except ImportError:
    pass

class FileNotFoundError(Exception):
    pass

class InputError(Exception):
    pass

#Get, parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('input_file')
parser.add_argument("-r", dest="rules_type",
                default="rules", help="Set of rules to apply")
parser.add_argument("-o", action="store_true",
                    dest="viewOutput", default=False,
                    help="View output in MusicXML interface?")

#Set flags
args = parser.parse_args()
scoreFile = args.input_file
ruleSet = args.rules_type
viewOutput = args.viewOutput

#set output file additional string
if ruleSet == "SL":
    ext_rule = "_SL"
else:
    ext_rule = ""

try:
    if not os.path.isfile(scoreFile):
        raise FileNotFoundError(scoreFile)

    (input_base,ext_sep,input_ext) = scoreFile.rpartition(os.extsep)

    input_file_name = input_base + ext_sep+input_ext

    output_file_name = (input_base + "_figured_bass" + ext_rule + 
                        ext_sep + input_ext)

    # Open work with Music21
    try:
        work = corpus.parseWork(input_file_name)
    except:
        raise InputError("score is not compatible with Music21 input formats")

    # Get the extraction rules
    extraction_rules = rules.get_rules(ruleSet)

    # Create the engine
    #extraction_engine = engine.GreedyEngine(work,extraction_rules)
    extraction_engine = engine.WindowedGreedyEngine(work,extraction_rules)

    # Set the engine.explorer parameters
    # (this is specific to the kind of engine)

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
    
    # Call the engine
    extraction_engine.compute_figured_bass()

    # Write the figured bass
    extraction_engine.write_figured_bass(output_file_name)
    print "\nGreat! It should have saved as '%s'\n" % output_file_name
    
    if viewOutput:
        print "Displaying output if xml viewer has been installed."
        s = converter.parse(output_file_name)
        s.show()

except FileNotFoundError as file:
    print "file '%s' does not exists" % file
    exit(1)

except InputError as msg:
    print "score %s is invalid: %s" % (sys.argv[1],msg)
    exit(1)

except engine.EngineParameterError as msg:
    print "Engine parameter error: " + str(msg)
    exit(1)

except rules.RuleImplementationError:
    print "cannot find extraction rules in rules.py or rules are not all valid"
    exit(1)
