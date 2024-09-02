import yfinance as yf
import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from the .env file


#Access the API key
# api_key = os.getenv("NEWS_API_KEY")

# #api_key = 'a50cb0d117d6485785d77a1d2def1f28'
# print(api_key)

# if not api_key:
#     raise ValueError("No API key found. Please set the NEWS_API_KEY in your .env file.")

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
    url = f"https://newsapi.org/v2/everything?q={query}&from={start_date}&to={end_date}&sortBy=popularity&pageSize={page_size}&apiKey={'0c95cea57abd4e29aa6666b04be03e6f'}"
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

    news_data = response.json()

    # Check if 'articles' key is in the response
    if 'articles' not in news_data:
        raise KeyError("'articles' not found in the API response. Response content: " + str(news_data))

    return news_data

def save_data_to_csv(data, filename, folder="data/raw"):
    """
    Save data to a CSV file in the specified folder.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)
    filepath = os.path.join(folder, filename)
    print(filepath)
    data.to_csv(filepath, index=False)

if __name__ == "__main__":
    # Example usage
    ticker = "AAPL"
    start_date = "2024-08-02"  # Example start date within allowed range
    end_date = "2024-08-30"    # Example end date
    api_key = "your_news_api_key"
    query = "Apple"

    # Download stock data
    stock_data = download_stock_data(ticker, start_date, end_date)
    save_data_to_csv(stock_data, "apple_stock_data.csv")

    # Fetch news articles
    news_data = fetch_news(api_key, query, start_date, end_date)
    news_df = pd.json_normalize(news_data['articles'])
    save_data_to_csv(news_df, "apple_news_data.csv")
