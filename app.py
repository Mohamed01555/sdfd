# app.py
import streamlit as st
from client_page import client_page
from employee_page import employee_page
import base64

page_bg_img = 'Pattern 2023-12-03 19_34_49.png'

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

set_png_as_page_bg(page_bg_img)

st.title("Speech Emotion Recognition Chat Web App")



tabs = st.tabs(["Client Page", "Employee Page"])



with tabs[0]:
    client_page()

with tabs[1]:
    employee_page()
