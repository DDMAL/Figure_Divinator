import figure_extractor
import music21 as m21
import argparse
import string

import logging_setup as Logging
import logging
LOG = Logging.getLogger('rules')
LOG2 = Logging.getLogger('f_extractor')


def _SL_full_test(chosen_rules=False):

    if chosen_rules != False:
        if chosen_rules[0] == False:
            chosen_rules = False
        else:
            for x in range(len(chosen_rules)):
                r = chosen_rules[x]
                if len(r) == 1 or not r[1].isdigit():
                    chosen_rules[x] = '0' + r

    # Number of parts in each .xml test files -- hard-coded!
    SIZE = 2
    solutions = {
        '03_1'   : "r2 A2_6 B-2 r2",                       # Page number: 45
        '03_2'   : "D2_6 E-2 r2",                       # Page number: 45
        '03_3'   : "r2 GG2_6 AA-2",                       # Page number: 45
        '04_1'   : "r2 A2 B-2_6",                       # Page number: 46
        '04_2'   : "r2 A2 B-2_6",                       # Page number: 46
        '05_1'   : "r2 F2_6 E2",                        # Page number: 46
        '05_2'   : "r2 B-2_6 A2",                       # Page number: 46
        '06_1'   : "r2 E2_6+ F2_6",                     # Page number: 46
        '06_2'   : "r2 BB2_6+ C2_6",                     # Page number: 46
        '06_3'   : "r2 E2_6+ F2_6",                     # Page number: 46
        '06_4'   : "r2 BB2_6+ C2_6",                     # Page number: 46
        '07_1'   : "r2 D2 BB2 C2_b AA2 BB-1",              # Page number: 47
        '07_2'   : "G2_b E2 F2_b D2_? E-1",               # Page number: 47
        '08b_1'  : "F2 D2_6b Eb2 C2_6 D1_#",        # Page number: 47
        '08b_2'  : "F4 E-4 D2_6,b E-4 D4 C2_6 D1_#",  # Page number: 47
        '08a_1'  : "F2 D2 E-2 C2 D1_#",              # Page number: 47
        '08a_2'  : "F4 E-4 D2 Eb4 D4 C2 D1_#",       # Page number: 47
        '10a'    : "A4 F#4_6 D4 E4_# C#4_6 AA4 D8 C#8 D8 E8 F#8 D8 E8_# F#8 E8 D8 C#8 BB8 AA4_# E4_# EE4_7 AA2_#",  # Page number: 47
        #'10a'    : "A4 F#4_6 D4 E4_# C#4_6 AA4 D8 C#8 D8 E8 F#8 D8 E8_# F#8 E8 D8 C#8 BB8 AA4_# E4_# EE4_7 AA2+4_#",  # Page number: 47
        #'10a'    : "3/4 A4 F#4_6 D4 E4_# C#4_6 AA4 D8 C#8 D8 E8 F#8 D8 E8_# F#8 E8 D8 C#8 BB8 AA4_# E4_# EE4_7 AA2+4_#",  # Page number: 47
        '11'     : "r4 C2 AA2_6",                        # Page number: 47
        '12'     : "F2 BB2",                          # Page number: 48
        '13'     : "c2 E2_6",                        # Page number: 48
        '14'     : "EE4_6 FF4_6,5 GG4",                  # Page number: 48
        '15'     : "D4 C4_6,#4,2 BB2_6",                # Page number: 49
        '16'     : "D4 C4_6,#4,2 BB-2_7",               # Page number: 49
        '17'     : "D2 BB-2_6 C2",                    # Page number:
        '18'     : "r2 GG2 EE2_6 FF2",                     # Page number: 50
        '19'     : "r2 BB2_6,5,3 GG2_7 C1",                 # Page number: 51
        '20'     : "E2_6-5 F2 C2",                   # Page number: 50
        '21'     : "r2 C2 C2_6 GG",                      # Page number: 51
        '22'     : "r2 C2 C2_6,#4,2 GG2",                  # Page number: 51
        '23'     : "r2 C4 D4_6 E2_6,b5,3 F1",             # Page number: 51
        '24a'    : "F4 E4_6 D4_6+ C2+4",             # Page number: 52
        '24b1'   : "r4 F4 E-4_6,#4,2 D4_6+ C2+4_b",       # Page number: 52-53
        '24b2'   : "r4 F4_b E-4_6,4,2 D4_6+,4,3 C2+4_b",     # Page number: 52-53
        '24c'    : "r4 A4 G4 F4_6 E2+4_#",              # Page number: 53
        '25a'    : "r4 G4 F4_6,#4,2 E4_6 D4_6+ C1",       # Page number: 54
        '25b'    : "G4 F4_6,#4,2 E-4_6 D4_6+ C1_b",    # Page number: 54
        '26a1'   : "G4 F4_6,#4,2 E4_6 D4_6+ C4 BB1_6",  # Page number: 54
        '26a2'   : "G4 F4_6,#4,2 E4_6 D4_6+ C4 GG1",    # Page number: 54
        '27a'    : "C4 D4_6,4,3 E4_6 F4_6,5,3 G1",       # Page number: 55
        '27b'    : "C4_b D4_6,4,3 E-4_6 F4_6,5,3 G1",    # Page number: 55
        '28'     : "G2_5,4 GG2_7 C1",                  # Page number: 55
        '29'     : "GG1_5,4,7 C1",                     # Page number: 55
        '30'     : "GG4_7 C1",                        # Page number: 56
        '31_1'    : "GG2._5,4;7 C2.",                 # Page number: 56
        '31_2'    : "GG2._5,4;7 C2.",                 # Page number: 56
        '32'     : "GG2._5,4;8,5,3;7,5,3 C2."            # Page number: 56
        }

    #Setup
    resultsscore = m21.stream.Score()
    resultsscore.append(m21.metadata.Metadata())
    resultsscore.metadata.title = "Saint Lambert's examples"

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
            n.lyric = 'Solution key:'
            n.color = 'red'
        if i == SIZE + 1:
            n.lyric = 'Our extraction:'
            n.color = 'black'
        p = m21.stream.Part()
        p.append(n)
        resultsscore.parts[i].append(p)

    for item in sorted(solutions.iteritems()):
        rule_number = item[0]

        rule_number_split = rule_number.split('_')
        just_number = rule_number_split[0].translate(None, string.letters)
        if chosen_rules != False and just_number not in chosen_rules:
            continue

        if len(rule_number_split) == 1:
            print "- - ->Testing rule/excerpt " + rule_number_split[0]
        else:
            print "- - ->Testing rule/excerpt " + rule_number_split[0] + " (" + rule_number_split[1] + ")"

        try:
            #Set up the extraction
            this_rule = ['SLRule_' + rule_number_split[0]]
            this_file = 'examplefiles_SL/SLRule_' + rule_number + '.xml'
            this_solution = solutions[rule_number]

            #Get extraction (while suppressing output)
            oldLog = LOG.level
            oldLog2 = LOG2.level
            LOG.setLevel(logging.CRITICAL)
            LOG2.setLevel(logging.CRITICAL)
            score = figure_extractor.full_extraction(this_file, ruleset=this_rule, solution=this_solution, display=False, save=False)
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

    resultsscore.show()
    print 'Done with SL test.'


# Run from command line:
if __name__ == '__main__':
    #Get, parse argument
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', nargs='*', dest='rules',
                        default=False,
                        help='Set of rules to list')
    args = parser.parse_args()

    _SL_full_test(args.rules)
