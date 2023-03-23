import streamlit as st
import numpy as np
import pandas as pd
import requests
from fastapi import FastAPI
import requests
from datetime import date
from dateutil.relativedelta import relativedelta
import datetime
import json
import langdetect
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
#from params import *

poly_key = st.secrets["POLY_KEY"]
alpha_key = st.secrets["ALPHA_KEY"]
news_key = st.secrets["NEWS_KEY"]

ticker = st.text_input('Insert Ticker here')
ticker = ticker.upper()

if ticker != "":
    company_logo, company_name, company_sector = requests.get('https://ssc-cont-ifhzucuzaa-ew.a.run.app/get_ticker_details?tickers=' + ticker)
    growth = round(requests.get('https://ssc-cont-ifhzucuzaa-ew.a.run.app/get_aggregate?tickers=' + ticker).json()['growth'], 2)
    div_yield = requests.get('https://ssc-cont-ifhzucuzaa-ew.a.run.app/get_dividend_yield?tickers=' + ticker).json()['Dividend Yield:']
    mkt_cap = requests.get('https://ssc-cont-ifhzucuzaa-ew.a.run.app/mkt_cap?tickers=' + ticker).json()['market_capitalization']

    ratios = requests.get('https://ssc-cont-ifhzucuzaa-ew.a.run.app/get_ratios?tickers=' + ticker).json()
    payout = ratios["Payout_ratio"]
    eps_next_year = ratios["EPS_next_1Y"]
    eps_past_five_years = ratios["EPS_past_5Y"]
    debt_over_fcf = ratios["Debt_over_FCF"]

    #ticker_details = requests.get('https://ssc-cont-ifhzucuzaa-ew.a.run.app/get_ticker_details?tickers=' + ticker).json()
    #line above from previous master


    # a 2x2 grid the long way
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(company_name)
            st.markdown(company_sector)
            st.markdown(mkt_cap)
            st.image(company_logo, width = 100)
        with col2:
            st.markdown(f'Sales Past 5Y: {growth}%')
            st.markdown(f'EPS Past 5Y: {eps_past_five_years}%')
            st.markdown(f'EPS Next Year: {eps_next_year}')
            st.markdown(f'Debt/FCF: {debt_over_fcf}')
            st.markdown(f'Divident Yield: {div_yield}')
            st.markdown(f'Market Cap: {mkt_cap}')
