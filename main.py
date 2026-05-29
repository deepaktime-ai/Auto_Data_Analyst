import streamlit as st
import pandas as pd
from advanced_agent import AdvancedDataAgent

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Auto Data Analyst Agent",
    page_icon="📊",
    layout="wide"
)

# -------------------------------
# SESSION STATE INIT
# -------------------------------
if "agent" not in st.session_state:
    st.session_state.agent = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------------
# UI HEADER
# -------------------------------
st.title("📊 Auto Data Analyst Agent")
st.markdown("Ask questions about your data like a data analyst.")

# -------------------------------
# FILE UPLOAD
# -------------------------------
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

# -------------------------------
# LOAD AGENT
# -------------------------------
if uploaded_file is not None and st.session_state.agent is None:
    try:
        st.session_state.agent = AdvancedDataAgent(uploaded_file)
        st.success("✅ Dataset loaded successfully!")
    except Exception as e:
        st.error(f"❌ Error loading dataset: {e}")

# -------------------------------
# USER INPUT
# -------------------------------
if st.session_state.agent is not None:
    user_query = st.text_input("💬 Ask your question:")

    if user_query:
        response = st.session_state.agent.run(user_query)

        # Save chat
        st.session_state.chat_history.append(("user", user_query))
        st.session_state.chat_history.append(("agent", response))

# -------------------------------
# DISPLAY CHAT
# -------------------------------
for role, message in st.session_state.chat_history:
    if role == "user":
        st.markdown(f"**🧑 You:** {message}")
    else:
        # If it's a matplotlib figure
        if hasattr(message, "figure") or str(type(message)).startswith("<class 'matplotlib"):
            st.markdown("**🤖 Agent (Chart):**")
            st.pyplot(message)
        else:
            st.markdown(f"**🤖 Agent:** {message}")