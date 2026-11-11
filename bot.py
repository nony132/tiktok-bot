import os
import telebot
from flask import Flask, request

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://' + os.getenv('RENDER_EXTERNAL_HOSTNAME', 'your-app.onrender.com') + '/' + TOKEN)
    return "Bot is running!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
