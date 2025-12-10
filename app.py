import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- CONFIGURATION ---
st.set_page_config(layout="wide", page_title="FinBERT Sentiment Dashboard")

# --- LOAD DATA ---
@st.cache_data # Caches the data so it doesn't reload on every click
def load_data():
    df = pd.read_csv('final_analysis.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Error: 'final_analysis.csv' not found. Please run the backend scripts first.")
    st.stop()

# --- SIDEBAR ---
st.sidebar.title("Configuration")
ticker = st.sidebar.text_input("Ticker Symbol", value="AMZN")
st.sidebar.markdown("---")
st.sidebar.markdown("**Project Status:**")
st.sidebar.success("Backend: Online")
st.sidebar.success(f"Data Points: {len(df)}")

# --- MAIN PAGE ---
st.title(f"📈 Financial Sentiment Analysis: {ticker}")
st.markdown("""
This dashboard correlates **News Sentiment** (derived via FinBERT) with **Stock Price Volatility**.
It demonstrates how unstructured text data impacts market movements.
""")

# Key Metrics Row
col1, col2, col3 = st.columns(3)
latest_price = df['Close'].iloc[-1]
latest_sentiment = df['Avg_Sentiment'].iloc[-1]
correlation = df['Rolling_Corr'].iloc[-1]

col1.metric("Latest Stock Price", f"${latest_price:.2f}")
col2.metric("Daily Sentiment Score", f"{latest_sentiment:.2f}", 
            delta_color="normal" if latest_sentiment > 0 else "inverse")
col3.metric("Sentiment-Price Correlation", f"{correlation:.2f}")

# --- VISUALIZATION ---
# Create a Dual-Axis Chart
fig = make_subplots(specs=[[{"secondary_y": True}]])

# 1. Stock Price Line (Blue)
# 1. Stock Price Line (Neon Style)
fig.add_trace(
    go.Scatter(
        x=df['Date'], 
        y=df['Close'], 
        name="Stock Price", 
        line=dict(color='#00F0FF', width=3), # Neon Cyan hex code
        fill='tozeroy', # Optional: Fills area under line
        fillcolor='rgba(0, 240, 255, 0.1)' # Faint glow under the line
    ),
    secondary_y=False
)

# 2. Sentiment Bar Chart (Green/Red)
# Color bars based on positive/negative sentiment
colors = ['green' if val > 0 else 'red' for val in df['Avg_Sentiment']]

fig.add_trace(
    go.Bar(x=df['Date'], y=df['Avg_Sentiment'], name="News Sentiment", marker_color=colors, opacity=0.6),
    secondary_y=True
)

# Layout Polish
fig.update_layout(
    title_text="Price vs. Sentiment Correlation",
    height=600,
    hovermode="x unified",
    xaxis_title="Date",
    legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center")
)

# Axis Titles
fig.update_yaxes(title_text="Stock Price ($)", secondary_y=False)
fig.update_yaxes(title_text="Sentiment Score (-1 to +1)", secondary_y=True)

st.plotly_chart(fig, use_container_width=True)

# --- RAW DATA TOGGLE ---
with st.expander("View Raw Analysis Data"):
    st.dataframe(df)

# --- EXPLANATION SECTION ---
st.markdown("### 🧠 How It Works")
st.info(
    """
    1. **Data Collection:** Scraped financial headlines via `BeautifulSoup` and stock data via `yfinance`.
    2. **NLP Engine:** Utilized **ProsusAI/FinBERT** (Transformer model) to classify sentiment.
    3. **Analysis:** Calculated a weighted daily sentiment score and correlated it with price percentage change.
    """
)