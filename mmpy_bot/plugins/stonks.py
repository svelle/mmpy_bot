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
    search_string = message.get_message()[10:]
    search_result = stock.lookup_symbol(search_string)

    if search_result:
        content = ("\n"
                   f"### Symbol: {search_result['symbol'].upper()}\n"
                   f"#### Company Name: {search_result['name']}\n"
                   f"#### Region: {search_result['region']}\n"
                   f"#### Currency: {search_result['currency']}\n"
                   )
    else:
        content = (f"\n#### Couldn't find info for {search_string.capitalize()}, "
                   "try another search string."
                   )
    message.reply_thread(content)


@listen_to('get info', re.IGNORECASE)
def get_info(message):
    msg_inp = message.get_message().split()
    name = str(msg_inp[2]).upper()

    if len(msg_inp) > 3:
        days = int(msg_inp[-1])
    else:
        days = 90

    stock_info = stock.lookup_stock(name)
    if not stock_info:
        message.reply_thread("\n# Error looking up stock.")
        return
    search_result = stock.lookup_symbol(name)
    if not search_result:
        message.reply_thread("\n# Error looking up stock.")
        return

    stock_image = stock.plot_last_three_months(stock_info['symbol'],
                                               search_result['currency'], days)

    content = ("\n"
               f"### Company Name: [{search_result['name']}](https://finance.yahoo.com/quote/{stock_info['symbol']})\n"
               f"### Symbol: {stock_info['symbol']}\n\n"
               f"### Price: {stock_info['price']}"
               "\n"
               f"| Daily Info         |    |\n"
               "| ------------------- | --- |\n"
               f"| Open               |{stock_info['open']}|\n"
               f"| High               |{stock_info['high']}|\n"
               f"| Low                |{stock_info['low']}|\n"
               f"| Previous Close     |{stock_info['previous_close']}|\n"
               f"| Change             |{stock_info['change']}|\n"
               f"| Change %           |{stock_info['change_percent']}|\n"
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
