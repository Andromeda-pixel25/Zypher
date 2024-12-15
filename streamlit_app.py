import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import requests
import wave
import pyaudio

st.title("🎤 Voice-based Chat")

# WebRTC for real-time audio input
webrtc_ctx = webrtc_streamer(
    key="voice",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    },
    media_stream_constraints={"audio": True, "video": False},
)

# Recording and Transcription
if "recording" not in st.session_state:
    st.session_state["recording"] = False

if webrtc_ctx.audio_receiver:
    audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
    if audio_frames:
        if not st.session_state["recording"]:
            st.session_state["recording"] = True
            st.info("Recording... Speak now!")

        # Save audio to file
        with wave.open("output.wav", "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            for audio_frame in audio_frames:
                wf.writeframes(audio_frame.to_ndarray().tobytes())

        # Transcription and Response
        if st.button("Transcribe & Get Response"):
            with open("output.wav", "rb") as audio_file:
                audio_data = audio_file.read()

            # Transcription
            transcription_response = requests.post(
                "https://api-inference.huggingface.co/models/openai/whisper-base",
                headers={"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"},
                data=audio_data,
            )

            try:
                transcription_data = transcription_response.json()
                if isinstance(transcription_data, list):
                    transcription = transcription_data[0].get("text", "Could not transcribe audio.")
                else:
                    transcription = transcription_data.get("text", "Could not transcribe audio.")
                st.write(f"**Transcription:** {transcription}")
            except ValueError:
                st.error("Failed to process transcription response.")

            # Chatbot Response
            chatbot_response = requests.post(
                "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill",
                headers={"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"},
                json={"inputs": transcription},
            )

            try:
                chatbot_data = chatbot_response.json()
                if isinstance(chatbot_data, list):
                    bot_reply = chatbot_data[0].get("generated_text", "No response.")
                else:
                    bot_reply = chatbot_data.get("generated_text", "No response.")
                st.write(f"**Bot:** {bot_reply}")
            except ValueError:
                st.error("Failed to process chatbot response.")

            # Text-to-Speech Response
            tts_response = requests.post(
                "https://api-inference.huggingface.co/models/facebook/tts",
                headers={"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"},
                json={"inputs": bot_reply},
            )

            if tts_response.status_code == 200:
                st.audio(tts_response.content, format="audio/wav")
            else:
                st.error("Failed to generate voice output.")
