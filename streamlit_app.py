# Directory structure:
# - main.py
# - pages/
#     - 1_Text_Response.py
#     - 2_Voice_Response.py
#     - 3_Image_Generation.py

# Main app (main.py)
import streamlit as st

st.set_page_config(page_title="AI Chatbot", layout="wide")
st.title("Welcome to the AI Chatbot App")

st.markdown("""
This app provides the following features:
- **Text Response**: Chat with the AI using text input.
- **Voice Response**: Speak to the AI and get responses.
- **Image Generation**: Generate images based on your descriptions.

Use the sidebar to navigate between pages.
""")

# Page 1: Text Response (pages/1_Text_Response.py)
import streamlit as st
import requests

st.title("Text Response")
st.markdown("""Chat with AI using text input.""")

# Hugging Face API for text generation
API_URL = "https://api-inference.huggingface.co/models/gpt2"
headers = {"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

user_input = st.text_input("Ask a question:")
if user_input:
    with st.spinner("Generating response..."):
        output = query({"inputs": user_input})
        st.text_area("Response:", value=output["generated_text"], height=200)
