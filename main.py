
from random import choice, randint
import telebot
#from telebot import  *
from keyboards import *
from text import text
from user import user
from const import *
import mysql.connector as sql
from sql_requests import *
from geo import geo_to_url
bot = telebot.TeleBot(TOKEN)

user = user()


bot = telebot.TeleBot(TOKEN)

# многоразовый отклик на кнопки в клаве
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    bot.answer_callback_query(callback_query_id=call.id, text=choice(text['rated_callback']))
    # 1 = симптом
    # 0 = заболевание и весь спектр трамв
    if call.data[0] == '1':
        user.setSymptomes(user.getSymptomes()+[call.data[1:]])
    elif call.data[0] == "0":
        user.setDiseases(user.getDiseases()+[call.data[1:]])
    print(user.getSymptomes())
    print(user.getDiseases())


@bot.message_handler(commands=['start'])
def main(message):

    # registration for new users
    if str(message.json['from']['id']) not in user_db.get_users_id():
        sent = bot.send_message(message.chat.id, text['greet_new'])
        bot.register_next_step_handler(sent, getInitials)
        print('User created')
    else:
        sent = bot.send_message(message.chat.id, text['greet_old_beginning']+user_db.getName(message.json['from']['id'])+text['greet_old_ending'])
        bot.register_next_step_handler(sent, menu_selector)



def symptomes_input(message):
    if message.text.lower() == 'готово':
        sent = bot.send_message(message.chat.id, text['chooseDiseases'], reply_markup=keyboard.choose_diseases())
        bot.register_next_step_handler(sent, diseases_input)
    else:
        sent = user.setSymptomes(user.getSymptomes()+message.text.split(', '))
        bot.register_next_step_handler(sent, symptomes_input)

def diseases_input(message):
    if message.text.lower() == 'готово':
        sent = bot.send_message(message.chat.id, text['chooseGeo'])
        bot.register_next_step_handler(sent, geo_input)

    else:
        sent = user.setDiseases(user.getDiseases() + message.text.split(', '))
        bot.register_next_step_handler(sent, diseases_input)








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

def getGender(message):
    if checkForRussian(message.text):
        #не включены остальные гендеры
        user.setGender(1 if message.text == "Мужской" else 0)

        sent = bot.send_message(message.from_user.id,f"{text['info']} \n\n "
                                              f"{text['surname']} {user.getSurname()}\n"
                                              f"{text['firstname']}{user.getName()} \n"
                                              f"{text['middlename']}{user.getMiddleName()}\n"
                                              f"{text['age']} {user.getAge()}\n"
                                              f"{text['gender']}{'мужской' if user.getGender() == 1 else 'женский'}"
                                ,reply_markup=keyboard.main())
        #без болезней, это костыль
        user_db.create(message.json['from']['id'], user.getName(), user.getSurname(), user.getMiddleName(), user.getAge(),
        user.getGender())

        bot.register_next_step_handler(sent, menu_selector)
    else:
        bot.send_message(message.from_user.id, text['wrongMessageInput'])
        bot.register_next_step_handler(message, getGender)


@bot.message_handler(content_types=["location"])
def geo_input(message):
    if message.location is not None:
        # широта долгота
        ID = str(message.json['from']['id'])
        info = user_db.getMainInfo(str(message.json['from']['id']))
#         info = {'name':'Валерий', 'surname':"Павлов", "middlename":"Петрович", "gender":"мужской","age":25}

        geo = geo_to_url(message.location.latitude, message.location.longitude)
        # unworking
        user_db.create_request(ID, info['name'], info['surname'], info['middlename'],
                               info['age'], info['gender'], user.getSymptomes(), user.getDiseases(),
                               geo)
        sent = bot.send_message(message.chat.id, text['request_sended'])
        for DR in DOCTOR_CHATS_ID:
            bot.send_message(DR, f"{text['new_request']} \n\n "
                                 f"{text['surname']} {info['surname']}\n"
                                 f"{text['firstname']}{info['name']} \n"
                                 f"{text['middlename']}{info['middlename']}\n"
                                 f"{text['age']} {info['age']}\n"
                                 f"{text['gender']}{info['gender']}\n\n"
                                 f"Жалобы/травмы:{' '.join(user.getDiseases())}\n\n"
                                 f"Симптомы:{' '.join(user.getSymptomes())}\n\n"
                                 f"Местоположение:\n{geo}")


        bot.register_next_step_handler(sent, menu_selector)

    else:
        sent = bot.send_message(message.chat.id, text['NoneGeo'])
        bot.register_next_step_handler(sent, geo_input)

def getAge(message):
    if 130 >= int(message.text) > 0 and type(eval(message.text)) !=float:
        user.setAge(int(message.text))
        sent = bot.send_message(message.from_user.id, text['genderInput'], reply_markup=keyboard.select_gender())
        bot.register_next_step_handler(sent, getGender)
    else:
        sent = bot.send_message(message.from_user.id, text['wrongMessageInput'])
        bot.register_next_step_handler(sent, getAge)


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