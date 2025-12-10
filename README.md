[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://finbert-sentiment-dashboard-g8n4hrxwkqxcfh25hzxuiw.streamlit.app)

# 📈 FinBERT Sentiment & Volatility Analyzer

A Full-Stack Machine Learning pipeline that correlates financial news sentiment with stock market volatility using Large Language Models (LLMs).

## 🚀 Overview
In the era of high-frequency trading, financial markets are overwhelmed by unstructured textual data, making manual analysis impossible. This project mitigates information overload by:
1. **Scraping** real-time financial news headlines.
2. **Quantifying** sentiment using `ProsusAI/FinBERT` (a Transformer model specialized for finance).
3. **Correlating** sentiment scores with stock price volatility to identify market signals.

## 🛠️ Tech Stack
* **AI/NLP:** Hugging Face Transformers, PyTorch, FinBERT
* **Data Engineering:** BeautifulSoup4, yfinance, Pandas
* **Frontend:** Streamlit, Plotly
* **Deployment:** Streamlit Community Cloud

## 📊 Key Features
* **Sentiment Quantifier:** Converts "fuzzy" text into mathematical scores (-1 to +1).
* **Rolling Correlation:** Calculates how strongly news impacts price over a 3-day window.
* **Interactive Dashboard:** Visualizes trends with dual-axis charts (Neon UI).

## 🔧 How to Run Locally
1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/finbert-sentiment-dashboard.git](https://github.com/YOUR_USERNAME/finbert-sentiment-dashboard.git)