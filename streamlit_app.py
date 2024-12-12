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

# Streamlit UI Configuration
st.set_page_config(page_title="ChatGPT-like Assistant", layout="wide")

# Custom CSS to move the input box to the bottom
st.markdown(
    """
    <style>
    .chat-container {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 90vh;
        margin: 0 auto;
        max-width: 800px;
        padding: 10px;
    }
    .messages-container {
        flex: 1;
        overflow-y: auto;
        margin-bottom: 20px;
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
    .send-button {
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
        display: flex;
        justify-content: center;
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar Section
with st.sidebar:
    st.header("Chat Assistant")
    st.info("This is a ChatGPT-like interface with a user-friendly layout.")

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
st.markdown("</div>", unsafe_allow_html=True)

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
html(custom_js, height=0)

# Handle User Input
message = st.experimental_get_query_params().get("component_value")
if message:
    st.session_state["messages"].append({"role": "user", "content": message})
    with st.spinner("AI is thinking..."):
        response = generate_text_response(message)
        st.session_state["messages"].append({"role": "assistant", "content": response})
        st.experimental_rerun()

# Close Chat Container
st.markdown("</div>", unsafe_allow_html=True)
