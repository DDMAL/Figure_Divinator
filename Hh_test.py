from music21 import *
import copy

score = converter.parse('xml_test_files_SL/Hotteterre-Op2-No3-1-Allemande.xml')
score = (score.measures(1, 4))

bassnum = len(score.getElementsByClass(stream.Part)) - 1
bassline = copy.deepcopy(score.getElementsByClass(stream.Part)[ bassnum ])

chords = score.chordify()

# for c in extraction.flat.getElementsByClass('Chord'):
#     c.closedPosition(forceOctave=4, inPlace=True)
#     c.removeRedundantPitches(inPlace=True)
#     c.annotateIntervals()

for n in bassline.flat:
    n.color = "red"

for n in chords.flat:
	n.color = "blue"

score.show()
bassline.show()
chords.show()

#bassline.insert(-1, chords.getElementsByClass(stream.Part)[0])
#bassline.show()

print "\nScore:"
for x in score:
	print x

print "\nChords:"
for x in chords:
	print x

print "\nBassline:"
for x in bassline:
	print x


# score.insert(-1,extraction)
# score.show()


# solution = tinyNotation.TinyNotationStream('E2_#6 F2_6')

# extraction.insert(0,solution)

# for n in solution.flat:
#     n.color = "blue"

# for p in score.getElementsByClass(stream.Part):
# 	extraction.insert(-1,p)


# #extraction.insert(0,solution)
# extraction.show()
# score.show()