
from pathlib import Path
from collections import Counter

# Find the dataset folder from the project root
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"

# RAVDESS emotion codes
EMOTIONS = {
    "01": "neutral",
    "02": "calm",
    "03": "happy",
    "04": "sad",
    "05": "angry",
    "06": "fearful",
    "07": "disgust",
    "08": "surprised",
}

audio_files = list(DATA_DIR.rglob("*.wav"))
emotion_counts = Counter()

for file_path in audio_files:
    # RAVDESS filenames look like 03-01-06-01-02-01-12.wav
    parts = file_path.stem.split("-")

    if len(parts) == 7 and parts[2] in EMOTIONS:
        emotion_counts[EMOTIONS[parts[2]]] += 1

print("VoxSense AI - Dataset Check")
print("-" * 30)
print(f"Total WAV files found: {len(audio_files)}")
print("\nFiles by emotion:")

for emotion, count in sorted(emotion_counts.items()):
    print(f"{emotion.capitalize():12} {count}")

if not audio_files:
    print("\nNo audio files found. Check the data folder.")
elif sum(emotion_counts.values()) == 0:
    print("\nAudio files found, but filenames need checking.")
else:
    print("\nDataset check complete!")
