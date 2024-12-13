import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import pyaudio
import wave
import requests

st.title("🎤 Voice-based Chat")

audio_value = st.audio_input("Record a voice message")

if audio_value:
    st.audio(audio_value)
if st.button("Transcribe & Get Response"):
            with audio_value as audio_file:
                audio_value = audio_file.read()
            headers = {"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"}
            response = requests.post(
                "https://api-inference.huggingface.co/models/openai/whisper-base",
                headers=headers,
                data=audio_value,
            )

            if response.status_code == 200:
                transcription = response.json().get("text", "Could not transcribe audio.")
                st.write(f"**Transcription:** {transcription}")

                # Get AI Response
                chatbot_response = requests.post(
                    "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill",
                    headers=headers,
                    json={"inputs": transcription},
                )
                if chatbot_response.status_code == 200:
                    ai_reply = chatbot_response.json().get("generated_text", "No response.")
                    st.write(f"**Bot:** {ai_reply}")
                    # Text-to-Speech Response
                    st.info("Reading out the response...")
                    tts_response = requests.post(
                        "https://api-inference.huggingface.co/models/facebook/tts",
                        headers=headers,
                        json={"inputs": ai_reply},
                    )
                    if tts_response.status_code == 200:
                        st.audio(tts_response.content, format="audio/wav")
                    else:
                        st.error("Could not generate voice response.")
                else:
                    st.error("Failed to get chatbot response.")
            else:
                st.error("Failed to transcribe audio.")

# # Streamlit-webrtc for real-time voice input
# webrtc_ctx = webrtc_streamer(
#     key="voice",
#     mode=WebRtcMode.SENDRECV,
#     rtc_configuration={
#         "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
#     },
#     media_stream_constraints={"audio": True, "video": False},
# )

# # Recording and Transcription
# if "recording" not in st.session_state:
#     st.session_state["recording"] = False

# if webrtc_ctx.audio_receiver:
#     audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
#     if audio_frames:
#         if not st.session_state["recording"]:
#             st.session_state["recording"] = True
#             st.info("Recording... Speak now!")

#         # Save audio frames to a buffer
#         wf = wave.open("output.wav", "wb")
#         wf.setnchannels(1)
#         wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
#         wf.setframerate(44100)
#         for audio_frame in audio_frames:
#             wf.writeframes(audio_frame.to_ndarray().tobytes())
#         wf.close()

#         # Display Transcription
#         if st.button("Transcribe & Get Response"):
#             with open("output.wav", "rb") as audio_file:
#                 audio_data = audio_file.read()
#             headers = {"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"}
#             response = requests.post(
#                 "https://api-inference.huggingface.co/models/openai/whisper-base",
#                 headers=headers,
#                 data=audio_data,
#             )

#             if response.status_code == 200:
#                 transcription = response.json().get("text", "Could not transcribe audio.")
#                 st.write(f"**Transcription:** {transcription}")

#                 # Get AI Response
#                 chatbot_response = requests.post(
#                     "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill",
#                     headers=headers,
#                     json={"inputs": transcription},
#                 )
#                 if chatbot_response.status_code == 200:
#                     ai_reply = chatbot_response.json().get("generated_text", "No response.")
#                     st.write(f"**Bot:** {ai_reply}")
#                     # Text-to-Speech Response
#                     st.info("Reading out the response...")
#                     tts_response = requests.post(
#                         "https://api-inference.huggingface.co/models/facebook/tts",
#                         headers=headers,
#                         json={"inputs": ai_reply},
#                     )
#                     if tts_response.status_code == 200:
#                         st.audio(tts_response.content, format="audio/wav")
#                     else:
#                         st.error("Could not generate voice response.")
#                 else:
#                     st.error("Failed to get chatbot response.")
#             else:
#                 st.error("Failed to transcribe audio.")
