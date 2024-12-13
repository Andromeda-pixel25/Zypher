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
