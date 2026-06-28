import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.claude_api import analyze_data_quality
from utils.data_utils import clean_dataframe, dataframe_to_csv_bytes


SEVERITY_COLOR = {"high": "🔴", "medium": "🟡", "low": "🟢"}


def show():
    st.markdown("## 🧹 Data Cleaning")
    st.markdown("AI-powered data quality analysis and one-click cleaning.")

    if "df" not in st.session_state or st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset first. Go to **Upload & Explore**.")
        return

    df = st.session_state.df

    # AI Quality Analysis
    st.markdown("### 🔍 AI Quality Analysis")
    if "quality_report" not in st.session_state:
        st.session_state.quality_report = None

    if st.button("🤖 Analyze Data Quality with AI", use_container_width=True):
        with st.spinner("Claude is inspecting your data quality..."):
            try:
                report = analyze_data_quality(df)
                st.session_state.quality_report = report
            except Exception as e:
                st.error(f"Error: {e}")

    if st.session_state.quality_report:
        report = st.session_state.quality_report
        
        score = report.get("overall_score", 0)
        color = "#4caf50" if score >= 80 else "#ff9800" if score >= 60 else "#f44336"
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f"""
            <div style="background:{color}20;border:2px solid {color};border-radius:16px;
                        padding:1.5rem;text-align:center;">
                <div style="font-size:3rem;font-weight:700;color:{color}">{score}</div>
                <div style="color:{color};font-weight:600;">Quality Score</div>
                <div style="color:#666;font-size:0.85rem;">/100</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"**Summary:** {report.get('summary', '')}")
            st.markdown("**Quick wins:**")
            for win in report.get("quick_wins", []):
                st.markdown(f"  • {win}")

        st.markdown("#### 🚨 Issues Found")
        issues = report.get("issues", [])
        if issues:
            for issue in issues:
                sev = issue.get("severity", "low")
                icon = SEVERITY_COLOR.get(sev, "⚪")
                with st.expander(f"{icon} {issue.get('type', '').replace('_', ' ').title()} — `{issue.get('column', '')}`"):
                    st.markdown(f"**Issue:** {issue.get('description', '')}")
                    st.markdown(f"**Fix:** {issue.get('suggestion', '')}")
        else:
            st.success("No major issues found!")

    st.markdown("---")

    # Manual cleaning actions
    st.markdown("### 🛠️ Cleaning Actions")
    st.markdown("Select the actions you want to apply:")

    actions_map = {
        "drop_duplicates": "🗑️ Remove duplicate rows",
        "drop_missing_rows": "❌ Drop rows with any missing value",
        "fill_numeric_median": "🔢 Fill numeric missing values with median",
        "fill_categorical_mode": "🔤 Fill text missing values with mode",
        "strip_whitespace": "✂️ Strip whitespace from text columns",
        "standardize_column_names": "🏷️ Standardize column names (lowercase, underscores)",
    }

    selected_actions = []
    col1, col2 = st.columns(2)
    action_list = list(actions_map.items())
    for i, (key, label) in enumerate(action_list):
        col = col1 if i % 2 == 0 else col2
        with col:
            if st.checkbox(label, key=f"action_{key}"):
                selected_actions.append(key)

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 3])
    with col_a:
        apply_btn = st.button("✨ Apply Cleaning", use_container_width=True)

    if apply_btn:
        if not selected_actions:
            st.warning("Please select at least one cleaning action.")
        else:
            with st.spinner("Cleaning your data..."):
                cleaned_df, log = clean_dataframe(df, selected_actions)
                st.session_state.cleaned_df = cleaned_df

            st.success("✅ Cleaning complete!")
            for entry in log:
                st.markdown(entry)

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Original rows", df.shape[0])
                st.metric("Original missing cells", int(df.isnull().sum().sum()))
            with col2:
                st.metric("Cleaned rows", cleaned_df.shape[0])
                st.metric("Remaining missing cells", int(cleaned_df.isnull().sum().sum()))

            st.markdown("### 👀 Preview of Cleaned Data")
            st.dataframe(cleaned_df.head(10), use_container_width=True)

            col_x, col_y = st.columns(2)
            with col_x:
                if st.button("✅ Use cleaned dataset for analysis", use_container_width=True):
                    st.session_state.df = cleaned_df
                    st.session_state.ai_charts = None
                    st.session_state.quality_report = None
                    st.success("Dataset updated! All pages will now use the cleaned data.")

            with col_y:
                st.download_button(
                    "⬇️ Download cleaned CSV",
                    data=dataframe_to_csv_bytes(cleaned_df),
                    file_name="cleaned_data.csv",
                    mime="text/csv",
                    use_container_width=True
                )
