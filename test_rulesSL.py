import figure_extractor
import music21 as m21

SIZE = 2  # Number of parts in each .xml test files -- hard-coded!

solutions = {
 #  'RULE_NAME_.xml'    : "SOLUTION STRING",                # Page number: #
    '3_1'    : "A2_6 Bb2",                       # Page number: 45
    '3_2'    : "D2_6 Eb2",                       # Page number: 45
    '3_3'    : "G2_6 Ab2",                       # Page number: 45
    '4_1'    : "A2 Bb2_6",                       # Page number: 46
    '4_2'    : "A2 Bb2_6",                       # Page number: 46
    '5_1'    : "F2_6 E2",                        # Page number: 46
    '5_2'    : "Bb2_6 A2",                       # Page number: 46
    '6_1'    : "E2_#6 F2_6",                     # Page number: 46
    '6_2'    : "B2_#6 C2_6",                     # Page number: 46
    '6_3'    : "E2_#6 F2_6",                     # Page number: 46
    '6_4'    : "B2_#6 C2_6",                     # Page number: 46
    '7_1'    : "D2 B2 C2_b A2 Bb1",              # Page number: 47
    '7_2'    : "G2_b E2 F2_b Eb1",               # Page number: 47
    '8b_1'   : "F2 D2_6,b Eb2 C2_6 D1_#",        # Page number: 47
    '8b_2'   : "F4 Eb4 D2_6,b Eb4 D4 C2_6 D1_#",  # Page number: 47
    '8a_1'   : "F2 D2 Eb2 C2 D1_#",              # Page number: 47
    '8a_2'   : "F4 Eb4 D2 Eb4 D4 C2 D1_#",       # Page number: 47
    '10_a'   : "A4 F#4_6 D4 E4_# C#4_6 A4 D8 C#8 D8 E8 F#8 D8 E8_# F#8 E8 D8 C#8 B8 A4_# E4_# E4_7 A2+4_#",  # Page number: 47
    '11'     : "C2 A2_6",                        # Page number: 47
    '12'     : "F2 B2",                          # Page number: 48
    '13'     : "C2 E2_6",                        # Page number: 48
    '14'     : "E4_6 F4_65 G4",                  # Page number: 48
    '15'     : "D4 C4_6#42 B2_6",                # Page number: 49
    '16'     : "D4 C4_6#42 Bb2_7",               # Page number: 49
    '17'     : "D2 Bb2_6 C2",                    # Page number:
    '18'     : "G2 E2_6 F2",                     # Page number: 50
    '19'     : "B2_653 G2_7 C1",                 # Page number: 51
    '20'     : "E2_6b5 F2 C2",                   # Page number: 50
    '21'     : "C2 C2_6 G",                      # Page number: 51
    '22'     : "C2 C2_6#42 G2",                  # Page number: 51
    '23'     : "C4 D4_6 E2_6b53 F1",             # Page number: 51
    '24a'    : "F4 E4_6 D4_#6 C2+4",             # Page number: 52
    '24b1'   : "F4 Eb4_6#42 D4_#6 C2+4_b",       # Page number: 52-53
    '24b2'   : "F4_b E4_642 D4_#643 C2+4_b",     # Page number: 52-53
    '24c'    : "A4 G4 F4_6 E2+4_#",              # Page number: 53
    '25a'    : "G4 F4_6#42 E4_6 D4_#6 C1",       # Page number: 54
    '25b'    : "G4 F4_6#42 Eb4_6 D4_#6 C1_b",    # Page number: 54
    '26a1'   : "G4 F4_6#42 E4_6 D4_#6 C4 B1_6",  # Page number: 54
    '26a2'   : "G4 F4_6#42 E4_6 D4_#6 C4 G1",    # Page number: 54
    '27a'    : "C4 D4_643 E4_6 F4_653 G1",       # Page number: 55
    '27b'    : "C4_b D4_643 Eb4_6 F4_653 G1",    # Page number: 55
    # '28'     : "G2_54 G2_7 C1",                  # Page number: 55
    '29'     : "G1_54,7 C1",                     # Page number: 55
    '30'     : "G4_7 C1",                        # Page number: 56
    '31a'    : "G2+4_54,7 C2+4",                 # Page number: 56
    '31b'    : "G2+4_54,7 C2+4",                 # Page number: 56
    '32'     : "G2+4_54,853,753 C2+4"            # Page number: 56
    }

#Setup
resultsscore = m21.stream.Score()
resultsscore.append(m21.metadata.Metadata())
resultsscore.metadata.title = "Saint Lambert's examples"

numparts = SIZE + 2
numstrings = ['Solution key:', 'Our extraction:']
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

for rule_number in solutions.keys():

    rule_number_split = rule_number.split('_')
    if len(rule_number_split) == 1:
        print "\n- - - - - - ->Starting rule " + rule_number_split[0] + "<- - - - - - -"
    else:
        print "\n- - - - - - ->Starting rule " + rule_number_split[0] + " (" + rule_number_split[1] + ") <- - - - - - -"

    try:
        #Get the extraction
        this_rule = 'SLRule_' + rule_number_split[0]
        this_file = 'examplefiles_SL/SLRule_' + rule_number + '.xml'
        this_solution = solutions[rule_number]
        score = figure_extractor.full_extraction(this_file, this_rule, solution=this_solution, display=False, save=False)

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
print 'done'
