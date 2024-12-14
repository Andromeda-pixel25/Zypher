import streamlit as st
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torch
import numpy as np
import soundfile as sf
import io

# Title
st.title("🎤 Voice-to-Text Chatbot with Whisper")

# Load Whisper model and processor
@st.cache_resource
def load_models():
    processor = WhisperProcessor.from_pretrained("openai/whisper-small")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")
    return processor, model

processor, model = load_models()

# Function to process audio
def process_audio(audio_bytes):
    try:
        # Read audio file
        audio_data, original_samplerate = sf.read(io.BytesIO(audio_bytes))
        
        # Ensure the audio is mono (single channel)
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)

        # Resample to 16 kHz if necessary
        if original_samplerate != 16000:
            num_samples = int(len(audio_data) * 16000 / original_samplerate)
            audio_data = np.interp(np.linspace(0, len(audio_data), num_samples), np.arange(len(audio_data)), audio_data)

        # Ensure the audio data is in the correct format
        audio_data = audio_data.astype(np.float32)

        return audio_data
    except Exception as e:
        st.error(f"Audio processing failed: {e}")
        return None

# Transcription function
def transcribe_audio(audio_data):
    try:
        # Prepare audio for the model, specifying language='en' for English
        inputs = processor(audio_data, sampling_rate=16000, return_tensors="pt", language="en")
        with torch.no_grad():
            predicted_ids = model.generate(inputs["input_features"])
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        return transcription
    except Exception as e:
        st.error(f"Transcription failed: {e}")
        return None

# Record audio input
st.info("Click below to record your voice and interact with the chatbot.")
audio_input = st.audio_input("Record your voice")

if audio_input:
    st.write("**Recorded Audio:**")
    st.audio(audio_input)  # Playback of the recorded audio

    if st.button("Transcribe & Get Response"):
        st.info("Processing audio...")

        # Process audio to ensure it's 16 kHz
        audio_data = process_audio(audio_input.getvalue())
        if audio_data is None:
            st.error("Could not process the audio for transcription.")
            st.stop()

        # Transcribe audio
        st.info("Transcribing audio...")
        transcription = transcribe_audio(audio_data)
        if transcription:
            st.write(f"**Transcription:** {transcription}")
        else:
            st.error("Failed to transcribe audio.")
else:
    st.warning("No valid audio input detected. Please record your voice again.")
