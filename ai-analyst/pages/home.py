import streamlit as st


def show():
    st.markdown('<p class="main-header">🤖 AI Analyst</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Your intelligent data exploration companion — powered by Claude AI</p>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div style="background:#f0f4ff;border-radius:12px;padding:1.2rem;text-align:center;border:1px solid #c7d2fe;">
            <div style="font-size:2rem;">📂</div>
            <div style="font-weight:600;margin-top:0.5rem;">Upload CSV</div>
            <div style="color:#666;font-size:0.85rem;margin-top:0.3rem;">Drag & drop any CSV file</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background:#f0fff4;border-radius:12px;padding:1.2rem;text-align:center;border:1px solid #bbf7d0;">
            <div style="font-size:2rem;">💬</div>
            <div style="font-weight:600;margin-top:0.5rem;">Chat with Data</div>
            <div style="color:#666;font-size:0.85rem;margin-top:0.3rem;">Ask questions in plain English</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="background:#fff7f0;border-radius:12px;padding:1.2rem;text-align:center;border:1px solid #fed7aa;">
            <div style="font-size:2rem;">📊</div>
            <div style="font-weight:600;margin-top:0.5rem;">Auto Charts</div>
            <div style="color:#666;font-size:0.85rem;margin-top:0.3rem;">AI-generated visualizations</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div style="background:#fdf0ff;border-radius:12px;padding:1.2rem;text-align:center;border:1px solid #e9d5ff;">
            <div style="font-size:2rem;">📋</div>
            <div style="font-weight:600;margin-top:0.5rem;">Smart Report</div>
            <div style="color:#666;font-size:0.85rem;margin-top:0.3rem;">Full AI summary report</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 1])
    with col_a:
        st.markdown("### 🚀 How to get started")
        st.markdown("""
1. **Upload & Explore** — Load your CSV file and see an instant overview
2. **Chat with Data** — Ask "What is the average sales?" or "Which region performed best?"
3. **Auto Charts** — Claude picks the best visualizations for your data
4. **Data Cleaning** — Fix missing values, duplicates, and formatting in one click
5. **Summary Report** — Get a full AI-written analysis ready to share
        """)

    with col_b:
        st.markdown("### 💡 Example questions you can ask")
        questions = [
            "What is the trend over time?",
            "Which category has the highest value?",
            "Are there any outliers in the data?",
            "Summarize the key findings.",
            "What are the top 5 performing products?",
            "Is there a correlation between X and Y?",
        ]
        for q in questions:
            st.markdown(f"• *\"{q}\"*")

    st.markdown("---")
    st.markdown("### 🎯 Quick Start — Try a Sample Dataset")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📦 Load Sales Data", use_container_width=True):
            import pandas as pd
            import numpy as np
            np.random.seed(42)
            n = 200
            df = pd.DataFrame({
                "date": pd.date_range("2024-01-01", periods=n, freq="D").astype(str),
                "product": np.random.choice(["Laptop", "Phone", "Tablet", "Watch", "Earbuds"], n),
                "region": np.random.choice(["North", "South", "East", "West"], n),
                "sales": np.random.randint(500, 5000, n),
                "units": np.random.randint(1, 50, n),
                "profit": np.random.randint(50, 1500, n),
                "customer_rating": np.round(np.random.uniform(3.0, 5.0, n), 1),
            })
            st.session_state.df = df
            st.session_state.filename = "sample_sales.csv"
            st.success("✅ Sample sales dataset loaded! Navigate to any page to explore.")

    with col2:
        if st.button("👥 Load HR Data", use_container_width=True):
            import pandas as pd
            import numpy as np
            np.random.seed(7)
            n = 150
            df = pd.DataFrame({
                "employee_id": range(1001, 1001 + n),
                "department": np.random.choice(["Engineering", "Sales", "HR", "Marketing", "Finance"], n),
                "experience_years": np.random.randint(1, 20, n),
                "salary": np.random.randint(30000, 120000, n),
                "performance_score": np.round(np.random.uniform(2.5, 5.0, n), 1),
                "gender": np.random.choice(["Male", "Female"], n),
                "attrition": np.random.choice(["Yes", "No"], n, p=[0.2, 0.8]),
            })
            st.session_state.df = df
            st.session_state.filename = "sample_hr.csv"
            st.success("✅ Sample HR dataset loaded! Navigate to any page to explore.")

    with col3:
        if st.button("🛒 Load E-commerce Data", use_container_width=True):
            import pandas as pd
            import numpy as np
            np.random.seed(99)
            n = 180
            df = pd.DataFrame({
                "order_id": [f"ORD{i:04d}" for i in range(1, n + 1)],
                "category": np.random.choice(["Electronics", "Clothing", "Books", "Home", "Sports"], n),
                "payment_method": np.random.choice(["Credit Card", "UPI", "NetBanking", "COD"], n),
                "order_value": np.random.randint(200, 8000, n),
                "discount_pct": np.random.choice([0, 5, 10, 15, 20], n),
                "delivery_days": np.random.randint(1, 10, n),
                "returned": np.random.choice(["Yes", "No"], n, p=[0.15, 0.85]),
            })
            st.session_state.df = df
            st.session_state.filename = "sample_ecommerce.csv"
            st.success("✅ Sample e-commerce dataset loaded! Navigate to any page to explore.")
