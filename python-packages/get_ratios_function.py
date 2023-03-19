import requests
import pandas as pd

alphavantage_key = "7QD6TN4TDCX63BZ6"

def get_ratios(ticker):
    months = {"January":"01", "February": "02", "March":"03", "April": "04", "May": "05",
    "June": "06", "July": "07", "August": "08", "September": "09", "October": "10",
    "November": "11", "December": "12"}
    
    # Replace <your_api_key> with your actual API key from Polygon
    url_overview = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol=' + ticker + '&apikey=' + alphavantage_key
    overview = requests.get(url_overview).json()
    
    url_earnings = 'https://www.alphavantage.co/query?function=EARNINGS&symbol=' + ticker + '&apikey=' + alphavantage_key
    earnings = requests.get(url_earnings).json()
    
    url_cf = 'https://www.alphavantage.co/query?function=CASH_FLOW&symbol=' + ticker + '&apikey=' + alphavantage_key
    cf = requests.get(url_cf).json()
    
    url_balance = 'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=' + ticker + '&apikey=' + alphavantage_key
    balance = requests.get(url_balance).json()
    
    url_income = 'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=' + ticker + '&apikey=' + alphavantage_key
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

