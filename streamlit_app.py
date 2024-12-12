import streamlit as st
import openai
from streamlit_chat import message

# Configure the OpenAI API
openai.api_key = "your-api-key-here"

# Set page layout and styling
st.set_page_config(page_title="ChatGPT-like UI", layout="wide")

# Custom CSS for fixing the textbox at the bottom and styling the page
st.markdown(
    """
    <style>
        .stApp {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 100vh;
        }
        .chat-container {
            flex: 1;
            overflow-y: auto;
            padding-bottom: 100px;
        }
        .input-container {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background: #f9f9f9;
            border-top: 1px solid #ddd;
            padding: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .input-container input[type="text"] {
            flex: 1;
            padding: 10px;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        .input-container button {
            padding: 10px 15px;
            font-size: 16px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            background-color: #4CAF50;
            color: white;
        }
        .input-container button:hover {
            background-color: #45a049;
        }
        .icon-button {
            background: none;
            border: none;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .icon-button img {
            width: 24px;
            height: 24px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Session state to store chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Chat display container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for message_data in st.session_state.messages:
    message(message_data["content"], is_user=message_data["is_user"])
st.markdown('</div>', unsafe_allow_html=True)

# Input container at the bottom
st.markdown('<div class="input-container">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([8, 1, 1], gap="small")

with col1:
    user_input = st.text_input("", placeholder="Type your message here...", key="user_input")

with col2:
    send_button = st.button("Send")

with col3:
    mic_button = st.button("🎤")  # Placeholder for mic functionality
st.markdown('</div>', unsafe_allow_html=True)

# Handle user input
if send_button and user_input:
    # Append user message
    st.session_state.messages.append({"content": user_input, "is_user": True})

    # Call OpenAI API to get a response
    with st.spinner("ChatGPT is typing..."):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        reply = response.choices[0].message.content

    # Append bot response
    st.session_state.messages.append({"content": reply, "is_user": False})

    # Clear user input
    st.session_state.user_input = ""

if mic_button:
    st.warning("Mic functionality is under development.")
