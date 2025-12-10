import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
import torch

def load_finbert():
    """
    Downloads and loads the ProsusAI FinBERT model.
    """
    print("Loading FinBERT model... (This may take a minute first time)")
    tokenizer = BertTokenizer.from_pretrained('ProsusAI/finbert')
    model = BertForSequenceClassification.from_pretrained('ProsusAI/finbert')
    
    # Create a pipeline (Easy-to-use wrapper)
    nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    return nlp

def analyze_sentiment(csv_file_path):
    print("--- PHASE 3: AI Sentiment Analysis ---")
    
    # 1. Load Data
    try:
        df = pd.read_csv(csv_file_path)
    except FileNotFoundError:
        print("Error: clean_news.csv not found. Did you run Phase 2?")
        return
        
    print(f"Loaded {len(df)} headlines.")
    
    # 2. Load Model
    nlp_pipeline = load_finbert()
    
    # 3. Analyze Headlines
    print("Analyzing headlines... (This uses your CPU/GPU)")
    
    # We will store results in lists
    labels = []
    scores = []
    
    # Iterate through headlines
    # Tip: In a real massive production system, we would batch this. 
    # For <1000 rows, a simple loop is fine.
    total = len(df)
    for index, row in df.iterrows():
        headline = row['Headline']
        
        # Handle empty headlines
        if pd.isna(headline) or str(headline).strip() == "":
            labels.append("neutral")
            scores.append(0.0)
            continue
            
        # Truncate if too long (BERT has a 512 token limit, headlines are usually short though)
        headline = str(headline)[:512]
        
        # Run AI
        result = nlp_pipeline(headline)[0]
        
        # result looks like: {'label': 'positive', 'score': 0.95}
        labels.append(result['label'])
        scores.append(result['score'])
        
        if index % 10 == 0:
            print(f"Processed {index}/{total}...")

    # 4. Add results to DataFrame
    df['sentiment_label'] = labels
    df['sentiment_confidence'] = scores
    
    # 5. Convert Label to a Math Number for Correlation
    # Positive = 1, Neutral = 0, Negative = -1
    label_map = {'positive': 1, 'neutral': 0, 'negative': -1}
    df['sentiment_score'] = df['sentiment_label'].map(label_map)
    
    # Weighted Score: If confidence is low (e.g. 0.5), the score is less strong.
    # Formula: Label_Value * Confidence
    df['weighted_score'] = df['sentiment_score'] * df['sentiment_confidence']

    # 6. Save
    output_file = 'scored_news.csv'
    df.to_csv(output_file, index=False)
    print(f"\nDone! Saved to {output_file}")
    print(df[['Headline', 'sentiment_label', 'weighted_score']].head())

if __name__ == "__main__":
    analyze_sentiment('clean_news.csv')