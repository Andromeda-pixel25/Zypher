# Page 2: Voice-based Chat (pages/Voice Chat.py)
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import av
from gtts import gTTS
import tempfile

st.title("🎤 Voice-based Chat")

st.markdown("""
### Instructions:
1. Click **Start** to record your voice.
2. Speak and then **stop** the recording.
3. Get the transcription and hear the chatbot's response.
""")

# WebRTC Configuration
RTC_CONFIGURATION = {
    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
}


def audio_processor(frame: av.AudioFrame):
    """Processes the audio frame and saves it."""
    audio = frame.to_ndarray()
    return audio


webrtc_ctx = webrtc_streamer(
    key="voice-chat",
    mode=WebRtcMode.SENDRECV,
    client_settings=ClientSettings(
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={"audio": True, "video": False},
    ),
    audio_processor_factory=audio_processor,
)

if "audio_data" not in st.session_state:
    st.session_state.audio_data = None

if webrtc_ctx and webrtc_ctx.state.playing:
    st.info("Recording in progress... Speak now!")

    if webrtc_ctx.audio_receiver:
        try:
            # Capture audio data
            audio_frames = webrtc_ctx.audio_receiver.get_frames()
            for frame in audio_frames:
                audio_data = frame.to_ndarray()
                st.session_state.audio_data = audio_data
            st.success("Audio recorded successfully!")
        except Exception as e:
            st.error(f"Error capturing audio: {e}")
else:
    st.warning("WebRTC is not initialized. Ensure microphone access is granted.")

if st.session_state.audio_data is not None:
    # Save and Process Recorded Audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(st.session_state.audio_data.tobytes())
        audio_path = tmp_file.name

    st.audio(audio_path, format="audio/wav")

    # Convert Speech to Text
    st.info("Sending audio for transcription...")
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/openai/whisper-base",
            headers={"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"},
            files={"file": open(audio_path, "rb")},
        )
        transcription = response.json().get("text", "Could not transcribe audio.")
        st.write(f"**Transcription:** {transcription}")

        # Generate Chatbot Response
        chatbot_response = requests.post(
            "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill",
            headers={"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"},
            json={"inputs": transcription},
        ).json().get("generated_text", "Sorry, I couldn't understand that.")
        st.write(f"**Chatbot Response:** {chatbot_response}")

        # Convert Text to Speech
        tts = gTTS(chatbot_response)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
            tts.save(tmp_audio.name)
            st.audio(tmp_audio.name, format="audio/mp3")

    except Exception as e:
        st.error(f"An error occurred: {e}")
