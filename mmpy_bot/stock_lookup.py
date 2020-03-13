from yfinance import Ticker, download
import json
import requests
from datetime import date, timedelta
import matplotlib.pyplot as plt


def look_up_stock(symbol: str):
    ticker = Ticker(symbol)
    stock_data = ticker.info
    currency = stock_data["currency"]
    interesting_data = dict(
        ask=f"{stock_data['ask']} {currency}",
        bid=f"{stock_data['bid']} {currency}",
        beta=round(stock_data["beta"], 2),
        name=stock_data["longName"],
        open=f"{stock_data['open']} {currency}",
        weeks_range=f"{round(stock_data['fiftyTwoWeekLow'], 2)} {currency} - {round(stock_data['fiftyTwoWeekHigh'], 2)} {currency}",
        days_range=f"{round(stock_data['dayLow'], 2)} {currency} - {round(stock_data['dayHigh'], 2)} {currency}",
        currency=currency,
        previous_close=f'{stock_data["previousClose"]} {currency}',
        dividend_rate=f"{stock_data['dividendRate']}%",
    )
    return interesting_data


def find_symbol_name(query: str):
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


def plot_last_three_months(symbol: str, currency="USD"):
    today = date.today()
    three_months_ago = today - timedelta(days=90)
    data = download(symbol, three_months_ago, today)
    data["Adj Close"].plot(title=f"{symbol.upper()} - Last three months")
    plt.ylabel(currency)
    plt.savefig("plot.png")
    plt.clf()
    return "plot.png"
