import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_utils import get_quick_stats, get_column_types


def show():
    st.markdown("## 📂 Upload & Explore")
    st.markdown("Upload your CSV file and get an instant overview of your data.")

    uploaded = st.file_uploader("Choose a CSV file", type=["csv"], label_visibility="collapsed")

    if uploaded:
        df = pd.read_csv(uploaded)
        st.session_state.df = df
        st.session_state.filename = uploaded.name
        st.success(f"✅ Loaded **{uploaded.name}** successfully!")

    if "df" not in st.session_state or st.session_state.df is None:
        st.info("👆 Upload a CSV file above, or go to **Home** to load a sample dataset.")
        return

    df = st.session_state.df
    stats = get_quick_stats(df)
    col_types = get_column_types(df)

    # Key metrics
    st.markdown("### 📊 Dataset at a Glance")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Rows", f"{stats['rows']:,}")
    c2.metric("Columns", stats['cols'])
    c3.metric("Completeness", f"{stats['completeness']}%")
    c4.metric("Duplicates", stats['duplicates'])
    c5.metric("Missing Cells", f"{stats['missing_cells']:,}")

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Numeric Columns", stats['numeric_cols'])
    col_b.metric("Text Columns", stats['categorical_cols'])
    col_c.metric("Other Columns", stats['cols'] - stats['numeric_cols'] - stats['categorical_cols'])

    st.markdown("---")

    # Data preview tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Preview", "📈 Numeric Stats", "🔤 Column Info", "❓ Missing Values"])

    with tab1:
        rows = st.slider("Rows to preview", 5, min(100, len(df)), 10)
        st.dataframe(df.head(rows), use_container_width=True)

    with tab2:
        if col_types["numeric"]:
            st.dataframe(df[col_types["numeric"]].describe().round(2), use_container_width=True)
        else:
            st.info("No numeric columns found.")

    with tab3:
        col_info = pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.values,
            "Non-Null Count": df.count().values,
            "Null Count": df.isnull().sum().values,
            "Null %": (df.isnull().sum().values / len(df) * 100).round(1),
            "Unique Values": df.nunique().values,
            "Sample Value": [str(df[c].dropna().iloc[0]) if not df[c].dropna().empty else "—" for c in df.columns]
        })
        st.dataframe(col_info, use_container_width=True)

    with tab4:
        missing = df.isnull().sum()
        missing = missing[missing > 0].sort_values(ascending=False)
        if missing.empty:
            st.success("🎉 No missing values found in your dataset!")
        else:
            missing_df = pd.DataFrame({
                "Column": missing.index,
                "Missing Count": missing.values,
                "Missing %": (missing.values / len(df) * 100).round(1)
            })
            st.dataframe(missing_df, use_container_width=True)
            
            import plotly.express as px
            fig = px.bar(missing_df, x="Column", y="Missing %", 
                         title="Missing Values by Column (%)",
                         color="Missing %", color_continuous_scale="Reds")
            fig.update_layout(showlegend=False, height=350)
            st.plotly_chart(fig, use_container_width=True)
