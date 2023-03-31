import requests
from datetime import date
#from dateutil.relativedelta import relativedelta
import json
#from params import *
#from dotenv import load_dotenv
#from tensorflow.keras import models
#from tensorflow.keras import layers
from scipy import stats
from datetime import date, datetime, timedelta
import pandas as pd
import numpy as np
import requests
from datetime import *
import matplotlib.pyplot as plt
import plotly.express as px

def get_company_nls(ticker):
    # API call to get company name, logo and industry sector
    return requests.get(
        'https://ssc-cont-ifhzucuzaa-ew.a.run.app/get_ticker_details?tickers='
        + ticker).json()

def get_growth(ticker):
    # API call to get sales growth of the company over last 5y
    return round(requests.get(
        'https://ssc-cont-ifhzucuzaa-ew.a.run.app/get_aggregate?tickers='
        + ticker).json()['growth'], 2)

def get_mkt_cap(ticker):
    # API call to get market capitalization of the company
    return requests.get(
        'https://ssc-cont-ifhzucuzaa-ew.a.run.app/mkt_cap?tickers='
        + ticker).json()['market_capitalization']

def get_ratios(ticker):
    # API call to get relevant indicators
    return requests.get(
        'https://ssc-cont-ifhzucuzaa-ew.a.run.app/get_ratios?tickers='
        +ticker).json()

def get_price(ticker):
    return requests.get(
        'https://ssc-cont-ifhzucuzaa-ew.a.run.app/get_stock_price?tickers='
        + ticker).json()["current_price"]


def get_stock_price_history(ticker):
    """Get stock history for a given stock
    over a 2 year date range in yearly timespan.
    """
    POLY_KEY_1 = 'wQ5FjyMjpTSO2j5vBxbLuIp72hwYd5E5'
    # Define the API URL and parameters
    end = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    start = (date.today() - timedelta(days=2*365)).strftime("%Y-%m-%d")
    limit = 5000
    # Replace <your_api_key> with your actual API key from Polygon
    url = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start}/{end}?adjusted=true&sort=asc&{limit}&apiKey={POLY_KEY_1}'
    # Send the request to the API
    response = requests.get(url).json()
    # Check if the response was successful
    response = pd.DataFrame.from_dict(response['results'])
    response.columns = ['volume', 'vwap', 'open',
                        'close', 'high', 'low',
                        'timestamp', 'n']
    response['date'] = response.timestamp.apply(
                        lambda i: date.fromtimestamp(i/1000))
    response = response[['volume', 'vwap', 'open',
                         'close', 'high', 'low',
                         'date', 'n']].set_index('date')
    fig = px.line(response, x=response.index, y="close", title='Price History')
    # Return the results
    return fig

'''
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
'''
