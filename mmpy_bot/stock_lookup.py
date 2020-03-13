from yfinance import Ticker, download
import json
import requests
from datetime import date, timedelta
import matplotlib.pyplot as plt


def look_up_stock(symbol):
    ticker = Ticker(symbol)
    stock_data = ticker.info
    interesting_data = dict(
        ask=stock_data["ask"],
        bid=stock_data["bid"],
        beta=stock_data["beta"],
        name=stock_data["longName"],
        open=stock_data["open"],
        weeeks_range=f"{stock_data['fiftyTwoWeekLow']} - {stock_data['fiftyTwoWeekHigh']}",
        days_range=f"{stock_data['dayLow']} - {stock_data['dayHigh']}",
        currency=stock_data["currency"],
        previous_close=stock_data["previousClose"]
    )
    return interesting_data


def find_symbol_name(query):
    response = requests.get(
        f"http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={query}&lang=en"
    ).content
    response = json.loads(response)
    try:
        symbol_candidate = response["ResultSet"]["Result"][0]
    except IndexError:
        return False
    return dict(
        symbol=symbol_candidate["symbol"],
        name=symbol_candidate["name"],
        exchange=symbol_candidate["exch"],
    )


def plot_last_three_months(symbol, currency="US-Dollar"):
    today = date.today()
    three_months_ago = today - timedelta(days=90)
    data = download(symbol, three_months_ago, today)
    data["Adj Close"].plot(title=f"{symbol} - Last three months")
    plt.ylabel(currency)
    plt.savefig("plot.png")
    return "plot.png"
