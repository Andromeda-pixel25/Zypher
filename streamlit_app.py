# Main page (main.py)
import streamlit as st

st.set_page_config(
    page_title="Multi-Page Chatbot",
    page_icon="🤖",
    layout="wide",
)

st.title("Welcome to the Multi-Page Chatbot")
st.markdown("""
### Available Features:
1. **Text-based Chat**: Interact with a chatbot powered by Hugging Face API.
2. **Voice-based Chat**: Speak to the chatbot and hear responses.
3. **Image Generation**: Generate images using Hugging Face's DALL-E.

Use the navigation menu on the left to explore.
""")

# Page 1: Text-based Chat (pages/Text Chat.py)
import streamlit as st
import requests

st.title("💬 Text-based Chat")

# Hugging Face API setup
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
HEADERS = {"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"}

def query(payload):
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    return response.json()

if "messages" not in st.session_state:
    st.session_state["messages"] = []

user_input = st.text_input("Ask me anything:", key="text_chat_input")
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    response = query({"inputs": user_input})
    bot_reply = response.get("generated_text", "I'm not sure how to respond to that.")
    st.session_state["messages"].append({"role": "bot", "content": bot_reply})

for message in st.session_state["messages"]:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    else:
        st.markdown(f"**Bot:** {message['content']}")
