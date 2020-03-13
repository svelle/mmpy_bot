# -*- coding: utf-8 -*-

import re

from mmpy_bot.bot import listen_to
from mmpy_bot.bot import respond_to

import mmpy_bot.stock_lookup as stock


@respond_to('help', re.IGNORECASE)
def help(message):
    content = ("\n"
               "#### Stonkbot for maximum Stonks!!!\n"
               "#### Available Commands:\n"
               "- `get info`: Gets info for a given stock symbol.\n"
               "- `get symbol`: Tries to get the symbol for a given company name.\n"
               )
    message.reply_thread(content)


@listen_to('get symbol', re.IGNORECASE)
def get_symbol(message):
    msg_inp = message.get_message().split()
    name = str(msg_inp[-1])

    search_result = stock.find_symbol_name(name)
    if search_result:
        content = ("\n"
                   f"### Symbol: {search_result['symbol'].upper()}\n"
                   f"#### Company Name: {search_result['name']}\n"
                   f"#### Exchange: {search_result['exchange']}\n"
                   )
    else:
        content = (f"\n#### Couldn't find info for {name}, "
                   "try another search string."
                   )
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

    content = ("\n"
               f"### Company Name: [{stock_info['name']}](https://finance.yahoo.com/quote/{symbol}])\n"
               f"### Symbol: {symbol}\n\n"
               "\n"
               f"| Previous Close |{stock_info['previous_close']}|\n"
               "| ---------------- | --- |\n"
               f"| Open           |{stock_info['open']}|\n"
               f"| Bid            |{stock_info['bid']}|\n"
               f"| Ask            |{stock_info['ask']}|\n"
               f"| Beta           |{stock_info['beta']}|\n"
               f"| Day's Range    |{stock_info['days_range']}|\n"
               f"| 52 Week Range  |{stock_info['weeks_range']}|\n"
               )

    file = open(stock_image, "rb")
    result = message.upload_file(file)
    file.close()
    if 'file_infos' not in result:
        message.reply('upload file error')
    file_id = result['file_infos'][0]['id']
    # file_id need convert to array
    message.reply_thread(content, [file_id])


help.__doc__ = "Shows the available commands for Stonkbot."
