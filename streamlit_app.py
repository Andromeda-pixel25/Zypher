# Directory structure:
# - main.py
# - pages/
#     - 1_Text_Response.py
#     - 2_Voice_Response.py
#     - 3_Image_Generation.py

# Main app (main.py)
import streamlit as st

st.set_page_config(page_title="AI Chatbot", layout="wide")
st.title("Welcome to the AI Chatbot App")

st.markdown("""
This app provides the following features:
- **Text Response**: Chat with the AI using text input.
- **Voice Response**: Speak to the AI and get responses.
- **Image Generation**: Generate images based on your descriptions.

Use the sidebar to navigate between pages.
""")

# Page 1: Text Response (pages/1_Text_Response.py)
import streamlit as st
import requests

st.title("Text Response")
st.markdown("""Chat with AI using text input.""")

# Hugging Face API for text generation
API_URL = "https://api-inference.huggingface.co/models/gpt2"
headers = {"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

user_input = st.text_input("Ask a question:")
if user_input:
    with st.spinner("Generating response..."):
        output = query({"inputs": user_input})
        st.text_area("Response:", value=output["generated_text"], height=200)

# Page 2: Voice Response (pages/2_Voice_Response.py)
import streamlit as st
import sounddevice as sd
import numpy as np
import requests
import tempfile
import wave

st.title("Voice Response")
st.markdown("""Speak to the AI and get responses.""")

# Record audio
fs = 44100
st.warning("Press the button below to start recording.")

def record_audio(duration=5):
    st.info("Recording... Speak now!")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    return audio

if st.button("Record"):
    audio_data = record_audio()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        wavefile = wave.open(tmp_file.name, 'wb')
        wavefile.setnchannels(1)
        wavefile.setsampwidth(2)
        wavefile.setframerate(fs)
        wavefile.writeframes(audio_data)
        wavefile.close()
        st.success(f"Saved recording: {tmp_file.name}")

# Transcribe audio and generate text response (optional)
# Use Hugging Face API or any transcription service

# Page 3: Image Generation (pages/3_Image_Generation.py)
import streamlit as st
import requests

st.title("Image Generation")
st.markdown("""Generate images based on your description.""")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-v1"
headers = {"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"}

def generate_image(prompt):
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    return response.content

description = st.text_input("Enter a description for the image:")
if description:
    with st.spinner("Generating image..."):
        image_data = generate_image(description)
        st.image(image_data, caption=description)
