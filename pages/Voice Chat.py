# Page 2: Voice-based Chat (pages/Voice Chat.py)
import streamlit as st
import streamlit.components.v1 as components
import requests

st.title("🎤 Voice-based Chat")

# WebRTC-based microphone recording component
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
            const audioUrl = URL.createObjectURL(audioBlob);
            const audio = new Audio(audioUrl);
            audioContainer.innerHTML = "";
            audioContainer.appendChild(audio);
            audio.controls = true;
            audio.play();

            const reader = new FileReader();
            reader.readAsDataURL(audioBlob);
            reader.onloadend = () => {
                const base64Audio = reader.result.split(",")[1];
                const audioInput = document.getElementById("audio_data");
                audioInput.value = base64Audio;
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
<input type="hidden" id="audio_data" name="audio_data" />
"""
components.html(MIC_COMPONENT)

# Transcription and response
if st.button("Get Transcription and Response"):
    audio_data = st.experimental_get_query_params().get("audio_data", [None])[0]
    if audio_data:
        response = requests.post(
            "https://api-inference.huggingface.co/models/openai/whisper-base",
            headers={"Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}"},
            data=audio_data,
        )
        try:
            response_data = response.json()
            transcription = response_data.get("text", "Could not transcribe audio.")
        except ValueError:
            transcription = "Error: Invalid response from transcription API."
        st.write(f"**Transcription:** {transcription}")
    else:
        st.error("No audio data available.")
