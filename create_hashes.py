# %%
import numpy as np
import matplotlib.pyplot as plt
from scipy import fft, signal
from scipy.io.wavfile import read

from create_constellations import create_constellation
# %%
Fs, audio_input = read("data/001. 24kgoldn - Mood (feat. iann dior).wav")

constellation_map = create_constellation(audio_input, Fs)
upper_frequency = 23_000
frequency_bits = 10


def create_hashes(constellation_map, song_id=None):
    hashes = {}
    # assume pre-sorted
    # Iterate the constellation
    for idx, (time, freq) in enumerate(constellation_map):
        # Iterate the next 100 pairs to produce the combinatorial hashes
        for other_time, other_freq in constellation_map[idx : idx + 100]:
            diff = other_time - time
            # If the time difference between the pairs is too small or large
            # ignore this set of pairs
            if diff <= 1 or diff > 10:
                continue

            # Place the frequencies (in Hz) into a 1024 bins
            freq_binned = freq / upper_frequency * (2 ** frequency_bits)
            other_freq_binned = other_freq / upper_frequency * (2 ** frequency_bits)

            # Produce a 32 bit hash
            hash = int(freq_binned) | (int(other_freq_binned) << 10) | (int(diff) << 20)
            hashes[hash] = (time, song_id)
    return hashes

# hashes = create_hashes(constellation_map)
# hashes
# %%
