import streamlit as st
import openai
import pyttsx3
import base64
from streamlit.components.v1 import html

# Set OpenAI API Key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Text-to-Speech engine
engine = pyttsx3.init()

# Function: Text-to-Speech
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Function: OpenAI GPT Query
def generate_text_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}],
    )
    return response["choices"][0]["message"]["content"]

# Function: OpenAI DALL·E Query
def generate_image(prompt):
    response = openai.Image.create(prompt=prompt, n=1, size="512x512")
    return response["data"][0]["url"]

# Custom Speech Recorder with JavaScript
def record_audio():
    recorder_script = """
    <script>
        const recordButton = document.getElementById("recordButton");
        const stopButton = document.getElementById("stopButton");
        const audioText = document.getElementById("audioText");

        let mediaRecorder;
        let audioChunks = [];

        recordButton.onclick = async () => {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];

            mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = async () => {
                const blob = new Blob(audioChunks, { type: "audio/webm" });
                const reader = new FileReader();
                reader.onloadend = () => {
                    const base64String = reader.result.split(",")[1];
                    audioText.value = base64String;
                };
                reader.readAsDataURL(blob);
            };

            mediaRecorder.start();
        };

        stopButton.onclick = () => {
            mediaRecorder.stop();
        };
    </script>

    <div>
        <button id="recordButton">🎙️ Start Recording</button>
        <button id="stopButton">⏹️ Stop Recording</button>
        <input type="hidden" id="audioText" name="audioText" value="">
    </div>
    """
    return recorder_script

# Streamlit UI
st.set_page_config(page_title="AI Assistant", layout="wide")

# App Title
st.title("AI Assistant with Text, Speech, and Image Generation")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("🎨 Generate AI Images")
    image_prompt = st.text_input("Enter a prompt for an image:")
    if st.button("Generate Image"):
        if image_prompt:
            image_url = generate_image(image_prompt)
            st.image(image_url, caption="Generated Image", use_column_width=True)
        else:
            st.warning("Please enter an image prompt.")

# Chat Interface
st.header("💬 Chat with AI")
user_query = st.text_input("Enter your message:")
if st.button("Send"):
    if user_query:
        with st.spinner("Generating response..."):
            ai_response = generate_text_response(user_query)
            st.write("**AI:**", ai_response)
            if st.checkbox("🔊 Speak Response"):
                speak_text(ai_response)
    else:
        st.warning("Please enter a message.")

# Speech Input
st.header("🎙️ Voice Input")
st.markdown("Click the buttons below to record your voice.")
html(record_audio(), height=150)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by [Your Name]")
