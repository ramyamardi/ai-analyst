# 🤖 AI Analyst

> Ask questions about your data in plain English. No SQL. No formulas. Just answers.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?style=flat-square&logo=streamlit)
![Claude API](https://img.shields.io/badge/Claude-Anthropic-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## ✨ Features

| Feature | Description |
|---|---|
| 📂 Upload & Explore | Upload any CSV and get instant stats, column info, and missing value breakdown |
| 💬 Chat with Data | Ask questions in plain English — Claude answers with specifics from your data |
| 📊 Auto Charts | AI picks the best 6 visualizations for your specific dataset |
| 🧹 Data Cleaning | One-click fix for duplicates, missing values, whitespace, and column naming |
| 📋 Summary Report | Full analyst-quality written report, ready to download and share |

---

## 🖥️ Demo

**Questions you can ask:**
- *"What is the monthly revenue trend?"*
- *"Which product category has the highest returns?"*
- *"Are there any outliers in the sales column?"*
- *"Summarize the key findings from this dataset."*

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| AI Engine | Claude API (Anthropic) — `claude-sonnet-4-6` |
| Data | Python, Pandas, NumPy |
| Charts | Plotly Express |

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/your-username/ai-analyst.git
cd ai-analyst
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set your Anthropic API key
```bash
# Mac/Linux
export ANTHROPIC_API_KEY=your_api_key_here

# Windows
set ANTHROPIC_API_KEY=your_api_key_here
```

Get your free API key at: https://console.anthropic.com

### 4. Run the app
```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser. 🎉

---

## 📁 Project Structure

```
ai-analyst/
├── app.py                  # Main Streamlit app + navigation
├── requirements.txt
├── README.md
├── pages/
│   ├── home.py             # Landing page + sample datasets
│   ├── upload.py           # CSV upload + data exploration
│   ├── chat.py             # Natural language Q&A with Claude
│   ├── charts.py           # AI chart suggestions + manual builder
│   ├── cleaning.py         # Data quality analysis + cleaning
│   └── report.py           # AI-generated summary report
└── utils/
    ├── claude_api.py       # All Claude API calls
    └── data_utils.py       # Data processing helpers
```

---

## 💡 How It Works

1. **You upload** a CSV file (or use one of 3 built-in sample datasets)
2. **Claude reads** the schema, column types, sample rows, and statistics
3. **You interact** — ask questions, request charts, trigger cleaning, or generate a report
4. **Claude responds** with data-grounded answers, chart configs, quality scores, and full reports

All AI features use the `claude-sonnet-4-6` model via the Anthropic API.

---

## 💡 Inspiration

Built during a Data Analyst internship working with 50,000+ records, 3 Power BI dashboards, and 15+ SQL queries. The goal: make data exploration as easy as asking a question.

---

## 📬 Connect

Made by **Ramya** · [LinkedIn](www.linkedin.com/in/ramya-mardi) · [GitHub](https://github.com/ramyashree)

⭐ Found this useful? Star the repo — it helps a lot!

---

## 📄 License

MIT License — free to use, modify, and distribute.
