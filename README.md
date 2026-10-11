# 🎙️ VoxSense AI — Speech Emotion Pattern Analyzer

VoxSense AI is a machine learning web application that analyzes speech audio and predicts a possible emotion from vocal patterns. It combines a Python backend with a React frontend to provide an interactive audio analysis experience.

## ✨ Features

- 🎤 Record speech directly in the browser
- 📁 Upload an audio recording for analysis
- 🧠 Predict speech emotion using a trained machine learning model
- 📊 Display prediction confidence and category scores
- 📈 Show speech analysis metrics, including duration, estimated pauses, and pitch variation
- 🖥️ Interactive web interface built with React

## 🛠️ Tech Stack

**Frontend**
- React
- Vite
- JavaScript
- CSS

**Backend**
- Python
- FastAPI
- Uvicorn
- Librosa
- NumPy
- Joblib

**Machine Learning**
- Scikit-learn
- MFCC audio features
- Trained emotion classification model

## 📂 Project Structure

```text
VoxSense-AI/
├── main.py
├── ml/
│   ├── extract_features.py
│   ├── train_model.py
│   ├── check_dataset.py
│   └── audio_test.py
├── models/
│   └── emotion_model.joblib
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
├── data/                 # Local training data (not uploaded)
├── .gitignore
└── README.md
```

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/gayithri2711/VoxSense-AI.git
cd VoxSense-AI
```

### 2. Set up the Python environment

```bash
python -m venv .venv
```

Activate it in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the required backend packages:

```powershell
pip install fastapi "uvicorn[standard]" python-multipart librosa numpy pandas scikit-learn soundfile matplotlib joblib
```

### 3. Start the backend

```powershell
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Open the API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### 4. Start the frontend

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open the local frontend URL shown in the terminal, usually [http://localhost:5173](http://localhost:5173).

## 📊 Speech Analysis Metrics

- **Predicted emotion:** The model's predicted category for the audio.
- **Confidence:** The model's confidence score for its prediction.
- **Estimated pauses:** An estimate based on quiet portions of the recording.
- **Pitch variation:** A measure of variation in the detected vocal pitch.

These measurements describe acoustic patterns. They do not establish a person's actual emotional state.

## ⚠️ Disclaimer

VoxSense AI is an experimental machine learning project for educational and research purposes. Speech emotion predictions may be inaccurate and can be affected by recording quality, language, speaker differences, and background noise. Predictions should not be treated as definitive judgments about a person's feelings.

## 👩‍💻 Author

**Gayithri**

GitHub: [@gayithri2711](https://github.com/gayithri2711)
