import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

def clean_news_dates(csv_file_path):
    """
    1. Loads the raw news data.
    2. Converts 'Dec-10-25' into standard '2025-12-10'.
    3. Combines Date and Time into a proper datetime object.
    """
    print("--- STEP 1: Cleaning Dates ---")
    df = pd.read_csv(csv_file_path)
    
    # Combined Date and Time into one string
    # We force the format to be string first to avoid errors
    df['full_timestamp'] = df['Date'].astype(str) + ' ' + df['Time'].astype(str)
    
    # Convert to datetime objects
    # format='%b-%d-%y %I:%M%p' handles "Dec-10-25 04:30PM"
    # %b = Month name (Dec), %d = Day, %y = Year (2-digit), %I = Hour (12-hr), %p = AM/PM
    try:
        df['parsed_date'] = pd.to_datetime(df['full_timestamp'], format='%b-%d-%y %I:%M%p')
        print("Dates parsed successfully.")
    except Exception as e:
        print(f"Date parsing failed. Trying simpler format or auto-detect. Error: {e}")
        # Fallback for different FinViz formats
        df['parsed_date'] = pd.to_datetime(df['full_timestamp'], errors='coerce')

    # Create a clean 'date_only' column for merging with stock data later
    df['date_only'] = df['parsed_date'].dt.date
    
    print(f"Cleaned {len(df)} rows of news data.")
    return df

def get_market_data(ticker, start_date, end_date):
    """
    Downloads daily stock prices (Open, Close, Volume) for the given date range.
    """
    print(f"\n--- STEP 2: Fetching Stock Prices for {ticker} ---")
    
    # We add a buffer to the dates to ensure we cover everything
    start_str = start_date.strftime('%Y-%m-%d')
    # yfinance end_date is exclusive, so we add 1 day
    end_str = (end_date + timedelta(days=1)).strftime('%Y-%m-%d')
    
    print(f"Downloading data from {start_str} to {end_str}...")
    
    stock_data = yf.download(ticker, start=start_str, end=end_str, progress=False)
    
    if stock_data.empty:
        print("Error: No stock data found. Check your dates or internet.")
        return None
    
    # Flatten the multi-index columns if they exist (common yfinance issue)
    stock_data.reset_index(inplace=True)
    
    # Keep only what we need
    # Adjust column names based on yfinance version (sometimes it's 'Date', sometimes 'Datetime')
    if 'Date' in stock_data.columns:
        stock_data['date_only'] = stock_data['Date'].dt.date
    elif 'Datetime' in stock_data.columns:
        stock_data['date_only'] = stock_data['Datetime'].dt.date
        
    final_stock = stock_data[['date_only', 'Open', 'Close', 'Volume']]
    print(f"Downloaded {len(final_stock)} days of stock data.")
    return final_stock

# --- EXECUTION ---
if __name__ == "__main__":
    # 1. Load and Clean News
    news_df = clean_news_dates('raw_news_data.csv')
    
    # 2. Figure out the date range we need
    min_date = news_df['parsed_date'].min()
    max_date = news_df['parsed_date'].max()
    
    # 3. Get Stock Prices for that range
    # Note: We hardcode the ticker 'AMZN' to match our previous step. 
    # In the final app, this will be dynamic.
    stock_df = get_market_data('AMZN', min_date, max_date)
    
    if stock_df is not None:
        # 4. Save both (Separately for now, we merge after AI analysis)
        news_df.to_csv('clean_news.csv', index=False)
        stock_df.to_csv('stock_data.csv', index=False)
        
        print("\nSUCCESS!")
        print("1. 'clean_news.csv' created (Ready for AI).")
        print("2. 'stock_data.csv' created (Ready for Analysis).")
        print("\nCheck 'stock_data.csv' to see if you have rows of prices.")