import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.claude_api import generate_summary_report
from utils.data_utils import get_quick_stats


def show():
    st.markdown("## 📋 AI Summary Report")
    st.markdown("Get a full analyst-style written report of your dataset — ready to share.")

    if "df" not in st.session_state or st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset first. Go to **Upload & Explore**.")
        return

    df = st.session_state.df
    filename = st.session_state.get("filename", "dataset")

    col1, col2 = st.columns([2, 1])
    with col1:
        report_name = st.text_input("Report title / dataset name", value=filename.replace(".csv", ""))
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        generate_btn = st.button("✨ Generate AI Report", use_container_width=True)

    if generate_btn:
        with st.spinner("Claude is writing your full analysis report... this takes ~15 seconds"):
            try:
                report = generate_summary_report(df, report_name)
                st.session_state.ai_report = report
            except Exception as e:
                st.error(f"Error: {e}")

    if "ai_report" in st.session_state and st.session_state.ai_report:
        report = st.session_state.ai_report

        st.markdown("---")
        
        # Quick stats header
        stats = get_quick_stats(df)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Rows", f"{stats['rows']:,}")
        c2.metric("Columns", stats['cols'])
        c3.metric("Completeness", f"{stats['completeness']}%")
        c4.metric("Duplicates", stats['duplicates'])

        st.markdown("---")
        
        # The report
        st.markdown(report)

        st.markdown("---")

        # Download options
        st.markdown("### ⬇️ Export Report")
        col_a, col_b = st.columns(2)

        with col_a:
            # Download as markdown
            md_content = f"# {report_name} — AI Analysis Report\n\n{report}"
            st.download_button(
                "📄 Download as Markdown (.md)",
                data=md_content.encode("utf-8"),
                file_name=f"{report_name}_report.md",
                mime="text/markdown",
                use_container_width=True
            )

        with col_b:
            # Download as plain text
            st.download_button(
                "📝 Download as Text (.txt)",
                data=report.encode("utf-8"),
                file_name=f"{report_name}_report.txt",
                mime="text/plain",
                use_container_width=True
            )

        st.info("💡 Tip: Copy the markdown file into Notion, Google Docs, or any markdown editor for a formatted version!")

    else:
        st.markdown("---")
        st.markdown("""
        ### What the report includes:
        - **Executive Summary** — high-level overview
        - **Dataset Overview** — structure, size, completeness
        - **Key Metrics** — important numbers and statistics  
        - **Patterns & Trends** — notable observations
        - **Data Quality** — assessment and issues
        - **Recommendations** — 3–5 actionable next steps
        - **Next Steps** — suggested analyses to perform
        
        Click the button above to generate your full report!
        """)
