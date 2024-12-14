# Page 3: Image Generation
import streamlit as st
import requests
from PIL import Image
import io
import time

st.title("🎨 Image Generation")

# Prompt input for the user
prompt = st.text_input("Describe the image you want to generate:")

# Cooldown mechanism to prevent excessive requests
if "last_request_time" not in st.session_state:
    st.session_state.last_request_time = 0
cooldown_period = 60  # in seconds

# Button to trigger the API call
if st.button("Generate Image") and prompt:
    current_time = time.time()
    time_since_last_request = current_time - st.session_state.last_request_time

    if time_since_last_request < cooldown_period:
        st.warning(f"Please wait {int(cooldown_period - time_since_last_request)} seconds before making another request.")
    else:
        with st.spinner("Generating your image..."):
            try:
                model_url = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"  # More reliable model
                response = requests.post(
                    model_url,
                    headers={"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"},
                    json={"inputs": prompt},
                    timeout=60  # Set a timeout to handle long generation times
                )

                if response.status_code == 200:
                    # Convert the response content to an image
                    image_bytes = response.content
                    image = Image.open(io.BytesIO(image_bytes))

                    # Display the image with a caption
                    st.image(image, caption=prompt, use_column_width=True)
                    st.session_state.last_request_time = current_time  # Update last request time
                elif response.status_code == 429:
                    st.error("Rate limit exceeded. Please wait a minute before trying again.")
                elif response.status_code == 503:
                    error_data = response.json()
                    wait_time = error_data.get("estimated_time", 20)
                    st.warning(f"The model is currently loading. Retrying in {int(wait_time)} seconds...")
                    time.sleep(wait_time)
                else:
                    # Handle other errors
                    st.error(f"Failed to generate image. Error {response.status_code}: {response.text}")
            except requests.exceptions.RequestException as e:
                # Handle network or request issues
                st.error(f"An error occurred: {e}")
else:
    st.write("Enter a description above and click 'Generate Image' to create your artwork.")
