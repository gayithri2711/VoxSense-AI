
from pathlib import Path

import librosa
import numpy as np
import pandas as pd

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
OUTPUT_FILE = DATA_DIR / "features.csv"

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

def extract_features(audio_path):
    """Extract 40 MFCC-based features from one audio recording."""
    audio, sample_rate = librosa.load(
        audio_path,
        sr=22050,
        mono=True
    )

    mfcc = librosa.feature.mfcc(
        y=audio,
        sr=sample_rate,
        n_mfcc=40
    )

    # Mean value of each of the 40 MFCCs
    return np.mean(mfcc, axis=1)


def main():
    audio_files = sorted(DATA_DIR.rglob("*.wav"))
    rows = []

    print(f"Found {len(audio_files)} audio files.")

    for index, audio_path in enumerate(audio_files, start=1):
        parts = audio_path.stem.split("-")

        # Skip files that don't follow the RAVDESS naming format
        if len(parts) != 7 or parts[2] not in EMOTIONS:
            continue

        try:
            features = extract_features(audio_path)

            row = {
                f"mfcc_{i + 1}": float(value)
                for i, value in enumerate(features)
            }
            row["emotion"] = EMOTIONS[parts[2]]
            row["actor"] = int(parts[6])

            rows.append(row)

        except Exception as error:
            print(f"\nCould not process {audio_path.name}: {error}")

        if index % 50 == 0 or index == len(audio_files):
            print(f"Processed {index}/{len(audio_files)} files")

    if not rows:
        print("No features extracted. Check the dataset folder.")
        return

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_FILE, index=False)

    print("\nFeature extraction complete!")
    print(f"Recordings processed: {len(df)}")
    print(f"Saved to: {OUTPUT_FILE}")
    print("\nEmotion counts:")
    print(df["emotion"].value_counts().sort_index())


if __name__ == "__main__":
    main()
