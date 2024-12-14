import streamlit as st
import speech_recognition as sr
import requests
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Title
st.title("🎤 Voice-based Chat")

# Initialize recognizer
recognizer = sr.Recognizer()

def record_audio():
    with sr.Microphone() as source:
        st.info("Recording... Speak now!")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            st.success("Recording complete!")
            return audio
        except sr.WaitTimeoutError:
            st.error("No speech detected. Try again.")
            return None

if st.button("Record Voice"):
    audio_data = record_audio()
    
    if audio_data:
        # Convert SpeechRecognition audio to WAV for processing
        st.info("Processing audio...")
        try:
            audio_bytes = audio_data.get_wav_data()
            headers = {"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"}

            # Send audio to Whisper API
            transcription_response = requests.post(
                "https://api-inference.huggingface.co/models/openai/whisper-large",
                headers=headers,
                files={"file": audio_bytes},
            )

            if transcription_response.status_code == 200:
                transcription_data = transcription_response.json()
                transcription = transcription_data.get("text", "Transcription failed.")
                st.write(f"**Transcription:** {transcription}")

                # Chatbot interaction
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
    st.warning("Click 'Record Voice' to start recording.")

