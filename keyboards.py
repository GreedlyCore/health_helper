from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from text import symptomes

class keyboard:
    @staticmethod
    def choose_symptome():
        Array = list()
        list_kb = list()
        for i in range(len(symptomes)):
            Array.append(InlineKeyboardButton(symptomes[i], callback_data=symptomes[i]))
            if not ((i+1) % 3):
                list_kb.append(Array)
                Array = []
        if Array not in list_kb:
            list_kb.append(Array)
        btnlist = []

        return InlineKeyboardMarkup(list_kb)

    @staticmethod
    def main():
       kb = ReplyKeyboardMarkup(True)
       kb.row('💊Запрос', 'Голосовое обращение')
       kb.row('Настройки')
       return kb

    @staticmethod
    def select_gender():
        kb = ReplyKeyboardMarkup(True)
        kb.row('Мужской', 'Женский')
        return kb

from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from text import symptomes

class keyboard:
    @staticmethod
    def choose_symptome():
        Array = list()
        list_kb = list()
        for i in range(len(symptomes)):
            Array.append(InlineKeyboardButton(symptomes[i], callback_data=symptomes[i]))
            if not ((i+1) % 3):
                list_kb.append(Array)
                Array = []
        if Array not in list_kb:
            list_kb.append(Array)
        #list_kb = [[InlineKeyboardButton(symptomes[i], callback_data=symptomes[i]) for i in range(j*3, j*3+2)] for j in range(3)]

        btnlist = []

        return InlineKeyboardMarkup(list_kb)
    @staticmethod
    def correctInfo():
        Array = [InlineKeyboardButton("Yes", callback_data="True"),
                 InlineKeyboardButton("No", callback_data="False"),]
        # list_kb = [[InlineKeyboardButton(symptomes[i], callback_data=symptomes[i]) for i in range(j*3, j*3+2)] for j in range(3)]

        return InlineKeyboardMarkup(Array)
    #@staticmethod
    #def settings():
    #    kb = ReplyKeyboardMarkup(True)
    #    kb.row('Статистика')
    #    kb.row('🧨Сбросить рекомендации', '🧠Сбросить статистику')
    #    kb.row('Назад')
    #    return kb