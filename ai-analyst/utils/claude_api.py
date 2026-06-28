import anthropic
import pandas as pd
import json

client = anthropic.Anthropic()

def get_dataframe_context(df: pd.DataFrame, max_rows: int = 5) -> str:
    """Build a concise context string from a dataframe for Claude."""
    context = f"""
Dataset Overview:
- Shape: {df.shape[0]} rows × {df.shape[1]} columns
- Columns: {list(df.columns)}
- Data types: {df.dtypes.to_dict()}
- Null counts: {df.isnull().sum().to_dict()}

Sample data (first {min(max_rows, len(df))} rows):
{df.head(max_rows).to_string()}

Numeric summary:
{df.describe().to_string() if not df.select_dtypes(include='number').empty else 'No numeric columns'}
"""
    return context


def chat_with_data(question: str, df: pd.DataFrame, chat_history: list) -> str:
    """Answer a natural language question about the dataframe."""
    context = get_dataframe_context(df)
    
    system_prompt = f"""You are an expert data analyst AI. You have access to a dataset and must answer the user's questions about it clearly and accurately.

{context}

Guidelines:
- Give direct, clear answers with specific numbers/values from the data
- If you suggest code, use Python/Pandas syntax
- Highlight key findings with bullet points
- If a question can't be answered from this data, say so clearly
- Be conversational but precise
"""
    
    messages = []
    for msg in chat_history[-6:]:  # Keep last 6 messages for context
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": question})
    
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=system_prompt,
        messages=messages
    )
    return response.content[0].text


def suggest_charts(df: pd.DataFrame) -> list:
    """Get AI-suggested chart types and configurations."""
    context = get_dataframe_context(df)
    
    prompt = f"""Based on this dataset, suggest 6 meaningful charts/visualizations.

{context}

Return ONLY a valid JSON array (no markdown, no explanation) with this exact structure:
[
  {{
    "title": "Chart title",
    "chart_type": "bar|line|scatter|pie|histogram|box|heatmap",
    "x_column": "column_name or null",
    "y_column": "column_name or null",
    "color_column": "column_name or null",
    "description": "Why this chart is useful",
    "insight": "What we might discover"
  }}
]

Only suggest columns that exist in the dataset: {list(df.columns)}
"""
    
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    text = response.content[0].text.strip()
    # Clean any accidental markdown
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    text = text.strip()
    
    return json.loads(text)


def analyze_data_quality(df: pd.DataFrame) -> dict:
    """Get AI analysis of data quality issues and cleaning suggestions."""
    context = get_dataframe_context(df)
    
    prompt = f"""Analyze the data quality of this dataset and provide cleaning recommendations.

{context}

Return ONLY valid JSON (no markdown) with this structure:
{{
  "overall_score": 85,
  "issues": [
    {{
      "type": "missing_values|duplicates|outliers|formatting|data_type",
      "column": "column_name or 'all'",
      "severity": "high|medium|low",
      "description": "Description of issue",
      "suggestion": "How to fix it"
    }}
  ],
  "quick_wins": ["action 1", "action 2"],
  "summary": "Overall assessment in 2 sentences"
}}
"""
    
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    text = response.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    text = text.strip()
    
    return json.loads(text)


def generate_summary_report(df: pd.DataFrame, filename: str = "dataset") -> str:
    """Generate a comprehensive narrative summary report."""
    context = get_dataframe_context(df, max_rows=10)
    
    prompt = f"""You are a senior data analyst. Generate a comprehensive summary report for this dataset named '{filename}'.

{context}

Write a professional report with these sections:
1. **Executive Summary** - 3-4 sentence overview
2. **Dataset Overview** - Structure, size, completeness
3. **Key Metrics** - Most important numbers and statistics
4. **Patterns & Trends** - Notable patterns you observe
5. **Data Quality** - Assessment of data quality
6. **Recommendations** - 3-5 actionable recommendations
7. **Next Steps** - Suggested analyses to perform

Be specific with numbers. Use markdown formatting. Write as if presenting to a business stakeholder.
"""
    
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text
