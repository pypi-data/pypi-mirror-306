# MIDI notes use a value between 0-127
def tuning_to_midi_note_mapping(tuning):
    note = tuning[0:-1]
    octave = int(tuning[-1])

    note_number = note_to_midi_number_mapping(note)

    # 12 is C0 for my soundfont (octave is 0, C == 0), so when its C2 ==> ((2*12) + 12) + 0 = 24 + 12 = 36
    # Note: different soundfonts may have a different number for C0 (I provided my soundfont, which can be found in the readme)
    octave_number = (octave * 12) + 12

    # This addition is similar to taking the frequency of the open string, and increasing it to the fret/note being played
    strings_midi_tuning = octave_number + note_number

    return strings_midi_tuning


# Returns a number from 0-11, where 0 == C, 1 == C#/Db, ..., 11 == B
def note_to_midi_number_mapping(note):
    if note == "C":
        return 0
    elif note == "C#" or note == "Db":
        return 1
    elif note == "D":
        return 2
    elif note == "D#" or note == "Eb":
        return 3
    elif note == "E":
        return 4
    elif note == "F":
        return 5
    elif note == "F#" or note == "Gb":
        return 6
    elif note == "G":
        return 7
    elif note == "G#" or note == "Ab":
        return 8
    elif note == "A":
        return 9
    elif note == "A#" or note == "Bb":
        return 10
    elif note == "B":
        return 11