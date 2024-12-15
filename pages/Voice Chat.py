import streamlit as st
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
import torch
import numpy as np
import soundfile as sf
import io

# Title
st.title("🎤 Zypher Voice-to-Text Chatbot with Whisper")

# Load Whisper model and processor
@st.cache_resource
def load_whisper_models():
    processor = WhisperProcessor.from_pretrained("openai/whisper-small")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-small")
    return processor, model

# Load chatbot model
@st.cache_resource
def load_chatbot_model():
    tokenizer = BlenderbotTokenizer.from_pretrained("facebook/blenderbot-400M-distill")
    chatbot_model = BlenderbotForConditionalGeneration.from_pretrained("facebook/blenderbot-400M-distill")
    return tokenizer, chatbot_model

whisper_processor, whisper_model = load_whisper_models()
chatbot_tokenizer, chatbot_model = load_chatbot_model()

# Function to process audio
def process_audio(audio_bytes):
    try:
        audio_data, original_samplerate = sf.read(io.BytesIO(audio_bytes))
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)

        if original_samplerate != 16000:
            num_samples = int(len(audio_data) * 16000 / original_samplerate)
            audio_data = np.interp(np.linspace(0, len(audio_data), num_samples), np.arange(len(audio_data)), audio_data)

        audio_data = audio_data.astype(np.float32)
        return audio_data
    except Exception as e:
        st.error(f"Audio processing failed: {e}")
        return None

# Transcription function
def transcribe_audio(audio_data):
    try:
        inputs = whisper_processor(audio_data, sampling_rate=16000, return_tensors="pt", language="en")
        with torch.no_grad():
            predicted_ids = whisper_model.generate(inputs["input_features"])
        transcription = whisper_processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        return transcription
    except Exception as e:
        st.error(f"Transcription failed: {e}")
        return None

# Chatbot response generation
def get_chatbot_response(user_input):
    try:
        inputs = chatbot_tokenizer(user_input, return_tensors="pt")
        with torch.no_grad():
            generated_ids = chatbot_model.generate(**inputs)
        response = chatbot_tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return response
    except Exception as e:
        st.error(f"Chatbot response generation failed: {e}")
        return None

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Record audio input
st.info("Click below to record your voice and interact with the chatbot.")
audio_input = st.audio_input("Record your voice")

if audio_input:
    st.write("**Recorded Audio:**")
    st.audio(audio_input)

    if st.button("Transcribe & Get Response"):
        st.info("Processing audio...")

        audio_data = process_audio(audio_input.getvalue())
        if audio_data is None:
            st.error("Could not process the audio for transcription.")
            st.stop()

        st.info("Transcribing audio...")
        transcription = transcribe_audio(audio_data)
        if transcription:
            st.write(f"**You:** {transcription}")

            # Append user input to chat history
            st.session_state.chat_history.append(f"You: {transcription}")

            # Get response from the chatbot
            st.info("Generating response from chatbot...")
            chatbot_response = get_chatbot_response(transcription)
            if chatbot_response:
                # Format chatbot response for user assistant style
                formatted_response = f"**Assistant:** {chatbot_response}"
                st.write(formatted_response)

                # Append chatbot response to chat history
                st.session_state.chat_history.append(f"Assistant: {chatbot_response}")

            else:
                st.error("Failed to get chatbot response.")
        else:
            st.error("Failed to transcribe audio.")
else:
    st.warning("No valid audio input detected. Please record your voice again.")

# Display chat history
if st.session_state.chat_history:
    st.write("### Chat History:")
    for message in st.session_state.chat_history:
        st.write(message)
