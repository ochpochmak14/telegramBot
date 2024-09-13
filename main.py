import telebot
import sqlite3
from telebot import types
from datetime import date
import os
from dotenv import load_dotenv
from isvalid_isthat_func import *
from db import *
load_dotenv()

My_Token = os.getenv('TOKEN')
bot = telebot.TeleBot(My_Token)


cur_weekday = date.today()

today = date.today()
today1 = str(date.today())
dtoday = today.strftime("%d/%m/%Y")



@bot.message_handler(commands=['start'])
def start(message):
    global my_d
    global user_id
    user_id = message.from_user.id
    
    conn = sqlite3.connect('my_database.db')
    cur = conn.cursor()
    
    cur.execute('CREATE TABLE IF NOT EXISTS data (tg_id int, lastname text,name text,surname text,date text, date2 text)')
    conn.commit()
    cur.close()
    conn.close()
    
    
    my_message = f'Здравствуйте, <b>Dr.</b><b>{message.from_user.first_name}</b>'
    bot.send_message(message.chat.id, my_message, parse_mode='html')
    
    markup = types.ReplyKeyboardMarkup()
    
    name_list = types.KeyboardButton('Получить список пациентов за сегодня')
    name_input = types.KeyboardButton('Внести пациента')
    days_list = types.KeyboardButton('Получить список за каждый день недели')
    
    markup.row(name_input, days_list)
    markup.row(name_list)
    
    bot.send_message(message.chat.id,'Держите список функций!', reply_markup=markup)
    bot.register_next_step_handler(message, branches)

bot.message_handler(content_types=['text'])       
def branches(message):
    if message.text == 'Внести пациента':
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        btn1 = types.KeyboardButton('Да')
        btn2 = types.KeyboardButton('Нет')
        btn3 = types.KeyboardButton('Главное меню')
        markup1.add(btn1, btn2)
        markup1.add(btn3)
        
        bot.send_message(message.chat.id, 'Введите фамилию: ', reply_markup=markup1)
            
        bot.register_next_step_handler(message, get_lastname)
    
    elif message.text == 'Получить список пациентов за сегодня':
        
       
        conn = sqlite3.connect('my_database.db')
        cur = conn.cursor()
        
        cur.execute(f'SELECT * FROM data WHERE tg_id = {user_id}')
        us = cur.fetchall()
        ans = ""
        for i in us:
            if i[5] == today1:
                ans += f'ФИО: {i[1]}, {i[2]}, {i[3]}, Дата рождения - {i[4]}\n'
       
        cur.close()
        conn.close()
        
        
        bot.send_message(message.chat.id, ans)
        start(message)
        
    
    elif message.text == 'Получить список за каждый день недели':
        
         conn = sqlite3.connect('my_database.db')
         cur = conn.cursor()
        
         cur.execute(f'SELECT * FROM data WHERE tg_id = {user_id}')
         us = cur.fetchall()
         ans = ""
         for i in us:
             
             ans += f'ФИО: {i[1]}, {i[2]}, {i[3]}, Дата рождения - {i[4]}\n, День посещения - {i[5]}\n'
        
         cur.close()
         conn.close()
        
        
        #  bot.register_next_step_handler(message,start)
         bot.send_message(message.chat.id, ans)
         start(message)
    
    else:
        bot.send_message(message.chat.id, 'Выберите одну из опций!༼ つ ◕_◕ ༽つ')
        bot.register_next_step_handler(message, branches)


def get_lastname(message):
    global lastname
    
    if message.text == 'Главное меню':
            start(message)
            
    elif(is_validate_string(message.text)):
        lastname = message.text
        bot.send_message(message.chat.id, 'Введите Имя: ')
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.chat.id, 'Введите фамилию: ')
        bot.register_next_step_handler(message, get_lastname)


def get_name(message):
    global name
    if message.text == 'Главное меню':
            start(message)
            
    elif(is_validate_string(message.text)):
        name = message.text
        bot.send_message(message.chat.id, 'Введите Отчество: ')
        bot.register_next_step_handler(message, get_surname)
    else:
    
        bot.send_message(message.chat.id, 'Введите Имя: ')
        bot.register_next_step_handler(message, get_name)
    
    
def get_surname(message):
    global surname
    if message.text == 'Главное меню':
            start(message)
            
    elif(is_validate_string(message.text)):
        surname = message.text
        markup2 = types.ReplyKeyboardMarkup()
    
        yes_k = types.KeyboardButton('Да')
        no_k = types.KeyboardButton('Нет')
    
        markup2.add(yes_k)
        markup2.add(no_k)

        
        bot.send_message(message.chat.id, f'Фамилия - {lastname}, Имя - {name}, Отчество - {surname} || <b>Все верно?</b> ',reply_markup=markup2, parse_mode='html')
        bot.register_next_step_handler(message, callback_one)
    else:
        bot.send_message(message.chat.id, 'Введите Отчество: ')
        bot.register_next_step_handler(message, get_surname)    


def get_date(message):
    global birth_date
    if message.text == 'Главное меню':
            start(message)
            
    elif(is_validate_date(message.text)):
        birth_date = message.text
        
        markup001 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        btn1 = types.KeyboardButton('Да')
        btn2 = types.KeyboardButton('Нет')
        
        bot.send_message(message.chat.id, f'Дата рождения - {birth_date}? <b>Все верно?</b>', reply_markup=markup001, parse_mode='html')
        bot.register_next_step_handler(message, callback_two)
    else:
        bot.send_message(message.chat.id, 'Введите дату рождения')
        bot.register_next_step_handler(message, get_date)


def callback_one(message):
    if(message.text == 'Нет'):
        bot.delete_message(message.chat.id, message.message_id)
        bot.register_next_step_handler(message, start)
        
        
    else:
        bot.send_message(message.chat.id, 'OK')
        # my_d["users"][str(message.chat.id)].append({
        #     str(cur_weekday) : []
        #     str(dtoday) : []
        # })
        bot.send_message(message.chat.id, 'Введите дату рождения в формате ГГ.ДД.ММ')
        bot.register_next_step_handler(message, get_date)
    
        
def callback_two(message):
    if message.text == 'Нет':
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, 'Введите дату рождения')
        bot.register_next_step_handler(message,get_date)
        
    else:
     
        conn = sqlite3.connect('my_database.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO data VALUES (?, ?, ?, ?, ?, ?)", (user_id, lastname, name, surname, birth_date, today1))
        conn.commit()
        cur.close()
        conn.close()
    
        markup002 = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton('Главное меню')
        markup002.add(btn1)
        bot.send_message(message.chat.id, 'OK', reply_markup=markup002)
        
        # my_d[user_id]["todat"].append([lastname,name,surname,birth_date])
        
        bot.register_next_step_handler(message, start)
        


bot.polling(non_stop=True)

