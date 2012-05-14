from music21 import *
import copy

url='xml_test_files_SL/Hotteterre-Op2-No3-1-Allemande.xml'

#Import original
score = converter.parse(url)
oldtitle=""
oldcomposer=""
try:
	oldtitle = score.metadata.title
	oldcomposer= score.metadata.composer
except:
	oldtitle = str(url)

#Make smaller for ease
score = (score.measures(1, 4))

#Get the bassline from the original
bassnum = len(score.getElementsByClass(stream.Part)) - 1
bassline = copy.deepcopy(score.getElementsByClass(stream.Part)[ bassnum ])
for n in bassline.flat:
    n.color = "red"

#Get the chords from the original
chords = score.chordify()
for c in chords.flat.getElementsByClass('Chord'):
    c.closedPosition(forceOctave=4, inPlace=True)
    c.removeRedundantPitches(inPlace=True)
    c.annotateIntervals()
    c.color = "blue"

#Make the score to return (incl. fig. bass)
reduction = stream.Score()
reduction.insert(0,bassline)

#Add metadata
if not reduction.metadata:
	reduction.insert(metadata.Metadata())
reduction.metadata.title = 'Figured bass reduction of \n' + oldtitle + '\n\n'
reduction.metadata.composer = oldcomposer + '\nFigure extraction: Automated'


#Insert the solution below the reduction
solution = tinyNotation.TinyNotationStream('E2_#6 F2_6')
for n in solution.flat:
	n.color="green"
reduction.insert(0,solution)

#Insert the original at the top
for partline in score.getElementsByClass(stream.Part):
 	reduction.insert(-1,partline)

#Insert the chords above the reduction
reduction.insert(-1,chords)

reduction.show()