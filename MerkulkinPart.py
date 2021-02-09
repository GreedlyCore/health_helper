from telebot import  *
import telebot
from keyboards import *
from text import text
from os import getcwd
from user import user
File = open("TOKEN", "r").read()
bot = telebot.TeleBot(File)
user = user()
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
    print(surName, firstName, middleName, message.chat.id, message.from_user.id)

    bot.send_message(message.chat.id, text['chooseSymptomes'],reply_markup=keyboard.choose_symptome())
def info(message):
    bot.send_message(message.from_user.id, text['info']
                     +"\n"+text['surname']+surName+'\n'+text['firstname']+firstName+'\n'+
                     text['middlename']+middleName+'\n'+text['age']+Age+'\n'+text[''])


@bot.message_handler(commands=['start'])
def getTextMessages(message):
    global typed
    bot.send_message(message.from_user.id, text["greet"])
    bot.register_next_step_handler(message, getInitials)

def gender(message):
    if len(message.text) != 1:
        bot.send_message(message.from_user.id, text['wrongMessageInput'])
        bot.register_next_step_handler(message, gender)
    elif not message.text.isalpha():
        user.setGender(message.text)
        print(user.getGender())
        bot.send_message(message.from_user.id, text['info']
                         + "\n" + text['surname'] + str(user.getSurname()) + '\n' + text['firstname'] + str(user.getName()) + '\n' +
                         text['middlename'] + str(user.getMiddleName()) + '\n' + text['age'] + str(user.getAge()) + '\n' + text['gender'] + str(user.getGender()), reply_markup=keyboard.correctInfo())

def age(message):
    try:
        if int(message.text) > 2:
            if int(message.text) <= 130:
                user.setAge(int(message.text))
                bot.send_message(message.from_user.id, text['genderInput'])
                bot.register_next_step_handler(message, gender)
            else:
                bot.send_message(message.from_user.id, text['wrongMessageInput'])
                bot.register_next_step_handler(message, age)
        else:
            bot.send_message(message.from_user.id, text['ageInput'])
            bot.register_next_step_handler(message, age)
    except:
        bot.send_message(message.from_user.id, text['wrongMessageInput'])
        bot.register_next_step_handler(message, age)

def getInitials(message):
    if len(message.text.split()) == 3 and message.text.replace(" ", "").isalpha() and checkForRussian(message.text):
        user.setSurname(message.text.split()[0])
        user.setName(message.text.split()[1])
        user.setMiddleName(message.text.split()[2])
        bot.send_message(message.from_user.id, text['ageInput'])
        bot.register_next_step_handler(message, age)
    else:
        bot.send_message(message.from_user.id, text['wrongMessageInput'])
        bot.register_next_step_handler(message, getInitials)


    #if message.text not in commands:
    #    Message = message.text.split()
    #    try:
    #        user.setSurname(Message[0])
    #        try:
    #            user.setName(Message[1])
    #            try:
    #                user.setMiddleName(Message[2])
    #                bot.send_message(message.from_user.id, text['age'])
    #                bot.register_next_step_handler(message, options)
    #            except:
    #                user.setSurname('не заполнено')
    #                user.setName('не заполнено')
    #                user.setMiddleName('не заполнено')
    #                bot.send_message(message.from_user.id, text['wrongMiddlenameInput'])
    #                bot.register_next_step_handler(message, Get_FIO)
    #        except:
    #            middleName = 'не заполнено'
    #            surName = 'не заполнено'
    #            firstName = 'не заполнено'
    #            bot.send_message(message.from_user.id, text['wrongFirstnameInput'])
    #            bot.register_next_step_handler(message, Get_FIO)
    #    except:
    #        middleName = 'не заполнено'
    #        surName = 'не заполнено'
    #        firstName = 'не заполнено'
    #        bot.send_message(message.from_user.id, text['wrongSurnameInput'])
    #        bot.register_next_step_handler(message, Get_FIO)
    #else:
    #    bot.send_message(message.from_user.id, text['wrongMessageInput'])
    #    bot.register_next_step_handler(message, Get_FIO)
bot.polling(none_stop=True, interval=0)

