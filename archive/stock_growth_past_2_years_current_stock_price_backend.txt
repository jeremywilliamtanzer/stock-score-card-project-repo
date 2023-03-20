import requests
from api_key import key
import datetime
import json

def get_stock_price(ticker):
    """Get stock growth for given stocks
    over a 2 year date range in yearly timespan. Meaning this function is comparing the closing stock price
    from yesterday to the closing stock price from (yesterday - 2 years).
    Today being the 14th of March 2023 we would compare yesterdays opening stock price (13.03.23) with the
    closing stock price of 13.03.2021.
    """
    # Define the API URL and parameters
    end_date = (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    start_date = (datetime.date.today() - datetime.timedelta(days=2*365)).strftime("%Y-%m-%d")

    # Replace <your_api_key> with your actual API key from Polygon
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start_date}/{end_date}?apiKey={key}"
    # Send the request to the API
    response = requests.get(url)
    # Check if the response was successful
    if response.status_code == 200:
        # Parse the response JSON data
        data = json.loads(response.content)
        # Get the current stock price
        current_price = data['results'][-1]['c']
        # Get the stock price from 5 years ago
        five_years_ago_price = data['results'][0]['c']
        # Calculate the price change percentage
        price_change_pct = (current_price - five_years_ago_price) / five_years_ago_price * 100
        # Return the results
        return {"current_price": current_price, "price_change_pct": price_change_pct}
    else:
        # If the response was not successful, raise an error
        raise ValueError("Unable to fetch stock price data. Status code: {}".format(response.status_code))

stock_price_data = get_stock_price('AAPL')
print(stock_price_data)
