# Getting Started
Converting mp3 files to wav files for later processing:

`ls *.mp3 | rg -o "(.*?)\.mp3" -r '$1' | xargs -n 1 -I '{}' -d '\n' ffmpeg -i '{}.mp3' -ac 1 'converted/{}.wav'`

# High Level Overview
So how does Shazam work? The answer is to look at music in terms of the frequencies of sound that combine to make it up, rather than as a string of notes or lyrics over time. Shazam works by developing *fingerprints* of a particular song by analysing the most important frequencies that comprise that track, and the time at which these frequencies are most prominent. For example, a song might have a bass drum at a particular frequency that is very distinct.

These fingerprints comprise a pair of particularly distinct frequencies, as well as the different in time at which these frequencies occur. The fingerprints are then formed into a *hash*, a single number which includes all this information. A particular song might have thousands of these hashes associated with it, and the hashes for all songs are placed into a large database.

When a user wishes to identify a song, the exact same process is conducted, creating thousands of hashes from the users recording of that song. Even in the presence of background noise, with compression and distortion, there will stil be some of those most distinct frequencies - that booming bass drum - that can be recovered. The server then searches for which songs have matches in the right places at the right time, to identify the original track.

And that's Shazam at a high level - however, how and why this works (as well as how to implement it), require a bit more analysis.