import streamlit as st
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq, AutoTokenizer, pipeline
import soundfile as sf
import numpy as np
import io
from scipy.signal import resample

st.title("🎤 Voice-to-Text Chatbot with Qwen")

# Model Details
TRANSCRIPTION_MODEL = "Qwen/Qwen2-Audio-7B-Instruct"
CHATBOT_MODEL = "Qwen/Qwen-7B-Chat"

@st.cache_resource
def load_models():
    try:
        # Load processor and transcription model
        processor = AutoProcessor.from_pretrained(TRANSCRIPTION_MODEL)
        transcription_model = AutoModelForSpeechSeq2Seq.from_pretrained(
            TRANSCRIPTION_MODEL,
            trust_remote_code=True  # Ensure custom configuration is loaded
        )

        # Load chatbot pipeline
        chatbot_pipeline = pipeline("text-generation", model=CHATBOT_MODEL, trust_remote_code=True)

        return processor, transcription_model, chatbot_pipeline
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None, None, None

processor, transcription_model, chatbot_pipeline = load_models()

if not processor or not transcription_model or not chatbot_pipeline:
    st.stop()

# Resample Audio
def resample_audio(audio_bytes):
    try:
        audio_data, original_samplerate = sf.read(io.BytesIO(audio_bytes))
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)
        if original_samplerate != 16000:
            num_samples = int(len(audio_data) * 16000 / original_samplerate)
            audio_data = resample(audio_data, num_samples)
        output_audio = io.BytesIO()
        sf.write(output_audio, audio_data, 16000, format="WAV")
        return output_audio.getvalue()
    except Exception as e:
        st.error(f"Audio processing failed: {e}")
        return None

# Transcribe Audio
def transcribe_audio(audio_bytes):
    try:
        inputs = processor(audio_bytes, sampling_rate=16000, return_tensors="pt")
        outputs = transcription_model.generate(input_ids=inputs["input_features"])
        transcription = processor.batch_decode(outputs, skip_special_tokens=True)[0]
        return transcription
    except Exception as e:
        st.error(f"Transcription failed: {e}")
        return None

# Chatbot Interaction
def get_chatbot_response(user_input):
    try:
        response = chatbot_pipeline(user_input, max_length=100)
        return response[0]["generated_text"]
    except Exception as e:
        st.error(f"Chatbot response failed: {e}")
        return None

# Voice Input
st.info("Click below to record your voice and interact with the chatbot.")
audio_input = st.audio_input("Record your voice")

if audio_input:
    st.write("**Recorded Audio:**")
    st.audio(audio_input, format="audio/wav")

    if st.button("Transcribe & Get Response"):
        audio_bytes_16khz = resample_audio(audio_input.getvalue())
        if not audio_bytes_16khz:
            st.error("Could not process the audio for transcription.")
            st.stop()

        # Transcribe
        transcription = transcribe_audio(audio_bytes_16khz)
        if transcription:
            st.write(f"**Transcription:** {transcription}")

            # Get chatbot response
            chatbot_response = get_chatbot_response(transcription)
            if chatbot_response:
                st.write(f"**Bot:** {chatbot_response}")
        else:
            st.error("Failed to transcribe audio.")
else:
    st.warning("No valid audio input detected. Please record your voice again.")
