
import os
import base64
import json
import html
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
from openai import OpenAI


# =====================================================
# CONFIG
# =====================================================

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

ROBOT_IMAGE = BASE_DIR / "chatbot_robot.png"

st.set_page_config(
    page_title="Shubham AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

if not API_KEY:
    st.error("OPENAI_API_KEY missing. Please check your .env file.")
    st.stop()

client = OpenAI(api_key=API_KEY)


# =====================================================
# SESSION STATE
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "voice" not in st.session_state:
    st.session_state.voice = True

if "pending" not in st.session_state:
    st.session_state.pending = None

if "speak_now" not in st.session_state:
    st.session_state.speak_now = False

if "stop_now" not in st.session_state:
    st.session_state.stop_now = False


# =====================================================
# PREMIUM CSS
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root {
    color-scheme: dark;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 75% 5%, #29205a 0%, transparent 30%),
        radial-gradient(ellipse at 5% 50%, #102c48 0%, transparent 30%),
        #080d1a !important;
    color: #f8fafc !important;
}

/* Hide Streamlit header */

header[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* Main container */

.block-container {
    max-width: 1450px;
    padding-top: 1.5rem;
    padding-bottom: 7rem;
}

/* Sidebar */

[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#101a32,#0a1020) !important;
    border-right: 1px solid #283858;
}

[data-testid="stSidebar"] * {
    color: #dce5fa;
}

.brand {
    font-size: 28px;
    font-weight: 900;
    letter-spacing: 1px;
    background: linear-gradient(90deg,#60a5fa,#c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.brand-sub {
    color: #7f91b6;
    font-size: 10px;
    letter-spacing: 2px;
    margin-top: 5px;
}

/* Hero */

.hero {
    position: relative;
    overflow: hidden;
    padding: 35px 38px;
    border-radius: 25px;
    border: 1px solid #4d5590;
    background: linear-gradient(
        115deg,
        #172e59,
        #382363,
        #15294b
    );
    box-shadow: 0 15px 55px #0005;
    margin-bottom: 27px;
}

.hero:after {
    content: "";
    position: absolute;
    width: 240px;
    height: 240px;
    right: -50px;
    top: -100px;
    border-radius: 50%;
    background: #a78bfa;
    filter: blur(95px);
    opacity: .3;
}

.online {
    display: inline-block;
    padding: 8px 14px;
    border-radius: 30px;
    background: #103b35;
    border: 1px solid #28765f;
    color: #6ee7b7;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
}

.hero h1 {
    color: white;
    font-size: clamp(29px,4vw,45px);
    font-weight: 900;
    margin: 17px 0 8px;
}

.hero p {
    color: #cbd5e1;
    font-size: 15px;
    line-height: 1.8;
    margin: 0;
}

/* Cards */

.panel {
    background: linear-gradient(145deg,#162643,#171b3a);
    border: 1px solid #35466d;
    border-radius: 22px;
    padding: 20px;
    box-shadow: 0 12px 35px #0003;
}

.robot-heading {
    color: #b9c5ff;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    text-align: center;
    margin-bottom: 8px;
}

.welcome {
    min-height: 290px;
    background: linear-gradient(145deg,#1b2c50,#2a2050);
    border: 1px solid #545b9c;
    border-radius: 22px;
    padding: 27px;
    box-shadow: 0 12px 35px #0003;
}

.welcome h2 {
    font-size: 26px;
    color: white;
    font-weight: 800;
}

.welcome p {
    color: #cbd5e1;
    line-height: 1.9;
    font-size: 14px;
}

.welcome strong {
    color: #c4b5fd;
}

/* Status */

.status {
    color: #6ee7b7;
    background: #103b35;
    border: 1px solid #28765f;
    border-radius: 30px;
    display: inline-block;
    padding: 8px 13px;
    font-size: 11px;
    font-weight: 700;
}

/* Section titles */

.section-title {
    font-size: 20px;
    font-weight: 800;
    color: #eef2ff;
    margin: 28px 0 16px;
}

/* Feature cards */

.feature {
    padding: 20px 12px;
    min-height: 112px;
    border-radius: 17px;
    background: linear-gradient(145deg,#182949,#191b3c);
    border: 1px solid #35466d;
    text-align: center;
    transition: .25s;
}

.feature:hover {
    border-color: #a78bfa;
    transform: translateY(-5px);
    box-shadow: 0 10px 25px #0005;
}

.feature .emoji {
    font-size: 27px;
}

.feature .name {
    color: #e2e8f0;
    font-size: 12px;
    font-weight: 700;
    margin-top: 10px;
}

/* Chat bubbles */

[data-testid="stChatMessage"] {
    background: #172542 !important;
    border: 1px solid #34466e !important;
    border-radius: 18px !important;
    padding: 16px !important;
    margin-bottom: 12px;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    color: #edf2ff !important;
    line-height: 1.8;
}

/* Chat input */

[data-testid="stBottom"] {
    background: #080d1a !important;
    border-top: 1px solid #293858;
}

[data-testid="stBottom"] > div {
    background: #080d1a !important;
}

[data-testid="stChatInput"] {
    background: #151f38 !important;
    border: 1px solid #7464d5 !important;
    border-radius: 17px !important;
    box-shadow: 0 0 25px #6952d522;
}

[data-testid="stChatInput"] textarea {
    color: white !important;
    -webkit-text-fill-color: white !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #a0aecb !important;
    -webkit-text-fill-color: #a0aecb !important;
}

/* Buttons */

.stButton > button {
    border-radius: 12px !important;
    border: 1px solid #5966a3 !important;
    color: white !important;
    background: linear-gradient(120deg,#293d72,#49357f) !important;
    font-weight: 700 !important;
    transition: .2s;
}

.stButton > button:hover {
    border-color: #c4b5fd !important;
    box-shadow: 0 0 16px #8b5cf655;
    transform: translateY(-2px);
}

/* Divider */

hr {
    border-color: #293957 !important;
}

/* Footer */

.footer {
    text-align: center;
    padding: 35px 10px;
    color: #8494b5;
    font-size: 12px;
}

@media(max-width:768px) {
    .hero {
        padding: 23px;
    }

    .welcome {
        min-height: auto;
    }

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# ROBOT IMAGE + ANIMATION
# =====================================================

def show_robot():

    if not ROBOT_IMAGE.exists():
        st.warning("Place chatbot_robot.png inside the project folder.")
        return

    encoded = base64.b64encode(
        ROBOT_IMAGE.read_bytes()
    ).decode("utf-8")

    robot_page = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>

    * {{
        box-sizing: border-box;
    }}

    body {{
        margin: 0;
        background: transparent;
        overflow: hidden;
    }}

    .stage {{
        height: 310px;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
    }}

    .glow {{
        position: absolute;
        width: 230px;
        height: 230px;
        border-radius: 50%;
        background: radial-gradient(
            circle,
            #8b5cf688,
            #06b6d444,
            transparent 70%
        );
        animation: pulse 3s infinite alternate;
    }}

    .robot {{
        width: 245px;
        height: 285px;
        object-fit: contain;
        position: relative;
        z-index: 2;
        filter: drop-shadow(0 15px 18px #0009);
        animation: float 3s ease-in-out infinite;
    }}

    @keyframes float {{
        0%,100% {{
            transform: translateY(0) rotate(-2deg);
        }}
        50% {{
            transform: translateY(-17px) rotate(2deg);
        }}
    }}

    @keyframes pulse {{
        from {{
            transform: scale(.8);
            opacity: .5;
        }}
        to {{
            transform: scale(1.2);
            opacity: 1;
        }}
    }}

    </style>
    </head>

    <body>
        <div class="stage">
            <div class="glow"></div>
            <img class="robot"
                src="data:image/png;base64,{encoded}">
        </div>
    </body>
    </html>
    """

    components.html(
        robot_page,
        height=315,
        scrolling=False
    )


# =====================================================
# OPENAI CHATBOT
# =====================================================

def rag_query(query, history):

    system_prompt = """
    You are Shubham AI, a friendly intelligent robot assistant.

    Rules:
    - Answer questions on any topic.
    - Help with Python, Java, SQL, AI, ML and Data Science.
    - Explain concepts in simple language.
    - Provide complete code when requested.
    - Use examples and proper formatting.
    - Remember the conversation context.
    - Reply in the same language as the user.
    - Never invent facts.
    - Be professional and friendly.
    """

    messages = [
        {"role": "system", "content": system_prompt}
    ]

    for msg in history[-20:]:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    messages.append({
        "role": "user",
        "content": query
    })

    try:
        response = client.responses.create(
            model=MODEL,
            input=messages,
            max_output_tokens=1500
        )

        return response.output_text or "No response generated."

    except Exception as error:
        return f"API Error: {str(error)}"


# =====================================================
# VOICE
# =====================================================

def speak(text):

    safe_text = json.dumps(text)

    components.html(f"""
    <script>
    const msg = {safe_text};

    if (window.speechSynthesis) {{
        window.speechSynthesis.cancel();

        const speech = new SpeechSynthesisUtterance(msg);
        speech.lang = "en-IN";
        speech.rate = 0.95;
        speech.pitch = 1.1;

        window.speechSynthesis.speak(speech);
    }}
    </script>
    """, height=0)


def stop_speaking():

    components.html("""
    <script>
    if (window.speechSynthesis) {
        window.speechSynthesis.cancel();
    }
    </script>
    """, height=0)


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown(
        '<div class="brand">🤖 SHUBHAM AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="brand-sub">YOUR PERSONAL AI COMPANION</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### ⚙️ SETTINGS")

    st.session_state.voice = st.toggle(
        "🔊 Robot Voice",
        value=st.session_state.voice
    )

    st.divider()

    st.markdown("### 🟢 SYSTEM STATUS")
    st.success("AI Assistant Online")

    st.caption(f"Model: {MODEL}")

    st.divider()

    st.markdown("### 💬 CONVERSATION")

    if st.button("＋ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending = None
        st.rerun()

    st.markdown("### RECENT MESSAGES")

    user_messages = [
        x["content"]
        for x in st.session_state.messages
        if x["role"] == "user"
    ]

    if user_messages:
        for item in user_messages[-6:]:
            st.caption("👤 " + item[:45])
    else:
        st.caption("Your conversations will appear here.")

    st.divider()

    st.markdown("### 🧠 CAPABILITIES")
    st.caption("💻 Coding Assistant")
    st.caption("📊 Data Analytics")
    st.caption("🤖 Artificial Intelligence")
    st.caption("🧠 Machine Learning")
    st.caption("🎓 Interview Preparation")

    st.divider()

    st.caption("Developed with ❤️ by Shubham Gupta")


# =====================================================
# HERO
# =====================================================

st.markdown("""
<div class="hero">

    <div class="online">● SYSTEM ONLINE</div>

    <h1>Meet Your AI Companion.</h1>

    <p>
        Hello Shubham! I'm your intelligent robot assistant.
        Ask me anything and let's explore the future together.
    </p>

</div>
""", unsafe_allow_html=True)


# =====================================================
# ROBOT + WELCOME
# =====================================================

robot_col, welcome_col = st.columns(
    [1, 1.2],
    gap="large"
)

with robot_col:

    st.markdown('<div class="panel">', unsafe_allow_html=True)

    st.markdown(
        '<div class="robot-heading">✦ YOUR AI COMPANION ✦</div>',
        unsafe_allow_html=True
    )

    show_robot()

    st.markdown(
        '<div style="text-align:center;color:#a5b4fc;'
        'font-weight:700;">SHUBHAM AI ROBOT</div>',
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)


with welcome_col:

    st.markdown("""
    <div class="welcome">

        <h2>👋 Hello, Shubham!</h2>

        <p>
            I'm <b>Shubham AI</b>, your personal intelligent
            robot assistant.
        </p>

        <p>
            I can help you learn programming, solve problems,
            understand AI concepts, create exciting projects
            and prepare for technical interviews.
        </p>

        <p>
            <strong>✨ What would you like to explore today?</strong>
        </p>

        <div class="status">● READY TO ASSIST</div>

    </div>
    """, unsafe_allow_html=True)


# =====================================================
# FEATURE CARDS
# =====================================================

st.markdown(
    '<div class="section-title">✦ Explore AI Capabilities</div>',
    unsafe_allow_html=True
)

features = [
    ("💻", "Coding Assistant"),
    ("🧠", "AI & Machine Learning"),
    ("📊", "Data Analytics"),
    ("🎓", "Interview Preparation")
]

cols = st.columns(4)

for col, (emoji, name) in zip(cols, features):

    with col:
        st.markdown(f"""
        <div class="feature">
            <div class="emoji">{emoji}</div>
            <div class="name">{name}</div>
        </div>
        """, unsafe_allow_html=True)


# =====================================================
# CHAT AREA
# =====================================================

st.markdown(
    '<div class="section-title">💬 Chat With Your Robot</div>',
    unsafe_allow_html=True
)

if not st.session_state.messages:

    st.caption("Start a conversation with Shubham AI:")

    suggestions = [
        "Explain Machine Learning",
        "Teach me Python",
        "What is RAG?",
        "Create a Data Science project"
    ]

    cols = st.columns(4)

    for i, col in enumerate(cols):

        with col:
            if st.button(
                suggestions[i],
                key=f"suggest_{i}",
                use_container_width=True
            ):
                st.session_state.pending = suggestions[i]
                st.rerun()


# Display history

for message in st.session_state.messages:

    avatar = "🤖" if message["role"] == "assistant" else "👤"

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])


# =====================================================
# USER INPUT
# =====================================================

query = st.chat_input("Message Shubham AI... ✨")

if st.session_state.pending:
    query = st.session_state.pending
    st.session_state.pending = None


if query:

    previous_history = st.session_state.messages.copy()

    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    with st.chat_message("user", avatar="👤"):
        st.markdown(query)

    with st.chat_message("assistant", avatar="🤖"):

        with st.spinner("🤖 Shubham AI is thinking..."):

            answer = rag_query(query, previous_history)

            st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    st.rerun()


# =====================================================
# VOICE CONTROLS
# =====================================================

last_answer = next(
    (
        m["content"]
        for m in reversed(st.session_state.messages)
        if m["role"] == "assistant"
    ),
    None
)

if last_answer:

    st.divider()

    st.markdown("### 🔊 ROBOT VOICE")

    c1, c2 = st.columns(2)

    with c1:
        if st.button("▶ Speak Answer", use_container_width=True):
            st.session_state.speak_now = True
            st.rerun()

    with c2:
        if st.button("■ Stop Voice", use_container_width=True):
            st.session_state.stop_now = True
            st.rerun()

    if st.session_state.speak_now:

        st.session_state.speak_now = False

        if st.session_state.voice:
            speak(last_answer)
        else:
            st.info("Enable Robot Voice in Settings first.")

    if st.session_state.stop_now:

        st.session_state.stop_now = False
        stop_speaking()


# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<div class="footer">

    <div style="
        font-size:22px;
        font-weight:900;
        color:#a5b4fc;
    ">
        🤖 SHUBHAM AI
    </div>

    <p>Powered by Python • Streamlit • OpenAI</p>

    <p>Designed & Developed by Shubham Gupta ❤️</p>

</div>
""", unsafe_allow_html=True)
