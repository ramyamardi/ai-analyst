import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.claude_api import suggest_charts
from utils.data_utils import get_column_types


def build_chart(df: pd.DataFrame, config: dict):
    """Build a Plotly chart from AI config."""
    ctype = config.get("chart_type", "bar")
    x = config.get("x_column")
    y = config.get("y_column")
    color = config.get("color_column")
    title = config.get("title", "Chart")

    # Validate columns exist
    for col in [x, y, color]:
        if col and col not in df.columns:
            return None

    try:
        if ctype == "bar":
            if x and y:
                fig = px.bar(df, x=x, y=y, color=color, title=title, barmode="group")
            elif x:
                counts = df[x].value_counts().reset_index()
                counts.columns = [x, "count"]
                fig = px.bar(counts, x=x, y="count", title=title)
            else:
                return None

        elif ctype == "line":
            fig = px.line(df, x=x, y=y, color=color, title=title, markers=True)

        elif ctype == "scatter":
            fig = px.scatter(df, x=x, y=y, color=color, title=title, trendline="ols" if not color else None)

        elif ctype == "pie":
            col_to_use = x or color
            if col_to_use:
                counts = df[col_to_use].value_counts().reset_index()
                counts.columns = [col_to_use, "count"]
                fig = px.pie(counts, names=col_to_use, values="count", title=title)
            else:
                return None

        elif ctype == "histogram":
            col_to_use = x or y
            if col_to_use:
                fig = px.histogram(df, x=col_to_use, color=color, title=title, nbins=30)
            else:
                return None

        elif ctype == "box":
            fig = px.box(df, x=x, y=y, color=color, title=title)

        elif ctype == "heatmap":
            num_cols = df.select_dtypes(include='number').columns
            if len(num_cols) >= 2:
                corr = df[num_cols].corr().round(2)
                fig = px.imshow(corr, text_auto=True, title=title, color_continuous_scale="RdBu_r", zmin=-1, zmax=1)
            else:
                return None
        else:
            return None

        fig.update_layout(height=380, margin=dict(t=50, b=30, l=30, r=30))
        return fig

    except Exception:
        return None


def show():
    st.markdown("## 📊 Auto Charts")
    st.markdown("Claude analyzes your dataset and recommends the most insightful visualizations.")

    if "df" not in st.session_state or st.session_state.df is None:
        st.warning("⚠️ Please upload a dataset first. Go to **Upload & Explore**.")
        return

    df = st.session_state.df
    col_types = get_column_types(df)

    # Manual chart builder
    with st.expander("🛠️ Build Your Own Chart", expanded=False):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            chart_type = st.selectbox("Chart Type", ["bar", "line", "scatter", "pie", "histogram", "box", "heatmap"])
        with c2:
            x_col = st.selectbox("X Axis", [None] + list(df.columns))
        with c3:
            y_col = st.selectbox("Y Axis", [None] + list(df.columns))
        with c4:
            color_col = st.selectbox("Color By", [None] + list(df.columns))

        if st.button("Generate Chart", use_container_width=True):
            custom_config = {
                "chart_type": chart_type, "x_column": x_col,
                "y_column": y_col, "color_column": color_col,
                "title": f"{chart_type.title()} — {x_col or ''} vs {y_col or ''}"
            }
            fig = build_chart(df, custom_config)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.error("Couldn't build this chart with the selected columns. Try different ones.")

    st.markdown("---")
    st.markdown("### 🤖 AI-Suggested Charts")

    if "ai_charts" not in st.session_state:
        st.session_state.ai_charts = None

    if st.button("✨ Generate AI Chart Suggestions", use_container_width=True):
        with st.spinner("Claude is analyzing your data and choosing the best charts..."):
            try:
                suggestions = suggest_charts(df)
                st.session_state.ai_charts = suggestions
            except Exception as e:
                st.error(f"Error generating suggestions: {e}")

    if st.session_state.ai_charts:
        suggestions = st.session_state.ai_charts
        st.success(f"✅ Claude suggested {len(suggestions)} charts for your dataset!")

        for i in range(0, len(suggestions), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                idx = i + j
                if idx < len(suggestions):
                    cfg = suggestions[idx]
                    with col:
                        fig = build_chart(df, cfg)
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
                            with st.expander(f"💡 Why this chart?"):
                                st.markdown(f"**{cfg.get('description', '')}**")
                                st.markdown(f"*Insight: {cfg.get('insight', '')}*")
                        else:
                            st.info(f"⚠️ Couldn't render: {cfg.get('title', 'chart')} — columns may not match.")
    else:
        st.info("Click the button above to let Claude choose the best charts for your data.")
