import streamlit as st
import numpy as np
import pandas as pd
import requests
from params import *

# key = st.secrets["APIKEY"]
# alpha_key = st.secrets["alphavantage_key"]

poly_key = POLYKEY
alpha_key = ALPHAKEY

ticker = st.text_input('Insert Ticker here')

if ticker != "":
    ticker_details = requests.get('https://ssc-cont-ifhzucuzaa-ew.a.run.app/get_ticker_details?tickers=' + ticker).json()

    # a 2x2 grid the long way
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(company_name)
            st.markdown(company_sector)
            st.image(company_logo, width = 100)
        with col2:
            st.markdown(requests.get('https://ssc-cont-ifhzucuzaa-ew.a.run.app/get_aggregate?tickers=' + ticker).json()['growth'])
            st.markdown(requests.get('https://ssc-cont-ifhzucuzaa-ew.a.run.app/get_dividend_yield?tickers=' + ticker).json()['Dividend Yield:'])
