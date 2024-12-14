import streamlit as st
import requests
import numpy as np
import io
import soundfile as sf
from scipy.signal import resample
import time

# Title
st.title("🎤 Voice-to-Text Chatbot with 16kHz Audio")

# Initialize Hugging Face models
HUGGINGFACE_API_TOKEN = st.secrets["HUGGINGFACE_API_TOKEN"]
WHISPER_MODEL_API = "https://api-inference.huggingface.co/models/openai/whisper-small"
CHATBOT_MODEL_API = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"

# Function to resample audio to 16kHz
def resample_audio(audio_bytes):
    try:
        # Read audio data
        data, samplerate = sf.read(io.BytesIO(audio_bytes))
        if samplerate != 16000:
            st.warning(f"Resampling audio from {samplerate} Hz to 16kHz...")
            num_samples = int(len(data) * 16000 / samplerate)
            resampled_data = resample(data, num_samples)
            audio_bytes_16khz = io.BytesIO()
            sf.write(audio_bytes_16khz, resampled_data, 16000, format="WAV")
            return audio_bytes_16khz.getvalue()
        return audio_bytes
    except Exception as e:
        st.error(f"Audio processing failed: {e}")
        return None

# Function to call Hugging Face API with retry logic
def call_huggingface_api(url, headers, files=None, data=None, json=None, retries=3, delay=10):
    for attempt in range(retries):
        response = requests.post(url, headers=headers, files=files, data=data, json=json)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 503:
            st.warning(f"Model is loading. Retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})")
            time.sleep(delay)
        else:
            st.error(f"API Error {response.status_code}: {response.text}")
            return None
    st.error("Model is unavailable after multiple retries. Please try again later.")
    return None

# Record Audio Input
st.info("Click below to record your voice and interact with the chatbot.")
audio_input = st.audio_input("Record your voice")

if audio_input:
    st.write("**Recorded Audio:**")
    st.audio(audio_input, format="audio/wav")

    if st.button("Transcribe & Get Response"):
        try:
            # Resample audio to 16kHz
            st.info("Processing audio...")
            audio_bytes_16khz = resample_audio(audio_input.getvalue())
            if not audio_bytes_16khz:
                st.error("Could not process the audio for transcription.")
                st.stop()

            # Call Whisper API for transcription with retry logic
            headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}
            transcription_response = call_huggingface_api(
                WHISPER_MODEL_API,
                headers,
                files={"file": io.BytesIO(audio_bytes_16khz)},
            )

            if transcription_response:
                transcription = transcription_response.get("text", "Transcription failed.")
                st.write(f"**Transcription:** {transcription}")

                # Chatbot interaction
                chatbot_response = call_huggingface_api(
                    CHATBOT_MODEL_API,
                    headers,
                    json={"inputs": transcription},
                )

                if chatbot_response:
                    ai_reply = chatbot_response.get("generated_text", "No response.")
                    st.write(f"**Bot:** {ai_reply}")
                else:
                    st.error("Failed to get chatbot response.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    st.warning("No valid audio input detected. Please record your voice again.")
