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
        #for i in range(0, len(symptomes), 3):
        #    btn = InlineKeyboardButton(text=symptomes[i], callback_data=symptomes[i])
        #    btnlist.append(btn)
        #    if (i+1) % 3 == 0:
        #        kb.row(btnlist)
        #        print(kb, btnlist)
        #        btnlist.clear()
            #kb.add(InlineKeyboardButton(symptomes[i], callback_data=symptomes[i]))
            #kb.add(InlineKeyboardButton(symptomes[i+1], callback_data=symptomes[i+1]))
            #kb.add(InlineKeyboardButton(symptomes[i+2], callback_data=symptomes[i+2]))

        return InlineKeyboardMarkup(list_kb)

    #@staticmethod
    #def settings():
    #    kb = ReplyKeyboardMarkup(True)
    #    kb.row('Статистика')
    #    kb.row('🧨Сбросить рекомендации', '🧠Сбросить статистику')
    #    kb.row('Назад')
    #    return kb