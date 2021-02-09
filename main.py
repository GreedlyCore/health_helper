
from keyboards import *

# from random import choice, randint
from const import *

# from time import time
import mysql.connector as sql
#pip install mysql-connector-python
from sql import *

from telebot import  *
import telebot
from keyboards import *
from text import text
from os import getcwd
from user import user
from datetime import datetime



bot = telebot.TeleBot(TOKEN)


user = user()


# многоразовый отклик на кнопки в клаве
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.answer_callback_query(callback_query_id=call.id, text=choice(text['rated_callback']))

    mark = float(call.data.split()[0])
    theme = call.data.split()[1:-1]
    article_id = call.data.split()[-1]






@bot.message_handler(commands=['start'])
def main(message):


    # register for new users
    if message.chat.id not in user_db.get_users_id():
        #-----------------------------------------------------REGISTRATION---------------------------------------------#
        sent = bot.send_message(message.chat.id, text['greet'])
        bot.register_next_step_handler(sent, getInitials)
        user_db.create(message.chat.id, user.getName(), user.getSurname(), user.getMiddleName(), user.getAge(),
                       diseases, user.getGender())


    bot.register_next_step_handler(sent, menu_selector)




@bot.message_handler(func=lambda message: True)
def menu_selector(message):
    if message.text == '🏥Обращение🏥':
            sent = bot.send_message(message.chat.id, text['back'], reply_markup=keyboard.main())
            bot.register_next_step_handler(sent, menu_selector)

    elif message.text == '🎤Голосовое обращение🏥':
        id = message.chat.id
        sent = bot.send_message(id, text['calibration'], reply_markup=keyboard.main())

        bot.register_next_step_handler(sent, menu_selector)

    elif message.text == '⚙Настройки':
        pass
    else:
        sent = bot.send_message(message.chat.id, text['wrong'], reply_markup=keyboard.main())
        bot.register_next_step_handler(sent, menu_selector)


def checkForRussian(text):
    print('Text= ', text)
    for i in text.replace(" ", "").upper():
        print('i=', i)
        print(ord(i))
        if 0 <= ord(i)-1040 <= 31:
            continue
        else:
            return False
    return True

def symptomes(message):
    bot.send_message(message.chat.id, text['chooseSymptomes'],reply_markup=keyboard.choose_symptome())
def info(message):
    bot.send_message(message.from_user.id, text['info']
                     +"\n"+text['surname']+surName+'\n'+text['firstname']+firstName+'\n'+
                     text['middlename']+middleName+'\n'+text['age']+Age+'\n'+text[''])

def getGender(message):
    if checkForRussian(message.text):
        #не включены гендеры-пулеметы
        user.setGender(1 if message.text == "Мужской" else 0)

        bot.send_message(message.from_user.id,f"{text['info']} \n\n "
                                              f"{text['surname']} {user.getSurname()}\n"
                                              f"{text['firstname']}{user.getName()} \n"
                                              f"{text['middlename']}{user.getMiddleName()}\n"
                                              f"{text['age']} {user.getAge()}\n"
                                              f"{text['gender']}{user.getGender()}"
                         , reply_markup=keyboard.correctInfo())

    else:
        bot.send_message(message.from_user.id, text['wrongMessageInput'])
        bot.register_next_step_handler(message, getGender)

def getAge(message):
    try:
        if int(message.text) > 2:
            if int(message.text) <= 130:
                user.setAge(int(message.text))
                bot.send_message(message.from_user.id, text['genderInput'], reply_markup=keyboard.select_gender())
                bot.register_next_step_handler(message, getGender)
            else:
                bot.send_message(message.from_user.id, text['wrongMessageInput'])
                bot.register_next_step_handler(message, getAge)
        else:
            bot.send_message(message.from_user.id, text['ageInput'])
            bot.register_next_step_handler(message, getAge)
    except:
        bot.send_message(message.from_user.id, text['wrongMessageInput'])
        bot.register_next_step_handler(message, getAge)

def getInitials(message):
    if len(message.text.split()) == 3 and message.text.replace(" ", "").isalpha() and checkForRussian(message.text):
        user.setSurname(message.text.split()[0])
        user.setName(message.text.split()[1])
        user.setMiddleName(message.text.split()[2])
        bot.send_message(message.from_user.id, text['ageInput'])
        bot.register_next_step_handler(message, getAge)
    else:
        bot.send_message(message.from_user.id, text['wrongMessageInput'])
        bot.register_next_step_handler(message, getInitials)



bot.polling(none_stop=True, interval=0)