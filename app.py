import streamlit as st
import pandas as pd
import numpy as np
import requests
from datetime import *
import matplotlib.pyplot as plt
import plotly.express as px
from app_utils import *
from backend.ssc_api.ssc_functions import *
from backend.ssc_api.utils import *
import random

### Page setting
st.set_page_config(layout="wide", page_title="Stock Scorecard")

## Style sheet
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.title(':blue[STOCK SCORECARD APP]')
st.subheader(':blue[_trade smarter, not harder_]')

ticker = st.text_input('Insert Company Ticker Here')
#ticker = st.selectbox('Insert Company Ticker Here', sorted_ticker_list)
ticker = ticker.upper()

st.markdown(':blue[_SSC QUICK METRICS_]')


### MOCK MODE: 1 -> cut out API calls to only test the UI
###            0 -> restore normal function calls
mock_mode = 0
# mock parameters
company_logo = "https://www.etestware.com/wp-content/uploads/2020/08/shutterstock_515285995-1200x580.jpg"
company_name = "Scorecard"
company_sector = "Financial info"
mkt_cap = 1000
latest_price = 100
dividend_yield = 3
growth = 10
payout = 10
eps_next_year = 10
eps_past_five_years = 10
debt_over_fcf = 10
news_sentiment = 10
predicted_close = 150
# END of mock parameters

### API CALLS & fundamentals calculation
if ticker != "":
    price_history = get_stock_price_history(ticker)
    if mock_mode:
        pass
    else:
        company_logo, company_name, company_sector = get_company_nls(ticker)
        growth = get_growth(ticker)
        mkt_cap = get_mkt_cap(ticker)
        ratios = get_ratios(ticker)
        latest_price = get_price(ticker)
        news_sentiment = get_sentiment(ticker)

        dividend_yield = ratios['Dividend_yield']
        payout = ratios["Payout_ratio"]
        eps_next_year = ratios["EPS_next_1Y"]
        eps_past_five_years = ratios["EPS_past_5Y"]
        debt_over_fcf = ratios["Debt_over_FCF"]


        # mock predicted_close
        predicted_close = latest_price * (100 + random.randint(-3,3))/100
        # predicted_close = get_prediction(ticker)
        '''        if ticker == 'TSLA':
            predicted_close = get_prediction(ticker)
        else:
            try:
                predicted_close = pred[ticker]
            except:
                predicted_close = 'model in development'
        '''
    fundamentals = {
    'dividend_yield': dividend_yield,
    'growth': growth,
    'payout': payout,
    'eps_next_year': eps_next_year,
    'eps_past_five_years': eps_past_five_years,
    'debt_over_fcf': debt_over_fcf*-1,
    'news_sentiment': news_sentiment
    }
    ## Show Scorecard
    with st.container():
        # first row
        col1, col2, score = st.columns((4,4,2))
        with col1:
            st.image(company_logo, width = 100)
            st.markdown(company_name)
            st.markdown(company_sector)
            st.markdown(f'Market Cap: USD {mkt_cap}MM')
            st.markdown(f'Stock Price: USD {latest_price}')
        with col2:
            st.markdown(f'Divident Yield: {dividend_yield}% {get_icon("dividend_yield", dividend_yield)}', unsafe_allow_html=True)
            st.markdown(f'Sales Past 5Y: {growth}% {get_icon("growth", growth)}', unsafe_allow_html=True)
            st.markdown(f'Payout Ratio: {payout}% {get_icon("payout", payout)}', unsafe_allow_html=True)
            st.markdown(f'EPS Next Year: {eps_next_year}% {get_icon("eps_next_year", eps_next_year)}', unsafe_allow_html=True)
            st.markdown(f'EPS Past 5Y: {eps_past_five_years}% {get_icon("eps_past_five_years", eps_past_five_years)}', unsafe_allow_html=True)
            st.markdown(f'Debt/FCF: {debt_over_fcf} years {get_icon("debt_over_fcf", debt_over_fcf*-1)}', unsafe_allow_html=True)
            st.markdown(f'News Sentiment: {news_sentiment}% {get_icon("news_sentiment", news_sentiment)}', unsafe_allow_html=True)
        with score:
            st.markdown(f'SCORE: {get_score(fundamentals)}/10', unsafe_allow_html=True)
        # second row
        col3, col4 = st.columns((8,2))
        with col3:
            st.plotly_chart(price_history)
        with col4:
            st.markdown(f'Predicted close: {predicted_close}', unsafe_allow_html=True)
