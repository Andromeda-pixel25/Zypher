import streamlit as st
import os
import openai
from streamlit.components.v1 import html

# Set up OpenAI API keys
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Page configuration
st.set_page_config(page_title="Chatbot", layout="wide")

# Navigation Menu
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Text Chat", "Voice Chat", "Image Generator"])

# Common Styles
styles = """
<style>
body {
    font-family: Arial, sans-serif;
}
.chat-container {
    display: flex;
    flex-direction: column;
    height: 80vh;
    overflow-y: auto;
    margin-bottom: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 10px;
}
.chat-input {
    position: fixed;
    bottom: 20px;
    width: 80%;
    margin: 0 auto;
    display: flex;
    align-items: center;
}
.chat-input input {
    flex-grow: 1;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
    margin-right: 10px;
}
.chat-input button {
    padding: 10px;
    border-radius: 5px;
    border: none;
    background-color: #007bff;
    color: white;
    cursor: pointer;
}
.chat-input button:hover {
    background-color: #0056b3;
}
</style>
"""

# Page 1: Text Chat
if page == "Text Chat":
    st.title("Text Chat with ZypherAI")
    st.markdown(styles, unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = ["Assistant: How can I assist you today?"]

    # Chat history
    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for message in st.session_state.chat_history:
            st.markdown(f"{message}")
        st.markdown('</div>', unsafe_allow_html=True)

    # User input
    user_input = st.text_input("Type your message", "", key="text_chat_input")
    if st.button("Send"):
        st.session_state.chat_history.append(f"User: {user_input}")
        response = openai.Completion.create(
            model="gpt-4",  # Or use "gpt-3.5-turbo" for lower cost
            prompt=user_input,
            max_tokens=150
        )
        st.session_state.chat_history.append(f"Assistant: {response.choices[0].text.strip()}")

# Page 2: Voice Chat
elif page == "Voice Chat":
    st.title("Voice Chat with ZypherAI")
    st.markdown(styles, unsafe_allow_html=True)

    # Microphone functionality (using HTML5 and JavaScript to capture audio)
    def record_audio():
        """Record audio using JavaScript and HTML5."""
        audio_html = """
        <script>
        function startRecording() {
            navigator.mediaDevices.getUserMedia({ audio: true })
                .then(stream => {
                    const mediaRecorder = new MediaRecorder(stream);
                    mediaRecorder.start();
                    mediaRecorder.ondataavailable = e => {
                        const audioBlob = new Blob([e.data], { type: 'audio/wav' });
                        const audioUrl = URL.createObjectURL(audioBlob);
                        const audio = new Audio(audioUrl);
                        audio.play();
                    };
                })
                .catch(error => console.error("Error accessing the microphone:", error));
        }
        </script>
        <button onclick="startRecording()">Start Recording</button>
        """
        return audio_html

    st.markdown(record_audio(), unsafe_allow_html=True)

    # After recording, send audio for transcription
    if st.button("Transcribe Audio"):
        # You would implement actual audio processing here
        audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"])
        if audio_file:
            with st.spinner("Transcribing..."):
                # Upload audio to OpenAI's Whisper API for transcription
                audio = openai.Audio.transcribe(
                    model="whisper-1",
                    file=audio_file,
                    language="en"
                )
                st.write(f"Transcription: {audio['text']}")
                
                # Get assistant's response based on transcription
                response = openai.Completion.create(
                    model="gpt-4",
                    prompt=audio['text'],
                    max_tokens=150
                )
                st.write(f"Assistant: {response.choices[0].text.strip()}")

# Page 3: Image Generator
elif page == "Image Generator":
    st.title("Image Generator with DALL-E")
    st.markdown(styles, unsafe_allow_html=True)

    prompt = st.text_input("Describe the image you want to generate")
    if st.button("Generate Image"):
        with st.spinner("Creating your image..."):
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            image_url = response['data'][0]['url']
            st.image(image_url, caption="Generated Image")
