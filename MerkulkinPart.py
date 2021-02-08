from telebot import  *
import telebot
from keyboards import *
from text import text
from os import getcwd

File = open("TOKEN", "r").read()
bot = telebot.TeleBot(File)
middleName = 'не заполнено'
surName = 'не заполнено'
firstName = 'не заполнено'
Age = 'не заполнено'
Symptoms = 'не заполнено'
Adress = "не заполнено"
commands = ["/start", "/options"]
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
bot.polling(none_stop=True, interval=0)