import streamlit as st
import requests

def send_request(user_message:str, chat_history_messages:list) -> dict:
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    json_data = {
        'message': {
            'message': user_message,
        },
        'chat_history': {
            'messages': chat_history_messages,
        },
    }

    response = requests.post('http://127.0.0.1:8000/chat', headers=headers, json=json_data)
    return response.json()
st.set_page_config(page_title="Pharma Chatbot", page_icon="💊", layout="wide")
st.title("Pharma Chatbot 🤖💊")

if "messages" not in st.session_state:
    st.session_state.messages = []

if prompt := st.chat_input("What is up?"):
    
    response = send_request(prompt, st.session_state.messages)
    print(response["chat_history"]["messages"][-1]["content"])
    
    st.session_state.messages = response["chat_history"]["messages"]

with st.chat_message("assistant"):
        st.markdown("Hi there! 😊 *I’m your pharma chatbot,* here to answer your questions about medicines with accurate info from the **FDA API**, share links to **drugs.com** if available, and focus solely on medicines—*ask me anything!* 💊")

for message in st.session_state.messages:
    if message["role"] == "system": continue
    with st.chat_message(message["role"]):
        st.markdown(message["content"])