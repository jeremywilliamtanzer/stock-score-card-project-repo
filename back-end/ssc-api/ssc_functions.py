from fastapi import FastAPI
import requests
from datetime import date
from dateutil.relativedelta import relativedelta
import datetime
import json
from params import *
import langdetect
import nltk
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
from dotenv import load_dotenv

load_dotenv()

POLY_KEY = os.environ.get('POLY_KEY')
ALPHA_KEY = os.environ.get('ALPHA_KEY')
NEWS_KEY = os.environ.get('NEWS_KEY')


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
    url_1 = f'https://api.polygon.io/vX/reference/financials?ticker={tickers}&period_of_report_date.lte={report_date_1}&timeframe={timespan}&include_sources=true&apiKey={POLY_KEY}'
    url_2 = f'https://api.polygon.io/vX/reference/financials?ticker={tickers}&period_of_report_date.lte={report_date_2}&timeframe={timespan}&include_sources=true&apiKey={POLY_KEY}'
    response_1 = requests.get(url_1).json()
    revenue_1 = response_1['results'][0]['financials']['income_statement']['revenues']['value']
    response_2 = requests.get(url_2).json()
    revenue_2 = response_2['results'][0]['financials']['income_statement']['revenues']['value']
    sales_growth = ((revenue_1/revenue_2)-1)*100
    #print(f'The sales growth of {ticker} in the last {year} years has been {round(sales_growth,2)}%')
    return {'growth': float(sales_growth)}

@api.get('/mkt_cap')
def market_cap(tickers):
    #change to uppercase
    tickers = tickers.upper()
    #instantiate url
    url = f'https://api.polygon.io/vX/reference/tickers/{tickers}?apiKey={POLY_KEY}'
    #response in .json
    api = requests.get(url).json()
    #get market cap + round to 2decimal and return in millions
    mkt_cap = round((api['results']['market_cap'] / 1_000_000_000), 2)
    return {'market_capitalization' : float(mkt_cap)}

@api.get('/get_ticker_details') #test with AAPL for Apple
def get_ticker_details(tickers):
    # Get ticker details from Polygon's Stocks API
    url = 'https://api.polygon.io/v3/reference/tickers/' + tickers + '&apikey=' + POLY_KEY
    ticker_details = requests.get(url).json()
    company_logo = ticker_details["results"]["branding"]["logo_url"] + '?apiKey=' + POLY_KEY
    company_name = ticker_details["results"]["name"]
    company_sector = ticker_details["results"]["sic_description"]
    #Divident Yield:
    return company_logo, company_name, company_sector

@api.get('/get_ratios') #test with AAPL for Apple
def get_ratios(tickers):
    months = {"January":"01", "February": "02", "March":"03", "April": "04", "May": "05",
    "June": "06", "July": "07", "August": "08", "September": "09", "October": "10",
    "November": "11", "December": "12"}

    # Replace <your_api_key> with your actual API key from Polygon
    url_overview = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol=' + tickers + '&apikey=' + ALPHA_KEY
    overview = requests.get(url_overview).json()

    url_earnings = 'https://www.alphavantage.co/query?function=EARNINGS&symbol=' + tickers + '&apikey=' + ALPHA_KEY
    earnings = requests.get(url_earnings).json()

    url_cf = 'https://www.alphavantage.co/query?function=CASH_FLOW&symbol=' + tickers + '&apikey=' + ALPHA_KEY
    cf = requests.get(url_cf).json()

    url_balance = 'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=' + tickers + '&apikey=' + ALPHA_KEY
    balance = requests.get(url_balance).json()

    url_income = 'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=' + tickers + '&apikey=' + ALPHA_KEY
    income = requests.get(url_income).json()

    # Dividend yield:
    Dividend_yield = round(float(overview['DividendYield'])*100,2)

    #Payout ratio:
    Payout_ratio = round(float(overview['DividendPerShare'])/float(overview['EPS'])*100,2)

    #EPS next 1Y (we get EPS next 1Y from Forward PE formula which is current price/1Y EPS):
    EPS_next_1Y = round(float(overview['ForwardPE'])/(float(overview['EPS'])*float(overview['PERatio']))*100,2)

    # Get EPS past 5Y from alphavantage API on tab earnings we need the if function because
    #the first result shown in earnings is only annual if the last quarter is the same as the annual results quarter
    if earnings['annualEarnings'][0]['fiscalDateEnding'][5:7] == months[overview['FiscalYearEnd']]:
        last_EPS = float(earnings['annualEarnings'][0]['reportedEPS'])
        five_years_EPS = float(earnings['annualEarnings'][4]['reportedEPS'])
    else:
        last_EPS = float(earnings['annualEarnings'][1]['reportedEPS'])
        five_years_EPS = float(earnings['annualEarnings'][5]['reportedEPS'])
    if last_EPS/five_years_EPS>0:
        EPS_past_5Y = round((((last_EPS/five_years_EPS)**0.2)-1)*100,2)
    elif last_EPS<0:
        EPS_past_5Y =round((((abs(last_EPS/five_years_EPS)**0.2))-1)*-100,2)
    else: EPS_past_5Y =round((((abs(last_EPS/five_years_EPS)**0.2))-1)*100,2)

    #Get Debt/FCF from Alphavantage API on tabs CF statement and BS statement

    Debt = float(balance['annualReports'][0]['longTermDebt'])+float(balance['annualReports'][0]['currentDebt'])
    Operating_cf = float(cf['annualReports'][0]['operatingCashflow'])
    Debt_over_FCF = round(Debt/Operating_cf,2)

    return {"Dividend_yield": Dividend_yield, "Payout_ratio": Payout_ratio, "EPS_next_1Y": EPS_next_1Y, "EPS_past_5Y": EPS_past_5Y, "Debt_over_FCF": Debt_over_FCF}

@api.get('/get_stock_price') #test with AAPL for Apple
def get_stock_price(tickers):
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
    url = f"https://api.polygon.io/v2/aggs/ticker/{tickers}/range/1/day/{start_date}/{end_date}?apiKey={POLY_KEY}"
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


@api.get('/news_score')
def news_score(tickers):
    # Get ticker to have company name, since news_api only uses company name
    url = f'https://api.polygon.io/v3/reference/tickers/{tickers}&apikey={POLY_KEY}'
    ticker_details = requests.get(url).json()
    company_name = ticker_details["results"]["name"]

    #use today's date
    today = date.today()
    today = today.strftime("%d-%m-%Y")

    #search in api news company_name related content
    url = f'https://newsapi.org/v2/everything?q={company_name}&from={today}&sortBy=publishedAt&apiKey={NEWS_KEY}'
    response = requests.get(url)
    response = response.json()

    #loop to genenrate content list
    articles_content = []
    for article in response['articles']:
        content = article['content']
        if content:
            try:
                if langdetect.detect(content) == 'en':
                    articles_content.append(content)
            except:
                pass

    #concatenate to have one bloc of string
    content_string = ''.join(articles_content)

    #perform sentiment analysis using nltk's SentimentIntensityAnalyzer
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(content_string)
    percentage_score = score['compound']*100
    percentage_score = f'{percentage_score} %'

    #return percentage score in dict format
    return {'percentage_score':float(percentage_score)}
