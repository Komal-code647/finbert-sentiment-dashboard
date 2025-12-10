import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_demo_data():
    print("--- SEEDING DEMO DATA ---")
    
    # 1. Generate last 30 days of dates
    end_date = datetime.now()
    dates = [end_date - timedelta(days=x) for x in range(30)]
    dates.reverse() # Sort oldest to newest
    
    # 2. Simulate realistic stock movement (Random Walk)
    # Starting price $220, moving slightly up/down each day
    price = 220.0
    prices = []
    
    # 3. Simulate Sentiment (correlated slightly with price)
    sentiments = []
    
    for _ in dates:
        # Random daily fluctuation (-2% to +2%)
        change_pct = np.random.uniform(-0.02, 0.02)
        price = price * (1 + change_pct)
        prices.append(price)
        
        # If price went up, sentiment is likely positive (with some noise)
        if change_pct > 0:
            # Mostly positive numbers (0 to 1)
            sent = np.random.uniform(-0.2, 0.9) 
        else:
            # Mostly negative numbers (-1 to 0.2)
            sent = np.random.uniform(-0.9, 0.2)
            
        sentiments.append(sent)

    # 4. Create DataFrame
    df = pd.DataFrame({
        'Date': [d.date() for d in dates],
        'Close': prices,
        'Avg_Sentiment': sentiments
    })
    
    # 5. Calculate the Metrics (just like in Phase 4)
    df['Price_Change_Pct'] = df['Close'].pct_change() * 100
    df['Rolling_Corr'] = df['Price_Change_Pct'].rolling(window=3).corr(df['Avg_Sentiment'])
    df = df.fillna(0)
    
    # 6. Save
    df.to_csv('final_analysis.csv', index=False)
    print("SUCCESS: Generated 30 days of demo data in 'final_analysis.csv'")

if __name__ == "__main__":
    generate_demo_data()