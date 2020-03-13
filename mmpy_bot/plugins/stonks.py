# -*- coding: utf-8 -*-

import re

from mmpy_bot.bot import listen_to
from mmpy_bot.bot import respond_to

import mmpy_bot.stock_lookup as stock

@respond_to('get symbol',  re.IGNORECASE)
def get_symbol(message):
    name = str(message.get_message().replace("get symbol ", ""))
    search_result = stock.find_symbol_name(name)

    content = f"\n ### Symbol: {search_result['symbol']} \n#### Company Name: {search_result['name']}\n#### Exchange: {search_result['exchange']}\n"
    message.reply(content)


@respond_to('get info', re.IGNORECASE)
def get_info(message):
    symbol = str(message.get_message()).replace("get info ", "")

    stock_info = stock.look_up_stock(symbol)
    stock_image = stock.plot_last_three_months(symbol)

    # | ---------------- | --- |\n

    content = f"""\n\n\
    # {stock_info['name']}
    ## {symbol}

    | Previous Close |{stock_info['previous_close']}|\n
    | Open           |{stock_info['open']}|\n
    | Bid            |{stock_info['bid']}|\n
    | Ask            |{stock_info['ask']}|\n
    | Beta           |{stock_info['beta']}|\n
    | Day's Range    |{stock_info['days_range']}|\n
    | 52 Week Range  |{stock_info['weeks_range']}|"""

    file = open(stock_image, "rb")
    result = message.upload_file(file)
    file.close()
    if 'file_infos' not in result:
        message.reply('upload file error')
    file_id = result['file_infos'][0]['id']
    # file_id need convert to array
    message.reply(content, [file_id])
