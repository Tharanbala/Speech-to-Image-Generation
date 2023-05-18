import requests
import base64
import streamlit as st

URL = "https://album-hr-colleges-paid.trycloudflare.com"
headers = {'Bypass-Tunnel-Reminder': "go",
           'mode': 'no-cors'}

def check_if_valid_backend(url):
    try:
        resp = requests.get(url, timeout=5, headers=headers)
        return resp.status_code == 200
    except requests.exceptions.Timeout:
        return False
    
def call_dalle(url, text):
    data = {"text": text}
    resp = requests.post(url + "/generate", headers=headers, json=data)
    if resp.status_code == 200:
        return resp
    
def create_and_show_images(text):
    valid = check_if_valid_backend(URL)
    if not valid:
        st.write("Backend service is not running")
    else:
        resp = call_dalle(URL, text)
        if resp is not None:
            data = resp.json()
            img_data = base64.b64decode(data['generatedImgs'][0])
            st.image(img_data)