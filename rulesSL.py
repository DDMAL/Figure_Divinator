# Rules for figuring unfigured bass parts
# Monsieur de Saint-Lambert
# Konstantin Bozhinov transcription - Version 1 (January 2011)

#TODO-HhK{"tone" == 2 semitones? 1 scale note?}
#TODO-Hh{Make sure all intervals are MODULO!!!!!!!}
#TODO-Hh{Depending on answer above, double-check "up a tone" v "up a semitone" everywhere!!!!}

from rules import *
from music21 import interval
import random

import logging_setup as Logging
LOG=Logging.getLogger('rules')

class SLRule(Rule):
    def __init__(self):
        Rule.__init__(self)
        self.umbrella = "Saint Lambert"

        # Can be redefined in sub-classes
        self.applicability_multiplier = 1.0

        # Set applicability as 0 - will get overwritten if applicable
        self.applicability = MIN_APPLICABILITY


class SLRule_test(SLRule):
    def apply(self,context):
        current_note = context.note

        self.applicability_multiplier = .3
        thisrand = random.randint(1,9)
        if thisrand > 4:
            self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)
            self.addition = IntervalAddition(current_note,65)


class SLRuleImplicit_1(SLRule):
    # Implicit rule 1:
    # If a note has a #6, label it.

    def __init__(self):
        SLRule.__init__(self)
        self.range = "1"
        self.details = "semi->#6"
        self.todo = "-"

    def apply(self,context):
        current_note = context.note

        try:
            # check if (first note has #6)
            fig_has_6 = 0
            current_pitches = context.work_browser.get_chord_notes(current_note)
            for j in range(len(current_pitches)-1, -1, -1):
                p = current_pitches[j]
                i = interval.notesToChromatic(current_note,p).semitones
                if i%12 == 9:
                    fig_has_6 = 1
                LOG.debug("note is: %s, interval is: %d", p, i%12)

            if (fig_has_6 == 1):
                LOG.debug("YOU PASS INCIDENTAL RULE 1!")
                self.applicability = (self.applicability_multiplier *
                                      MAX_APPLICABILITY)
                self.addition = IntervalAddition(current_note,'#6')

        except IndexError:
            print "last note!"

        except AttributeError:
            print "error on: ", current_note


class SLRule1a(SLRule):
    # Status: limbo! #TODO-HhK{Konstantin clarification needed: switching}

    # Rule 1a:
    # When the bass note goes up by a semitone
    # * First note gets a 6, second nothing. #TODO-HhK{"nothing"=="clear what is there"=="35"}
    # * ...

    def __init__(self):
        SLRule.__init__(self)
        self.range = "2, both (maybe just first)"
        self.details = "-"
        self.todo = "clarify switch; clarify 'nothing';"

    def apply(self,context):
        current_note = context.note

        try:
            # check if if (bass note up by a semitone)
            next_note = context.work_browser.get_next_bass_note(current_note)
            melodic_interval = interval.notesToChromatic(
                                current_note,next_note).semitones

            if melodic_interval == 1:
                LOG.debug("YOU PASS RULE 1a! Cool.")
                self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)
                #TODO-HhK{Which rule to follow?}

                # * First note gets a 6
                self.addition = IntervalAddition(current_note,6)

                # *...second nothing. #TODO-HhK{Does
                #"nothing" mean don't add anything new, or eliminate any
                #figure already there?}

        except IndexError:
          print "last note!"

        except AttributeError:
          print "error on: ", current_note


class SLRule1b(SLRule):
    # Status: limbo! #TODO-HhK{Konstantin clarification needed: switching}

    # Rule 1b:
    # When the bass note goes up by a semitone
    # ... 
    # second gets 6.

    def __init__(self):
        SLRule.__init__(self)
        self.range = "2, both (maybe just second)"
        self.details = "-"
        self.todo = "clarify switch; clarify 'nothing';"

    def apply(self,context):
        current_note = context.note

        try:
            # check if if (bass note up by a semitone)
            next_note = context.work_browser.get_next_bass_note(current_note)
            melodic_interval = interval.notesToChromatic(
                                current_note,next_note).semitones

            if melodic_interval == 1:
                LOG.debug("YOU PASS RULE 1b! Cool.")
                self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)
                # * Or, first gets nothing, ##TODO-HhK{Does
                #"nothing" mean don't add anything new, or eliminate any
                #figure already there?}

                # * ...second gets 6.
                self.addition = IntervalAddition(next_note,6)

        except IndexError:
            LOG.info("last note!")

        except AttributeError:
            LOG.warning("error on: %s", current_note)


class SLRule2(SLRule):
    # Status: complete!

    # Rule 2:
    # If (bass note down by a semitone) and (second note is on beat 1)
    # and (second note is a perfect chord):
    # * First note gets a 6

    def __init__(self):
        SLRule.__init__(self)
        self.range = "2, first"
        self.details = "chordqual->perfect,beat"
        self.todo = "chord quality;"

    def apply(self,context):
        current_note = context.note

        try:
            next_note = context.work_browser.get_next_bass_note(current_note)
            melodic_interval = interval.notesToChromatic(
                                current_note,next_note).semitones
            next_note_beat = next_note.beat
            next_note_chord = context.work_browser.get_chord(next_note)

            # check: (bass note down by a semitone) and (second note is on
            # beat 1) and (second note is a perfect chord):
            #TODO-HhK{Konstantin clarification needed: "perfect chord is M?"}
            if (melodic_interval == -1 and next_note_beat == 1 and
                next_note_chord.isMajorTriad()):

                # * First note gets a 6
                LOG.debug("YOU PASS RULE 2!")
                self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)
                self.addition = IntervalAddition(context.note,6)

        except IndexError:
            LOG.info("last note!")

        except AttributeError:
            LOG.warning("error on: %s", current_note)


class SLRule3(SLRule):
    # Rule 3:
    # When bass note goes up by a semitone
    # and the first note has a #6
    # * Second note gets a 6

    def __init__(self):
        SLRule.__init__(self)
        self.range = "2, second"
        self.details = "semi->#6"
        self.todo = "-"  

    def apply(self,context):
        current_note = context.note

        try:
            LOG.debug("Trying rule 3 again, on note %s", current_note)
            # check if (bass note down by a semitone)
            next_note = context.work_browser.get_next_bass_note(current_note)
            melodic_interval = interval.notesToChromatic(
                                current_note,next_note).semitones

            LOG.debug("Interval is: %d", melodic_interval)

            # check if (first note has #6)
            fig_has_6 = 0
            current_pitches = context.work_browser.get_chord_notes(current_note)
            for j in range(len(current_pitches)-1, -1, -1):
                p = current_pitches[j]
                i = interval.notesToChromatic(current_note,p).semitones
                if i%12 == 9:
                    fig_has_6 = 1
                LOG.debug("note is: %s, interval is: %d", p, i%12)

            if (melodic_interval == 1 and fig_has_6 == 1):
                 # * Second note gets a 6
                LOG.debug("YOU PASS RULE 3!")
                self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)
                self.addition = IntervalAddition(next_note,6)

            else:
                LOG.debug("You don't pass rule3.")

        except IndexError:
            LOG.info("last note!")

        except AttributeError:
            LOG.warning("error on: %s", current_note)


class SLRule4(SLRule):
    # Rule 4:
    # When bass note goes down by a minor 3rd
    # * If first chord is perfect, second gets false fifth (no figure)

    def __init__(self):
        SLRule.__init__(self)
        self.range = "2"
        self.details = "chordqual->perfect"
        self.todo = "chord quality; false fifth;"

    def apply(self,context):
        current_note = context.note

        try:
            next_note = context.work_browser.get_next_bass_note(current_note)
            melodic_interval = interval.notesToChromatic(
                                current_note,next_note).semitones
            first_chord = context.work_browser.get_chord(current_note)

            # check if (bass note down by a minor 3rd) and (first chord perfect)
            #TODO-HhK{Konstantin clarification needed: "perfect chord is M?"}
            if (melodic_interval == -4 and first_chord.isMajorTriad()):
                LOG.debug("YOU PASS RULE 4!")
                # * Second note gets a false fifth (no figure)
                #TODO-HhK{Konstantin clarification needed: details on what false
                #fifth looks like in all cases}
                self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)

                context.figured_bass.clear_figure(next_note)

        except IndexError:
            LOG.info("last note!")

        except AttributeError:
            LOG.warning("error on: %s", current_note)


class SLRule5(SLRule):
    # Rule 5:
    # When bass note goes down by a major 3rd
    # * If first note is perfect and major, second gets a 6

    def __init__(self):
        SLRule.__init__(self)
        self.range = "2, second"
        self.details = "chordqual->perfect,major"
        self.todo = "chord quality;"

    def apply(self,context):
        current_note = context.note

        try:
            next_note = context.work_browser.get_next_bass_note(current_note)
            melodic_interval = interval.notesToChromatic(
                                current_note,next_note).semitones
            first_chord = context.work_browser.get_chord(current_note)

            # When bass note goes down by a major 3rd and first note is perfect
            # and major
            #TODO-HhK{Clarification: perfect chord is M?}
            #TODO-HhK{Clarification: how is "perfect and major" not redundant?}
            if (melodic_interval == -4 and first_chord.isMajorTriad()):
                # second gets a 6
                LOG.debug("YOU PASS RULE 5!")
                self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)

                self.addition = IntervalAddition(next_note,6)

        except IndexError:
            LOG.info("last note!")

        except AttributeError:
            LOG.warning("error on: %s", current_note)


class SLRule6(SLRule):
    # Status: limbo! #TODO-HhK{Clarification: I don't understand this rule!}

    # Rule 6:
    # When bass note goes down by a false 5th
    # * No figure ( include the b5 in second chord)

    def __init__(self):
        SLRule.__init__(self)
        self.range = "2, first (maybe both)"
        self.details = "-"
        self.todo = "Everything! false 5; clarify notes;"

    def apply(self,context):
        pass


class SLRule7(SLRule):
    # Rule 7:
    # When bass note goes up by a 3rd or 6th (of any kind)
    # * Second note gets a 6

    def __init__(self):
        SLRule.__init__(self)
        self.range = "2, second"
        self.details = "-"
        self.todo = "-"

    def apply(self,context):
        current_note = context.note

        try:
            next_note = context.work_browser.get_next_bass_note(current_note)
            melodic_interval = interval.notesToChromatic(
                                current_note,next_note).semitones

            if (melodic_interval == 3 or melodic_interval == 4 or
                    melodic_interval == 8 or melodic_interval == 9):
                # * Second note gets a 6
                LOG.debug("YOU PASS RULE 7!")
                self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)

                self.addition = IntervalAddition(next_note,6)

        except IndexError:
            LOG.info("last note!")

        except AttributeError:
            LOG.warning("error on: %s", current_note)


class SLRule8(SLRule):
    # Rule 8:
    # When bass note goes up 3 consecutive tones
    # * 1st note gets a 6
    # * 2nd note gets a 65
    # * 3rd note gets a major chord (no figure)

    def __init__(self):
        SLRule.__init__(self)
        self.range = "4 (maybe 3), first 3"
        self.details = "-"
        self.todo = "clarify 3 consec;"

    def apply(self,context):
        current_note = context.note

        try:
            next_note = context.work_browser.get_next_bass_note(current_note)
            third_note = context.work_browser.get_next_bass_note(next_note)
            melodic_interval = interval.notesToChromatic(
                                current_note,next_note).semitones
            melodic_interval_2 = interval.notesToChromatic(
                                next_note,third_note).semitones

            # When bass note goes up 3 consecutive tones
            #TODO-HhK{I'm not sure how to interpret this: how many bass notes
            # are being dealt with here, and are we talking chromatically
            # consecutive or scale consecutive or what?}
            if (melodic_interval == 1 and melodic_interval_2 == 1):
                LOG.debug("YOU PASS RULE 8!")
                self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)
                # * 1st note gets a 6
                self.addition = IntervalAddition(current_note,6)

                # * 2nd note gets a 65
                #TODO-HhK{Clarification: this is a misprint and should be 5,no?}
                self.addition = IntervalAddition(next_note,5)

                # * 3rd note gets a major chord (no figure)
                #TODO-HhK{Again: no figure means...clear figure?}
                context.figured_bass.clear_figure(third_note)

        except IndexError:
            LOG.info("last note!")

        except AttributeError:
            LOG.warning("error on: %s", current_note)


class SLRule9(SLRule):
    # Rule 9:
    # When bass note goes down 3 consecutive tones and if first chord is major
    # * 2nd gets '-'
    # * 3rd gets a 6

    def __init__(self):
        SLRule.__init__(self)
        self.range = "3 (maybe 4), first 3"
        self.details = "chordqual->M"
        self.todo = "clarify 3 consec;"

    def apply(self,context):
        current_note = context.note

        try:
            next_note = context.work_browser.get_next_bass_note(current_note)
            third_note = context.work_browser.get_next_bass_note(next_note)
            melodic_interval = interval.notesToChromatic(
                                current_note,next_note).semitones
            melodic_interval_2 = interval.notesToChromatic(
                                next_note,third_note).semitones
            first_chord = context.work_browser.get_chord(current_note)

            # When bass note goes down 3 consecutive tones and if first chord
            # is major:
            #TODO-HhK{Again: how many bass notes
            # are being dealt with here, and are we talking chromatically
            # consecutive or scale consecutive or what? *I chose to look at 3
            # notes, but it is very possible this means 4 should be used.}
            if (melodic_interval == -1 and melodic_interval_2 == -1 and
                    first_chord.isMajorTriad()):
                LOG.debug("YOU PASS RULE 9!")
                self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)
                # * 2nd gets '-'
                #TODO-Hh{When using fb module, this might be different}
                #TODO-Hh{Might need to order this better, somehow}
                self.addition = IntervalAddition(next_note,'-')

                # * 3rd gets a 6
                self.addition = IntervalAddition(third_note,6)

        except IndexError:
            LOG.info("last note!")

        except AttributeError:
            LOG.warning("error on: %s", current_note)


class SLRule10(SLRule):
    # Rule 10:
    # When bass note goes down 3 consecutive tones and the third note has a 7
    # * 1st gets no figure
    # * Second gets '-'

    def __init__(self):
        SLRule.__init__(self)
        self.range = "4 (maybe 3), first 2"
        self.details = "semi->7"
        self.todo = "clarify 3 consec;"

    def apply(self,context):
        current_note = context.note

        try:
            next_note = context.work_browser.get_next_bass_note(current_note)
            third_note = context.work_browser.get_next_bass_note(next_note)
            melodic_interval = interval.notesToChromatic(
                                current_note,next_note).semitones
            melodic_interval_2 = interval.notesToChromatic(
                                next_note,third_note).semitones
            third_note_chord = context.work_browser.get_chord(third_note)

            # When bass note goes down 3 consecutive tones
            # and the third note has a 7
            if (melodic_interval == -1 and melodic_interval_2 == -1 and
                    third_note_chord.containsSeventh()):

                LOG.debug("YOU PASS RULE 10!")
                self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)

                 # * 1st gets no figure #TODO-Hh{"no figure"...}
                context.figured_bass.clear_figure(current_note)

                # * Second gets '-'
                #TODO-Hh{When using fb module, this might be different}
                self.addition = IntervalAddition(next_note,'-')

        except IndexError:
            LOG.info("last note!")

        except AttributeError:
            LOG.warning("error on: %s", current_note)


class SLRule11(SLRule):
    # Rule 11:
    # When bass note goes down by a major/minor 3rd,
    # then goes up a tone and third chord is major and is on first beat
    # * 2nd gets a 6

    def __init__(self):
        SLRule.__init__(self)
        self.range = "3, second"
        self.details = "chordqual->M,beat"
        self.todo = "-"

    def apply(self,context):
        current_note = context.note

        try:
            next_note = context.work_browser.get_next_bass_note(current_note)
            third_note = context.work_browser.get_next_bass_note(next_note)
            melodic_interval = interval.notesToChromatic(
                                current_note,next_note).semitones
            melodic_interval_2 = interval.notesToChromatic(
                                next_note,third_note).semitones
            third_chord = context.work_browser.get_chord(current_note)
            third_note_beat = third_note.beat

            # When bass note goes down by a major/minor 3rd,
            # then goes up a tone and third chord is major and is on first beat
            #TODO-HhK{"up a tone" means two semitones or up a scale tone?}
            if ((melodic_interval == -3 or melodic_interval == -4) and
                    melodic_interval_2 == 2 and third_chord.isMajorTriad() and
                    third_note_beat == 1):
                LOG.debug("YOU PASS RULE 11!")
                self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)
                # * 2nd gets a 6
                self.addition = IntervalAddition(next_note,6)

        except IndexError:
            LOG.info("last note!")

        except AttributeError:
            LOG.warning("error on: %s", current_note)


class SLRule12(SLRule):
    # Rule 12:
    # When bass note goes down a minor 3rd, then goes up a semitone
    # * 1st gets perfect major chord (no figure)
    # * 2nd gets a 6
    # * 3rd gets perfect major chord (no figure)

    def __init__(self):
        SLRule.__init__(self)
        self.range = "3, all three"
        self.details = "-"
        self.todo = "-"

    def apply(self,context):
        current_note = context.note

        try:
            next_note = context.work_browser.get_next_bass_note(current_note)
            third_note = context.work_browser.get_next_bass_note(next_note)
            melodic_interval = interval.notesToChromatic(
                                current_note,next_note).semitones
            melodic_interval_2 = interval.notesToChromatic(
                                next_note,third_note).semitones


            # When bass note goes down a minor 3rd, then goes up a semitone
            if (melodic_interval == -3 and melodic_interval_2 == 1):
                LOG.debug("You PASS RULE 12!")
                self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)

                # * 1st gets perfect major chord (no figure)
                context.figured_bass.clear_figure(current_note)

                # * 2nd gets a 6
                self.addition = IntervalAddition(next_note,6)

                # * 3rd gets perfect major chord (no figure)
                context.figured_bass.clear_figure(third_note)


        except IndexError:
            LOG.info("last note!")

        except AttributeError:
            LOG.warning("error on: %s", current_note)


class SLRule13(SLRule):
    # Rule 13:
    # When bass note goes up a semitone,
    # then goes up a 5th or down a 4th and is on 1st beat
    # * 1st gets 6 b5
    # * 2nd no figure
    # * 3rd no figure

    def __init__(self):
        SLRule.__init__(self)
        self.range = "3, all three"
        self.details = "beat"
        self.todo = "-"

    def apply(self,context):
        try:
            current_note = context.note
            current_note_beat = current_note.beat

            next_note = context.work_browser.get_next_bass_note(current_note)
            third_note = context.work_browser.get_next_bass_note(next_note)
            melodic_interval = interval.notesToChromatic(
                                current_note,next_note).semitones
            melodic_interval_2 = interval.notesToChromatic(
                                next_note,third_note).semitones

            # When bass note goes up a semitone,
            # then goes up a 5th or down a 4th and is on 1st beat
            #TODO-HhK{Clarification: *current* note is on the 1st beat, right?}{last but context}
            if (melodic_interval == 1 and current_note_beat == 1 and
                    (melodic_interval_2 == 7 or melodic_interval_2 == -5)):
                LOG.debug("You PASS RULE 13!")
                self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)

                # * 1st gets 6 b5
                self.addition = MultipleIntervalAddition(context.note,['b5','b5'])

                # * 2nd no figure
                context.figured_bass.clear_figure(next_note)

                # * 3rd no figure
                context.figured_bass.clear_figure(third_note)

        except IndexError:
            LOG.info("last note!")

        except AttributeError:
            LOG.warning("error on: %s", current_note)

        except Exception as inst:
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args


class SLRule14(SLRule):
    # Rule 14:
    # When bass note goes down a major 3rd, then goes up a 4th
    # * 2nd note gets a 7
    # * 3rd note gets perfect chord (no figure)

    def __init__(self):
        SLRule.__init__(self)
        self.range = "3, first two"
        self.details = "-"
        self.todo = "-"

    def apply(self,context):
        current_note = context.note

        try:
            next_note = context.work_browser.get_next_bass_note(current_note)
            third_note = context.work_browser.get_next_bass_note(next_note)
            melodic_interval = interval.notesToChromatic(
                                current_note,next_note).semitones
            melodic_interval_2 = interval.notesToChromatic(
                                next_note,third_note).semitones

            # When bass note goes down a major 3rd, then goes up a 4th
            if (melodic_interval == -4 and melodic_interval_2 == 5):
                LOG.debug("You PASS RULE 14!")
                self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)

                # * 2nd note gets a 7
                self.addition = IntervalAddition(next_note,7)

                # * 3rd note gets perfect chord (no figure)
                #TODO-Hh{"no figure"...}
                context.figured_bass.clear_figure(third_note)

        except IndexError:
            LOG.info("last note!")

        except AttributeError:
            LOG.warning("error on: %s", current_note)


class SLRule15(SLRule):
    # Rule 15:
    # When bass remains same for two notes and then goes up a 5th
    # and the 3rd note is on 1st beat
    # * 1st note gets no figure
    # * 2nd note gets a 6
    # * 3rd note gets no figure

    def __init__(self):
        SLRule.__init__(self)
        self.range = "3"
        self.details = "beat"
        self.todo = "-"

    def apply(self,context):
        current_note = context.note

        try:
            next_note = context.work_browser.get_next_bass_note(current_note)
            third_note = context.work_browser.get_next_bass_note(next_note)
            melodic_interval = interval.notesToChromatic(
                                current_note,next_note).semitones
            melodic_interval_2 = interval.notesToChromatic(
                                next_note,third_note).semitones
            third_note_beat = third_note.beat

            # When bass remains same for two notes and then goes up a 5th
            # and the 3rd note is on 1st beat
            if (melodic_interval == 0 and melodic_interval_2 == 7 and
                    third_note_beat == 1):
                LOG.debug("You PASS RULE 15!")
                self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)
                # * 1st note gets no figure #TODO-Hh{"no figure"...}
                context.figured_bass.clear_figure(current_note)

                # * 2nd note gets a 6
                self.addition = IntervalAddition(next_note,6)

                # * 3rd note gets no figure #TODO-Hh{"no figure"...}
                context.figured_bass.clear_figure(third_note)

        except IndexError:
            LOG.info("last note!")

        except AttributeError:
            LOG.warning("error on: %s", current_note)


class SLRule16(SLRule):
    # Rule 16:
    # When bass note remains same for two notes and then the 3rd goes down a
    # 4th and is on the 1st beat
    # * 1st gets no figure
    # * 2nd gets a 6 #4
    # * 3rd gets no figure

    def __init__(self):
        SLRule.__init__(self)
        self.range = "3"
        self.details = "beat"
        self.todo = "-"

    def apply(self,context):
        current_note = context.note

        try:
            next_note = context.work_browser.get_next_bass_note(current_note)
            third_note = context.work_browser.get_next_bass_note(next_note)
            melodic_interval = interval.notesToChromatic(
                                current_note,next_note).semitones
            melodic_interval_2 = interval.notesToChromatic(
                                next_note,third_note).semitones
            third_note_beat = third_note.beat

            # When bass note remains same for two notes and then the 3rd goes
            # down a 4th and is on the 1st beat
            if (melodic_interval == 0 and melodic_interval_2 == -5 and
                    third_note_beat == 1):
                LOG.debug("You PASS RULE 16!")
                self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)

                # * 1st gets no figure #TODO-Hh{"no figure"...}
                context.figured_bass.clear_figure(current_note)

                # * 2nd gets a 6 #4
                self.addition = MultipleIntervalAddition(context.note,['#4','6'])

                # * 3rd gets no figure #TODO-Hh{"no figure"...}
                context.figured_bass.clear_figure(third_note)

        except IndexError:
            LOG.info("last note!")

        except AttributeError:
            LOG.warning("error on: %s", current_note)


class SLRule17(SLRule):
    # Rule 17:
    # When bass note goes up a tone, then up a tone,
    # then up a semitone (sol la si ut) and last note is on 1st beat
    # * 1st note gets no figure
    # * 2nd note gets a 6
    # * 3rd note gets no figure (diminished chord) #TODO-HhK{is "diminished 
    #           chord" a comment or something that needs to be programmed in?}
    # * 4th note gets no figure

    def __init__(self):
        SLRule.__init__(self)
        self.range = "4, all"
        self.details = "beat"
        self.todo = "'diminished' figure(?)"

    def apply(self,context):
        current_note = context.note

        try:
            next_note = context.work_browser.get_next_bass_note(current_note)
            third_note = context.work_browser.get_next_bass_note(next_note)
            melodic_interval = interval.notesToChromatic(
                                current_note,next_note).semitones
            melodic_interval_2 = interval.notesToChromatic(
                                next_note,third_note).semitones
            fourth_note = context.work_browser.get_next_bass_note(third_note)
            melodic_interval_3 = interval.notesToChromatic(
                                third_note,fourth_note).semitones
            fourth_note_beat = fourth_note.beat

            # When bass note goes up a tone, then up a tone,
            # then up a semitone (sol la si ut) and last note is on 1st beat
            if (melodic_interval == 2 and melodic_interval_2 == 2 and
                    melodic_interval_3 == 1 and fourth_note_beat == 1):
                LOG.debug("You PASS RULE 17!")
                self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)

                # * 1st note gets no figure  #TODO-Hh{"no figure"...}
                context.figured_bass.clear_figure(current_note)

                # * 2nd note gets a 6
                self.addition = IntervalAddition(next_note,6)

                # * 3rd note gets no figure (diminished chord)
                #TODO-Hh{"no figure"...}
                #TODO-HhK{how is 'diminished' indicated by no figure?}
                context.figured_bass.clear_figure(third_note)

                # * 4th note gets no figure  #TODO-Hh{"no figure"...}
                context.figured_bass.clear_figure(fourth_note)

        except IndexError:
            LOG.info("last note!")

        except AttributeError:
            LOG.warning("error on: %s", current_note)


class SLRule18(SLRule):
    # Status: complete!

    # Rule 18:
    # When bass note goes down a semitone, then down a tone,
    # then down a tone and the last note is on 1st beat
    # * 1st note gets no figure
    # * 2nd note gets a 6
    # * 3rd note gets #6
    # * 4th note gets no figure

    def __init__(self):
        SLRule.__init__(self)
        self.range = "4, all"
        self.details = "beat"
        self.todo = "-"

    def apply(self,context):
        current_note = context.note

        try:
            next_note = context.work_browser.get_next_bass_note(current_note)
            third_note = context.work_browser.get_next_bass_note(next_note)
            melodic_interval = interval.notesToChromatic(
                                current_note,next_note).semitones
            melodic_interval_2 = interval.notesToChromatic(
                                next_note,third_note).semitones
            fourth_note = context.work_browser.get_next_bass_note(third_note)
            melodic_interval_3 = interval.notesToChromatic(
                                third_note,fourth_note).semitones
            fourth_note_beat = fourth_note.beat

            # When bass note goes down a semitone, then down a tone,
            # then down a tone and the last note is on 1st beat
            if (melodic_interval == -1 and melodic_interval_2 == -2 and
                    melodic_interval_3 == -2 and fourth_note_beat == 1):
                LOG.debug("You PASS RULE 18!")
                self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)

                # * 1st note gets no figure  #TODO-Hh{"no figure"...}
                context.figured_bass.clear_figure(current_note)

                # * 2nd note gets a 6
                self.addition = IntervalAddition(next_note,6)

                # * 3rd note gets #6
                #TODO-Hh{When using fb module, this might be different}
                self.addition = IntervalAddition(third_note,'#6')

                # * 4th note gets no figure  #TODO-Hh{"no figure"...}
                context.figured_bass.clear_figure(fourth_note)

        except IndexError:
            LOG.info("last note!")

        except AttributeError:
            LOG.warning("error on: %s", current_note)


class SLRule19(SLRule):
    # Rule 19:
    # When bass note goes down a tone, then down a semitone, then down a tone
    # * 1st note gets no figure
    # * 2nd note get a '-'
    # * 3rd note gets a #6
    # * 4th note gets no figure

    def __init__(self):
        SLRule.__init__(self)
        self.range = "4, all"
        self.details = "-"
        self.todo = "-"

    def apply(self,context):
        current_note = context.note

        try:
            next_note = context.work_browser.get_next_bass_note(current_note)
            third_note = context.work_browser.get_next_bass_note(next_note)
            melodic_interval = interval.notesToChromatic(
                                current_note,next_note).semitones
            melodic_interval_2 = interval.notesToChromatic(
                                next_note,third_note).semitones
            fourth_note = context.work_browser.get_next_bass_note(third_note)
            melodic_interval_3 = interval.notesToChromatic(
                                third_note,fourth_note).semitones

            # When bass note goes down a tone, then down a semitone,
            # then down a tone
            if (melodic_interval == -2 and melodic_interval_2 == -1 and
                    melodic_interval_3 == -2):
                LOG.debug("You PASS RULE 19!")
                self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)

                # * 1st note gets no figure  #TODO-Hh{"no figure"...}
                context.figured_bass.clear_figure(current_note)

                # * 2nd note gets a '-'
                #TODO-Hh{When using fb module, this might be different}
                self.addition = IntervalAddition(next_note,'-')

                # * 3rd note gets #6
                #TODO-Hh{When using fb module, this might be different}
                self.addition = IntervalAddition(third_note,'#6')

                # * 4th note gets no figure  #TODO-Hh{"no figure"...}
                context.figured_bass.clear_figure(fourth_note)

        except IndexError:
            LOG.info("last note!")

        except AttributeError:
            LOG.warning("error on: %s", current_note)


class SLRule20(SLRule):
    # Rule 20:
    # When bass note goes down a tone, then down a tone, then down a semitone
    # * 1st note gets no figure
    # * 2nd note gets no figure
    # * 3rd note gets a 6
    # * 4th note gets no figure

    def __init__(self):
        SLRule.__init__(self)
        self.range = "4, all"
        self.details = "-"
        self.todo = "-"

    def apply(self,context):
        current_note = context.note

        try:
            next_note = context.work_browser.get_next_bass_note(current_note)
            third_note = context.work_browser.get_next_bass_note(next_note)
            melodic_interval = interval.notesToChromatic(
                                current_note,next_note).semitones
            melodic_interval_2 = interval.notesToChromatic(
                                next_note,third_note).semitones
            fourth_note = context.work_browser.get_next_bass_note(third_note)
            melodic_interval_3 = interval.notesToChromatic(
                                third_note,fourth_note).semitones

            # When bass note goes down a tone, then down a tone,
            # then down a semitone
            if (melodic_interval == -2 and melodic_interval_2 == -2 and
                    melodic_interval_3 == -1):
                LOG.debug("You PASS RULE 20!")
                self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)

                # * 1st note gets no figure #TODO-Hh{"no figure"...}
                context.figured_bass.clear_figure(current_note)

                # * 2nd note gets no figure #TODO-Hh{"no figure"...}
                context.figured_bass.clear_figure(next_note)

                # * 3rd note gets 6
                self.addition = IntervalAddition(third_note,6)

                # * 4th note gets no figure #TODO-Hh{"no figure"...}
                context.figured_bass.clear_figure(fourth_note)

        except IndexError:
            LOG.info("last note!")

        except AttributeError:
            LOG.warning("error on: %s", current_note)


class SLRule21(SLRule):
    # Rule 21:
    # When bass note goes down a tone, then down a semitone, then down a tone,
    # then down a tone
    # * 1st note gets no figure
    # * 2nd note gets a 6#42 or just '-'
    # * 3rd gets a 6
    # * 4th gets a 6
    # * 5th gets no figure

    def __init__(self):
        SLRule.__init__(self)
        self.range = "5, all"
        self.details = "-"
        self.todo = "-"

    def apply(self,context):
        current_note = context.note

        try:
            next_note = context.work_browser.get_next_bass_note(current_note)
            third_note = context.work_browser.get_next_bass_note(next_note)
            melodic_interval = interval.notesToChromatic(
                                current_note,next_note).semitones
            melodic_interval_2 = interval.notesToChromatic(
                                next_note,third_note).semitones
            fourth_note = context.work_browser.get_next_bass_note(third_note)
            melodic_interval_3 = interval.notesToChromatic(
                                third_note,fourth_note).semitones
            fifth_note = context.work_browser.get_next_bass_note(fourth_note)
            melodic_interval_4 = interval.notesToChromatic(
                                fourth_note,fifth_note).semitones

            # When bass note goes down a tone, then down a semitone,
            # then down a tone, then down a tone
            if (melodic_interval == -2 and melodic_interval_2 == -1 and
                    melodic_interval_3 == -2 and melodic_interval_4 == -2):
                LOG.debug("You PASS RULE 21!")
                self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)

                # * 1st note gets no figure #TODO-Hh{"no figure"...}
                context.figured_bass.clear_figure(current_note)

                # * 2nd note gets a 6#42 or just '-' (Note: "-" part of cleanup step)
                #TODO-Hh{When using fb module, this might be different}
                self.addition = MultipleIntervalAddition(next_note,['2','#4','6'])

                # * 3rd gets a 6
                self.addition = IntervalAddition(third_note,6)

                # * 4th gets a 6
                self.addition = IntervalAddition(fourth_note,6)

                # * 5th gets no figure #TODO-Hh{"no figure"...}
                context.figured_bass.clear_figure(fifth_note)

        except IndexError:
            LOG.info("last note!")

        except AttributeError:
            LOG.warning("error on: %s", current_note)


class SLRule22(SLRule):
    # Rule 22:
    # When bass note goes down a tone, then down a tone, then down a semitone,
    # then down a tone
    # * 1st note gets no figure
    # * 2nd note gets a '-'
    # * 3rd note gets a 6
    # * 4th note gets a 6
    # * 5th note gets no figure

    def __init__(self):
        SLRule.__init__(self)
        self.range = "5, all"
        self.details = "-"
        self.todo = "-"

    def apply(self,context):
        current_note = context.note

        try:
            next_note = context.work_browser.get_next_bass_note(current_note)
            third_note = context.work_browser.get_next_bass_note(next_note)
            melodic_interval = interval.notesToChromatic(
                                current_note,next_note).semitones
            melodic_interval_2 = interval.notesToChromatic(
                                next_note,third_note).semitones
            fourth_note = context.work_browser.get_next_bass_note(third_note)
            melodic_interval_3 = interval.notesToChromatic(
                                third_note,fourth_note).semitones
            fifth_note = context.work_browser.get_next_bass_note(fourth_note)
            melodic_interval_4 = interval.notesToChromatic(
                                fourth_note,fifth_note).semitones

            # When bass note goes down a tone, then down a tone,
            # then down a semitone, then down a tone
            if (melodic_interval == -2 and melodic_interval_2 == -2 and
                    melodic_interval_3 == -1 and melodic_interval_4 == -2):
                LOG.debug("You PASS RULE 22!")
                self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)

                # * 1st note gets no figure #TODO-Hh{"no figure"...}
                context.figured_bass.clear_figure(current_note)

                # * 2nd note gets a '-'
                #TODO-Hh{When using fb module, this might be different}
                self.addition = IntervalAddition(next_note,'-')

                # * 3rd note gets a 6
                self.addition = IntervalAddition(third_note,6)

                # * 4th note gets a 6
                self.addition = IntervalAddition(fourth_note,6)

                # * 5th gets no figure #TODO-Hh{"no figure"...}
                context.figured_bass.clear_figure(fifth_note)

        except IndexError:
            LOG.info("last note!")

        except AttributeError:
            LOG.warning("error on: %s", current_note)


class SLRule23(SLRule):
    # Rule 23:
    # When bass note goes up a tone, then up a tone, then up a semitone,
    # then up a tone
    # * 1st note gets no figure
    # * 2nd note gets a 6
    # * 3rd note gets a 6
    # * 4th note gets a 65
    # * 5th note gets no figure

    def __init__(self):
        SLRule.__init__(self)
        self.range = "5, all"
        self.details = "-"
        self.todo = "-"

    def apply(self,context):
        current_note = context.note

        try:
            next_note = context.work_browser.get_next_bass_note(current_note)
            third_note = context.work_browser.get_next_bass_note(next_note)
            melodic_interval = interval.notesToChromatic(
                                current_note,next_note).semitones
            melodic_interval_2 = interval.notesToChromatic(
                                next_note,third_note).semitones
            fourth_note = context.work_browser.get_next_bass_note(third_note)
            melodic_interval_3 = interval.notesToChromatic(
                                third_note,fourth_note).semitones
            fifth_note = context.work_browser.get_next_bass_note(fourth_note)
            melodic_interval_4 = interval.notesToChromatic(
                                fourth_note,fifth_note).semitones

            # When bass note goes up a tone, then up a tone, then up a semitone,
            # then up a tone
            if (melodic_interval == 2 and melodic_interval_2 == 2 and
                    melodic_interval_3 == 1 and melodic_interval_4 == 2):
                LOG.debug("You PASS RULE 23!")
                self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)

                # * 1st note gets no figure #TODO-Hh{"no figure"...}
                context.figured_bass.clear_figure(current_note)

                # * 2nd note gets a 6
                self.addition = IntervalAddition(next_note,6)

                # * 3rd note gets a 6
                self.addition = IntervalAddition(third_note,6)

                # * 4th note gets a 65
                #TODO-HhK{"65"?? Really? Or miss-print?}
                self.addition = MultipleIntervalAddition(fourth_note,['5','6'])

                # * 5th gets no figure #TODO-Hh{"no figure"...}
                context.figured_bass.clear_figure(fifth_note)

        except IndexError:
            LOG.info("last note!")

        except AttributeError:
            LOG.warning("error on: %s", current_note)


class SLRule24(SLRule):
    # Rule 24:
    # When bass note goes up a tone, then up a semitone,
    # then up a tone, then up a tone
    # * 1st note gets no figure
    # * 2nd note gets a #6
    # * 3rd note gets a 6
    # * 4th note gets a 65
    # * 5th note gets no figure

    def __init__(self):
        SLRule.__init__(self)
        self.range = "5, all"
        self.details = "-"
        self.todo = "-"

    def apply(self,context):
        current_note = context.note

        try:
            next_note = context.work_browser.get_next_bass_note(current_note)
            third_note = context.work_browser.get_next_bass_note(next_note)
            melodic_interval = interval.notesToChromatic(
                                current_note,next_note).semitones
            melodic_interval_2 = interval.notesToChromatic(
                                next_note,third_note).semitones
            fourth_note = context.work_browser.get_next_bass_note(third_note)
            melodic_interval_3 = interval.notesToChromatic(
                                third_note,fourth_note).semitones
            fifth_note = context.work_browser.get_next_bass_note(fourth_note)
            melodic_interval_4 = interval.notesToChromatic(
                                fourth_note,fifth_note).semitones

            # When bass note goes up a tone, then up a semitone,
            # then up a tone, then up a tone
            if (melodic_interval == 2 and melodic_interval_2 == 1 and
                    melodic_interval_3 == 2 and melodic_interval_4 == 2):
                LOG.debug("You PASS RULE 24!")
                self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)

                # * 1st note gets no figure #TODO-Hh{"no figure"...}
                context.figured_bass.clear_figure(current_note)

                # * 2nd note gets a #6
                #TODO-Hh{When using fb module, this might be different}
                self.addition = IntervalAddition(next_note,'#6')

                # * 3rd note gets a 6
                self.addition = IntervalAddition(third_note,6)

                # * 4th note gets a 65
                self.addition = MultipleIntervalAddition(fourth_note,['6','5'])

                # * 5th gets no figure #TODO-Hh{"no figure"...}
                context.figured_bass.clear_figure(fifth_note)

        except IndexError:
            LOG.info("last note!")

        except AttributeError:
            LOG.warning("error on: %s", current_note)


class SLRule25(SLRule):
    # Status: limbo! #TODO-HhK{Konstantin clarification needed: candence???}

    # Rule 25:
    # When at a cadence -
    # -sol sol ut gets 4 7 no figure, respectively

    def __init__(self):
        SLRule.__init__(self)
        self.range = "3, all"
        self.details = "-"
        self.todo = "cadence!;"

    def apply(self,context):
        pass


class SLRule26(SLRule):
    # Status: limbo! #TODO-HhK{Konstantin clarification needed: candence???}

    # Rule 26:
    # cadence - short sol ut
    # Short sol gets 7 (no 4) and ut gets no figure

    def __init__(self):
        SLRule.__init__(self)
        self.range = "2, both"
        self.details = "-"
        self.todo = "cadence!;"

    def apply(self,context):
        pass


class SLRule27(SLRule):
    # Status: limbo! #TODO-HhK{Konstantin clarification needed: candence???}

    # Rule 27:
    # When at a cadence - long sol ut
    # * Long sol gets 4 and 7 and ut gets no figure

    def __init__(self):
        SLRule.__init__(self)
        self.range = "2, both"
        self.details = "-"
        self.todo = "cadence!;"

    def apply(self,context):
        pass


class SLRule28(SLRule):
    # Status: limbo! #TODO-HhK{Konstantin clarification needed: candence???}

    # Rule 28:
    # When at a cadence and sol is 3 beats in 3/4 time
    # * Sol gets 4, no figure, then a 7 (respectively on each beat)

    def __init__(self):
        SLRule.__init__(self)
        self.range = "3, all"
        self.details = "beat"
        self.todo = "cadence!; rhythm?!"

    def apply(self,context):
        pass


class SLRuleOthers(SLRule):
    # SL rules yet to be implemented
    # TODO-HhK{Are there any others? Have there been any updates?}

    def __init__(self):
        SLRule.__init__(self)
        self.range = "to_define"
        self.details = "to_define"

    def apply(self,context):
        pass