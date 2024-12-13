import streamlit as st
import torch
from transformers import WhisperForConditionalGeneration, WhisperProcessor, GPT2LMHeadModel, GPT2Tokenizer, EncoderDecoderCache
import numpy as np
import soundfile as sf
import io
from scipy.signal import resample

# Load the Whisper model and processor for transcription
whisper_model_name = "openai/whisper-large"
whisper_processor = WhisperProcessor.from_pretrained(whisper_model_name)
whisper_model = WhisperForConditionalGeneration.from_pretrained(whisper_model_name)

# Load the GPT-2 model and tokenizer for generating responses
gpt_model_name = "gpt2"
gpt_tokenizer = GPT2Tokenizer.from_pretrained(gpt_model_name)
gpt_model = GPT2LMHeadModel.from_pretrained(gpt_model_name)

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
            # Convert audio input to a format suitable for Whisper
            audio_bytes = voice_input.getvalue()
            audio_io = io.BytesIO(audio_bytes)
            audio_data, sample_rate = sf.read(audio_io)

            # Resample if the sample rate is not 16 kHz
            if sample_rate != 16000:
                num_samples = int(len(audio_data) * (16000 / sample_rate))
                audio_data = resample(audio_data, num_samples)
                sample_rate = 16000  # Set to 16 kHz

            # Use the Whisper processor to transcribe the audio with language set to English
            audio_input = whisper_processor(audio_data, return_tensors="pt", sampling_rate=16000)
            audio_input['language'] = 'en'  # Specify English for translation
            audio_input['attention_mask'] = (audio_input['input_ids'] != whisper_processor.pad_token_id).long()

            with torch.no_grad():
                generated_ids = whisper_model.generate(**audio_input)
            transcription = whisper_processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

            st.write(f"**Transcription:** {transcription}")

            # Tokenize the transcription for the GPT-2 model
            inputs = gpt_tokenizer.encode(transcription, return_tensors="pt")

            # Generate a response from the GPT-2 model
            with torch.no_grad():
                outputs = gpt_model.generate(inputs, max_length=50, pad_token_id=gpt_tokenizer.eos_token_id)
            response_text = gpt_tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Display the response
            st.write(f"**Bot:** {response_text}")

        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    st.warning("No valid audio input detected. Please record your voice again.")
