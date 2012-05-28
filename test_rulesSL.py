import figure_extractor
from music21 import *

solutions = {	'1a': 'BB2_6 C2', 
				'1b':'AA2  BB-2_6',
				'2':'BB-2_6  AA2',
				'3':'E2_#6 F2_6',
				'4':'D2  BB2',
				'5':'D2 BB-2'}

resultsscore = stream.Score()
m = stream.Measure()

for x in solutions.keys():
    this_rule = 'SLRule' + x
    this_file = 'xml_test_files_SL/Lambert ' + x + '.xml'
    this_solution = solutions[x]
    score = figure_extractor.full_extraction(this_file, this_rule, solution=this_solution, display=False)

    #first time through
    if x == solutions.keys()[0]:
        numparts = len(score.output_score.getElementsByClass(stream.Stream))
        print numparts
        for i in range(numparts):
            resultsscore.append(stream.Part())

    #Every time
    for i in range(numparts):
        r = note.Rest(type='whole')
        r.lyric = "hi"
        m = stream.Measure()
        m.append(r)
        resultsscore.append(m.makeAccidentals(inPlace=True))
        resultsscore[i].append(score.output_score[i+1])
        
resultsscore.show()
print 'done'


r = note.Rest(type='whole')
r.lyric = "hi"
m = stream.Measure()
m.append(r)
resultsscore.append(m.makeAccidentals(inPlace=True))
