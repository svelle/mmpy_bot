from yfinance import Ticker, download
import json
import requests
from datetime import date, timedelta

import mmpy_bot_settings as settings

from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt

ts = TimeSeries(key=settings.VANTAGE_KEY)


def lookup_stock(query: str):
    try:
        data = ts.get_quote_endpoint(query)[0]
    except IndexError:
        return False
    print(data)
    return dict(
        symbol=data['01. symbol'],
        open=data['02. open'],
        high=data['03. high'],
        low=data['04. low'],
        price=data['05. price'],
        volume=data['06. volume'],
        lates_trading_day=data['07. latest trading day'],
        previous_close=data['08. previous close'],
        change=data['09. change'],
        change_percent=data['10. change percent'],
    )


def lookup_symbol(query: str):
    try:
        data = ts.get_symbol_search(query)
    except ValueError:
        return False
    if not data[0]:
        return False
    else:
        data = data[0][0]
    return dict(
        symbol=data['1. symbol'],
        name=data['2. name'],
        region=data['4. region'],
        currency=data['8. currency'],
    )


def plot_last_three_months(symbol: str, currency="USD", days=90):
    today = date.today()
    three_months_ago = today - timedelta(days)
    data = download(symbol, three_months_ago, today)
    data["Adj Close"].plot(title=f"{symbol.upper()} - Last {days} days")
    plt.ylabel(currency)
    plt.savefig("plot.png")
    plt.clf()
    return "plot.png"
