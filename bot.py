import os
import telebot
from flask import Flask
import yt_dlp

TOKEN = "9068039553:AAF1N1q_gdqH7120KAikDsn2PYJeQMSVeCw"
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is active!"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Send a TikTok link and I will download it for you.")

@bot.message_handler(func=lambda message: True)
def download_tiktok(message):
    url = message.text.strip()
    if "tiktok.com" not in url:
        bot.reply_to(message, "Please send a valid TikTok link.")
        return

    msg = bot.reply_to(message, "⏳ Downloading video...")
    
    output_path = "video.mp4"
    
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'best',
    }

    try:
        if os.path.exists(output_path):
            os.remove(output_path)
            
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        with open(output_path, 'rb') as video:
            bot.send_video(message.chat.id, video, reply_to_message_id=message.message_id)
            
        bot.delete_message(message.chat.id, msg.message_id)
        
        if os.path.exists(output_path):
            os.remove(output_path)
            
    except Exception as e:
        bot.edit_message_text(f"Error: {e}", message.chat.id, msg.message_id)
        if os.path.exists(output_path):
            os.remove(output_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
