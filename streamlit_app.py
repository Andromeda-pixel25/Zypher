import streamlit as st
import os
import google.generativeai as genai
import pyttsx3
from streamlit_mic_recorder import mic_recorder, speech_to_text
from audio_recorder_streamlit import audio_recorder

# Initialize Google Generative AI
genai.configure(api_key="AIzaSyA7V6N800cWrvaW2hlgHazi62i4Gh-idZk")
model = genai.GenerativeModel('gemini-pro')

# Initialize messages
messages = model.start_chat()

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

st.title("ZypherAi")
st.markdown("_________________________________________________________________________________")
st.markdown("Powered by Google Generative AI for Seamless Conversations")
image = "https://github.com/Andromeda-pixel25/smartbot-using-python/blob/main/letter-z%20(1).png?raw=true"
st.image(image)

# Text to Speech function
def speak(text):
    engine.say(text)  # Use the 'say' method correctly
    engine.runAndWait()

# Mapping the role to streamlit format
def role_to_streamlit(role):
    if role == "model":
        return "assistant"
    else:
        return role

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    role = role_to_streamlit(message["role"])
    text = message["text"]
    with st.chat_message(role):
        st.markdown(text)

# Prompt and voice input
prompt_text = st.chat_input("Ask away...")
footer_container = st.container()
with footer_container:
    audio_bytes = audio_recorder()

# If user provides text input
if prompt_text:
    st.chat_message("user").markdown(prompt_text)
    response = model.send_message(prompt_text)
    st.session_state.messages.append({"role": "assistant", "text": response.text})
    with st.chat_message("assistant"):
        st.markdown(response.text)

# For voice input
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
            st.chat_message("user").markdown(transcript)
            response = model.send_message(transcript)
            st.session_state.messages.append({"role": "assistant", "text": response.text})
            with st.chat_message("assistant"):
                st.markdown(response.text)
            speak(response.text)  # Speak the response text
        else:
            st.error("Could not transcribe the audio. Please try again.")
        os.remove(webm_file_path)
