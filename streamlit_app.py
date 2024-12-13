# Main page (main.py)
import streamlit as st

st.set_page_config(
    page_title="Multi-Page Chatbot",
    page_icon="🤖",
    layout="wide",
)

st.title("Welcome to the Multi-Page Chatbot")
st.markdown("""
### Available Features:
1. **Text-based Chat**: Interact with a chatbot powered by Hugging Face API.
2. **Voice-based Chat**: Speak to the chatbot and hear responses.
3. **Image Generation**: Generate images using Hugging Face's DALL-E.

Use the navigation menu on the left to explore.
""")

# Page 1: Text-based Chat (pages/Text Chat.py)
import streamlit as st
import requests

st.title("💬 Text-based Chat")

# Hugging Face API setup
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
HEADERS = {"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"}

def query(payload):
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json()

if "messages" not in st.session_state:
    st.session_state["messages"] = []

user_input = st.text_input("Ask me anything:", key="text_chat_input")
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    response = query({"inputs": user_input})
    bot_reply = response.get("generated_text", "I'm not sure how to respond to that.")
    st.session_state["messages"].append({"role": "bot", "content": bot_reply})

for message in st.session_state["messages"]:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    else:
        st.markdown(f"**Bot:** {message['content']}")

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
    transcription = response.json().get("text", "Could not transcribe audio.")
    st.write(f"**Transcription:** {transcription}")

# Page 3: Image Generation (pages/Image Generation.py)
import streamlit as st
import requests

st.title("🎨 Image Generation")

prompt = st.text_input("Describe the image you want to generate:", key="image_gen_input")
if prompt:
    response = requests.post(
        "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2",
        headers={"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"},
        json={"inputs": prompt},
    )

    if response.status_code == 200:
        image_bytes = response.content
        st.image(image_bytes, caption=prompt, use_column_width=True)
    else:
        st.error("Failed to generate image. Please try again.")
