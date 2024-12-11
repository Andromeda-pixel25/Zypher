import streamlit as st
import speech_recognition as sr
import tempfile
from audio_recorder_streamlit import audio_recorder

# App title
st.set_page_config(page_title="Zypher Chatbot")
st.title('Zypher Chatbot')
st.markdown("This chatbot leverages advanced AI for seamless conversations!")

# Sidebar configurations
st.sidebar.title("Zypher AI")
st.sidebar.markdown("Record your voice or type your query!")

# Chat history initialization
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Speech-to-text function
def process_audio(audio_file_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand that."
    except Exception as e:
        return f"Error: {e}"

# Handle voice input via audio recorder
st.markdown("### Record your voice:")
audio_bytes = audio_recorder()

if audio_bytes:
    # Save audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_bytes)
        audio_path = temp_audio.name

    # Process the audio and generate text
    with st.spinner("Processing your voice..."):
        transcript = process_audio(audio_path)

    # Display transcribed text
    if transcript:
        st.session_state["messages"].append({"role": "user", "content": transcript})
        with st.chat_message("user"):
            st.write(transcript)

# Text input for fallback
prompt = st.chat_input("Type your query...")
if prompt:
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate AI response
if st.session_state["messages"][-1]["role"] == "user":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = "This is a placeholder response. Replace with your AI logic."
            st.write(response)
    st.session_state["messages"].append({"role": "assistant", "content": response})
