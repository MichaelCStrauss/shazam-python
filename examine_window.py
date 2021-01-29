# %%
import numpy as np
import matplotlib.pyplot as plt
from scipy import fft, signal
import scipy
from scipy.io.wavfile import read

# Read the input WAV files
# Fs is the sampling frequency of the file
Fs, input = read("data/001. 24kgoldn - Mood (feat. iann dior).wav")

time_to_plot = np.arange(Fs * 1, Fs * 1.5, dtype=int)
plt.plot(time_to_plot, input[time_to_plot])
plt.title("Sound Signal")
plt.xlabel("Time Index")
plt.ylabel("Magnitude")

# %%
window_length_seconds = 2
window_length_samples = int(window_length_seconds * Fs)
window_length_samples += window_length_samples % 2
num_peaks = 7

amount_to_pad = window_length_samples - input.size % window_length_samples

song_input = np.pad(input, (0, amount_to_pad))

frequencies, times, stft = signal.stft(
    song_input, Fs, nperseg=window_length_samples, nfft=window_length_samples
)


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

peaks, props = signal.find_peaks(abs(window), prominence=0, distance=500)
n_peaks = min(num_peaks, len(peaks))
# Get the n_peaks largest peaks from the prominences
largest_peaks = np.argpartition(props["prominences"], -n_peaks)[-n_peaks:]
astrological_map = []
for peak in peaks[largest_peaks]:
    astrological_map.append([frequencies[peak], abs(window)[peak]])

plt.figure()
plt.plot(frequencies, abs(window), label="Filtered Power Spectrum")
plt.scatter(*zip(*astrological_map), color="r", zorder=10, label="Peaks")
plt.legend()
plt.title("Filtered Log Power Spectrum of Window")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Log Power")
plt.show()


# %%
