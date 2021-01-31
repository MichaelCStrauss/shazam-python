# Shazam In Python

This repository gives an overview of how the original versions of Shazam, detailed in [Wang](Wang03-shazam.pdf),
operate, with code examples in Python. 

I recommend reading [the Jupyter notebook](article.ipynb), rendered on [my website](https://michaelstrauss.dev/shazam-in-python).

## Basic Instructions for Running the Code

This loose collection of files are made to be modified to suit your own files and directory structure, however some basic guidance is to:

1. Install requirements: `pip install -r requirements.txt`
2. Create a collection of `.wav` files in `data/` from MP3s using a command such as `ls *.mp3 | rg -o "(.*?)\.mp3" -r '$1' | xargs -n 1 -I '{}' -d '\n' ffmpeg -i '{}.mp3' -ac 1 'converted/{}.wav`
3. Create a database of song fingerprints: `python create_database.py`
4. Match a `recording.wav` to one of the songs in the database using: `python find_match.py`