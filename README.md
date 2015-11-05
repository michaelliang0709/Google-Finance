# Google Finance

Get both historical and real-time stock price in NYSE and NASDAQ from Google Finance.

Historical data is got from web crawler, real-time data is got from API.

Other awesome modules: <a href ='https://github.com/hongtaocai/googlefinance'>googlefinance</a> and <a href ='https://github.com/lukaszbanasiak/yahoo-finance'>yahoo-finance</a>.

# Example

```
>>> from Google_Finance import get_hist_price
>>> get_hist_price("goog", "2015.11.4")
{
  "close_price": "728.11", 
  "date": "Nov 04, 2015", 
  "stock_symbol": "GOOG"
}
{
  "realtime_price": "728.11", 
  "stock_symbol": "GOOG"
}
>>> 
>>> from Google_Finance import get_realtime_price
>>> get_realtime_price("goog")
{
  "close_price": "728.11", 
  "date": "Nov 04, 2015", 
  "stock_symbol": "GOOG"
}
{
  "realtime_price": "728.11", 
  "stock_symbol": "GOOG"
}
```
