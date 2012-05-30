import figure_extractor
from music21 import *

solutions = [
                ('1a', 'BB2_6 C2_falsefifth'),
    			('2', 'BB-1_6  AA1'),
    			('3', 'E2_#6 F2_6'),
    			('4', 'D2  BB2_falsefifth'),
    			('5', 'D2 BB-2_6')
            ]
SIZE = 2; #Number of parts in the test files -- hardcoded!


#Setup
resultsscore = stream.Score()
resultsscore.append(metadata.Metadata())
resultsscore.metadata.title = "Saint Lambert's examples"

numparts = SIZE + 2
numstrings = ['Solution key:','Our extraction:']
for i in range(numparts):
    resultsscore.append(stream.Part())
    n = note.Note()
    n.duration.type = "whole"
    n.color = 'blue'
    n.lyric = ':'
    if i == 0: n.lyric = '   Original:'
    if i == SIZE:
        n.lyric = 'Solution key:'
        n.color = 'red'
    if i == SIZE + 1:
        n.lyric = 'Our extraction:'
        n.color = 'black'
    p = stream.Part()
    p.append(n)
    resultsscore.parts[i].append(p)

for x in solutions:
    print "* * * *Starting sample " + x[0] + "* * * * *"
    #Get the extraction
    this_rule = 'SLRule' + x[0]
    this_file = 'xml_test_files_SL/Lambert ' + x[0] + '.xml'
    this_solution = x[1]
    score = figure_extractor.full_extraction(this_file, this_rule, solution=this_solution, display=False)

    #Label the extracted score
    if score.output_score[2].flat.getElementsByClass(note.Note)[0]:
        lyriclabel = '<File ' +  x[0] + '>'
        score.output_score[2].flat.getElementsByClass(note.Note)[0].lyric = lyriclabel

    #Add this extracted score to full results
    for i in range(numparts):
        resultsscore.parts[i].append(score.output_score[i+1])

resultsscore.show()
print 'done'