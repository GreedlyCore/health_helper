import telebot
from Include.sql import article_db
from keyboards import *
from bs4 import BeautifulSoup
import requests as rq
from sd_parser import *
from fake_headers import Headers
from random import choice, randint
from const import *
from text import text
from os import getcwd
from datetime import datetime
from time import time
import mysql.connector as sql
from sql import *

header = Headers(
    browser="chrome",  # Generate only Chrome UA
    os="win",  # Generate ony Windows platform
    headers=True  # generate misc headers
)



bot = telebot.TeleBot(TOKEN)




@bot.message_handler(commands=['start'])
def main(message):
    sent = bot.send_message(message.chat.id, text['greet'], reply_markup=keyboard.main())

    # register for new users
    if message.chat.id not in user_db.get_users_id():
        user_db.create(message.chat.id)

    bot.register_next_step_handler(sent, menu_selector)


# многоразовый отклик на кнопки в клаве
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.answer_callback_query(callback_query_id=call.id, text=choice(text['rated_callback']))

    mark = float(call.data.split()[0])
    theme = call.data.split()[1:-1]
    article_id = call.data.split()[-1]

    if '&' in theme:
        del (theme[1])
        theme = '_'.join([i.lower() for i in theme])
    else:
        theme = '_'.join([i.lower() for i in theme])

    article_db.rate(article_id, mark)
    user_db.update_count_rated(call.from_user.id, mark)
    user_db.rate(call.from_user.id, theme, mark)
    user_db.add_view(call.from_user.id, article_id, mark)


def settings(message):
    if message.text == '🧨Сбросить рекомендации':
        user_db.reboot_coefs(message.chat.id)
        sent = bot.send_message(message.chat.id, text['reboot'], reply_markup=keyboard.main())
        bot.register_next_step_handler(sent, menu_selector)
    else:
        sent = bot.send_message(message.chat.id, text['wrong'], reply_markup=keyboard.settings())
        bot.register_next_step_handler(sent, settings)


@bot.message_handler(func=lambda message: True)
def menu_selector(message):
    if message.text == '📤Получить статью':
            sent = bot.send_message(message.chat.id, text['back'], reply_markup=keyboard.main())
            bot.register_next_step_handler(sent, menu_selector)

    elif message.text == '⚖Калибровка':
        id = message.chat.id
        sent = bot.send_message(id, text['calibration'], reply_markup=keyboard.main())

        bot.register_next_step_handler(sent, menu_selector)

    elif message.text == '⏰Рассылка':
        sent = bot.send_message(message.chat.id, text['auto'], reply_markup=keyboard.main())
        bot.register_next_step_handler(sent, menu_selector)
    elif message.text == '⚙Настройки':
        sent = bot.send_message(message.chat.id, text['settings'], reply_markup=keyboard.settings())
        bot.register_next_step_handler(sent, settings)
    else:
        sent = bot.send_message(message.chat.id, text['wrong'], reply_markup=keyboard.main())
        bot.register_next_step_handler(sent, menu_selector)


bot.polling()
