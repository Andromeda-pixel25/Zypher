# Zypher AI: Multipage App with Sidebar
import streamlit as st
import requests

# Configure Streamlit page
st.set_page_config(
    page_title="Zypher AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar Navigation
st.sidebar.title("Zypher AI Navigation")
page = st.sidebar.radio("Go to:", ["Text Response", "Voice Interaction", "Image Generation"])

if page == "Text Response":
    st.title("📝 Text Response")

    # Input for the user's text prompt
    prompt = st.text_input("Ask Zypher AI anything:")

    # Button to send the prompt
    if st.button("Get Response") and prompt:
        with st.spinner("Thinking..."):
            try:
                # Sending the prompt to Hugging Face Inference API
                model_url = "https://api-inference.huggingface.co/models/facebook/opt-350m"  # Lightweight model
                response = requests.post(
                    model_url,
                    headers={"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"},
                    json={"inputs": prompt},
                    timeout=60  # Set timeout to handle response delays
                )

                if response.status_code == 200:
                    # Parse and display the model's response
                    output = response.json()["generated_text"]
                    st.success("Response:")
                    st.write(output)
                elif response.status_code == 503:
                    st.warning("The model is loading. Please try again after a few seconds.")
                else:
                    st.error(f"Failed to fetch response. Error {response.status_code}: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")
    else:
        st.write("Enter a question above and click 'Get Response' to chat with Zypher AI!")

