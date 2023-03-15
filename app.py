import streamlit as st
import numpy as np
import pandas as pd
import requests

from params import *

key = st.secrets["APIKEY"]
alpha_key = st.secrets["alphavantage_key"]



#poly_key = POLYKEY
#alpha_key = ALPHAKEY


ticker = st.text_input('Insert Ticker here')
ticker = ticker.upper()



if ticker != "":

    url = 'https://api.polygon.io/v3/reference/tickers/' + ticker + '?apiKey=' + key
    ticker_details = requests.get(url).json()
    company_logo = ticker_details["results"]["branding"]["logo_url"] + '?apiKey=' + key
    company_name = ticker_details["results"]["name"]
    company_sector = ticker_details["results"]["sic_description"]
    growth = round(requests.get('https://ssc-cont-ifhzucuzaa-ew.a.run.app/get_aggregate?tickers=' + ticker).json()['growth'], 2)
    div_yield = requests.get('https://ssc-cont-ifhzucuzaa-ew.a.run.app/get_dividend_yield?tickers=' + ticker).json()['Dividend Yield:']
    #mkt_cap = requests.get('https://ssc-cont-ifhzucuzaa-ew.a.run.app/get_dividend_yield?tickers=' + ticker).json()['market_capitalization']

#    ticker_details = requests.get('https://ssc-cont-ifhzucuzaa-ew.a.run.app/get_ticker_details?tickers=' + ticker).json()
# line above from previous master

    # a 2x2 grid the long way
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(company_name)
            st.markdown(company_sector)
            st.image(company_logo, width = 100)
        with col2:
            st.markdown(f'Growth: {growth}%')
            st.markdown(f'Divident Yield: {div_yield}')
            #st.markdown(f'Market Cap: {mkt_cap}')
