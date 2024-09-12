import telebot
from telebot import types
from datetime import date
import os
from dotenv import load_dotenv

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
    name_input = types.KeyboardButton('Ввести пациента')
    days_list = types.KeyboardButton('Получить список за каждый день недели')
    
    markup.row(name_input, days_list)
    markup.row(name_list)
    
    bot.send_message(message.chat.id,'Держите список функций!', reply_markup=markup)



bot.polling(non_stop=True)

