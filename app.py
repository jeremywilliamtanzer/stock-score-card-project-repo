import streamlit as st
import pandas as pd
import requests
from datetime import *
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# poly_key = st.secrets["POLY_KEY"]
# alpha_key = st.secrets["ALPHA_KEY"]
# news_key = st.secrets["NEWS_KEY"]

ticker = st.text_input('Insert Ticker here')
ticker = ticker.upper()

def get_stock_price_history(tickers):
    """Get stock history for a given stock
    over a 2 year date range in yearly timespan.
    """
    POLY_KEY_1 = 'rW1fMPt5T8N4lrq6J4HM58LKZj1VBoPl'
    tickers = tickers.upper()

    # Define the API URL and parameters
    end = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    start = (date.today() - timedelta(days=2*365)).strftime("%Y-%m-%d")

    # Replace <your_api_key> with your actual API key from Polygon
    url = f'https://api.polygon.io/v2/aggs/ticker/{tickers}/range/1/day/{start}/{end}?adjusted=true&sort=asc&limit=120&apiKey={POLY_KEY_1}'
    # Send the request to the API
    response = requests.get(url).json()
    # Check if the response was successful
    response = pd.DataFrame.from_dict(response['results'])
    response.columns = ['volume', 'vwap', 'open', 'close', 'high', 'low', 'timestamp', 'n']
    response['date'] = response.timestamp.apply(lambda i: date.fromtimestamp(i/1000))
    response = response[['volume', 'vwap', 'open', 'close', 'high', 'low', 'date', 'n']].set_index('date')
    fig = px.line(response, x=response.index, y="close", title='Price History')
    # Return the results
    return fig

if ticker != "":
    company_logo, company_name, company_sector = requests.get('https://ssc-cont-ifhzucuzaa-ew.a.run.app/get_ticker_details?tickers=' + ticker).json()
    # growth = round(requests.get('https://ssc-cont-ifhzucuzaa-ew.a.run.app/get_aggregate?tickers=' + ticker).json()['growth'], 2)
    # mkt_cap = requests.get('https://ssc-cont-ifhzucuzaa-ew.a.run.app/mkt_cap?tickers=' + ticker).json()['market_capitalization']
    # ratios = requests.get('https://ssc-cont-ifhzucuzaa-ew.a.run.app/get_ratios?tickers=' + ticker).json()
    # # latest_price = requests.get('https://ssc-cont-ifhzucuzaa-ew.a.run.app/get_stock_price?tickers=' + ticker).json()["current_price"]

    # dividend_yield = ratios['Dividend_yield']
    # payout = ratios["Payout_ratio"]
    # eps_next_year = ratios["EPS_next_1Y"]
    # eps_past_five_years = ratios["EPS_past_5Y"]
    # debt_over_fcf = ratios["Debt_over_FCF"]

    # st.image(company_logo, width = 100)
    # a 2x2 grid the long way
    # with st.container():
    #     col1, col2 = st.columns(2)
    #     with col1:
    #         st.markdown('Hello World')
    #         st.markdown(company_name)
    #         st.markdown(company_sector)
    #         st.markdown(f'Market Cap: USD{mkt_cap}MM')
    #         st.markdown(f'Stock Price: USD{latest_price}')
    #     with col2:
    #         st.markdown('Hello World')
    #         st.markdown(f'Sales Past 5Y: {growth}%')
    #         st.markdown(f'EPS Past 5Y: {eps_past_five_years}%')
    #         st.markdown(f'EPS Next Year: {eps_next_year}%')
    #         st.markdown(f'Debt/FCF: {debt_over_fcf} years')
    #         st.markdown(f'Divident Yield: {dividend_yield}%')
    # st.plotly_chart(get_stock_price_history(ticker))

    st.image(company_logo, width = 100)
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('Microsoft Corporation')
            st.markdown('Prepackaged Software')
            st.markdown('Market Cap: USD 10000MM')
            st.markdown('Stock Price: USD 100')
        with col2:
            st.markdown('Sales Past 5Y: 5%')
            st.markdown('EPS Past 5Y: 10%')
            st.markdown('EPS Next Year: 10%')
            st.markdown('Debt/FCF: 4 years')
            st.markdown('Divident Yield: 3%')
    st.plotly_chart(get_stock_price_history(ticker))
