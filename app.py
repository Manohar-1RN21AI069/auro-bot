import streamlit as st
import requests
import time
from datetime import datetime

# App title and config
st.set_page_config(page_title="AURA - Chatbot", layout="centered")
st.title("🤖 AURA - Your AI Assistant")

# Sidebar for future features like history
st.sidebar.title("Chat Settings")
#st.sidebar.markdown("Model: **Zephyr-7B-Alpha**")

# === Branding ===
with st.sidebar:
    #st.image("logo.png", width=10)
    st.markdown("### 🚀 AURA")
    st.markdown("##### *Your Private AI Copilot*")
    st.markdown("---")

    # === Chat History Section ===
    st.markdown("#### 📜 Chat History")

    # Fake sessions for demo (you can populate from actual history later)
    sessions = {
        "Session 1": "2025-04-01 14:30",
        "Session 2": "2025-04-07 10:15",
        "Session 3": "2025-04-09 08:50"
    }

    search_query = st.text_input("🔍 Search chats")
    for name, ts in sessions.items():
        if search_query.lower() in name.lower():
            st.button(f"{name} — {ts}")

    st.markdown("---")

    # === Default Useful Features ===
    st.markdown("#### ⚙️ Quick Settings")
    st.toggle("🎙️ Enable Voice Input")
    st.toggle("📤 Auto Save Chats")
    st.slider("🧠 Token Limit", 100, 1024, 256)
    st.selectbox("💬 Response Style", ["Concise", "Balanced", "Detailed"])
    st.color_picker("🎨 Accent Color", "#00ADB5")

    st.markdown("---")

    # === Footer ===
    st.markdown("#### ℹ️ Info")
    st.markdown("*Version:* `v3.0-beta`")
    st.markdown("*Powered by:* `OpenAI`, `CTransformers`, `Zephyr-7B`")
    st.markdown("Made with ❤️ by **Manohar**")

    st.markdown("<br><br>", unsafe_allow_html=True)

# Session state to maintain chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Text input
user_input = st.chat_input("Say something...")

# When user sends a message
if user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Display assistant typing placeholder
    with st.chat_message("assistant"):
        with st.spinner("AURA is thinking..."):
            # API call to backend
            placeholder = st.empty()
            full_response = ""

            endpoint = "http://localhost:8000/chat"

            try:
                response = requests.post(endpoint, json={"message": user_input})
                if response.status_code == 200:
                    reply = response.json()["response"]
                else:
                    reply = "⚠️ Backend error! Try again later."
            except Exception as e:
                reply = f"🚫 Request failed: {str(e)}"

            for char in reply:
                full_response += char
                placeholder.markdown(full_response + "▌")
                time.sleep(0.02)

            placeholder.markdown(full_response)

    # Append assistant message
    st.session_state.messages.append({"role": "assistant", "content": reply})

