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
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: #fff;
        padding: 10px;
        border-top: 1px solid #ddd;
        box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
    }
    .input-textbox {
        flex: 1;
        height: 40px;
        border-radius: 20px;
        padding: 10px;
        border: 1px solid #ccc;
    }
    .send-button, .image-button {
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 50%;
        padding: 10px;
        height: 40px;
        width: 40px;
        font-size: 18px;
        display: flex;
        justify-content: center;
        align-items: center;
        cursor: pointer;
    }
    .image-button {
        background-color: #ffc107;
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
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hello! How can I assist you today?"}
    ]

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

# Input Row (Textbox and Buttons)
col1, col2, col3 = st.columns([5, 1, 1])
with col1:
    user_input = st.text_input("", placeholder="Type a message...")
with col2:
    if st.button("Send", key="send_button"):
        if user_input:
            st.session_state["messages"].append({"role": "user", "content": user_input})
            with st.spinner("AI is thinking..."):
                response = generate_text_response(user_input)
                st.session_state["messages"].append({"role": "assistant", "content": response})
            st.experimental_rerun()
with col3:
    if st.button("Image", key="image_button"):
        if user_input:
            st.session_state["messages"].append({"role": "user", "content": user_input})
            with st.spinner("Generating image..."):
                image_url = generate_image(user_input)
                st.session_state["messages"].append({"role": "image", "content": image_url})
            st.experimental_rerun()

# Close Chat Container
st.markdown("</div>", unsafe_allow_html=True)
