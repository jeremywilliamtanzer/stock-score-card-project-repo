import streamlit as st
#import plotly.graph_objects as go
import numpy as np
import pandas as pd
import requests
#from front_end.params import *

#key = APIKEY

ticker = st.text_input('Insert Ticker here')

if ticker != "":
    url = 'https://api.polygon.io/v3/reference/tickers/' + ticker + '?apiKey=' + key
    ticker_details = requests.get(url).json()
    company_logo = ticker_details["results"]["branding"]["logo_url"] + '?apiKey=' + key
    company_name = ticker_details["results"]["name"]
    company_sector = ticker_details["results"]["sic_description"]

    # a 2x2 grid the long way
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(company_name)
            # st.markdown('hello_world')
            st.markdown(company_sector)
            st.image(company_logo, width = 100)
        with col2:
            st.markdown(requests.get('https://ssc-cont-ifhzucuzaa-ew.a.run.app/get_aggregate?tickers=' + ticker).json()['growth'])
