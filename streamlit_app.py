# Zypher AI: Multipage App with Sidebar
import streamlit as st
import requests
import time

st.logo(
    "letter-z (1).png",
    size="large"
)

# Configure Streamlit page
st.set_page_config(
    page_title="Zypher AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Text input using st.chat_input
prompt = st.chat_input("Ask Zypher AI anything:")

model_url = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"

if prompt:
    with st.spinner("Thinking..."):
        try:
            while True:  # Retry loop
                response = requests.post(
                    model_url,
                    headers={"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"},
                    json={"inputs": prompt},
                    timeout=60  # Timeout to handle delays
                )

                if response.status_code == 200:
                    # Successful response
                    result = response.json()
                    output = result["generated_text"] if isinstance(result, dict) else result[0].get("generated_text", "No response text found.")
                    st.chat_message("assistant").write(output)
                    break
                elif response.status_code == 503:
                    # Model is loading; retry after estimated time
                    error_data = response.json()
                    wait_time = error_data.get("estimated_time", 10)  # Default to 10 seconds if not provided
                    st.warning(f"The model is loading. Retrying in {int(wait_time)} seconds...")
                    time.sleep(wait_time)
                else:
                    st.error(f"Failed to fetch response. Error {response.status_code}: {response.text}")
                    break
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")




