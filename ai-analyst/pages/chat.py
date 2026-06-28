import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.claude_api import chat_with_data


def show():
    st.markdown("## 💬 Chat with Your Data")
    st.markdown("Ask anything about your dataset in plain English.")

    if "df" not in st.session_state or st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset first. Go to **Upload & Explore**.")
        return

    df = st.session_state.df

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Suggested questions
    st.markdown("### 💡 Try these questions")
    cols = st.columns(3)
    suggestions = [
        "What is the overall summary of this dataset?",
        "Which column has the most missing values?",
        "What are the top 5 rows by the highest value?",
        "Are there any obvious patterns or trends?",
        "What is the average of all numeric columns?",
        "How many unique values does each column have?",
    ]
    for i, suggestion in enumerate(suggestions):
        with cols[i % 3]:
            if st.button(suggestion, key=f"sugg_{i}", use_container_width=True):
                st.session_state.pending_question = suggestion

    st.markdown("---")

    # Chat history display
    if st.session_state.chat_history:
        st.markdown("### 🗨️ Conversation")
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="chat-message-user">
                    <strong>You:</strong><br>{msg["content"]}
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message-ai">
                    <strong>🤖 AI Analyst:</strong><br>{msg["content"]}
                </div>""", unsafe_allow_html=True)
        
        if st.button("🗑️ Clear conversation"):
            st.session_state.chat_history = []
            st.rerun()

    st.markdown("---")

    # Input area
    default_q = st.session_state.pop("pending_question", "")
    question = st.text_area(
        "Ask a question about your data",
        value=default_q,
        placeholder="e.g. What is the average sales by region? Which product has the highest profit?",
        height=80
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        ask_btn = st.button("Ask ✨", use_container_width=True)

    if ask_btn and question.strip():
        with st.spinner("🤔 Analyzing your data..."):
            try:
                answer = chat_with_data(question.strip(), df, st.session_state.chat_history)
                st.session_state.chat_history.append({"role": "user", "content": question.strip()})
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
    elif ask_btn:
        st.warning("Please type a question first.")
