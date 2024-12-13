# Page 2: Voice-based Chat (pages/Voice Chat.py)
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import requests
from gtts import gTTS
import os

st.title("🎤 Voice-based Chat")

st.markdown("""
### Instructions:
1. **Click 'Start Recording'** to record your voice.
2. Speak and then **stop recording**.
3. Get the transcription and hear the chatbot's response.
""")

# WebRTC Configuration
RTC_CONFIGURATION = {
    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
}

webrtc_ctx = webrtc_streamer(
    key="voice-chat",
    mode=WebRtcMode.SENDRECV,
    client_settings=ClientSettings(
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={"audio": True, "video": False},
    )
)

if webrtc_ctx and webrtc_ctx.audio_receiver:
    try:
        # Capture audio frames
        audio_frames = webrtc_ctx.audio_receiver.get_frames()
        if audio_frames:
            st.success("Audio captured successfully. Transcribing...")

            # Save captured audio
            audio_file_path = "recorded_audio.wav"
            with open(audio_file_path, "wb") as audio_file:
                audio_file.write(audio_frames[0].to_ndarray().tobytes())

            # Transcribe using Hugging Face API
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
            tts_audio_file = "response_audio.mp3"
            tts.save(tts_audio_file)
            st.audio(tts_audio_file, format="audio/mp3")

    except Exception as e:
        st.error(f"An error occurred while processing audio: {e}")
else:
    st.warning("WebRTC is not initialized. Ensure microphone access is granted.")
