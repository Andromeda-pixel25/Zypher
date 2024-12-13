import streamlit as st
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load the GPT-2 model and tokenizer
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Set the title of the Streamlit app
st.title("\U0001F3A4 Voice-based Chat")

# Record voice input using st.audio_input
st.info("Click below to record your voice and interact with the chatbot.")
voice_input = st.audio_input("Record your voice")

# Ensure voice input is not empty
if voice_input:
    st.write("**Recorded Audio:**")
    st.audio(voice_input, format="audio/wav")

    if st.button("Transcribe & Get Response"):
        try:
            # Process the audio input (This is just a placeholder; you would use actual transcription)
            # Here you would integrate your audio transcription service
            transcription = "This is a sample transcription of the audio input."

            # Tokenize the transcription for the model
            inputs = tokenizer.encode(transcription, return_tensors="pt")

            # Generate a response from the model
            with torch.no_grad():
                outputs = model.generate(inputs, max_length=50)
            response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Display the response
            st.write(f"**Bot:** {response_text}")

        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    st.warning("No valid audio input detected. Please record your voice again.")
