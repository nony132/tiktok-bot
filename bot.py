import os
import telebot
from flask import Flask, request
import yt_dlp

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Send me a TikTok link.")

@bot.message_handler(func=lambda message: True)
def download_tiktok(message):
    url = message.text.strip()
    if "tiktok.com" not in url:
        bot.reply_to(message, "Please send a valid TikTok link.")
        return

    msg = bot.reply_to(message, "Downloading...")
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_file = ydl.prepare_filename(info)
        
        with open(video_file, 'rb') as vid:
            bot.send_video(message.chat.id, vid)
        
        bot.delete_message(message.chat.id, msg.message_id)
        if os.path.exists(video_file):
            os.remove(video_file)
            
    except Exception as e:
        bot.edit_message_text("Error downloading video.", message.chat.id, msg.message_id)

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
