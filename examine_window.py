# %%
import numpy as np
import matplotlib.pyplot as plt
from scipy import fft, signal
import scipy
from scipy.io.wavfile import read

# %%
Fs, input = read("data/001. 24kgoldn - Mood (feat. iann dior).wav")

# Parameters
window_length_seconds = 2
window_length_samples = int(window_length_seconds * Fs)
window_length_samples += window_length_samples % 2
num_peaks = 7

amount_to_pad = window_length_samples - input.size % window_length_samples

song_input = np.pad(input, (0, amount_to_pad))

frequencies, times, stft = signal.stft(
    song_input, Fs, nperseg=window_length_samples, nfft=window_length_samples
)

astrological_map = []

windows = stft.T


num_windows = windows.shape[0]
window = windows[num_windows // 2 + 5, :]
plt.plot(frequencies, abs(window) ** 2)
plt.title("Power Spectrum of Window")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Power")

# %%
spectrum = np.log(abs(window) ** 2)
plt.figure()
plt.plot(frequencies, spectrum)
plt.title("Log Power Spectrum of Window")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Log Power")
# %%
filter_freq = 0.005
b, a = signal.butter(3, filter_freq, "low")

filtered = signal.filtfilt(b, a, spectrum)

peaks, props = signal.find_peaks(filtered, prominence=0)
n_peaks = min(num_peaks, len(peaks))
# Get the n_peaks largest peaks from the prominences
largest_peaks = np.argpartition(props["prominences"], -n_peaks)[-n_peaks:]
for peak in peaks[largest_peaks]:
    astrological_map.append([frequencies[peak], filtered[peak]])

plt.plot(frequencies, filtered, label='Filtered Power Spectrum')
plt.scatter(*zip(*astrological_map), color="r", zorder=10, label="Peaks")
plt.legend()
plt.title("Filtered Log Power Spectrum of Window")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Log Power")
plt.show()

