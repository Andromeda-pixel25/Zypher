import streamlit as st
import openai
import pyttsx3
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

# Streamlit UI Configuration
st.set_page_config(page_title="ChatGPT-like Assistant", layout="wide")

# JavaScript for Handling Input
custom_js = """
<script>
    const sendButton = document.getElementById('send-button');
    const micButton = document.getElementById('mic-button');
    const textInput = document.getElementById('text-input');

    // Send Button Logic
    sendButton.addEventListener('click', () => {
        const message = textInput.value;
        if (message) {
            Streamlit.setComponentValue(message);
            textInput.value = '';  // Clear input after sending
        }
    });

    // Enter Key to Send
    textInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendButton.click();
        }
    });
</script>
"""

# Chat Style Layout
st.markdown(
    """
    <style>
    .chat-box { 
        background: #f7f8fc; 
        border-radius: 10px; 
        padding: 10px; 
        margin: 5px 0; 
        width: fit-content; 
    }
    .user-box { 
        background: #dcf8c6; 
        border-radius: 10px; 
        padding: 10px; 
        margin: 5px 0; 
        width: fit-content; 
        align-self: flex-end;
    }
    .assistant-box { 
        background: #eeeeee; 
        border-radius: 10px; 
        padding: 10px; 
        margin: 5px 0; 
        width: fit-content; 
        align-self: flex-start;
    }
    .input-row {
        display: flex; 
        align-items: center; 
        gap: 10px;
        margin-top: 10px;
    }
    .input-textbox {
        flex: 1;
        height: 50px;
        border-radius: 25px;
        padding: 10px;
        border: 1px solid #ccc;
    }
    .send-button {
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 50%;
        padding: 10px;
        height: 50px;
        width: 50px;
        font-size: 18px;
    }
    .mic-button {
        background-color: #28a745;
        color: white;
        border: none;
        border-radius: 50%;
        padding: 10px;
        height: 50px;
        width: 50px;
        font-size: 18px;
    }
    .sidebar-header {
        font-size: 18px;
        font-weight: bold;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar Section
with st.sidebar:
    st.markdown("<div class='sidebar-header'>🎨 Generate Images</div>", unsafe_allow_html=True)
    image_prompt = st.text_input("Enter image prompt:")
    if st.button("Generate Image"):
        if image_prompt:
            image_url = generate_image(image_prompt)
            st.image(image_url, caption="Generated Image", use_column_width=True)
        else:
            st.warning("Please enter a prompt!")

# Chat Area
st.markdown("<h2>💬 Chat with AI</h2>", unsafe_allow_html=True)

# Session State to Store Chat History
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]

# Display Messages
for message in st.session_state["messages"]:
    if message["role"] == "user":
        st.markdown(f"<div class='chat-box user-box'>{message['content']}</div>", unsafe_allow_html=True)
    elif message["role"] == "assistant":
        st.markdown(f"<div class='chat-box assistant-box'>{message['content']}</div>", unsafe_allow_html=True)

# Input Row (Custom HTML/JS)
st.markdown(
    """
    <div class='input-row'>
        <input id='text-input' class='input-textbox' type='text' placeholder='Type a message...' />
        <button id='send-button' class='send-button'>⮞</button>
        <button id='mic-button' class='mic-button'>🎙️</button>
    </div>
    """,
    unsafe_allow_html=True,
)

# JavaScript Recorder
html(custom_js, height=0)

# Handle User Input
message = st.query_params().get("component_value")
if message:
    st.session_state["messages"].append({"role": "user", "content": message})
    with st.spinner("AI is thinking..."):
        response = generate_text_response(message)
        st.session_state["messages"].append({"role": "assistant", "content": response})
        st.experimental_rerun()
