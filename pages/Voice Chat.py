import streamlit as st
import soundfile as sf
import io
import requests

# Set the title of the Streamlit app
st.title("🎤 Voice-based Chat")

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

            # Ensure the sample rate is 16 kHz for Whisper
            if sample_rate != 16000:
                st.warning("The audio sample rate must be 16 kHz. Please record again.")
            else:
                # Save the audio data to a temporary file
                temp_audio_file = "temp_audio.wav"
                sf.write(temp_audio_file, audio_data, sample_rate)

                # Transcribe audio using Hugging Face Whisper
                headers = {
                    "Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}",
                }
                with open(temp_audio_file, 'rb') as audio_file:
                    transcription_response = requests.post(
                        "https://api-inference.huggingface.co/models/openai/whisper-large",
                        headers=headers,
                        files={"file": audio_file},
                    )

                if transcription_response.status_code == 200:
                    transcription_data = transcription_response.json()
                    transcription = transcription_data.get("text", "Could not transcribe audio.")
                    st.write(f"**Transcription:** {transcription}")

                    # Chatbot response
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
    st.warning("No valid audio input detected. Please record your voice again.")
