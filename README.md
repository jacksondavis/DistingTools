# DistingTools
Basic python scripts for formatting samples or MIDI to the Disting Mk4 eurorack module formats

Currently only supports converting files for the multisample audio algorithms J-2 and J-6

**Requries FFMPEG**
- Install link: https://ffmpeg.org/download.html
- Make sure `ffmpeg` is in your path since this uses `subprocess.call()` to run FFMPEG from the CLI

## Summary
Whipped this up quickly and will add to it. Right now it supports converting certain files downloaded
from https://www.pianobook.co.uk/ that have samples named "C1.wav", "C2.wav", "C3.wav", etc. 

## Running
Will add better file parsing, but if files are in the above format you can run:
`python .\convert_multisamples.py <folder_containing_samples>`

This will create a folder called `<folder_containing_samples>/converted`, with audio files in the Disting Mk4 expected
format, and a `playlist.txt` file used for modes J-2 and J-6.

## Example
An example of working sample files is here. Download in the DecentSampler format: https://www.pianobook.co.uk/packs/fluteviolin/

Unzip that file, find the location of the `/samples/wave/` directory, and run:
`python .\convert_multisamples.py <samples folder>`
