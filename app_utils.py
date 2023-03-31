# imports

ticker_list = ('AAPL', 'BABA', 'GME', 'PLTR',
               'SBUX', 'TSLA', 'ACN', 'ADM',
               'AMZN', 'AAL', 'GOOG', 'BLK',
               'BSX', 'CAT', 'CSCO', 'EBAY',
               'XOM', 'GM', 'HUM', 'LMT',
               'MA', 'MCD')
sorted_ticker_list = sorted(ticker_list)

def get_icon(var_name, value):
    # returns ✅ or ❌ based on the fundamental value
    thresholds = {
        'dividend_yield': 2,
        'growth': 12,
        'payout': 60,
        'eps_next_year': 10,
        'eps_past_five_years': 7,
        'debt_over_fcf': -4,
        'news_sentiment': 50
        }
    if value > thresholds[var_name]:
        return '✅'
    else:
        return '❌'
