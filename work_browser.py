"""Code to facilitate manipulating Music21 work, notes, intervals, etc.
"""

# See http://mit.edu/music21/doc/html/contents.html
# for Music21 docs

import music21
from music21 import clef
from music21 import note
from music21.note import Note
from music21 import interval



class WorkBrowser(object):
    """Simple class to facilitate manipulating the work.
    """

    def __init__(self,work):
        self.work = work

        # Extract the bass notes of the work
        # TODO-Hh{??Do we want to chordify before getting bassline?
        #           ...it would make sure we took all tonality changes
        #           into account...}
        # TODO-HhK{Is figured bass only notated when the bass line changes?
        #           Or maybe when any above pitch is changed, a new bass note is
        #           added and tied?}
        self.bass_notes =  self.get_bass_line().flat.getElementsByClass(Note)

        # Save a copy of the flatten work
        # ACHTUNG: this takes some time to compute.
        # Henceforth, use the copy directly (self.flat_work) to save time.
        work  = work.stripTies(inPlace=False)
        self.flat_work = work.flat.sorted

        # Save a copy of the work notes
        self.notes = self.flat_work.getElementsByClass(Note)

        # Save a copy of the work in chords
        self.chords = self.notes.chordify()

        # Caching overlapping notes
        self.overlapping_notes={}

        # Caching simultaneous notes
        self.simultaneous_notes={}

        # Caching next notes
        # Each notes is mapped to a sequence of notes
        self.next_notes={}

        # Caching previous notes
        # Each notes is mapped to a time-reversed sequence of notes
        self.previous_notes={}


    def get_bass_line(self):
        #TODO-Hh{add work-around if no self-titled 'bass line' is present}
        try:
            return self.work['bass']
        except:
            raise InputError("cannot extract bass line from score")

    def get_chord(self,note):
        note_location = note.offset
        chord = self.chords.getElementAtOrBefore(note_location)
        print chord
        return chord

    def note_of_index(self,index):
        return self.bass_notes[index]

    def index_of_note(self,note):
        index = 0
        for bass_note in self.bass_notes:
            if note == bass_note:
                return index
            else:
                index = index + 1
        raise KeyError #TODO-Hh{Check errors!}

    def get_overlapping_notes(self,note):
        # Cache
        try:
            return self.overlapping_notes[note]
        except KeyError:
            overlapping_notes = self.notes.getElementsByOffset(note.offset,
                                    note.offset + note.duration.quarterLength)
            overlapping_notes.remove(note)

            # Cache
            self.overlapping_notes[note] = overlapping_notes

            return overlapping_notes

    def get_simultaneous_notes(self,note):
        # Cache
        try:
            return self.simultaneous_notes[note]
        except KeyError:
            simultaneous_notes = self.notes.getElementsByOffset(note.offset)
            simultaneous_notes.remove(note)

            # Cache
            self.simultaneous_notes[note] = simultaneous_notes

            return simultaneous_notes

    def get_harmonic_intervals(self,note,notes):
        #TODO-HhK{Make sure it's okay that we're using generic intervals}

        # We are using  Music21 Generic interval, which gives a number
        # (e.g. third = 3) w/o quality (m3 = M3 = 3)
        # For other kinds of intervals, see:
        # http://mit.edu/music21/doc/html/moduleInterval.html

        # Compute all harmonic intervals with current note
        harmonic_intervals = [interval.notesToGeneric(note,other_note) for
                                other_note in notes]

        # Convert all intervals to mod7 intervals (e.g. 9th = 2nd)
        harmonic_intervals = [inter.mod7 for inter in harmonic_intervals]

        return harmonic_intervals

    def get_next_notes(self,note,N=1):
        #TODO-Hh{Flawed!!!!!!!! Don't use until fixed!}
        # TODO: is there a more efficient way to implement this?
        # using getElementsByOffset? (and ignoring rests)
        # getting the index in the part and slicing the list?

        # Cache
        try:
            cached_notes =  self.next_notes[note]
            if len(cached_notes)>=N:
                return cached_notes
            else:
                raise
        except:
            # Get the part that this note belongs to
            part = note.parent
            if part is None:
                raise InputError("cannot extract part for note %s" %note)

            # Iterate the notes of the part
            # Push N notes after the current
            next_notes=[]
            insert_notes=False
            for other_note in part:
                if not insert_notes and other_note == note:
                    insert_notes=True
                elif insert_notes:
                    next_notes.append(other_note)
                elif len(next_notes)>= N:
                    # Cache
                    self.next_notes[note]=next_notes
                    return next_notes

    def get_previous_notes(self,note,N=1):
        #TODO-Hh{Flawed!!!!!!!! Don't use until fixed!}
        # TODO: is there a more efficient way to implement this?
        # using getElementsByOffset? (and ignoring rests)
        # getting the index in the part and slicing the list?

        # Cache
        try:
            cached_notes =  self.previous_notes[note]
            if len(cached_notes)>=N:
                return cached_notes
            else:
                raise
        except:
            # Get the part that this note belongs to
            part = note.parent
            if part is None:
                raise InputError("cannot extract part for note %s" %note)


            # Iterate the notes of the part
            # Continously store N notes
            # Return when current note is found
            previous_notes=[]
            for other_note in part:
                if other_note == note:
                    # Cache
                    self.previous_notes[note]=previous_notes
                    return previous_notes
                else:
                    previous_notes.insert(0,other_note)
                    if len(previous_notes) > N:
                        previous_notes.pop()

    def get_next_bass_note(self,note,N=1):
        index = self.index_of_note(note)
        try:
            return self.bass_notes[index+N]
        except:
            raise IndexError