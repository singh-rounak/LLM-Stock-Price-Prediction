import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import os

def preprocess_stock_data(filepath):
    """
    Preprocess stock price data.
    """
    stock_data = pd.read_csv(filepath)
    stock_data.fillna(method='ffill', inplace=True)
    return stock_data

def preprocess_news_data(filepath):
    """
    Preprocess news data and generate sentiment scores using a pre-trained BERT model.
    """
    news_data = pd.read_csv(filepath)
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=3)

    def classify_sentiment(text):
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        sentiment = torch.argmax(probs).item()
        return sentiment

    news_data['sentiment'] = news_data['description'].apply(lambda x: classify_sentiment(str(x)))
    return news_data

def save_preprocessed_data(data, filename, folder="data/processed"):
    """
    Save preprocessed data to a CSV file in the specified folder.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)
    filepath = os.path.join(folder, filename)
    data.to_csv(filepath, index=False)

if __name__ == "__main__":
    # Example usage
    stock_data = preprocess_stock_data("data/raw/apple_stock_data.csv")
    save_preprocessed_data(stock_data, "apple_stock_data_processed.csv")

    news_data = preprocess_news_data("data/raw/apple_news_data.csv")
    save_preprocessed_data(news_data, "apple_news_data_processed.csv")
