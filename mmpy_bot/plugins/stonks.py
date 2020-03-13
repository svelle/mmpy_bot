# -*- coding: utf-8 -*-

import re

from mmpy_bot.bot import listen_to

import mmpy_bot.stock_lookup as stock


@listen_to('get symbol', re.IGNORECASE)
def get_symbol(message):
    msg_inp = message.get_message().split()
    name = str(msg_inp[-1]).upper()

    search_result = stock.find_symbol_name(name)

    content = f"""\n ### Symbol: {search_result['symbol']}
#### Company Name: {search_result['name']}
#### Exchange: {search_result['exchange']}
"""
    message.reply_thread(content)


@listen_to('get info', re.IGNORECASE)
def get_info(message):
    msg_inp = message.get_message().split()
    symbol = str(msg_inp[-1]).upper()

    try:
        stock_info = stock.look_up_stock(symbol)
    except IndexError:
        message.reply_thread(
            "\n## Symbol not found!\n### Trying lookup for queried Symbol...")
        get_symbol(message)
        return

    stock_image = stock.plot_last_three_months(symbol, stock_info['currency'])

    content = f"""\n### Company Name: [{stock_info['name']}](https://finance.yahoo.com/quote/{symbol}])
### Symbol: {symbol}

| Previous Close |{stock_info['previous_close']}|
| ---------------- | --- |
| Open           |{stock_info['open']}|
| Bid            |{stock_info['bid']}|
| Ask            |{stock_info['ask']}|
| Beta           |{stock_info['beta']}|
| Day's Range    |{stock_info['days_range']}|
| 52 Week Range  |{stock_info['weeks_range']}|
"""

    file = open(stock_image, "rb")
    result = message.upload_file(file)
    file.close()
    if 'file_infos' not in result:
        message.reply('upload file error')
    file_id = result['file_infos'][0]['id']
    # file_id need convert to array
    message.reply_thread(content, [file_id])


get_symbol.__doc__ = "Try's to lookup the symbol for a given company name."
get_info.__doc__ = "Try's to lookup data for the given symbol."
