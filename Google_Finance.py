__author__ = 'michaelliang0709'
# Python 2.7
import requests, json, re
from bs4 import BeautifulSoup
from datetime import datetime

# fake an user agent
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36'}

# historical price
def get_hist_data(params):
    response = requests.get("https://www.google.com/finance/historical", params=params,
                     headers=headers, verify=True)
    return BeautifulSoup(response.text, 'html.parser')

# real-time price
def get_realtime_data(params):
    response = requests.get("http://finance.google.com/finance/info?client=ig",
                            params=params, headers=headers, verify=True)
    return response.text, response.status_code

def translate_date(date):
    # format: 2015.1.1
    date = datetime.strptime(date, '%Y.%m.%d')
    # format: 2015 Jan 01
    return date.strftime('%Y %b %d')

def format_date(date):
    date = datetime.strptime(date, '%Y %b %d')
    return date.strftime('%b %d, %Y')

def get_data(symbol, date):
    data = []
    # parameters of the URL
    params = {'q': symbol, 'startdate': date, 'enddate': date}
    html_data = get_hist_data(params)
    # get the line of prices
    for s in html_data('td'):
        try:
            if s.get('class')[0] == 'rgt':
                s = str(s.text)
                data = s.split('\n')
                break
        except: continue
    if data == []:
        data = ['-'] * 4
        return data
    for d in data:
        if d == '':
            data.remove(d)
    # Open, High, Low, Close, Volume
    if len(data) == 5:
        data.pop()
    return data

def get_hist_price(symbol, date):
    try:
        date = translate_date(date)
        # get the close price
        price = get_data(symbol, date)[3]
        # format: Jan 01, 2015
        date = format_date(date)
        dict = {u"stock_symbol":symbol.upper(), u"date":date, u"close_price":price}
        #dict = json.JSONEncoder().encode(dict)
        return json.dumps(dict, sort_keys = True, indent = 2)
    except Exception as e:
        return "Error:", e.message

def get_realtime_price(symbol):
    try:
        params = {'q': symbol}
        data, code = get_realtime_data(params)
        if code != 200:
            price = '-'
        else:
            # l_cur:LastTradeWithCurrency
            text = data.split('"l_cur"')[1][0:10]
            text = re.sub('^\W+', '', text)
            price = re.sub('\W+$', '', text)
        dict = {u"realtime_price":price, u"stock_symbol":symbol.upper()}
        return json.dumps(dict, indent = 2)
    except Exception as e:
        return "Error:", e.message
