# client_page.py
import streamlit as st
import soundfile as sf
import audio_processing
from pydub import AudioSegment
from io import BytesIO
import numpy as np
import tensorflow as tf
import os

model = tf.keras.models.load_model('res2_model.h5')

emotion_emoji_dict = {
    'angry': '😠',
    'disgust': '🤢',
    'fear': '😨',
    'happy': '😊',
    'neutral': '😐',
    'sad': '😢',
    'surprise': '😲'
}

def predict_emotion(features):
    prediction = model.predict(features)
    emotion_index = np.argmax(prediction)
    print(emotion_index)
    emotion_label = audio_processing.classes[emotion_index]
    emotion_emoji = emotion_emoji_dict[emotion_label]
    return emotion_emoji

def read_messages(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            messages = file.readlines()[::2]

        return messages
    return []

def write_message(file_path, message):
    with open(file_path, 'a') as file:
        file.write(message + '\n')

def client_page():
    st.header("Client Page")

    # Audio upload and processing
    uploaded_file = st.file_uploader("Upload a voice clip", type=["wav", "mp3"])
    
    if uploaded_file is not None:
        st.session_state['audio_bytes'] = uploaded_file.read()
        st.audio(st.session_state['audio_bytes'], format='audio/wav')
        
        if uploaded_file.type == "audio/mp3":
            audio = AudioSegment.from_mp3(BytesIO(st.session_state['audio_bytes']))
            audio.export("temp.wav", format="wav")
            file_path = "temp.wav"
        else:
            file_path = uploaded_file.name

        features = audio_processing.get_features(file_path)
        st.session_state['emotion'] = predict_emotion(features)
        
    if st.button("Record using microphone"):
        st.info("Microphone recording feature to be added.")
        pass

    # Chat functionality
    st.subheader("Chat")
    chat_file = 'chat.txt'
    
    # Display chat messages
    messages = read_messages(chat_file)
    for msg in messages:
        st.write(msg)
    
    client_message = st.text_area("You:", key="client_message_area")
    
    i = 0
    if st.button("Send", key="send_client"):
        if client_message:
            if i == 0:
                write_message(chat_file, f"You: {client_message}")
                client_message = ""  # Clear text area after sending
        i += 1
    