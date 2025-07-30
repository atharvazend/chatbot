import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()       

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#Initialization to the gemini model 
model=genai.GenerativeModel("gemini-1.5-flash")

chat = model.start_chat(history=[])

# Initialize chat history in session state if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

def get_responce(text):
    chat = model.start_chat(history=st.session_state['chat_history'])
    response = chat.send_message(text, stream=True)
    return response

st.header("Gemini chatbot")

# Input and Send button at the bottom
input = st.text_input("Say something...", key="input")
submit = st.button("Get response", key="send_button")


if submit and input:
    response = get_responce(input)

    # Add user query to chat history
    st.session_state['chat_history'].append({"role": "user", "parts": [input]})

    full_response = ""
    for answer in response:
        full_response += answer.text
        st.write(answer.text)       # Display chunks as they arrive (streaming)

    # Add bot response to chat history
    st.session_state['chat_history'].append({"role": "model", "parts": [full_response]})

    



# Display chat history
st.subheader("Chat History:")
for message in st.session_state['chat_history']:
    if message["role"] == "user":
        st.markdown(f'**You:** {message['parts'][0]}')
    elif message["role"] == "model":
        st.markdown(f'**Bot:** {message['parts'][0]}')




if st.button("Clear Chat"):
    st.session_state.chat_history = []
    
