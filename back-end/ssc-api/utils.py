import requests
from datetime import date
from dateutil.relativedelta import relativedelta
import json
from params import *
from dotenv import load_dotenv
from tensorflow.keras import models
from tensorflow.keras import layers
from scipy import stats
import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta

# auxiliary function to get data
def get_stock_data(ticker, multiplier, timespan, from_date, to_date):
    # Make the API request
    api_url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{from_date}/{to_date}"
    response = requests.get(api_url, params={"apiKey": "wQ5FjyMjpTSO2j5vBxbLuIp72hwYd5E5"})

    # Check for errors
    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")

    # Extract the data from the response
    data = response.json()["results"]
    stock_data = []
    for d in data:
        stock_data.append({
            "Date": pd.to_datetime(d["t"], unit='ms').date(),
            "Open": d["o"],
            "High": d["h"],
            "Low": d["l"],
            "Close": d["c"],
            "Adj Close": d["c"],
            "Volume": d["v"],
        })

    # Convert the data to a dataframe
    df = pd.DataFrame(stock_data)
    df = df.reset_index(drop=True)

    return df

def predict_next_day_price(model, X_test, confidence=0.95):
    # Use the trained model to make predictions on the test set
    y_pred = model.predict(X_test)
    # Calculate the mean of all the predictions
    mean_prediction = np.mean(y_pred)
    # Calculate the standard deviation of the predictions
    std_deviation = np.std(y_pred)
    # Calculate the confidence interval
    interval = stats.norm.interval(confidence, loc=mean_prediction, scale=std_deviation)
    lower_bound, upper_bound = interval
    # Return the mean prediction and confidence interval as a dictionary
    return {'mean_prediction': mean_prediction, 'lower_bound': lower_bound, 'upper_bound': upper_bound}

    # load the saved model
