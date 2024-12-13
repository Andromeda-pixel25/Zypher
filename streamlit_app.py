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
