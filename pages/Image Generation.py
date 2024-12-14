# Page 3: Image Generation
import streamlit as st
import requests
from PIL import Image
import io
import time

st.title("🎨 Image Generation")

# Prompt input for the user
prompt = st.text_input("Describe the image you want to generate:")

# Button to trigger the API call
if st.button("Generate Image") and prompt:
    with st.spinner("Generating your image..."):
        try:
            model_url = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"  # Alternative model

            # API request to Hugging Face's stable diffusion model
            response = requests.post(
                model_url,
                headers={"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"},
                json={"inputs": prompt},
                timeout=60  # Set a timeout to handle long generation times
            )

            # Handle loading state for models
            if response.status_code == 503:
                st.warning("The model is currently loading. Retrying in 20 seconds...")
                time.sleep(20)
                response = requests.post(
                    model_url,
                    headers={"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"},
                    json={"inputs": prompt},
                    timeout=60
                )

            if response.status_code == 200:
                # Convert the response content to an image
                image_bytes = response.content
                image = Image.open(io.BytesIO(image_bytes))

                # Display the image with a caption
                st.image(image, caption=prompt, use_column_width=True)
            else:
                # Error handling for unsuccessful API requests
                st.error(f"Failed to generate image. Error {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            # Handle network or request issues
            st.error(f"An error occurred: {e}")
else:
    st.write("Enter a description above and click 'Generate Image' to create your artwork.")
