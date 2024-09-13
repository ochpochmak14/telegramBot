import telebot
import sqlite3
from telebot import types
from datetime import date
import os
from dotenv import load_dotenv
from isvalid_isthat_func import *

load_dotenv()

My_Token = os.getenv('TOKEN')
bot = telebot.TeleBot(My_Token)
date_now = date.today()


@bot.message_handler(commands=['start'])
def start(message):
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
        
        markup1.add(btn1, btn2)
        
        bot.send_message(message.chat.id, 'Введите фамилию: ', reply_markup=markup1)
            
        bot.register_next_step_handler(message, get_lastname)
    
    elif message.text == 'Получить список пациентов за сегодня':
        pass
    
    elif message.text == 'Получить список за каждый день недели':
        pass
    
    else:
        bot.send_message(message.chat.id, 'Выберите одну из опций!༼ つ ◕_◕ ༽つ')
        bot.register_next_step_handler(message, branches)


def get_lastname(message):
    global lastname
    if(is_validate_string(message.text)):
        lastname = message.text
        bot.send_message(message.chat.id, 'Введите Имя: ')
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.chat.id, 'Введите фамилию: ')
        bot.register_next_step_handler(message, get_lastname)


def get_name(message):
    global name
    if(is_validate_string(message.text)):
        name = message.text
        bot.send_message(message.chat.id, 'Введите Отчество: ')
        bot.register_next_step_handler(message, get_surname)
    else:
    
        bot.send_message(message.chat.id, 'Введите Имя: ')
        bot.register_next_step_handler(message, get_name)
    
    
def get_surname(message):
    global surname
    if(is_validate_string(message.text)):
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
    if(is_validate_date(message.text)):
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
        bot.send_message(message.chat.id, 'Введите дату рождения в формате ГГ.ДД.ММ')
        bot.register_next_step_handler(message, get_date)
    
        
def callback_two(message):
    if message.text == 'Нет':
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, 'Введите дату рождения')
        bot.register_next_step_handler(message,get_date)
        
    else:
        bot.send_message(message.chat.id, 'OK')
        


bot.polling(non_stop=True)

