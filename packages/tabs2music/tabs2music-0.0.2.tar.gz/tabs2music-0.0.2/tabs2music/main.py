from pathlib import Path
from .midi_and_wav_creation import notes_to_midi, midi_to_wav
from .tabs_parser import read_tabs_file


# tabs_path: a path to the .txt file containing the tabs input. The name of the file is the song name
# audio_save_path: a path to the directory the .midi and .wav files should be saved to
# soundfont_path: a path to the soundfont file
# save_midi (optional): if True, the .midi file will be saved, otherwise it is deleted
# play_midi (optional): if True, the .midi file will be played via the terminal on creation, otherwise nothing is played
# tempo (optional): measured in bpm, and changing the value from the default 120 will change the speed of the song
def run(tabs_path, audio_save_path, soundfont_path, save_midi=False, play_midi=False, tempo=120):
    # This returns the parsed output from the tabs file, and the song name
    notes, song_name = read_tabs_file(tabs_path)

    # The Path object ensures the file paths are handled as needed for any OS
    audio_save_path = Path(audio_save_path)
    audio_file_path = audio_save_path / song_name
    midi_save_path = str(audio_file_path.with_suffix('.midi'))
    wav_save_path = str(audio_file_path.with_suffix('.wav'))

    # The parsed tabs are converted to a MIDI file, and then that is converted to a wav file
    notes_to_midi(notes, midi_save_path, tempo)
    midi_to_wav(soundfont_path, midi_save_path, wav_save_path, play_midi) 

    # The intermediate MIDI file is deleted by default, however the user can specify it should be saved
    if not save_midi:
        midi_path = Path(midi_save_path)
        midi_path.unlink()