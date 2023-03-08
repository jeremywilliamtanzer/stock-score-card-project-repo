import requests
import pandas as pd
from api_key import key

tickers = (input('Input short stock name: '),)
start_date = '2022-01-01'
end_date = '2023-01-01'
timespan = 'day'

def get_aggregates(tickers):
    """Get aggregate bars for a stock
    over a given date range in custom time window sizes.
    """
    for ticker in tickers:
        print(f'Calling the API for {ticker}:')
        url = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/{timespan}/{start_date}/{end_date}?adjusted=true&sort=asc&limit=120&apiKey={key}'
        response = requests.get(url).json()
        df = pd.DataFrame(response['results'])
        print(df)

get_aggregates(tickers)




# https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/2023-01-09/2023-01-09?adjusted=true&sort=asc&limit=120&apiKey=wQ5FjyMjpTSO2j5vBxbLuIp72hwYd5E5
# response = requests.get('https://api.polygon.io/v2/aggs/ticker/', params={'stocksTicker': ticker, 'multiplier': 1, 'timespan': 'day', 'from': '2022-01-01', 'to': '2023-01-01'},
