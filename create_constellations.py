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

    amount_to_pad = window_length_samples - audio.size % window_length_samples

    song_input = np.pad(audio, (0, amount_to_pad))

    frequencies, times, stft = signal.stft(
        song_input, Fs, nperseg=window_length_samples, nfft=window_length_samples, return_onesided=True
    )

    constellation_map = []

    for time_idx, window in enumerate(stft.T):
        spectrum = abs(window)
        peaks, props = signal.find_peaks(spectrum, prominence=0, distance=500)
        n_peaks = min(num_peaks, len(peaks))
        # Get the n_peaks largest peaks from the prominences
        largest_peaks = np.argpartition(props["prominences"], -n_peaks)[-n_peaks:]
        for peak in peaks[largest_peaks]:
            frequency = frequencies[peak]
            constellation_map.append([time_idx, frequency])

    return constellation_map


# Fs, input = read("data/001. 24kgoldn - Mood (feat. iann dior).wav")
# constellation_map = create_constellation(input, Fs)
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

# # %%
