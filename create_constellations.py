# %%
import numpy as np
import matplotlib.pyplot as plt
from scipy import fft, signal
from scipy.io.wavfile import read

# %%


def create_constellation(audio, Fs):
    # Parameters
    window_length_seconds = 0.5
    window_length_samples = int(window_length_seconds * Fs)
    window_length_samples += window_length_samples % 2
    num_peaks = 15

    # Pad the song to divide evenly into windows
    amount_to_pad = window_length_samples - audio.size % window_length_samples

    song_input = np.pad(audio, (0, amount_to_pad))

    # Perform a short time fourier transform
    frequencies, times, stft = signal.stft(
        song_input, Fs, nperseg=window_length_samples, nfft=window_length_samples, return_onesided=True
    )

    constellation_map = []

    for time_idx, window in enumerate(stft.T):
        # Spectrum is by default complex. 
        # We want real values only
        spectrum = abs(window)
        # Find peaks - these correspond to interesting features
        # Note the distance - want an even spread across the spectrum
        peaks, props = signal.find_peaks(spectrum, prominence=0, distance=200)

        # Only want the most prominent peaks
        # With a maximum of 15 per time slice
        n_peaks = min(num_peaks, len(peaks))
        # Get the n_peaks largest peaks from the prominences
        # This is an argpartition
        # Useful explanation: https://kanoki.org/2020/01/14/find-k-smallest-and-largest-values-and-its-indices-in-a-numpy-array/
        largest_peaks = np.argpartition(props["prominences"], -n_peaks)[-n_peaks:]
        for peak in peaks[largest_peaks]:
            frequency = frequencies[peak]
            constellation_map.append([time_idx, frequency])

    return constellation_map


Fs, input = read("data/001. 24kgoldn - Mood (feat. iann dior).wav")
constellation_map = create_constellation(input, Fs)
# plt.scatter(*zip(*constellation_map))
# Fs, input = read("recording1.wav")
# constellation_map = create_constellation(input, Fs)
# for c in constellation_map:
#     c[0] += 70
# plt.scatter(*zip(*constellation_map))
# plt.title("Constellation Map")
# plt.xlabel("Time (index)")
# plt.ylabel("Frequency (Hz)")
# # plt.xlim((65, 100))
# plt.show()

# # # %%

# # %%

# %%
