from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

def get_news_data(ticker):
    """
    Scrapes news headlines for a specific stock ticker from FinViz.
    """
    print(f"Fetching news for {ticker}...")
    
    # 1. The URL Target
    url = f'https://finviz.com/quote.ashx?t={ticker}&p=d'
    
    # 2. The "Disguise" (Headers)
    # Websites block Python scripts. We must pretend to be a Chrome browser.
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers)
        # Check if the website accepted our request (Status 200 = OK)
        if response.status_code != 200:
            print(f"Failed to retrieve data. Status Code: {response.status_code}")
            return None
            
        # 3. Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # FinViz puts news in a specific HTML table with id='news-table'
        news_table = soup.find(id='news-table')
        
        if not news_table:
            print("Could not find news table. The website structure might have changed.")
            return None
            
        parsed_data = []
        
        # 4. Iterate through every row (tr) in the table
        for row in news_table.findAll('tr'):
            # The headline is inside an 'a' tag (anchor)
            title_tag = row.a 
            # The timestamp is inside a 'td' tag
            date_data = row.td.text.split()
            
            if title_tag is None:
                continue

            title = title_tag.text
            
            # 5. Handle Date Formats
            # FinViz format is tricky: 
            # Row 1: "Dec-10-25 09:30AM"
            # Row 2: "09:45AM" (It skips the date if it's the same day!)
            
            if len(date_data) == 1:
                time = date_data[0]
                # Use the date from the previous iteration
            else:
                date = date_data[0]
                time = date_data[1]
                
            parsed_data.append([ticker, date, time, title])
            
        # 6. Create DataFrame
        df = pd.DataFrame(parsed_data, columns=['Ticker', 'Date', 'Time', 'Headline'])
        print(f"Successfully scraped {len(df)} headlines.")
        return df

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# --- EXECUTION ---
if __name__ == "__main__":
    # Let's test with a volatile stock
    ticker_symbol = 'AMZN' 
    
    news_df = get_news_data(ticker_symbol)
    
    if news_df is not None:
        # Save to CSV so we don't have to scrape again and again
        news_df.to_csv('raw_news_data.csv', index=False)
        print("\nPreview of data:")
        print(news_df.head())
        print("\nSaved to 'raw_news_data.csv'")