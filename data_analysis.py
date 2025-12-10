import pandas as pd
import numpy as np

def analyze_correlation(news_path, stock_path):
    print("--- PHASE 4: Data Merging & Analysis ---")
    
    # 1. Load News Data
    print("Loading News Data...")
    news_df = pd.read_csv(news_path)
    # Ensure date is actually a date object
    news_df['date_only'] = pd.to_datetime(news_df['date_only']).dt.date
    
    # 2. Aggregation: Squash 50 headlines into 1 "Daily Score"
    # We group by date and take the mean of 'weighted_score'
    daily_sentiment = news_df.groupby('date_only')['weighted_score'].mean().reset_index()
    daily_sentiment.columns = ['Date', 'Avg_Sentiment']
    print(f"Aggregated news into {len(daily_sentiment)} daily scores.")
    
    # 3. Load Stock Data (With the Fix for the AMZN row)
    print("Loading Stock Data...")
    # 'header=0' reads the first row as columns. We will drop the second row manually if needed.
    stock_df = pd.read_csv(stock_path)
    
    # FIX: Check if Row 0 contains ticker names (like 'AMZN') and drop it
    if stock_df.iloc[0, 1] == 'AMZN' or stock_df.iloc[0, 1] == stock_df.columns[1]:
        print("Detected 'Ghost Header' row (Ticker names). Removing it...")
        stock_df = stock_df.iloc[1:]
        
    # Convert columns to numbers (just in case they became strings)
    cols = ['Open', 'Close', 'Volume']
    for c in cols:
        stock_df[c] = pd.to_numeric(stock_df[c])
        
    stock_df['Date'] = pd.to_datetime(stock_df['date_only']).dt.date
    stock_df = stock_df[['Date', 'Close', 'Volume']] # Keep only what we need
    
    # 4. Merge the two worlds
    # Inner join: We only keep days where we have BOTH news and stock data
    merged_df = pd.merge(stock_df, daily_sentiment, on='Date', how='inner')
    
    # 5. Feature Engineering (The "Alpha")
    # Raw price doesn't matter. The *change* in price matters.
    # We calculate "Daily Return" (%)
    merged_df['Price_Change_Pct'] = merged_df['Close'].pct_change() * 100
    
    # Rolling Correlation: How much does Sentiment match Price over a 3-day window?
    # +1.0 = Perfect Sync, -1.0 = Opposite, 0 = Random
    merged_df['Rolling_Corr'] = merged_df['Price_Change_Pct'].rolling(window=3).corr(merged_df['Avg_Sentiment'])

    # Fill NaN values (first few rows won't have a rolling score)
    merged_df = merged_df.fillna(0)
    
    print("\n--- ANALYSIS RESULT ---")
    print(merged_df[['Date', 'Close', 'Avg_Sentiment', 'Price_Change_Pct', 'Rolling_Corr']].tail())
    
    # 6. Save for the Dashboard
    merged_df.to_csv('final_analysis.csv', index=False)
    print("\nSaved to 'final_analysis.csv'. Ready for Phase 5 (Dashboard)!")

if __name__ == "__main__":
    analyze_correlation('scored_news.csv', 'stock_data.csv')