import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import requests

#@st.cache_data
def get_plotly_data():

    z_data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv')
    z = z_data.values
    sh_0, sh_1 = z.shape
    x, y = np.linspace(0, 1, sh_0), np.linspace(0, 1, sh_1)
    return x, y, z

ticker = st.text_input('Insert Ticker here')

st.markdown("""# This is a header
## This is a sub header
This is text""")

api_key = 'rW1fMPt5T8N4lrq6J4HM58LKZj1VBoPl'

if ticker != "":
    url = 'https://api.polygon.io/v3/reference/tickers/' + ticker + '?apiKey=' + api_key
    ticker_details = requests.get(url).json()
    company_logo = ticker_details["results"]["branding"]["logo_url"]
    company_icon = ticker_details["results"]["branding"]["icon_url"]
    company_name = ticker_details["results"]["name"]
    company_sector = ticker_details["results"]["sic_description"]
    x, y, z = get_plotly_data()

    fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
    fig.update_layout(title='IRR', autosize=True, margin=dict(l=40, r=40, b=40, t=40))

    # a 2x2 grid the long way
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.company_logo
            st.write(company_name)
            st.write(company_sector)
            st.plotly_chart(fig)
        with col2:
            st.write('Caption for first chart')
            st.plotly_chart(fig)

# df = pd.DataFrame({
#     'first column': list(range(1, 11)),
#     'second column': np.arange(10, 101, 10)
# })

# # this slider allows the user to select a number of lines
# # to display in the dataframe
# # the selected value is returned by st.slider
# line_count = st.slider('Select a line count', 1, 10, 3)

# # and used to select the displayed lines
# head_df = df.head(line_count)

# head_df
