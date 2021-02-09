
from random import choice, randint
import mysql.connector as sql
from telebot import  *
import telebot
from keyboards import *
from text import text
from os import getcwd
from user import user
from const import *
import mysql.connector as sql
from sql import *
bot = telebot.TeleBot(TOKEN)

user = user()


bot = telebot.TeleBot(TOKEN)

# многоразовый отклик на кнопки в клаве
# 1 = симптом
# 0 = заболевание и весь спектр трамв

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.answer_callback_query(callback_query_id=call.id, text=choice(text['rated_callback']))
    if call.data[0] == '1':
        user.setSymptomes(user.getSymptomes()+[call.data[1:]])
    elif call.data[0] == "0":
        user.setDiseases(user.getDiseases()+[call.data[1:]])
    print(user.getSymptomes())
    print(user.getDiseases())







@bot.message_handler(commands=['start'])
def main(message):

    # register for new users
    if message.chat.id not in user_db.get_users_id():
    #-----------------------------------------------------REGISTRATION---------------------------------------------#
        sent = bot.send_message(message.chat.id, text['greet_new'])
        bot.register_next_step_handler(sent, getInitials)

        print('Success')
    else:
        sent = bot.send_message(message.chat.id, text['greet_old_beginning']+user_db.getName(message.chat.id)+text['greet_old_ending'])

        bot.register_next_step_handler(sent, menu_selector)



def symptomes_input(message):
    if message.text.lower() == 'конец':
        sent = bot.send_message(message.chat.id, text['chooseDiseases'], reply_markup=keyboard.choose_diseases())
        bot.register_next_step_handler(sent, diseases_input)
    else:
        user.setSymptomes(user.getSymptomes()+message.text.split(', '))
        bot.register_next_step_handler(sent, symptomes_input)

def diseases_input(message):
    if message.text.lower() == 'конец':
        sent = bot.send_message(message.chat.id, text['chooseGeo'])
        bot.register_next_step_handler(sent, geo_input)

    else:
        user.setDiseases(user.getDiseases() + message.text.split(', '))
        bot.register_next_step_handler(sent, diseases_input)




@bot.message_handler(content_types=["location"])
def geo_input(message):
    if message.location is not None:
        print(message.location)
        print("latitude: %s; longitude: %s" % (message.location.latitude, message.location.longitude)) #широта долгота
        user.setAddress([message.location.latitude, message.location.longitude])
        id = message.chat.id
        user_db.create_request(id, user_db.getName(id), user_db.getSurName(id), user_db.getMiddleName(id), user_db.getAge(id), user.getSymptomes(), user.getDiseases(), [message.location.latitude, message.location.longitude])
    else:
        sent = bot.send_message(message.chat.id, text['NoneGeo'])
        bot.register_next_step_handler(sent, geo_input)





@bot.message_handler(func=lambda message: True)
def menu_selector(message):
    if message.text == '🏥Обращение🏥':
            sent = bot.send_message(message.chat.id, text['chooseSymptomes'], reply_markup=keyboard.choose_symptome())
            bot.register_next_step_handler(sent, symptomes_input)

    elif message.text == '🎤Голосовое обращение🏥':
        pass

    elif message.text == '⚙Настройки':
        pass
    else:
        sent = bot.send_message(message.chat.id, text['wrongMessageInput'], reply_markup=keyboard.main())
        bot.register_next_step_handler(sent, menu_selector)


def checkForRussian(text):
    for i in text.replace(" ", "").upper():
        if 0 <= ord(i)-1040 <= 31:
            continue
        else:
            return False
    return True

def symptomes(message):
    bot.send_message(message.chat.id, text['chooseSymptomes'],reply_markup=keyboard.choose_symptome())


def getGender(message):
    if checkForRussian(message.text):
        #не включены гендеры-пулеметы
        user.setGender(1 if message.text == "Мужской" else 0)

        sent = bot.send_message(message.from_user.id,f"{text['info']} \n\n "
                                              f"{text['surname']} {user.getSurname()}\n"
                                              f"{text['firstname']}{user.getName()} \n"
                                              f"{text['middlename']}{user.getMiddleName()}\n"
                                              f"{text['age']} {user.getAge()}\n"
                                              f"{text['gender']}{'мужской' if user.getGender() == 1 else 'женский'}"
                                ,reply_markup=keyboard.main())
        #без болезней, это костыль
        user_db.create(message.chat.id, user.getName(), user.getSurname(), user.getMiddleName(), user.getAge(),
        user.getGender()) #list(set(user.getDiseases())),

        bot.register_next_step_handler(sent, menu_selector)
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