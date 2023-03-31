# imports

ticker_list = ('AAPL', 'BABA', 'GME', 'PLTR',
               'SBUX', 'TSLA', 'ACN', 'ADM',
               'AMZN', 'AAL', 'GOOG', 'BLK',
               'BSX', 'CAT', 'CSCO', 'EBAY',
               'XOM', 'GM', 'HUM', 'LMT',
               'MA', 'MCD')
sorted_ticker_list = sorted(ticker_list)

thresholds = {
    'dividend_yield': 2,
    'growth': 12,
    'payout': 60,
    'eps_next_year': 10,
    'eps_past_five_years': 7,
    'debt_over_fcf': -4,
    'news_sentiment': 50
    }

def get_icon(var_name, value):
    # returns ✅ or ❌ based on the fundamental value
    if value > thresholds[var_name]:
        return '✅'
    else:
        return '❌'

def get_score(fundamentals):
    # returns ✅ or ❌ based on the fundamental value
    score = 2
    for measure, val in fundamentals.items():
        if val > thresholds[measure]:
            score += 1
    return score
