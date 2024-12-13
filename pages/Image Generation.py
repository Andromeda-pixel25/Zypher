import streamlit as st
import requests

st.title("🎨 Image Generation")

prompt = st.text_input("Describe the image you want to generate:", key="image_gen_input")
if prompt:
    response = requests.post(
        "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2",
        headers={"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"},
        json={"inputs": prompt},
    )

    if response.status_code == 200:
        image_bytes = response.content
        st.image(image_bytes, caption=prompt, use_column_width=True)
    else:
        st.error("Failed to generate image. Please try again.")
