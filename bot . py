import os
from flask import Flask
import telebot

TOKEN = "9068039553:AAF1N1q_gdqH7120KAikDsn2PYJeQMSVeCw"
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is active!"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! The bot is running 24/7 successfully.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
