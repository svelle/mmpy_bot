from yfinance import Ticker
import json
import requests


def look_up_stock(symbol):
    ticker = Ticker(symbol)
    stock_data = ticker.info
    interesting_data = dict(
        ask=stock_data["ask"],
        bid=stock_data["bid"],
        beta=stock_data["beta"],
        name=stock_data["longName"],
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
