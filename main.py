
from pathlib import Path
import os
import joblib
import librosa
import numpy as np

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware


# Project paths
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "emotion_model.joblib"

# Load the trained model
bundle = joblib.load(MODEL_PATH)
model = bundle["model"]
feature_columns = bundle["feature_columns"]
emotions = bundle["emotions"]

app = FastAPI(title="VoxSense AI API")

# Allow our local React website to connect
frontend_url = os.getenv("FRONTEND_URL", "").strip()

allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

if frontend_url:
    allowed_origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "VoxSense AI API is running!",
        "project": "VoxSense AI",
    }



@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".wav"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a WAV audio file.",
        )

    audio_bytes = await file.read()

    if not audio_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    try:
        import io

        audio, sample_rate = librosa.load(
            io.BytesIO(audio_bytes),
            sr=22050,
            mono=True,
            duration=15,
        )

        if len(audio) == 0:
            raise ValueError("No audio samples found.")

        mfcc = librosa.feature.mfcc(
            y=audio,
            sr=sample_rate,
            n_mfcc=40,
        )

        features = np.mean(mfcc.T, axis=0).reshape(1, -1)
                # Speech analysis metrics
        duration_seconds = round(len(audio) / sample_rate, 2)

        rms = librosa.feature.rms(y=audio)[0]
        silence_threshold = max(float(np.max(rms)) * 0.05, 0.005)
        silent_frames = rms < silence_threshold

        frame_duration = 512 / sample_rate
        estimated_pauses = 0
        in_pause = False
        pause_frames = 0

        for silent in silent_frames:
            if silent:
                pause_frames += 1
            else:
                if pause_frames * frame_duration >= 0.3:
                    estimated_pauses += 1
                pause_frames = 0

        if pause_frames * frame_duration >= 0.3:
            estimated_pauses += 1

        pitch = librosa.yin(
            audio,
            fmin=70,
            fmax=400,
            sr=sample_rate,
        )

        valid_pitch = pitch[np.isfinite(pitch)]

        pitch_variation_hz = (
            round(float(np.std(valid_pitch)), 2)
            if len(valid_pitch) > 1
            else None
        )

        probabilities = model.predict_proba(features)[0]
        predicted_index = int(np.argmax(probabilities))
        predicted_emotion = str(model.classes_[predicted_index])

        scores = {
            str(label): round(float(score), 4)
            for label, score in zip(model.classes_, probabilities)
        }

        return {
            "prediction": predicted_emotion,
            "confidence": round(
                float(probabilities[predicted_index]), 4
            ),
            "scores": scores,
                        "speech_analysis": {
                "duration_seconds": duration_seconds,
                "estimated_pauses": estimated_pauses,
                "pitch_variation_hz": pitch_variation_hz,
            },
            "note": (
                "This estimates vocal-expression patterns; "
                "it does not determine a person's true feelings."
            ),
        }

    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=f"Could not process this audio file: {error}",
        ) from error
