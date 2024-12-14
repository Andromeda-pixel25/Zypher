import streamlit as st
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torch
import numpy as np
import io
import soundfile as sf

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

        # Check original sample rate
        st.write(f"Original Sample Rate: {original_samplerate} Hz")

        # Resample to 16 kHz if necessary
        if original_samplerate != 16000:
            num_samples = int(len(audio_data) * 16000 / original_samplerate)
            audio_data = np.interp(np.linspace(0, len(audio_data), num_samples), np.arange(len(audio_data)), audio_data)
            st.write("Audio resampled to 16 kHz.")
        else:
            st.write("Audio is already at 16 kHz.")

        # Ensure the audio data is in the correct format
        audio_data = audio_data.astype(np.float32)

        # Save the processed audio as 16 kHz WAV
        output_audio = io.BytesIO()
        sf.write(output_audio, audio_data, 16000, format="WAV")
        output_audio.seek(0)  # Move to the start of the BytesIO object
        return output_audio.read()
    except Exception as e:
        st.error(f"Audio processing failed: {e}")
        return None

# Transcription function
def transcribe_audio(audio_bytes):
    try:
        # Prepare audio for the model
        inputs = processor(audio_bytes, sampling_rate=16000, return_tensors="pt")
        st.write("Inputs for model:", inputs)  # Debugging line
        with torch.no_grad():
            predicted_ids = model.generate(inputs["input_features"])
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        return transcription
    except Exception as e:
        st.error(f"Transcription failed: {e}")
        return None

# Placeholder for chatbot response
def get_chatbot_response(user_input):
    return f"Bot: You said '{user_input}'"

# Record audio input
st.info("Click below to record your voice and interact with the chatbot.")
audio_input = st.audio_input("Record your voice")

if audio_input:
    st.write("**Recorded Audio:**")
    st.audio(audio_input, format="audio/wav")

    if st.button("Transcribe & Get Response"):
        st.info("Processing audio...")

        # Process audio to ensure it's 16 kHz
        audio_bytes_16khz = process_audio(audio_input.getvalue())
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
