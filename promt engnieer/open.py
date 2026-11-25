
import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load API Key
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

api_key = os.getenv("OPENAI_API_KEY")

# Page Configuration
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
.title {
    text-align: center;
    font-size: 40px;
    font-weight: bold;
    color: #00c6ff;
}
.subtitle {
    text-align: center;
    color: gray;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown(
    '<div class="title">🤖 Shubham AI Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Ask anything and get instant AI answers</div>',
    unsafe_allow_html=True
)

st.divider()

# Check API Key
if not api_key:
    st.error("API Key not found! Please check your .env file.")
    st.stop()

# OpenAI Client
client = OpenAI(api_key=api_key)

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")

    st.write("Model: GPT-6 Luna")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Powered by OpenAI API")
    st.caption("Developed by Shubham Gupta")

# Display Previous Messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
user_input = st.chat_input("Ask me anything...")

if user_input:

    # Display User Message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate AI Response
    with st.chat_message("assistant"):

        with st.spinner("AI is thinking..."):

            try:

                response = client.responses.create(
                    model="gpt-6-luna",
                    input=[
                        {
                            "role": "system",
                            "content": (
                                "You are a helpful AI assistant. "
                                "Answer questions clearly and accurately. "
                                "Use simple language and examples when useful."
                            )
                        },
                        *st.session_state.messages
                    ],
                    max_output_tokens=1000
                )

                answer = response.output_text

                st.markdown(answer)

                # Save AI Response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:

                st.error(f"API Error: {str(e)}")
