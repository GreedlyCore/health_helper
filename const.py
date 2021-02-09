import mysql.connector as sql

TOKEN = "1530239123:AAFzSI5EhoOuT3tfzr1sPnT2dHqmnhRXT4Y"
DATABASE = sql.connect(
    host="127.0.0.1",
    user="root",
    port="3306",
    password="12345",#password="123456789bb",
    database="sys"
)
DOCTOR_CHATS_ID = [426578062]