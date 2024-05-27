# employee_page.py
import streamlit as st
import numpy as np
import tensorflow as tf
import soundfile as sf
import os


def read_messages(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            messages = file.readlines()[::2]
        return messages
    return []

def write_message(file_path, message):
    with open(file_path, 'a') as file:
        file.write(message + '\n')

def employee_page():
    st.header("Employee Page")
    
    if 'audio_bytes' in st.session_state:
        st.audio(st.session_state['audio_bytes'], format='audio/wav')
        if 'emotion' in st.session_state:
            t = st.markdown(f"<div style='font-size: 100px;'>{st.session_state['emotion']}</div>", unsafe_allow_html=True)
            # st.write(f"Predicted Emotion: {t}")    

    st.subheader("Chat")
    chat_file = 'chat.txt'
    
    # Display chat messages
    messages = read_messages(chat_file)
    for msg in messages:
        st.write(msg)
    
    employee_message = st.text_area("You:")
    
    if st.button("Send"):
        if employee_message:
            write_message(chat_file, f"Employee: {employee_message}")
            employee_message= ""  # Clear text area after sending
    