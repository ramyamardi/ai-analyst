import streamlit as st

st.set_page_config(
    page_title="AI Analyst",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #666;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        border-left: 4px solid #667eea;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
    }
    .stButton > button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
    }
    .chat-message-user {
        background: #e8f4fd;
        border-radius: 12px 12px 4px 12px;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #667eea;
    }
    .chat-message-ai {
        background: #f0f7ee;
        border-radius: 12px 12px 12px 4px;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #4caf50;
    }
    div[data-testid="stSidebarNav"] { display: none; }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown("## 🤖 AI Analyst")
    st.markdown("---")
    
    page = st.radio(
        "Navigate",
        ["🏠 Home", "📂 Upload & Explore", "💬 Chat with Data", "📊 Auto Charts", "🧹 Data Cleaning", "📋 Summary Report"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    if "df" in st.session_state and st.session_state.df is not None:
        df = st.session_state.df
        st.success(f"✅ Dataset loaded")
        st.caption(f"📄 {st.session_state.get('filename', 'data.csv')}")
        st.caption(f"🔢 {df.shape[0]:,} rows × {df.shape[1]} cols")
    else:
        st.info("📂 No dataset loaded yet.\nGo to Upload & Explore first.")
    
    st.markdown("---")
    st.caption("Built with Claude API · Streamlit · Pandas")

# Page routing
if page == "🏠 Home":
    from pages import home
    home.show()
elif page == "📂 Upload & Explore":
    from pages import upload
    upload.show()
elif page == "💬 Chat with Data":
    from pages import chat
    chat.show()
elif page == "📊 Auto Charts":
    from pages import charts
    charts.show()
elif page == "🧹 Data Cleaning":
    from pages import cleaning
    cleaning.show()
elif page == "📋 Summary Report":
    from pages import report
    report.show()
