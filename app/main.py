import streamlit as st
import anthropic
from dotenv import load_dotenv
import os

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = st.secrets["SYSTEM_PROMPT"]

# Page configuration — must be first Streamlit call
st.set_page_config(
    page_title="Vaerdeg Performance AI",
    page_icon="⚡",
    layout="centered"
)

# Password protection
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown("## VAERDEG Performance AI")
        password = st.text_input("Access Code", type="password")
        if st.button("Enter"):
            if password == st.secrets["APP_PASSWORD"]:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid access code")
        st.stop()

check_password()

# Header
st.title("Vaerdeg")
st.caption("Performance Behavior AI - powered by Dr. Annemieke Griffin's methodology")

st.divider()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What's on your mind?"):

    # Add user message to history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from Vaerdeg AI
    with st.chat_message("assistant"):
        with st.spinner(""):
            response = client.messages.create(
                model="claude-sonnet-4-5",
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=st.session_state.messages
            )
            assistant_message = response.content[0].text
            st.markdown(assistant_message)

    # Add assistant response to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": assistant_message
    })