from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from text import symptomes, diseases


class keyboard:
    @staticmethod
    def choose_symptome():
        Array = list()
        list_kb = list()
        for i in range(len(symptomes)):
            Array.append(InlineKeyboardButton(symptomes[i], callback_data="1"+symptomes[i]))
            if not ((i+1) % 3):
                list_kb.append(Array)
                Array = []
        if Array not in list_kb:
            list_kb.append(Array)

        return InlineKeyboardMarkup(list_kb)


    @staticmethod
    def choose_diseases():
        Array = list()
        list_kb = list()
        for i in range(len(diseases)):
            Array.append(InlineKeyboardButton(diseases[i], callback_data="0" + diseases[i]))
            if not ((i + 1) % 3):
                list_kb.append(Array)
                Array = []
        if Array not in list_kb:
            list_kb.append(Array)

        return InlineKeyboardMarkup(list_kb)
    @staticmethod
    def main():
       kb = ReplyKeyboardMarkup(True)
       kb.row('🏥Обращение🏥', '🎤Голосовое обращение🏥')
       kb.row('⚙Настройки')
       return kb

    @staticmethod
    def select_gender():
        kb = ReplyKeyboardMarkup(True)
        kb.row('Мужской', 'Женский')
        return kb

    @staticmethod
    def gender():
        Array = [[InlineKeyboardButton("Мужской", callback_data=1),
                 InlineKeyboardButton("Женский", callback_data=0),]]
        return InlineKeyboardMarkup(Array)
    @staticmethod
    def correctInfo():
        Array = [[InlineKeyboardButton("Yes", callback_data="True"),
                 InlineKeyboardButton("No", callback_data="False"),]]


        return InlineKeyboardMarkup(Array)
