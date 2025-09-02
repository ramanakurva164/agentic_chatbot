import streamlit as st
# from agents import MasterAgent
from agents import MasterAgent  # Update this path if MasterAgent is defined elsewhere
import os
import time
from datetime import datetime

# ✅ Configure Streamlit
st.set_page_config(page_title="Multi-Agent Chatbot", page_icon="🤖", layout="wide")

# ✅ Initialize Agent
@st.cache_resource
def get_master_agent():
    return MasterAgent()

# ✅ Custom CSS for better message alignment
st.markdown("""
<style>
.user-message {
    display: flex;
    justify-content: flex-end;
    margin: 10px 0;
}

.user-bubble {
    background: #dcf8c6;
    color: black;
    padding: 10px 15px;
    border-radius: 18px;
    border-bottom-right-radius: 5px;
    max-width: 70%;
    word-wrap: break-word;
    box-shadow: 0 1px 2px rgba(0,0,0,0.1);
}

.bot-message {
    display: flex;
    justify-content: flex-start;
    margin: 10px 0;
}

.bot-bubble {
    background: #ffffff;
    color: black;
    padding: 10px 15px;
    border-radius: 18px;
    border-bottom-left-radius: 5px;
    max-width: 70%;
    word-wrap: break-word;
    box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    border: 1px solid #e5e5ea;
}

.stApp {
    background: black;
}

.main .block-container {
    background: #e5ddd5;
    padding-top: 2rem;
}

/* Sidebar styling */
.sidebar .sidebar-content {
    background: #075e54;
}

.sidebar .stButton > button {
    width: 100%;
    background: #25d366;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px;
    margin: 5px 0;
}

.sidebar .stButton > button:hover {
    background: #128c7e;
}

.sidebar .stDownloadButton > button {
    width: 100%;
    background: #17a2b8;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px;
    margin: 5px 0;
}

.sidebar .stDownloadButton > button:hover {
    background: #138496;
}

/* Hide default chat elements to prevent duplication */
.stChatMessage {
    display: none !important;
}
.input-container {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: #f8f9fa;
    padding: 15px 20px;
    border-top: 1px solid #ddd;
    box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
    z-index: 1000;
}
</style>
""", unsafe_allow_html=True)

# ✅ Initialize session state FIRST
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "ai", "content": "Hello 👋 I'm your assistant. Ask me anything!"}
    ]

if "master_agent" not in st.session_state:
    st.session_state.master_agent = get_master_agent()

# ✅ Sidebar controls
with st.sidebar:
    st.header("🎛️ Chat Controls")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat", type="primary"):
        st.session_state.messages = [
            {"role": "ai", "content": "Hello 👋 I'm your assistant. Ask me anything!"}
        ]
        st.rerun()
    
    # Export/Download chat
    if len(st.session_state.messages) > 1:
        # Prepare chat content for download
        chat_content = ""
        for msg in st.session_state.messages:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sender = "You" if msg["role"] == "user" else "Assistant"
            chat_content += f"[{timestamp}] {sender}: {msg['content']}\n\n"
        
        st.download_button(
            label="💾 Download Chat",
            data=chat_content,
            file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
    else:
        st.info("No chat history to download")
    
    st.divider()
    
    

# ✅ Main chat area
st.title("🤖 Multi-Agent Conversational Assistant")

# ✅ Create a container for messages (SINGLE DISPLAY)
message_container = st.container()

# ✅ Display messages ONCE
with message_container:
    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            # User message - aligned to right
            st.markdown(
                f"""
                <div class="user-message">
                    <div class="user-bubble">{msg["content"]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            # Bot message - aligned to left
            st.markdown(
                f"""
                <div class="bot-message">
                    <div class="bot-bubble">{msg["content"]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

# ✅ Chat input - USE FORM to prevent immediate submission
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([8, 1])
    
    with col1:
        user_input = st.text_input(
            "Message", 
            placeholder="Type your message...",
            label_visibility="collapsed",
            key="user_input_form"
        )
    
    with col2:
        submit_button = st.form_submit_button("➤")

# ✅ Process input ONLY when form is submitted
if submit_button and user_input and user_input.strip():
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input.strip()})
    
    # Get AI response
    try:
        response = st.session_state.master_agent.route(user_input.strip())
        
        # Handle None response
        if response is None:
            ai_reply = "Sorry, I couldn't process your request. Please try again."
        elif isinstance(response, str):
            ai_reply = response
        else:
            ai_reply = str(response)
    except Exception as e:
        ai_reply = f"⚠️ Error: {str(e)}"
    
    # Add AI response
    st.session_state.messages.append({"role": "ai", "content": ai_reply})
    
    # Single rerun
    st.rerun()

# ✅ Add auto-scroll script
st.markdown("""
<script>
function scrollToBottom() {
    window.scrollTo(0, document.body.scrollHeight);
}
setTimeout(scrollToBottom, 100);
</script>
""", unsafe_allow_html=True)
