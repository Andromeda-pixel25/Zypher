# Zypher AI: Multipage App with Sidebar
import streamlit as st
import requests
import time

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

    # Chat input for the user's text prompt
    user_input = st.chat_input("Ask Zypher AI anything:")

    # Display chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for message in st.session_state.chat_history:
        role, content = message
        if role == "user":
            st.chat_message("user").write(content)
        else:
            st.chat_message("assistant").write(content)

    if user_input:
        # Display the user's message in chat
        st.chat_message("user").write(user_input)
        st.session_state.chat_history.append(("user", user_input))

        with st.spinner("Thinking..."):
            try:
                # Sending the prompt to Hugging Face Inference API
                model_url = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"  # A good conversational model
                response = requests.post(
                    model_url,
                    headers={"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"},
                    json={"inputs": user_input},
                    timeout=60  # Set timeout to handle response delays
                )

                if response.status_code == 200:
                    # Parse and display the model's response
                    output = response.json()[0]["generated_text"]  # Adjusted to access the first element of the list
                    st.chat_message("assistant").write(output)
                    st.session_state.chat_history.append(("assistant", output))
                elif response.status_code == 503:
                    error_data = response.json()
                    wait_time = error_data.get("estimated_time", 10)  # Default to 10 seconds if not provided
                    st.warning(f"The model is loading. Retrying in {int(wait_time)} seconds...")
                    time.sleep(wait_time)
                else:
                    st.error(f"Failed to fetch response. Error {response.status_code}: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"An error occurred: {e}")

elif page == "Voice Interaction":
    st.title("🎙️ Voice Interaction")
    st.write("This feature is under development.")

elif page == "Image Generation":
    st.title("🎨 Image Generation")
    st.write("This feature is under development.")
