import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

def create_dataset(stock_data, sentiment_data, time_step=1):
    """
    Prepare the dataset by combining stock price and sentiment data.
    """
    stock_data['sentiment'] = sentiment_data['sentiment']
    dataset = stock_data[['Close', 'sentiment']].values
    X, y = [], []
    for i in range(len(dataset) - time_step - 1):
        X.append(dataset[i:(i + time_step), :])
        y.append(dataset[i + time_step, 0])
    return np.array(X), np.array(y)

def build_lstm_model(input_shape):
    """
    Build and compile the LSTM model.
    """
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

if __name__ == "__main__":
    # Example usage
    stock_data = pd.read_csv("data/processed/apple_stock_data_processed.csv")
    sentiment_data = pd.read_csv("data/processed/apple_news_data_processed.csv")

    X, y = create_dataset(stock_data, sentiment_data, time_step=60)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Build and train the model
    model = build_lstm_model((X_train.shape[1], X_train.shape[2]))
    model.fit(X_train, y_train, batch_size=32, epochs=10, validation_data=(X_test, y_test))

    # Save the model
    model.save("model/stock_price_lstm_model.h5")
