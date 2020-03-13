# -*- coding: utf-8 -*-

import re

from mmpy_bot.bot import listen_to
from mmpy_bot.bot import respond_to

import mmpy_bot.stock_lookup as stock

@respond_to('get symbol',  re.IGNORECASE)
def get_symbol(message):
    input = message.get_message().split()
    name = input[-1]

    search_result = stock.find_symbol_name(name)

    content = f"\n ### Symbol: {search_result['symbol']} \n#### Company Name: {search_result['name']}\n#### Exchange: {search_result['exchange']}\n"
    message.reply_thread(content)


@respond_to('get info', re.IGNORECASE)
def get_info(message):
    input = message.get_message().split()
    symbol = input[-1]

    try:
        stock_info = stock.look_up_stock(symbol)
    except IndexError:
        message.reply_thread("\n## Symbol not found!\n### Trying lookup for queried Symbol...")
        get_symbol(message)
        return


    stock_image = stock.plot_last_three_months(symbol)

    content = f"\n\n### Company Name: [{stock_info['name']}](https://finance.yahoo.com/quote/{symbol}])\n### Symbol: {symbol}\n\n| Previous Close |{stock_info['previous_close']}|\n| ---------------- | --- |\n| Open           |{stock_info['open']}|\n| Bid            |{stock_info['bid']}|\n| Ask            |{stock_info['ask']}|\n| Beta           |{stock_info['beta']}|\n| Day's Range    |{stock_info['days_range']}|\n| 52 Week Range  |{stock_info['weeks_range']}|"

    file = open(stock_image, "rb")
    result = message.upload_file(file)
    file.close()
    if 'file_infos' not in result:
        message.reply('upload file error')
    file_id = result['file_infos'][0]['id']
    # file_id need convert to array
    message.reply_thread(content, [file_id])
