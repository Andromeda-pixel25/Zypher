# Page 2: Voice-based Chat (pages/Voice Chat.py)
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import requests
from gtts import gTTS
import os

st.title("🎤 Voice-based Chat")

st.markdown("""
### Steps to Use:
1. Click the **Start Recording** button to record your voice.
2. Stop recording and wait for the transcription.
3. Hear the bot's response spoken aloud.
""")

# WebRTC settings
webrtc_ctx = webrtc_streamer(
    key="voice-chat",
    mode=WebRtcMode.SENDRECV,
    client_settings=ClientSettings(
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        media_stream_constraints={"audio": True, "video": False},
    )
)

if webrtc_ctx.audio_receiver:
    audio_frames = webrtc_ctx.audio_receiver.get_frames()
    if audio_frames:
        st.success("Audio captured successfully. Transcribing...")

        # Save audio as WAV file
        audio_file_path = "recorded_audio.wav"
        with open(audio_file_path, "wb") as audio_file:
            audio_file.write(audio_frames[0].to_ndarray().tobytes())

        # Transcribe using Hugging Face Whisper model
        try:
            with open(audio_file_path, "rb") as f:
                transcription_response = requests.post(
                    "https://api-inference.huggingface.co/models/openai/whisper-base",
                    headers={"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"},
                    files={"file": f}
                )
            transcription = transcription_response.json().get("text", "Could not transcribe audio.")
            st.write(f"**Transcription:** {transcription}")

            # Generate chatbot response
            bot_response = requests.post(
                "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill",
                headers={"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"},
                json={"inputs": transcription}
            ).json().get("generated_text", "I couldn't generate a response.")
            st.write(f"**Bot Response:** {bot_response}")

            # Convert response to speech
            tts = gTTS(bot_response)
            tts.save("response_audio.mp3")
            st.audio("response_audio.mp3", format="audio/mp3")

        except Exception as e:
            st.error(f"An error occurred: {e}")
