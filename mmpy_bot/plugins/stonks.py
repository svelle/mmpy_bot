# -*- coding: utf-8 -*-

import re

from mmpy_bot.bot import listen_to
from mmpy_bot.bot import respond_to

import mmpy_bot.stock_lookup as stock


@respond_to('get_stock', re.IGNORECASE)
def web_api_reply(message):
    symbol = str(message.get_message()).replace("get_stock ", "")

    stock_info = stock.look_up_stock(symbol)
    stock_image = stock.plot_last_three_months(symbol)

    content = f"""\n\n\
    | Previous Close |{stock_info['previous_close']}|\n
    |----------------|---|\n
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
