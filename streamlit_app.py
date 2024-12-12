import streamlit as st
import openai
from streamlit.components.v1 import html

# Set OpenAI API Key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Function: OpenAI GPT Query
def generate_text_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": prompt}],
    )
    return response["choices"][0]["message"]["content"]

# Function: OpenAI Image Generation
def generate_image(prompt):
    response = openai.Image.create(prompt=prompt, n=1, size="512x512")
    return response["data"][0]["url"]

# Streamlit UI Configuration
st.set_page_config(page_title="ChatGPT-like Assistant", layout="wide")

# Custom CSS for layout
st.markdown(
    """
    <style>
    body {
        margin: 0;
        padding: 0;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        height: 95vh;
        margin: 0 auto;
        max-width: 800px;
        padding: 10px;
    }
    .messages-container {
        flex: 1;
        overflow-y: auto;
        padding-bottom: 20px;
    }
    .input-row {
        display: flex;
        align-items: center;
        gap: 10px;
        position: sticky;
        bottom: 0;
        background: #fff;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
    }
    .input-textbox {
        flex: 1;
        height: 50px;
        border-radius: 25px;
        padding: 10px;
        border: 1px solid #ccc;
    }
    .send-button, .mic-button, .image-button {
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 50%;
        padding: 10px;
        height: 50px;
        width: 50px;
        font-size: 18px;
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
    }
    .mic-button {
        background-color: #28a745;
    }
    .image-button {
        background-color: #ffc107;
    }
    .output-image {
        max-width: 100%;
        margin: 10px 0;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar Section
with st.sidebar:
    st.header("Chat Assistant")
    st.info("This is a ChatGPT-like interface with text and image generation functionality.")

# Chat Container
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# Session State for Messages
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]

# Display Messages
st.markdown("<div class='messages-container'>", unsafe_allow_html=True)
for message in st.session_state["messages"]:
    if message["role"] == "user":
        st.markdown(f"<div class='chat-box user-box'>{message['content']}</div>", unsafe_allow_html=True)
    elif message["role"] == "assistant":
        st.markdown(f"<div class='chat-box assistant-box'>{message['content']}</div>", unsafe_allow_html=True)
    elif message["role"] == "image":
        st.image(message["content"], use_column_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# Input Row (Custom HTML/JS)
st.markdown(
    """
    <div class='input-row'>
        <input id='text-input' class='input-textbox' type='text' placeholder='Type a message...' />
        <button id='send-button' class='send-button'>⮞</button>
        <button id='mic-button' class='mic-button'>🎙️</button>
        <button id='image-button' class='image-button'>🖼️</button>
    </div>
    """,
    unsafe_allow_html=True,
)

# JavaScript for Handling Input
custom_js = """
<script>
    const sendButton = document.getElementById('send-button');
    const micButton = document.getElementById('mic-button');
    const imageButton = document.getElementById('image-button');
    const textInput = document.getElementById('text-input');

    // Send Button Logic
    sendButton.addEventListener('click', () => {
        const message = textInput.value;
        if (message) {
            Streamlit.setComponentValue({"type": "text", "content": message});
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

    // Image Generation Button Logic
    imageButton.addEventListener('click', () => {
        const message = textInput.value;
        if (message) {
            Streamlit.setComponentValue({"type": "image", "content": message});
            textInput.value = '';  // Clear input after sending
        }
    });
</script>
"""
html(custom_js, height=0)

# Handle User Input
user_input = st.query_params.get("component_value")
if user_input:
    input_type = user_input.get("type")
    input_content = user_input.get("content")
    if input_type == "text":
        st.session_state["messages"].append({"role": "user", "content": input_content})
        with st.spinner("AI is thinking..."):
            response = generate_text_response(input_content)
            st.session_state["messages"].append({"role": "assistant", "content": response})
    elif input_type == "image":
        st.session_state["messages"].append({"role": "user", "content": input_content})
        with st.spinner("Generating image..."):
            image_url = generate_image(input_content)
            st.session_state["messages"].append({"role": "image", "content": image_url})
    st.experimental_rerun()

# Close Chat Container
st.markdown("</div>", unsafe_allow_html=True)
