import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
import tensorflow as tf

def evaluate_model(model, X_test, y_test):
    """
    Evaluate the model's performance using MAE and RMSE.
    """
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    return mae, rmse

if __name__ == "__main__":
    # Example usage
    model = tf.keras.models.load_model("model/stock_price_lstm_model.h5")
    X_test = np.load("data/processed/X_test.npy")
    y_test = np.load("data/processed/y_test.npy")

    mae, rmse = evaluate_model(model, X_test, y_test)
    print(f"MAE: {mae}")
    print(f"RMSE: {rmse}")
