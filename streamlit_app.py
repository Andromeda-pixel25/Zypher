import streamlit as st
import speech_recognition as sr
import tempfile

# App title
st.set_page_config(page_title="Zypher Chatbot")
st.title("Zypher Chatbot")
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
def record_and_transcribe():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak now.")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            st.success("Recording complete. Transcribing...")
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand that."
        except Exception as e:
            return f"Error: {e}"

# Function to generate AI response (placeholder logic)
def generate_ai_response(user_input):
    # Replace this logic with your AI model integration
    return f"AI Response to: {user_input}"

# Input container
input_container = st.container()
with input_container:
    cols = st.columns([10, 1, 1])  # Adjust column widths
    user_input = cols[0].text_input("Type your message...", key="text_input", label_visibility="collapsed")
    mic_button = cols[1].button("🎙️", key="mic_button")
    send_button = cols[2].button("➡️", key="send_button")

# Voice recording and transcription prompt (above the text box)
if mic_button:
    with st.spinner("Recording..."):
        transcript = record_and_transcribe()

    if transcript:
        # Add transcription to chat and generate a response
        st.session_state["messages"].append({"role": "user", "content": transcript})
        with st.chat_message("user"):
            st.write(transcript)

        # Generate and display AI response
        response = generate_ai_response(transcript)
        st.session_state["messages"].append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

# Handle text input submission
if send_button and user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Generate and display AI response
    response = generate_ai_response(user_input)
    st.session_state["messages"].append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)
