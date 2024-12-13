# Main page (main.py)
import streamlit as st

st.set_page_config(
    page_title="Multi-Page Chatbot",
    page_icon="🤖",
    layout="wide",
)
import requests

st.title("Zypher Chat")

API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
HEADERS = {"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"}

def query(payload):
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    try:
        return response.json()
    except ValueError:
        return {"error": "Invalid JSON response from API."}

if "messages" not in st.session_state:
    st.session_state["messages"] = []

user_input = st.text_input("Ask me anything:", key="text_chat_input")
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    response = query({"inputs": user_input})
    if isinstance(response, dict) and "generated_text" in response:
        bot_reply = response["generated_text"]
    else:
        bot_reply = response.get("error", "I'm not sure how to respond to that.")
    st.session_state["messages"].append({"role": "bot", "content": bot_reply})

for message in st.session_state["messages"]:
    if message["role"] == "user":
        st.markdown(f"**You:** {message['content']}")
    else:
        st.markdown(f"**Bot:** {message['content']}")
