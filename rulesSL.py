# Rules for figuring unfigured bass parts
# Monsieur de Saint-Lambert
# Konstantin Bozhinov transcription - Version 1 (January 2011)

#TODO-Hh{*Need to account for multiple figures added by one rule? Make
# sure it's possible if needed!}
from rules import *
from music21 import interval
import random

class SLRule(Rule):
    def __init__(self):
        Rule.__init__(self)

        # Can be redefined in sub-classes
        self.applicability_multiplier = 1.0

        # Set applicability as 0 - will get overwritten if applicable
        self.applicability = MIN_APPLICABILITY


class SLRule_test(SLRule):
    def apply(self,context):
        self.applicability_multiplier = .3
        thisrand = random.randint(1,9)
        if thisrand > 4:
            self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)
            self.addition = IntervalAddition(context.note,thisrand)



class SLRule1(SLRule):
    # Status: limbo! #TODO-HhK{Konstantin clarification needed.}

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
                print "YOU PASS RULE 1! Cool."
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
          print "last note!"

        except AttributeError:
          print "error on: ", current_note


class SLRule2(SLRule):
    # Status: complete!

    # Rule 2:
    # If (bass note down by a semitone) and (second note is on beat 1)
    # and (second note is a perfect chord):
    # * First note gets a 6
    def apply(self,context):
        current_note = context.note

        try:
            # check if if (bass note down by a semitone)
            next_note = context.work_browser.get_next_bass_note(current_note)
            melodic_interval = interval.notesToChromatic(
                                current_note,next_note).semitones

            if not melodic_interval == -1:
                self.applicability = MIN_APPLICABILITY
                self.addition = NullAddition()
                return

            print "Awesome! Melodic interval is %s!" % melodic_interval

            # check if (second note is on beat 1)
            next_note_beat = next_note.beat
            if not next_note_beat == 1:
                self.applicability = MIN_APPLICABILITY
                self.addition = NullAddition()
                return

            print "Awesome! Next note is on beat %s!" % next_note_beat

            # check if (second note is a perfect chord):
            #TODO-HhK{Konstantin clarification needed: "perfect chord is M?"}
            next_note_chord = context.work_browser.get_chord(next_note)
            if not next_note_chord.isMajorTriad():
                self.applicability = MIN_APPLICABILITY
                self.addition = NullAddition()
                return
            print "Awesome! Next note chord is %s!" % next_note_chord


            # * First note gets a 6
            print "YOU PASS! Cool. This note, %s, gets a 6" % current_note
            self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)
            self.addition = IntervalAddition(context.note,6)

        except IndexError:
          print "last note!"

        except AttributeError:
          print "error on: ", current_note



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
            if (melodic_interval == 1 and
                fig_has_6 == 1):
                 # * Second note gets a 6
                print "YOU PASS RULE 3!"
                self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)
                self.addition = IntervalAddition(next_note,6)

        except IndexError:
          print "last note!"

        except AttributeError:
          print "error on: ", current_note


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
                print "YOU PASS RULE 4!"
                # * Second note gets a false fifth (no figure)
                #TODO-HhK{Konstantin clarification needed: details on what false
                #fifth looks like in all cases}
                self.applicability = (self.applicability_multiplier *
                                    MAX_APPLICABILITY)

                context.figured_bass.clear_figure(next_note)

        except IndexError:
          print "last note!"

        except AttributeError:
          print "error on: ", current_note


class SLRuleOthers(SLRule):
    # SL rules yet to be implemented
    # Status: not started

    def get_harmonic_notes(self,context):
        """To be re-defined in sub-classess"""

    def apply(self,context):
        pass
        #print "to implement: SL rules"


        # 5. When bass note goes down by a major 3rd
        # * If first note is perfect and major, second gets a 6

        # 6. When bass note goes down by a false 5th
        # * No figure ( include the b5 in second chord)

        # 7. When bass note goes up by a 3rd or 6th (of any kind)
        # * Second note gets a 6

        # 8. When bass note goes up 3 consecutive tones
        # * 1st note gets a 6
        # * 2nd note gets a 65
        # * 3rd note gets a major chord (no figure)

        # 9. When bass note goes down 3 consecutive tones and if first chord is major
        # * 2nd gets '-'
        # * 3rd gets a 6

        # 10. When bass note goes down 3 consecutive tones and the third note has a 7
        # * 1st gets no figure
        # * Second gets '-'

        # 11. When bass note goes down by a major/minor 3rd, then goes up a tone and third chord is major and is on first beat
        # * 2nd gets a 6

        # 12. When bass note goes down a minor 3rd, then goes up a semitone
        # * 1st gets perfect major chord (no figure)
        # * 2nd gets a 6
        # * 3rd gets perfect major chord (no figure)

        # 13. When bass note goes up a semitone, then goes up a 5th or down a 4th and is on 1st beat
        # * 1st gets 6 b5
        # * 2nd no figure
        # * 3rd no figure

        # 14. When bass note goes down a major 3rd, then goes up a 4th
        # * 2nd note gets a 7
        # * 3rd note gets perfect chord (no figure)

        # 15. When bass remains same for two notes and then goes up a 5th and the 3rd note is on 1st beat
        # * 1st note gets no figure
        # * 2nd note gets a 6
        # * 3rd note gets no figure

        # 16. When bass note remains same for two notes and then the 3rd goes down a 4th and is on the 1st beat
        # * 1st gets no figure
        # * 2nd gets a 6 #4
        # * 3rd gets no figure

        # 17. When bass note goes up a tone, then up a tone, then up a semitone (sol la si ut) and last note is on 1st beat
        # * 1st note gets no figure
        # * 2nd note gets a 6
        # * 3rd note gets no figure (diminished chord)
        # * 4th note gets no figure

        # 18. When bass note goes down a semitone, then down a tone, then down a tone and the last note is on 1st beat
        # * 1st note gets no figure
        # * 2nd note gets a 6
        # * 3rd note gets #6
        # * 4th note gets no figure

        # 19. When bass note goes down a tone, then down a semitone, then down a tone
        # * 1st note gets no figure
        # * 2nd note get a '-'
        # * 3rd note gets a #6
        # * 4th note gets no figure

        # 20. When bass note goes down a tone, then down a tone, then down a semitone
        # * 1st note gets no figure
        # * 2nd note gets no figure
        # * 3rd note gets a 6
        # * 4th note gets no figure

        # 21. When bass note goes down a tone, then down a semitone, then down a tone, then down a tone
        # * 1st note gets no figure
        # * 2nd note gets a 6#42 or just '-'
        # * 3rd gets a 6
        # * 4th gets a 6
        # * 5th gets no figure

        # 22. When bass note goes down a tone, then down a tone, then down a semitone, then down a tone
        # * 1st note gets no figure
        # * 2nd note gets a '-'
        # * 3rd note gets a 6
        # * 4th note gets a 6
        # * 5th note gets no figure

        # 23. When bass note goes up a tone, then up a tone, then up a semitone, then up a tone
        # * 1st note gets no figure
        # * 2nd note gets a 6
        # * 3rd note gets a 6
        # * 4th note gets a 65
        # * 5th note gets no figure

        # 24. When bass note goes up a tone, then up a semitone, then up a tone, then up a tone
        # * 1st note gets no figure
        # * 2nd note gets a #6
        # * 3rd note gets a 6
        # * 4th note gets a 65
        # * 5th note gets no figure

        # 25. When at a cadence -
        # -sol sol ut gets 4 7 no figure, respectively

        # 26. cadence - short sol ut
        # Short sol gets 7 (no 4) and ut gets no figure

        # 27. When at a cadence - long sol ut
        # * Long sol gets 4 and 7 and ut gets no figure

        # 28. When at a cadence and sol is 3 beats in 3/4 time
        # * Sol gets 4, no figure, then a 7 (respectively on each beat)
