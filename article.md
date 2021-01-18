# Getting Started
Converting mp3 files to wav files for later processing:

`ls *.mp3 | rg -o "(.*?)\.mp3" -r '$1' | xargs -n 1 -I '{}' -d '\n' ffmpeg -i '{}.mp3' -ac 1 'converted/{}.wav'`