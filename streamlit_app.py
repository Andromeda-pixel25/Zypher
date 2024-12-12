import streamlit as st
import os
import google.generativeai as genai
import pyttsx3
from audio_recorder_streamlit import audio_recorder
from streamlit_mic_recorder import speech_to_text

# Initialize Google Generative AI
genai.configure(api_key="AIzaSyA7V6N800cWrvaW2hlgHazi62i4Gh-idZk")
model = genai.GenerativeModel('gemini-pro')

# Initialize pyttsx3 for text-to-speech functionality
engine = pyttsx3.init()

# Title and intro
st.title("ZypherAi")
st.markdown("_________________________________________________________________________________")
st.markdown("Powered by Google Generative AI for Seamless Conversations")
image = "https://github.com/Andromeda-pixel25/smartbot-using-python/blob/main/letter-z%20(1).png?raw=true"
st.image(image)

# Text-to-Speech function
def speak(text):
    engine.say(text)  # Use the 'say' method correctly
    engine.runAndWait()

# Role conversion for display
def role_to_streamlit(role):
    if role == "model":
        return "assistant"
    else:
        return role

# Initialize chat history if not already in session state
if "messages" not in st.session_state:
    st.session_state.messages = model.start_chat(history=[])

# Display chat history
for message in st.session_state.messages.history:
    role = role_to_streamlit(getattr(message, "role"))
    text = ""
    parts = getattr(message, "parts", None)
    if parts:
        for part in parts:
            if hasattr(part, "text"):
                text = part.text
                break
    with st.chat_message(role):
        st.markdown(text)

# Text input and voice input components
prompt_text = st.chat_input("Ask away...")

# Record audio button in footer
footer_container = st.container()
with footer_container:
    audio_bytes = audio_recorder()

# Handle text input
if prompt_text:
    st.chat_message("user").markdown(prompt_text)
    response = st.session_state.messages.send_message(prompt_text)
    with st.chat_message("assistant"):
        st.markdown(response.text)
    speak(response.text)  # Speak the response

# Handle voice input
if audio_bytes:
    with st.spinner("Transcribing..."):
        # Write the audio bytes to a temporary file
        webm_file_path = "temp_audio.mp3"
        with open(webm_file_path, "wb") as f:
            f.write(audio_bytes)

        # Convert the audio to text using the speech_to_text function
        transcript = speech_to_text(webm_file_path)
        if transcript:
            # Send transcribed text as a message
            st.session_state.messages.send_message(transcript)
            with st.chat_message("user"):
                st.write(transcript)
            os.remove(webm_file_path)

            # Get the response and display it
            response = st.session_state.messages.send_message(transcript)
            with st.chat_message("assistant"):
                st.markdown(response.text)
            speak(response.text)  # Speak the response
        else:
            st.error("Could not transcribe the audio. Please try again.")
