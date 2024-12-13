# Page 2: Voice-based Chat (pages/Voice Chat.py)
import streamlit as st
import requests
import io
import base64

st.title("🎤 Voice-based Chat")

st.markdown("""
### Steps to Use:
1. Use the **Record Audio** button to upload your voice recording.
2. Submit your recording to get a transcription and response.
""")

# Audio input using st.audio
audio_file = st.file_uploader("Record or upload an audio file (WAV format recommended):", type=["wav"])

if st.button("Get Transcription and Response"):
    if audio_file:
        # Convert uploaded audio file to bytes
        audio_bytes = audio_file.read()

        # Send the audio bytes to the transcription API
        try:
            transcription_response = requests.post(
                "https://api-inference.huggingface.co/models/openai/whisper-base",
                headers={"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"},
                files={"file": audio_bytes}
            )

            transcription = transcription_response.json().get("text", "Could not transcribe audio.")
            st.write(f"**Transcription:** {transcription}")

            # Generate a response from the bot
            bot_response = requests.post(
                "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill",
                headers={"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"},
                json={"inputs": transcription}
            ).json().get("generated_text", "I couldn't generate a response.")

            st.write(f"**Bot Response:** {bot_response}")

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please upload an audio file.")
