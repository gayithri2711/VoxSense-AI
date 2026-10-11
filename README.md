# 🎙️ VoxSense AI — Speech Emotion Pattern Analyzer

**VoxSense AI** is a machine learning project that analyzes uploaded speech audio and predicts an emotion category from extracted audio features.

🌐 **Live Demo:** https://voxsense-ai-frontend.onrender.com  
📘 **API Documentation:** https://voxsense-ai-api.onrender.com/docs

## ✨ Features

- 🎧 Upload WAV audio for analysis
- 🤖 Predict an emotion category using a trained machine learning model
- 📊 Display prediction confidence and class scores
- 🎵 Extract MFCC audio features using Librosa
- 📈 Analyze speech characteristics such as duration, pauses, and pitch variation
- 🌐 Access the application through a deployed web interface and API

## 🛠️ Tech Stack

**Frontend**
- React
- Vite
- JavaScript

**Backend**
- Python
- FastAPI
- Uvicorn

**Machine Learning & Audio Processing**
- Scikit-learn
- Librosa
- NumPy
- SoundFile
- Joblib

**Deployment**
- Render
- GitHub

## 🏗️ How It Works

1. The user uploads a WAV audio file through the web interface.
2. The backend processes the audio and extracts MFCC features.
3. The trained machine learning model generates an emotion-category prediction.
4. The API returns the predicted category, confidence, class scores, and available speech-analysis measurements.
5. The frontend displays the analysis results.

## 🚀 Try the Live Application

1. Open the [VoxSense AI website](https://voxsense-ai-frontend.onrender.com).
2. Upload a supported WAV audio file.
3. Run the analysis.
4. Review the predicted emotion category and analysis results.

## 💻 Run Locally

### Prerequisites

- Python installed
- Node.js and npm installed
- Git installed

### 1. Clone the repository

```bash
git clone https://github.com/gayithri2711/VoxSense-AI.git
cd VoxSense-AI
```

### 2. Set up the Python backend

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the backend from the repository root:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

Interactive API documentation: `http://127.0.0.1:8000/docs`

### 3. Set up the frontend

Open a second terminal:

```bash
cd frontend
npm install
```

Create a `.env` file inside the `frontend` directory containing:

```env
VITE_API_URL=http://127.0.0.1:8000/predict
```

Start the frontend:

```bash
npm run dev
```

Open the local URL printed by Vite in your terminal.

## 📁 Project Structure

```text
VoxSense-AI/
├── frontend/          # React frontend
├── models/            # Trained machine learning model
├── main.py            # FastAPI backend
├── requirements.txt   # Python dependencies
├── render.yaml        # Backend deployment configuration
└── README.md
```

## ⚠️ Limitations

- Predictions depend on the quality of the audio and the training data.
- Emotion categories are model estimates, not definitive measurements of a person's feelings.
- Supported audio formats and prediction categories depend on the implementation and trained model.
- The first request after inactivity may take longer because of free-tier hosting.

## 🔮 Future Improvements

- Add more audio-format support.
- Improve model evaluation and prediction reliability.
- Add visualizations of audio features.
- Expand testing and error handling.
- Improve accessibility and the user experience.

## 👩‍💻 Author

**Gayithri**

GitHub: https://github.com/gayithri2711

---

⭐ If you find this project interesting, consider starring the repository.
