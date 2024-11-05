from midiutil import MIDIFile
from midi2audio import FluidSynth


# Takes the notes defined in the tabs file and writes them to a midi file at the specified path
def notes_to_midi(guitar_strings, midi_save_path, tempo):
    # Initialize the MIDI file variables;
    track    = 0    # don't change
    channel  = 0    # don't change
    time     = 0    # In beats (don't change)
    duration = 1    # In beats (don't change)
    tempo    = tempo   # In BPM (user input)
    volume   = 127  # 0-127, as per the MIDI standard (don't change, max volume)

    MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created automatically)
    MyMIDI.addTempo(track, time, tempo)

    # For every string, add their notes to the midi file
    for string in guitar_strings:
        # These three values are used to handle notes that can be played for longer than one beat
        duration_extension = 0
        start_time = None
        previous_pitch = None
        
        # Go through each beat for this string and add the notes as needed
        for i, note in enumerate(string):
            if note == "-": # Rest / doesn't add a note for this beat
                continue
            elif note == "~" and previous_pitch != None: # Extends the previous note played
                duration_extension += duration
            elif note == "|": # TODO: add this functionality
                pass
            else: # If the pitch is a number, then we play it
                # If a note has already been encounter before, we play it with the specified duration
                if previous_pitch != None:
                    MyMIDI.addNote(track, channel, previous_pitch, start_time, duration_extension, volume)
                
                # The below initializes the first note encountered, and resets the note for all future notes
                duration_extension = 1
                start_time = i
                previous_pitch = note
        
        # WHen all the notes have been read, check if there is a final pitch to add to the file
        if previous_pitch != None:
            MyMIDI.addNote(track, channel, previous_pitch, start_time, duration_extension, volume)


    with open(midi_save_path, "wb") as output_file:
        MyMIDI.writeFile(output_file)


# Converts the midi file into a wav file
# If the user specifies, they can hear the audio when they run the code by making play=True
def midi_to_wav(soundfont_path, midi_save_path, wav_save_path, play_midi):
    fs = FluidSynth(soundfont_path)
    fs.midi_to_audio(midi_save_path, wav_save_path)
    if play_midi:
        fs.play_midi(midi_save_path)