
import os
import streamlit as st
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

# LangSmith configuration
if LANGSMITH_API_KEY:
    os.environ["LANGSMITH_TRACING"] = "true"
    os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY
    os.environ["LANGSMITH_PROJECT"] = os.getenv(
        "LANGSMITH_PROJECT", "Gemini-AI-Chatbot"
    )

# Page configuration
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Simple CSS
st.markdown("""
<style>
.stApp {
    background-color: #f7f8fa;
}

.block-container {
    max-width: 850px;
    padding-top: 2rem;
}

.chat-title {
    text-align: center;
    font-size: 32px;
    font-weight: 700;
    color: #222;
}

.chat-subtitle {
    text-align: center;
    color: #777;
    margin-bottom: 25px;
}

[data-testid="stChatMessage"] {
    border-radius: 12px;
    padding: 12px;
}

[data-testid="stChatInput"] {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(
    '<div class="chat-title">🤖 AI Chatbot</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="chat-subtitle">Powered by Google Gemini</div>',
    unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    st.title("Settings")
    st.write("Model: Gemini 3.6 Flash")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Powered by LangChain and LangSmith")

# Validate API key
if not GOOGLE_API_KEY:
    st.error("GOOGLE_API_KEY not found. Please check your .env file.")
    st.stop()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize Gemini model
@st.cache_resource
def get_chain():
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.2,
        max_output_tokens=2048,
        max_retries=3,
        timeout=60
    )

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a helpful AI assistant. "
            "Explain concepts clearly and provide complete code "
            "when the user requests it."
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ])

    return prompt | llm | StrOutputParser()

chain = get_chain()

# Welcome message
if not st.session_state.messages:
    st.info("Hello! 👋 Ask me anything. I'm here to help you.")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:

    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare previous chat history
    chat_history = []

    for message in st.session_state.messages[:-1]:
        if message["role"] == "user":
            chat_history.append(
                HumanMessage(content=message["content"])
            )
        else:
            chat_history.append(
                AIMessage(content=message["content"])
            )

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = chain.invoke(
                    {
                        "input": user_input,
                        "chat_history": chat_history
                    },
                    config={
                        "run_name": "Gemini-AI-Chat",
                        "tags": ["Streamlit", "Gemini"]
                    }
                )

                st.markdown(response)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

            except Exception as e:
                st.error(f"Error: {str(e)}")
