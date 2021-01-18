# %%
import numpy as np
import matplotlib.pyplot as plt
from scipy import fft, signal
from scipy.io.wavfile import read

# %%


def create_constellation(audio, Fs):
    # Parameters
    window_length_seconds = 3
    window_length_samples = int(window_length_seconds * Fs)
    window_length_samples += window_length_samples % 2
    num_peaks = 3

    amount_to_pad = window_length_samples - audio.size % window_length_samples

    song_input = np.pad(audio, (0, amount_to_pad))

    frequencies, times, stft = signal.stft(
        song_input, Fs, nperseg=window_length_samples, nfft=window_length_samples
    )

    constellation_map = []

    for time_idx, window in enumerate(stft.T):
        spectrum = np.log(abs(window) ** 2)
        filter_freq = 0.005
        b, a = signal.butter(3, filter_freq, "low")

        filtered = signal.filtfilt(b, a, spectrum)
        peaks, props = signal.find_peaks(filtered, prominence=0)
        n_peaks = min(num_peaks, len(peaks))
        # Get the n_peaks largest peaks from the prominences
        largest_peaks = np.argpartition(props["prominences"], -n_peaks)[-n_peaks:]
        for peak in peaks[largest_peaks]:
            constellation_map.append([times[time_idx], frequencies[peak]])

    return constellation_map


Fs, input = read("data/001. 24kgoldn - Mood (feat. iann dior).wav")
constellation_map = create_constellation(input, Fs)
plt.scatter(*zip(*constellation_map))
plt.title("Constellation Map")
plt.xlabel("Time (s)")
plt.ylabel("Frequency (Hz)")

# %%
