
import numpy as np
import librosa

print("VoxSense AI - Audio Feature Test")
print("-" * 35)

sample_rate = 22050
duration = 2

time = np.linspace(
    0, duration, sample_rate * duration, endpoint=False
)
audio = (0.5 * np.sin(2 * np.pi * 220 * time)).astype(np.float32)

mfcc = librosa.feature.mfcc(
    y=audio,
    sr=sample_rate,
    n_mfcc=13
)

print(f"Sample rate: {sample_rate} Hz")
print(f"Duration: {duration} seconds")
print(f"MFCC feature shape: {mfcc.shape}")
print("Audio feature extraction works!")
