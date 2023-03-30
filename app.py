import streamlit as st
import pandas as pd
import requests
from datetime import *
import datetime
import matplotlib.pyplot as plt
import plotly.express as px

# poly_key = st.secrets["POLY_KEY"]
# alpha_key = st.secrets["ALPHA_KEY"]
# news_key = st.secrets["NEWS_KEY"]



ticker_list = ('AAPL', 'SBUX', 'TSLA', 'ACN', 'ADM', 'AMZN', 'AAL', 'GOOG', 'BLK', 'BSX', 'CAT', 'CSCO', 'EBAY', 'XOM', 'GM', 'HUM', 'LMT', 'MA', 'MCD')
sorted_ticker_list = sorted(ticker_list)

st.title(':blue[STOCK SCORECARD APP]')
st.subheader(':blue[_trade smarter, not harder_]')

ticker = st.selectbox('Insert Company Ticker Here',
                      sorted_ticker_list)
ticker = ticker.upper()


def get_stock_price_history(tickers):
    """Get stock history for a given stock
    over a 2 year date range in yearly timespan.
    """
    tickers = tickers.upper()
    POLY_KEY_1 = 'wQ5FjyMjpTSO2j5vBxbLuIp72hwYd5E5'
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
st.markdown(':blue[_SSC QUICK METRICS_]')
if ticker != "":
    company_logo, company_name, company_sector = requests.get('https://ssc-cont-ifhzucuzaa-ew.a.run.app/get_ticker_details?tickers=' + ticker).json()
    # growth = round(requests.get('https://ssc-cont-ifhzucuzaa-ew.a.run.app/get_aggregate?tickers=' + ticker).json()['growth'], 2)
    # mkt_cap = requests.get('https://ssc-cont-ifhzucuzaa-ew.a.run.app/mkt_cap?tickers=' + ticker).json()['market_capitalization']
    # ratios = requests.get('https://ssc-cont-ifhzucuzaa-ew.a.run.app/get_ratios?tickers=' + ticker).json()
    # latest_price = requests.get('https://ssc-cont-ifhzucuzaa-ew.a.run.app/get_stock_price?tickers=' + ticker).json()["current_price"]
    # news_sentiment = requests.get('https://ssc-cont-ifhzucuzaa-ew.a.run.app/news_score?tickers=' + ticker).json()["current_price"]

    # dividend_yield = ratios['Dividend_yield']
    # payout = ratios["Payout_ratio"]
    # eps_next_year = ratios["EPS_next_1Y"]
    # eps_past_five_years = ratios["EPS_past_5Y"]
    # debt_over_fcf = ratios["Debt_over_FCF"]

    mkt_cap = 1736
    latest_price = 270
    dividend_yield = 3
    growth = 10
    payout = 46
    eps_next_year = 14.45
    eps_past_five_years = 10.45
    debt_over_fcf = 5
    news_sentiment = 78

    if dividend_yield > 2:
        icon_1 = '✅'
    else:
        icon_1 = '❌'

    if growth > 12:
        icon_2 = '✅'
    else:
        icon_2 = '❌'

    if payout > 60:
        icon_3 = '✅'
    else:
        icon_3 = '❌'

    if eps_next_year > 10:
        icon_4 = '✅'
    else:
        icon_4 = '❌'

    if eps_past_five_years > 7:
        icon_5 = '✅'
    else:
        icon_5 = '❌'

    if debt_over_fcf < 4:
        icon_6 = '✅'
    else:
        icon_6 = '❌'

    if news_sentiment > 50:
        icon_7 = '✅'
    else:
        icon_7 = '❌'

    st.image(company_logo, width = 100)
    # a 2x2 grid the long way
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(company_name)
            st.markdown(company_sector)
            st.markdown(f'Market Cap: USD{mkt_cap}MM')
            st.markdown(f'Stock Price: USD{latest_price}')
        with col2:
            st.markdown(f'Divident Yield: {dividend_yield}% {icon_1}', unsafe_allow_html=True)
            st.markdown(f'Sales Past 5Y: {growth}% {icon_2}', unsafe_allow_html=True)
            st.markdown(f'Payout Ratio: {payout}% {icon_3}', unsafe_allow_html=True)
            st.markdown(f'EPS Next Year: {eps_next_year}% {icon_4}', unsafe_allow_html=True)
            st.markdown(f'EPS Past 5Y: {eps_past_five_years}% {icon_5}', unsafe_allow_html=True)
            st.markdown(f'Debt/FCF: {debt_over_fcf} years {icon_6}', unsafe_allow_html=True)
            st.markdown(f'News Sentiment: {news_sentiment}% {icon_7}', unsafe_allow_html=True)
    st.plotly_chart(get_stock_price_history(ticker))
