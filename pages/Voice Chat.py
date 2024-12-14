import streamlit as st
from transformers import WhisperForConditionalGeneration, WhisperProcessor
import torch
import soundfile as sf
import numpy as np
import io
from scipy.signal import resample

# Title
st.title("🎤 Voice-to-Text Chatbot with Whisper")

# Load the Whisper model and processor
@st.cache_resource
def load_models():
    processor = WhisperProcessor.from_pretrained("openai/whisper-small")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")
    return processor, model

processor, model = load_models()

# Function to process audio
def resample_audio(audio_bytes):
    try:
        # Read the audio data
        audio_data, original_samplerate = sf.read(io.BytesIO(audio_bytes))
        
        # Ensure the audio is mono (single channel)
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)
        
        # Resample if not 16 kHz
        if original_samplerate != 16000:
            num_samples = int(len(audio_data) * 16000 / original_samplerate)
            audio_data = resample(audio_data, num_samples)

        # Save the processed audio as 16 kHz WAV
        output_audio = io.BytesIO()
        sf.write(output_audio, audio_data, 16000, format="WAV")
        return output_audio.getvalue()
    except Exception as e:
        st.error(f"Audio processing failed: {e}")
        return None

# Transcription Function
def transcribe_audio(audio_bytes):
    try:
        inputs = processor(audio_bytes, sampling_rate=16000, return_tensors="pt")
        with torch.no_grad():
            predicted_ids = model.generate(inputs["input_features"])
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        return transcription
    except Exception as e:
        st.error(f"Transcription failed: {e}")
        return None

# Chatbot Function
def get_chatbot_response(user_input):
    # Placeholder for chatbot response logic
    return f"Bot: You said '{user_input}'"

# Record Audio Input
st.info("Click below to record your voice and interact with the chatbot.")
audio_input = st.audio_input("Record your voice")

if audio_input:
    st.write("**Recorded Audio:**")
    st.audio(audio_input, format="audio/wav")

    if st.button("Transcribe & Get Response"):
        # Resample audio to 16kHz
        st.info("Processing audio...")
        audio_bytes_16khz = resample_audio(audio_input.getvalue())
        if not audio_bytes_16khz:
            st.error("Could not process the audio for transcription.")
            st.stop()

        # Transcribe audio
        st.info("Transcribing audio...")
        transcription = transcribe_audio(audio_bytes_16khz)
        if transcription:
            st.write(f"**Transcription:** {transcription}")

            # Get chatbot response
            st.info("Getting chatbot response...")
            chatbot_response = get_chatbot_response(transcription)
            st.write(chatbot_response)
        else:
            st.error("Failed to transcribe audio.")
else:
    st.warning("No valid audio input detected. Please record your voice again.")
