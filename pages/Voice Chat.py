import streamlit as st
import soundfile as sf
import io
import requests

st.title("🎤 Voice-based Chat")

# Record voice input
voice_input = st.audio_input("Record your voice")

if voice_input:
    st.audio(voice_input, format="audio/wav")
    if st.button("Transcribe & Chat"):
        try:
            # Convert audio to 16kHz
            audio_bytes = voice_input.getvalue()
            audio_io = io.BytesIO(audio_bytes)
            audio_data, sample_rate = sf.read(audio_io)

            if sample_rate != 16000:
                st.error("Audio must be 16kHz. Please record again.")
            else:
                # Save to temporary file
                temp_audio_file = "temp_audio.wav"
                sf.write(temp_audio_file, audio_data, sample_rate)

                # Transcription (Hugging Face Whisper)
                headers = {"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"}
                with open(temp_audio_file, 'rb') as audio_file:
                    transcription_response = requests.post(
                        "https://api-inference.huggingface.co/models/openai/whisper-large",
                        headers=headers,
                        files={"file": audio_file},
                    )

                if transcription_response.status_code == 200:
                    transcription_data = transcription_response.json()
                    transcription = transcription_data.get("text", "Transcription failed.")
                    st.write(f"**Transcription:** {transcription}")

                    # Chatbot (Hugging Face BlenderBot)
                    chatbot_response = requests.post(
                        "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill",
                        headers=headers,
                        json={"inputs": transcription},
                    )

                    if chatbot_response.status_code == 200:
                        chatbot_data = chatbot_response.json()
                        ai_reply = chatbot_data.get("generated_text", "No response.")
                        st.write(f"**Bot:** {ai_reply}")
                    else:
                        st.error(f"Chatbot failed: {chatbot_response.text}")
                else:
                    st.error(f"Transcription failed: {transcription_response.text}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    st.warning("No audio input detected.")
