
import { useEffect, useRef, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000/predict";

export default function App() {
  const [file, setFile] = useState(null);
  const [recording, setRecording] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [duration, setDuration] = useState(0);

  const recorderRef = useRef(null);
  const chunksRef = useRef([]);
  const streamRef = useRef(null);
  const timerRef = useRef(null);
  const secondsRef = useRef(0);

  useEffect(() => {
    return () => {
      clearInterval(timerRef.current);
      streamRef.current?.getTracks().forEach((track) => track.stop());
    };
  }, []);

  async function startRecording() {
    try {
      setError("");
      setResult(null);
      setFile(null);
      setDuration(0);
      secondsRef.current = 0;

      const stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
      });

      streamRef.current = stream;

      const recorder = new MediaRecorder(stream);
      recorderRef.current = recorder;
      chunksRef.current = [];

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) chunksRef.current.push(event.data);
      };

      recorder.onstop = async () => {
        const recordedBlob = new Blob(chunksRef.current, {
          type: recorder.mimeType || "audio/webm",
        });

        try {
          const arrayBuffer = await recordedBlob.arrayBuffer();
          const audioContext = new AudioContext();
          const decoded = await audioContext.decodeAudioData(arrayBuffer);

          const wavBlob = convertToWav(decoded);
          setFile(
            new File([wavBlob], "recording.wav", { type: "audio/wav" })
          );

          await audioContext.close();
        } catch {
          setError(
            "Couldn't convert this recording to WAV. Try Chrome or Edge and record again."
          );
        }

        stream.getTracks().forEach((track) => track.stop());
        streamRef.current = null;
      };

      recorder.start();
      setRecording(true);

      timerRef.current = setInterval(() => {
        secondsRef.current += 1;
        setDuration(secondsRef.current);
      }, 1000);
    } catch {
      setError("Microphone access failed. Allow microphone permission in your browser.");
    }
  }

  function stopRecording() {
    if (recorderRef.current?.state === "recording") {
      recorderRef.current.stop();
    }

    clearInterval(timerRef.current);
    setRecording(false);
  }

  function convertToWav(audioBuffer) {
    const channels = audioBuffer.numberOfChannels;
    const sampleRate = audioBuffer.sampleRate;
    const frames = audioBuffer.length;
    const bytesPerSample = 2;
    const output = new ArrayBuffer(44 + frames * channels * bytesPerSample);
    const view = new DataView(output);

    function writeString(offset, value) {
      for (let i = 0; i < value.length; i++) {
        view.setUint8(offset + i, value.charCodeAt(i));
      }
    }

    writeString(0, "RIFF");
    view.setUint32(4, 36 + frames * channels * bytesPerSample, true);
    writeString(8, "WAVE");
    writeString(12, "fmt ");
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true);
    view.setUint16(22, channels, true);
    view.setUint32(24, sampleRate, true);
    view.setUint32(28, sampleRate * channels * bytesPerSample, true);
    view.setUint16(32, channels * bytesPerSample, true);
    view.setUint16(34, 16, true);
    writeString(36, "data");
    view.setUint32(40, frames * channels * bytesPerSample, true);

    let offset = 44;
    for (let i = 0; i < frames; i++) {
      for (let channel = 0; channel < channels; channel++) {
        const sample = Math.max(-1, Math.min(1, audioBuffer.getChannelData(channel)[i]));
        view.setInt16(
          offset,
          sample < 0 ? sample * 32768 : sample * 32767,
          true
        );
        offset += 2;
      }
    }

    return new Blob([output], { type: "audio/wav" });
  }

  async function analyzeAudio() {
    if (!file) {
      setError("Record your voice or choose a WAV file first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(API_URL, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Audio analysis failed.");
      }

      setResult(data);
    } catch (err) {
      setError(err.message || "Couldn't connect to the backend. Is it running?");
    } finally {
      setLoading(false);
    }
  }

  function chooseFile(event) {
    const selected = event.target.files?.[0];
    if (!selected) return;

    setFile(selected);
    setResult(null);
    setError("");
    setDuration(0);
  }

  const audioUrl = file ? URL.createObjectURL(file) : null;

  useEffect(() => {
    return () => {
      if (audioUrl) URL.revokeObjectURL(audioUrl);
    };
  }, [audioUrl]);

  return (
    <main className="app">
      <header className="header">
        <div className="brand">◈ VoxSense AI</div>
        <span className="status">Speech Emotion Pattern Analyzer</span>
      </header>

      <section className="hero">
        <p className="eyebrow">VOICE • AUDIO • MACHINE LEARNING</p>
        <h1>Understand the patterns in your voice.</h1>
        <p>Record a sample or upload a WAV file to analyze vocal-expression patterns.</p>
      </section>

      <section className="upload-card">
        <h2>🎙️ Record your voice</h2>
        <p>Allow microphone access when your browser asks.</p>

        <div className="record-controls">
          <button onClick={startRecording} disabled={recording || loading}>
            🎤 Start recording
          </button>
          <button onClick={stopRecording} disabled={!recording}>
            ⏹ Stop recording
          </button>
          <span className={recording ? "recording-live" : ""}>
            {recording ? `Recording… ${duration}s` : `Duration: ${duration}s`}
          </span>
        </div>

        <div className="divider">OR UPLOAD AN AUDIO FILE</div>
        <label className="file-picker">
          Choose audio file
          <input type="file" accept=".wav,audio/wav" onChange={chooseFile} />
        </label>

        {file && (
          <div className="audio-preview">
            <p>Selected: {file.name}</p>
            <audio controls src={audioUrl} />
            <button onClick={analyzeAudio} disabled={loading || recording}>
              {loading ? "Analyzing..." : "Analyze audio"}
            </button>
          </div>
        )}

        {error && <p className="error-message">{error}</p>}
      </section>

      {result && (
        <section className="result-card">
          <p className="eyebrow">ANALYSIS RESULT</p>
          <h2>Predicted pattern: {result.prediction}</h2>
          <p>Model confidence: {(result.confidence * 100).toFixed(1)}%</p>

          <h3>Category scores</h3>
          {Object.entries(result.scores || {})
            .sort((a, b) => b[1] - a[1])
            .map(([emotion, score]) => (
              <div className="score-row" key={emotion}>
                <span>{emotion}</span>
                <div className="score-track">
                  <div
                    className="score-fill"
                    style={{ width: `${Math.max(0, Math.min(1, score)) * 100}%` }}
                  />
                </div>
                <span>{(score * 100).toFixed(1)}%</span>
              </div>
            ))}

          
          <h3>Speech Analysis</h3>
          <div className="speech-analysis">
            <div className="analysis-metric">
              <span className="metric-icon">◷</span>
              <span>Audio Duration</span>
              <strong>
                {result.speech_analysis?.duration_seconds ?? "—"} sec
              </strong>
            </div>

            <div className="analysis-metric">
              <span className="metric-icon">♫</span>
              <span>Estimated Pauses</span>
              <strong>
                {result.speech_analysis?.estimated_pauses ?? "—"}
              </strong>
            </div>

            <div className="analysis-metric">
              <span className="metric-icon">〰</span>
              <span>Pitch Variation</span>
              <strong>
                {result.speech_analysis?.pitch_variation_hz != null
                  ? `${result.speech_analysis.pitch_variation_hz} Hz`
                  : "Unavailable"}
              </strong>
            </div>
          </div>

          <div className="waveform">
            {[18, 30, 14, 42, 24, 52, 34, 60, 28, 46, 18, 55, 36, 64, 24, 44, 16, 38, 56, 26, 48, 20, 40, 58, 30, 46, 18, 36, 52, 24].map(
              (height, index) => (
                <span
                  key={index}
                  className="waveform-bar"
                  style={{ height: `${height}px` }}
                />
              )
            )}
          </div>

          <p className="disclaimer">
            This estimates vocal-expression patterns; it cannot determine a person's true feelings.
          </p>
        </section>
      )}
    </main>
  );
}
