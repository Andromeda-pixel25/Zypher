# Page 2: Voice-based Chat (pages/Voice Chat.py)
import streamlit as st
import streamlit.components.v1 as components
import requests
import base64

st.title("🎤 Voice-based Chat")

st.markdown("""
### Steps to Use:
1. Click **Start Recording** to record your voice.
2. Click **Stop Recording** to end the recording.
3. Submit your recording to get a transcription and response.
""")

# HTML and JavaScript for microphone recording
MIC_COMPONENT = """
<script>
    const recordButton = document.createElement("button");
    recordButton.innerText = "Start Recording";
    recordButton.style.background = "#4CAF50";
    recordButton.style.color = "white";
    recordButton.style.border = "none";
    recordButton.style.padding = "10px 20px";
    recordButton.style.cursor = "pointer";
    recordButton.style.margin = "10px 0";

    const stopButton = document.createElement("button");
    stopButton.innerText = "Stop Recording";
    stopButton.style.background = "#f44336";
    stopButton.style.color = "white";
    stopButton.style.border = "none";
    stopButton.style.padding = "10px 20px";
    stopButton.style.cursor = "pointer";
    stopButton.style.margin = "10px 0";
    stopButton.disabled = true;

    const audioContainer = document.createElement("div");

    let mediaRecorder;
    let audioChunks = [];

    recordButton.onclick = async () => {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            audioChunks = [];
            const reader = new FileReader();
            reader.readAsDataURL(audioBlob);
            reader.onloadend = () => {
                const audioBase64 = reader.result.split(",")[1];
                const inputField = document.getElementById("audio_data");
                inputField.value = audioBase64;
            };
        };

        mediaRecorder.start();
        recordButton.disabled = true;
        stopButton.disabled = false;
    };

    stopButton.onclick = () => {
        mediaRecorder.stop();
        recordButton.disabled = false;
        stopButton.disabled = true;
    };

    document.body.appendChild(recordButton);
    document.body.appendChild(stopButton);
    document.body.appendChild(audioContainer);
</script>
<input type="hidden" id="audio_data" />
"""
components.html(MIC_COMPONENT)

audio_data = st.text_input("Paste the recorded audio data (Base64) below after recording:", key="audio_input")

if st.button("Get Transcription and Response"):
    if audio_data:
        try:
            # Send the audio data for transcription
            transcription_response = requests.post(
                "https://api-inference.huggingface.co/models/openai/whisper-base",
                headers={"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"},
                json={"inputs": base64.b64decode(audio_data)}
            )

            transcription = transcription_response.json().get("text", "Could not transcribe audio.")
            st.write(f"**Transcription:** {transcription}")

            # Generate a response
            bot_response = requests.post(
                "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill",
                headers={"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"},
                json={"inputs": transcription}
            ).json().get("generated_text", "I couldn't generate a response.")

            st.write(f"**Bot Response:** {bot_response}")

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("No audio data available.")
