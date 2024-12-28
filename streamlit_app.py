import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key="AIzaSyA7V6N800cWrvaW2hlgHazi62i4Gh-idZk")
model = genai.GenerativeModel('gemini-pro')

messages = model.start_chat()

st.title("ZypherAi")
st.write("____________________________________________________________________________________________")
st.markdown("Powered by Google Generative AI for Seamless Conversations")
image="https://github.com/Andromeda-pixel25/smartbot-using-python/blob/main/letter-z%20(1).png?raw=true"
st.logo(image,size="large")

def role_to_streamlit(role):
    if role == "model":
        return "assistant"
    else:
        return role
        
if "messages" not in st.session_state:
    st.session_state.messages = model.start_chat(history = [])
    
for message in st.session_state.messages.history:
    role = role_to_streamlit(getattr(message, "role"))
    text = ""
    parts = getattr(message, "parts", None) #none is specified to run even if nothing exists
    
    if parts:
        for part in parts:
            if hasattr(part, "text"): # Check if `text` attribute exists
                text = part.text
                break
            
# display the history
    with st.chat_message(role):
        st.markdown(text)

#input
prompt=st.chat_input("ask away..")
if prompt:
    st.chat_message("user").markdown(prompt)
    response = st.session_state.messages.send_message(prompt)
    with st.chat_message("assistant"):
        st.markdown(response.text)








