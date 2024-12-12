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

# Function to process audio and transcribe it
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

# Function to generate AI response (placeholder logic)
def generate_ai_response(user_input):
    # Replace this logic with your AI model integration
    return f"AI Response to: {user_input}"

# Text input and voice recording in input area
input_container = st.container()
with input_container:
    cols = st.columns([8, 1, 1])  # Adjust column widths
    with cols[0]:
        prompt = st.text_input("Ask away...", key="text_input")
    with cols[1]:
        mic_clicked = st.button("🎤", key="mic_button")
    with cols[2]:
        send_clicked = st.button("➡️", key="send_button")

# Handle microphone input
if mic_clicked:
    st.info("Recording...")
    audio_bytes = audio_recorder()

    if audio_bytes:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(audio_bytes)
            audio_path = temp_audio.name

        # Process the audio and transcribe it
        with st.spinner("Transcribing your voice..."):
            transcript = process_audio(audio_path)

        # Add transcription to chat and generate a response
        if transcript:
            st.session_state["messages"].append({"role": "user", "content": transcript})
            with st.chat_message("user"):
                st.write(transcript)

            # Generate and display AI response
            response = generate_ai_response(transcript)
            st.session_state["messages"].append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.write(response)

# Handle text input submission
if send_clicked and prompt:
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate and display AI response
    response = generate_ai_response(prompt)
    st.session_state["messages"].append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)
