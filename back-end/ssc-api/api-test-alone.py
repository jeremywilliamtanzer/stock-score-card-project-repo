from fastapi import FastAPI
import requests
from api_key import poly_key
from datetime import date
from dateutil.relativedelta import relativedelta
from api_key import alphavantage_key

api = FastAPI()

@api.get('/')
def index():
    return {'ok': 'api connected'}

#always add @api.get as a root
@api.get('/my_calc')
def my_calc(feature1, features2):
    return {'results': (float(feature1) + float(features2))}


#tickers = (input('Input short stock name: '),)


@api.get('/get_aggregate') #test with AAPL for Apple
def get_aggregates(tickers):
    """Get revenue growth for given stocks
    over a 5 year date range in yearly timespan meaning comparing the revenue of last year
    compared to the revenue of (last year - 4).
    Being in March 2023 we would compare yearly revenue from 2022 with yearly revenue from 2018.
    """
    report_date_1 = date.today()
    report_date_2 = date.today()- relativedelta(years=4)
    timespan = 'annual'
    year   = 5
    #tickers = [tickers]
    tickers = tickers.upper()

    #for ticker in tickers:
    #print(f'Calling the API for {ticker}...')
    url_1 = f'https://api.polygon.io/vX/reference/financials?ticker={tickers}&period_of_report_date.lte={report_date_1}&timeframe={timespan}&include_sources=true&apiKey={poly_key}'
    url_2 = f'https://api.polygon.io/vX/reference/financials?ticker={tickers}&period_of_report_date.lte={report_date_2}&timeframe={timespan}&include_sources=true&apiKey={poly_key}'
    response_1 = requests.get(url_1).json()
    revenue_1 = response_1['results'][0]['financials']['income_statement']['revenues']['value']
    response_2 = requests.get(url_2).json()
    revenue_2 = response_2['results'][0]['financials']['income_statement']['revenues']['value']
    sales_growth = ((revenue_1/revenue_2)-1)*100
    #print(f'The sales growth of {ticker} in the last {year} years has been {round(sales_growth,2)}%')
    return {'growth': float(sales_growth)}


@api.get('/get_dividend_yield') #test with AAPL for Apple
def get_dividend_yield(tickers):
    #change to uppercase
    tickers = tickers.upper()
    # Get dividend yield from Overview tab on Alphavantage API
    url_overview = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol=' + tickers + '&apikey=' + alphavantage_key
    overview = requests.get(url_overview).json()
    #Divident Yield:
    return {"Dividend Yield:": (str(round(float(overview['DividendYield'])*100,2))+ "%")}


api.get('/mkt_cap')
def market_cap(tickers):
    #change to uppercase
    tickers = tickers.upper()
    #instantiate url
    url = f'https://api.polygon.io/vX/reference/tickers/{tickers}?apiKey={key}'
    #response in .json
    api = requests.get(url).json()
    #get market cap + round to 2decimal and return in millions
    mkt_cap = round((api['results']['market_cap'] / 1_000_000_000), 2)
    return {'market_capitalization' : mkt_cap}

@api.get('/get_ticker_details') #test with AAPL for Apple
def get_ticker_details(ticker):
    # Get ticker details from Polygon's Stocks API
    url = 'https://api.polygon.io/v3/reference/tickers/' + tickers + '&apikey=' + poly_key
    ticker_details = requests.get(url_overview).json()
    company_logo = ticker_details["results"]["branding"]["logo_url"] + '?apiKey=' + poly_key
    company_name = ticker_details["results"]["name"]
    company_sector = ticker_details["results"]["sic_description"]
    #Divident Yield:
    return company_logo, company_name, company_sector

