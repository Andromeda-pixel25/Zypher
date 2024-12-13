# Page 2: Voice-based Chat (pages/Voice Chat.py)
import streamlit as st
import sounddevice as sd
import numpy as np
import wave
import requests

st.title("🎤 Voice-based Chat")

# Recording settings
fs = 44100  # Sample rate
seconds = 5  # Duration of recording

# Record audio
if st.button("Record Voice"):
    st.write("Recording...")
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2, dtype='int16')
    sd.wait()  # Wait until recording is finished

    # Save to WAV file
    filename = "temp_audio.wav"
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(np.dtype('int16').itemsize)
        wf.setframerate(fs)
        wf.writeframes(recording.tobytes())

    st.audio(filename, format="audio/wav")
    
    # Transcribe using Hugging Face Whisper model
    response = requests.post(
        "https://api-inference.huggingface.co/models/openai/whisper-base",
        headers={"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"},
        files={"file": open(filename, "rb")},
    )
    try:
        response_data = response.json()
        transcription = response_data.get("text", "Could not transcribe audio.")
    except ValueError:
        transcription = "Error: Invalid response from transcription API."
    st.write(f"**Transcription:** {transcription}")
