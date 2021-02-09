import mysql.connector as sql
from datetime import datetime

from random import sample
from time import time
from const import DATABASE





class user_db:
    mydb = DATABASE

    @staticmethod
    def create(id, name, surname, middlename, age, diseases, gender):

        cursor = user_db.mydb.cursor()

        sql = "INSERT INTO users (id_tg, name, surname, middlename, age, diseases, gender) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (id, name, surname, middlename, age, gender)
        mycursor.execute(sql, val)
        user_db.mydb.commit()
    @staticmethod
    def create_report(id, name, surname, middlename, age, diseases, gender):
        cursor = user_db.mydb.cursor()
        sql = "INSERT INTO reports (id_tg, name, surname, middlename, age, diseases, gender, time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (id, name, surname, middlename, age, gender, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        mycursor.execute(sql, val)
        user_db.mydb.commit()


    @staticmethod
    def get_users_id():
        cursor = user_db.mydb.cursor()
        request = cursor.execute("SELECT id_tg FROM users")
        # turn into beautiful list
        return [i[0] for i in cursor.fetchall()]

