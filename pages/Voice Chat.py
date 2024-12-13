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

                # Debugging: Show the structure of the transcription data
                st.write("**Transcription Data Structure:**")
                st.json(transcription_data)

                # Ensure transcription_data is parsed correctly
                transcription = "Could not transcribe audio."
                
                if isinstance(transcription_data, dict) and "text" in transcription_data:
                    transcription = transcription_data["text"]
                
                st.write(f"**Transcription:** {transcription}")

                # Send transcription to chatbot model
                chatbot_response = requests.post(
                    "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill",
                    headers=headers,
                    json={"inputs": transcription},
                )

                # Debugging: Show the raw chatbot response
                st.write("**Chatbot API Raw Response:**")
                st.json(chatbot_response.json())

                if chatbot_response.status_code == 200:
                    chatbot_data = chatbot_response.json()
                    st.write("**Chatbot Data Structure:**")
                    st.json(chatbot_data)

                    if isinstance(chatbot_data, dict):
                        ai_reply = chatbot_data.get("generated_text", "No response.")
                    elif isinstance(chatbot_data, list) and len(chatbot_data) > 0:
                        ai_reply = chatbot_data[0].get("generated_text", "No response.")
                    else:
                        ai_reply = "Unexpected response structure."

                    st.write(f"**Bot:** {ai_reply}")

                    # Generate Text-to-Speech for the chatbot response
                    tts_response = requests.post(
                        "https://api-inference.huggingface.co/models/facebook/tts",
                        headers=headers,
                        json={"inputs": ai_reply},
                    )

                    # Debugging: Show the raw TTS response
                    st.write("**Text-to-Speech API Raw Response:**")
                    st.json(tts_response.json())

                    if tts_response.status_code == 200:
                        st.audio(tts_response.content, format="audio/wav")
                    else:
                        st.error(f"Could not generate voice response. Status Code: {tts_response.status_code}, Response: {tts_response.text}")
                else:
                    st.error("Failed to get chatbot response.")
            else:
                st.error("Failed to transcribe audio.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    st.warning("No valid audio input detected. Please record your voice again.")
