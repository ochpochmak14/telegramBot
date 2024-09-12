import telebot
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
    
    

bot.polling(non_stop=True)

