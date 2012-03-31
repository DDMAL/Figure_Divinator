# Rules for figuring unfigured bass parts
# Monsieur de Saint-Lambert
# Konstantin Bozhinov transcription - Version 1 (January 2011)

#TODO-Hh{"no figure" the same as "major - so no figure"? If not, check all
# rules that say "no figure"!}
#TODO-Hh{Figure out how "no figure" is different from not having added anything
# yet -- how to prioritize no figure? save it as something different
# temporarily? After all, "no figure" is different from "no figure signifying
# major" is different from "no figure has been added yet"....}

#TODO-HhK{"tone" == 2 semitones? 1 scale note?}
#TODO-Hh{Depending on answer above,
#        double-check "up a tone" v "up a semitone" everywhere!!!!}

from rules import *
from music21 import interval
import random

import logging_setup as Logging
LOG=Logging.getLogger('rules')

class SLRule(Rule):
    def __init__(self):
        Rule.__init__(self)

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


class SLRule1(SLRule):
    # Status: limbo! #TODO-HhK{Konstantin clarification needed: switching}

    # Rule 1:
    # When the bass note goes up by a semitone
    # * First note gets a 6, second nothing.
    # * Or, first gets nothing, second gets 6.
    def apply(self,context):
        current_note = context.note

        try:
            # check if if (bass note down by a semitone)
            next_note = context.work_browser.get_next_bass_note(current_note)
            melodic_interval = interval.notesToChromatic(
                                current_note,next_note).semitones

            if melodic_interval == -1:
                LOG.debug("YOU PASS RULE 1! Cool.")
                self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)
                #TODO-HhK{Which rule to follow?}
                outcome = random.randint(0,1)
                if outcome == 0:
                    # * First note gets a 6, second nothing. #TODO-HhK{Does
                    #"nothing" mean don't add anything new, or eliminate any
                    #figure already there?}
                    self.addition = IntervalAddition(current_note,6)
                else:
                    # * Or, first gets nothing, second gets 6.
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
    # Status: complete!

    # Rule 3:
    # When bass note goes up by a semitone
    # and the first note has a #6
    # * Second note gets a 6
    def apply(self,context):
        current_note = context.note
        fig_has_6 =  context.figured_bass.has_interval(current_note,6)

        try:
            # check if if (bass note down by a semitone)
            next_note = context.work_browser.get_next_bass_note(current_note)
            melodic_interval = interval.notesToChromatic(
                                current_note,next_note).semitones
            if (melodic_interval == 1 and fig_has_6 == 1):
                 # * Second note gets a 6
                LOG.debug("YOU PASS RULE 3!")
                self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)
                self.addition = IntervalAddition(next_note,6)

        except IndexError:
            LOG.info("last note!")

        except AttributeError:
            LOG.warning("error on: %s", current_note)


class SLRule4(SLRule):
    # Status: complete!

    # Rule 4:
    # When bass note goes down by a minor 3rd
    # * If first chord is perfect, second gets false fifth (no figure)

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
    # Status: complete!

    # Rule 5:
    # When bass note goes down by a major 3rd
    # * If first note is perfect and major, second gets a 6

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

    def apply(self,context):
        pass


class SLRule7(SLRule):
    # Status: complete!

    # Rule 7:
    # When bass note goes up by a 3rd or 6th (of any kind)
    # * Second note gets a 6

    def apply(self,context):
        current_note = context.note

        try:
            next_note = context.work_browser.get_next_bass_note(current_note)
            melodic_interval = interval.notesToChromatic(
                                current_note,next_note).semitones

            #TODO-HhK{Was "of any kind" interpreted correctly? (didn't include
            # diminished 6th...is that also correct?)}
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
    # Status: complete!

    # Rule 8:
    # When bass note goes up 3 consecutive tones
    # * 1st note gets a 6
    # * 2nd note gets a 65
    # * 3rd note gets a major chord (no figure)

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
    # Status: complete!

    # Rule 9:
    # When bass note goes down 3 consecutive tones and if first chord is major
    # * 2nd gets '-'
    # * 3rd gets a 6

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
    # Status: complete!

    # Rule 10:
    # When bass note goes down 3 consecutive tones and the third note has a 7
    # * 1st gets no figure
    # * Second gets '-'

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
            #TODO-HhK{I'm not sure how to interpret this: how many bass notes
            # are being dealt with here, and are we talking chromatically
            # consecutive or scale consecutive or what?}
            #TODO-HhK{"third note has a 7" means it already has that figure or
            # there's a 7 in the chord?}
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
    # Status: complete!

    # Rule 11:
    # When bass note goes down by a major/minor 3rd,
    # then goes up a tone and third chord is major and is on first beat
    # * 2nd gets a 6

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
    # Status: complete!

    # Rule 12:
    # When bass note goes down a minor 3rd, then goes up a semitone
    # * 1st gets perfect major chord (no figure)
    # * 2nd gets a 6
    # * 3rd gets perfect major chord (no figure)

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
    # Status: complete!

    # Rule 13:
    # When bass note goes up a semitone,
    # then goes up a 5th or down a 4th and is on 1st beat
    # * 1st gets 6 b5
    # * 2nd no figure
    # * 3rd no figure

    def apply(self,context):
        current_note = context.note
        current_note_beat = current_note.beat

        try:
            next_note = context.work_browser.get_next_bass_note(current_note)
            third_note = context.work_browser.get_next_bass_note(next_note)
            melodic_interval = interval.notesToChromatic(
                                current_note,next_note).semitones
            melodic_interval_2 = interval.notesToChromatic(
                                next_note,third_note).semitones

            # When bass note goes up a semitone,
            # then goes up a 5th or down a 4th and is on 1st beat
            #TODO-HhK{Clarification: *current* note is on the 1st beat, right?}
            if (melodic_interval == 1 and current_note_beat == 1 and
                    (melodic_interval_2 == 7 or melodic_interval_2 == -5)):
                LOG.debug("You PASS RULE 13!")
                self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)

                # * 1st gets 6 b5
                #TODO-Hh{When using fb module, this might be different}
                self.addition = MultipleIntervalAddition(context.note,['6','b5'])

                # * 2nd no figure
                context.figured_bass.clear_figure(next_note)

                # * 3rd no figure
                context.figured_bass.clear_figure(third_note)

        except IndexError:
            LOG.info("last note!")

        except AttributeError:
            LOG.warning("error on: %s", current_note)

class SLRule14(SLRule):
    # Status: complete!

    # Rule 14:
    # When bass note goes down a major 3rd, then goes up a 4th
    # * 2nd note gets a 7
    # * 3rd note gets perfect chord (no figure)

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
    # Status: complete!

    # Rule 15:
    # When bass remains same for two notes and then goes up a 5th
    # and the 3rd note is on 1st beat
    # * 1st note gets no figure
    # * 2nd note gets a 6
    # * 3rd note gets no figure

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
    # Status: complete!

    # Rule 16:
    # When bass note remains same for two notes and then the 3rd goes down a
    # 4th and is on the 1st beat
    # * 1st gets no figure
    # * 2nd gets a 6 #4
    # * 3rd gets no figure

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
                #TODO-Hh{When using fb module, this might be different}
                self.addition = MultipleIntervalAddition(context.note,['#4','6'])

                # * 3rd gets no figure #TODO-Hh{"no figure"...}
                context.figured_bass.clear_figure(third_note)

        except IndexError:
            LOG.info("last note!")

        except AttributeError:
            LOG.warning("error on: %s", current_note)

class SLRule17(SLRule):
    # Status: complete!

    # Rule 17:
    # When bass note goes up a tone, then up a tone,
    # then up a semitone (sol la si ut) and last note is on 1st beat
    # * 1st note gets no figure
    # * 2nd note gets a 6
    # * 3rd note gets no figure (diminished chord)
    # * 4th note gets no figure

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
    # Status: complete!

    # Rule 19:
    # When bass note goes down a tone, then down a semitone, then down a tone
    # * 1st note gets no figure
    # * 2nd note get a '-'
    # * 3rd note gets a #6
    # * 4th note gets no figure

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
    # Status: complete!

    # Rule 20:
    # When bass note goes down a tone, then down a tone, then down a semitone
    # * 1st note gets no figure
    # * 2nd note gets no figure
    # * 3rd note gets a 6
    # * 4th note gets no figure

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
    # Status: limbo! #TODO-HhK{Konstantin clarification needed: switching}

    # Rule 21:
    # When bass note goes down a tone, then down a semitone, then down a tone,
    # then down a tone
    # * 1st note gets no figure
    # * 2nd note gets a 6#42 or just '-'
    # * 3rd gets a 6
    # * 4th gets a 6
    # * 5th gets no figure

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

                # * 2nd note gets a 6#42 or just '-'
                #TODO-HhK{Which rule to follow?? How to decide}
                outcome = random.randint(0,1)
                if outcome == 0:
                    # * 2nd note gets a 6#42
                    #TODO-HhK{"6#42"?? Really? Or miss-print?}
                    #TODO-Hh{When using fb module, this might be different}
                    self.addition = MultipleIntervalAddition(next_note,['#42','6'])

                else:
                    # * 2nd note gets a '-'
                    self.addition = IntervalAddition(next_note,'-')


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
    # Status: complete!

    # Rule 22:
    # When bass note goes down a tone, then down a tone, then down a semitone,
    # then down a tone
    # * 1st note gets no figure
    # * 2nd note gets a '-'
    # * 3rd note gets a 6
    # * 4th note gets a 6
    # * 5th note gets no figure

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
    # Status: complete!

    # Rule 23:
    # When bass note goes up a tone, then up a tone, then up a semitone,
    # then up a tone
    # * 1st note gets no figure
    # * 2nd note gets a 6
    # * 3rd note gets a 6
    # * 4th note gets a 65
    # * 5th note gets no figure

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
                self.addition = IntervalAddition(fourth_note,65)

                # * 5th gets no figure #TODO-Hh{"no figure"...}
                context.figured_bass.clear_figure(fifth_note)

        except IndexError:
            LOG.info("last note!")

        except AttributeError:
            LOG.warning("error on: %s", current_note)

class SLRule24(SLRule):
    # Status: complete!

    # Rule 24:
    # When bass note goes up a tone, then up a semitone,
    # then up a tone, then up a tone
    # * 1st note gets no figure
    # * 2nd note gets a #6
    # * 3rd note gets a 6
    # * 4th note gets a 65
    # * 5th note gets no figure

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
                #TODO-HhK{"65"?? Really? Or miss-print?}
                self.addition = IntervalAddition(fourth_note,65)

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

    def apply(self,context):
        pass


class SLRule26(SLRule):
    # Status: limbo! #TODO-HhK{Konstantin clarification needed: candence???}

    # Rule 26:
    # cadence - short sol ut
    # Short sol gets 7 (no 4) and ut gets no figure

    def apply(self,context):
        pass


class SLRule27(SLRule):
    # Status: limbo! #TODO-HhK{Konstantin clarification needed: candence???}

    # Rule 27:
    # When at a cadence - long sol ut
    # * Long sol gets 4 and 7 and ut gets no figure

    def apply(self,context):
        pass


class SLRule28(SLRule):
    # Status: limbo! #TODO-HhK{Konstantin clarification needed: candence???}

    # Rule 28:
    # When at a cadence and sol is 3 beats in 3/4 time
    # * Sol gets 4, no figure, then a 7 (respectively on each beat)

    def apply(self,context):
        pass


class SLRuleOthers(SLRule):
    # SL rules yet to be implemented
    # TODO-HhK{Are there any others? Have there been any updates?}

    def apply(self,context):
        pass
