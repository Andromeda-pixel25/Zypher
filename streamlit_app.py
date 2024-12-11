import streamlit as st
import replicate
import os
import tempfile
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder

# App title
st.set_page_config(page_title="Zypher Chatbot")

# Replicate Credentials
with st.sidebar:
    st.title('Zypher 🦙Llama-2 Chatbot💬')
    st.write('This chatbot is created using the open-source Llama 2 LLM model from Meta.')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('API key already provided!', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api) == 40):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
    os.environ['REPLICATE_API_TOKEN'] = replicate_api

    st.subheader('Models and parameters')
    selected_model = st.sidebar.selectbox('Choose a Llama2 model', ['Llama2-7B', 'Llama2-13B'], key='selected_model')
    if selected_model == 'Llama2-7B':
        llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    elif selected_model == 'Llama2-13B':
        llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=1.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.sidebar.slider('max_length', min_value=20, max_value=80, value=50, step=5)
    st.markdown('Made By: Vedika')

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Function for generating LLaMA2 response. Refactored from https://github.com/a16z-infra/llama2-chatbot
def generate_llama2_response(prompt_input):
    string_dialogue = "You are a helpful assistant."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    output = replicate.run(llm, 
                           input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
                                  "temperature": temperature, "top_p": top_p, "max_length": max_length, "repetition_penalty": 1})
    return output

# Handle text input
if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)

# Handle voice input
st.markdown("---")
voice_input = st.button("Record Voice Input")
if voice_input:
    with st.spinner("Recording..."):
        mic_audio = mic_recorder()
        if mic_audio:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                temp_audio.write(mic_audio)
                temp_audio_path = temp_audio.name

            # Speech recognition
            recognizer = sr.Recognizer()
            with sr.AudioFile(temp_audio_path) as source:
                audio_data = recognizer.record(source)
            try:
                transcript = recognizer.recognize_google(audio_data)
                st.write("Transcribed Text:", transcript)
                st.session_state.messages.append({"role": "user", "content": transcript})

                # Generate response for voice input
                if transcript:
                    with st.chat_message("assistant"):
                        with st.spinner("Thinking..."):
                            response = generate_llama2_response(transcript)
                            placeholder = st.empty()
                            full_response = ''
                            for item in response:
                                full_response += item
                                placeholder.markdown(full_response)
                            placeholder.markdown(full_response)
                    message = {"role": "assistant", "content": full_response}
                    st.session_state.messages.append(message)

            except sr.UnknownValueError:
                st.error("Could not understand the audio. Please try again.")
            except sr.RequestError as e:
                st.error(f"Speech recognition error: {e}")
            finally:
                os.remove(temp_audio_path)
