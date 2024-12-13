import streamlit as st
import requests
import numpy as np
import torch
from transformers import QwenForCausalLM, QwenTokenizer
from io import BytesIO

# Load the Qwen model and tokenizer
model_name = "Qwen/Qwen2-Audio-7B-Instruct"
tokenizer = QwenTokenizer.from_pretrained(model_name)
model = QwenForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto")

# Set the title of the Streamlit app
st.title("\U0001F3A4 Voice-based Chat")

# Record voice input using st.audio_input
st.info("Click below to record your voice and interact with the chatbot.")
voice_input = st.audio_input("Record your voice")

# Ensure voice input is not empty
if voice_input is not None:
    st.write("**Recorded Audio:**")
    st.audio(voice_input, format="audio/wav")

    if st.button("Transcribe & Get Response"):
        try:
            # Get the raw audio data from the recorded audio
            audio_bytes = voice_input.getvalue()

            # Convert audio bytes to numpy array (if needed)
            audio_np = np.frombuffer(audio_bytes, dtype=np.float32)

            # Process the audio input using the Qwen model
            inputs = tokenizer(audio_np, return_tensors="pt", padding=True)

            # Generate a response from the model
            with torch.no_grad():
                outputs = model.generate(**inputs)
            response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Display the response
            st.write(f"**Bot:** {response_text}")

            # Optionally: Implement Text-to-Speech (TTS) here if desired
            # For TTS, you can use any compatible model or API

        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    st.warning("No valid audio input detected. Please record your voice again.")
