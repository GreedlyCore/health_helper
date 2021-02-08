# import telebot
# from Include.sql import article_db
# from keyboards import *
# from bs4 import BeautifulSoup
# import requests as rq
# from sd_parser import *
# from fake_headers import Headers
# from random import choice, randint
# from const import *
# from text import text
# from os import getcwd
# from datetime import datetime
# from time import time
# import mysql.connector as sql
# from sql import *

from telebot import  *
import telebot
from keyboards import *
from text import text
from os import getcwd

# header = Headers(
#     browser="chrome",  # Generate only Chrome UA
#     os="win",  # Generate ony Windows platform
#     headers=True  # generate misc headers
# )



bot = telebot.TeleBot(TOKEN)


class user:
    def __init__(self, name, surname, patronymic, age, symptoms, address):
        self.name = 'не заполнено'
        self.surname = 'не заполнено'
        self.patronymic = 'не заполнено'
        self.age = 'не заполнено'
        self.symptoms = 'не заполнено'
        self.address = "не заполнено"




@bot.message_handler(commands=['start'])
def main(message):
    sent = bot.send_message(message.chat.id, text['greet'], reply_markup=keyboard.main())

    # register for new users
    if message.chat.id not in user_db.get_users_id():
        registration()
        # user_db.create(message.chat.id)

    bot.register_next_step_handler(sent, menu_selector)


# многоразовый отклик на кнопки в клаве
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.answer_callback_query(callback_query_id=call.id, text=choice(text['rated_callback']))

    mark = float(call.data.split()[0])
    theme = call.data.split()[1:-1]
    article_id = call.data.split()[-1]



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


bot.polling(none_stop=True, interval=0)







def options(message):
    print(surName, firstName, middleName)

    bot.send_message(message.chat.id, text['chooseSymptomes'],reply_markup=keyboard.choose_symptome())
    bot.send_message(message.from_user.id, text['info']
                     +"\n"+text['surname']+surName+'\n'+text['firstname']+firstName+'\n'+
                     text['middlename']+middleName+'\n'+text['age']+Age)


@bot.message_handler(commands=['start'])
def getTextMessages(message):
    global typed
    bot.send_message(message.from_user.id, text["greet"])
    bot.register_next_step_handler(message, options)

def Get_FIO(message):
    global middleName, firstName, surName
    if message.text not in commands:
        Message = message.text.split()
        try:
            surName = Message[0]
            try:
                firstName = Message[1]
                try:
                    middleName = Message[2]

                except:
                    middleName = 'не заполнено'
                    surName = 'не заполнено'
                    firstName = 'не заполнено'
                    bot.send_message(message.from_user.id, text['wrongMiddlenameInput'])
                    bot.register_next_step_handler(message, Get_FIO)
                options(message)
            except:
                middleName = 'не заполнено'
                surName = 'не заполнено'
                firstName = 'не заполнено'
                bot.send_message(message.from_user.id, text['wrongFirstnameInput'])
                bot.register_next_step_handler(message, Get_FIO)
        except:
            middleName = 'не заполнено'
            surName = 'не заполнено'
            firstName = 'не заполнено'
            bot.send_message(message.from_user.id, text['wrongSurnameInput'])
            bot.register_next_step_handler(message, Get_FIO)
    else:
        bot.send_message(message.from_user.id, text['wrongMessageInput'])
        bot.register_next_step_handler(message, Get_FIO)

