from yfinance import Ticker


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
