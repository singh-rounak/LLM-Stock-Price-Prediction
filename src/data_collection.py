import yfinance as yf
import requests
import pandas as pd
import os

def download_stock_data(ticker, start_date, end_date):
    """
    Download historical stock data from Yahoo Finance.
    """
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    stock_data.reset_index(inplace=True)
    return stock_data

def fetch_news(api_key, query, start_date, end_date, page_size=100):
    """
    Fetch news articles from a news API.
    """
    url = f"https://newsapi.org/v2/everything?q={query}&from={start_date}&to={end_date}&sortBy=popularity&pageSize={page_size}&apiKey={api_key}"
    response = requests.get(url)
    news_data = response.json()
    return news_data

def save_data_to_csv(data, filename, folder="data/raw"):
    """
    Save data to a CSV file in the specified folder.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)
    filepath = os.path.join(folder, filename)
    data.to_csv(filepath, index=False)

if __name__ == "__main__":
    # Example usage
    ticker = "AAPL"
    start_date = "2022-01-01"
    end_date = "2023-01-01"
    api_key = "your_news_api_key"
    query = "Apple"

    # Download stock data
    stock_data = download_stock_data(ticker, start_date, end_date)
    save_data_to_csv(stock_data, "apple_stock_data.csv")

    # Fetch news articles
    news_data = fetch_news(api_key, query, start_date, end_date)
    news_df = pd.json_normalize(news_data['articles'])
    save_data_to_csv(news_df, "apple_news_data.csv")
