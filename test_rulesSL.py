# Copyright (C) 2012 by Hannah Robertson
"""
Script for testing specific rules in the Saint Lambert rule set.

To run from command line, in terminal run ::

    python test_rulesSL.py [-r rule_numbers]

where rule_numbers correspond to rules in the set, e.g. ``-r 3 5 20``.

For full command line option flags, in terminal do ::

    python test_rulesSL.py -h

Written to be easily converted to test any other rule set. To do this, see
comments inside script.

"""

import figure_extractor
import music21 as m21
import argparse

import logging_setup as Logging
import logging
LOG = Logging.getLogger('rules')
LOG2 = Logging.getLogger('f_extractor')


###############################################################################
## Building a new testing script? Only change the variables in this section! ##
###############################################################################

SIZE = 2        # Number of parts in each .xml test file (piano scores prob. have 2)
OUTPUT_TITLE = "Saint Lambert's examples"
RULE_PREFIX = "SLRule_"    # Prefix for all rules being tested. If none, use ''
XML_FILE_LOCATION_AND_PREFIX = "examplefiles_SL/SLRule_"  # Where the test files are stored

# Solution dictionary should be of the form 'rulekey': 'solutionNotationString'
# ruleKey should be the name of the rule number (w/out prefix). If there are multiple
# test files for a single rule, append '_casenumber' to the rulekey. For example,
# a single test file for rule SLRule_03 should be saved as 'SLRule_03.xml' and
# would therefore have ruleKey '03'; multiple files could be named
# 'SLRule_03_1.xml' and 'SLRule_03_2.xml' and have ruleKeys '03_1' and '03_2'.

SOLUTION_DICTIONARY = {
        '03_1'   : "r2 A2_6 B-2 r2",                        # Page number: 45
        '03_2'   : "D1_6 E-1",                              # Page number: 45
        '03_3'   : "GG1_6 AA-1",                            # Page number: 45
        '04_1'   : "A1 B-1_6",                              # Page number: 46
        '04_2'   : "A1 B-1_6",                              # Page number: 46
        '05_1'   : "F1_6 E",                                # Page number: 46
        '05_2'   : "B-1_6 A",                               # Page number: 46
        '06_1'   : "E1_6+ F1_6",                            # Page number: 46
        '06_2'   : "BB1_6+ C1_6",                           # Page number: 46
        '06_3'   : "E1_6+ F1_6",                            # Page number: 46
        '06_4'   : "BB1_6+ C1_6",                           # Page number: 46
        '07_1'   : "D2 BB2 C2_b AA2 BB-1",                  # Page number: 47
        '07_2'   : "G2_b E2 F2_b D2_? E-1",                 # Page number: 47
        '08b_1'  : "F2 D2_6b Eb2 C2_6 D1_#",                # Page number: 47
        '08b_2'  : "F4 E-4 D2_6,b E-4 D4 C2_6 D1_#",        # Page number: 47
        '08a_1'  : "F2 D2 E-2 C2 D1_#",                     # Page number: 47
        '08a_2'  : "F4 E-4 D2 Eb4 D4 C2 D1_#",              # Page number: 47
        '10a'    : "A4 F#4_6 D4 E4_# C#4_6 AA4 D8 C#8 D8 E8 F#8 D8 E8_# F#8 E8 D8 C#8 BB8 AA4_# E4_# EE4_7 AA2._#",  # Page number: 47
        #'10a'    : "3/4 A4 F#4_6 D4 E4_# C#4_6 AA4 D8 C#8 D8 E8 F#8 D8 E8_# F#8 E8 D8 C#8 BB8 AA4_# E4_# EE4_7 AA2+4_#",  # Page number: 47
        '11'     : "C2 AA2_6",                              # Page number: 47
        '12'     : "F2 BB2",                                # Page number: 48
        '13'     : "c2 E2_6",                               # Page number: 48
        '14'     : "EE4_6 FF4_6,5 GG4",                     # Page number: 48
        '15'     : "D4 C4_6,4+,2 BB2_6",                    # Page number: 49
        '16'     : "D4 C4_6,4+,2 BB-2_7",                   # Page number: 49
        '17'     : "D2 BB-2_6 C1",                          # Page number:
        '18'     : "GG2 EE2_6 FF1",                         # Page number: 50
        '19'     : "BB2_6,5,3 GG2_7 C1",                    # Page number: 51
        '20'     : "E2_6,5b F2 C1",                         # Page number: 50
        '21'     : "C2 C2_6 GG1",                           # Page number: 51
        '22'     : "C2 C2_6,4+,2 GG1",                      # Page number: 51
        '23'     : "C4 D4_6 E2_6,b5,3 F1",                  # Page number: 51
        '24a'    : "F4 E4_6 D4_6+ C2.",                     # Page number: 52
        '24b1'   : "F4 E-4_6,4+,2 D4_6+ C2._b",             # Page number: 52-53
        '24b2'   : "F4_b E-4_6,4,2 D4_6+,4,3 C2._b",        # Page number: 52-53
        '24c'    : "A4 G4 F4_6 E2._#",                      # Page number: 53
        '25a'    : "G4 F4_6,4+,2 E4_6 D4_6+ C1",            # Page number: 54
        '25b'    : "G4 F4_6,4+,2 E-4_6 D4_6+ C1_b",         # Page number: 54
        '26a1'   : "r2. G4 F4_6,4+,2 E4_6 D4_6+ C4 BB1_6",  # Page number: 54
        '26a2'   : "r2. G4 F4_6,4+,2 E4_6 D4_6+ C4 GG1",    # Page number: 54
        '27a'    : "C4 D4_6,4,3 E4_6 F4_6,5,3 G1",          # Page number: 55
        '27b'    : "C4_b D4_6,4,3 E-4_6 F4_6,5,3 G1",       # Page number: 55
        '28'     : "G2_5,4 GG2_7 C1",                       # Page number: 55
        '29'     : "GG1_5,4,7 C1",                          # Page number: 55
        '30'     : "GG1_7 C1",                              # Page number: 56
        '31_1'    : "GG2._5,4;7 C2.",                       # Page number: 56
        '31_2'    : "GG2._5,4;7 C2.",                       # Page number: 56
        '32'     : "GG2._5,4;8,5,3;7,5,3 C2."               # Page number: 56
        }

###############################################################################
## Anything below this section probably shouldn't be modified! ################
###############################################################################


def _SL_full_test(chosen_rules=False, clean=True, show_all_output=False):
    """
    Tests a set of rules against unit test files (.xml) and given solutions.

    Outputs a single solution score.

    """
    if chosen_rules != False:
        if chosen_rules[0] == False:
            chosen_rules = False
        else:
            for x in range(len(chosen_rules)):
                r = chosen_rules[x]
                if len(r) == 1 or not r[1].isdigit():
                    chosen_rules[x] = '0' + r

    #Setup
    resultsscore = m21.stream.Score()
    resultsscore.append(m21.metadata.Metadata())
    resultsscore.metadata.title = OUTPUT_TITLE

    numparts = SIZE + 2
    for i in range(numparts):
        resultsscore.append(m21.stream.Part())
        n = m21.note.Note()
        n.duration.type = "whole"
        n.color = 'blue'
        n.lyric = ':'
        if i == 0:
            n.lyric = '   Original:'
        if i == SIZE:
            n.lyric = 'Given Solution:'
            n.color = 'red'
        if i == SIZE + 1:
            n.lyric = 'Figure Divination:'
            n.color = 'black'
        p = m21.stream.Part()
        p.append(n)
        resultsscore.parts[i].append(p)

    for item in sorted(SOLUTION_DICTIONARY.iteritems()):
        rule_number = item[0]

        rule_number_split = rule_number.split('_')
        just_number = rule_number_split[0][:2]
        if chosen_rules != False and just_number not in chosen_rules:
            continue

        if len(rule_number_split) == 1:
            print "- - ->Testing rule/excerpt " + rule_number_split[0]
        else:
            print "- - ->Testing rule/excerpt " + rule_number_split[0] + " (" + rule_number_split[1] + ")"

        try:
            #Set up the extraction
            this_rule = [RULE_PREFIX + rule_number_split[0]]
            this_file = 'examplefiles_SL/SLRule_' + rule_number + '.xml'
            this_solution = SOLUTION_DICTIONARY[rule_number]

            #Get extraction (while suppressing output)
            oldLog = LOG.level
            oldLog2 = LOG2.level
            if not show_all_output:
                LOG.setLevel(logging.CRITICAL)
                LOG2.setLevel(logging.CRITICAL)
            score = figure_extractor.full_extraction(this_file, ruleset=this_rule, solution=this_solution, clean=clean, display=False, save=False)
            LOG.setLevel(oldLog)
            LOG2.setLevel(oldLog2)

            #Label the extracted score
            if score.output_score[2].flat.getElementsByClass(m21.note.Note)[0]:
                lyriclabel = '<File ' + rule_number + '>'
                score.output_score[2].flat.getElementsByClass(m21.note.Note)[0].lyric = lyriclabel

            #Add this extracted score to full results
            for i in range(numparts):
                resultsscore.parts[i].append(score.output_score[i + 1])
        except:
            print "Nope, problems with %s. On to the next one." % rule_number

    #Save result score - TODO
    xmlfilename = 'results/unit_testing_' + RULE_PREFIX + 'rules.xml'
    resultsscore.write(fmt='musicxml', fp=xmlfilename)
    print 'File saved to figured_bass_extractor/%s' % xmlfilename

    #Show result score
    resultsscore.show()
    print 'Done with test of %s.' % OUTPUT_TITLE


# Run from command line:
if __name__ == '__main__':
    #Get, parse argument
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', action='store_false',
                    dest='clean_figure_string', default=True,
                    help='Show all implicit figures (e.g. \'3,5\') in score output')
    parser.add_argument('-o', action='store_true',
                    dest='show_all_output', default=False,
                    help = 'Print/log full rule application output')
    parser.add_argument('-r', nargs='*', dest='rules',
                        default=False,
                        help='Choose rules to apply')
    args = parser.parse_args()

    _SL_full_test(chosen_rules=args.rules, clean=args.clean_figure_string,
                show_all_output=args.show_all_output)
