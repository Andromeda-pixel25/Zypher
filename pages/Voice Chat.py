import streamlit as st
import torch
from langchain.chains import LLMChain
from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
import numpy as np
import soundfile as sf
import io
from scipy.signal import resample

# Set the title of the Streamlit app
st.title("\U0001F3A4 Voice-based Chat")

# Record voice input using st.audio_input
st.info("Click below to record your voice and interact with the chatbot.")
voice_input = st.audio_input("Record your voice")

# Ensure voice input is not empty
if voice_input is not None:
    st.write("**Recorded Audio:**")
    st.audio(voice_input, format="audio/wav")

    if st.button("Transcribe & Get Response"):
        try:
            # Convert audio input to a format suitable for Whisper
            audio_bytes = voice_input.getvalue()
            audio_io = io.BytesIO(audio_bytes)
            audio_data, sample_rate = sf.read(audio_io)

            # Resample if the sample rate is not 16 kHz
            if sample_rate != 16000:
                num_samples = int(len(audio_data) * (16000 / sample_rate))
                audio_data = resample(audio_data, num_samples)
                sample_rate = 16000  # Set to 16 kHz

            # Save the audio data to a temporary file to send to Whisper
            temp_audio_file = "temp_audio.wav"
            sf.write(temp_audio_file, audio_data, sample_rate)

            # Create a LangChain Whisper model for transcription
            whisper_model = HuggingFaceHub(
                repo_id="openai/whisper-large",
                model_kwargs={"language": "en"}
            )

            # Transcribe audio using LangChain
            transcription = whisper_model.predict(temp_audio_file)
            st.write(f"**Transcription:** {transcription}")

            # Create a GPT-2 model for generating responses
            gpt_model = HuggingFaceHub(repo_id="gpt2")

            # Generate a response from the GPT-2 model
            response = gpt_model.predict(transcription)
            st.write(f"**Bot:** {response}")

        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    st.warning("No valid audio input detected. Please record your voice again.")
