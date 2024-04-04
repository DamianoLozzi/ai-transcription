from pyAudioAnalysis import audioSegmentation
import matplotlib.pyplot as plt

# Input audio file
input_file = "src/resources/test_files/test_long.mp3"

# Speaker diarization
diarization = audioSegmentation.speaker_diarization(input_file, n_speakers=0, mid_window=2.0, mid_step=0.2, short_window=0.05, lda_dim=0)

# Plot the diarization
plt.figure(figsize=(10, 2))
plt.plot(diarization)
plt.title("Speaker Diarization")
plt.xlabel("Time (seconds)")
plt.ylabel("Speaker ID")
plt.show()