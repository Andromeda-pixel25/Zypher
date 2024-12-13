import streamlit as st
import requests

st.title("\U0001F3A4 Voice-based Chat")

# Record Voice Input using st.audio_input
st.info("Click below to record your voice and interact with the chatbot.")
voice_input = st.audio_input("Record your voice")

# Ensure voice input is not empty
if voice_input:
    st.write("**Recorded Audio:**")
    st.audio(voice_input, format="audio/wav")

    if st.button("Transcribe & Get Response"):
        try:
            headers = {"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"}

            # Send audio to Hugging Face Whisper API for transcription
            transcription_response = requests.post(
                "https://api-inference.huggingface.co/models/openai/whisper-base",
                headers=headers,
                data=voice_input.getvalue(),
            )

            # Debugging: Display the raw response
            st.write("**Transcription API Raw Response:**")
            st.json(transcription_response.json())

            if transcription_response.status_code == 200:
                transcription_data = transcription_response.json()

                # Ensure transcription_data is parsed correctly
                transcription = "Could not transcribe audio."
                if isinstance(transcription_data, dict) and "text" in transcription_data:
                    transcription = transcription_data["text"]
                elif isinstance(transcription_data, list) and len(transcription_data) > 0:
                    # Check if the first element is a dictionary
                    if isinstance(transcription_data[0], dict) and "text" in transcription_data[0]:
                        transcription = transcription_data[0]["text"]
                    else:
                        transcription = str(transcription_data[0])  # Fallback in case of unexpected structure

                st.write(f"**Transcription:** {transcription}")

                # Send transcription to chatbot model
                chatbot_response = requests.post(
                    "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill",
                    headers=headers,
                    json={"inputs": transcription},
                )

                if chatbot_response.status_code == 200:
                    chatbot_data = chatbot_response.json()
                    ai_reply = chatbot_data.get("generated_text", "No response.")
                    st.write(f"**Bot:** {ai_reply}")

                    # Generate Text-to-Speech for the chatbot response
                    tts_response = requests.post(
                        "https://api-inference.huggingface.co/models/facebook/tts",
                        headers=headers,
                        json={"inputs": ai_reply},
                    )

                    if tts_response.status_code == 200:
                        st.audio(tts_response.content, format="audio/wav")
                    else:
                        st.error("Could not generate voice response.")
                else:
                    st.error("Failed to get chatbot response.")
            else:
                st.error("Failed to transcribe audio.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    st.warning("No valid audio input detected. Please record your voice again.")
