import os
import subprocess

import sys


class DistingConvertor:
    def __init__(self, input_folder):
        folder_abs_path = os.path.abspath(input_folder)
        if not os.path.isdir(folder_abs_path):
            raise ValueError(f"Invalid folder: {folder_abs_path}")
        self.input_folder = folder_abs_path
        self.output_folder = f"{self.input_folder}/converted"
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def convert_files(self):
        for file in os.listdir(self.input_folder):
            if file.endswith(".wav"):
                self.convert_file_to_disting_format(file)

    def convert_file_to_disting_format(self, file):
        input_file = os.path.join(self.input_folder, file)
        output_file = os.path.join(self.output_folder, f"{os.path.splitext(file)[0]}.wav")
        print(f"OUTPUT: {output_file}")
        output_file = os.path.normpath(output_file)
        subprocess.call(["ffmpeg", "-y", "-i", input_file, "-ar", "44100", "-ac", "1", "-sample_fmt", "s16", output_file])

    def generate_multisample_playlist(self):
        # Open the file in write mode
        playlist_path = f"{self.output_folder}/playlist.txt"
        with open(playlist_path, "w+") as f:
            # Write disting playlist v1 header
            f.write("disting playlist v1\n")
            # Disable looping for multisamples
            f.write("-loop = 0\n")
            # Only pick new samples when new trigger happens
            f.write("-retriggerOnSampleChange = 0\n")
            # Keep track of the previous MIDI note written to the playlist for calculating the split values
            previous_midi_note = None
            # Sort files by ascending note order
            sorted_note_files = self.get_sorted_note_files()
            # Parse the note wav files to their MIDI numbers
            for file in sorted_note_files:
                # Write the file name first
                f.write(f"{file}\n")
                # Get the note's midi value and assign it to the natural key
                note = file.split(".wav")[0]
                midi_value = self._note_to_midi_number(note)
                # Calculate split if it's not the first note
                if previous_midi_note:
                    # Calculate the rounded integer average between the new and previous midi values
                    switch_value = (midi_value + previous_midi_note + 1) // 2
                    f.write(f"-switch={switch_value}\n")
                f.write(f"-natural={midi_value}\n")
                previous_midi_note = midi_value

    def get_sorted_note_files(self):
        wav_files = []
        for file in os.listdir(self.input_folder):
            if file.endswith(".wav"):
                wav_files.append(file)
        return sorted(wav_files, key=self._note_sort_key)

    def _note_sort_key(self, note_file):
        note = note_file.split(".wav")[0]
        midi_value = self._note_to_midi_number(note)
        return midi_value

    @staticmethod
    def _note_to_midi_number(note: str):
        pitch_classes = {
            "C": 0,
            "C#": 1,
            "D": 2,
            "D#": 3,
            "E": 4,
            "F": 5,
            "F#": 6,
            "G": 7,
            "G#": 8,
            "A": 9,
            "A#": 10,
            "B": 11,
        }
        note_pitch_class = note[:-1]
        note_octave = int(note[-1])
        midi_number = 12 + 12 * note_octave + pitch_classes[note_pitch_class]
        return midi_number

    def convert(self):
        self.convert_files()
        self.generate_multisample_playlist()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python convert_multisamples.py [arg]")
    else:
        folder = sys.argv[1]
        disting_convertor = DistingConvertor(folder)
        disting_convertor.convert()
